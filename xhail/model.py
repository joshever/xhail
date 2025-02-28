import clingo
from parser import Parser
from structures import Modeh
from terms import Atom

class Model:
    program = ""
    clingo_models = []
    delta = []

    def __init__(self, EX, MH, MB, BG, DEPTH):
        self.EX = EX
        self.MH = MH
        self.MB = MB
        self.BG = BG
        self.DEPTH = DEPTH

    def call(self):
        control = clingo.Control()
        control.add("base", [], self.program)
        control.ground([("base", [])])
        clingo_models = []
        def on_model(clingo_model):
            clingo_model = clingo_model.symbols(shown=True)
            clingo_models.append(clingo_model)
        control.solve(on_model=on_model)
        self.clingo_models = clingo_models
        return clingo_models
    
    def loadExamples(self, examples):
        examplesProgram = '%EXAMPLES%\n'
        for example in examples:
            examplesProgram += example.createProgram() + '\n'
        self.program += examplesProgram + '\n'
        return examplesProgram
    
    def loadAbducibles(self, modehs):
        abduciblesProgram = '%ABDUCIBLES%\n'
        for modeh in modehs:
            abduciblesProgram += modeh.createProgram() + '\n'
        self.program += abduciblesProgram
        return abduciblesProgram + '\n'
    
    def loadBackground(self, background):
        backgroundProgram = '%BACKGROUND%\n' + '\n'.join([str(b) for b in background]) + '\n'
        self.program += backgroundProgram
        return backgroundProgram + '\n'
    
    def writeProgram(self):
        file = open("abduce.lp", "w")
        file.write(self.program)
        file.close()

    def clearProgram(self):
        self.program = ""

    def getProgram(self):
        return self.program
    
    def getClingoModels(self):
        return self.clingo_models[0]
    
    def isSubsumed(self, atom: Atom, modeh: Modeh):
        if atom.predicate == modeh.atom.predicate:
            return True
        return False
    
    # ---------- find abduced predicates ---------- #
    def getDelta(self):
        model = self.getClingoModels()
        strModel = ""
        for m in model:
            strModel += str(m) + '.\n'

        simpleParser = Parser()
        simpleParser.loadString(strModel)
        facts = simpleParser.parseProgram()

        for fact in facts:
            for mh in self.MH:
                if self.isSubsumed(fact.head, mh):
                    self.delta.append(fact.head)
        return self.delta