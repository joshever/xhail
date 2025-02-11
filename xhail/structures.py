from terms import Atom, Normal


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
        program.append('#maximize{' + f'{str(self.weight)}@{str(self.priority)} : {negation_string}{self.atom}' + '}.')
        program.append(f':- {self.atom}.' if self.negation else f':- not {self.atom}.')
        return '\n'.join(program)
    
    def __str__(self):
        return ('not ' if self.negation else '') + str(self.atom)

class Modeh:
    KEY_WORD = '#modeh'
    WEIGHT_OPERATOR = '='
    PRIORITY_OPERATOR = '@'
    CONSTRAINT_OPERATOR = ':'
    CONSTRAINT_SEPARATOR = '-'
    weight = 1
    priority = 1
    min = 0 #default 0
    max = 1000000 #this just has to be super big by default

    def __init__(self, atom: Atom, n: str): #these will be placeholder atoms
        self.atom = atom
        self.n = n
        self.types = [term.type for term in atom.terms]

    def setWeight(self, weight):
        self.weight = weight

    def setPriority(self, priority):
        self.priority = priority

    def setMax(self, max):
        self.max = max

    def setMin(self, min):
        self.min = min
    
    def createProgram(self):
        alphabet = [Normal(chr(i)) for i in range(ord('A'), ord('Z'))]
        vars = alphabet[:len(self.atom.terms)]
        vars_string = ', '.join([str(v) for v in vars])
        newAtom = Atom(self.atom.predicate, vars)

        program = []
        constraint_types = ', '.join([str(Atom(t, vars)) for t in self.types])
        program.append(str(self.min) + ' { abduced_' + str(newAtom) + ' : '+ constraint_types + ' } ' + str(self.max) + '.')
        program.append('#minimize{' + f'{str(self.weight)}@{str(self.priority)}, {vars_string}: abduced_{newAtom}, {constraint_types}' + '}.')
        clause_types = ', '.join([str(Atom(t, vars)) for t in self.types])
        program.append(f'{newAtom} :- abduced_{newAtom}, {clause_types}.')
        program.append(f'#show abduced_{newAtom.predicate}/{str(len(newAtom.terms))}.')
        return '\n'.join(program)
    
    def __str__(self):
        return 'modeh ' + str(self.atom)
    

class Modeb:
    KEY_WORD = '#modeb'
    WEIGHT_OPERATOR = '='
    PRIORITY_OPERATOR = '@'
    CONSTRAINT_OPERATOR = ':'
    CONSTRAINT_SEPARATOR = '-'
    weight = 1
    priority = 1
    min = 0 #default 0
    max = 1000000 #this just has to be super big by default

    def __init__(self, atom: Atom, n: str, negation=False): #these will be placeholder atoms
        self.atom = atom
        self.n = n
        self.negation = negation
        self.types = [term.type for term in atom.terms]

    def setWeight(self, weight):
        self.weight = weight

    def setPriority(self, priority):
        self.priority = priority

    def setMax(self, max):
        self.max = max

    def setMin(self, min):
        self.min = min
    
    def createProgram(self):
        pass
    
    def __str__(self):
        return 'modeh ' + str(self.atom)