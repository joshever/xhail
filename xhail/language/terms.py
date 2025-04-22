# --------------------------------- #
# ---------- TERM CLASS ----------- #
# --------------------------------- #

class Term:
    pass

# -------------------------------------- #
# ---------- ATOM TERM CLASS ----------- #
# -------------------------------------- #

class Atom(Term):
    type = ''
    arity = -1

    def __init__(self, predicate: str, terms: list[Term]):
        self.terms = terms
        self.predicate = predicate
        self.arity = len(self.terms)
    
    def __str__(self):
        self.arity = len(self.terms)
        clause_terms = ','.join([str(x) for x in self.terms])
        return f'{self.predicate}{'(' + clause_terms + ')' if self.arity != 0 else ''}'

    def getVariables(self): # return Term (with its type)
        variables = []
        for term in self.terms:
            if isinstance(term, Normal) and term.getType() != '' and term.getType() != 'constant':
                variables += [term]
            elif isinstance(term, Atom):
                variables += term.getVariables()
            else: 
                continue
        return variables
    
    def getTypes(self):
        variables = self.getVariables()
        return [str(Atom(var.type, [var.value])) for var in variables]
    
    def getArity(self):
        return len(self.terms)

# ---------------------------------------- #
# ---------- NORMAL TERM CLASS ----------- #
# ---------------------------------------- #

class Normal(Term):
    type = ''

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value
    
    def getType(self):
        return self.type
    
    def setType(self, type):
        self.type = type

# --------------------------------------------- #
# ---------- PLACEMARKER TERM CLASS ----------- #
# --------------------------------------------- #

class PlaceMarker(Term):
    def __init__(self, marker: str, type: str):
        self.marker = marker
        self.type = type

    def __str__(self):
        return self.marker + self.type

# ------------------------------------ #
# ---------- LITERAL CLASS ----------- #
# ------------------------------------ #

class Literal:
    def __init__(self, atom: Atom, negation: bool):
        self.atom = atom
        self.negation = negation
    
    def __str__(self):
        return ('not ' if self.negation else '') + str(self.atom)
    
# ----------------------------------------- #
# ---------- MISC LITERAL CLASS ----------- #
# ----------------------------------------- #

class MiscLiteral:
    def __init__(self, misc: str, negation: bool):
        self.misc = misc
        self.negation = negation
    
    def __str__(self):
        return ('not ' if self.negation else '') + self.misc

# ----------------------------------- #
# ---------- CLAUSE CLASS ----------- #
# ----------------------------------- #

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
        return str(self.head) + (' :- ' + ', '.join([str(literal) for literal in self.body]) if self.body != [] else '') + '.'
    
    def generalise(self): # returned generalised clause.
        matching = {} # lowercase to uppercase
        unique = set()
        # 1 search tree
        unique.update(self.findConstants(self.head, unique))
        for literal in self.body:
            unique.update(self.findConstants(literal.atom, unique))
        # map constants to variables
        ordered = sorted(list(unique))
        for i in range(1, len(ordered)+1):
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
        terms = atom.terms # PlaceHolder / Normal / Atom / None
        for term in terms:
            if isinstance(term, Normal):
                if term.type != 'constant':
                    unique.add(term.value)
                else:
                    print(term, term.type)
            elif isinstance(term, Atom):
                if term.type == 'constant':
                    continue
            else:
                unique.update(self.findConstants(term, unique))
        return unique
    
    def replaceConstants(self, atom, matching):
        newAtom = Atom(atom.predicate, [])
        terms = atom.terms
        for term in terms:
            if isinstance(term, Normal):
                if term.type != 'constant':
                    newAtom.terms.append(Normal(matching[term.value]))
                else:
                    newAtom.terms.append(Normal(term.value))
            elif isinstance(term, Atom) and term.type == 'constant':
                newAtom.terms.append(term)
            else:
                newTerm = self.replaceConstants(term, matching)
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

# --------------------------------- #
# ---------- FACT CLASS ----------- #
# --------------------------------- #

class Fact(Clause):
    def __init__(self, head: Atom):
        self.head = head
    
    def __str__(self):
        return str(self.head) + '.'

# --------------------------------------- #
# ---------- CONSTRAINT CLASS ----------- #
# --------------------------------------- #

class Constraint(Clause):
    def __init__(self, body: list[Literal]):
        self.body = body

    def __str__(self):
        return f':- {', '.join([str(literal) for literal in self.body])}.'