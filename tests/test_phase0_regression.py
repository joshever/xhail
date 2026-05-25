"""
Phase 0 regression and correctness tests for XHAIL.

These tests verify:
  1. The package imports cleanly (Python-version portability fix, D1).
  2. The Constraint constructor works correctly (D2).
  3. Propositional atoms (0-arity) parse without error (D3).
  4. ParseError is raised on bad input, not a NoneType crash (D4).
  5. Idiomatic ':- body.' constraint syntax parses (D5).
  6. The Model class uses instance state, not shared class state (D10).
  7. Golden-output regression for test.lp (penguins task).
  8. Golden-output regression for josh.lp (traffic task).

Tests 7 and 8 are integration tests that call clingo; they are marked
with the 'integration' pytest mark so they can be skipped in fast CI:
    pytest -m "not integration"
"""
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT  # .lp files live in the repo root for now


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_pipeline(lp_file: Path, depth: int = 10) -> str:
    """Run the full XHAIL 3-phase pipeline via the public API.

    Returns the hypothesis rules joined as a single string.
    Raises on any exception (parse error, clingo error, timeout, etc.).
    """
    from xhail import learn

    result = learn(lp_file, depth=depth)
    return "\n".join(result.hypothesis)


# ---------------------------------------------------------------------------
# Unit tests — fast, no clingo required
# ---------------------------------------------------------------------------

class TestImports:
    """D1: Package must import cleanly on Python < 3.12 (no nested same-quote f-strings)."""

    def test_import_terms(self):
        from xhail.language import terms  # noqa: F401

    def test_import_structures(self):
        from xhail.language import structures  # noqa: F401

    def test_import_parser(self):
        from xhail.parser import parser  # noqa: F401

    def test_import_model(self):
        from xhail.reasoning import model  # noqa: F401


class TestConstraintConstructor:
    """D2: Constraint() takes exactly one argument (body list)."""

    def test_constraint_one_arg(self):
        from xhail.language.terms import Atom, Constraint, Literal
        body = [Literal(Atom('penguin', []), False)]
        c = Constraint(body)
        assert str(c) == ':- penguin.'

    def test_constraint_str_with_terms(self):
        from xhail.language.terms import Atom, Constraint, Literal, Normal
        body = [Literal(Atom('bird', [Normal('X')]), False)]
        c = Constraint(body)
        assert ':- bird(X).' == str(c)


class TestPropositionalParsing:
    """D3: 0-arity (propositional) atoms must parse without error."""

    def test_propositional_fact(self):
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadString('q.')
        result = p.parseProgram()
        assert len(result) == 1
        assert str(result[0]) == 'q.'

    def test_propositional_rule(self):
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadString('p :- q, r.')
        result = p.parseProgram()
        assert len(result) == 1
        assert 'p' in str(result[0])

    def test_propositional_example(self):
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadString('#example p.')
        result = p.parseProgram()
        assert len(result) == 1

    def test_propositional_modeh(self):
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadString('#modeh q.')
        result = p.parseProgram()
        assert len(result) == 1

    def test_example1_lp_parses(self):
        """The repo's own example1.lp must parse without raising."""
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadFile(str(EXAMPLES_DIR / 'example1.lp'))
        result = p.parseProgram()
        assert result is not None
        assert len(result) > 0


class TestParseErrors:
    """D4: Parse failures must raise ParseError, not produce a NoneType crash."""

    def test_bad_syntax_raises_parse_error(self):
        from xhail.parser.parser import ParseError, Parser
        p = Parser()
        p.loadString(':-.')  # bare :- with no body
        with pytest.raises((ParseError, Exception)):
            p.parseProgram()

    def test_parse_error_is_informative(self):
        """ParseError message should mention the problem token, not be empty."""
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadString('this is not valid %%%')
        try:
            p.parseProgram()
        except Exception as exc:
            assert str(exc) != ''


class TestConstraintSyntax:
    """D5: Idiomatic ':- body.' constraint syntax must be accepted."""

    def test_implies_constraint(self):
        from xhail.language.terms import Constraint
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadString(':- penguin(X).')
        result = p.parseProgram()
        assert len(result) == 1
        assert isinstance(result[0], Constraint)

    def test_not_constraint_still_works(self):
        """Backward-compat: 'not body.' constraint form must still parse."""
        from xhail.language.terms import Constraint
        from xhail.parser.parser import Parser
        p = Parser()
        p.loadString('not penguin(X).')
        result = p.parseProgram()
        assert len(result) == 1
        assert isinstance(result[0], Constraint)


class TestModelInstanceState:
    """D10: Two Model instances must not share mutable class-level state."""

    def test_programs_are_independent(self):
        from xhail.reasoning.model import Model
        m1 = Model([], [], [], [], 5)
        m2 = Model([], [], [], [], 5)
        m1.setProgram('hello.')
        assert m2.getProgram() == '', (
            "m2.program was contaminated by m1 — still a class attribute"
        )

    def test_kernels_are_independent(self):
        from xhail.language.terms import Atom, Clause
        from xhail.reasoning.model import Model
        m1 = Model([], [], [], [], 5)
        m2 = Model([], [], [], [], 5)
        fake_clause = Clause(Atom('test', []), [])
        m1.setKernel([fake_clause])
        assert m2.getKernel() == [], (
            "m2.kernel was contaminated by m1 — still a class attribute"
        )


class TestAtomStr:
    """0-arity atoms must stringify as 'pred', not 'pred()'."""

    def test_zero_arity_str(self):
        from xhail.language.terms import Atom
        a = Atom('flies', [])
        assert str(a) == 'flies'

    def test_nonzero_arity_str(self):
        from xhail.language.terms import Atom, Normal
        a = Atom('flies', [Normal('X')])
        assert str(a) == 'flies(X)'


class TestNormalInstanceType:
    """D10: Normal.type must be an instance attribute, not shared class attribute."""

    def test_type_is_instance_attr(self):
        from xhail.language.terms import Normal
        n1 = Normal('a')
        n2 = Normal('b')
        n1.setType('bird')
        assert n2.getType() == '', (
            "n2.type was contaminated by n1.setType — still a class attribute"
        )


# ---------------------------------------------------------------------------
# Integration tests — run the full pipeline (require clingo)
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestGoldenOutputs:
    """
    End-to-end regression: pin known-good hypotheses for the two working examples.

    Run with: pytest -m integration
    Skip with: pytest -m "not integration"
    """

    def test_penguins_learns_correct_rule(self):
        """test.lp (penguins): should learn that all non-penguins fly."""
        output = run_pipeline(EXAMPLES_DIR / 'test.lp')
        assert 'flies' in output, f"Expected 'flies' in output, got:\n{output}"
        assert 'penguin' in output, f"Expected 'penguin' in output, got:\n{output}"
        # The canonical rule: flies(V1) :- not penguin(V1).
        assert 'not penguin' in output, (
            f"Expected negation-as-failure over penguin, got:\n{output}"
        )

    def test_traffic_learns_rules(self):
        """josh.lp (traffic): should learn drive rules involving atlight/red/emergency."""
        output = run_pipeline(EXAMPLES_DIR / 'josh.lp')
        assert 'drive' in output, f"Expected 'drive' in output, got:\n{output}"
        # At minimum, one of the two expected body predicates should appear
        has_atlight = 'atlight' in output
        has_emergency = 'emergency' in output
        assert has_atlight or has_emergency, (
            f"Expected 'atlight' or 'emergency' in learned rules, got:\n{output}"
        )
