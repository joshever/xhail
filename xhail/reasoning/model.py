import clingo
from ..parser.parser import Parser
from ..language.terms import Atom, Normal, PlaceMarker

class Model:
    program = ""
    clingo_models = []
    best_model = None
    delta = []
    kernel = [] # clauses

    def __init__(self, EX, MH, MB, BG, DEPTH):
        self.EX = EX
        self.MH = MH
        self.MB = MB
        self.BG = BG
        self.DEPTH = DEPTH

    # ---------- METHODS ---------- #
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
    
    def getBestModel(self):
        control = clingo.Control()#["--opt-mode=opt"])
        #control.configuration.solve.models = 0
        control.add("base", [], self.program)
        control.ground([("base", [])])
        clingo_models = []
        
        def on_model(clingo_model):
            model_symbols = clingo_model.symbols(shown=True)
            model_cost = clingo_model.cost
            print(model_symbols, model_cost)
            clingo_models.append([model_symbols, model_cost])
        
        control.solve(on_model=on_model)
        #result = handle.get()  # Wait for the solving process to finish
        #if not clingo_models:
        #    return None
        if clingo_models == []:
            return '[]'
        # Select the best model based on lexicographical order of the cost vector
        best_model = min(clingo_models, key=lambda m: [int(c) for c in m[1]])
        self.best_model = best_model
        return best_model[0]

    
    def writeProgram(self, destination):
        file = open(destination, "w")
        file.write(self.program)
        file.close()

    def clearProgram(self):
        self.program = ""

    # ensures normal values are the same, and any placeholders can be different.
    def isSubsumed(self, atom, mode): # 
        if atom.predicate != mode.predicate:
            return False
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
               if not self.isSubsumed(term1, term2):
                   return False
            elif isinstance(term2, Normal):
                if term1.value != term2.value:
                    return False
            elif isinstance(term2, PlaceMarker) and isinstance(term1, Normal):
                if self.getMatches([Atom(term2.type, [term1])]) == []:
                    return False
                else:
                    continue
            else:
                continue
        return True
    
    def parseModel(self, model):
        strModel = ""
        for m in model:
            strModel += str(m) + '.\n'

        simpleParser = Parser()
        simpleParser.loadString(strModel)
        facts = simpleParser.parseProgram()

        return facts

    # ---------- GETTERS ---------- #

    def getProgram(self):
        return self.program
    
    def getClingoModels(self):
        return self.clingo_models
    
    def getDelta(self):
        self.delta = self.getAtoms(self.MH)
        return self.delta
    
    def getMatches(self, atomConditions):
        model = self.getClingoModels()[0]
        facts = self.parseModel(model)

        result = []
        for fact in facts:
            for mh in atomConditions:
                if self.isSubsumed(fact.head, mh):
                    result.append(fact.head)
        return result

    def getKernel(self):
        return self.kernel

    # ---------- SETTERS ---------- #
    
    def setKernel(self, kernel):
        self.kernel = kernel

    def setProgram(self, program):
        self.program = program
    
    def getExamples(self):
        return self.EX
    
    def getBackground(self):
        return self.BG
    
    