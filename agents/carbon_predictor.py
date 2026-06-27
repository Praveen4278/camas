"""
CAMAS Carbon Predictor Agent
Estimates CO2 emissions based on energy usage and carbon intensity.

Formula: CO2 (grams) = Energy (kWh) × CarbonIntensity (gCO2/kWh)
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Approximate model energy profiles (kWh per 1000 tokens, rough estimates)
MODEL_ENERGY_PROFILES = {
    "phi3":          {"kwh_per_1k_tokens": 0.000050},  # ~50 mWh
    "llama3.2:3b":   {"kwh_per_1k_tokens": 0.000120},
    "llama3.2:8b":   {"kwh_per_1k_tokens": 0.000300},
    "default":       {"kwh_per_1k_tokens": 0.000200},
}

# Carbon intensity by region (gCO2/kWh) – reference values
REGIONAL_INTENSITIES = {
    "global_average":  400.0,
    "us_average":      386.0,
    "eu_average":      255.0,
    "nordic":           50.0,
    "china":           555.0,
    "india":           708.0,
    "renewable_heavy":  30.0,
}


@dataclass
class CarbonPrediction:
    predicted_co2_g: float
    energy_kwh: float
    carbon_intensity_g_per_kwh: float
    model: str
    token_count: int
    region: str
    is_mock: bool


def get_model_energy_estimate(model: str, token_count: int) -> float:
    """Estimate energy (kWh) for a given model and token count."""
    profile = MODEL_ENERGY_PROFILES.get(model, MODEL_ENERGY_PROFILES["default"])
    kwh = profile["kwh_per_1k_tokens"] * (token_count / 1000.0)
    return round(kwh, 9)


def predict_carbon(
    model: str,
    measured_energy_kwh: float | None,
    token_count: int = 500,
    carbon_intensity_g_per_kwh: float | None = None,
    region: str = "global_average",
    mock_mode: bool = True,
    mock_intensity: float = 400.0,
) -> CarbonPrediction:
    """
    Predict CO2 emissions.

    If measured_energy_kwh is provided (from CodeCarbon), use that.
    Otherwise fall back to model-based estimate.

    CO2 (g) = Energy (kWh) × CarbonIntensity (gCO2/kWh)
    """
    # Determine carbon intensity
    if carbon_intensity_g_per_kwh is not None:
        intensity = carbon_intensity_g_per_kwh
        is_mock = False
    elif mock_mode:
        intensity = mock_intensity
        is_mock = True
    else:
        intensity = REGIONAL_INTENSITIES.get(region, REGIONAL_INTENSITIES["global_average"])
        is_mock = False

    # Determine energy
    if measured_energy_kwh is not None and measured_energy_kwh > 0:
        energy = measured_energy_kwh
    else:
        energy = get_model_energy_estimate(model, token_count)

    co2_g = energy * intensity

    pred = CarbonPrediction(
        predicted_co2_g=round(co2_g, 6),
        energy_kwh=round(energy, 9),
        carbon_intensity_g_per_kwh=intensity,
        model=model,
        token_count=token_count,
        region=region,
        is_mock=is_mock,
    )
    logger.debug(
        f"CarbonPredictor → model={model}, energy={energy:.6f} kWh, "
        f"intensity={intensity} gCO2/kWh, CO2={co2_g:.4f} g"
    )
    return pred
