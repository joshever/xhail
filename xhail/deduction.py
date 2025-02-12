

from structures import Modeh
from terms import Atom


class deduction:
    def __init__(self, delta, EX, MH, MB, BG):
        self.delta = delta
        self.EX = EX
        self.MH = MH
        self.MB = MB
        self.BG = BG

    def isSubsumed(atom: Atom, modeh: Modeh):
        if atom.predicate == modeh.atom.predicate:
            return True
        return False
    
    def getPositiveMarker(modeh: Modeh):
        n = []
        atom = Modeh.atom
        for t in atom.terms:
            if isinstance(type(t), Atom):
                
        pass

    def deduce(self):
        kernel = {}
        # find clause head
        for alpha in self.delta:
            head = None
            for mh in self.MH:
                if self.isSubsumed(alpha, mh):
                    head = mh
            if head == None:
                continue
            kernel[alpha] = []

            # find clause body
            for mb in self.MB:


        return