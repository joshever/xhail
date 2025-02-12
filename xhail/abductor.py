from parser import parseProgram
from terms import Atom, Fact, PlaceMarker, Normal
from structures import Example, Modeh
import clingo

# ----- ABDUCTION PHASE (1) ------- #
# ---------- abductor ----------- #
class Abduction:
    # model to be updated
    models = []
    program = ""

    # ---------- examples, modehs, background required ----------- #
    def __init__(self, E, M, B):
        self.E = E
        self.M = M
        self.B = B

    # ---------- recreate program given parsed params ----------- #
    def createProgram(self):
        backgroundProgram = self.collateBackground()
        examplesProgram = self.collateExamples()
        abduciblesProgram = self.collateAbducibles()

        program = '\n' + backgroundProgram + '\n' + examplesProgram + '\n' + abduciblesProgram
        file = open("abduce.lp", "w")
        file.write(program)
        file.close()
        self.program = program
        return program
    
    def collateExamples(self):
        examplesProgram = '%EXAMPLES%\n'
        for example in self.E:
            examplesProgram += example.createProgram() + '\n'
        return examplesProgram

    def collateAbducibles(self):
        abduciblesProgram = '%ABDUCIBLES%\n'
        for modeh in self.M:
            abduciblesProgram += modeh.createProgram() + '\n'
        return abduciblesProgram
    
    def collateBackground(self):
        backgroundProgram = '%BACKGROUND%\n' + '\n'.join([str(b) for b in self.B]) + '\n'
        return backgroundProgram
    
    # ---------- call clingo to generate solutions ----------- #
    def callClingo(self):
        control = clingo.Control()
        control.add("base", [], self.program)
        control.ground([("base", [])])
        models = []
        def on_model(model):
            model = model.symbols(shown=True)
            models.append(model)
        control.solve(on_model=on_model)
        self.models = models
        return models
    
    def getDelta(self):
        # ---------- find abduced_ predicates ---------- #
        model = self.models[0]
        strModel = ""
        for m in model:
            strModel += str(m) + '.\n'
        abduced_facts = parseProgram(strModel)
        
        # ---------- add delta atoms, then remove abduced_ ---------- #
        delta = []
        for fact in abduced_facts:
            delta.append(Atom(fact.head.predicate.replace('abduced_', ''), fact.head.terms))
        return delta
