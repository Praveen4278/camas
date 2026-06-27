# CAMAS Research Tables

## Summary: Key Results

| Metric | Baseline | CAMAS | Improvement |
|--------|----------|-------|-------------|
| Energy (kWh) | 0.011148 | 0.005182 | **53.5% ↓** |
| CO₂ (g) | 4.4593 | 2.0726 | **53.5% ↓** |
| Avg Latency (ms) | 2287.9 | 1514.8 | **33.8% ↓** |
| Cost (USD) | $0.003300 | $0.001754 | **46.9% ↓** |

## Table 1: Experimental Results

> Values reported as **Mean ± 95% CI** (n=100 queries per mode).
> p-values from Wilcoxon signed-rank test (two-tailed). See Table 3 for ± Std Dev.

| Metric | Baseline | CAMAS | Reduction | p-value |
|--------|----------|-------|-----------|---------|
| Avg Latency (ms) | 2287.88 ± 89.41 | 1514.79 ± 146.64 | 33.8% | p < 0.001 |
| Avg Energy/Query (kWh) | 0.000111 ± 0.000004 | 0.000052 ± 0.000007 | 53.5% | p < 0.001 |
| Avg CO₂/Query (g) | 0.0446 ± 0.0014 | 0.0207 ± 0.0029 | 53.5% | p < 0.001 |
| Avg Cost/Query (USD) | 0.000033 ± 0.000000 | 0.000018 ± 0.000003 | 46.9% | p < 0.001 |
| Total Energy (kWh) | 0.011148 | 0.005182 | 53.5% | — |
| Total CO₂ (g)     | 4.4593   | 2.0726   | 53.5% | — |
| Total Cost (USD)   | 0.003300 | 0.001754 | 46.9% | — |
| Benchmark Size (prompts) | 100 | 100 | — | — |

## Table 2: Routing Statistics (CAMAS Mode)

| Model | Queries Routed | Percentage |
|-------|---------------|------------|
| llama3.2:8b | 46 | 46.0% |
| llama3.2:3b | 29 | 29.0% |
| phi3 | 25 | 25.0% |

## Table 3: Variability

> Values reported as **Mean ± Standard Deviation** (n=100 queries per mode).
> Note: CAMAS shows higher std dev in latency because dynamic routing intentionally
> dispatches queries across models with different response times.

| Metric | Baseline | CAMAS |
|--------|----------|-------|
| Latency (ms) | 2287.88 ± 456.18 | 1514.79 ± 748.16 |
| Energy/Query (kWh) | 0.000111 ± 0.000018 | 0.000052 ± 0.000037 |
| CO₂/Query (g) | 0.0446 ± 0.0073 | 0.0207 ± 0.0149 |
| Cost/Query (USD) | 0.000033 ± 0.000000 | 0.000018 ± 0.000014 |
