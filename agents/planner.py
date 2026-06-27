"""
CAMAS Planner Agent
Decomposes tasks, estimates complexity/priority/memory
"""

import re
import logging
from typing import TypedDict

logger = logging.getLogger(__name__)


class TaskProfile(TypedDict):
    complexity: float       # 1-10
    priority: float         # 1-10
    memory_requirement: float  # 1-10
    decomposition: list[str]
    query_length: int
    estimated_tokens: int


# Complexity heuristics keyword sets
_HIGH_COMPLEXITY_KEYWORDS = {
    # Design / architecture tasks
    "design", "architect", "architect a", "design a", "build a", "implement",
    "implement a", "develop a", "create a system", "engineer",
    # Analysis / research
    "analyze", "analyse", "compare and contrast", "evaluate", "synthesize",
    "research", "survey", "investigate", "assess", "derive",
    # Technical depth signals
    "algorithm", "algorithms", "mathematical", "proof", "formally prove",
    "from first principles", "from scratch", "mathematical foundations",
    "complexity analysis", "derive the", "computational complexity",
    # ML / AI domain (always complex)
    "machine learning", "deep learning", "neural network", "transformer",
    "backpropagation", "reinforcement learning", "federated learning",
    "generative", "diffusion model", "variational autoencoder", "gan",
    "large language model", "llm", "rlhf", "fine-tun",
    # Systems / distributed (always complex)
    "distributed system", "distributed", "consensus", "fault-tolerant",
    "zero-trust", "sharding", "linearizable", "exactly-once",
    "Byzantine", "raft", "paxos", "crdt", "operational transform",
    # Security / cryptography
    "zero-knowledge", "cryptograph", "homomorphic", "bft",
    # Coding tasks
    "write a program", "write code", "implement in python", "code a",
    "debug", "optimize", "optimize the",
    # Scope / scale signals
    "comprehensive", "end-to-end", "multi-tenant", "billion", "million requests",
    "at scale", "production", "trade-off", "trade-offs",
    # Academic signals
    "advanced", "expert", "phd", "dissertation", "white paper",
}

_MEDIUM_COMPLEXITY_KEYWORDS = {
    "describe", "summarize", "explain", "outline", "compare",
    "what is", "how does", "how do", "pros and cons", "difference between",
    "differences between", "overview", "steps", "process", "method",
    "write a short", "write a brief", "give an example",
}

_LOW_COMPLEXITY_KEYWORDS = {
    "who is", "who was", "who invented", "who wrote", "who painted",
    "what year", "what color", "what is the capital", "how many",
    "name the", "name three", "define the word", "what does",
    "convert ", "translate ", "spell ",
}


def estimate_complexity(query: str) -> float:
    """
    Estimate query complexity on a 1–10 scale.
    Keyword signal dominates; length is a secondary tiebreaker.
    """
    q_lower = query.lower()
    words   = q_lower.split()
    length  = len(words)

    # Keyword hits (check substrings for multi-word phrases)
    high_hits = sum(1 for kw in _HIGH_COMPLEXITY_KEYWORDS if kw in q_lower)
    med_hits  = sum(1 for kw in _MEDIUM_COMPLEXITY_KEYWORDS if kw in q_lower)
    low_hits  = sum(1 for kw in _LOW_COMPLEXITY_KEYWORDS if kw in q_lower)

    # Start from keyword-dominant base
    if high_hits >= 2:
        base = 6.0
    elif high_hits == 1:
        base = 4.5
    elif med_hits >= 1:
        base = 3.0
    elif low_hits >= 1:
        base = 1.5
    else:
        # Fallback to length only when no keywords match
        if length <= 5:   base = 1.5
        elif length <= 15: base = 2.5
        elif length <= 35: base = 4.0
        else:              base = 6.0

    # Secondary adjustments
    score = base + (high_hits - 1) * 0.7 + med_hits * 0.2 - low_hits * 0.4

    # Length nudge (±1 max) — longer queries are usually more involved
    if length > 20:  score += 0.5
    if length > 35:  score += 0.5
    if length <= 6:  score -= 0.3

    # Structural signals
    if any(c in query for c in ["\n", "1.", "a)"]):
        score += 0.5   # multi-part question
    if re.search(r"\bcode\b|\bfunction\b|\bclass\b|\bimport\b", q_lower):
        score += 1.0

    return round(max(1.0, min(10.0, score)), 2)


def estimate_priority(query: str) -> float:
    """Estimate task priority 1–10 based on urgency signals."""
    q_lower = query.lower()
    urgent_kws = {"urgent", "asap", "immediately", "critical", "emergency",
                  "important", "deadline", "priority", "now", "quickly"}
    low_kws = {"sometime", "whenever", "no rush", "low priority", "optional"}
    hits = sum(1 for kw in urgent_kws if kw in q_lower)
    low  = sum(1 for kw in low_kws if kw in q_lower)
    return round(max(1.0, min(10.0, 5.0 + hits * 1.5 - low * 1.0)), 2)


def estimate_memory(complexity: float) -> float:
    """Estimate memory requirement 1–10 proportional to complexity."""
    return round(max(1.0, min(10.0, complexity * 0.9 + 0.5)), 2)


def decompose_task(query: str) -> list[str]:
    """Simple rule-based task decomposition."""
    subtasks = ["Parse and understand query"]
    q_lower = query.lower()
    if any(kw in q_lower for kw in ["compare", "versus", "vs"]):
        subtasks.append("Identify comparison subjects")
        subtasks.append("Gather information on each subject")
        subtasks.append("Synthesize comparison")
    if any(kw in q_lower for kw in ["explain", "describe", "what is"]):
        subtasks.append("Retrieve relevant knowledge")
        subtasks.append("Structure explanation")
    if any(kw in q_lower for kw in ["code", "implement", "write a function", "program"]):
        subtasks.append("Design solution architecture")
        subtasks.append("Implement code")
        subtasks.append("Validate correctness")
    subtasks.append("Generate response")
    return subtasks


def run_planner(query: str) -> TaskProfile:
    """Main planner entry point."""
    complexity = estimate_complexity(query)
    priority   = estimate_priority(query)
    memory_req = estimate_memory(complexity)
    subtasks   = decompose_task(query)
    token_est  = max(50, len(query.split()) * 4)

    profile: TaskProfile = {
        "complexity": complexity,
        "priority": priority,
        "memory_requirement": memory_req,
        "decomposition": subtasks,
        "query_length": len(query.split()),
        "estimated_tokens": token_est,
    }
    logger.debug(f"Planner → complexity={complexity}, priority={priority}, mem={memory_req}")
    return profile
