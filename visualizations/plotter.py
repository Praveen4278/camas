"""
CAMAS Visualization Module
Generates publication-quality graphs for IEEE paper inclusion.
"""

import logging
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)


def generate_all_plots(baseline_data: dict, camas_data: dict, output_dir: str = None):
    """
    Generate all 6 publication-quality visualizations.
    
    Args:
        baseline_data: dict from memory_agent.get_experiment_summary()
        camas_data: dict from memory_agent.get_experiment_summary()
        output_dir: output directory path
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import numpy as np
    except ImportError:
        logger.error("[Viz] matplotlib not installed.")
        return {}

    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "visualizations"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Publication style
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "legend.framealpha": 0.8,
    })

    COLORS = {
        "baseline": "#E05C5C",
        "camas": "#2E86AB",
        "highlight": "#F4A261",
        "neutral": "#6C757D",
        "phi3": "#52B788",
        "medium": "#2E86AB",
        "complex": "#E05C5C",
    }

    generated = {}

    # ── Helper ────────────────────────────────────────────────────────────────
    def save(fig, name):
        for ext in ["png", "svg"]:
            p = output_dir / f"{name}.{ext}"
            fig.savefig(str(p))
        plt.close(fig)
        generated[name] = str(output_dir / f"{name}.png")
        logger.info(f"[Viz] Saved {name}.png and {name}.svg")

    def safe(d, key, default=0.0):
        v = d.get(key)
        return float(v) if v is not None else default

    # ── Figure 1: Energy Comparison ──────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle("Figure 1: Energy Consumption — Baseline vs. CAMAS", fontweight="bold")

    # Total energy
    ax = axes[0]
    vals = [safe(baseline_data, "total_energy") * 1000,
            safe(camas_data, "total_energy") * 1000]  # Convert to Wh
    bars = ax.bar(["Baseline\n(llama3.2:8b)", "CAMAS\n(Dynamic Routing)"],
                  vals, color=[COLORS["baseline"], COLORS["camas"]], width=0.5,
                  edgecolor="white", linewidth=1.5)
    ax.set_ylabel("Total Energy (Wh)")
    ax.set_title("Total Experiment Energy")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001*max(vals),
                f"{val:.4f}", ha="center", va="bottom", fontweight="bold")
    if vals[0] > 0:
        pct = (vals[1] - vals[0]) / vals[0] * 100
        ax.text(0.98, 0.95, f"Δ {pct:+.1f}%", transform=ax.transAxes,
                ha="right", va="top", color=COLORS["camas"] if pct < 0 else COLORS["baseline"],
                fontsize=12, fontweight="bold")

    # Per-query energy
    ax = axes[1]
    vals = [safe(baseline_data, "avg_energy") * 1e6,
            safe(camas_data, "avg_energy") * 1e6]  # µWh
    bars = ax.bar(["Baseline", "CAMAS"], vals,
                  color=[COLORS["baseline"], COLORS["camas"]], width=0.5,
                  edgecolor="white", linewidth=1.5)
    ax.set_ylabel("Avg. Energy per Query (µWh)")
    ax.set_title("Per-Query Energy Consumption")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001*max(vals, default=1),
                f"{val:.2f}", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    save(fig, "fig1_energy_comparison")

    # ── Figure 2: Carbon Comparison ───────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle("Figure 2: Carbon Emissions — Baseline vs. CAMAS", fontweight="bold")

    ax = axes[0]
    vals = [safe(baseline_data, "total_co2") * 1000,
            safe(camas_data, "total_co2") * 1000]  # g CO2
    bars = ax.bar(["Baseline", "CAMAS"], vals,
                  color=[COLORS["baseline"], COLORS["camas"]], width=0.5,
                  edgecolor="white", linewidth=1.5)
    ax.set_ylabel("Total CO₂ Emissions (g)")
    ax.set_title("Total CO₂ Emissions")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0001*max(vals, default=1),
                f"{val:.4f}g", ha="center", va="bottom", fontweight="bold")
    if vals[0] > 0:
        pct = (vals[1] - vals[0]) / vals[0] * 100
        ax.text(0.98, 0.95, f"Δ {pct:+.1f}%", transform=ax.transAxes,
                ha="right", va="top", fontsize=12, fontweight="bold",
                color=COLORS["camas"] if pct < 0 else COLORS["baseline"])

    ax = axes[1]
    vals = [safe(baseline_data, "avg_co2") * 1e6,
            safe(camas_data, "avg_co2") * 1e6]  # µg CO2
    bars = ax.bar(["Baseline", "CAMAS"], vals,
                  color=[COLORS["baseline"], COLORS["camas"]], width=0.5,
                  edgecolor="white", linewidth=1.5)
    ax.set_ylabel("Avg. CO₂ per Query (µg)")
    ax.set_title("Per-Query Carbon Footprint")
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001*max(vals, default=1),
                f"{val:.2f}", ha="center", va="bottom", fontweight="bold")

    plt.tight_layout()
    save(fig, "fig2_carbon_comparison")

    # ── Figure 3: Latency Comparison ─────────────────────────────────────────
    from database import get_connection
    conn = get_connection()
    try:
        cursor = conn.cursor()
        b_latencies, c_latencies = [], []
        for eid, lst in [(baseline_data.get("experiment_id"), b_latencies),
                         (camas_data.get("experiment_id"), c_latencies)]:
            if eid:
                cursor.execute("SELECT latency_ms FROM performance_logs WHERE experiment_id=?", (eid,))
                lst.extend([row[0] for row in cursor.fetchall() if row[0]])
    finally:
        conn.close()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 3: Latency Distribution — Baseline vs. CAMAS", fontweight="bold")

    # Box plot
    ax = axes[0]
    data_to_plot = [b_latencies or [0], c_latencies or [0]]
    bp = ax.boxplot(data_to_plot, labels=["Baseline", "CAMAS"],
                    patch_artist=True, notch=False, widths=0.5)
    for patch, color in zip(bp["boxes"], [COLORS["baseline"], COLORS["camas"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_ylabel("Latency (ms)")
    ax.set_title("Latency Distribution (Box Plot)")

    # Histogram
    ax = axes[1]
    if b_latencies:
        ax.hist(b_latencies, bins=20, alpha=0.6, color=COLORS["baseline"],
                label="Baseline", density=True)
    if c_latencies:
        ax.hist(c_latencies, bins=20, alpha=0.6, color=COLORS["camas"],
                label="CAMAS", density=True)
    ax.set_xlabel("Latency (ms)")
    ax.set_ylabel("Density")
    ax.set_title("Latency Histogram")
    ax.legend()

    plt.tight_layout()
    save(fig, "fig3_latency_comparison")

    # ── Figure 4: Cost Comparison ─────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle("Figure 4: Operational Cost — Baseline vs. CAMAS", fontweight="bold")

    categories = ["Total Cost (USD)", "Avg. Cost/Query (USD)"]
    b_vals = [safe(baseline_data, "total_cost"), safe(baseline_data, "avg_cost")]
    c_vals = [safe(camas_data, "total_cost"), safe(camas_data, "avg_cost")]

    x = range(len(categories))
    width = 0.35
    bars1 = ax.bar([i - width/2 for i in x], b_vals, width,
                   label="Baseline", color=COLORS["baseline"], alpha=0.85)
    bars2 = ax.bar([i + width/2 for i in x], c_vals, width,
                   label="CAMAS", color=COLORS["camas"], alpha=0.85)
    ax.set_xticks(list(x))
    ax.set_xticklabels(categories)
    ax.set_ylabel("Cost (USD)")
    ax.legend()
    ax.set_title("Cost Comparison")

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.000001,
                    f"${h:.5f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    save(fig, "fig4_cost_comparison")

    # ── Figure 5: Routing Distribution ───────────────────────────────────────
    from database import get_connection
    conn = get_connection()
    try:
        cursor = conn.cursor()
        camas_eid = camas_data.get("experiment_id", "")
        cursor.execute("""
            SELECT selected_model, COUNT(*) as n
            FROM routing_logs WHERE experiment_id=?
            GROUP BY selected_model
        """, (camas_eid,))
        routing_rows = cursor.fetchall()
    finally:
        conn.close()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 5: Model Routing Distribution (CAMAS)", fontweight="bold")

    if routing_rows:
        models = [r[0] for r in routing_rows]
        counts = [r[1] for r in routing_rows]
        colors = []
        for m in models:
            if "phi3" in m:
                colors.append(COLORS["phi3"])
            elif "3b" in m:
                colors.append(COLORS["medium"])
            else:
                colors.append(COLORS["complex"])

        # Pie
        ax = axes[0]
        wedges, texts, autotexts = ax.pie(
            counts, labels=models, colors=colors, autopct="%1.1f%%",
            startangle=90, pctdistance=0.8
        )
        for at in autotexts:
            at.set_fontweight("bold")
        ax.set_title("Routing by Model (Pie)")

        # Bar
        ax = axes[1]
        bars = ax.bar(models, counts, color=colors, width=0.5,
                      edgecolor="white", linewidth=1.5)
        ax.set_ylabel("Number of Queries")
        ax.set_title("Routing by Model (Count)")
        ax.set_xlabel("Selected Model")
        for bar, cnt in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(cnt), ha="center", va="bottom", fontweight="bold")
    else:
        for ax in axes:
            ax.text(0.5, 0.5, "No routing data", transform=ax.transAxes,
                    ha="center", va="center")

    plt.tight_layout()
    save(fig, "fig5_routing_distribution")

    # ── Figure 6: Sleep-State Statistics ─────────────────────────────────────
    from database import get_connection
    conn = get_connection()
    try:
        cursor = conn.cursor()
        camas_eid = camas_data.get("experiment_id", "")
        cursor.execute("""
            SELECT agent_name,
                   SUM(CASE WHEN state='ACTIVE' THEN duration_seconds ELSE 0 END) as active_s,
                   SUM(CASE WHEN state='SLEEP' THEN duration_seconds ELSE 0 END) as sleep_s,
                   COUNT(CASE WHEN state='ACTIVE' THEN 1 END) as wakeups
            FROM sleep_logs WHERE experiment_id=?
            GROUP BY agent_name
        """, (camas_eid,))
        sleep_rows = cursor.fetchall()
    finally:
        conn.close()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 6: Agent Sleep-State Statistics (CAMAS)", fontweight="bold")

    if sleep_rows:
        agents = [r[0] for r in sleep_rows]
        actives = [r[1] or 0 for r in sleep_rows]
        sleeps = [r[2] or 0 for r in sleep_rows]
        wakeups = [r[3] or 0 for r in sleep_rows]

        # Stacked bar: active vs sleep
        ax = axes[0]
        x = range(len(agents))
        ax.bar(x, actives, label="Active", color=COLORS["camas"], alpha=0.85)
        ax.bar(x, sleeps, bottom=actives, label="Sleep", color=COLORS["neutral"], alpha=0.7)
        ax.set_xticks(list(x))
        ax.set_xticklabels(agents, rotation=15)
        ax.set_ylabel("Duration (s)")
        ax.set_title("Active vs. Sleep Time per Agent")
        ax.legend()

        # Wakeup bar
        ax = axes[1]
        bars = ax.bar(agents, wakeups, color=COLORS["highlight"],
                      width=0.5, edgecolor="white")
        ax.set_ylabel("Number of Wakeups")
        ax.set_title("Agent Wakeup Count")
        ax.set_xlabel("Agent")
        for bar, wk in zip(bars, wakeups):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(wk), ha="center", va="bottom", fontweight="bold")
    else:
        axes[0].text(0.5, 0.5, "No sleep state data\n(agents may not have entered sleep)",
                     transform=axes[0].transAxes, ha="center", va="center")
        axes[1].text(0.5, 0.5, "No wakeup data",
                     transform=axes[1].transAxes, ha="center", va="center")

    plt.tight_layout()
    save(fig, "fig6_sleep_state_statistics")

    logger.info(f"[Viz] Generated {len(generated)} figures in {output_dir}")
    return generated
