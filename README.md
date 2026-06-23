# XHAIL — eXtended Hybrid Abductive Inductive Learning

[![CI](https://github.com/everettmakes/xhail/actions/workflows/ci.yml/badge.svg)](https://github.com/everettmakes/xhail/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/everettmakes/xhail/branch/main/graph/badge.svg)](https://codecov.io/gh/everettmakes/xhail)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A research-grade Python implementation of the XHAIL Inductive Logic Programming framework, built on [clingo](https://potassco.org/clingo/) 5.6+.

XHAIL learns **interpretable logic-program rules** from background knowledge and examples. Given observations, it produces human-readable hypotheses that are sound with respect to the background knowledge — no gradient descent, no black-box parameters. The learned rules can be read, verified, and extended by domain experts.

```prolog
% Input: background knowledge + examples
bird(a). bird(b). bird(c). penguin(d).
bird(X) :- penguin(X).
#modeh flies(+bird).
#modeb not penguin(+bird).
#example flies(a). #example not flies(d).

% Output: learned hypothesis (< 5 ms)
flies(V1) :- not penguin(V1).
```

---

## Contents

- [Motivation](#motivation)
- [How it works](#how-it-works)
- [Benchmark results](#benchmark-results)
- [Installation](#installation)
- [Usage](#usage)
- [Input format](#input-format)
- [Repository layout](#repository-layout)
- [Engineering notes](#engineering-notes)
- [Comparison to other ILP systems](#comparison-to-other-ilp-systems)
- [Roadmap](#roadmap)
- [Citation](#citation)

---

## Motivation

Statistical ML excels at pattern recognition but produces models that are opaque, brittle under distribution shift, and unable to incorporate prior symbolic knowledge. Inductive Logic Programming (ILP) takes the complementary path: it searches the space of logic programs and returns the simplest hypothesis that is logically consistent with the observations.

XHAIL's specific approach — **abduction followed by deduction followed by induction**, all implemented as Answer Set Programming (ASP) solve calls — gives it three properties that matter for real research:

1. **Transparency.** Each intermediate result (the abduced atom set Δ, the kernel set K, the final hypothesis H) is a first-class artefact. You can inspect, checkpoint, and debug each phase independently.
2. **Expressiveness.** Because the language is Answer Set Programming, XHAIL handles negation-as-failure, integrity constraints, and non-monotonic reasoning natively — things that classical ILP systems (Aleph, Metagol) cannot express.
3. **Correctness guarantees.** The hypothesis is guaranteed to cover every positive example and violate no negative example, by construction.

---

## How it works

XHAIL decomposes hypothesis search into three focused solve calls:

```
Input (.lp file)
│
├─ Background knowledge (BG) — domain axioms, type facts, integrity constraints
├─ Mode declarations (#modeh / #modeb) — define the hypothesis language
└─ Examples (#example) — positive and negative observations
│
▼
╔══════════════════════════════════════════════════════════════╗
║  Phase 1 · Abduction                                         ║
║                                                              ║
║  Find the minimal set of ground atoms Δ (consistent with BG) ║
║  such that BG ∪ Δ satisfies every example.                   ║
║                                                              ║
║  Δ = { happens(infect(bob),1), happens(infect(carol),2) }   ║
╚══════════════════════════════════════════════════════════════╝
│
▼
╔══════════════════════════════════════════════════════════════╗
║  Phase 2 · Deduction — BFS kernel construction               ║
║                                                              ║
║  Build the kernel set K: one maximally-specific clause per   ║
║  leaf of a BFS over (abduced atoms × mode schemas).          ║
║  Parent-pointer reconstruction gives O(depth) chain recall.  ║
║  Full ancestor tracking prevents BFS cycles in O(1) per step.║
║                                                              ║
║  K = { happens(infect(bob),T)  :- holdsAt(ill(alice),T),    ║
║         happens(infect(carol),T) :- holdsAt(ill(bob),T), … } ║
╚══════════════════════════════════════════════════════════════╝
│
▼
╔══════════════════════════════════════════════════════════════╗
║  Phase 3 · Induction                                         ║
║                                                              ║
║  Search for the smallest subset H ⊆ K (by literal count)    ║
║  such that BG ∪ H covers every positive example and          ║
║  violates no negative example. Solved with a clingo          ║
║  optimisation program (minimize{use(I,J)}).                  ║
║                                                              ║
║  H = { happens(infect(bob),V1)   :- holdsAt(ill(alice),V1). ║
║         happens(infect(carol),V1) :- holdsAt(ill(bob),V1).  }║
╚══════════════════════════════════════════════════════════════╝
│
▼
Learned hypothesis — printed to stdout or returned via Python API
```

---

## Benchmark results

The suite covers ten canonical ILP tasks across classical logic, Event Calculus, negation-as-failure, and multi-body reasoning. Timings on Python 3.11, clingo 5.7, 4-core laptop (wall time measured with `--jobs 4`).

| Benchmark | Domain | Rules | CPU time | Notes |
|---|---|:---:|---:|---|
| `animals` | Classification | 1 | 6 ms | `mammal(V1) :- produces_milk(V1).` |
| `blocks` | Event Calculus | 2 | 8 ms | pick_up / put_down rules |
| `epidemic` | Event Calculus | 2 | 9 ms | Chained infection cascade, NAF temporal negatives |
| `event_calculus` | Event Calculus | 1 | 8 ms | `happens(work(alice),V1) :- holdsAt(awake(alice),V1).` |
| `grandfather` | Recursive relations | 1 | 41 ms | 2-literal chain; predicate-indexed BFS |
| `penguins` | NAF / exceptions | 1 | 2 ms | `flies(V1) :- not penguin(V1).` |
| `propositional` | Propositional | 1 | 4 ms | `output :- .` (zero-arity rule) |
| `sugar` | Event Calculus | 2 | 7 ms | Priority-ordered resource consumption, NAF |
| `traffic` | Rules | 1 | 4 ms | `stop(V1) :- red(V1).` |
| `trains` | Structural | 1 | 28 ms | 3-body rule; induction selects subset of kernel |
| **Total** | | **13** | **117 ms CPU / 58 ms wall** | 10 / 10 solved |

Reproduce with:

```bash
python experiments/run_benchmarks.py           # parallel (default: all cores)
python experiments/run_benchmarks.py --jobs 1  # sequential, for profiling
```

---

## Installation

Requires **Python ≥ 3.10**. The `clingo` ASP solver is installed automatically as a Python wheel.

```bash
git clone https://github.com/everettmakes/xhail.git
cd xhail
pip install -e ".[dev]"
```

Verify:

```bash
xhail --version
xhail run experiments/benchmarks/penguins.lp
# flies(V1) :- not penguin(V1).
```

---

## Usage

### Command line

```bash
# Run the learner on any .lp file
xhail run myfile.lp

# Increase deduction depth (default 10) for deeper rule bodies
xhail run myfile.lp --depth 15

# Show phase-by-phase progress
xhail run myfile.lp --verbose

# Write intermediate ASP programs to disk for debugging
xhail run myfile.lp --debug --debug-output ./debug_out/
```

### Python API

```python
from xhail import learn

result = learn("experiments/benchmarks/trains.lp", depth=10)

print(result.success)          # True
print(result.n_rules)          # 1
for rule in result.hypothesis:
    print(rule)
# eastbound(V1) :- has_car(V1,V2), triangle_load(V2), rectangle(V2).

print(repr(result))
# LearningResult(success=True, n_rules=1, source='experiments/benchmarks/trains.lp')
```

The `learn()` function is the single public entry point. It is thread-safe: each call creates a fresh `Model` instance with no shared mutable state.

---

## Input format

XHAIL input files are Answer Set Programs (`.lp`) with three additional directives:

```prolog
% ── Background knowledge ──────────────────────────────────────
% Any valid ASP rules, facts, and integrity constraints.
bird(a). bird(b). bird(c).
penguin(d).
bird(X) :- penguin(X).

% ── Mode declarations ─────────────────────────────────────────
% #modeh  defines allowed head predicates.
% #modeb  defines allowed body predicates.
% Placemarkers:
%   +type   input variable  — must be grounded by a prior term
%   -type   output variable — introduced by this literal
%   #type   ground constant — appears literally in the hypothesis
#modeh flies(+bird).
#modeb penguin(+bird).
#modeb not penguin(+bird).    % negation-as-failure body literal

% ── Examples ──────────────────────────────────────────────────
#example flies(a).             % positive: must be entailed by H
#example flies(b).
#example flies(c).
#example not flies(d).         % negative: must NOT be entailed by H
```

### Placemarker reference

| Marker | Role | Effect |
|--------|------|--------|
| `+type` | Input variable | Must be grounded by the head or a prior body literal. Introduces a typed existential variable `V1`, `V2`, … |
| `-type` | Output variable | Introduced by this literal; can be used downstream. |
| `#type` | Ground constant | The actual constant (e.g. `alice`) appears in the learned rule, not a variable. Useful for domain-specific rules. |

---

## Repository layout

```
xhail/
├── xhail/                      Core Python package
│   ├── __init__.py             Public API — learn(), LearningResult
│   ├── cli.py                  xhail CLI (argparse, logging setup)
│   ├── core.py                 Pipeline orchestrator
│   ├── language/
│   │   ├── terms.py            Atom, Clause, Literal, Normal, PlaceMarker, Fact
│   │   └── structures.py       Mode declarations
│   ├── parser/
│   │   └── parser.py           PLY-based .lp parser (tokeniser + grammar)
│   └── reasoning/
│       ├── abduction.py        Phase 1 — ASP abduction, builds Δ
│       ├── deduction.py        Phase 2 — BFS kernel construction
│       ├── induction.py        Phase 3 — ASP minimisation, builds H
│       ├── model.py            Shared state (clingo bridge, subsumption cache)
│       └── utils.py            ASP serialisation helpers
│
├── experiments/
│   ├── benchmarks/             10 canonical .lp benchmarks
│   ├── run_benchmarks.py       Benchmark runner (timing, memory, hypothesis)
│   ├── plot_results.py         Matplotlib visualisation
│   └── results/                CSV / JSON metrics (git-ignored)
│
├── tests/
│   ├── conftest.py             Shared fixtures
│   ├── test_benchmarks.py      Integration tests — one class per benchmark
│   ├── test_language.py        Unit tests — term / clause data structures
│   ├── test_phase0_regression.py  Regression tests for 14 fixed defects
│   └── test_pipeline_edge_cases.py  Edge cases — UNSAT, empty kernel, timeout
│
├── .github/workflows/ci.yml    GitHub Actions — lint, type-check, test, benchmark
├── pyproject.toml              Build config, Ruff, mypy, pytest settings
├── RELATED_WORK.md             Full comparison: Aleph, Metagol, ILASP, FastLAS
└── RESEARCH_FRAMING.md         Research questions, hypotheses, known limitations
```

---

## Engineering notes

Several non-obvious engineering decisions are worth documenting:

**BFS kernel construction (deduction phase).** The original implementation used a parent-key string to track the immediate predecessor of each BFS node, causing O(depth × level_size) chain reconstruction and allowing A→B→A cycles. The rewrite stores a `frozenset` of all ancestor keys on each node (O(1) cycle detection) and a direct `parent_node` pointer for O(depth) chain reconstruction. Chains terminate when the ancestor set blocks all further extensions — for typical benchmarks (5–15 unique matching atoms), this keeps the BFS polynomial.

**Leaf-node kernel collection.** The kernel is collected from BFS *leaf nodes* — nodes that generated no children — rather than from the deepest BFS level. This correctly handles benchmarks where different head atoms produce chains of different depths (e.g. the epidemic benchmark: the bob-rule terminates at depth 1 while the carol-rule extends to depth 2; collecting only from `levels[top]` silently discarded the bob-rule).

**Type membership caching.** The subsumption check `isSubsumed(atom, mode)` requires verifying that each ground constant belongs to the correct type (e.g. `alice` ∈ `person`). The original implementation called `getMatches` on the entire model for every subsumption check — quadratic in model size. The rewrite builds a `dict[type_name, frozenset[str]]` once per abduced model from unary facts, reducing subsumption to a frozenset lookup.

**Predicate-indexed BFS.** During deduction, the inner loop previously cross-joined every (schema, fact) pair — O(|schemas| × |all_facts|) per BFS level. A `{predicate → [Atom]}` index built once from the abduced model reduces this to O(|schemas| × |bucket_size|). On `grandfather` (20+ parent facts, 5 grandparent targets) this cuts the BFS cross-join by ~10×, dropping per-run time from ~270 ms to ~41 ms. On `trains` (100+ car facts) the improvement is similar (81 ms → 28 ms).

**Parallel clingo.** Both `call()` (abduction) and `getBestModel()` (induction) pass `--parallel-mode=N` (N = min(4, cpu_count)) to clingo, engaging its built-in thread-pool at no extra implementation cost.

**Induction kernel cap.** After generalisation and deduplication, the induction ASP program scales linearly with `|K| × max_body_size`. Empirical profiling across all 10 benchmarks shows that abstract clauses collapse to a single body length after generalisation (typically 5 literals). A default cap of **10 shortest abstract clauses** (configurable via `XHAIL_MAX_KERNEL`) is therefore sufficient — it gives induction full selectional flexibility while keeping the ASP program ~4× smaller than the former cap of 50:

```
cap=5  → 90 ms total, 10/10 solved
cap=10 → 97 ms total, 10/10 solved   ← default (safety margin)
cap=50 → 375 ms total, 10/10 solved  ← former default, 4× slower
```

**Parallel benchmark runner.** `run_benchmarks.py` uses `concurrent.futures.ProcessPoolExecutor` to run all benchmarks concurrently (default: all CPU cores, configurable via `--jobs N`). All 10 benchmarks complete in ~58 ms wall time vs ~117 ms sequential, displaying speedup vs CPU time in the summary footer.

---

## Running the tests

```bash
# Unit tests only — no clingo, runs in < 1 s
pytest -m "not integration"

# Full suite — unit + integration + edge cases
pytest

# With coverage
pytest --cov=xhail --cov-report=term-missing

# Specific benchmark
pytest tests/test_benchmarks.py::TestTrainsBenchmark -v
```

All 147 tests pass on Python 3.10, 3.11, and 3.12 (94% line coverage).

---

## Comparison to other ILP systems

| System | Hypothesis language | NAF | Solver | Intermediate artefacts | Recursive programs |
|--------|---------------------|:---:|--------|:----------------------:|:------------------:|
| [Aleph](https://www.cs.ox.ac.uk/activities/programinduction/Aleph/aleph.html) | Horn clauses | ✗ | Prolog | ✗ | Limited |
| [Metagol](https://github.com/metagol/metagol) | Metarule instances | ✗ | Prolog | ✗ | ✓ |
| [ILASP](https://doc.ilasp.com/) | Full ASP | ✓ | clingo | ✗ | Limited |
| [FastLAS](https://spike-imperial.github.io/FastLAS/) | Normal + choice rules | ✓ | clingo | ✗ | Limited |
| **XHAIL** (this work) | Normal rules with NAF | ✓ | clingo | ✓ (Δ, K, H) | ✗ |

**vs Aleph / Metagol.** XHAIL supports negation-as-failure, which is essential for defeasible rules ("flies unless penguin"). Classical ILP systems based on definite Horn clauses cannot express this.

**vs ILASP.** Both use clingo and support NAF. The key difference is architecture: ILASP treats hypothesis search as a single, monolithic optimisation; XHAIL exposes Δ (abduced atoms) and K (kernel clauses) as checkpointable intermediate results. This makes it possible to inspect *why* a particular hypothesis was found — or wasn't.

**vs FastLAS.** FastLAS optimises for scalability via a faster partial evaluation strategy. XHAIL prioritises legibility of the learning process, making it better suited to research contexts where understanding *how* a hypothesis was derived matters as much as the hypothesis itself.

See [`RELATED_WORK.md`](RELATED_WORK.md) for a detailed technical comparison and [`RESEARCH_FRAMING.md`](RESEARCH_FRAMING.md) for open research questions.

---

## Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Correctness & stabilisation — 14 defects fixed, 105 regression tests | ✅ Done |
| 1 | Repository professionalisation — packaging, public API, CLI | ✅ Done |
| 2 | Testing & CI — GitHub Actions (lint + type-check + test + benchmark), Codecov | ✅ Done |
| 3 | Experimental framework — 10 benchmarks, metrics runner, timing | ✅ Done |
| 4 | Performance engineering — BFS leaf collection, type-member cache, predicate-indexed BFS, parallel clingo, parallel benchmark runner | ✅ Done |
| 5 | Research positioning — related-work comparison, research framing | ✅ Done |
| 6 | Technical report / mini-paper | 🔲 Next |
| 7 | Extensions — noisy examples, neuro-symbolic integration, LLM-guided rule synthesis | 🔲 Planned |

---

## Citation

If you use this software in research, please cite both this implementation and the original XHAIL paper:

```bibtex
@software{everett2025xhail,
  author = {Everett, Josh},
  title  = {{XHAIL}: eXtended Hybrid Abductive Inductive Learning},
  url    = {https://github.com/everettmakes/xhail},
  year   = {2025}
}

@article{ray2009xhail,
  author  = {Ray, Oliver},
  title   = {Nonmonotonic abductive inductive learning},
  journal = {Journal of Applied Logic},
  volume  = {7},
  number  = {3},
  pages   = {329--340},
  year    = {2009}
}
```

---

## License

MIT — see [LICENSE](LICENSE).
