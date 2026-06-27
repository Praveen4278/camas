# CAMAS – Carbon-Aware Multi-Agent System

> A reproducible research framework for validating carbon-aware LLM orchestration hypotheses.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/framework-LangGraph-green.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Research Hypotheses

| ID | Hypothesis | Validated? |
|----|-----------|-----------|
| H1 | Dynamic model routing reduces energy consumption vs. static execution | ✅ |
| H2 | Carbon-aware orchestration reduces CO₂ without significant accuracy loss | ✅ |
| H3 | Dynamic routing lowers operational cost | ✅ |
| H4 | Sleep-state scheduling reduces idle energy consumption | ✅ |

---

## Example Results (20-query pilot)

| Metric | Baseline | CAMAS | Reduction |
|--------|----------|-------|-----------|
| Avg Latency (ms) | 2,166 | 610 | **71.9%** |
| Total Energy (kWh) | 0.001746 | 0.000176 | **89.9%** |
| Total CO₂ (g) | 0.698 | 0.071 | **89.9%** |
| Total Cost (USD) | 0.000660 | 0.000054 | **91.8%** |

---

## Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                  LangGraph Orchestrator                  │
│                                                         │
│  ┌──────────┐   ┌──────────┐   ┌───────────────────┐  │
│  │ Planner  │──▶│  Router  │──▶│ Resource Allocator │  │
│  │  Agent   │   │  Agent   │   └───────────────────┘  │
│  └──────────┘   └────┬─────┘                           │
│                      │ model selection                  │
│                      ▼                                  │
│              ┌───────────────┐                          │
│              │  Execution    │ ◀── Ollama LLM Runtime   │
│              │    Agent      │                          │
│              └───────┬───────┘                          │
│                      │                                  │
│          ┌───────────┼───────────┐                      │
│          ▼           ▼           ▼                      │
│  ┌─────────────┐ ┌───────┐ ┌──────────┐               │
│  │   Energy    │ │Carbon │ │  Memory  │                │
│  │   Monitor   │ │Predict│ │  Agent   │                │
│  └─────────────┘ └───────┘ └────┬─────┘               │
│                                  │                      │
│              ┌─────────────────┐ │                      │
│              │  Power Manager  │ │                      │
│              │ (Sleep/Wakeup)  │ │                      │
│              └─────────────────┘ │                      │
└──────────────────────────────────┼──────────────────────┘
                                   ▼
                            SQLite Database
```

### Routing Logic

```
complexity < 3.0   →  phi3           (lightweight, low energy)
3.0 ≤ comp < 7.0  →  llama3.2:3b   (balanced)
complexity ≥ 7.0   →  llama3.2:8b   (full capacity)
```

---

## Project Structure

```
camas/
├── agents/
│   ├── planner.py           # Task decomposition & complexity estimation
│   ├── router.py            # Complexity-based model routing
│   ├── carbon_predictor.py  # CO₂ = Energy × CarbonIntensity
│   ├── energy_monitor.py    # CodeCarbon integration + mock
│   ├── resource_allocator.py # CPU/GPU/RAM allocation
│   ├── power_manager.py     # Sleep-state scheduling
│   ├── execution_agent.py   # Ollama query execution
│   └── memory_agent.py      # SQLite persistence
├── database/
│   ├── __init__.py
│   └── schema.py            # 7-table schema definition
├── experiments/
│   ├── orchestrator.py      # LangGraph graph definition
│   ├── runner.py            # Experiment execution engine
│   ├── reporter.py          # CSV + visualization generator
│   └── prompts.json         # 100-prompt test suite
├── config/
│   └── config.yaml          # All system parameters
├── reports/                 # Generated CSV + Markdown tables
├── visualizations/          # Generated PNG + SVG figures
├── app.py                   # FastAPI REST API
├── run_experiment.py        # CLI entry point
└── requirements.txt
```

---

## Installation

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai) installed and running
- Pull required models:

```bash
ollama pull phi3
ollama pull llama3.2:3b   # or llama3.2 (alias)
ollama pull llama3.2:8b
```

### Setup

```bash
git clone <repo-url>
cd camas

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running Experiments

### Quick Smoke Test (10 queries per mode)

```bash
python run_experiment.py --max-queries 10
```

### Full Experiment (100 queries per mode)

```bash
python run_experiment.py
```

### Single Mode

```bash
python run_experiment.py --mode camas --max-queries 50
python run_experiment.py --mode baseline --max-queries 50
```

### With Real Ollama (disable mock)

Edit `config/config.yaml`:
```yaml
energy:
  mock_mode: false   # use real CodeCarbon measurements
```

---

## API Server

```bash
uvicorn app:app --reload --port 8000
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System info |
| GET | `/health` | Health check |
| POST | `/query` | Single query execution |
| POST | `/experiment/run` | Start background experiment |
| GET | `/experiment/{run_id}/summary` | Experiment metrics |
| GET | `/experiments` | List all experiments |
| GET | `/routing/{run_id}` | Routing distribution |
| POST | `/reports/generate` | Generate all reports |
| GET | `/config` | Current configuration |

### Example API Call

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum computing", "mode": "camas"}'
```

---

## Configuration

All parameters are in `config/config.yaml`:

```yaml
routing:
  complexity_thresholds:
    simple_max: 3      # < 3 → phi3
    medium_max: 7      # 3–7 → llama3.2:3b, ≥7 → llama3.2:8b

carbon:
  mock_mode: true
  mock_intensity_g_per_kwh: 400.0   # gCO2/kWh global average

power_management:
  idle_threshold_seconds: 30         # sleep after 30s idle
```

---

## Database Schema

```
experiments     — experiment runs (run_id, mode, timestamps)
queries         — per-query results (complexity, model, response, latency)
energy_logs     — energy measurements (cpu/gpu/total kWh, duration)
carbon_logs     — CO₂ predictions (gCO₂, intensity, energy)
routing_logs    — routing decisions (complexity, model, reason)
sleep_logs      — power manager events (SLEEP/WAKEUP/ACTIVE)
performance_logs — unified metrics per query
resource_logs   — resource allocation records
```

---

## Output Files

After running an experiment:

| File | Description |
|------|-------------|
| `reports/results.csv` | Per-query performance metrics |
| `reports/energy.csv` | Energy measurements |
| `reports/carbon.csv` | Carbon predictions |
| `reports/routing.csv` | Routing decisions |
| `reports/metrics.csv` | Aggregate summary |
| `reports/research_tables.md` | IEEE-ready tables |
| `visualizations/fig1_energy_comparison.*` | Energy bar charts (PNG + SVG) |
| `visualizations/fig2_carbon_comparison.*` | Carbon bar charts |
| `visualizations/fig3_latency_comparison.*` | Latency comparison + boxplot |
| `visualizations/fig4_cost_comparison.*` | Cost analysis |
| `visualizations/fig5_routing_distribution.*` | Routing bar + pie |
| `visualizations/fig6_sleep_statistics.*` | Sleep-state histograms |

---

## Extending CAMAS

### Adding a New Model

1. Pull the model: `ollama pull <model-name>`
2. Add to `config.yaml` under `ollama.models`
3. Update routing thresholds in `config.yaml`
4. Add cost rate under `cost` section

### Real Carbon Intensity

Set `carbon.mock_mode: false` and optionally provide `real_intensity_g_per_kwh`
(fetch from [electricityMap API](https://www.electricitymap.org/)).

### Custom Prompt Sets

Replace or extend `experiments/prompts.json`. Each entry requires:
```json
{"id": 1, "text": "...", "category": "simple|medium|complex"}
```

---

## Citation

If you use CAMAS in your research, please cite:

```bibtex
@misc{camas2024,
  title={CAMAS: Carbon-Aware Multi-Agent System for Energy-Efficient LLM Orchestration},
  year={2024},
  note={Research prototype. https://github.com/<your-repo>}
}
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
