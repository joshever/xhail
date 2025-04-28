from xhail.language.terms import Atom, Normal, PlaceMarker
from xhail.state.interface import Interface

class Context:
    delta = []
    kernel = []
    hypothesis = []
    interfaces = []
    abd_id = 0
    ind_id = 1
    state = 'solving'

    v = False
    e = False
    t = 10
    c = 10

    def __init__(self, EX, MH, MB, BG, DEPTH):
        self.EX = EX
        self.MH = MH
        self.MB = MB
        self.BG = BG
        self.DEPTH = DEPTH

    # ---------- METHODS ---------- #
    def loadDelta(self, id):
        self.delta = self.loadMatches(id, [mh.atom for mh in self.MH])
        return self.delta
    
    def addInterface(self, program, e, c, t):
        id = len(self.interfaces)
        self.interfaces.append(Interface(id, program, e, c, t))
        return id
    
    def writeInterfaceProgram(self, id, destination):
        self.interfaces[id].writeProgram(destination)

    def loadMatches(self, id, atomConditions):
        if not self.e:
            model = self.interfaces[id].getBestModel()
        else:
            model = self.interfaces[id].getNextModel()
        facts = self.interfaces[id].parseModel(model)
        result = []
        for fact in facts:
            for mh in atomConditions:
                res, _ = self.isSubsumed(id, fact.head, mh)
                if res:
                    result.append(fact.head)
        return result
    
    def incrementModel(self):
        return self.interfaces[self.abd_id].incrementModel()

    # ---------- GETTERS ---------- #
    def getDelta(self):
        return self.delta
    
    def getInterfaceResult(self, id):
        return self.interfaces[id].getBestModel()

    def getKernel(self):
        return self.kernel
    
    def getHypothesis(self):
        return self.hypothesis
    
    def getState(self):
        return self.state

    # ---------- SETTERS ---------- #
    def setKernel(self, kernel):
        self.kernel = kernel
    
    def setHypothesis(self, hypothesis):
        self.hypothesis = hypothesis

    def setState(self, state):
        self.state = state

    def setVerbose(self, val):
        self.verbose = val

    def setExpressivity(self, e, t, c):
        self.e = e
        self.t = t
        self.c = c
    
    # ---------- SUBSUMPTION METHOD ---------- #
    def isSubsumed(self, id, atom, mode):
        if atom.predicate != mode.predicate:
            return (False, None)
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
               res, term1 = self.isSubsumed(id, term1, term2)
               if not res:
                   return (False, None)
            elif isinstance(term2, Normal):
                if term1.value != term2.value:
                    return (False, None)
                else:
                    if term2.type == 'constant':
                        term1.type = 'constant'
                        continue
            elif isinstance(term2, PlaceMarker) and isinstance(term1, Atom):
                if self.loadMatches(id, [Atom(term2.type, [term1])]) == []:
                    return (False, None)
                elif term2.marker == '$':
                      term1.type = 'constant'
                      continue
                else:
                    continue
            elif isinstance(term2, PlaceMarker) and isinstance(term1, Normal):
                if self.loadMatches(id, [Atom(term2.type, [term1])]) == []:
                    return (False, None)
                elif term2.marker == '$':
                      term1.type = 'constant'
                      continue
                else:
                    continue
            else:
                continue
        return (True, atom)