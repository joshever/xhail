from xhail.language.terms import Atom, Clause, Literal, Normal, PlaceMarker
from ..parser.parser import Parser

class Induction:
    def __init__(self, model):
        self.model = model
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG

    def loadChoice(self, clauses): # literal 0 == clause head. literal 1 = first clause literal. !!! clause 0 is first clause
        program = "{ use(V1, 0) } :- clause(V1).\n"
        program += "{ use(V1, V2) } :- clause(V1), literal(V1, V2).\n"


        for idc, clause in enumerate(clauses):
            program += f"clause({idc}).\n"
            for idl in range(1, len(clause.body)+1):
                program += f"literal({idc}, {idl}).\n"
        return program
    
    def loadClauseLevels(self, clauses):
        program = ""
        for idc, clause in enumerate(clauses):
            # level 0 include not. all levels
            levels = []
            for idl in range(len(clause.body) + 1):
                levels.append(f"level({idc},{idl})")
                program += f"level({idc},{idl}) :- use({idc},{idl}).\n"
            program += ":- not " + ','.join(levels) + ".\n"
        return program
    
    def loadMinimize(self, clauses):
        program = ""
        for idc, clause in enumerate(clauses):
            for idl in range(len(clause.body)+1):
                program += "#minimize{ 1@1 : "+f"use({idc},{idl})"+" }.\n"
        return program
    
    def loadUseTry(self, clauses):
        program = ""

        for idc, clause in enumerate(clauses):
            program += str(clause.head) + " :- " + f"use({idc}, 0)"
            for idl in range(1, len(clause.body)+1):
                program += f",try({idc}, {idl}, {','.join([term.value for term in clause.head.terms])})"
            print("hey: ",','.join(clause.getTypes()))
            program += ','.join(clause.getTypes())

        # logic
        for idc, clause in enumerate(clauses):
            for idl, literal in enumerate(clause.body):
                program += f"try({idc}, {idl+1}, {','.join([var.value for var in literal.atom.getVariables()])}) :- use({idc}, {idl+1}), {str(literal)}, {','.join(literal.atom.getTypes())}.\n"
                program += f"try({idc}, {idl+1}, {','.join([var.value for var in literal.atom.getVariables()])}) :- not use({idc}, {idl+1}), {','.join(literal.atom.getTypes())}.\n"
        
        return program

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

        for clause in clauses:
            print(clause.getTypes())

        
        # ---------- Constuct Program ---------- #
        program = self.model.getProgram()
        program += self.loadChoice(clauses)
        program += self.loadClauseLevels(clauses)
        program += self.loadMinimize(clauses)
        program += self.loadUseTry(clauses)


        self.model.setProgram(program)
        self.model.writeProgram("xhail/output/induce.lp")
        self.model.call()
        