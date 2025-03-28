from xhail.language.structures import Modeb, Modeh
from ..language.terms import Atom, Clause, Literal, Normal, PlaceMarker

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
    
    def extractTerms(self, schemas, facts, priorityTerms, allTerms, previous, mode):
        level = []
        for schema in schemas:
            for fact in facts:
                factPriorityTerms = priorityTerms.copy()
                factAllTerms = allTerms.copy()
                if str(fact) != str(previous) and self.model.isSubsumed(fact, schema):
                    if mode == 'head':
                        factPriorityTerms = self.getMarkerTerms(fact, schema, '+')
                        factAllTerms = factPriorityTerms
                    elif mode == 'body':
                        # check if positive terms fulfilled.
                        factPositiveTerms = self.getMarkerTerms(fact, schema, '+')
                        # if positive terms in priorty or backup...
                        if factPositiveTerms.issubset(factAllTerms):
                            factPriorityTerms.difference(factPositiveTerms)
                            factPositiveTerms.difference(factPriorityTerms)
                            factPositiveTerms.difference(factAllTerms)
                            factPriorityTerms.update(self.getMarkerTerms(fact, schema, '-'))
                            factAllTerms.update(factPriorityTerms)
                        else:
                            continue         
                    else:
                        continue
                    level.append([fact, factPriorityTerms, factAllTerms, previous])
        return level

    def findNext(self, atomToFind, levels, idl):
        if atomToFind == None:
            return []
        else:
            for idc, choice in enumerate(levels[idl]):
                if str(choice[0]) == str(atomToFind):
                    chain = self.findNext(choice[3], levels, idl-1)
                    chain.append(choice[0])
                    return chain
        return ["Mistake!"]





    
    def runPhase(self):
        head_atoms = [mh.atom for mh in self.MH]
        body_atoms = [mb.atom for mb in self.MB if mb.negation == False]
        negated_bodies = [Atom(f'not_{mb.atom.predicate}', mb.atom.terms) for mb in self.MB if mb.negation == True]
        body_atoms += negated_bodies
        conditions = head_atoms + body_atoms
        matches = self.model.getMatches(conditions)
        d = 1
        levels = []
        priorityTerms, allTerms = set([]), set([])
        levels.append(self.extractTerms(head_atoms, matches, priorityTerms, allTerms, None, 'head'))
        while d <= self.DEPTH:
            currentLevel = []
            for prevMatch in levels[d-1]:
                if prevMatch[1] == None:
                    continue
                else:
                    results = self.extractTerms(body_atoms, matches, prevMatch[1], prevMatch[2], prevMatch[0], 'body')
                    if results == None:
                        continue
                    for result in results:
                        currentLevel.append(result)
            if currentLevel == []:
                d = self.DEPTH + 1
                continue
            levels.append(currentLevel)

            d += 1


        results = []
        top = len(levels) - 1
            

        clauses = []
        for choice in levels[top]:
            chain = self.findNext(choice[3], levels, top-1)
            chain.append(choice[0])
            clauses.append(Clause(chain[0], [Literal(Atom(atom.predicate[4:], atom.terms), True) if atom.predicate[:4] == "not_" else Literal(atom, False) for atom in chain[1:]]))
        
        self.model.setKernel(clauses)