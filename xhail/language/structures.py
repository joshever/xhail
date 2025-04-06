import copy
from ..language.terms import Atom, Normal, PlaceMarker

# ----------------------------------- #
# ---------- EXAMPLE CLASS ---------- #
# ----------------------------------- #

class Example:
    KEY_WORD = '#example'
    WEIGHT_OPERATOR = '='
    PRIORITY_OPERATOR = '@'
    weight = 1
    priority = 1

    def __init__(self, atom: Atom, negation=False):
        self.atom = atom
        self.negation = negation

    def setWeight(self, weight):
        self.weight = weight

    def setPriority(self, priority):
        self.priority = priority

    def createProgram(self):
        program = []
        negation_string = 'not ' if self.negation else ''
        program.append('%#maximize{' + f'{str(self.weight)}@{str(self.priority)} : {negation_string}{self.atom}' + '}.')
        program.append(f':- {self.atom}.' if self.negation else f':- not {self.atom}.')
        return '\n'.join(program)
    
    def __str__(self):
        return '#example '+ ('not ' if self.negation else '') + str(self.atom)

# ---------------------------------- #
# ---------- MODEH CLASS ----------- #
# ---------------------------------- #

class Modeh:
    KEY_WORD = '#modeh'
    WEIGHT_OPERATOR = '='
    PRIORITY_OPERATOR = '@'
    CONSTRAINT_OPERATOR = ':'
    CONSTRAINT_SEPARATOR = '-'
    weight = 1
    priority = 2
    min = 0
    max = 1000000

    def __init__(self, atom: Atom, n: str):
        self.atom = atom
        self.n = n

    def setWeight(self, weight):
        self.weight = weight

    def setPriority(self, priority):
        self.priority = priority

    def setMax(self, max):
        self.max = max

    def setMin(self, min):
        self.min = min

    def getMax(self):
        return self.max
    
    def getMin(self):
        return self.min

    def generalise(self, atom, n=1):
        terms = atom.terms
        for idt, term in enumerate(terms):
            if isinstance(term, PlaceMarker):
                value = f'V{n}'
                type = term.type
                atom.terms[idt] = Normal(value)
                atom.terms[idt].setType(type)
                n += 1
            else:
                term, n = self.generalise(term, n)
        return atom, n
    
    def createProgram(self):
        new_atom = copy.deepcopy(self.atom)
        generalised_atom, n = self.generalise(new_atom)
        types = ', '.join(generalised_atom.getTypes())
        variables = ', '.join([f"V{i}" for i in range(1, n)])

        program = []
        program.append(str(self.min) + ' { abduced_' + str(generalised_atom) + f'{(':' + types) if self.atom.arity != 0 else ''} ' + '} ' + str(self.max) + '.')
        program.append('#minimize{' + f'{str(self.weight)}@{str(self.priority)}{(',' + variables) if self.atom.arity != 0 else ''}: abduced_{generalised_atom}' + f'{(',' + types) if self.atom.arity != 0 else ''}' + '}.')
        program.append(f'{generalised_atom} :- abduced_{generalised_atom}{(',' + types) if self.atom.arity != 0 else ''}.')
        return '\n'.join(program)

    def __str__(self):
        return '#modeh ' + str(self.atom)
    
# ---------------------------------- #
# ---------- MODEB CLASS ----------- #
# ---------------------------------- #

class Modeb:
    KEY_WORD = '#modeb'
    WEIGHT_OPERATOR = '='
    PRIORITY_OPERATOR = '@'
    CONSTRAINT_OPERATOR = ':'
    CONSTRAINT_SEPARATOR = '~'
    weight = 1
    priority = 1
    min = 0
    max = 1000000

    def __init__(self, atom: Atom, n: str, negation=False):
        self.atom = atom
        self.n = n
        self.negation = negation

    def setWeight(self, weight):
        self.weight = weight

    def setPriority(self, priority):
        self.priority = priority

    def setMax(self, max):
        self.max = max

    def setMin(self, min):
        self.min = min

    def generalise(self, atom, n=1):
        terms = atom.terms
        for idt, term in enumerate(terms):
            if isinstance(term, PlaceMarker):
                value = f'V{n}'
                type = term.type
                atom.terms[idt] = Normal(value)
                atom.terms[idt].setType(type)
                n += 1
            else:
                term, n = self.generalise(term, n)
        return atom, n
    
    def createProgram(self):
        if self.negation == True:
            new_atom = copy.deepcopy(self.atom)
            generalised_atom, _ = self.generalise(new_atom)
            types = ', '.join(generalised_atom.getTypes())
            program = f"{str(Atom(f"not_{generalised_atom.predicate}", generalised_atom.terms))} :- not {generalised_atom}, {types}."
        else:
            program = ""

        return program
    
    def __str__(self):
        return f'#modeb {'not ' if self.negation == True else ''}{str(self.atom)}'