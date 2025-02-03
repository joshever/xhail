from xhail.terms import Atom,
import xhail.modes

class Example:
    KEY_WORD = '#example'
    weight = 1
    priority = 1

    def __init__(self, atom: Atom, negation: bool):
        self.atom = atom
        self.negation = negation

    def setWeight(self, weight):
        self.weight = weight

    def setPriority(self, priority):
        self.priority = priority

    def createProgram(self):
        program = ' not ' if not self.negation else ' '
        program = f'#maximize[{program}{self.atom} ={self.weight} @{self.priority} ].'
    


    



class Abductor:
    def __init__(self, E, M):
        self.E = E


    # ---------- STAGE 1 : collect examples ---------- #
    # 