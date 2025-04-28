import clingo
from xhail.parser.parser import Parser

class Interface:
    best_model = None
    enumerated_models = []
    model_selector = -1
    program = ""

    def __init__(self, id, program, isExpressive, timelimit, modellimit):
        self.id = id
        self.program = program
        self.expressive = isExpressive
        self.timelimit = timelimit
        self.modellimit = modellimit
        if isExpressive:
            self.loadManyModels(timelimit, modellimit)
        else:
            self.loadBestModel()

    def loadManyModels(self, timeLimit, countLimit):
        results = {}
        ctl = clingo.Control(["0", "--opt-mode=enum"])
        ctl.add("base", [], self.program)
        ctl.ground([("base", [])])
        ctl.configuration.solve.time_limit = timeLimit
        with ctl.solve(yield_=True) as handle:
            for i, model in enumerate(handle):
                if i >= countLimit:
                    break
                
                atoms = model.symbols(shown=True)
                atom_list = [str(atom) for atom in atoms]
                score = model.cost[0] if model.cost else 0
                if score not in results:
                    results[score] = []
                results[score].append(atom_list)

        for score, models in sorted(results.items()):
            for model in models:
                self.enumerated_models.append(model)
        self.model_selector = 0

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
        self.best_model = min_models[0]
        return self.best_model
    
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
    
    def getNextModel(self):
        if self.model_selector == -1 or self.model_selector >= len(self.enumerated_models):
            return []
        else:
            return self.enumerated_models[self.model_selector]
    
    def incrementModel(self):
        self.model_selector += 1
        if self.model_selector >= len(self.enumerated_models):
            return False
        else:
            return True
    
    def getProgram(self):
        return self.program
    
    # ---------- SETTERS ---------- #
    def setProgram(self, program):
        self.program = program