"""
CAMAS Database Schema and Initialization
SQLite-based storage for research metrics
"""

import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_connection(db_path: str) -> sqlite3.Connection:
    """Get a database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize_database(db_path: str) -> None:
    """Create all tables if they don't exist."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        -- Experiments table: tracks each experimental run
        CREATE TABLE IF NOT EXISTS experiments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id      TEXT NOT NULL UNIQUE,
            mode        TEXT NOT NULL CHECK(mode IN ('baseline','camas')),
            start_time  TEXT NOT NULL,
            end_time    TEXT,
            total_queries INTEGER DEFAULT 0,
            config_json TEXT,
            notes       TEXT
        );

        -- Queries table: one row per query execution
        CREATE TABLE IF NOT EXISTS queries (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id          TEXT NOT NULL,
            query_id        TEXT NOT NULL,
            query_text      TEXT NOT NULL,
            complexity      REAL,
            priority        REAL,
            memory_req      REAL,
            model_selected  TEXT,
            routing_reason  TEXT,
            response_text   TEXT,
            latency_ms      REAL,
            token_count     INTEGER,
            timestamp       TEXT NOT NULL,
            FOREIGN KEY(run_id) REFERENCES experiments(run_id)
        );

        -- Energy logs: per-query energy measurements
        CREATE TABLE IF NOT EXISTS energy_logs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id        TEXT NOT NULL,
            run_id          TEXT NOT NULL,
            total_energy_kwh REAL,
            cpu_energy_kwh  REAL,
            gpu_energy_kwh  REAL,
            duration_sec    REAL,
            timestamp       TEXT NOT NULL
        );

        -- Carbon logs: per-query CO2 estimates
        CREATE TABLE IF NOT EXISTS carbon_logs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id        TEXT NOT NULL,
            run_id          TEXT NOT NULL,
            predicted_co2_g REAL,
            carbon_intensity_g_per_kwh REAL,
            energy_kwh      REAL,
            timestamp       TEXT NOT NULL
        );

        -- Routing logs: routing decisions
        CREATE TABLE IF NOT EXISTS routing_logs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id        TEXT NOT NULL,
            run_id          TEXT NOT NULL,
            complexity      REAL,
            model_selected  TEXT,
            routing_reason  TEXT,
            timestamp       TEXT NOT NULL
        );

        -- Sleep logs: power management state transitions
        CREATE TABLE IF NOT EXISTS sleep_logs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name      TEXT NOT NULL,
            run_id          TEXT NOT NULL,
            state           TEXT NOT NULL CHECK(state IN ('ACTIVE','SLEEP','WAKEUP')),
            duration_sec    REAL,
            timestamp       TEXT NOT NULL
        );

        -- Performance logs: aggregated per-query performance
        CREATE TABLE IF NOT EXISTS performance_logs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id        TEXT NOT NULL,
            run_id          TEXT NOT NULL,
            mode            TEXT NOT NULL,
            latency_ms      REAL,
            energy_kwh      REAL,
            co2_g           REAL,
            cost_usd        REAL,
            model           TEXT,
            complexity      REAL,
            timestamp       TEXT NOT NULL
        );

        -- Resource allocation logs
        CREATE TABLE IF NOT EXISTS resource_logs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id        TEXT NOT NULL,
            run_id          TEXT NOT NULL,
            complexity_band TEXT,
            cpu_cores       INTEGER,
            gpu_memory_gb   REAL,
            ram_gb          REAL,
            timestamp       TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {db_path}")
