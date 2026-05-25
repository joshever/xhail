# Related Work — ILP Systems

This document positions XHAIL within the landscape of Inductive Logic Programming (ILP).
It covers the four most relevant systems: **Aleph**, **Metagol**, **ILASP**, and **FastLAS**,
then summarises XHAIL's design choices and known limitations in light of each.

---

## Background: What ILP Systems Do

All ILP systems solve the same core problem: given background knowledge **B**, positive
examples **E⁺**, and negative examples **E⁻**, find a hypothesis **H** such that:

- **B ∪ H ⊨ e** for every **e ∈ E⁺** (H explains the positives)
- **B ∪ H ⊭ e** for every **e ∈ E⁻** (H does not over-generalise)

They differ substantially in the *language* of B and H, the *semantics* used, the *search
strategy*, and which corner cases (recursion, negation, non-determinism) they support.

---

## System Summaries

### Aleph

**Reference:** Srinivasan (2001). *The Aleph Manual.* University of Oxford.

Aleph is a mature, widely-used ILP system implemented in Prolog. It operates in the
**classical ILP paradigm** (Muggleton & De Raedt, 1994): it constructs hypotheses in
Horn clause logic using **inverse entailment** and a **greedy set-cover** search. For
each uncovered positive example, Aleph:

1. Saturates the example against the background knowledge to form a *bottom clause* —
   the most-specific clause that entails the example.
2. Searches the generalisation lattice above the bottom clause for a clause that covers
   the example without covering negatives.
3. Adds the best clause to the hypothesis and repeats.

**Strengths:** Mature, well-documented, handles large realistic datasets (pharmacology,
biology), integrates with SWI-Prolog and YAP. Strong community and tool support.

**Limitations:** Restricted to *Horn clauses* (no negation-as-failure, no constraints).
Greedy set-cover is not globally optimal. The Prolog-based implementation does not
leverage modern ASP solvers.

---

### Metagol

**Reference:** Muggleton, Lin, Pahlavi & Tamaddoni-Nezhad (2015). *Meta-Interpretive
Learning of Higher-Order Dyadic Datalog*. Machine Learning, 100(1).

Metagol implements **Meta-Interpretive Learning (MIL)** — a fundamentally different
approach to ILP. Instead of mode declarations, the user supplies *metarules*: higher-order
clause templates such as:

```prolog
% P(X,Y) :- Q(X,Z), R(Z,Y)   (chain metarule)
metarule([P,Q,R], [P,X,Y], [[Q,X,Z],[R,Z,Y]]).
```

Metagol proves examples using a Prolog meta-interpreter that simultaneously instantiates
metarules. The learned hypothesis is the set of metarule instantiations that prove all
positive examples.

**Strengths:** Naturally learns **recursive programs** (programs that refer to themselves),
which most other ILP systems cannot. Strong theoretical guarantees on sample complexity.
Supports predicate invention. Excellent for string/sequence tasks and program synthesis.

**Limitations:** Limited to a fixed inventory of metarules (the user must anticipate the
recursive structure). The Prolog proof-search underpinning does not handle NAF or
non-deterministic theories. Poorly suited to learning *classification rules* with
exceptions (where NAF is essential).

---

### ILASP

**Reference:** Law, Russo & Broda (2014, 2020). *Inductive Learning of Answer Set
Programs.* ECAI 2014; *The ILASP System for Inductive Learning of Answer Set Programs.*
Theory and Practice of Logic Programming, 2020.

ILASP (**I**nductive **L**earning of **A**nswer **S**et **P**rograms) is the most
general ASP-based ILP system. It learns full Answer Set Programs, including:

- Normal rules (with NAF)
- Choice rules (`{ a } :- b.`)
- Hard constraints (`:- a, b.`)
- Weak constraints (optimisation)

Examples in ILASP are **partial interpretations** — constraints on which atoms must or
must not appear in some answer set. This is strictly richer than ground-atom examples:
it allows expressing that "some acceptable world must satisfy this constraint", enabling
**preference learning** and **learning of non-deterministic theories**.

ILASP frames learning as a form of brave/cautious reasoning over the space of ASP programs,
and uses ASP solvers (clingo) to enumerate and test candidate hypotheses.

**Strengths:** Most expressive ILP framework available. Handles defaults, exceptions,
preferences, non-determinism, and constraints all within a unified ASP semantics. Active
development (ILASP 4.x as of 2023).

**Limitations:** Computationally expensive for large hypothesis spaces. Scalability is
a known bottleneck, motivating FastLAS.

---

### FastLAS

**Reference:** Law, Russo, Bertrand & Broda (AAAI 2020). *FastLAS: Scalable Inductive
Logic Programming Incorporating Domain-Specific Optimisation Criteria.*

FastLAS is a **scalable** ILP system developed by the same group as ILASP. It uses the
same **Context-dependent Learning from Answer Sets** framework but makes aggressive
efficiency trade-offs:

- The hypothesis space is pruned aggressively using *space reduction* techniques.
- The user can specify a **custom scoring function** for learned rules, replacing the
  default minimality bias with domain-specific optimisation criteria.
- FastLAS1 (AAAI 2020) has significant restrictions compared to ILASP.
- FastLAS2 (IJCAI 2021) lifts key restrictions, adding support for
  *non-observational predicate learning* and multi-answer-set background knowledge.

**Strengths:** Significantly faster than ILASP on large tasks where FastLAS's restrictions
are acceptable. Domain-specific scoring functions are a novel and practically valuable
feature.

**Limitations:** Less expressive than ILASP. Optimisation criteria are user-defined, which
increases the burden on the practitioner.

---

## Comparison Table

| Dimension                | Aleph          | Metagol            | ILASP             | FastLAS            | **XHAIL (this work)**    |
|--------------------------|----------------|--------------------|-------------------|--------------------|--------------------------|
| **Hypothesis language**  | Horn clauses   | Metarule instances | Full ASP          | Normal + choice rules | Normal rules (NAF)    |
| **Negation (NAF)**       | ✗              | ✗                  | ✓                 | ✓                  | ✓                        |
| **Constraints**          | ✗              | ✗                  | ✓ (hard + weak)   | ✓ (hard)           | ✗ (not yet)              |
| **Recursive programs**   | Limited        | ✓ (via metarules)  | Limited           | Limited            | ✗ (times out)            |
| **Example type**         | Ground atoms   | Ground atoms       | Partial interpretations | Partial interp. | Ground atoms          |
| **Search strategy**      | Greedy set-cover | Proof search     | ASP enumeration   | Pruned ASP enum.   | ASP (3-phase pipeline)   |
| **Solver backend**       | Prolog         | Prolog             | clingo            | clingo             | clingo                   |
| **Predicate invention**  | ✗              | ✓                  | ✗                 | ✓ (FastLAS2)       | ✗                        |
| **Implementation lang.** | Prolog         | Prolog             | C++ / Python      | C++ / Python       | Python                   |
| **Maturity**             | High (2001–)   | High (2015–)       | High (2014–)      | Medium (2020–)     | Research prototype       |
| **Open source**          | ✓              | ✓                  | Partial           | ✓                  | ✓                        |

---

## Where XHAIL Sits

XHAIL occupies a distinct position defined by its **three-phase abductive-inductive
pipeline**:

1. **Abduction** — use ASP to find a minimal set of ground atoms Δ (abduced facts) that,
   together with the background, is consistent with all examples.
2. **Deduction** — construct a *kernel set* of maximally-specific clauses that justify Δ
   in terms of the mode language.
3. **Induction** — find the minimal subset of the kernel that covers all examples, using
   ASP as the optimisation oracle.

This architecture differs from Aleph (no abduction phase, no ASP) and from ILASP (no
explicit abduction/deduction split — ILASP enumerates hypotheses directly). The three-phase
decomposition reduces each sub-problem to a tractable ASP solve, rather than searching the
full hypothesis space at once.

**XHAIL's key advantages over ILASP:**
- The pipeline structure provides interpretable intermediate results (the abduced Δ and
  the kernel are human-readable at each phase).
- The deduction phase produces maximally-specific clauses before generalisation, which
  keeps the induction problem small.

**XHAIL's key limitations relative to ILASP:**
- Restricted to normal rules only (no choice rules, no weak constraints).
- Examples must be ground atoms, not partial interpretations.
- Multi-head learning is not supported in the current implementation.
- Recursive modeb predicates cause non-termination in the deduction phase.

**XHAIL vs FastLAS:** FastLAS prioritises scalability over interpretability of the search.
XHAIL's phase decomposition provides a more pedagogically transparent view of *why* a
hypothesis was chosen.

**XHAIL vs Metagol:** Metagol excels at recursive program synthesis via metarules but
cannot learn exception-based rules with NAF. XHAIL's NAF support makes it better suited
to real-world classification tasks with defaults and exceptions (e.g., "birds fly unless
they are penguins").

**XHAIL vs Aleph:** Both use mode declarations and similar example formats. XHAIL adds
ASP's full NAF and a globally-optimal induction step (via ASP minimisation) instead of
Aleph's greedy set-cover, at the cost of restricting the hypothesis language to normal
ASP rules rather than arbitrary Horn clauses.

---

## Summary

XHAIL's core scientific contribution is demonstrating that the **abductive-inductive
decomposition** of the ILP problem can be implemented *entirely within ASP*, using clingo
as a uniform solver across all three phases. This makes the system concise (~1,000 lines
of Python orchestrating ASP programs), formally grounded in answer set semantics, and
directly extensible by ASP practitioners who wish to inspect or modify the intermediate
programs at each phase.

The principal open research questions this raises are:
- Is the three-phase decomposition more efficient than direct hypothesis enumeration
  (as in ILASP) for the class of tasks XHAIL handles?
- Can the deduction phase be made to handle recursive modeb without non-termination?
- Can multi-head learning be added without restructuring the induction phase?

These are elaborated in [RESEARCH_FRAMING.md](RESEARCH_FRAMING.md).

---

## References

- Ray, O. (2009). Nonmonotonic abductive inductive learning. *Journal of Applied Logic*, 7(3), 329–340.
- Srinivasan, A. (2001). *The Aleph Manual.* University of Oxford.
- Muggleton, S., Lin, D., Pahlavi, N., & Tamaddoni-Nezhad, A. (2015). Meta-interpretive learning of higher-order dyadic datalog: predicate invention revisited. *Machine Learning*, 100(1), 49–73.
- Law, M., Russo, A., & Broda, K. (2014). Inductive learning of answer set programs. In *ECAI 2014*, pp. 311–316.
- Law, M., Russo, A., & Broda, K. (2020). The ILASP system for inductive learning of answer set programs. *Theory and Practice of Logic Programming*.
- Law, M., Russo, A., Bertrand, J., & Broda, K. (2020). FastLAS: Scalable inductive logic programming incorporating domain-specific optimisation criteria. In *AAAI 2020*.
- Law, M., Russo, A., Bertrand, J., & Broda, K. (2021). Scalable non-observational predicate learning in ASP. In *IJCAI 2021*.
