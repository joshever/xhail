

from logging import PlaceHolder
from structures import Modeh
from terms import Atom, Fact


class deduction:
    def __init__(self, delta, EX, MH, MB, BG):
        self.delta = delta
        self.EX = EX
        self.MH = MH
        self.MB = MB
        self.BG = BG

    def isSubsumed(self, atom: Atom, modeh: Modeh):
        if atom.predicate == modeh.atom.predicate:
            return True
        return False

    def positiveHelper(self, a, m):
        t = set([])
        for term1, term2 in zip(a.terms, m.terms):
            # check type?
            # : type == atom
            if isinstance(term2, Atom):
                t += self.positiveHelper(term1, term2)
            elif isinstance(term2, PlaceHolder) and term2.marker == '+':
                t.add(term1.value)
            else:
                continue
        return t

    def deduce(self):
        A = []
        T = self.BG + [Fact(d) for d in self.delta]
        k = {}

        # loop through alpha values (subset of delta)
        for alpha in self.delta:

            # find modeh that is subsumed by alpha
            modeh = None
            for m in self.MH:
                if self.isSubsumed(alpha, m):
                    modeh = m
            
            # if no modeh found skip for alpha
            if modeh == None:
                continue

            # get set of positive variables
            n = self.positiveHelper(alpha, modeh.atom)

            # head declaration
            k[alpha] = []

            # iterative expansion
            depth = len(self.MB) # TEMPORARY -> this needs updating
            for d in range(depth):
                # iteratively add constraints and see if satisfiable.
                





        