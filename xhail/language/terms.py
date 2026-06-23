# ----- CLASS DEFINITIONS FOR HOLDING XHAIL DATA ----- #
# ---------- term (covers atom, placemarker, and normal) ---------- #
class Term:
    pass


# ---------- atom term ---------- #
class Atom(Term):
    def __init__(self, predicate: str, terms: list[Term]):
        self.terms = terms
        self.predicate = predicate

    def __str__(self):
        if not self.terms:
            return self.predicate
        clause_terms = ",".join([str(x) for x in self.terms])
        return f"{self.predicate}({clause_terms})"

    def getVariables(self):  # return Term (with its type)
        variables = []
        for term in self.terms:
            # Ground Normals (from '#' placemarkers) are literal constants in the
            # hypothesis — they are NOT variables and must not appear in type constraints.
            if isinstance(term, Normal) and term.getType() != "" and not term.ground:
                variables += [term]
            elif isinstance(term, Atom):
                variables += term.getVariables()
            else:
                continue
        return variables

    def getTypes(self):
        variables = self.getVariables()
        return [str(Atom(var.type, [var.value])) for var in variables]


# ---------- normal term ---------- #
class Normal(Term):
    def __init__(self, value: str, ground: bool = False):
        self.value = value
        self.type = ""  # instance attribute — was a class attribute (D10: shared mutable state)
        # ground=True means this term came from a '#' placemarker and should remain
        # as a literal constant in the learned hypothesis (not generalised to a variable).
        self.ground = ground

    def __str__(self):
        return self.value

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def setGround(self, ground: bool) -> None:
        """Mark this term as a ground constant (from a '#' placemarker)."""
        self.ground = ground


# ---------- placemarker term ---------- #
class PlaceMarker(Term):
    def __init__(self, marker: str, type: str):
        self.marker = marker
        self.type = type

    def __str__(self):
        return self.marker + self.type


# ---------- literal ---------- #
class Literal:
    def __init__(self, atom: Atom, negation: bool):
        self.atom = atom
        self.negation = negation

    def __str__(self):
        return ("not " if self.negation else "") + str(self.atom)


class MiscLiteral:
    def __init__(self, misc: str):
        self.misc = misc

    def __str__(self):
        return self.misc


# ---------- noraml clause (covers normal clause, fact and constraint) ---------- #
class Clause:
    def __init__(self, head: Atom, body: list[Literal]):
        self.head = head
        self.body = body

    def isHorn(self):
        for literal in self.body:
            if literal.negation:
                return False
        return True

    def __str__(self):
        return str(self.head) + " :- " + ", ".join([str(literal) for literal in self.body]) + "."

    def generalise(self):  # returned generalised clause.
        matching = {}  # lowercase to uppercase
        unique = set()
        # 1 search tree
        unique.update(self.findConstants(self.head, unique))
        for literal in self.body:
            unique.update(self.findConstants(literal.atom, unique))
        # map constants to variables
        ordered = sorted(list(unique))
        for i in range(1, len(ordered) + 1):
            matching[ordered.pop()] = "V" + str(i)
        # 2 update tree
        head = self.replaceConstants(self.head, matching)
        literals = []
        for literal in self.body:
            atom = self.replaceConstants(literal.atom, matching)
            literals.append(Literal(atom, literal.negation))
        clause = Clause(head, literals)
        return clause

    def findConstants(self, atom, unique):
        """Collect all non-ground constant values for variable generalisation.

        Ground Normals (``term.ground = True``) come from ``#`` placemarkers and
        are literal constants in the hypothesis — they are intentionally excluded
        so they remain unchanged after generalisation.
        """
        terms = atom.terms  # PlaceHolder / Normal / Atom / None
        for term in terms:
            if isinstance(term, Normal) and not term.ground:
                unique.add(term.value)
            elif isinstance(term, Atom):
                unique.update(self.findConstants(term, unique))
        return unique

    def replaceConstants(self, atom, matching):
        """Replace non-ground constants with variable names from *matching*.

        Ground Normals are preserved as-is so they appear literally in the
        learned hypothesis (e.g. ``glucose`` stays ``glucose``, not ``V1``).
        Type annotations are propagated to new variable Normals so that the
        induction phase can generate correct type-constraint literals.
        """
        newAtom = Atom(atom.predicate, [])
        terms = atom.terms
        for term in terms:
            if isinstance(term, Normal):
                if term.ground:
                    # Preserve ground constant (from '#' placemarker) unchanged,
                    # carrying the type annotation so getVariables() still works.
                    new_normal = Normal(term.value, ground=True)
                    new_normal.setType(term.type)
                    newAtom.terms.append(new_normal)
                else:
                    # Replace with variable; carry the type to the new variable Normal
                    # so that getVariables() / getTypes() produce correct constraints.
                    new_normal = Normal(matching[term.value])
                    new_normal.setType(term.type)
                    newAtom.terms.append(new_normal)
            else:
                newTerm = self.replaceConstants(
                    term, matching
                )  # D8 fix: was passing self as first arg
                newAtom.terms.append(newTerm)
        return newAtom

    def getVariables(self):
        variables = []
        variables += self.head.getVariables()
        for literal in self.body:
            variables += literal.atom.getVariables()
        return variables

    def getTypes(self):
        variables = self.getVariables()
        return [str(Atom(var.type, [var.value])) for var in variables]


# ---------- fact clause ---------- #
class Fact(Clause):
    def __init__(self, head: Atom):
        self.head = head

    def __str__(self):
        return str(self.head) + "."


# ---------- constraint clause ---------- #
class Constraint(Clause):
    def __init__(self, body: list[Literal]):
        self.body = body

    def __str__(self):
        body_str = ", ".join(
            str(lit) for lit in self.body
        )  # D1 fix: was a nested same-quote f-string (PEP 701)
        return f":- {body_str}."
