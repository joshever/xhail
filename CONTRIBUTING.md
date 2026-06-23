# Contributing to XHAIL

Thank you for your interest in contributing. This document covers the development workflow, code standards, and testing requirements.

---

## Development setup

```bash
git clone https://github.com/everettmakes/xhail.git
cd xhail
pip install -e ".[dev]"
```

This installs the package in editable mode plus the full development toolchain: `pytest`, `ruff`, `mypy`, and `pre-commit`.

---

## Running the tests

```bash
# Fast — unit tests only, no clingo, < 0.5 s
pytest -m "not integration"

# Full suite — unit + integration (calls clingo, ~5 s)
pytest

# With line coverage
pytest --cov=xhail --cov-report=term-missing

# Single benchmark
pytest tests/test_benchmarks.py::TestGrandfatherBenchmark -v
```

The test suite is split into:

- **Unit tests** (`-m "not integration"`) — pure Python, no clingo required. Run these in a tight feedback loop during development.
- **Integration tests** (`-m integration`) — invoke the full three-phase pipeline. Required before opening a PR.

---

## Running the benchmarks

```bash
# All 10 benchmarks in parallel (default: all CPU cores)
python experiments/run_benchmarks.py

# Sequential, for profiling
python experiments/run_benchmarks.py --jobs 1

# Single benchmark
python experiments/run_benchmarks.py --benchmark grandfather

# Tune depth
python experiments/run_benchmarks.py --depth 15
```

Results are written to `experiments/results/` (CSV + JSON). The directory is git-ignored — do not commit result files.

---

## Code standards

### Formatting and linting

```bash
ruff format .          # auto-format (Black-compatible)
ruff check .           # lint (E, F, W, I)
mypy xhail/            # static type checking
```

All three must pass with zero errors before a PR is reviewed. The CI pipeline enforces this on every push.

### Type annotations

New functions and methods should carry type annotations. The `xhail.reasoning.*` modules have many untyped legacy functions — annotating them incrementally is welcome. The `xhail.parser.*` module uses PLY's dynamic dispatch pattern and is exempt (`[[tool.mypy.overrides]] ignore_errors = true` in `pyproject.toml`).

### Logging

Use the module-level logger, not `print`:

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Kernel truncated to %d clause(s).", max_kernel)
logger.info("Learned hypothesis (%d rule(s)).", len(rules))
logger.warning("Empty kernel — check mode declarations.")
```

Debug messages should be terse and machine-readable. Info messages describe phase outcomes. Warnings signal likely misconfiguration.

### Docstrings

Public functions and non-trivial internal methods should have docstrings explaining *what* the function does and *why* any non-obvious implementation choices were made. See `deduction.py::extractTerms` and `induction.py::runPhase` for examples of the expected level of detail.

---

## Adding a benchmark

1. Create `experiments/benchmarks/<name>.lp` with background knowledge, mode declarations, and examples.
2. Add a test class to `tests/test_benchmarks.py`:

```python
@pytest.mark.integration
class TestMyBenchmark:
    def test_learns_correct_rule(self):
        result = learn(BENCHMARKS / "my_benchmark.lp")
        assert result.success
        combined = " ".join(result.hypothesis)
        assert "expected_predicate" in combined
```

3. Run `python experiments/run_benchmarks.py --benchmark my_benchmark` and verify it solves correctly.

---

## Pull request checklist

Before opening a PR:

- [ ] `ruff format .` — no formatting changes
- [ ] `ruff check .` — zero lint errors
- [ ] `mypy xhail/` — zero type errors
- [ ] `pytest` — all tests pass (including integration)
- [ ] `python experiments/run_benchmarks.py` — 10/10 benchmarks solved
- [ ] New or changed behaviour has corresponding tests
- [ ] Public API changes are reflected in docstrings and `README.md`

---

## Architecture overview

```
learn(file)                          ← public entry point (xhail/core.py)
  │
  ├─ Parser.parseFile()              ← xhail/parser/parser.py
  │    Extracts BG, MH, MB, EX from the .lp file
  │
  ├─ Abduction.runPhase()            ← xhail/reasoning/abduction.py
  │    ASP solve: BG + MH → Δ (minimal abduced atom set)
  │
  ├─ Deduction.runPhase()            ← xhail/reasoning/deduction.py
  │    BFS over (Δ × MB): builds kernel set K
  │    Key invariants:
  │      • frozenset ancestor tracking  → O(1) cycle detection per step
  │      • parent_node pointer          → O(depth) chain reconstruction
  │      • predicate index              → O(bucket) fact lookup per schema
  │      • leaf-node collection         → every head atom contributes ≥1 clause
  │
  └─ Induction.runPhase()            ← xhail/reasoning/induction.py
       ASP optimisation: BG + K → H (minimal-literal subset of K)
       Uses #minimize{1@2,I,J : use(I,J)} over {use(clause,literal)} choices
```

The `Model` class (`xhail/reasoning/model.py`) is the shared state object passed between phases. It owns the clingo bridge, the `_type_members` subsumption cache, and the kernel/hypothesis stores. Each call to `learn()` creates a fresh `Model` — there is no shared mutable state between calls.

---

## Known limitations

- **No recursive rules.** The BFS terminates when no new body atoms can be added (ancestor-set cycle guard). This prevents learning mutually-recursive programs. See `RESEARCH_FRAMING.md` for the planned extension.
- **Single-head rules only.** The current mode schema language does not support disjunctive heads (`a | b :- body`).
- **Unix timeout.** The deduction timeout uses `threading.Thread.join(timeout)`, which works on all platforms. If the background thread hangs in clingo's C extension, the process may need to be killed externally.
- **No noise handling.** All examples are assumed noise-free. The roadmap includes a probabilistic relaxation layer.
