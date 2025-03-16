import clingo
from ..parser.parser import Parser
from ..language.structures import Modeb, Modeh
from ..language.terms import Atom, Normal, PlaceMarker

class Model:
    program = ""
    clingo_models = []
    delta = []
    kernel = {}

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
    
    def writeProgram(self):
        file = open("xhail/output/abduce.lp", "w")
        file.write(self.program)
        file.close()
    
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
        self.program += abduciblesProgram + '\n'
        return abduciblesProgram
    
    def loadNegations(self, modebs):
        negationProgram = '%NEGATIONS%\n'
        for modeb in modebs:
            if modeb.negation == True:
                negationProgram += modeb.createProgram() + '\n'
            else:
                continue
        self.program += negationProgram
        return negationProgram + '\n'
        
    def loadBackground(self, background):
        backgroundProgram = '%BACKGROUND%\n' + '\n'.join([str(b) for b in background]) + '\n'
        self.program += backgroundProgram + '\n'
        return backgroundProgram + '\n'

    def clearProgram(self):
        self.program = ""
    
    # ensures normal values are the same, and any placeholders can be different.
    def isSubsumed(self, a, m): 
        if a.predicate != m.predicate:
            return False
        for term1, term2 in zip(a.terms, m.terms):
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
        return True

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
        strModel = ""
        for m in model:
            strModel += str(m) + '.\n'

        simpleParser = Parser()
        simpleParser.loadString(strModel)
        facts = simpleParser.parseProgram()

        result = []
        for fact in facts:
            for mh in atomConditions:
                if self.isSubsumed(fact.head, mh):
                    result.append(fact.head)
        return result


    # ---------- SETTERS ---------- #
    
    def setKernel(self, kernel):
        self.kernel = kernel

    def setProgram(self, program):
        self.program = program
    
    
    