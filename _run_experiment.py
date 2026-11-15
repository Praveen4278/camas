"""
CAMAS Experiment CLI
Run both baseline and CAMAS experiments and generate full reports.

Usage:
    python run_experiment.py                    # full 100-query experiment
    python run_experiment.py --max-queries 10   # quick smoke test
    python run_experiment.py --mode camas       # only CAMAS mode
"""

import sys
import logging
import argparse
from pathlib import Path

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("camas.log", mode="a"),
    ],
    force=True,
)
logger = logging.getLogger("camas.cli")


def main():
    parser = argparse.ArgumentParser(description="CAMAS Experiment Runner")
    parser.add_argument("--config",      default="config/config.yaml")
    parser.add_argument("--max-queries", type=int, default=None,
                        help="Limit number of queries per mode (default: all 100)")
    parser.add_argument("--mode",        choices=["baseline","camas","both"], default="both")
    parser.add_argument("--no-reports",  action="store_true")
    parser.add_argument("--ablation",    action="store_true",
                        help="Run ablation study (full CAMAS vs no-routing vs no-sleep)")
    parser.add_argument("--scalability", action="store_true",
                        help="Run scalability sweep (25/50/75/100 queries)")
    args = parser.parse_args()

    # Load config
    with open(args.config) as f:
        config = yaml.safe_load(f)

    # Ensure output dirs exist
    Path(config["experiment"]["results_dir"]).mkdir(parents=True, exist_ok=True)
    Path(config["experiment"]["visualization_dir"]).mkdir(parents=True, exist_ok=True)
    Path(config["experiment"]["database_path"]).parent.mkdir(parents=True, exist_ok=True)

    from experiments.runner import load_prompts, run_experiment
    prompts = load_prompts(config["experiment"]["prompts_file"])

    run_ids = {}
    modes = []
    if args.mode in ("both", "baseline"):
        modes.append("baseline")
    if args.mode in ("both", "camas"):
        modes.append("camas")

    for mode in modes:
        logger.info(f"{'='*60}")
        logger.info(f"Starting {mode.upper()} experiment")
        logger.info(f"{'='*60}")
        run_id = run_experiment(
            mode=mode, config=config, prompts=prompts,
            max_queries=args.max_queries,
        )
        run_ids[mode] = run_id
        logger.info(f"Completed {mode.upper()} → run_id={run_id}")

    if not args.no_reports and modes:
        logger.info("Generating reports and visualizations…")
        _generate_reports(config, run_ids)

    if args.ablation:
        logger.info("Running ablation study…")
        _run_ablation(config, prompts, args.max_queries)

    if args.scalability:
        logger.info("Running scalability sweep…")
        _run_scalability(config, prompts)

    logger.info("Done. Results in:")
    logger.info(f"  Reports:        {config['experiment']['results_dir']}/")
    logger.info(f"  Visualizations: {config['experiment']['visualization_dir']}/")
    logger.info(f"  Database:       {config['experiment']['database_path']}")


def _generate_reports(config: dict, run_ids: dict) -> None:
    from pathlib import Path
    from database.schema import get_connection
    from agents.memory_agent import MemoryAgent
    from experiments.reporter import (
        export_performance_csv, export_routing_csv, export_energy_csv,
        export_carbon_csv, export_metrics_csv, generate_research_tables,
        generate_visualizations,
    )

    conn = get_connection(config["experiment"]["database_path"])
    ma   = MemoryAgent(conn)

    out_dir = Path(config["experiment"]["results_dir"])
    viz_dir = Path(config["experiment"]["visualization_dir"])

    all_perf    = [r for r in ma.get_all_performance()
                   if r["run_id"] in set(run_ids.values())]
    all_routing = [r for r in ma.get_all_routing()
                   if r["run_id"] in set(run_ids.values())]
    all_energy  = [r for r in ma.get_all_energy()
                   if r["run_id"] in set(run_ids.values())]
    all_carbon  = [r for r in ma.get_all_carbon()
                   if r["run_id"] in set(run_ids.values())]

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

    camas_run_id = run_ids.get("camas", "")
    routing_dist = ma.get_routing_distribution(camas_run_id) if camas_run_id else {}

    sleep_rows = conn.execute("SELECT * FROM sleep_logs").fetchall()
    sleep_logs = [dict(r) for r in sleep_rows]

    export_performance_csv(all_perf, out_dir)
    export_routing_csv(all_routing, out_dir)
    export_energy_csv(all_energy, out_dir)
    export_carbon_csv(all_carbon, out_dir)
    export_metrics_csv(summaries, out_dir)
    generate_research_tables(summaries, routing_dist, out_dir, all_perf=all_perf)
    generate_visualizations(summaries, all_perf, routing_dist, sleep_logs, viz_dir)

    conn.close()
    logger.info("Reports generated successfully.")


def _run_ablation(config: dict, prompts: list, max_queries: int | None) -> None:
    from experiments.runner import run_experiment
    from database.schema import get_connection
    from agents.memory_agent import MemoryAgent
    from experiments.reporter import generate_ablation_tables

    # Use a fast config: no inter-batch sleep, cap at 50 queries per condition
    fast_config = dict(config)
    fast_config["power_management"] = {
        **config["power_management"],
        "inter_batch_sleep_seconds": 0,
    }
    n_queries = min(max_queries or 50, 50)

    conditions = [
        ("baseline", None),
        ("camas",    "no_routing"),
        ("camas",    "no_sleep"),
        ("camas",    None),
    ]
    keys = ["baseline", "no_routing", "no_sleep", "full_camas"]
    ablation_results = {}

    for (mode, ablation), key in zip(conditions, keys):
        logger.info(f"  Ablation: running {key} ({n_queries} queries)...")
        run_id = run_experiment(
            mode=mode, config=fast_config, prompts=prompts,
            max_queries=n_queries, ablation=ablation,
        )
        conn = get_connection(config["experiment"]["database_path"])
        ma   = MemoryAgent(conn)
        rows = [r for r in ma.get_all_performance() if r["run_id"] == run_id]
        conn.close()
        if rows:
            n = len(rows)
            ablation_results[key] = {
                "avg_latency_ms":   sum(r["latency_ms"]  for r in rows) / n,
                "total_energy_kwh": sum(r["energy_kwh"]  for r in rows),
                "total_co2_g":      sum(r["co2_g"]        for r in rows),
                "total_cost_usd":   sum(r["cost_usd"]     for r in rows),
            }
        logger.info(f"  Ablation: {key} done.")

    out_dir = Path(config["experiment"]["results_dir"])
    generate_ablation_tables(ablation_results, out_dir)
    logger.info(f"Ablation table saved to {out_dir}/ablation_study.md")


def _run_scalability(config: dict, prompts: list) -> None:
    from experiments.runner import run_experiment
    from database.schema import get_connection
    from agents.memory_agent import MemoryAgent
    from experiments.reporter import generate_scalability_table

    # No inter-batch sleep for scalability runs
    fast_config = dict(config)
    fast_config["power_management"] = {
        **config["power_management"],
        "inter_batch_sleep_seconds": 0,
    }

    sizes = [10, 25, 50, 100]
    scale_results = []

    for n in sizes:
        logger.info(f"  Scalability: running CAMAS with {n} queries...")
        run_id = run_experiment(
            mode="camas", config=fast_config, prompts=prompts, max_queries=n,
        )
        conn = get_connection(config["experiment"]["database_path"])
        ma   = MemoryAgent(conn)
        rows = [r for r in ma.get_all_performance() if r["run_id"] == run_id]
        conn.close()
        if rows:
            scale_results.append({
                "n_queries":        len(rows),
                "avg_latency_ms":   sum(r["latency_ms"]  for r in rows) / len(rows),
                "total_energy_kwh": sum(r["energy_kwh"]  for r in rows),
                "total_co2_g":      sum(r["co2_g"]        for r in rows),
                "total_cost_usd":   sum(r["cost_usd"]     for r in rows),
            })
        logger.info(f"  Scalability: {n} queries done.")

    out_dir = Path(config["experiment"]["results_dir"])
    generate_scalability_table(scale_results, out_dir)
    logger.info(f"Scalability table saved to {out_dir}/scalability.md")
