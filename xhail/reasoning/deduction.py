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
                if self.model.isSubsumed(fact, schema):
                    if mode == 'head':
                        priorityTerms = self.getMarkerTerms(fact, schema, '+')
                        allTerms = priorityTerms
                    elif mode == 'body':
                        # check if positive terms fulfilled.
                        positiveTerms = self.getMarkerTerms(fact, schema, '+')
                        # if positive terms in priorty or backup...
                        if positiveTerms.issubset(allTerms):
                            if priorityTerms != None:
                                priorityTerms = priorityTerms.difference(positiveTerms)
                                positiveTerms = positiveTerms.difference(priorityTerms)
                            positiveTerms = positiveTerms.difference(allTerms)
                            priorityTerms = priorityTerms.update(self.getMarkerTerms(fact, schema, '-'))
                        else:
                            continue         
                    else:
                        continue
                    level.append([fact, priorityTerms, allTerms, previous])
        return level
    
    def runPhase(self):
        head_atoms = [mh.atom for mh in self.MH]
        body_atoms = [mb.atom for mb in self.MB if mb.negation == False]
        negated_bodies = [Atom(f'not_{mb.atom.predicate}', mb.atom.terms) for mb in self.MB if mb.negation == True]
        body_atoms += negated_bodies
        conditions = head_atoms + body_atoms
        matches = self.model.getMatches(conditions)
        #for match in matches:
        #    print([t.type for t in match.terms])

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
            
        clauses = []
        currentLevel = len(levels) - 1
        for solution in levels[currentLevel]: # solution is possible end body literal
            i = currentLevel
            body = []
            while solution[3] != None: # while not 
                if solution[0].predicate[:4] == "not_":
                    predicate = solution[0].predicate[4:]
                    negation = True
                else:
                    negation = False
                body.append(Literal(Atom(predicate, solution[0].terms), negation))
                for option in levels[currentLevel - 1]:
                    if option[0] == solution[3]:
                        solution = option
                        i -= 1
                        break

            if solution[3] == None:
                head = solution[0]

            clause = Clause(head, body)
            clauses.append(clause)
        self.model.setKernel(clauses)