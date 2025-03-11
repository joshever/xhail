from ..language.terms import Atom, Literal, Normal, PlaceMarker
import itertools

class Deduction:
    def __init__(self, model):
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.DEPTH = model.DEPTH
        self.model = model

    # think this logic through. can I have marker but atom for the other thing!!! ugh!!!
    def markerHelper(self, a, m, marker):
        n = set()
        for term1, term2 in zip(a.terms, m.terms):
            if isinstance(term2, Atom):
                n.update(self.markerHelper(term1, term2, marker))
            elif isinstance(term2, PlaceMarker) and term2.marker == marker:
                n.add(term1.value)
            else:
                continue
        return n
    
    def substitute(self, s, a, n): # a starts a copy of s
        for i in range(len(s.terms)):
            if isinstance(s.terms[i], PlaceMarker) and s.terms[i].marker == '+':
                a.terms += [Normal(n.pop())]
            elif isinstance(s.terms[i], Atom):
                a_term, n = self.substitute(self, s, a, n)
                a.terms += [a_term]
            else:
                a.terms += [s.terms[i]]
                continue
        return a, n
    
    # ---------- call clingo to generate solutions ----------- #
    def isSat(self, literal):
        atom = literal.atom
        tally = [str(ca) == str(atom) for ca in self.model.getClingoModels()[0]]
        if literal.negation == False and True in tally:
            return True
        if literal.negation == True and not True in tally:
            return True
        return False
    
    # recursive function.
    def tryCombination(self, modebs, terms):
        modeb = modebs.pop()

        #substitute terms into modeb
        #update terms
        atom, terms = self.substitute(modeb.atom, Atom(modeb.atom.predicate, []), terms)
        negation = modeb.negation

        terms = terms.update(self.markerHelper(atom, modeb.atom, '-'))

        #find ALL predicates in solution that match the modeb.atom predicate
        matches = self.model.getMatches(atom) # assume first model for now

        #TODO: for each valid fact: call tryCombination(modebs, terms)
        for match in matches:
            solutions = self.tryCombination(modebs, terms, [[Literal(atom, negation)]])

        #TODO: add list of solutions returned to list other returned list of solutions.
        
        #TODO: if modebs = [] return [[]]
        #TODO: else return [[body1, body2], [body1, body2]]

        if len(modebs) == 1:
            # carry out calulation
            return
        else:
            modeb = modebs.pop()
            self.tryCombination()
        

    def runPhase(self):

        # empty kernel set
        k = {}

        # loop through alpha values (subset of delta)
        for alpha in self.model.getDelta():
            print("new alpha \n")
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
            #for combination in combinations:
            #    print([(str(c.atom), str(c.negation)) for c in combination])
            valid = False
            while valid == False and combinations != []:
                n = N
                body = []
                combination = combinations.pop()
                for i in range(self.DEPTH):
                    # input: combination, 
                    #find the solutions with the same predicate as the combination component.
                    #check if the modeb is subsumed to the example.
                    #check if all versions of this fit?
                    #can I do this recursively?
                    modeb = combination[i]
                    atom, n = self.substitute(modeb.atom, Atom(modeb.atom.predicate, []), n)
                    literal = Literal(atom, modeb.negation)
                    if self.isSat(literal):
                        body.append(literal)
                        valid = True
                    else:
                        valid = False
                    n.update(self.markerHelper(literal.atom, modeb.atom, '-'))
            print([str(b) for b in body])
            k[alpha] = body
                    
        #for key in k.keys():
        #    print(f"key : {str(key)}")
        #    print(f"values : {[str(body) for body in k[key]]}\n")

        self.model.setKernel(k)