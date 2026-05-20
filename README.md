# XHAIL

**eXtended Hybrid Abductive Inductive Learning** — a symbolic Inductive Logic Programming (ILP) system built on Answer Set Programming (ASP).

XHAIL learns interpretable logic-program rules from background knowledge and labelled examples by chaining three phases: **abduction → deduction → induction**. It is a clean Python reimplementation of the XHAIL paradigm introduced by Oliver Ray (2009), built on the [clingo](https://potassco.org/clingo/) ASP solver.

---

## Why XHAIL?

Most modern machine learning systems are statistical black boxes. XHAIL takes the opposite approach: it learns *symbolic rules* that are human-readable, verifiable, and consistent with the background knowledge. This makes it relevant to:

- **Explainable AI** — learned rules can be inspected and justified
- **Neuro-symbolic systems** — symbolic hypotheses can be combined with neural perception
- **Program synthesis** — learning logic programs from examples
- **Scientific discovery** — deriving interpretable laws from observations

---

## Installation

Requires **Python ≥ 3.10** and [clingo](https://potassco.org/clingo/) (installed automatically).

```bash
git clone https://github.com/everettmakes/xhail.git
cd xhail
pip install -e ".[dev]"
```

Verify the install:

```bash
xhail --version
xhail run test.lp
```

---

## Quick start

### Command line

```bash
# Learn which birds fly (classic penguins task)
xhail run test.lp
# flies(V1) :- not penguin(V1).

# Verbose mode — shows phase progress on stderr
xhail run josh.lp --verbose

# Debug mode — writes intermediate ASP programs to disk
xhail run test.lp --debug --debug-output ./debug/
```

### Python API

```python
from xhail import learn

result = learn("test.lp", depth=10)

if result.success:
    for rule in result.hypothesis:
        print(rule)
# → flies(V1) :- not penguin(V1).

print(repr(result))
# LearningResult(success=True, n_rules=1, source='test.lp')
```

---

## Input format

XHAIL input files are Answer Set Programs (`.lp`) with four kinds of declaration:

```prolog
% Background knowledge
bird(X) :- penguin(X).
bird(a). bird(b). bird(c).
penguin(d).

% Mode declarations — define the hypothesis search space
#modeh flies(+bird).          % head predicates the learner may use
#modeb penguin(+bird).        % body predicates (+ = input variable)
#modeb not penguin(+bird).    % negation-as-failure is allowed

% Labelled examples
#example flies(a).
#example flies(b).
#example flies(c).
#example not flies(d).        % negative example
```

| Keyword     | Meaning |
|-------------|---------|
| `#modeh`    | Allowed head predicate. `+type` is an input (typed) variable. |
| `#modeb`    | Allowed body predicate. `-type` is an output variable. |
| `#example`  | Positive or negative example to explain. |

---

## How it works

```
Input (.lp)
    │
    ▼
┌──────────┐    minimal explanation Δ
│Abduction │──────────────────────────► atoms that satisfy all examples
└──────────┘
    │
    ▼
┌──────────┐    kernel set K
│Deduction │──────────────────────────► maximally-specific clauses over Δ
└──────────┘
    │
    ▼
┌──────────┐    hypothesis H ⊆ K
│Induction │──────────────────────────► minimal clause subset covering examples
└──────────┘
    │
    ▼
Learned rules (stdout / LearningResult)
```

All three phases are implemented as ASP problems solved by clingo, keeping the implementation concise and the correctness guarantees strong.

---

## Repository layout

```
xhail/
├── xhail/                  Python package
│   ├── __init__.py         Public API: learn(), LearningResult
│   ├── cli.py              xhail command-line interface
│   ├── core.py             Pipeline orchestration
│   ├── language/           Term and clause data structures
│   ├── parser/             PLY-based .lp parser
│   └── reasoning/          Abduction, deduction, induction phases + Model
├── tests/                  pytest suite (unit + integration)
├── test.lp                 Penguins benchmark
├── josh.lp                 Traffic-light benchmark
├── example1.lp             Propositional benchmark
├── pyproject.toml          Packaging and tool config
└── XHAIL_AUDIT_AND_ROADMAP.md   Development roadmap
```

---

## Running the tests

```bash
# Fast unit tests only (no clingo calls)
pytest -m "not integration"

# Full suite including end-to-end pipeline tests
pytest
```

---

## Roadmap

This project is being actively developed from an undergraduate dissertation prototype into a research-engineering portfolio project. See [`XHAIL_AUDIT_AND_ROADMAP.md`](XHAIL_AUDIT_AND_ROADMAP.md) for the full plan.

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Correctness & stabilisation — 14 defects fixed, 22 regression tests | ✅ Done |
| 1 | Repository professionalisation — packaging, CLI, public API | ✅ Done |
| 2 | Testing & CI — GitHub Actions, coverage reporting | 🔲 Next |
| 3 | Experimental framework — benchmarks, evaluation metrics, reproducible runs | 🔲 Planned |
| 4 | Research positioning — related-work comparison (ILASP, Aleph, Metagol, FastLAS) | 🔲 Planned |
| 5 | Technical report / mini-paper | 🔲 Planned |

---

## Citation

If you use this software in research, please cite both this implementation and the original XHAIL paper:

```bibtex
@software{everett2024xhail,
  author = {Everett, Josh},
  title  = {{XHAIL}: eXtended Hybrid Abductive Inductive Learning},
  url    = {https://github.com/everettmakes/xhail},
  year   = {2024}
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
