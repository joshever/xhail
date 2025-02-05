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
        negation_string = 'not ' if self.negation else ''
        program.append('#maximize{' + f'{str(self.weight)}@{str(self.priority)} : {negation_string}{self.atom}' + '}.')
        program.append(f':- {self.atom}.' if self.negation else f':- not {self.atom}.')
        return '\n'.join(program)
    
    def __str__(self):
        return ('not ' if self.negation else '') + str(self.atom)

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
        vars_string = ', '.join([str(v) for v in vars])
        newAtom = Atom(self.atom.predicate, vars)

        program = []
        constraint_types = ', '.join([str(Atom(t, vars)) for t in self.types])
        program.append(str(self.lower) + ' { abduced_' + str(newAtom) + ' : '+ constraint_types + ' } ' + str(self.upper) + '.')
        program.append('#minimize{' + f'{str(self.weight)}@{str(self.priority)}, {vars_string}: abduced_{newAtom}, {constraint_types}' + '}.')
        clause_types = ', '.join([str(Atom(t, vars)) for t in self.types])
        program.append(f'{newAtom} :- abduced_{newAtom}, {clause_types}.')
        program.append(f'#show abduced_{newAtom.predicate}/{str(len(newAtom.terms))}.')
        return '\n'.join(program)
    
    def __str__(self):
        return 'modeh ' + str(self.atom)
    

class Abductor:
    def __init__(self, E, M, B):
        self.E = E
        self.M = M
        self.B = B

    def createProgram(self):
        program = ''
        for example in self.E:
            program += example.createProgram() + '\n'
        program += '\n'
        for modeh in self.M:
            program += modeh.createProgram() + '\n'
        
        program = '\n'.join(self.B) + '\n\n' + program
        return program
    
    def callClingo(self, program):
        print(program)
        control = clingo.Control()
        control.add("base", [], program)
        control.ground([("base", [])])
        models = []
        def on_model(model):
            model = model.symbols(shown=True)
            models.append(model)
        control.solve(on_model=on_model)
        return models

