"""
CAMAS Report Generator
Generates CSV reports, research tables, and publication-quality graphs.
"""

import csv
import json
import logging
from pathlib import Path
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

logger = logging.getLogger(__name__)

# Publication style
plt.rcParams.update({
    "font.family":     "DejaVu Sans",
    "font.size":       11,
    "axes.titlesize":  13,
    "axes.labelsize":  12,
    "legend.fontsize": 10,
    "figure.dpi":      150,
    "axes.grid":       True,
    "grid.alpha":      0.3,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
})

COLORS = {
    "baseline": "#E74C3C",
    "camas":    "#2ECC71",
    "phi3":     "#3498DB",
    "medium":   "#9B59B6",
    "complex":  "#E67E22",
    "sleep":    "#95A5A6",
    "active":   "#27AE60",
}


# ---------------------------------------------------------------------------
# CSV Exports
# ---------------------------------------------------------------------------

def export_performance_csv(all_perf: list[dict], out_dir: Path) -> None:
    path = out_dir / "results.csv"
    if not all_perf:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_perf[0].keys())
        writer.writeheader()
        writer.writerows(all_perf)
    logger.info(f"Exported {path}")


def export_routing_csv(all_routing: list[dict], out_dir: Path) -> None:
    path = out_dir / "routing.csv"
    if not all_routing:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_routing[0].keys())
        writer.writeheader()
        writer.writerows(all_routing)
    logger.info(f"Exported {path}")


def export_energy_csv(all_energy: list[dict], out_dir: Path) -> None:
    path = out_dir / "energy.csv"
    if not all_energy:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_energy[0].keys())
        writer.writeheader()
        writer.writerows(all_energy)
    logger.info(f"Exported {path}")


def export_carbon_csv(all_carbon: list[dict], out_dir: Path) -> None:
    path = out_dir / "carbon.csv"
    if not all_carbon:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_carbon[0].keys())
        writer.writeheader()
        writer.writerows(all_carbon)
    logger.info(f"Exported {path}")


def export_metrics_csv(summaries: dict, out_dir: Path) -> None:
    """Aggregate metrics summary."""
    rows = []
    for mode, s in summaries.items():
        rows.append({**s, "mode": mode})
    path = out_dir / "metrics.csv"
    if rows:
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    logger.info(f"Exported {path}")


# ---------------------------------------------------------------------------
# Research Tables (Markdown + JSON)
# ---------------------------------------------------------------------------

def generate_research_tables(
    summaries: dict,
    routing_dist: dict,
    out_dir: Path,
    all_perf: list[dict] | None = None,
) -> str:
    """Generate IEEE-style research tables as Markdown."""
    lines = []
    lines.append("# CAMAS Research Tables\n")

    b = summaries.get("baseline", {})
    c = summaries.get("camas",    {})

    # ── Statistical helpers ───────────────────────────────────────────
    def pct_red(bv, cv):
        return f"{(bv - cv) / bv * 100:.1f}%" if bv else "N/A"

    def ci95(values):
        n = len(values)
        if n < 2:
            return 0.0
        sd  = statistics.stdev(values)
        return 1.96 * sd / (n ** 0.5)

    # Wilcoxon signed-rank (manual, no scipy needed)
    def wilcoxon_p(a: list[float], b_: list[float]) -> str:
        """Approximate one-sample Wilcoxon signed-rank p-value (two-tailed).
        Returns formatted string like 'p < 0.001'."""
        try:
            diffs = [x - y for x, y in zip(a, b_) if x != y]
            if not diffs:
                return "p = 1.000"
            abs_d = sorted(abs(d) for d in diffs)
            ranks = {v: i + 1 for i, v in enumerate(abs_d)}
            W = sum(ranks[abs(d)] for d in diffs if d > 0)
            n = len(diffs)
            # Normal approximation
            mu_w  = n * (n + 1) / 4
            sig_w = (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
            z = (W - mu_w) / sig_w if sig_w else 0
            # Two-tailed p from standard normal (approximation)
            import math
            p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
            if p < 0.001:  return "p < 0.001"
            if p < 0.01:   return "p < 0.010"
            if p < 0.05:   return "p < 0.050"
            return        f"p = {p:.3f}"
        except Exception:
            return "N/A"

    perf = all_perf or []
    b_rows = [r for r in perf if r["mode"] == "baseline"]
    c_rows = [r for r in perf if r["mode"] == "camas"]

    b_lat  = [r["latency_ms"] for r in b_rows]
    c_lat  = [r["latency_ms"] for r in c_rows]
    b_e    = [r["energy_kwh"] for r in b_rows]
    c_e    = [r["energy_kwh"] for r in c_rows]
    b_co2  = [r["co2_g"]      for r in b_rows]
    c_co2  = [r["co2_g"]      for r in c_rows]
    b_cost = [r["cost_usd"]   for r in b_rows]
    c_cost = [r["cost_usd"]   for r in c_rows]

    # ── Compact Summary Table ─────────────────────────────────────────
    lines.append("## Summary: Key Results\n")
    lines.append("| Metric | Baseline | CAMAS | Improvement |")
    lines.append("|--------|----------|-------|-------------|")
    compact = [
        ("Energy (kWh)",    f"{b.get('total_energy_kwh',0):.6f}",  f"{c.get('total_energy_kwh',0):.6f}",  pct_red(b.get('total_energy_kwh',0),  c.get('total_energy_kwh',0))),
        ("CO\u2082 (g)",         f"{b.get('total_co2_g',0):.4f}",      f"{c.get('total_co2_g',0):.4f}",       pct_red(b.get('total_co2_g',0),       c.get('total_co2_g',0))),
        ("Avg Latency (ms)",f"{b.get('avg_latency_ms',0):.1f}",    f"{c.get('avg_latency_ms',0):.1f}",     pct_red(b.get('avg_latency_ms',0),    c.get('avg_latency_ms',0))),
        ("Cost (USD)",      f"${b.get('total_cost_usd',0):.6f}",   f"${c.get('total_cost_usd',0):.6f}",    pct_red(b.get('total_cost_usd',0),    c.get('total_cost_usd',0))),
    ]
    for label, bv, cv, imp in compact:
        lines.append(f"| {label} | {bv} | {cv} | **{imp} ↓** |")
    lines.append("")

    # ── Table 1: Full Experimental Results with CI ────────────────────
    lines.append("## Table 1: Experimental Results\n")
    lines.append("> Values reported as **Mean ± 95% CI** (n=100 queries per mode).")
    lines.append("> p-values from Wilcoxon signed-rank test (two-tailed). See Table 3 for ± Std Dev.\n")
    lines.append("| Metric | Baseline | CAMAS | Reduction | p-value |")
    lines.append("|--------|----------|-------|-----------|---------|")

    def row(label, bv, cv, b_vals, c_vals, fmt=".4f"):
        b_ci = ci95(b_vals) if b_vals else 0
        c_ci = ci95(c_vals) if c_vals else 0
        p    = wilcoxon_p(b_vals, c_vals) if b_vals and c_vals else "N/A"
        lines.append(
            f"| {label} "
            f"| {bv:{fmt}} ± {b_ci:{fmt}} "
            f"| {cv:{fmt}} ± {c_ci:{fmt}} "
            f"| {pct_red(bv, cv)} "
            f"| {p} |"
        )

    row("Avg Latency (ms)",     b.get('avg_latency_ms',0),  c.get('avg_latency_ms',0),  b_lat,  c_lat,  ".2f")
    row("Avg Energy/Query (kWh)",b.get('avg_energy_kwh',0), c.get('avg_energy_kwh',0),  b_e,    c_e,    ".6f")
    row("Avg CO\u2082/Query (g)",    b.get('avg_co2_g',0),       c.get('avg_co2_g',0),       b_co2,  c_co2,  ".4f")
    row("Avg Cost/Query (USD)",  b.get('avg_cost_usd',0),    c.get('avg_cost_usd',0),    b_cost, c_cost, ".6f")
    lines.append(f"| Total Energy (kWh) | {b.get('total_energy_kwh',0):.6f} | {c.get('total_energy_kwh',0):.6f} | {pct_red(b.get('total_energy_kwh',0), c.get('total_energy_kwh',0))} | — |")
    lines.append(f"| Total CO\u2082 (g)     | {b.get('total_co2_g',0):.4f}   | {c.get('total_co2_g',0):.4f}   | {pct_red(b.get('total_co2_g',0),    c.get('total_co2_g',0))} | — |")
    lines.append(f"| Total Cost (USD)   | {b.get('total_cost_usd',0):.6f} | {c.get('total_cost_usd',0):.6f} | {pct_red(b.get('total_cost_usd',0), c.get('total_cost_usd',0))} | — |")
    lines.append(f"| Benchmark Size (prompts) | {b.get('n_queries',0)} | {c.get('n_queries',0)} | — | — |")
    lines.append("")

    # ── Table 2: Routing Statistics ───────────────────────────────────
    lines.append("## Table 2: Routing Statistics (CAMAS Mode)\n")
    lines.append("| Model | Queries Routed | Percentage |")
    lines.append("|-------|---------------|------------|")
    total_routed = sum(routing_dist.values()) if routing_dist else 1
    for model, cnt in sorted(routing_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| {model} | {cnt} | {cnt/total_routed*100:.1f}% |")
    lines.append("")

    # ── Table 3: Per-Metric Std Dev ───────────────────────────────────
    lines.append("## Table 3: Variability\n")
    lines.append("> Values reported as **Mean ± Standard Deviation** (n=100 queries per mode).")
    lines.append("> Note: CAMAS shows higher std dev in latency because dynamic routing intentionally")    
    lines.append("> dispatches queries across models with different response times.\n")
    lines.append("| Metric | Baseline | CAMAS |")
    lines.append("|--------|----------|-------|")
    def sd_row(label, b_vals, c_vals, fmt=".4f"):
        bmu = statistics.mean(b_vals) if b_vals else 0
        cmu = statistics.mean(c_vals) if c_vals else 0
        bsd = statistics.stdev(b_vals) if len(b_vals) > 1 else 0
        csd = statistics.stdev(c_vals) if len(c_vals) > 1 else 0
        lines.append(f"| {label} | {bmu:{fmt}} ± {bsd:{fmt}} | {cmu:{fmt}} ± {csd:{fmt}} |")
    sd_row("Latency (ms)",       b_lat,  c_lat,  ".2f")
    sd_row("Energy/Query (kWh)", b_e,    c_e,    ".6f")
    sd_row("CO\u2082/Query (g)",      b_co2,  c_co2,  ".4f")
    sd_row("Cost/Query (USD)",   b_cost, c_cost, ".6f")
    lines.append("")

    content = "\n".join(lines)
    (out_dir / "research_tables.md").write_text(content)
    logger.info(f"Exported {out_dir / 'research_tables.md'}")
    return content


def generate_ablation_tables(ablation_results: dict, out_dir: Path) -> str:
    """
    Generate ablation study table.

    ablation_results: {
        "full_camas":        {avg_latency_ms, total_energy_kwh, total_co2_g, total_cost_usd},
        "no_routing":        {...},   # always llama3.2:8b, no sleep
        "no_sleep":          {...},   # routing ON, sleep OFF
    }
    """
    lines = ["# CAMAS Ablation Study\n"]
    lines.append("> Each condition runs the same 100-prompt benchmark.")
    lines.append("> Routing OFF = always llama3.2:8b. Sleep OFF = inter-batch pauses removed.\n")
    lines.append("| Configuration | Avg Latency (ms) | Total Energy (kWh) | Total CO₂ (g) | Total Cost (USD) |")
    lines.append("|---------------|-----------------|-------------------|--------------|-----------------|")

    order = [
        ("Baseline (static 8b)",     "baseline"),
        ("CAMAS — routing OFF",       "no_routing"),
        ("CAMAS — sleep OFF",         "no_sleep"),
        ("Full CAMAS",                "full_camas"),
    ]
    ref_energy = ablation_results.get("baseline", {}).get("total_energy_kwh", 1) or 1
    for label, key in order:
        d = ablation_results.get(key, {})
        if not d:
            continue
        lat   = d.get("avg_latency_ms",   0)
        eng   = d.get("total_energy_kwh", 0)
        co2   = d.get("total_co2_g",      0)
        cost  = d.get("total_cost_usd",   0)
        delta = f"({(eng - ref_energy)/ref_energy*100:+.1f}%)" if key != "baseline" else "(ref)"
        lines.append(f"| {label} | {lat:.1f} | {eng:.6f} {delta} | {co2:.4f} | {cost:.6f} |")

    content = "\n".join(lines)
    path = out_dir / "ablation_study.md"
    path.write_text(content)
    logger.info(f"Exported {path}")
    return content


def generate_scalability_table(scale_results: list[dict], out_dir: Path) -> str:
    """
    Generate scalability table.

    scale_results: list of {n_queries, avg_latency_ms, total_energy_kwh,
                             total_co2_g, total_cost_usd, routing_dist}
    """
    lines = ["# CAMAS Scalability Analysis\n"]
    lines.append("> CAMAS mode run at increasing benchmark sizes.")
    lines.append("> Energy and cost are totals; latency is per-query average.\n")
    lines.append("| Benchmark Size | Avg Latency (ms) | Total Energy (kWh) | Total CO₂ (g) | Total Cost (USD) |")
    lines.append("|---------------|-----------------|-------------------|--------------|-----------------|")
    for r in scale_results:
        lines.append(
            f"| {r['n_queries']:>4d} prompts "
            f"| {r['avg_latency_ms']:.1f} "
            f"| {r['total_energy_kwh']:.6f} "
            f"| {r['total_co2_g']:.4f} "
            f"| {r['total_cost_usd']:.6f} |"
        )
    content = "\n".join(lines)
    path = out_dir / "scalability.md"
    path.write_text(content)
    logger.info(f"Exported {path}")
    return content


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------

def _bar_comparison(
    ax, baseline_val, camas_val, ylabel, title, unit="",
    label_fmt=".4f", b_err=None, c_err=None,
):
    yerr = [[0, 0], [b_err or 0, c_err or 0]] if (b_err or c_err) else None
    bars = ax.bar(
        ["Baseline", "CAMAS"],
        [baseline_val, camas_val],
        color=[COLORS["baseline"], COLORS["camas"]],
        width=0.5, edgecolor="white", linewidth=1.2,
        yerr=yerr, capsize=6, error_kw={"elinewidth": 1.5, "ecolor": "#333"},
    )
    for bar, val in zip(bars, [baseline_val, camas_val]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() * 1.02,
            f"{val:{label_fmt}}{unit}", ha="center", va="bottom", fontsize=9,
        )
    if baseline_val > 0:
        reduction = (baseline_val - camas_val) / baseline_val * 100
        ax.set_title(f"{title}\n(↓{reduction:.1f}% reduction)", fontsize=12)
    else:
        ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(baseline_val, camas_val) * 1.25)


def _stats(values: list[float]) -> tuple[float, float, float, float]:
    """Return (mean, std, ci95_lo, ci95_hi) for a sample."""
    if not values:
        return 0.0, 0.0, 0.0, 0.0
    n   = len(values)
    mu  = statistics.mean(values)
    sd  = statistics.stdev(values) if n > 1 else 0.0
    sem = sd / (n ** 0.5)
    ci  = 1.96 * sem          # 95% CI half-width
    return mu, sd, mu - ci, mu + ci


def generate_visualizations(
    summaries: dict,
    all_perf: list[dict],
    routing_dist: dict,
    sleep_logs: list[dict],
    out_dir: Path,
) -> list[Path]:
    """Generate all publication-quality figures. Returns list of saved paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []

    b = summaries.get("baseline", {})
    c = summaries.get("camas", {})

    baseline_perf = [r for r in all_perf if r["mode"] == "baseline"]
    camas_perf    = [r for r in all_perf if r["mode"] == "camas"]

    # per-query series for stats
    b_energy = [r["energy_kwh"] for r in baseline_perf]
    c_energy = [r["energy_kwh"] for r in camas_perf]
    b_lat    = [r["latency_ms"] for r in baseline_perf]
    c_lat    = [r["latency_ms"] for r in camas_perf]
    b_co2    = [r["co2_g"]      for r in baseline_perf]
    c_co2    = [r["co2_g"]      for r in camas_perf]
    b_cost   = [r["cost_usd"]   for r in baseline_perf]
    c_cost   = [r["cost_usd"]   for r in camas_perf]

    _, b_e_sd, _, _ = _stats(b_energy)
    _, c_e_sd, _, _ = _stats(c_energy)
    _, b_l_sd, _, _ = _stats(b_lat)
    _, c_l_sd, _, _ = _stats(c_lat)
    _, b_co2_sd, _, _ = _stats(b_co2)
    _, c_co2_sd, _, _ = _stats(c_co2)
    _, b_cost_sd, _, _ = _stats(b_cost)
    _, c_cost_sd, _, _ = _stats(c_cost)

    # ------------------------------------------------------------------
    # Figure 1: Energy Comparison
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 1: Energy Consumption Comparison", fontweight="bold")
    _bar_comparison(
        axes[0],
        b.get("total_energy_kwh", 0), c.get("total_energy_kwh", 0),
        "Total Energy (kWh)", "Total Energy Consumed", " kWh",
    )
    _bar_comparison(
        axes[1],
        b.get("avg_energy_kwh", 0), c.get("avg_energy_kwh", 0),
        "Energy per Query (kWh)", "Average Energy per Query", " kWh",
        b_err=b_e_sd, c_err=c_e_sd,
    )
    plt.tight_layout()
    for ext in ["png", "svg"]:
        p = out_dir / f"fig1_energy_comparison.{ext}"
        plt.savefig(p, bbox_inches="tight")
        saved.append(p)
    plt.close()

    # ------------------------------------------------------------------
    # Figure 2: Carbon Comparison
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 2: Carbon Emissions Comparison (CO₂)", fontweight="bold")
    _bar_comparison(
        axes[0],
        b.get("total_co2_g", 0), c.get("total_co2_g", 0),
        "Total CO₂ (g)", "Total Carbon Emissions", " g",
    )
    _bar_comparison(
        axes[1],
        b.get("avg_co2_g", 0), c.get("avg_co2_g", 0),
        "CO₂ per Query (g)", "Average CO₂ per Query", " g",
        b_err=b_co2_sd, c_err=c_co2_sd,
    )
    plt.tight_layout()
    for ext in ["png", "svg"]:
        p = out_dir / f"fig2_carbon_comparison.{ext}"
        plt.savefig(p, bbox_inches="tight")
        saved.append(p)
    plt.close()

    # ------------------------------------------------------------------
    # Figure 3: Latency Comparison
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 3: Latency Comparison", fontweight="bold")

    b_lat_mu, b_lat_sd, _, _ = _stats(b_lat)
    c_lat_mu, c_lat_sd, _, _ = _stats(c_lat)
    _bar_comparison(
        axes[0],
        b_lat_mu, c_lat_mu,
        "Avg Latency (ms)",
        f"Average Latency\n(Baseline: {b_lat_mu:.0f}±{b_lat_sd:.0f} ms  CAMAS: {c_lat_mu:.0f}±{c_lat_sd:.0f} ms)",
        " ms", label_fmt=".0f",
        b_err=b_lat_sd, c_err=c_lat_sd,
    )

    if b_lat and c_lat:
        bp = axes[1].boxplot(
            [b_lat, c_lat],
            patch_artist=True, notch=False,
        )
        axes[1].set_xticks([1, 2])
        axes[1].set_xticklabels(["Baseline", "CAMAS"])
        for patch, color in zip(bp["boxes"], [COLORS["baseline"], COLORS["camas"]]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        axes[1].set_title("Latency Distribution (Boxplot)")
        axes[1].set_ylabel("Latency (ms)")

    plt.tight_layout()
    for ext in ["png", "svg"]:
        p = out_dir / f"fig3_latency_comparison.{ext}"
        plt.savefig(p, bbox_inches="tight")
        saved.append(p)
    plt.close()

    # ------------------------------------------------------------------
    # Figure 4: Cost Comparison
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 4: Cost Comparison (USD)", fontweight="bold")
    _bar_comparison(
        axes[0],
        b.get("total_cost_usd", 0), c.get("total_cost_usd", 0),
        "Total Cost (USD)", "Total Operational Cost", "",
        label_fmt=".6f",
    )
    _bar_comparison(
        axes[1],
        b.get("avg_cost_usd", 0), c.get("avg_cost_usd", 0),
        "Cost per Query (USD)", "Average Cost per Query", "",
        label_fmt=".6f", b_err=b_cost_sd, c_err=c_cost_sd,
    )
    plt.tight_layout()
    for ext in ["png", "svg"]:
        p = out_dir / f"fig4_cost_comparison.{ext}"
        plt.savefig(p, bbox_inches="tight")
        saved.append(p)
    plt.close()

    # ------------------------------------------------------------------
    # Figure 5: Routing Distribution
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 5: CAMAS Routing Distribution", fontweight="bold")

    if routing_dist:
        models = list(routing_dist.keys())
        counts = [routing_dist[m] for m in models]
        bar_colors = [COLORS.get(m.split(":")[0], "#3498DB") for m in models]
        # Map model names to short labels
        labels = [m.replace("llama3.2:", "llama3.2\n") for m in models]

        axes[0].bar(labels, counts, color=bar_colors, edgecolor="white")
        axes[0].set_title("Queries per Model")
        axes[0].set_ylabel("Number of Queries")
        for i, (cnt, lbl) in enumerate(zip(counts, labels)):
            axes[0].text(i, cnt + 0.3, str(cnt), ha="center", fontsize=10)

        total = sum(counts)
        pcts = [c / total * 100 for c in counts]
        wedges, texts, autotexts = axes[1].pie(
            counts, labels=labels, autopct="%1.1f%%",
            colors=bar_colors, startangle=140,
        )
        axes[1].set_title("Routing Distribution (%)")

    plt.tight_layout()
    for ext in ["png", "svg"]:
        p = out_dir / f"fig5_routing_distribution.{ext}"
        plt.savefig(p, bbox_inches="tight")
        saved.append(p)
    plt.close()

    # ------------------------------------------------------------------
    # Figure 6: Sleep-State Statistics (4-metric informational panel)
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("Figure 6: Power Management Sleep-State Statistics", fontweight="bold")
    axes = axes.flatten()

    sleep_events  = [s for s in sleep_logs if s["state"] == "SLEEP"]
    wakeup_events = [s for s in sleep_logs if s["state"] == "WAKEUP"]
    sleep_durs    = [s["duration_sec"] for s in sleep_events  if s.get("duration_sec")]
    wakeup_durs   = [s["duration_sec"] for s in wakeup_events if s.get("duration_sec")]

    total_sleep_s  = sum(sleep_durs)
    total_active_s = sum(r["latency_ms"] / 1000 for r in camas_perf)
    total_wall_s   = total_active_s + total_sleep_s
    idle_pct       = (total_sleep_s / total_wall_s * 100) if total_wall_s > 0 else 0
    # Idle energy saved: assume model idle power = phi3 CPU watts × sleep time
    idle_power_w   = 12.0
    energy_saved_wh = idle_power_w * total_sleep_s / 3600
    avg_wakeup_ms  = statistics.mean(wakeup_durs) * 1000 if wakeup_durs else 0

    # Panel 1: Active vs Sleep time stacked bar
    ax = axes[0]
    ax.bar(["Orchestrator"], [total_active_s], color=COLORS["active"],  label="Active",  width=0.4)
    ax.bar(["Orchestrator"], [total_sleep_s],  color=COLORS["sleep"],   label="Sleep",   width=0.4,
           bottom=[total_active_s])
    ax.set_ylabel("Duration (s)")
    ax.set_title(f"Active vs Sleep Time\n(Total sleep: {total_sleep_s:.1f}s)")
    ax.legend()
    ax.text(0, total_active_s + total_sleep_s + 2, f"{idle_pct:.1f}% idle",
            ha="center", fontsize=11, fontweight="bold", color=COLORS["sleep"])

    # Panel 2: Sleep event durations
    ax = axes[1]
    if sleep_durs:
        ax.bar(range(1, len(sleep_durs) + 1), sleep_durs,
               color=COLORS["sleep"], edgecolor="white", width=0.6)
        ax.axhline(statistics.mean(sleep_durs), color="#333", linestyle="--",
                   linewidth=1.2, label=f"Mean: {statistics.mean(sleep_durs):.1f}s")
        ax.legend()
    ax.set_xlabel("Sleep Event #")
    ax.set_ylabel("Duration (s)")
    ax.set_title(f"Sleep Event Durations\n({len(sleep_durs)} events, avg {statistics.mean(sleep_durs) if sleep_durs else 0:.1f}s)")
    ax.set_xticks(range(1, len(sleep_durs) + 1))

    # Panel 3: Idle time % vs active time %
    ax = axes[2]
    wedge_data  = [total_active_s, total_sleep_s]
    wedge_labels = [f"Active\n{total_active_s:.0f}s", f"Sleep\n{total_sleep_s:.0f}s"]
    ax.pie(wedge_data, labels=wedge_labels,
           colors=[COLORS["active"], COLORS["sleep"]],
           autopct="%1.1f%%", startangle=90)
    ax.set_title(f"Time Distribution\n(Idle energy saved: {energy_saved_wh:.4f} Wh)")

    # Panel 4: Sleep/Wakeup counts + avg wakeup overhead
    ax = axes[3]
    metrics_labels = ["Sleep\nEvents", "Wakeup\nEvents", "Avg Wakeup\nOverhead (ms)"]
    metrics_vals   = [len(sleep_durs), len(wakeup_durs), avg_wakeup_ms]
    bars = ax.bar(metrics_labels, metrics_vals,
                  color=[COLORS["sleep"], COLORS["active"], COLORS["complex"]],
                  edgecolor="white", width=0.5)
    for bar, val in zip(bars, metrics_vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.04,
                f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_title("Transition Counts & Overhead")
    ax.set_ylabel("Count / ms")

    plt.tight_layout()
    for ext in ["png", "svg"]:
        p = out_dir / f"fig6_sleep_statistics.{ext}"
        plt.savefig(p, bbox_inches="tight")
        saved.append(p)
    plt.close()

    logger.info(f"Generated {len(saved)} visualization files")
    return saved
