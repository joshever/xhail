

from structures import Modeh
from terms import Atom, Constraint, Fact, Literal, Normal, PlaceMarker

class Deduction:
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
        t = set()
        for term1, term2 in zip(a.terms, m.terms):
            if isinstance(term2, Atom):
                t.update(self.positiveHelper(term1, term2))
            elif isinstance(term2, PlaceMarker) and term2.marker == '+':
                t.add((term1.value, term2.type))
            else:
                continue
        return t
    
    def substitute(self, a, n): # a starts a copy of s
        nt = set()
        nt.update(n)
        for i in range(len(a.terms)):
            if isinstance(a.terms[i], PlaceMarker) and a.terms[i].marker == '+':
                a.terms[i] = Normal(nt.pop()[0])
            elif isinstance(a.terms[i], Atom):
                a.terms[i] = self.substitute(self, a.terms[i], nt)
            else:
                continue 
        return a

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
                modeb = self.MB[d]

                # step 1 : extract schema from modeb
                print("n", n)
                schema = str(Constraint([Literal(self.substitute(Atom(modeb.atom.predicate, modeb.atom.terms), n), not modeb.negation)]))
                print("n", n)
                types = '\n'.join( [ str(Constraint([Literal(Atom(x[1], [Normal(x[0])]), True)])) for x in n] )
                exampleProgram = '\n'.join([e.createProgram() for e in self.EX])
                backgroundProgram = '\n'.join([str(b) for b in self.BG])
                deltaProgram = '\n'.join([str(d) for d in self.delta])
                query = types + '\n' + schema + '\n' + deltaProgram + '\n' + backgroundProgram  +'\n' + exampleProgram

                # step 2 : add to clingo model, see if terms are allowed.
                print("\n\n\nQUERY --------------------", query)

                # step 3 : if terms allowed, add to body of kernel set.





        