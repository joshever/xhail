from terms import Atom, PlaceMarker, Normal
from structures import Example, Modeh
import clingo

# ----- ABDUCTION PHASE (1) ------- #
# ---------- abductor ----------- #
class Abductor:

    # ---------- examples, modehs, background required ----------- #
    def __init__(self, E, M, B):
        self.E = E
        self.M = M
        self.B = B

    # ---------- recreate program given parsed params ----------- #
    def createProgram(self):
        
        examplesProgram = '%EXAMPLES%\n'
        for example in self.E:
            examplesProgram += example.createProgram() + '\n'

        abduciblesProgram = '%ABDUCIBLES%\n'
        for modeh in self.M:
            abduciblesProgram += modeh.createProgram() + '\n'

        backgroundProgram = '%BACKGROUND%\n' + '\n'.join([str(b) for b in self.B]) + '\n'
    
        program = '\n' + backgroundProgram + '\n' + examplesProgram + '\n' + abduciblesProgram
        file = open("abduce.lp", "w")
        file.write(program)
        file.close()
        return program
    
    # ---------- call clingo to generate solutions ----------- #
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

