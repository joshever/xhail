"""
Unit tests for xhail.language — term and clause data structures.

Covers:
- Atom / Normal / PlaceMarker / Literal string representations
- Fact and Constraint string representations
- Clause.isHorn()
- Clause.generalise() — the key pre-processing step before induction
- Modeh / Modeb program generation
"""


from xhail.language.structures import Modeb, Modeh
from xhail.language.terms import (
    Atom,
    Clause,
    Constraint,
    Fact,
    Literal,
    Normal,
    PlaceMarker,
)

# ---------------------------------------------------------------------------
# Atom
# ---------------------------------------------------------------------------

class TestAtom:
    def test_zero_arity(self):
        assert str(Atom("flies", [])) == "flies"

    def test_one_arg(self):
        assert str(Atom("bird", [Normal("X")])) == "bird(X)"

    def test_two_args(self):
        a = Atom("atlight", [Normal("car1"), Normal("a")])
        assert str(a) == "atlight(car1,a)"

    def test_get_variables_empty(self):
        """0-arity atom has no variables."""
        assert Atom("p", []).getVariables() == []

    def test_get_variables_with_typed_normal(self):
        n = Normal("V1")
        n.setType("bird")
        atom = Atom("flies", [n])
        variables = atom.getVariables()
        assert len(variables) == 1
        assert variables[0].value == "V1"

    def test_get_variables_untyped_normal_excluded(self):
        """Untyped Normal terms (constants) are not returned as variables."""
        n = Normal("penguin")  # no type set
        atom = Atom("bird", [n])
        assert atom.getVariables() == []


# ---------------------------------------------------------------------------
# Normal
# ---------------------------------------------------------------------------

class TestNormal:
    def test_str(self):
        assert str(Normal("abc")) == "abc"

    def test_type_default_empty(self):
        assert Normal("x").getType() == ""

    def test_set_type(self):
        n = Normal("x")
        n.setType("bird")
        assert n.getType() == "bird"

    def test_type_is_instance_not_class(self):
        """Setting type on one Normal must not affect another (D10 regression)."""
        n1 = Normal("a")
        n2 = Normal("b")
        n1.setType("car")
        assert n2.getType() == ""


# ---------------------------------------------------------------------------
# Literal
# ---------------------------------------------------------------------------

class TestLiteral:
    def test_positive(self):
        lit = Literal(Atom("bird", [Normal("X")]), False)
        assert str(lit) == "bird(X)"

    def test_negative(self):
        lit = Literal(Atom("penguin", [Normal("X")]), True)
        assert str(lit) == "not penguin(X)"

    def test_positive_propositional(self):
        lit = Literal(Atom("p", []), False)
        assert str(lit) == "p"

    def test_negative_propositional(self):
        lit = Literal(Atom("q", []), True)
        assert str(lit) == "not q"


# ---------------------------------------------------------------------------
# Fact
# ---------------------------------------------------------------------------

class TestFact:
    def test_fact_with_args(self):
        f = Fact(Atom("bird", [Normal("a")]))
        assert str(f) == "bird(a)."

    def test_fact_propositional(self):
        f = Fact(Atom("p", []))
        assert str(f) == "p."


# ---------------------------------------------------------------------------
# Constraint
# ---------------------------------------------------------------------------

class TestConstraint:
    def test_single_literal(self):
        body = [Literal(Atom("penguin", [Normal("X")]), False)]
        c = Constraint(body)
        assert str(c) == ":- penguin(X)."

    def test_negated_literal(self):
        body = [Literal(Atom("flies", [Normal("X")]), True)]
        c = Constraint(body)
        assert str(c) == ":- not flies(X)."

    def test_multi_literal(self):
        body = [
            Literal(Atom("bird", [Normal("X")]), False),
            Literal(Atom("penguin", [Normal("X")]), True),
        ]
        c = Constraint(body)
        assert str(c) == ":- bird(X), not penguin(X)."


# ---------------------------------------------------------------------------
# Clause
# ---------------------------------------------------------------------------

class TestClause:
    def _make_penguins_clause(self):
        """flies(a) :- bird(a), not penguin(a)."""
        head = Atom("flies", [Normal("a")])
        body = [
            Literal(Atom("bird", [Normal("a")]), False),
            Literal(Atom("penguin", [Normal("a")]), True),
        ]
        return Clause(head, body)

    def test_str(self):
        c = self._make_penguins_clause()
        assert str(c) == "flies(a) :- bird(a), not penguin(a)."

    def test_is_horn_false_when_negated_body(self):
        c = self._make_penguins_clause()
        assert c.isHorn() is False

    def test_is_horn_true_when_all_positive(self):
        head = Atom("bird", [Normal("X")])
        body = [Literal(Atom("animal", [Normal("X")]), False)]
        c = Clause(head, body)
        assert c.isHorn() is True

    def test_generalise_replaces_constants_with_variables(self):
        """Clause.generalise() should swap ground constants for Vn variables."""
        head = Atom("flies", [Normal("a")])
        body = [Literal(Atom("bird", [Normal("a")]), False)]
        c = Clause(head, body)
        g = c.generalise()
        # The constant 'a' should become some variable Vn
        generalised_str = str(g)
        assert "a" not in generalised_str
        assert "V" in generalised_str

    def test_generalise_consistent_variable_mapping(self):
        """The same constant in head and body should map to the same variable."""
        head = Atom("flies", [Normal("a")])
        body = [
            Literal(Atom("bird", [Normal("a")]), False),
            Literal(Atom("penguin", [Normal("a")]), True),
        ]
        c = Clause(head, body)
        g = c.generalise()
        # All occurrences of 'a' should become the same Vn
        parts = str(g).split(":-")
        head_var = parts[0].strip().split("(")[1].rstrip(")")
        body_parts = parts[1].strip()
        assert head_var in body_parts

    def test_generalise_two_constants_get_different_variables(self):
        head = Atom("atlight", [Normal("car1"), Normal("a")])
        body = [Literal(Atom("red", [Normal("a")]), False)]
        c = Clause(head, body)
        g = c.generalise()
        generalised_str = str(g)
        # Should have V1 and V2 (or similar) — two distinct variables
        assert "V1" in generalised_str
        assert "V2" in generalised_str


# ---------------------------------------------------------------------------
# Modeh / Modeb program generation
# ---------------------------------------------------------------------------

class TestModehProgram:
    def test_standard_arity_generates_choice_rule(self):
        atom = Atom("flies", [PlaceMarker("+", "bird")])
        mh = Modeh(atom, "*")
        program = mh.createProgram()
        assert "abduced_flies" in program
        assert "#minimize" in program

    def test_zero_arity_generates_valid_program(self):
        atom = Atom("q", [])
        mh = Modeh(atom, "*")
        program = mh.createProgram()
        # Should not produce 'q()' — must be 'q'
        assert "q()" not in program
        assert "abduced_q" in program
        assert "#minimize" in program


class TestModebProgram:
    def test_non_negated_returns_empty(self):
        atom = Atom("penguin", [PlaceMarker("+", "bird")])
        mb = Modeb(atom, "*", negation=False)
        assert mb.createProgram() == ""

    def test_negated_generates_negation_rule(self):
        atom = Atom("penguin", [PlaceMarker("+", "bird")])
        mb = Modeb(atom, "*", negation=True)
        program = mb.createProgram()
        assert "not_penguin" in program
        assert "not penguin" in program
