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
        clause_terms = ','.join([str(x) for x in self.terms])
        return f'{self.predicate}({clause_terms})'

# ---------- normal term ---------- #   
class Normal(Term):
    def __init__(self, value: str): #constant
        self.value = value

    def __str__(self):
        return self.value

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
        return ('not ' if self.negation else '') + str(self.atom)
    
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
            if literal.negation == True:
                return False
        return True
    
    def __str__(self):
        return str(self.head) + ' :- ' + ', '.join([str(literal) for literal in self.body]) + '.'

# ---------- fact clause ---------- #   
class Fact(Clause):
    def __init__(self, head: Atom):
        self.head = head
    
    def __str__(self):
        return str(self.head) + '.'

# ---------- constraint clause ---------- #   
class Constraint(Clause):
    def __init__(self, body: list[Literal]):
        self.body = body

    def __str__(self):
        return f':- {', '.join([str(literal) for literal in self.body])}.'

"""
# ---------- program??? ---------- #   

Q: is a program only made of clauses?

class Program():
    def __init__(self, clauses: list[Clause]):
        self.clauses = clauses

    def isHorn(self):
        for clause in self.clauses:
            if clause.isHorn() == False:
                return False
        return True
    
    def __str__(self):
        result = ""
        for clause in self.clauses:
            result += str(clause) + '.\n'
        return result
"""