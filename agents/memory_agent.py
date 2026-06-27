"""
CAMAS Memory Agent
Stores and retrieves query results, energy data, and metrics.
"""

import logging
import sqlite3
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class QueryRecord:
    query_id: str
    run_id: str
    query_text: str
    complexity: float
    priority: float
    memory_req: float
    model_selected: str
    routing_reason: str
    response_text: str
    latency_ms: float
    token_count: int
    timestamp: str

@dataclass
class PerformanceRecord:
    query_id: str
    run_id: str
    mode: str
    latency_ms: float
    energy_kwh: float
    co2_g: float
    cost_usd: float
    model: str
    complexity: float
    timestamp: str


class MemoryAgent:
    """Handles all database persistence for CAMAS."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def store_query(self, record: QueryRecord) -> None:
        self.conn.execute(
            """
            INSERT INTO queries
                (run_id, query_id, query_text, complexity, priority, memory_req,
                 model_selected, routing_reason, response_text, latency_ms, token_count, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.run_id, record.query_id, record.query_text,
                record.complexity, record.priority, record.memory_req,
                record.model_selected, record.routing_reason, record.response_text,
                record.latency_ms, record.token_count, record.timestamp,
            ),
        )
        self.conn.commit()

    def store_energy(
        self, query_id: str, run_id: str,
        total_kwh: float, cpu_kwh: float, gpu_kwh: float, duration_sec: float
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO energy_logs
                (query_id, run_id, total_energy_kwh, cpu_energy_kwh, gpu_energy_kwh,
                 duration_sec, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (query_id, run_id, total_kwh, cpu_kwh, gpu_kwh, duration_sec,
             datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def store_carbon(
        self, query_id: str, run_id: str,
        co2_g: float, intensity: float, energy_kwh: float
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO carbon_logs
                (query_id, run_id, predicted_co2_g, carbon_intensity_g_per_kwh,
                 energy_kwh, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (query_id, run_id, co2_g, intensity, energy_kwh,
             datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def store_routing(
        self, query_id: str, run_id: str,
        complexity: float, model: str, reason: str
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO routing_logs
                (query_id, run_id, complexity, model_selected, routing_reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (query_id, run_id, complexity, model, reason,
             datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def store_performance(self, record: PerformanceRecord) -> None:
        self.conn.execute(
            """
            INSERT INTO performance_logs
                (query_id, run_id, mode, latency_ms, energy_kwh, co2_g,
                 cost_usd, model, complexity, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.query_id, record.run_id, record.mode, record.latency_ms,
                record.energy_kwh, record.co2_g, record.cost_usd, record.model,
                record.complexity, record.timestamp,
            ),
        )
        self.conn.commit()

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get_experiment_summary(self, run_id: str) -> dict:
        rows = self.conn.execute(
            "SELECT * FROM performance_logs WHERE run_id = ?", (run_id,)
        ).fetchall()
        if not rows:
            return {}
        data = [dict(r) for r in rows]
        n = len(data)
        return {
            "run_id": run_id,
            "n_queries": n,
            "avg_latency_ms":   sum(r["latency_ms"] for r in data) / n,
            "total_energy_kwh": sum(r["energy_kwh"] for r in data),
            "total_co2_g":      sum(r["co2_g"] for r in data),
            "total_cost_usd":   sum(r["cost_usd"] for r in data),
            "avg_energy_kwh":   sum(r["energy_kwh"] for r in data) / n,
            "avg_co2_g":        sum(r["co2_g"] for r in data) / n,
            "avg_cost_usd":     sum(r["cost_usd"] for r in data) / n,
        }

    def get_routing_distribution(self, run_id: str) -> dict[str, int]:
        rows = self.conn.execute(
            """
            SELECT model_selected, COUNT(*) as cnt
            FROM routing_logs WHERE run_id = ?
            GROUP BY model_selected
            """,
            (run_id,),
        ).fetchall()
        return {r["model_selected"]: r["cnt"] for r in rows}

    def get_all_performance(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM performance_logs ORDER BY timestamp").fetchall()
        return [dict(r) for r in rows]

    def get_all_routing(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM routing_logs ORDER BY timestamp").fetchall()
        return [dict(r) for r in rows]

    def get_all_energy(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM energy_logs ORDER BY timestamp").fetchall()
        return [dict(r) for r in rows]

    def get_all_carbon(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM carbon_logs ORDER BY timestamp").fetchall()
        return [dict(r) for r in rows]

    def get_sleep_stats(self, run_id: str) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM sleep_logs WHERE run_id = ? ORDER BY timestamp", (run_id,)
        ).fetchall()
        return [dict(r) for r in rows]
