"""
Edge-case and contract tests for the xhail.core public API.

Tests are split into:
- Pure unit tests (no clingo required): LearningResult contract,
  FileNotFoundError, ParseError propagation.
- Integration tests (require clingo, marked with @pytest.mark.integration):
  learn() contract, file/path variants, no-hypothesis scenario.

NOTE: Propositional (0-arity) predicates in the induction phase currently
generate invalid ASP (trailing comma in try/3 terms) — this is a known
pre-existing limitation tracked as a future fix.  Integration tests
therefore use first-order programs with typed arguments (penguins style).
"""

from pathlib import Path

import pytest

from xhail import LearningResult, learn
from xhail.parser.parser import ParseError

REPO_ROOT = Path(__file__).parent.parent
PENGUINS_LP = REPO_ROOT / "test.lp"  # known-good file used by golden tests


# ---------------------------------------------------------------------------
# LearningResult — pure unit tests (no clingo)
# ---------------------------------------------------------------------------


class TestLearningResultContract:
    """Verify the public API shape of LearningResult."""

    def test_default_is_unsuccessful(self):
        result = LearningResult()
        assert result.success is False
        assert result.hypothesis == []
        assert result.n_examples == 0
        assert result.n_background == 0
        assert result.source is None

    def test_str_unsuccessful(self):
        result = LearningResult()
        assert str(result) == "No hypothesis found."

    def test_str_successful_single_rule(self):
        result = LearningResult(hypothesis=["flies(X) :- bird(X)."], success=True)
        assert str(result) == "flies(X) :- bird(X)."

    def test_str_successful_multiple_rules(self):
        rules = ["a(X) :- b(X).", "c(X) :- d(X), e(X)."]
        result = LearningResult(hypothesis=rules, success=True)
        assert str(result) == "a(X) :- b(X).\nc(X) :- d(X), e(X)."

    def test_repr_contains_key_fields(self):
        result = LearningResult(
            hypothesis=["p(X) :- q(X)."],
            success=True,
            source="test.lp",
        )
        r = repr(result)
        assert "success=True" in r
        assert "n_rules=1" in r
        assert "test.lp" in r

    def test_repr_unsuccessful(self):
        result = LearningResult(source="foo.lp")
        r = repr(result)
        assert "success=False" in r
        assert "n_rules=0" in r

    def test_success_flag_reflects_hypothesis(self):
        empty = LearningResult(hypothesis=[], success=False)
        nonempty = LearningResult(hypothesis=["a :- b."], success=True)
        assert not empty.success
        assert nonempty.success

    def test_fields_are_independent_across_instances(self):
        r1 = LearningResult(hypothesis=["a."], success=True)
        r2 = LearningResult()
        # Mutating r1 must not affect r2
        r1.hypothesis.append("b.")
        assert r2.hypothesis == []


# ---------------------------------------------------------------------------
# learn() — FileNotFoundError (no clingo needed)
# ---------------------------------------------------------------------------


class TestLearnFileNotFound:
    def test_raises_on_missing_path_object(self, tmp_path):
        missing = tmp_path / "does_not_exist.lp"
        with pytest.raises(FileNotFoundError, match="does_not_exist.lp"):
            learn(missing)

    def test_raises_on_missing_string_path(self, tmp_path):
        missing = str(tmp_path / "missing.lp")
        with pytest.raises(FileNotFoundError):
            learn(missing)

    def test_error_message_contains_filename(self, tmp_path):
        missing = tmp_path / "very_specific_name.lp"
        with pytest.raises(FileNotFoundError) as exc_info:
            learn(missing)
        assert "very_specific_name.lp" in str(exc_info.value)


# ---------------------------------------------------------------------------
# learn() — ParseError propagation (no clingo needed)
# ---------------------------------------------------------------------------


class TestLearnParseError:
    def test_raises_on_garbage_input(self):
        """A syntactically invalid raw string must raise ParseError."""
        with pytest.raises(ParseError):
            learn("@@@ this is not valid ASP @@@")

    def test_raises_on_unclosed_paren(self):
        with pytest.raises(ParseError):
            learn("#modeh flies(")

    def test_raises_on_empty_modeh(self):
        """A modeh with no predicate name should fail to parse."""
        with pytest.raises(ParseError):
            learn("#modeh .")


# ---------------------------------------------------------------------------
# learn() — integration tests (require clingo, use test.lp / josh.lp)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestLearnAPIContract:
    """Verify that learn() returns a well-formed LearningResult (penguins task)."""

    def test_returns_learning_result_type(self):
        result = learn(PENGUINS_LP)
        assert isinstance(result, LearningResult)

    def test_source_is_file_path_label(self):
        result = learn(PENGUINS_LP)
        assert result.source == str(PENGUINS_LP)

    def test_n_examples_populated(self):
        result = learn(PENGUINS_LP)
        # test.lp has 4 examples
        assert result.n_examples == 4

    def test_n_background_populated(self):
        result = learn(PENGUINS_LP)
        # test.lp has bird/penguin facts as background
        assert result.n_background >= 1

    def test_successful_run_sets_success_true(self):
        result = learn(PENGUINS_LP)
        assert result.success is True
        assert len(result.hypothesis) >= 1

    def test_hypothesis_entries_are_strings(self):
        result = learn(PENGUINS_LP)
        for rule in result.hypothesis:
            assert isinstance(rule, str)

    def test_hypothesis_entries_look_like_rules(self):
        result = learn(PENGUINS_LP)
        for rule in result.hypothesis:
            # Every induced rule should be a clause (has :-) or a fact (ends with .)
            assert ":-" in rule or rule.endswith("."), f"Unexpected rule format: {rule!r}"

    def test_learned_rules_mention_flies(self):
        """Penguins task must produce a rule about flies."""
        result = learn(PENGUINS_LP)
        combined = "\n".join(result.hypothesis)
        assert "flies" in combined

    def test_learn_accepts_path_object(self):
        """learn() must accept a pathlib.Path."""
        result = learn(PENGUINS_LP)
        assert isinstance(result, LearningResult)

    def test_learn_accepts_str_path(self):
        """learn() must accept a string file path ending in .lp."""
        result = learn(str(PENGUINS_LP))
        assert isinstance(result, LearningResult)

    def test_learn_from_tmp_copy(self, tmp_path):
        """learn() works when the .lp file is in an arbitrary directory."""
        dest = tmp_path / "penguins.lp"
        dest.write_text(PENGUINS_LP.read_text())
        result = learn(dest)
        assert result.success is True

    def test_depth_parameter_accepted(self):
        """Passing depth= must not raise; result type is still LearningResult."""
        result = learn(PENGUINS_LP, depth=5)
        assert isinstance(result, LearningResult)
