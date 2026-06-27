"""
CAMAS Experiment Runner
Executes baseline and CAMAS experiments over the prompt dataset.
"""

import json
import uuid
import time
import logging
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Literal

from database.schema import get_connection, initialize_database
from agents.memory_agent import MemoryAgent
from agents.power_manager import PowerManagedAgent
from agents.energy_monitor import idle_energy_kwh
from experiments.orchestrator import run_single_query

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_prompts(prompts_path: str) -> list[dict]:
    with open(prompts_path) as f:
        data = json.load(f)
    return data["prompts"]


def run_experiment(
    mode: Literal["baseline", "camas"],
    config: dict,
    prompts: list[dict],
    max_queries: int | None = None,
    progress_callback=None,
    ablation: str | None = None,   # "no_routing" | "no_sleep"
) -> str:
    """
    Run a full experiment in the given mode.
    Returns the run_id.
    """
    run_id = f"{mode}_{uuid.uuid4().hex[:8]}"
    db_path = config["experiment"]["database_path"]

    initialize_database(db_path)
    conn = get_connection(db_path)
    memory_agent = MemoryAgent(conn)

    # Register experiment
    start_time = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT INTO experiments (run_id, mode, start_time, config_json)
        VALUES (?, ?, ?, ?)
        """,
        (run_id, mode, start_time, json.dumps(config)),
    )
    conn.commit()

    # Power management for key agents
    power_mgr = PowerManagedAgent(
        agent_name="orchestrator",
        idle_threshold_seconds=config["power_management"]["idle_threshold_seconds"],
        db_conn=conn,
        run_id=run_id,
    )

    # Adjust config for mode
    run_config = dict(config)
    run_config["energy"]["mock_mode"] = True
    if mode == "baseline":
        run_config["experiment"]["baseline_mode"] = True
    if ablation == "no_routing":
        # Force every query to the heavy model — routing disabled
        run_config["ollama"] = dict(run_config["ollama"])
        run_config["ollama"]["models"] = {
            **run_config["ollama"]["models"], "simple": "llama3.2:8b", "medium": "llama3.2:8b"
        }
    if ablation == "no_sleep":
        # Remove inter-batch pauses so power manager never sleeps
        run_config["power_management"] = dict(run_config["power_management"])
        run_config["power_management"]["inter_batch_sleep_seconds"] = 0

    subset = prompts[:max_queries] if max_queries else prompts
    total = len(subset)
    batch_size = 20  # sleep pause after every N queries
    inter_batch_sleep = run_config["power_management"].get("inter_batch_sleep_seconds", 12)
    sleep_enabled = ablation != "no_sleep" and mode != "baseline"

    # Idle energy spreads across queries in a batch (batch_size queries share one pause)
    # Pre-compute idle energy per query for this condition
    def _idle_energy_per_query(model: str) -> float:
        """Idle energy attributed to one query based on sleep state during inter-batch pause."""
        if inter_batch_sleep <= 0 or total <= batch_size:
            return 0.0
        num_pauses = max(0, (total - 1) // batch_size)
        total_idle_sec = num_pauses * inter_batch_sleep
        avg_idle_per_query = total_idle_sec / total
        return idle_energy_kwh(model, avg_idle_per_query, sleeping=sleep_enabled)

    logger.info(f"Starting experiment: mode={mode}, run_id={run_id}, queries={total}, sleep_enabled={sleep_enabled}")

    for i, prompt in enumerate(subset):
        # Insert idle pause between batches so power manager transitions to SLEEP
        if i > 0 and i % batch_size == 0 and inter_batch_sleep > 0:
            logger.info(f"  [batch pause] sleeping {inter_batch_sleep}s to allow sleep-state transition...")
            power_mgr.notify_task_end()
            time.sleep(inter_batch_sleep)
            power_mgr.flush_pending_db_logs()

        power_mgr.notify_task_start()
        try:
            final_state = run_single_query(
                query=prompt["text"],
                run_id=run_id,
                mode=mode,
                config=run_config,
                memory_agent=memory_agent,
                db_conn=conn,
                idle_energy_kwh_addend=_idle_energy_per_query,
            )
            if progress_callback:
                progress_callback(i + 1, total, final_state)
            else:
                pct = (i + 1) / total * 100
                model = final_state.get("model", "?")
                energy = final_state.get("total_energy_kwh", 0)
                logger.info(
                    f"  [{pct:5.1f}%] Query {i+1}/{total} | model={model} | "
                    f"energy={energy:.6f} kWh"
                )
        except Exception as exc:
            logger.error(f"Query {i+1} failed: {exc}")
        finally:
            power_mgr.notify_task_end()

    # Finalise experiment record
    end_time = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "UPDATE experiments SET end_time=?, total_queries=? WHERE run_id=?",
        (end_time, total, run_id),
    )
    conn.commit()

    stats = power_mgr.shutdown()
    power_mgr.flush_pending_db_logs()
    logger.info(
        f"Experiment {run_id} complete | active={stats.total_active_sec:.1f}s "
        f"sleep={stats.total_sleep_sec:.1f}s wakeups={stats.num_wakeups}"
    )

    conn.close()
    return run_id
