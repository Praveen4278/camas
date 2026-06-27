"""
CAMAS Execution Agent
Executes queries via Ollama and collects response metrics.
"""

import time
import logging
import requests
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    response: str
    latency_ms: float
    token_count: int
    model: str
    success: bool
    error: str | None = None


def count_tokens(text: str) -> int:
    """Approximate token count (whitespace tokenization × 1.3 factor)."""
    return max(1, int(len(text.split()) * 1.3))


def execute_query(
    query: str,
    model: str,
    ollama_base_url: str = "http://localhost:11434",
    timeout: int = 120,
    mock_mode: bool = False,
) -> ExecutionResult:
    """
    Execute a query against an Ollama model.

    Falls back to mock response if Ollama is unavailable.
    """
    if mock_mode:
        return _mock_execute(query, model)

    url = f"{ollama_base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": query,
        "stream": False,
        "options": {"temperature": 0.7},
    }

    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        latency_ms = (time.time() - start) * 1000

        response_text = data.get("response", "")
        # Ollama returns eval_count (output tokens) and prompt_eval_count
        token_count = (
            data.get("eval_count", 0) + data.get("prompt_eval_count", 0)
            or count_tokens(response_text)
        )

        return ExecutionResult(
            response=response_text,
            latency_ms=round(latency_ms, 2),
            token_count=token_count,
            model=model,
            success=True,
        )

    except requests.exceptions.ConnectionError:
        logger.warning(f"Ollama not reachable at {ollama_base_url}. Using mock.")
        return _mock_execute(query, model)
    except Exception as exc:
        latency_ms = (time.time() - start) * 1000
        logger.error(f"Execution failed: {exc}")
        return ExecutionResult(
            response="",
            latency_ms=round(latency_ms, 2),
            token_count=0,
            model=model,
            success=False,
            error=str(exc),
        )


# ---------------------------------------------------------------------------
# Mock responses for offline testing / reproducibility
# ---------------------------------------------------------------------------

_MOCK_RESPONSES = {
    "phi3": (
        "This is a concise response from phi3, the lightweight model. "
        "It is well suited for simple tasks that require minimal compute."
    ),
    "llama3.2:3b": (
        "This is a medium-depth response from llama3.2:3b. "
        "The 3-billion parameter model balances quality and efficiency, "
        "making it a strong choice for mid-complexity queries."
    ),
    "llama3.2:8b": (
        "This is a comprehensive response from llama3.2:8b. "
        "The 8-billion parameter model provides high-quality reasoning "
        "for complex analytical and generative tasks requiring deep understanding. "
        "It consumes more energy but delivers superior accuracy on challenging prompts."
    ),
}

# Simulate realistic latency variance by model tier (ms)
_MOCK_LATENCY = {
    "phi3":        (400,  800),
    "llama3.2:3b": (800,  1600),
    "llama3.2:8b": (1500, 3000),
}


def _mock_execute(query: str, model: str) -> ExecutionResult:
    import random
    lo, hi = _MOCK_LATENCY.get(model, (1000, 2000))
    latency_ms = random.uniform(lo, hi)
    time.sleep(latency_ms / 1000)  # simulate real delay
    response = _MOCK_RESPONSES.get(model, "Mock response.")
    return ExecutionResult(
        response=response,
        latency_ms=round(latency_ms, 2),
        token_count=count_tokens(response),
        model=model,
        success=True,
        error=None,
    )
