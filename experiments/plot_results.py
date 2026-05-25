#!/usr/bin/env python3
"""
XHAIL Results Visualiser
========================

Reads experiments/results/results.csv (produced by run_benchmarks.py) and
generates publication-quality figures saved to experiments/results/figures/.

Usage
-----
    python experiments/plot_results.py
    python experiments/plot_results.py --results-dir experiments/results
    python experiments/plot_results.py --format pdf   # or png (default)

Figures produced
----------------
    runtime_bar.png          Wall-clock time per benchmark (bar chart)
    rule_complexity_bar.png  Mean body-literal count per benchmark
    memory_bar.png           Peak RSS memory usage per benchmark
    summary_table.png        All metrics rendered as a table image
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

RESULTS_DIR = REPO_ROOT / "experiments" / "results"
FIGURES_DIR = RESULTS_DIR / "figures"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_latest(results_dir: Path) -> list[dict]:
    """Load the most recent run from results.csv (highest timestamp per benchmark)."""
    csv_path = results_dir / "results.csv"
    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found. Run run_benchmarks.py first.", file=sys.stderr)
        sys.exit(1)

    rows: list[dict] = []
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("ERROR: results.csv is empty.", file=sys.stderr)
        sys.exit(1)

    # Keep only the latest run per benchmark (highest timestamp)
    latest: dict[str, dict] = {}
    for row in rows:
        name = row["benchmark"]
        if name not in latest or row["timestamp"] > latest[name]["timestamp"]:
            latest[name] = row

    return list(latest.values())


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------


def _setup_style(plt) -> None:
    """Apply a clean, publication-friendly style."""
    plt.rcParams.update({
        "figure.dpi": 150,
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linestyle": "--",
    })


PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]


def plot_runtime(rows: list[dict], out_dir: Path, fmt: str) -> Path:
    import matplotlib.pyplot as plt

    _setup_style(plt)
    names = [r["benchmark"] for r in rows]
    times = [float(r["runtime_s"]) for r in rows]
    colours = [PALETTE[i % len(PALETTE)] for i in range(len(names))]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(names, times, color=colours, edgecolor="white", height=0.55)
    ax.bar_label(bars, fmt="%.3fs", padding=4, fontsize=9)
    ax.set_xlabel("Wall-clock time (seconds)")
    ax.set_title("XHAIL Benchmark Runtime", fontweight="bold")
    ax.set_xlim(0, max(times) * 1.25)
    fig.tight_layout()

    out = out_dir / f"runtime_bar.{fmt}"
    fig.savefig(out)
    plt.close(fig)
    return out


def plot_rule_complexity(rows: list[dict], out_dir: Path, fmt: str) -> Path:
    import matplotlib.pyplot as plt

    _setup_style(plt)
    names = [r["benchmark"] for r in rows]
    complexities = [float(r["rule_complexity"]) for r in rows]
    colours = [PALETTE[i % len(PALETTE)] for i in range(len(names))]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(names, complexities, color=colours, edgecolor="white", height=0.55)
    ax.bar_label(bars, fmt="%.1f", padding=4, fontsize=9)
    ax.set_xlabel("Mean body literals per rule")
    ax.set_title("XHAIL Rule Complexity", fontweight="bold")
    ax.set_xlim(0, max(complexities) * 1.4 if max(complexities) > 0 else 2)
    fig.tight_layout()

    out = out_dir / f"rule_complexity_bar.{fmt}"
    fig.savefig(out)
    plt.close(fig)
    return out


def plot_memory(rows: list[dict], out_dir: Path, fmt: str) -> Path:
    import matplotlib.pyplot as plt

    _setup_style(plt)
    names = [r["benchmark"] for r in rows]
    mems = [float(r["peak_memory_mb"]) for r in rows]
    colours = [PALETTE[i % len(PALETTE)] for i in range(len(names))]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(names, mems, color=colours, edgecolor="white", height=0.55)
    ax.bar_label(bars, fmt="%.2f MB", padding=4, fontsize=9)
    ax.set_xlabel("Peak RSS memory (MiB)")
    ax.set_title("XHAIL Peak Memory Usage", fontweight="bold")
    ax.set_xlim(0, max(mems) * 1.35 if max(mems) > 0 else 10)
    fig.tight_layout()

    out = out_dir / f"memory_bar.{fmt}"
    fig.savefig(out)
    plt.close(fig)
    return out


def plot_summary_table(rows: list[dict], out_dir: Path, fmt: str) -> Path:
    import matplotlib.pyplot as plt

    _setup_style(plt)

    col_labels = ["Benchmark", "✓", "Rules", "Examples", "Time (s)", "Complexity", "Hypothesis"]
    table_data = []
    for r in rows:
        ok = "✓" if r["success"] == "True" else "✗"
        hyp = r["hypothesis"][:40] + "…" if len(r["hypothesis"]) > 40 else r["hypothesis"]
        table_data.append([
            r["benchmark"], ok, r["n_rules"], r["n_examples"],
            f"{float(r['runtime_s']):.3f}", f"{float(r['rule_complexity']):.1f}", hyp,
        ])

    fig, ax = plt.subplots(figsize=(13, 1.2 + 0.45 * len(rows)))
    ax.axis("off")
    tbl = ax.table(
        cellText=table_data,
        colLabels=col_labels,
        loc="center",
        cellLoc="left",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.6)

    # Style header row
    for j in range(len(col_labels)):
        tbl[(0, j)].set_facecolor("#4C72B0")
        tbl[(0, j)].set_text_props(color="white", fontweight="bold")

    # Alternating row colours
    for i in range(1, len(rows) + 1):
        for j in range(len(col_labels)):
            tbl[(i, j)].set_facecolor("#F0F4FA" if i % 2 == 0 else "white")

    ax.set_title("XHAIL Benchmark Summary", fontweight="bold", pad=16, fontsize=12)
    fig.tight_layout()

    out = out_dir / f"summary_table.{fmt}"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Visualise XHAIL benchmark results.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--results-dir", type=Path, default=RESULTS_DIR,
        help="Directory containing results.csv",
    )
    p.add_argument(
        "--format", choices=["png", "pdf", "svg"], default="png",
        help="Output figure format",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    try:
        import matplotlib  # noqa: F401
    except ImportError:
        print(
            "matplotlib is required for plotting.\n"
            "Install it with: pip install matplotlib --break-system-packages",
            file=sys.stderr,
        )
        sys.exit(1)

    rows = load_latest(args.results_dir)
    out_dir = args.results_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    fmt = args.format
    produced = []
    produced.append(plot_runtime(rows, out_dir, fmt))
    produced.append(plot_rule_complexity(rows, out_dir, fmt))
    produced.append(plot_memory(rows, out_dir, fmt))
    produced.append(plot_summary_table(rows, out_dir, fmt))

    print(f"Figures written to {out_dir}/")
    for p in produced:
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
