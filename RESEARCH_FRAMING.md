# Research Framing — XHAIL

This document defines the research questions, hypotheses, experimental design, known
limitations, and future directions for the XHAIL project. It is intended as the
intellectual spine of the project — the "why does this work matter and what does it
claim?" document that underpins the eventual technical report.

---

## 1. Central Research Question

> **Can the abductive-inductive decomposition of ILP — where abduction, deduction, and
> induction are implemented as three independent ASP solve calls — produce correct,
> interpretable hypotheses competitive with monolithic approaches, while providing
> superior transparency of the intermediate reasoning steps?**

This question has two components:

- **Correctness:** Does the three-phase pipeline reliably learn the intended hypothesis?
- **Transparency:** Are the intermediate artefacts (abduced atom set Δ, kernel set K)
  meaningful to a practitioner, and do they make the learned hypothesis easier to trust
  and inspect?

The XHAIL paradigm (Ray, 2009) was introduced theoretically. This project asks whether
a clean Python reimplementation using modern clingo is viable, where the bottlenecks are,
and what the practical scope of the approach is.

---

## 2. Hypotheses

**H1 — Correctness on standard tasks.** The three-phase XHAIL pipeline correctly learns
the expected hypothesis on standard ILP benchmark tasks (penguins, animal classification,
traffic rules, propositional circuits), as verified by 101 passing regression tests.

**H2 — Phase decomposition aids interpretability.** Each phase produces a human-readable
intermediate result:
- Abduction: the minimal set Δ of ground atoms that "explains" the examples
- Deduction: the kernel K of maximally-specific clauses derivable from Δ
- Induction: the minimal H ⊆ K that covers all examples

A practitioner can inspect each artefact independently (using `--debug --debug-output`)
to understand *why* XHAIL reached its hypothesis. Monolithic systems (ILASP, FastLAS)
do not provide equivalent intermediate artefacts.

**H3 — NAF is essential for real-world defaults.** Negation-as-failure is required to
learn useful rules in domains with exceptions (e.g., "flies unless penguin"). The
penguins benchmark, which explicitly requires NAF, cannot be solved by Horn-clause systems
(Aleph, Metagol).

**H4 — The deduction phase is the scalability bottleneck.** Recursive modeb predicates
cause non-termination in the current deduction phase. This is where search complexity
concentrates, and is the natural target for future optimisation.

---

## 3. Experimental Aims

### 3.1 Correctness verification (completed — Phases 0–3)

- 14 defects fixed in the original codebase (Phase 0)
- 101 automated tests: unit, integration, and benchmark regression tests (Phases 2–3)
- 4 benchmark tasks solved correctly with measured metrics

### 3.2 Benchmarking (completed — Phase 3)

The `experiments/run_benchmarks.py` runner records the following metrics per task:

| Metric | What it measures |
|--------|-----------------|
| `runtime_s` | End-to-end wall-clock time for `learn()` |
| `peak_memory_mb` | Peak RSS memory (via `resource.getrusage`) |
| `rule_complexity` | Mean number of body literals per learned rule |
| `n_rules` | Number of rules in the learned hypothesis |
| `n_examples` | Size of the example set |
| `n_background` | Size of the background knowledge |
| `success` | Whether a non-empty hypothesis was found |

### 3.3 Comparative positioning (completed — Phase 4)

Qualitative comparison against Aleph, Metagol, ILASP, FastLAS across: hypothesis
language, NAF support, example types, solver backend, and scalability. See
[RELATED_WORK.md](RELATED_WORK.md).

### 3.4 Scalability profiling (future — Phase 5 extension)

Planned: vary the size of the example set and background knowledge systematically across
the benchmark tasks and measure how runtime scales. This would allow empirical comparison
of the per-phase cost structure.

---

## 4. Known Limitations

These limitations were discovered during Phases 0–3 and are documented as open research
problems rather than implementation defects. Each is a potential future contribution.

### L1 — Multi-head learning not supported

**Symptom:** When more than one `#modeh` declaration is present, the induction phase
assigns all learned rules to the first head predicate.

**Root cause:** In `induction.py`, `runPhase()` hardcodes `new_head = clauses[0].head`
when assembling the hypothesis from the selected kernel clauses, ignoring which clause
each body came from.

**Impact:** Tasks requiring separate predicates to be learned simultaneously (e.g.,
learning both `stop/1` and `go/1` in the traffic domain) cannot be expressed.

**Fix direction:** The induction phase must track which modeh predicate generated each
kernel clause and use that predicate as the head of the corresponding induced rule.

---

### L2 — Recursive modeb causes non-termination

**Symptom:** If a modeb predicate appears in the head of a rule and also in its own
body (or transitively), the deduction phase generates a non-terminating ASP grounding.

**Root cause:** The deduction phase builds maximally-specific clauses by grounding the
background knowledge. Recursive predicates cause unbounded grounding depth.

**Impact:** Recursive ILP tasks (list membership, path reachability, ancestor relations)
cannot be expressed in XHAIL without triggering timeouts.

**Fix direction:** A bounded grounding depth (already controlled by the `depth` parameter)
should be enforced more aggressively at the clause-construction level, and/or the
deduction ASP program should include an explicit recursion guard.

---

### L3 — Output variables in modeh not supported

**Symptom:** A `#modeh` declaration with a `-type` (output) placemarker, such as
`#modeh grandparent(+person, -person)`, causes an `AttributeError` in the abduction
phase (`generalise()` calls `.terms` on a `PlaceMarker` object).

**Root cause:** The `generalise()` method in `structures.py` checks `isinstance(term, Atom)`
but `PlaceMarker` inherits from the same base, so the output placemarker is passed into
the recursive atom-processing branch, which expects `.terms`.

**Impact:** Multi-argument head predicates where the second argument is a new binding
(common in relational tasks) cannot be expressed. Workaround: use `+type` for all modeh
arguments.

**Fix direction:** `generalise()` should explicitly check `isinstance(term, PlaceMarker)`
before dispatching to the atom branch.

---

### L4 — Propositional (0-arity) trailing comma in induction (fixed in Phase 3)

**Symptom:** 0-arity predicates (no arguments) in modeh/modeb previously generated
`try(0, 1, )` with a trailing comma in the induction ASP program — invalid clingo syntax.

**Root cause:** `loadUseTry()` used `', '.join([var.value for var in ...])` unconditionally;
an empty variable list produced the trailing comma.

**Status:** Fixed in Phase 3 via `_try_term()` helper which conditionally omits the
variable argument list. Propositional learning now fully functional, tested in
`tests/test_benchmarks.py::TestPropositionalBenchmark`.

---

### L5 — No timeout enforcement per phase

**Symptom:** Certain benchmark configurations (recursive modeb, large grounding) hang
indefinitely rather than returning a useful error.

**Root cause:** While a `DeductionTimeoutError` class exists and `depth` is passed through,
per-phase wall-clock timeouts are not enforced in the ASP solver calls.

**Impact:** The experiment runner uses OS-level `timeout` as a workaround. A broken
pipeline cannot be distinguished from a slow one without external tooling.

**Fix direction:** Pass a `timeout` argument to clingo's solve call and raise
`DeductionTimeoutError` (or a new `AbductionTimeoutError`) when it fires.

---

## 5. Novelty and Contribution

This implementation's contributions relative to prior XHAIL work are:

1. **Clean Python reimplementation.** The only prior public implementation (Bragaglia
   & Ray, Java) is unmaintained. This project provides a modern, pip-installable Python
   package with a public API (`from xhail import learn`), CLI (`xhail run`), and type
   annotations.

2. **14 correctness defects fixed.** The original undergraduate prototype had significant
   bugs in: the parser (missing propositional atoms, `:- constraints`), the induction
   phase (trailing-comma ASP, shared class state), the deduction phase (no timeout), and
   the data structures (no-op set operations, `replaceConstants` indexing).

3. **Reproducible experimental framework.** `experiments/run_benchmarks.py` enables
   one-command reproducible benchmark runs with structured metric logging. No equivalent
   was available in prior XHAIL work.

4. **Documented limitation taxonomy.** L1–L5 above constitute the first systematic
   characterisation of XHAIL's expressiveness boundaries, derived empirically from
   attempting canonical ILP benchmarks.

---

## 6. Future Research Directions

### Near-term (natural Phase 5 targets)

- **Fix L1 (multi-head):** Correct the `new_head` assignment in `induction.py`. Adds
  the traffic domain and any other multi-predicate classification task.
- **Fix L3 (output vars in modeh):** One-line type check in `generalise()`. Unblocks
  relational tasks like family relations.
- **Fix L5 (per-phase timeouts):** Thread a `timeout_s` parameter into each phase's
  solve call.

### Medium-term

- **Scalability analysis:** Vary example count and background size systematically;
  plot per-phase runtime to identify which phase dominates.
- **Comparison experiment:** Run the same tasks in Aleph and/or ILASP; compare runtime,
  hypothesis quality, and the interpretability of intermediate artefacts.
- **Recursive deduction:** Investigate bounded-depth grounding strategies that allow
  a constrained class of recursive modeb predicates.

### Long-term

- **Neuro-symbolic integration:** Use a neural perception model to generate the
  background knowledge (ground facts) from raw inputs, with XHAIL learning the
  symbolic rules. The interpretable phase decomposition makes XHAIL a natural ILP
  backend for neuro-symbolic pipelines.
- **Noisy examples:** Extend the abduction phase to tolerate inconsistent examples
  (majority-voting or weighted coverage).
- **LLM-assisted rule synthesis:** Use a language model to propose candidate body
  predicates, reducing the search space before the deduction phase.
- **Probabilistic hypotheses:** Integrate distributional semantics into the kernel set
  construction, producing ProbLog- or LPMLN-style probabilistic rules.

---

## 7. Summary

XHAIL is a research-grade re-engineering of a theoretically well-motivated but
previously under-implemented ILP paradigm. The three-phase abductive-inductive pipeline
produces correct, interpretable hypotheses on standard tasks, with transparent
intermediate artefacts at each phase. The known limitations (L1–L5) form a concrete
research agenda: each is a solvable engineering problem that, when fixed, expands the
class of tasks XHAIL can address. The most impactful near-term direction is fixing the
multi-head limitation (L1), which would immediately unlock a large class of multi-class
classification tasks.

---

## References

- Ray, O. (2009). Nonmonotonic abductive inductive learning. *Journal of Applied Logic*, 7(3), 329–340.
- Law, M., Russo, A., & Broda, K. (2020). The ILASP system for inductive learning of answer set programs. *Theory and Practice of Logic Programming*.
- Law, M., Russo, A., Bertrand, J., & Broda, K. (2020). FastLAS: Scalable inductive logic programming incorporating domain-specific optimisation criteria. In *AAAI 2020*.
- Muggleton, S., Lin, D., Pahlavi, N., & Tamaddoni-Nezhad, A. (2015). Meta-interpretive learning of higher-order dyadic datalog. *Machine Learning*, 100(1), 49–73.
- Srinivasan, A. (2001). *The Aleph Manual.* University of Oxford.
