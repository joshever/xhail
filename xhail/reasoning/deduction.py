from ..language.terms import Atom, Literal, Normal, PlaceMarker
import itertools

class Deduction:
    def __init__(self, model):
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.DEPTH = model.DEPTH
        self.model = model

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
    def isSat(self, literal):
        atom = literal.atom
        tally = [str(ca) == str(atom) for ca in self.model.getClingoModels()[0]]
        if literal.negation == False and True in tally:
            return True
        if literal.negation == True and not True in tally:
            return True
        return False

    def runPhase(self):

        # empty kernel set
        k = {}

        # loop through alpha values (subset of delta)
        for alpha in self.model.getDelta():

            # find modeh that is subsumed by alpha and skip if none found
            modeh = None
            for m in self.MH:
                if self.model.isSubsumed(alpha, m):
                    modeh = m
            if modeh == None:
                continue

            # get set of variables we can use for body (+ markers) and set head declaration
            N = self.markerHelper(alpha, modeh.atom, '+')
            k[alpha] = []

            # loop through body options
            combinations = list(itertools.combinations_with_replacement(self.MB, self.DEPTH))
            valid = False
            while valid == False and combinations != []:
                n = N
                body = []
                combination = combinations.pop()
                for i in range(self.DEPTH):
                    modeb = combination[i]
                    literal = Literal(self.substitute(modeb.atom, Atom(modeb.atom.predicate, []), n), modeb.negation)
                    if self.isSat(literal):
                        body.append(literal)
                        valid = True
                    else:
                        valid = False
                    n.update(self.markerHelper(literal.atom, modeb.atom, '-'))
            k[alpha] = body
                    
        #for key in k.keys():
        #    print(f"key : {str(key)}")
        #    print(f"values : {[str(body) for body in k[key]]}\n")

        self.model.setKernel(k)