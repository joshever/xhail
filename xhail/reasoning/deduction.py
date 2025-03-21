from xhail.language.structures import Modeb, Modeh
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
        print([str(c) for c in conditions])

        matches = self.model.getMatches(conditions)
        print([str(m) for m in matches])

        d = 1
        levels = [] # [level (ie 0, 1, 2) : {fact, priorityTerms, backupTerms}
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
            
        
        currentLevel = len(levels) - 1
        for solution in levels[currentLevel]: # solution is possible end body literal
            i = currentLevel
            result = ""
            while solution[3] != None: # while not head
                if i == currentLevel:
                    result += str(solution[0]) # add fact
                else:
                    result += str(solution[0]) + ", "
                for option in levels[currentLevel - 1]:
                    if option[0] == solution[3]:
                        solution = option
                        i -= 1
                        break
            if solution[3] == None:
                result = str(solution[0]) + " :- " + result + "."
            print(result + "\n")