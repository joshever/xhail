from terms import Atom, PlaceMarker, Normal
import clingo

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
        negation_string = '' if self.negation else 'not '
        #program.append(f'#maximize [{negation_string}{self.atom} = {self.weight} @{self.priority}].')
        program.append(f'#maximize [{negation_string}{self.atom}].')
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
    
    def createProgram(self):
        alphabet = [Normal(chr(i)) for i in range(ord('A'), ord('Z'))]
        vars = alphabet[:len(self.atom.terms)]
        newAtom = Atom(self.atom.predicate, vars)

        program = []
        constraint_types = ' : '.join([str(Atom(t, vars)) for t in self.types])
        program.append(str(self.lower) + ' { abduced_' + str(newAtom) + ' : '+ constraint_types + ' } ' + str(self.upper) + '.')
        #program.append(f'#minimize [abduced_{newAtom} = {str(self.weight)} @{str(self.priority)} : {constraint_types}].')
        program.append(f'#minimize [abduced_{newAtom} : {constraint_types}].')
        clause_types = ', '.join([str(Atom(t, vars)) for t in self.types])
        program.append(f'{newAtom} :- abduced_{newAtom}, {clause_types}.')
        return '\n'.join(program)
    

class Abductor:
    def __init__(self, E, M):
        self.E = E
        self.M = M

    def createProgram(self):
        program = ''
        for example in self.E:
            program += example.createProgram() + '\n'
        
        for modeh in self.M:
            program += modeh.createProgram() + '\n'

        return program
    
    def callClingo(self, program):
        control = clingo.Control()
        control.add("base", [], program)
        control.ground([("base", [])])
        models = []
        def on_model(model):
            models.append(model)
            print("Answer Set:", model)
        control.solve(on_model=on_model)
        return models

examples = [Example(Atom('flies', [Normal('a')])),
            Example(Atom('flies', [Normal('b')])),
            Example(Atom('flies', [Normal('c')])),
            Example(Atom('flies', [Normal('d')]), True)]

modes = [Modeh(Atom('flies', [PlaceMarker('+', 'bird')]), '*')]

background = """
bird(X):-penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).
"""
program = background
abductor = Abductor(examples, modes)
program += abductor.createProgram()
print(program)
program += '\n#show flies_prime/1.'
solution = abductor.callClingo(program)
print(solution)