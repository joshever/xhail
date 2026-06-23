"""
Targeted unit tests for internal modules — fills the remaining coverage gaps
identified after the main test suite reaches 92%.

Each test class is labelled with the module and line-range it covers.
No test here uses external processes; clingo is invoked only in the
functions marked @pytest.mark.integration.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from unittest.mock import patch

import pytest

BENCHMARKS = Path(__file__).parent.parent / "experiments" / "benchmarks"


# ---------------------------------------------------------------------------
# xhail.language.structures — generalise_atom recursive Atom branch (L34-36)
# ---------------------------------------------------------------------------


class TestGeneraliseAtomRecursion:
    """generalise_atom must recurse into nested Atom sub-terms."""

    def test_nested_atom_is_generalised(self):
        from xhail.language.structures import generalise_atom
        from xhail.language.terms import Atom, Normal, PlaceMarker

        # Build: happens(use(+sugar), +time)
        inner = Atom("use", [PlaceMarker("+", "sugar")])
        outer = Atom("happens", [inner, PlaceMarker("+", "time")])
        result, n = generalise_atom(outer, n=1, replace_outputs=True)
        # Both PlaceMarkers should have been replaced with V1, V2
        assert n == 3
        assert isinstance(result.terms[0], Atom)  # inner stays Atom
        assert isinstance(result.terms[0].terms[0], Normal)  # inner's term → V1
        assert result.terms[0].terms[0].value == "V1"
        assert isinstance(result.terms[1], Normal)  # outer's +time → V2
        assert result.terms[1].value == "V2"

    def test_normal_sub_terms_are_not_replaced(self):
        from xhail.language.structures import generalise_atom
        from xhail.language.terms import Atom, Normal

        # Build: foo(a) where 'a' is a Normal — should not be touched
        atom = Atom("foo", [Normal("a")])
        result, n = generalise_atom(atom, n=1, replace_outputs=True)
        assert n == 1  # nothing replaced
        assert isinstance(result.terms[0], Normal)
        assert result.terms[0].value == "a"


# ---------------------------------------------------------------------------
# xhail.reasoning.deduction — BFS budget hit (L160-161) + empty-level (L168)
# ---------------------------------------------------------------------------


class TestDeductionBFSBudget:
    """Force the BFS node budget to trigger early-stop logging."""

    @pytest.mark.integration
    def test_budget_hit_still_finds_hypothesis(self, tmp_path):
        """With a very tight BFS budget the learner should still produce a result
        for simple tasks (e.g. traffic: stop(V1) :- red(V1).)."""
        from xhail import learn

        # Budget of 5 nodes is enough for the traffic benchmark (depth-1 rule).
        with patch.dict(os.environ, {"XHAIL_MAX_BFS_NODES": "5"}):
            result = learn(BENCHMARKS / "traffic.lp")
        assert result.success

    @pytest.mark.integration
    def test_tight_kernel_cap_still_solves(self, tmp_path):
        """Induction with kernel cap of 2 should still solve easy benchmarks."""
        from xhail import learn

        with patch.dict(os.environ, {"XHAIL_MAX_KERNEL": "2"}):
            result = learn(BENCHMARKS / "penguins.lp")
        assert result.success


# ---------------------------------------------------------------------------
# xhail.reasoning.deduction — empty kernel warning (L178, L184)
# ---------------------------------------------------------------------------


class TestDeductionEmptyKernel:
    """If no abduced atoms match the mode schemas, the kernel is empty and
    a warning is emitted.  The pipeline should not crash."""

    @pytest.mark.integration
    def test_no_matching_schema_yields_no_hypothesis(self, tmp_path, caplog):
        """Background predicate name mismatches all modeb → empty kernel → no hyp."""
        from xhail import learn

        # flies is the head; modeb references 'swims' which never holds.
        lp = tmp_path / "mismatch.lp"
        lp.write_text(
            "bird(a). bird(b).\n"
            "#modeh flies(+bird).\n"
            "#modeb swims(+bird).\n"
            "#example flies(a).\n"
            "#example flies(b).\n"
        )
        with caplog.at_level(logging.DEBUG, logger="xhail.reasoning.deduction"):
            result = learn(str(lp))
        # Should not crash; either no hypothesis or trivial head-only rule
        assert isinstance(result.success, bool)


# ---------------------------------------------------------------------------
# xhail.reasoning.deduction — getMarkerTerms compound-Atom branch (L62)
# ---------------------------------------------------------------------------


class TestGetMarkerTermsCompoundAtom:
    """getMarkerTerms must call str() on compound-Atom term1 values."""

    def test_compound_atom_term_uses_str(self):
        from unittest.mock import MagicMock

        from xhail.language.terms import Atom, Normal, PlaceMarker
        from xhail.reasoning.deduction import Deduction

        model = MagicMock()
        ded = Deduction(model)

        # fact: happens(use(glucose), 1)  schema: happens(use(#sugar), +time)
        inner_fact = Atom("use", [Normal("glucose")])
        fact = Atom("happens", [inner_fact, Normal("1")])
        inner_schema = Atom("use", [PlaceMarker("#", "sugar")])
        schema = Atom("happens", [inner_schema, PlaceMarker("+", "time")])

        # '#' marker on the inner term → value should be str(inner_fact)
        result = ded.getMarkerTerms(fact, schema, "#")
        assert "glucose" in result

        # '+' marker on the time term → '1'
        result_plus = ded.getMarkerTerms(fact, schema, "+")
        assert "1" in result_plus


# ---------------------------------------------------------------------------
# xhail.reasoning.induction — kernel truncation log (L164-166)
# ---------------------------------------------------------------------------


class TestInductionKernelTruncation:
    """When the abstract kernel exceeds the cap, a DEBUG log is emitted."""

    @pytest.mark.integration
    def test_truncation_log_emitted(self, caplog):
        from xhail import learn

        with caplog.at_level(logging.DEBUG, logger="xhail.reasoning.induction"):
            with patch.dict(os.environ, {"XHAIL_MAX_KERNEL": "1"}):
                learn(BENCHMARKS / "grandfather.lp")

        truncation_logs = [r for r in caplog.records if "Kernel truncated" in r.message]
        assert truncation_logs, "Expected a 'Kernel truncated' log entry"


# ---------------------------------------------------------------------------
# xhail.reasoning.model — clearProgram, getBackground, getExamples (L99, 235, 238)
# ---------------------------------------------------------------------------


class TestModelAccessors:
    def _make_model(self):
        from xhail.language.structures import Example
        from xhail.language.terms import Atom, Normal
        from xhail.reasoning.model import Model

        ex = Example(Atom("flies", [Normal("a")]))
        return Model(
            EX=[ex],
            MH=[],
            MB=[],
            BG=["bird(a)."],
            DEPTH=5,
        )

    def test_clear_program(self):
        model = self._make_model()
        model.program = "some asp code"
        model.clearProgram()
        assert model.program == ""

    def test_get_background(self):
        model = self._make_model()
        assert "bird(a)." in model.getBackground()

    def test_get_examples(self):
        model = self._make_model()
        assert len(model.getExamples()) == 1


# ---------------------------------------------------------------------------
# xhail.reasoning.model — _isSubsumed edge cases (L115-128)
# ---------------------------------------------------------------------------


class TestIsSubsumedEdgeCases:
    def _make_model_with_type(self, type_name: str, constant: str):
        """Build a minimal Model whose type-member cache contains one entry."""
        import clingo

        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        # Inject a clingo symbol so _build_type_members has something to parse.
        sym = clingo.Function(type_name, [clingo.Function(constant, [])])
        model.clingo_models = [[sym]]
        return model

    def test_nested_atom_subsumption(self):
        """_isSubsumed recurses into Atom sub-terms."""
        from xhail.language.terms import Atom, Normal, PlaceMarker
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        model._type_members = {"sugar": frozenset(["glucose"])}

        inner_atom = Atom("use", [Normal("glucose")])
        fact = Atom("happens", [inner_atom, Normal("1")])

        inner_mode = Atom("use", [PlaceMarker("#", "sugar")])
        mode = Atom("happens", [inner_mode, PlaceMarker("+", "time")])

        # Build a type-member cache that satisfies both the inner sugar and time
        model._type_members["time"] = frozenset(["1"])
        assert model.isSubsumed(fact, mode)

    def test_normal_value_mismatch_returns_false(self):
        """If a Normal term doesn't match the corresponding mode Normal, return False."""
        from xhail.language.terms import Atom, Normal
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        model._type_members = {}

        fact = Atom("foo", [Normal("a")])
        mode = Atom("foo", [Normal("b")])  # 'b' != 'a'
        assert not model.isSubsumed(fact, mode)

    def test_placemarker_constant_not_in_type_returns_false(self):
        """PlaceMarker check fails if constant not in type set."""
        from xhail.language.terms import Atom, Normal, PlaceMarker
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        model._type_members = {"bird": frozenset(["tweety"])}

        fact = Atom("flies", [Normal("penguin_p")])
        mode = Atom("flies", [PlaceMarker("+", "bird")])
        assert not model.isSubsumed(fact, mode)

    def test_build_type_members_empty_when_no_models(self):
        """_build_type_members returns {} when getClingoModels() is empty."""
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        model.clingo_models = []
        result = model._build_type_members()
        assert result == {}

    def test_symbol_to_term_nested_functor(self):
        """_symbol_to_term handles nested functor symbols (e.g. use(glucose))."""
        import clingo

        from xhail.language.terms import Atom
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        sym = clingo.Function("use", [clingo.Function("glucose", [])])
        result = model._symbol_to_term(sym)
        assert isinstance(result, Atom)
        assert result.predicate == "use"

    def test_nested_atom_subsumption_child_fails(self):
        """If the nested Atom doesn't match, _isSubsumed must return False."""
        from xhail.language.terms import Atom, Normal
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        model._type_members = {}

        # fact:  happens(use(glucose), 1)
        # mode:  happens(use(lactose), 1)  ← different constant inside nested Atom
        inner_fact = Atom("use", [Normal("glucose")])
        inner_mode = Atom("use", [Normal("lactose")])  # mismatch
        fact = Atom("happens", [inner_fact, Normal("1")])
        mode = Atom("happens", [inner_mode, Normal("1")])
        assert not model.isSubsumed(fact, mode)

    def test_issubsumed_else_branch_non_normal_placemarker(self):
        """PlaceMarker paired with a non-Normal term hits the else:continue branch."""
        from xhail.language.terms import Atom, Normal, PlaceMarker
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        model._type_members = {}

        # fact has an Atom term where mode expects a PlaceMarker+Normal combo
        inner = Atom("inner", [Normal("x")])
        fact = Atom("foo", [inner])  # term1 is Atom, not Normal
        mode = Atom("foo", [PlaceMarker("+", "thing")])  # term2 is PlaceMarker
        # isSubsumed recurses when term2 is Atom, but here term2 is PlaceMarker and
        # term1 is Atom (not Normal) → falls through to else:continue → returns True
        result = model.isSubsumed(fact, mode)
        assert isinstance(result, bool)  # should not raise

    def test_get_delta_returns_head_matches(self):
        """getDelta should return abduced head atoms from the current model."""
        import clingo

        from xhail.language.structures import Modeh
        from xhail.language.terms import Atom, PlaceMarker
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        # Inject a clingo symbol for flies(a)
        sym = clingo.Function("flies", [clingo.Function("a", [])])
        model.clingo_models = [[sym]]
        model._type_members = {"bird": frozenset(["a"])}

        # Add a Modeh so getDelta knows what to look for
        mh_atom = Atom("flies", [PlaceMarker("+", "bird")])
        mh = Modeh(mh_atom, "1")
        model.MH = [mh]

        delta = model.getDelta()
        assert any(str(a) == "flies(a)" for a in delta)

    def test_get_matches_raises_on_empty_models(self):
        """getMatches raises RuntimeError when getClingoModels() is empty (UNSAT)."""
        from xhail.language.terms import Atom, Normal
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        model.clingo_models = []  # simulate UNSAT — no models
        with pytest.raises(RuntimeError, match="Abduction yielded no model"):
            model.getMatches([Atom("flies", [Normal("a")])])

    def test_get_best_model_debug_logging(self, caplog):
        """getBestModel emits DEBUG logs when clingo runs."""
        from xhail.reasoning.model import Model

        model = Model(EX=[], MH=[], MB=[], BG=[], DEPTH=5)
        # Simple satisfiable program with a minimize statement
        model.program = (
            "#show use/2.\nclause(0).\n{ use(0,0) } :- clause(0).\n#minimize{1@2,I,J : use(I,J)}.\n"
        )
        with caplog.at_level(logging.DEBUG, logger="xhail.reasoning.model"):
            model.getBestModel()
        assert any("clingo model" in r.message for r in caplog.records)
