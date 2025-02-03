class Term:
    pass

class Atom:
    def __init__(self, predicate: str, terms: list[Term]):
        self.terms = terms
        self.predicate = predicate
    
    def __str__(self):
        return self.predicate + '(' + ','.join([term.toString() for term in self.terms]) + ')'

"""
class Clause:
    def __init__(self, head: Atom, body: list[Literal]):
        self.head = head
        self.body = body

    def isHorn(self):
        for literal in self.body:
            if literal.negation == True:
                return False
        return True
    
    def toString(self):
        return self.head.toString + ' :- ' + ', '.join([literal.toString() for literal in self.body])

class Fact(Clause):
    def __init__(self, head: Atom):
        self.head = head
    
    def toString(self):
        return self.head.toString() + '.\n'

class Constraint(Clause):
    def __init__(self, body: list[Literal]):
        self.body = body

    def toString(self):
        return ':- ' + ', '.join([literal.toString() for literal in self.body]) + '.\n'

class LogicProgram():
    def __init__(self, clauses: list[Clause]):
        self.clauses = clauses

    def isHorn(self):
        for clause in self.clauses:
            if clause.isHorn() == False:
                return False
        return True
    
    def toString(self):
        result = ""
        for clause in self.clauses:
            result += clause.toString() + '.\n'
        return result

class Normal(Term):
    def __init__(self, value: str): #constant
        self.value = value

    def toString(self):
        return self.value

class Normal(Term):
    def __init__(self, function: Atom): #function
        self.function = function

    def toString(self):
        self.function.toString()

class PlaceMarker(Term):
    def __init__(self, marker: str, type: str):
        self.marker = marker
        self.type = type
"""