# CAMAS Research Tables

## Summary: Key Results

| Metric | Baseline | CAMAS | Improvement |
|--------|----------|-------|-------------|
| Energy (kWh) | 0.011617 | 0.010605 | **8.7% ↓** |
| CO₂ (g) | 4.6467 | 4.2419 | **8.7% ↓** |
| Avg Latency (ms) | 2404.2 | 1543.5 | **35.8% ↓** |
| Cost (USD) | $0.003300 | $0.003507 | **-6.3% ↓** |

## Table 1: Experimental Results

> Values reported as **Mean ± 95% CI** (n=100 queries per mode).
> p-values from Wilcoxon signed-rank test (two-tailed). See Table 3 for ± Std Dev.

| Metric | Baseline | CAMAS | Reduction | p-value |
|--------|----------|-------|-----------|---------|
| Avg Latency (ms) | 2404.18 ± 81.62 | 1543.49 ± 106.17 | 35.8% | p < 0.001 |
| Avg Energy/Query (kWh) | 0.000116 ± 0.000003 | 0.000053 ± 0.000005 | 54.4% | p < 0.001 |
| Avg CO₂/Query (g) | 0.0465 ± 0.0013 | 0.0212 ± 0.0021 | 54.4% | p < 0.001 |
| Avg Cost/Query (USD) | 0.000033 ± 0.000000 | 0.000018 ± 0.000002 | 46.9% | p < 0.001 |
| Total Energy (kWh) | 0.011617 | 0.010605 | 8.7% | — |
| Total CO₂ (g)     | 4.6467   | 4.2419   | 8.7% | — |
| Total Cost (USD)   | 0.003300 | 0.003507 | -6.3% | — |
| Benchmark Size (prompts) | 100 | 200 | — | — |

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
| Latency (ms) | 2404.18 ± 416.45 | 1543.49 ± 766.04 |
| Energy/Query (kWh) | 0.000116 ± 0.000017 | 0.000053 ± 0.000038 |
| CO₂/Query (g) | 0.0465 ± 0.0067 | 0.0212 ± 0.0152 |
| Cost/Query (USD) | 0.000033 ± 0.000000 | 0.000018 ± 0.000014 |
