#!/usr/bin/env python3
"""
XHAIL Benchmark Runner
======================

Runs all benchmark tasks in experiments/benchmarks/, records metrics, and
exports results to experiments/results/results.csv and results.json.

Usage
-----
    python experiments/run_benchmarks.py                  # all benchmarks
    python experiments/run_benchmarks.py --benchmark penguins
    python experiments/run_benchmarks.py --seed 42 --depth 10 --timeout 30

Output
------
    experiments/results/results.csv   — flat metrics table (append mode)
    experiments/results/results.json  — full structured results
    experiments/results/latest.json   — result of the most recent run only

Metrics recorded per benchmark
-------------------------------
    benchmark       benchmark name (stem of .lp file)
    success         whether a hypothesis was found
    n_rules         number of rules in the learned hypothesis
    n_examples      number of examples in the task
    n_background    number of background clauses
    runtime_s       wall-clock time for learn() in seconds
    peak_memory_mb  peak RSS memory during learn() in MiB
    rule_complexity mean number of body literals per rule (0 for facts)
    hypothesis      learned rules joined by ' | '
    seed            random seed used (for future stochastic extensions)
    depth           deduction depth parameter
    timestamp       ISO-8601 UTC timestamp of the run
"""

from __future__ import annotations

import argparse
import csv
import json
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure the repo root is on sys.path so xhail imports work when running
# the script from any directory.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from xhail import LearningResult, learn  # noqa: E402  (after sys.path manipulation)

BENCHMARKS_DIR = REPO_ROOT / "experiments" / "benchmarks"
RESULTS_DIR = REPO_ROOT / "experiments" / "results"


# ---------------------------------------------------------------------------
# Metrics helpers
# ---------------------------------------------------------------------------


def _peak_memory_mb() -> float:
    """Return peak RSS memory usage of this process in MiB (Linux/macOS)."""
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Linux reports bytes; macOS reports bytes too (both as int)
    # resource.ru_maxrss is in kilobytes on Linux, bytes on macOS
    if sys.platform == "darwin":
        return usage / (1024 ** 2)
    return usage / 1024  # Linux: kb → MiB


def _rule_complexity(result: LearningResult) -> float:
    """Mean number of body literals per learned rule.

    Facts (rules with no body, e.g. ``p.`` or ``p :- .``) contribute 0.
    Returns 0.0 if no hypothesis was found.
    """
    if not result.hypothesis:
        return 0.0
    counts = []
    for rule in result.hypothesis:
        if ":-" not in rule:
            counts.append(0)
        else:
            body = rule.split(":-", 1)[1].rstrip(". \n")
            # strip whitespace; empty body is a fact
            body = body.strip()
            if not body:
                counts.append(0)
            else:
                counts.append(len(body.split(",")))
    return sum(counts) / len(counts)


# ---------------------------------------------------------------------------
# Single benchmark run
# ---------------------------------------------------------------------------


def run_benchmark(
    lp_path: Path,
    depth: int = 10,
    seed: int = 0,
) -> dict:
    """Run a single benchmark and return a metrics dict."""
    mem_before = _peak_memory_mb()
    t0 = time.perf_counter()

    try:
        result = learn(lp_path, depth=depth)
        error = None
    except Exception as exc:
        result = LearningResult()
        error = f"{type(exc).__name__}: {exc}"

    elapsed = time.perf_counter() - t0
    mem_after = _peak_memory_mb()

    hypothesis_str = " | ".join(result.hypothesis) if result.hypothesis else ""

    return {
        "benchmark": lp_path.stem,
        "success": result.success,
        "n_rules": len(result.hypothesis),
        "n_examples": result.n_examples,
        "n_background": result.n_background,
        "runtime_s": round(elapsed, 4),
        "peak_memory_mb": round(max(mem_after - mem_before, 0.0), 2),
        "rule_complexity": round(_rule_complexity(result), 3),
        "hypothesis": hypothesis_str,
        "error": error or "",
        "seed": seed,
        "depth": depth,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


CSV_FIELDS = [
    "benchmark", "success", "n_rules", "n_examples", "n_background",
    "runtime_s", "peak_memory_mb", "rule_complexity", "hypothesis",
    "error", "seed", "depth", "timestamp",
]


def write_csv(rows: list[dict], path: Path, append: bool = True) -> None:
    """Append (or create) a CSV results file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if (append and path.exists()) else "w"
    with path.open(mode, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if mode == "w":
            writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict], path: Path) -> None:
    """Overwrite a JSON results file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(rows, f, indent=2)


def print_summary(rows: list[dict]) -> None:
    """Print a human-readable results table to stdout."""
    header = f"{'Benchmark':<18} {'OK':>4} {'Rules':>5} {'Time(s)':>8} {'Mem(MB)':>8}  Hypothesis"
    sep = "-" * 80
    print(sep)
    print(header)
    print(sep)
    for r in rows:
        ok = "✓" if r["success"] else "✗"
        err = f"  ERROR: {r['error']}" if r["error"] else ""
        print(
            f"{r['benchmark']:<18} {ok:>4} {r['n_rules']:>5} "
            f"{r['runtime_s']:>8.3f} {r['peak_memory_mb']:>8.2f}  "
            f"{r['hypothesis'][:50]}{err}"
        )
    print(sep)
    n_ok = sum(1 for r in rows if r["success"])
    total_time = sum(r["runtime_s"] for r in rows)
    print(f"  {n_ok}/{len(rows)} benchmarks solved  |  total time: {total_time:.3f}s")
    print(sep)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run XHAIL benchmarks and record metrics.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--benchmark",
        metavar="NAME",
        help="Run only this benchmark (stem of .lp file, e.g. 'penguins'). "
             "Omit to run all.",
    )
    p.add_argument("--depth", type=int, default=10, help="Deduction depth.")
    p.add_argument("--seed", type=int, default=0, help="Random seed (reserved for future use).")
    p.add_argument("--timeout", type=float, default=60.0, help="Per-benchmark timeout in seconds.")
    p.add_argument(
        "--no-append",
        action="store_true",
        help="Overwrite results.csv instead of appending.",
    )
    p.add_argument(
        "--results-dir",
        type=Path,
        default=RESULTS_DIR,
        help="Directory to write results into.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # Discover benchmarks
    if args.benchmark:
        lp_files = [BENCHMARKS_DIR / f"{args.benchmark}.lp"]
        if not lp_files[0].exists():
            print(f"ERROR: benchmark file not found: {lp_files[0]}", file=sys.stderr)
            sys.exit(1)
    else:
        lp_files = sorted(BENCHMARKS_DIR.glob("*.lp"))
        if not lp_files:
            print(f"No .lp files found in {BENCHMARKS_DIR}", file=sys.stderr)
            sys.exit(1)

    print(f"Running {len(lp_files)} benchmark(s) [depth={args.depth}, seed={args.seed}]")

    rows: list[dict] = []
    for lp in lp_files:
        print(f"  {lp.stem}...", end=" ", flush=True)
        row = run_benchmark(lp, depth=args.depth, seed=args.seed)
        rows.append(row)
        status = "OK" if row["success"] else ("ERROR" if row["error"] else "NO HYP")
        print(f"{status}  ({row['runtime_s']:.3f}s)")

    # Write results
    results_dir = args.results_dir
    csv_path = results_dir / "results.csv"
    json_path = results_dir / "results.json"
    latest_path = results_dir / "latest.json"

    write_csv(rows, csv_path, append=not args.no_append)
    # Merge with existing JSON for full history
    existing: list[dict] = []
    if json_path.exists() and not args.no_append:
        with json_path.open() as f:
            existing = json.load(f)
    write_json(existing + rows, json_path)
    write_json(rows, latest_path)

    print(f"\nResults written to {results_dir}/")
    print_summary(rows)


if __name__ == "__main__":
    main()
