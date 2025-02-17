import copy
from structures import Modeh
from terms import Atom, Constraint, Fact, Literal, Normal, PlaceMarker
import clingo

class Deduction:
    def __init__(self, model):
        self.delta = model.delta
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.model = model

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
    
    def substitute(self, s, a, n): # a starts a copy of s
        nt = set()
        nt.update(n)
        for i in range(len(s.terms)):
            if isinstance(s.terms[i], PlaceMarker) and s.terms[i].marker == '+':
                a.terms += [Normal(nt.pop()[0])]
            elif isinstance(s.terms[i], Atom):
                a.terms += [self.substitute(self, s, a, nt)]
            else:
                a.terms += [s.terms[i]]
                continue
        return a
    
    # ---------- call clingo to generate solutions ----------- #
    def isSat(self, atom):
        tally = [str(ca) == str(atom) for ca in  self.model.getClingoModels()]
        if tally.contains(True):
            return True
        return False
   

    def runPhase(self, program):
        k = {}

        # loop through alpha values (subset of delta)
        for alpha in self.delta:

            # find modeh that is subsumed by alpha
            modeh = None
            for m in self.MH:
                if self.model.isSubsumed(alpha, m):
                    modeh = m
            
            # if no modeh found skip for alpha
            if modeh == None:
                continue

            # get set of positive variables
            n = self.positiveHelper(alpha, modeh.atom)

            # head declaration
            k[alpha] = []

            # iterative expansion
            """
            think about depth
            q(+r, +r, -r)
            p(a) :- q(a, a, b), 
            - becomes + after
            """

            depth = len(self.MB) # TEMPORARY -> this needs updating
            for d in range(depth):
                # iteratively add constraints and see if satisfiable.
                modeb = self.MB[d]

                # step 1 : extract schema from modeb
                schema_literal = Literal(self.substitute(modeb.atom, Atom(modeb.atom.predicate, []), n), modeb.negation)
                #schema = str(Constraint([schema_literal]))
                #types = '\n'.join( [ str(Constraint([Literal(Atom(x[1], [Normal(x[0])]), True)])) for x in n] )


                isSat = self.isSat(schema_literal.atom)

                if isSat:
                    k[alpha] = k[alpha] + [Literal(schema_literal.atom, not schema_literal.negation)]
        for key in k.keys():
            print(f"key : {str(key)}")
            print(f"values : {[str(body) for body in k[key]]}\n")

        #REPLACE WITH FRESH VARIABLES