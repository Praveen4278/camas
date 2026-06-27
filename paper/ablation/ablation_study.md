# CAMAS Ablation Study

> Each condition runs the same 100-prompt benchmark.
> Routing OFF = always llama3.2:8b. Sleep OFF = inter-batch pauses removed.

| Configuration | Avg Latency (ms) | Total Energy (kWh) | Total CO₂ (g) | Total Cost (USD) |
|---------------|-----------------|-------------------|--------------|-----------------|
| Baseline (static 8b) | 2318.2 | 0.004669 (ref) | 1.8675 | 0.001650 |
| CAMAS — routing OFF | 2147.3 | 0.004324 (-7.4%) | 1.7298 | 0.001650 |
| CAMAS — sleep OFF | 1018.1 | 0.001178 (-74.8%) | 0.4713 | 0.000276 |
| Full CAMAS | 1016.3 | 0.001182 (-74.7%) | 0.4728 | 0.000276 |