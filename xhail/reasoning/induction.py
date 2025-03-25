from xhail.language.terms import Atom, Clause, Literal, Normal, PlaceMarker
from ..parser.parser import Parser

class Induction:
    def __init__(self, model):
        self.model = model
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG

    def loadChoice(self, clauses, shape, program = ""):
        program += "{ use(V1, 0) } :- clause(V1).\n"
        program += "{ use(V1, V2) } :- clause(V1), literal(V1, V2).\n"

        for c in range(len(clauses)):
            program += f"clause({c}).\n"
            for l in range(1, shape[c]):
                program += f"literal({c}, {l}).\n"
        return program
    
    def loadClauseLevels(self, clauses, shape, program = ""):
        for c in range(len(clauses)):
            # level 0 include not. all levels
            levels = []
            for l in range(shape[c]):
                levels.append(f"level({c},{l})")
                program += f"level({c},{l}) :- use({c},{l}).\n"
            program += ":- not " + ','.join(levels) + ".\n"
        return program
    
    def loadMinimize(self, clauses, shape, program = ""):
        for c in range(len(clauses)):
            for l in range(shape[c]):
                program += "#minimize{ 1@1 : "+f"use({c},{l})"+" }.\n"
        return program
    
    def loadUseTry(self, clauses, shape, program=""):
        for idc, clause in enumerate(clauses):
            program += str(clause.head) + " :- " + f"use({idc}, 0)"
            for idl in range(1, shape[idc]):
                program += f",try({idc}, {idl}, {clause.head.terms})"
            program += "type(V1)"

        # logic
        for i, c in enumerate(clauses):
            for j, l in enumerate(c):
                program += f"try({i}, {j}, {vars[literals[i][j]]}) :- use({i}, {j}), not penguin(V1), bird(V1).\n"
                program += f"try({i}, {j}, {vars}) :- not use({i}, {j}), bird(V1).\n"

    def updateAtomTypes(self, atom, mode): # modeb / modeh terms
        if atom.predicate != mode.predicate:
            return (False, None)
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
               res = self.updateTypes(term1, term2)
               if res[0] == False:
                   return (False, None)
               else:
                   term1 = res[1]
            elif isinstance(term2, Normal):
                if term1.value != term2.value:
                    return (False, None)
            elif isinstance(term2, PlaceMarker) and isinstance(term1, Normal):
                term1.setType(term2.type)
            else:
                continue
        return (True, atom)
    
    def updateClauseTypes(self, clauses):
        new_clauses = []
        for clause in clauses:
            new_head = None
            new_body = []
            for modeh in self.MH:
                valid, head = self.updateAtomTypes(clause.head, modeh.atom)
                if valid == True:
                    new_head = head
                    break
            for literal in clause.body:
                for modeb in self.MB:
                    valid, new_literal = self.updateAtomTypes(literal.atom, modeb.atom)
                    if valid == True:
                        new_body.append(Literal(new_literal, literal.negation))
                        break
            new_clauses.append(Clause(new_head, new_body))
        return new_clauses
    
    def keepUniqueClauses(self, clauses):
        result = []
        visited = set()
        for clause in clauses:
            clauseStr = str(clause)
            if clauseStr not in visited:
                visited.add(clauseStr)
                result.append(clause)
        return result

    def runPhase(self):
        # INPUT
        clauses = [clause.generalise() for clause in self.model.getKernel()]
        clauses = self.keepUniqueClauses(clauses)
        clauses = self.updateClauseTypes(clauses)

        """
        # ---------- Constuct Program ---------- #
        program += self.loadChoice(clauses, shape)
        program += self.loadClauseLevels(clauses, shape)
        program += self.loadMinimize(clauses, shape)
        program += self.loadUseTry(clauses, shape)


        self.model.setProgram(program)
        self.model.writeProgram("xhail/output/induce.lp")
        self.model.call()
        """