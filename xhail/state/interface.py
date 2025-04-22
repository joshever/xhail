import clingo
from xhail.parser.parser import Parser
from xhail.language.terms import isSubsumed

class Interface:
    best_model = None
    program = ""

    def __init__(self, id, program, timeout):
        self.id = id
        self.program = program
        self.timeout = timeout
        self.loadBestModel()

    # ---------- METHODS ---------- #
    def loadBestModel(self):
        control = clingo.Control()
        control.add("base", [], self.program)
        control.ground([("base", [])])
        clingo_models = []
        
        def on_model(clingo_model):
            model_symbols = clingo_model.symbols(shown=True)
            model_cost = clingo_model.cost
            clingo_models.append([model_symbols, model_cost])
        
        control.solve(on_model=on_model)
        if clingo_models == []:
            return '[]'
        best_model = min(clingo_models, key=lambda m: [int(c) for c in m[1]])
        self.best_model = best_model[0]
        return best_model[0]
    
    def parseModel(self, model):
        strModel = ""
        if model == None:
            return []
        for m in model:
            strModel += str(m) + '.\n'
        simpleParser = Parser()
        simpleParser.loadString(strModel)
        facts = simpleParser.parseProgram()
        return facts
    
    def writeProgram(self, destination):
        file = open(destination, "w")
        file.write(self.program)
        file.close()
    
    # ---------- GETTERS ---------- #
    def getBestModel(self):
        return self.best_model
    
    def getProgram(self):
        return self.program
    
    # ---------- SETTERS ---------- #
    def setProgram(self, program):
        self.program = program