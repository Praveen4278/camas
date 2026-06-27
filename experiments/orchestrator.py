"""
CAMAS LangGraph Orchestrator
Defines the multi-agent graph for both CAMAS and Baseline modes.
"""

import uuid
import logging
from datetime import datetime, timezone
from typing import TypedDict, Annotated, Any

from langgraph.graph import StateGraph, END

from agents.planner import run_planner
from agents.router import route_task
from agents.carbon_predictor import predict_carbon
from agents.energy_monitor import measure_energy_simple
from agents.resource_allocator import allocate_resources, log_allocation
from agents.execution_agent import execute_query
from agents.memory_agent import MemoryAgent, QueryRecord, PerformanceRecord

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Graph State
# ---------------------------------------------------------------------------

class CAMASState(TypedDict):
    # Input
    query: str
    run_id: str
    query_id: str
    mode: str           # "camas" | "baseline"
    config: dict

    # Planner output
    complexity: float
    priority: float
    memory_req: float

    # Router output
    model: str
    routing_reason: str

    # Execution output
    response: str
    latency_ms: float
    token_count: int

    # Energy output
    total_energy_kwh: float
    cpu_energy_kwh: float
    gpu_energy_kwh: float
    duration_sec: float

    # Carbon output
    co2_g: float
    carbon_intensity: float

    # Cost
    cost_usd: float

    # Idle energy attribution (callable or None)
    idle_energy_kwh_addend: Any

    # Database
    db_conn: Any
    memory_agent: Any


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

def planner_node(state: CAMASState) -> dict:
    """Decompose and profile the task."""
    if state["mode"] == "baseline":
        # Skip planning; use fixed defaults
        return {
            "complexity": 7.5,
            "priority": 5.0,
            "memory_req": 7.0,
        }
    profile = run_planner(state["query"])
    return {
        "complexity": profile["complexity"],
        "priority":   profile["priority"],
        "memory_req": profile["memory_requirement"],
    }


def router_node(state: CAMASState) -> dict:
    """Select the appropriate model."""
    cfg = state["config"]
    if state["mode"] == "baseline":
        model = cfg.get("ollama", {}).get("models", {}).get("baseline", "llama3.2:8b")
        return {"model": model, "routing_reason": "Baseline: always uses heavy model."}

    thresholds = cfg.get("routing", {})
    decision = route_task(
        complexity=state["complexity"],
        simple_model=cfg["ollama"]["models"]["simple"],
        medium_model=cfg["ollama"]["models"]["medium"],
        complex_model=cfg["ollama"]["models"]["complex"],
        simple_threshold=thresholds.get("complexity_thresholds", {}).get("simple_max", 3.0),
        medium_threshold=thresholds.get("complexity_thresholds", {}).get("medium_max", 7.0),
    )

    # Log routing decision
    if state.get("memory_agent") and state.get("db_conn"):
        state["memory_agent"].store_routing(
            state["query_id"], state["run_id"],
            state["complexity"], decision.model, decision.reason,
        )

    # Resource allocation
    alloc = allocate_resources(state["complexity"])
    if state.get("db_conn"):
        log_allocation(state["db_conn"], state["query_id"], state["run_id"], alloc)

    return {"model": decision.model, "routing_reason": decision.reason}


def execution_node(state: CAMASState) -> dict:
    """Execute the query against the selected model."""
    cfg = state["config"]
    ollama_url  = cfg.get("ollama", {}).get("base_url", "http://localhost:11434")
    ollama_timeout = cfg.get("ollama", {}).get("timeout", 120)
    mock = cfg.get("energy", {}).get("mock_mode", True)

    result = execute_query(
        query=state["query"],
        model=state["model"],
        ollama_base_url=ollama_url,
        timeout=ollama_timeout,
        mock_mode=mock,
    )

    # Energy measurement (mock-based, tied to latency)
    duration_sec = result.latency_ms / 1000.0
    em = measure_energy_simple(state["model"], duration_sec, mock_mode=True)

    # Add attributed idle energy for this query
    addend_fn = state.get("idle_energy_kwh_addend")
    idle_e = addend_fn(state["model"]) if callable(addend_fn) else 0.0

    return {
        "response": result.response,
        "latency_ms": result.latency_ms,
        "token_count": result.token_count,
        "total_energy_kwh": round(em.total_energy_kwh + idle_e, 9),
        "cpu_energy_kwh":   em.cpu_energy_kwh,
        "gpu_energy_kwh":   em.gpu_energy_kwh,
        "duration_sec":     em.duration_sec,
    }


def carbon_predictor_node(state: CAMASState) -> dict:
    """Predict CO2 emissions."""
    cfg = state["config"]
    carbon_cfg = cfg.get("carbon", {})

    pred = predict_carbon(
        model=state["model"],
        measured_energy_kwh=state.get("total_energy_kwh"),
        token_count=state.get("token_count", 500),
        carbon_intensity_g_per_kwh=carbon_cfg.get("real_intensity_g_per_kwh"),
        mock_mode=carbon_cfg.get("mock_mode", True),
        mock_intensity=carbon_cfg.get("mock_intensity_g_per_kwh", 400.0),
    )
    return {
        "co2_g": pred.predicted_co2_g,
        "carbon_intensity": pred.carbon_intensity_g_per_kwh,
    }


def cost_calculator_node(state: CAMASState) -> dict:
    """Calculate monetary cost of query."""
    cfg = state["config"]
    cost_cfg = cfg.get("cost", {})

    rate_map = {
        "phi3":        cost_cfg.get("phi3_cost_per_1m_tokens", 0.10),
        "llama3.2:3b": cost_cfg.get("llama3_2_3b_cost_per_1m_tokens", 0.20),
        "llama3.2:8b": cost_cfg.get("llama3_2_8b_cost_per_1m_tokens", 0.75),
    }
    rate = rate_map.get(state["model"], 0.5)
    cost = rate * (state.get("token_count", 0) / 1_000_000)
    return {"cost_usd": round(cost, 8)}


def memory_node(state: CAMASState) -> dict:
    """Persist all metrics to database."""
    ma: MemoryAgent = state.get("memory_agent")
    if ma is None:
        return {}

    ts = datetime.now(timezone.utc).isoformat()

    ma.store_query(QueryRecord(
        query_id=state["query_id"],
        run_id=state["run_id"],
        query_text=state["query"],
        complexity=state.get("complexity", 0.0),
        priority=state.get("priority", 0.0),
        memory_req=state.get("memory_req", 0.0),
        model_selected=state.get("model", ""),
        routing_reason=state.get("routing_reason", ""),
        response_text=state.get("response", ""),
        latency_ms=state.get("latency_ms", 0.0),
        token_count=state.get("token_count", 0),
        timestamp=ts,
    ))

    ma.store_energy(
        state["query_id"], state["run_id"],
        state.get("total_energy_kwh", 0.0),
        state.get("cpu_energy_kwh", 0.0),
        state.get("gpu_energy_kwh", 0.0),
        state.get("duration_sec", 0.0),
    )

    ma.store_carbon(
        state["query_id"], state["run_id"],
        state.get("co2_g", 0.0),
        state.get("carbon_intensity", 400.0),
        state.get("total_energy_kwh", 0.0),
    )

    ma.store_performance(PerformanceRecord(
        query_id=state["query_id"],
        run_id=state["run_id"],
        mode=state["mode"],
        latency_ms=state.get("latency_ms", 0.0),
        energy_kwh=state.get("total_energy_kwh", 0.0),
        co2_g=state.get("co2_g", 0.0),
        cost_usd=state.get("cost_usd", 0.0),
        model=state.get("model", ""),
        complexity=state.get("complexity", 0.0),
        timestamp=ts,
    ))

    return {}


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    """Construct the CAMAS LangGraph."""
    graph = StateGraph(CAMASState)

    graph.add_node("planner",          planner_node)
    graph.add_node("router",           router_node)
    graph.add_node("executor",         execution_node)
    graph.add_node("carbon_predictor", carbon_predictor_node)
    graph.add_node("cost_calculator",  cost_calculator_node)
    graph.add_node("memory",           memory_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner",          "router")
    graph.add_edge("router",           "executor")
    graph.add_edge("executor",         "carbon_predictor")
    graph.add_edge("carbon_predictor", "cost_calculator")
    graph.add_edge("cost_calculator",  "memory")
    graph.add_edge("memory",           END)

    return graph.compile()


# Compiled graph (singleton)
_COMPILED_GRAPH = None


def get_compiled_graph():
    global _COMPILED_GRAPH
    if _COMPILED_GRAPH is None:
        _COMPILED_GRAPH = build_graph()
    return _COMPILED_GRAPH


def run_single_query(
    query: str,
    run_id: str,
    mode: str,
    config: dict,
    memory_agent: MemoryAgent,
    db_conn,
    idle_energy_kwh_addend=None,   # callable(model) -> float, or None
) -> dict:
    """Run one query through the CAMAS graph and return the final state."""
    query_id = str(uuid.uuid4())[:8]
    graph = get_compiled_graph()

    initial_state: CAMASState = {
        "query": query,
        "run_id": run_id,
        "query_id": query_id,
        "mode": mode,
        "config": config,
        "idle_energy_kwh_addend": idle_energy_kwh_addend,
        "complexity": 0.0,
        "priority": 0.0,
        "memory_req": 0.0,
        "model": "",
        "routing_reason": "",
        "response": "",
        "latency_ms": 0.0,
        "token_count": 0,
        "total_energy_kwh": 0.0,
        "cpu_energy_kwh": 0.0,
        "gpu_energy_kwh": 0.0,
        "duration_sec": 0.0,
        "co2_g": 0.0,
        "carbon_intensity": 0.0,
        "cost_usd": 0.0,
        "db_conn": db_conn,
        "memory_agent": memory_agent,
    }

    final_state = graph.invoke(initial_state)
    return final_state
