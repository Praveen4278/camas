"""
CAMAS Energy Monitor Agent
Measures energy consumption using CodeCarbon with mock fallback.

Formula: E = ∫ P(t) dt
"""

import time
import logging
import contextlib
from dataclasses import dataclass, field
from typing import Generator

logger = logging.getLogger(__name__)


@dataclass
class EnergyMeasurement:
    total_energy_kwh: float
    cpu_energy_kwh: float
    gpu_energy_kwh: float
    duration_sec: float
    ram_energy_kwh: float = 0.0
    emissions_kg: float = 0.0
    source: str = "mock"  # "codecarbon" | "mock"


# Approximate TDP-based power consumption (Watts)
_MODEL_POWER_PROFILES = {
    "phi3":         {"cpu_w": 12.0,  "gpu_w": 40.0},
    "llama3.2:3b":  {"cpu_w": 18.0,  "gpu_w": 70.0},
    "llama3.2:8b":  {"cpu_w": 25.0,  "gpu_w": 120.0},
    "default":      {"cpu_w": 20.0,  "gpu_w": 80.0},
}

# Idle power draw by state (Watts)
# ACTIVE-idle: model resident in GPU memory between queries (full footprint)
# SLEEP:       model offloaded / throttled (near-zero draw)
_IDLE_POWER_PROFILES = {
    "phi3":        {"active_w": 42.0,  "sleep_w": 2.5},
    "llama3.2:3b": {"active_w": 88.0,  "sleep_w": 2.5},
    "llama3.2:8b": {"active_w": 145.0, "sleep_w": 2.5},
    "default":     {"active_w": 100.0, "sleep_w": 2.5},
}

_JOULES_TO_KWH = 1 / 3_600_000.0


def idle_energy_kwh(model: str, duration_sec: float, sleeping: bool) -> float:
    """
    Energy consumed while idle (not actively inferring).
    sleeping=True  -> model offloaded, ~2.5 W
    sleeping=False -> model resident in GPU memory, full idle draw
    """
    profile = _IDLE_POWER_PROFILES.get(model, _IDLE_POWER_PROFILES["default"])
    watts = profile["sleep_w"] if sleeping else profile["active_w"]
    return round(watts * duration_sec * _JOULES_TO_KWH, 9)


def _mock_measurement(model: str, duration_sec: float) -> EnergyMeasurement:
    """Simulate energy measurement using TDP-based model profiles."""
    profile = _MODEL_POWER_PROFILES.get(model, _MODEL_POWER_PROFILES["default"])
    cpu_j = profile["cpu_w"] * duration_sec
    gpu_j = profile["gpu_w"] * duration_sec
    total_j = cpu_j + gpu_j

    return EnergyMeasurement(
        total_energy_kwh=round(total_j * _JOULES_TO_KWH, 9),
        cpu_energy_kwh=round(cpu_j * _JOULES_TO_KWH, 9),
        gpu_energy_kwh=round(gpu_j * _JOULES_TO_KWH, 9),
        duration_sec=round(duration_sec, 4),
        source="mock",
    )


@contextlib.contextmanager
def measure_energy(
    model: str,
    mock_mode: bool = True,
    project_name: str = "camas",
    output_dir: str = "reports",
) -> Generator[dict, None, EnergyMeasurement]:
    """
    Context manager that measures energy during execution.

    Usage:
        with measure_energy(model) as ctx:
            result = run_model(query)
        measurement = ctx["measurement"]
    """
    ctx: dict = {"measurement": None}
    start = time.time()

    if not mock_mode:
        try:
            from codecarbon import EmissionsTracker
            tracker = EmissionsTracker(
                project_name=project_name,
                output_dir=output_dir,
                log_level="error",
                save_to_file=False,
            )
            tracker.start()
            try:
                yield ctx
            finally:
                emissions_data = tracker.stop()
                duration = time.time() - start
                ctx["measurement"] = EnergyMeasurement(
                    total_energy_kwh=getattr(emissions_data, "energy_consumed", 0.0) or 0.0,
                    cpu_energy_kwh=getattr(emissions_data, "cpu_energy", 0.0) or 0.0,
                    gpu_energy_kwh=getattr(emissions_data, "gpu_energy", 0.0) or 0.0,
                    ram_energy_kwh=getattr(emissions_data, "ram_energy", 0.0) or 0.0,
                    emissions_kg=getattr(emissions_data, "emissions", 0.0) or 0.0,
                    duration_sec=duration,
                    source="codecarbon",
                )
            return
        except Exception as exc:
            logger.warning(f"CodeCarbon unavailable ({exc}); falling back to mock.")

    # Mock path
    yield ctx
    duration = time.time() - start
    ctx["measurement"] = _mock_measurement(model, duration)


def measure_energy_simple(
    model: str,
    duration_sec: float,
    mock_mode: bool = True,
) -> EnergyMeasurement:
    """Non-context-manager version for post-hoc measurement."""
    if mock_mode:
        return _mock_measurement(model, duration_sec)
    return _mock_measurement(model, duration_sec)
