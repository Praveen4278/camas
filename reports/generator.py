"""
CAMAS Report Generator
Generates CSV reports and LaTeX/text research tables.
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_connection

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates all research output files for CAMAS experiments."""

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "reports"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_conn(self):
        return get_connection()

    def generate_results_csv(self, experiment_ids: list = None) -> str:
        """Generate main results.csv with per-query metrics."""
        filepath = self.output_dir / "results.csv"
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            where = ""
            params = ()
            if experiment_ids:
                placeholders = ",".join("?" * len(experiment_ids))
                where = f"WHERE q.experiment_id IN ({placeholders})"
                params = tuple(experiment_ids)

            cursor.execute(f"""
                SELECT 
                    q.experiment_id,
                    q.query_id,
                    q.mode,
                    q.complexity_score,
                    q.priority_score,
                    q.memory_requirement,
                    r.selected_model,
                    r.routing_reason,
                    r.complexity_score as routed_complexity,
                    e.total_energy_kwh,
                    e.cpu_energy_kwh,
                    e.gpu_energy_kwh,
                    e.duration_seconds,
                    c.predicted_co2_kg,
                    c.carbon_intensity_kg_per_kwh,
                    p.latency_ms,
                    p.total_tokens,
                    p.cost_usd,
                    p.throughput_tokens_per_sec
                FROM queries q
                LEFT JOIN routing_logs r ON q.query_id = r.query_id
                LEFT JOIN energy_logs e ON q.query_id = e.query_id
                LEFT JOIN carbon_logs c ON q.query_id = c.query_id
                LEFT JOIN performance_logs p ON q.query_id = p.query_id
                {where}
                ORDER BY q.experiment_id, q.timestamp
            """, params)

            cols = [d[0] for d in cursor.description]
            rows = cursor.fetchall()

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                writer.writerows(rows)

            logger.info(f"[Report] results.csv → {filepath} ({len(rows)} rows)")
            return str(filepath)
        finally:
            conn.close()

    def generate_metrics_csv(self, experiment_ids: list = None) -> str:
        """Generate aggregated metrics.csv per experiment."""
        filepath = self.output_dir / "metrics.csv"
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            where = ""
            params = ()
            if experiment_ids:
                placeholders = ",".join("?" * len(experiment_ids))
                where = f"WHERE q.experiment_id IN ({placeholders})"
                params = tuple(experiment_ids)

            cursor.execute(f"""
                SELECT 
                    q.experiment_id,
                    q.mode,
                    COUNT(DISTINCT q.query_id) as total_queries,
                    AVG(q.complexity_score) as avg_complexity,
                    AVG(e.total_energy_kwh) as avg_energy_kwh,
                    SUM(e.total_energy_kwh) as total_energy_kwh,
                    AVG(c.predicted_co2_kg) as avg_co2_kg,
                    SUM(c.predicted_co2_kg) as total_co2_kg,
                    AVG(p.latency_ms) as avg_latency_ms,
                    MIN(p.latency_ms) as min_latency_ms,
                    MAX(p.latency_ms) as max_latency_ms,
                    AVG(p.cost_usd) as avg_cost_usd,
                    SUM(p.cost_usd) as total_cost_usd,
                    SUM(p.total_tokens) as total_tokens,
                    AVG(p.throughput_tokens_per_sec) as avg_throughput
                FROM queries q
                LEFT JOIN energy_logs e ON q.query_id = e.query_id
                LEFT JOIN carbon_logs c ON q.query_id = c.query_id
                LEFT JOIN performance_logs p ON q.query_id = p.query_id
                {where}
                GROUP BY q.experiment_id, q.mode
                ORDER BY q.experiment_id
            """, params)

            cols = [d[0] for d in cursor.description]
            rows = cursor.fetchall()

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                writer.writerows(rows)

            logger.info(f"[Report] metrics.csv → {filepath}")
            return str(filepath)
        finally:
            conn.close()

    def generate_routing_csv(self, experiment_ids: list = None) -> str:
        """Generate routing.csv with model distribution."""
        filepath = self.output_dir / "routing.csv"
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            where = ""
            params = ()
            if experiment_ids:
                placeholders = ",".join("?" * len(experiment_ids))
                where = f"WHERE experiment_id IN ({placeholders})"
                params = tuple(experiment_ids)

            cursor.execute(f"""
                SELECT 
                    experiment_id,
                    selected_model,
                    COUNT(*) as query_count,
                    AVG(complexity_score) as avg_complexity,
                    MIN(complexity_score) as min_complexity,
                    MAX(complexity_score) as max_complexity,
                    AVG(routing_latency_ms) as avg_routing_latency_ms
                FROM routing_logs
                {where}
                GROUP BY experiment_id, selected_model
                ORDER BY experiment_id, selected_model
            """, params)

            cols = [d[0] for d in cursor.description]
            rows = cursor.fetchall()

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                writer.writerows(rows)

            logger.info(f"[Report] routing.csv → {filepath}")
            return str(filepath)
        finally:
            conn.close()

    def generate_carbon_csv(self, experiment_ids: list = None) -> str:
        """Generate carbon.csv with CO2 metrics."""
        filepath = self.output_dir / "carbon.csv"
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            where = ""
            params = ()
            if experiment_ids:
                placeholders = ",".join("?" * len(experiment_ids))
                where = f"WHERE experiment_id IN ({placeholders})"
                params = tuple(experiment_ids)

            cursor.execute(f"""
                SELECT *
                FROM carbon_logs
                {where}
                ORDER BY experiment_id, timestamp
            """, params)

            cols = [d[0] for d in cursor.description]
            rows = cursor.fetchall()

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                writer.writerows(rows)

            logger.info(f"[Report] carbon.csv → {filepath}")
            return str(filepath)
        finally:
            conn.close()

    def generate_energy_csv(self, experiment_ids: list = None) -> str:
        """Generate energy.csv with energy metrics."""
        filepath = self.output_dir / "energy.csv"
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            where = ""
            params = ()
            if experiment_ids:
                placeholders = ",".join("?" * len(experiment_ids))
                where = f"WHERE experiment_id IN ({placeholders})"
                params = tuple(experiment_ids)

            cursor.execute(f"""
                SELECT *
                FROM energy_logs
                {where}
                ORDER BY experiment_id, timestamp
            """, params)

            cols = [d[0] for d in cursor.description]
            rows = cursor.fetchall()

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                writer.writerows(rows)

            logger.info(f"[Report] energy.csv → {filepath}")
            return str(filepath)
        finally:
            conn.close()

    def generate_research_tables(
        self,
        baseline_id: str,
        camas_id: str
    ) -> str:
        """
        Generate Table 1, 2, 3 as formatted text for inclusion in papers.
        """
        filepath = self.output_dir / "research_tables.txt"
        conn = self._get_conn()

        try:
            cursor = conn.cursor()

            def get_metrics(eid):
                cursor.execute("""
                    SELECT 
                        COUNT(DISTINCT q.query_id) as n,
                        AVG(q.complexity_score) as avg_cx,
                        AVG(e.total_energy_kwh) as avg_e,
                        SUM(e.total_energy_kwh) as sum_e,
                        AVG(c.predicted_co2_kg) as avg_co2,
                        SUM(c.predicted_co2_kg) as sum_co2,
                        AVG(p.latency_ms) as avg_lat,
                        AVG(p.cost_usd) as avg_cost,
                        SUM(p.cost_usd) as sum_cost
                    FROM queries q
                    LEFT JOIN energy_logs e ON q.query_id = e.query_id
                    LEFT JOIN carbon_logs c ON q.query_id = c.query_id
                    LEFT JOIN performance_logs p ON q.query_id = p.query_id
                    WHERE q.experiment_id = ?
                """, (eid,))
                row = cursor.fetchone()
                cols = [d[0] for d in cursor.description]
                return dict(zip(cols, row)) if row else {}

            bm = get_metrics(baseline_id)
            cm = get_metrics(camas_id)

            def pct_change(b, c):
                if b and b != 0:
                    return ((c - b) / b) * 100
                return 0

            energy_reduction = pct_change(
                bm.get("sum_e", 1), cm.get("sum_e", 1)
            )
            carbon_reduction = pct_change(
                bm.get("sum_co2", 1), cm.get("sum_co2", 1)
            )
            cost_reduction = pct_change(
                bm.get("sum_cost", 1), cm.get("sum_cost", 1)
            )
            latency_change = pct_change(
                bm.get("avg_lat", 1), cm.get("avg_lat", 1)
            )

            # Get routing distribution
            cursor.execute("""
                SELECT selected_model, COUNT(*) as n
                FROM routing_logs WHERE experiment_id=?
                GROUP BY selected_model
            """, (camas_id,))
            routing_dist = cursor.fetchall()

            # Sleep stats
            cursor.execute("""
                SELECT state, SUM(duration_seconds) as total_secs
                FROM sleep_logs WHERE experiment_id=?
                GROUP BY state
            """, (camas_id,))
            sleep_rows = dict(cursor.fetchall())

            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

            tables = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           CAMAS Research Results — Generated {now}           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Baseline ID : {baseline_id:<58} ║
║  CAMAS ID    : {camas_id:<58} ║
╚══════════════════════════════════════════════════════════════════════════════╝

TABLE 1: Experimental Results Summary
══════════════════════════════════════════════════════════════════════════════
Metric                    │ Baseline (llama3.2:8b)   │ CAMAS (Dynamic)    │ Δ%
──────────────────────────┼──────────────────────────┼────────────────────┼──────────
Queries Executed          │ {bm.get('n', 0):<25}│ {cm.get('n', 0):<19}│  —
Avg. Complexity           │ {bm.get('avg_cx', 0):<25.4f}│ {cm.get('avg_cx', 0):<19.4f}│  —
Avg. Latency (ms)         │ {bm.get('avg_lat', 0):<25.2f}│ {cm.get('avg_lat', 0):<19.2f}│ {latency_change:+.1f}%
Total Energy (kWh)        │ {bm.get('sum_e', 0):<25.6f}│ {cm.get('sum_e', 0):<19.6f}│ {energy_reduction:+.1f}%
Avg. Energy/Query (kWh)   │ {bm.get('avg_e', 0):<25.8f}│ {cm.get('avg_e', 0):<19.8f}│ {energy_reduction:+.1f}%
Total CO₂ (kg)            │ {bm.get('sum_co2', 0):<25.8f}│ {cm.get('sum_co2', 0):<19.8f}│ {carbon_reduction:+.1f}%
Avg. CO₂/Query (kg)       │ {bm.get('avg_co2', 0):<25.8f}│ {cm.get('avg_co2', 0):<19.8f}│ {carbon_reduction:+.1f}%
Total Cost (USD)          │ {bm.get('sum_cost', 0):<25.6f}│ {cm.get('sum_cost', 0):<19.6f}│ {cost_reduction:+.1f}%
Avg. Cost/Query (USD)     │ {bm.get('avg_cost', 0):<25.6f}│ {cm.get('avg_cost', 0):<19.6f}│ {cost_reduction:+.1f}%
══════════════════════════════════════════════════════════════════════════════
H1 (Energy): {"SUPPORTED" if energy_reduction < -5 else "PARTIAL" if energy_reduction < 0 else "NOT SUPPORTED"}
H2 (Carbon): {"SUPPORTED" if carbon_reduction < -5 else "PARTIAL" if carbon_reduction < 0 else "NOT SUPPORTED"}
H3 (Cost):   {"SUPPORTED" if cost_reduction < -5 else "PARTIAL" if cost_reduction < 0 else "NOT SUPPORTED"}


TABLE 2: CAMAS Routing Statistics
══════════════════════════════════════════════════════════════════════════════
Model               │ Queries Routed │ % of Total
────────────────────┼────────────────┼───────────────────
"""
            total_routed = sum(n for _, n in routing_dist)
            for model, n in routing_dist:
                pct = n / total_routed * 100 if total_routed else 0
                tables += f"{model:<19} │ {n:<14} │ {pct:.1f}%\n"

            tables += f"""────────────────────┴────────────────┴───────────────────
Total               │ {total_routed:<14} │ 100%
══════════════════════════════════════════════════════════════════════════════


TABLE 3: Energy and Carbon Metrics Detail
══════════════════════════════════════════════════════════════════════════════
                          │ Baseline                 │ CAMAS
──────────────────────────┼──────────────────────────┼───────────────────────
Avg CPU Energy (kWh)      │ (see energy.csv)         │ (see energy.csv)
Avg GPU Energy (kWh)      │ (see energy.csv)         │ (see energy.csv)
Carbon Intensity (kg/kWh) │ 0.2330                   │ 0.2330
Energy Reduction          │ —                        │ {abs(energy_reduction):.2f}%
Carbon Reduction          │ —                        │ {abs(carbon_reduction):.2f}%
Sleep State Active        │ Not Implemented          │ {sleep_rows.get('SLEEP', 0):.1f}s total sleep
Sleep Wakeups             │ —                        │ (see sleep_logs table)
══════════════════════════════════════════════════════════════════════════════
"""

            with open(filepath, "w") as f:
                f.write(tables)

            logger.info(f"[Report] research_tables.txt → {filepath}")
            return str(filepath)

        finally:
            conn.close()

    def generate_all(self, baseline_id: str, camas_id: str):
        """Generate all reports."""
        ids = [baseline_id, camas_id]
        files = {
            "results": self.generate_results_csv(ids),
            "metrics": self.generate_metrics_csv(ids),
            "routing": self.generate_routing_csv(ids),
            "carbon": self.generate_carbon_csv(ids),
            "energy": self.generate_energy_csv(ids),
            "tables": self.generate_research_tables(baseline_id, camas_id)
        }
        logger.info(f"[Report] All reports generated: {list(files.keys())}")
        return files
