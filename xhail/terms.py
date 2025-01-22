class Term:
    pass

class Atom:
    def __init__(self, predicate: str, terms: list[Term]):
        self.terms = terms
        self.predicate = predicate

class Literal:
    def __init__(self, atom: Atom, negation: bool):
        self.atom = atom
        self.negation = negation

class Clause:
    def __init__(self, head: Atom, body: list[Literal]):
        self.head = head
        self.body = body

    def isHorn(self):
        for literal in self.body:
            if literal.negation == True:
                return False
        return True

class Fact(Clause):
    def __init__(self, head: Atom):
        super().__init__(head, body=True)

class Constraint(Clause):
    def __init__(self, body: list[Literal]):
        super().__init__(body, head=False)

class LogicProgram():
    def __init__(self, clauses: list[Clause]):
        self.clauses = clauses

    def isHorn(self):
        for clause in self.clauses:
            if clause.isHorn() == False:
                return False
        return True

class Normal(Term):
    def __init__(self, value: str): #constant
        self.value = value

class Normal(Term):
    def __init__(self, function: Atom):
        self.function = function

class PlaceMarker(Term):
    def __init__(self, marker: str, type: str):
        self.marker = marker
        self.type = type


        
