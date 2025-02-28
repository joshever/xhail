import copy
from structures import Modeh
from terms import Atom, Constraint, Fact, Literal, Normal, PlaceMarker
import clingo
import itertools

class Deduction:
    def __init__(self, model):
        self.delta = model.delta
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.DEPTH = model.DEPTH
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
    
    def markerHelper(self, a, m, marker):
        t = set()
        for term1, term2 in zip(a.terms, m.terms):
            if isinstance(term2, Atom):
                t.update(self.markerHelper(term1, term2, marker))
            elif isinstance(term2, PlaceMarker) and term2.marker == marker:
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
   

    def runPhase(self):

        # empty kernel set
        k = {}

        # loop through alpha values (subset of delta)
        for alpha in self.delta:

            # find modeh that is subsumed by alpha and skip if none found
            modeh = None
            for m in self.MH:
                if self.model.isSubsumed(alpha, m):
                    modeh = m
            if modeh == None:
                continue

            # get set of variables we can use for body (+ markers) and set head declaration
            n = self.markerHelper(alpha, modeh.atom, '+')
            k[alpha] = []


            combinations = list(itertools.combinations_with_replacement(self.MB, self.DEPTH))
            for comb in combinations:
                

                

               

                



                # O(n^2) time
                for i in range(len(self.MB)):
                    for j in range(len(self.MB)):
                        self.addBody(n, )
                
                # iteratively add constraints and see if satisfiable.
                modeb = self.MB[d]

                # step 1 : extract schema from modeb
                schema_literal = Literal(self.substitute(modeb.atom, Atom(modeb.atom.predicate, []), n), modeb.negation)

                #schema = str(Constraint([schema_literal]))
                #types = '\n'.join( [ str(Constraint([Literal(Atom(x[1], [Normal(x[0])]), True)])) for x in n] )

                # think about + and -. - of body added to n once added
                isSat = self.isSat(schema_literal.atom)

                if isSat:
                    k[alpha] = k[alpha] + [Literal(schema_literal.atom, not schema_literal.negation)]
                    new_positives = self.markerHelper(alpha, modeh.atom, '-')
                    


        for key in k.keys():
            print(f"key : {str(key)}")
            print(f"values : {[str(body) for body in k[key]]}\n")

        #REPLACE WITH FRESH VARIABLES