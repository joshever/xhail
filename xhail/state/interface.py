import clingo
from xhail.parser.parser import Parser

class Interface:
    best_model = None
    program = ""
    models = []

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
        min_score = min(s for _, s in clingo_models)
        min_models = [m for m, s in clingo_models if s == min_score]
        self.best_model = 0
        self.models = min_models
        return self.models[0]
    
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
        return self.models[self.best_model] if self.best_model != None else None
    
    def getNextModel(self):
        if self.best_model + 1 < len(self.models):
            self.best_model += 1
            return self.models[self.best_model]
        else:
            return None
    
    def getProgram(self):
        return self.program
    
    # ---------- SETTERS ---------- #
    def setProgram(self, program):
        self.program = program