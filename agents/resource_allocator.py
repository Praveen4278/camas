"""
CAMAS Resource Allocation Agent
Allocates CPU, GPU, and RAM based on task complexity.
"""

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass
class ResourceAllocation:
    complexity_band: str   # "low" | "medium" | "high"
    cpu_cores: int
    gpu_memory_gb: float
    ram_gb: float
    complexity: float


_PROFILES = {
    "low":    {"cpu_cores": 2,  "gpu_memory_gb": 1.0,  "ram_gb": 2.0},
    "medium": {"cpu_cores": 4,  "gpu_memory_gb": 4.0,  "ram_gb": 8.0},
    "high":   {"cpu_cores": 8,  "gpu_memory_gb": 8.0,  "ram_gb": 16.0},
}


def allocate_resources(
    complexity: float,
    simple_threshold: float = 3.0,
    medium_threshold: float = 7.0,
    custom_profiles: dict | None = None,
) -> ResourceAllocation:
    """
    Allocate compute resources proportional to task complexity.
    """
    profiles = custom_profiles or _PROFILES

    if complexity < simple_threshold:
        band = "low"
    elif complexity < medium_threshold:
        band = "medium"
    else:
        band = "high"

    profile = profiles[band]
    alloc = ResourceAllocation(
        complexity_band=band,
        cpu_cores=profile["cpu_cores"],
        gpu_memory_gb=profile["gpu_memory_gb"],
        ram_gb=profile["ram_gb"],
        complexity=complexity,
    )
    logger.debug(
        f"ResourceAllocator → band={band}, CPU={alloc.cpu_cores}, "
        f"GPU={alloc.gpu_memory_gb}GB, RAM={alloc.ram_gb}GB"
    )
    return alloc


def log_allocation(
    conn: sqlite3.Connection,
    query_id: str,
    run_id: str,
    alloc: ResourceAllocation,
) -> None:
    """Persist allocation to database."""
    conn.execute(
        """
        INSERT INTO resource_logs
            (query_id, run_id, complexity_band, cpu_cores, gpu_memory_gb, ram_gb, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            query_id, run_id,
            alloc.complexity_band, alloc.cpu_cores,
            alloc.gpu_memory_gb, alloc.ram_gb,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
