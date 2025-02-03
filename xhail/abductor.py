from terms import Atom, Term, PlaceMarker, Normal

class Example:
    KEY_WORD = '#example'
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
        negation_string = ' ' if self.negation else ' not '
        program.append(f'#maximize[{negation_string}{self.atom} ={self.weight} @{self.priority} ].')
        program.append(f':- {self.atom}' if self.negation else f':- not {self.atom}.')
        return '\n'.join(program)

class Modeh:
    KEY_WORD = '#modeh'
    weight = 1
    priority = 1
    lower = 0
    upper = 1000000

    def __init__(self, atom: Atom, n: str): #these will be placeholder atoms
        self.atom = atom
        self.n = n
        self.types = [term.type for term in atom.terms]

    def setWeight(self, weight):
        self.weight = weight

    def setPriority(self, priority):
        self.priority = priority

    def setUpper(self, upper):
        self.upper = upper

    def setLower(self, lower):
        self.lower = lower
    
    def createProgram(self, eAtom):
        program = []
        constraint_types = ' : '.join(self.types)
        program.append(str(self.lower) + ' { abduced_' + str(eAtom) + ' : '+ constraint_types + ' } ' + str(self.upper) + '.')
        program.append(f'#minimize[ abduced_{eAtom} ={str(self.weight)} @{str(self.priority)} : {constraint_types} ].')
        clause_types = ','.join(self.types)
        program.append(f'{eAtom} :- abduced_{eAtom}, {clause_types}.')
        return '\n'.join(program)
    

class Abductor:
    def __init__(self, E, M):
        self.E = E
        self.M = M

    def createProgram(self):
        program = ''
        preds = {}
        for example in self.E:
            program += example.createProgram() + '\n'
            for modeh in self.M:
                if modeh.atom.predicate == example.atom.predicate:
                    preds[modeh.atom.predicate] = example.atom
        
        for modeh in self.M:
            program += modeh.createProgram(preds[modeh.atom.predicate]) + '\n'

        return program

examples = [Example(Atom('flies', [Normal('a')])),
            Example(Atom('flies', [Normal('b')])),
            Example(Atom('flies', [Normal('c')])),
            Example(Atom('flies', [Normal('d')]), True)]

modes = [Modeh(Atom('flies', [PlaceMarker('+', 'bird')]), '*')]

background = """
#hide.
#show abduced_flies/1.
#show bird/1.
#show flies/1.
#show penguin/1.

bird(X):-penguin(X).
bird(a;b;c).
penguin(d).

"""

abductor = Abductor(examples, modes)

program = abductor.createProgram()

print(background + program)


    