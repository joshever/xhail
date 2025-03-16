from ..language.terms import Atom, Literal, Normal, PlaceMarker
import itertools


class Deduction:
    def __init__(self, model):
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.DEPTH = model.DEPTH
        self.model = model

    # ---------- get marker terms given specific marker (+/-) ---------- #
    def getMarkerTerms(self, atom, mode, marker):
        n = set()
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
                n.update(self.getMarkerTerms(term1, term2, marker))
            elif isinstance(term2, PlaceMarker) and term2.marker == marker:
                n.add(term1.value)
            else:
                continue
        return n
    
    # ---------- place terms for n into the atom, given a +placemarker, otherwise keep other terms ---------- #
    def substitute(self, schema, atom, n): # a starts a copy of s
        for i in range(len(schema.terms)):
            if isinstance(schema.terms[i], PlaceMarker) and schema.terms[i].marker == '+':
                atom.terms += [Normal(n.pop())]
            elif isinstance(schema.terms[i], Atom):
                a_term, n = self.substitute(self, schema, atom, n)
                atom.terms += [a_term]
            else:
                atom.terms += [schema.terms[i]]
                continue
        return atom, n
    
    # ---------- call clingo to generate solutions ----------- #
    def isSat(self, literal):
        atom = literal.atom
        tally = [str(ca) == str(atom) for ca in self.model.getClingoModels()[0]]
        if literal.negation == False and True in tally:
            return True
        if literal.negation == True and not True in tally:
            return True
        return False
    
    # ---------- recursively find valid body literals for deduction ---------- # 
    def tryCombination(self, remaining_modebs, remaining_terms):
        modeb = remaining_modebs.pop()
        atom, terms = self.substitute(modeb.atom, Atom(modeb.atom.predicate, []), remaining_terms)
        negation = modeb.negation

        solutions = [[]]
        matches = self.model.getMatches(atom)
        for match in matches:
            if negation == False:
                terms = terms.update(self.getMarkerTerms(match, modeb.atom, '-'))
                answers = self.tryCombination(remaining_modebs, terms)
                for answer in answers:
                    if None not in answer:
                        solutions.append([match].append(answer))
            else:
                return [[None]]
            
        return solutions


    def runPhase(self):

        heads = [mh.atom for mh in self.MH]
        print([str(m) for m in heads])

        bodies = [mb.atom for mb in self.MB if mb.negation == False]
        negated_bodies = [Atom(f'not_{mb.atom.predicate}', mb.atom.terms) for mb in self.MB if mb.negation == True]
        bodies += negated_bodies
        print([str(m) for m in bodies])

        conditions = heads + bodies
        matches = self.model.getMatches(conditions)

        print([str(m) for m in matches])

        # negated bodies.
        
        # match types.
        # for each matched type, modeb has not matches.


        """
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
            N = self.getMarkerTerms(alpha, modeh.atom, '+')
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
                remaining_modebs = 
                self.tryCombination()
            k[alpha] = body
                    
        #for key in k.keys():
        #    print(f"key : {str(key)}")
        #    print(f"values : {[str(body) for body in k[key]]}\n")

        self.model.setKernel(k)"
        """