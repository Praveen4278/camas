"""
CAMAS FastAPI Application
REST API for experiment management and result retrieval.
"""

import json
import logging
import yaml
from pathlib import Path
from typing import Literal, Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from database.schema import get_connection, initialize_database
from agents.memory_agent import MemoryAgent
from experiments.runner import load_config, load_prompts, run_experiment
from experiments.reporter import (
    export_performance_csv, export_routing_csv, export_energy_csv,
    export_carbon_csv, export_metrics_csv, generate_research_tables,
    generate_visualizations,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CAMAS API",
    description="Carbon-Aware Multi-Agent System – Research API",
    version="1.0.0",
)

CONFIG_PATH = "config/config.yaml"
_config = None


def get_config() -> dict:
    global _config
    if _config is None:
        _config = load_config(CONFIG_PATH)
    return _config


def get_db():
    cfg = get_config()
    initialize_database(cfg["experiment"]["database_path"])
    return get_connection(cfg["experiment"]["database_path"])


# ---------------------------------------------------------------------------
# Request/Response Models
# ---------------------------------------------------------------------------

class SingleQueryRequest(BaseModel):
    query: str
    mode: Literal["baseline", "camas"] = "camas"

class ExperimentRequest(BaseModel):
    mode: Literal["baseline", "camas"]
    max_queries: Optional[int] = None

class ExperimentResponse(BaseModel):
    run_id: str
    mode: str
    status: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "system": "CAMAS – Carbon-Aware Multi-Agent System",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", summary="Run a single query")
async def single_query(req: SingleQueryRequest):
    """Execute a single query through the CAMAS pipeline."""
    from experiments.orchestrator import run_single_query
    cfg = get_config()
    conn = get_db()
    ma = MemoryAgent(conn)
    import uuid
    run_id = f"api_{uuid.uuid4().hex[:6]}"

    final = run_single_query(
        query=req.query,
        run_id=run_id,
        mode=req.mode,
        config=cfg,
        memory_agent=ma,
        db_conn=conn,
    )
    conn.close()
    return {
        "query": req.query,
        "mode": req.mode,
        "model": final.get("model"),
        "complexity": final.get("complexity"),
        "response": final.get("response"),
        "latency_ms": final.get("latency_ms"),
        "energy_kwh": final.get("total_energy_kwh"),
        "co2_g": final.get("co2_g"),
        "cost_usd": final.get("cost_usd"),
        "routing_reason": final.get("routing_reason"),
    }


@app.post("/experiment/run", response_model=ExperimentResponse)
async def start_experiment(req: ExperimentRequest, background_tasks: BackgroundTasks):
    """Start an experiment asynchronously."""
    cfg = get_config()
    prompts = load_prompts(cfg["experiment"]["prompts_file"])

    import uuid
    run_id = f"{req.mode}_{uuid.uuid4().hex[:8]}"

    def _run():
        run_experiment(
            mode=req.mode,
            config=cfg,
            prompts=prompts,
            max_queries=req.max_queries,
        )

    background_tasks.add_task(_run)
    return ExperimentResponse(run_id=run_id, mode=req.mode, status="started")


@app.get("/experiment/{run_id}/summary")
def experiment_summary(run_id: str):
    """Get summary metrics for a completed experiment."""
    conn = get_db()
    ma = MemoryAgent(conn)
    summary = ma.get_experiment_summary(run_id)
    conn.close()
    if not summary:
        raise HTTPException(404, f"No data found for run_id={run_id}")
    return summary


@app.get("/experiments")
def list_experiments():
    """List all recorded experiments."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM experiments ORDER BY start_time DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/routing/{run_id}")
def routing_distribution(run_id: str):
    conn = get_db()
    ma = MemoryAgent(conn)
    dist = ma.get_routing_distribution(run_id)
    conn.close()
    return dist


@app.post("/reports/generate")
async def generate_reports():
    """Generate all CSV reports and visualizations from stored data."""
    cfg = get_config()
    conn = get_db()
    ma = MemoryAgent(conn)

    out_dir = Path(cfg["experiment"]["results_dir"])
    viz_dir = Path(cfg["experiment"]["visualization_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    viz_dir.mkdir(parents=True, exist_ok=True)

    all_perf    = ma.get_all_performance()
    all_routing = ma.get_all_routing()
    all_energy  = ma.get_all_energy()
    all_carbon  = ma.get_all_carbon()

    # Compute summaries per mode
    summaries = {}
    for mode in ["baseline", "camas"]:
        rows = [r for r in all_perf if r["mode"] == mode]
        if rows:
            n = len(rows)
            summaries[mode] = {
                "n_queries":      n,
                "avg_latency_ms": sum(r["latency_ms"] for r in rows) / n,
                "total_energy_kwh": sum(r["energy_kwh"] for r in rows),
                "avg_energy_kwh": sum(r["energy_kwh"] for r in rows) / n,
                "total_co2_g":    sum(r["co2_g"] for r in rows),
                "avg_co2_g":      sum(r["co2_g"] for r in rows) / n,
                "total_cost_usd": sum(r["cost_usd"] for r in rows),
                "avg_cost_usd":   sum(r["cost_usd"] for r in rows) / n,
            }

    # Routing distribution for CAMAS
    camas_routing_rows = [r for r in all_routing if "baseline" not in r.get("run_id", "")]
    routing_dist = {}
    for r in camas_routing_rows:
        m = r["model_selected"]
        routing_dist[m] = routing_dist.get(m, 0) + 1

    # Sleep logs
    sleep_logs = conn.execute("SELECT * FROM sleep_logs").fetchall()
    sleep_logs = [dict(r) for r in sleep_logs]

    export_performance_csv(all_perf, out_dir)
    export_routing_csv(all_routing, out_dir)
    export_energy_csv(all_energy, out_dir)
    export_carbon_csv(all_carbon, out_dir)
    export_metrics_csv(summaries, out_dir)
    generate_research_tables(summaries, routing_dist, out_dir)
    saved_figs = generate_visualizations(summaries, all_perf, routing_dist, sleep_logs, viz_dir)

    conn.close()
    return {
        "status": "generated",
        "csv_files": ["results.csv","routing.csv","energy.csv","carbon.csv","metrics.csv"],
        "tables": "research_tables.md",
        "figures": [str(p) for p in saved_figs],
    }


@app.get("/config")
def show_config():
    return get_config()
