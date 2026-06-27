"""
CAMAS Task Router Agent
Routes tasks to appropriate LLM model based on complexity score.
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RoutingDecision:
    model: str
    reason: str
    complexity: float
    complexity_band: str  # "low" | "medium" | "high"


def route_task(
    complexity: float,
    simple_model: str = "phi3",
    medium_model: str = "llama3.2:3b",
    complex_model: str = "llama3.2:8b",
    simple_threshold: float = 3.0,
    medium_threshold: float = 7.0,
) -> RoutingDecision:
    """
    Route a task to an appropriate model based on complexity score.

    Rules:
        complexity < 3   → simple_model  (phi3)
        3 <= comp < 7    → medium_model  (llama3.2:3b)
        complexity >= 7  → complex_model (llama3.2:8b)
    """
    if complexity < simple_threshold:
        model = simple_model
        band  = "low"
        reason = (
            f"Complexity {complexity:.2f} < {simple_threshold} → "
            f"lightweight model '{simple_model}' selected for energy efficiency."
        )
    elif complexity < medium_threshold:
        model = medium_model
        band  = "medium"
        reason = (
            f"Complexity {complexity:.2f} in [{simple_threshold}, {medium_threshold}) → "
            f"medium model '{medium_model}' selected for balanced performance."
        )
    else:
        model = complex_model
        band  = "high"
        reason = (
            f"Complexity {complexity:.2f} ≥ {medium_threshold} → "
            f"capable model '{complex_model}' selected for high-quality output."
        )

    decision = RoutingDecision(
        model=model,
        reason=reason,
        complexity=complexity,
        complexity_band=band,
    )
    logger.debug(f"Router → model={model}, band={band}, complexity={complexity}")
    return decision
