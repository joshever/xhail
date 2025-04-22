from xhail.language.terms import Atom, Clause, Literal, Normal, PlaceMarker

# -------------------------------------- #
# ---------- INDUCTION CLASS ----------- #
# -------------------------------------- #

class Induction:
    def __init__(self, context):
        self.context = context
        self.MH = context.MH
        self.MB = context.MB
        self.BG = context.BG
        self.EX = context.EX

    # ---------- LOAD METHODS ---------- #

    def loadExamples(self, examples):
        examplesProgram = '%EXAMPLES%\n'
        for example in examples:
            examplesProgram += example.createProgram() + '\n'
        return examplesProgram + '\n'
    
    def loadBackground(self, background):
        backgroundProgram = '%BACKGROUND%\n' + '\n'.join([str(b) for b in background]) + '\n'
        return backgroundProgram + '\n'

    def loadChoice(self, clauses):
        program = "\n"
        program += "1 { use(V1, 0) } :- clause(V1).\n"
        if self.context.DEPTH != 0 and sum((1 if clause.body != [] else 0) for clause in clauses) > 0:
            program += "{ use(V1, V2) } :- clause(V1), literal(V1, V2).\n"

        for idc, clause in enumerate(clauses):
            program += f"clause({idc}).\n"
            for idl in range(1, len(clause.body)+1):
                program += f"literal({idc}, {idl}).\n"
        return program
    
    def loadClauseLevels(self, clauses):
        program = "\n"
        if self.context.DEPTH != 0 and sum((1 if clause.body != [] else 0) for clause in clauses) > 0:
            program += ":- level(X, Y), not level(X, 0).\n"
            for idc, clause in enumerate(clauses):
                # level 0 include not. all levels
                levels = []
                for idl in range(len(clause.body) + 1):
                    levels.append(f"level({idc},{idl})")
                    program += f"level({idc},{idl}) :- use({idc},{idl}).\n"
        return program
    
    def loadMinimize(self, clauses):
        program = "\n"
        for idc, clause in enumerate(clauses):
            for idl in range(len(clause.body)+1):
                program += "#minimize{ 1@2 : "+f"use({idc},{idl})"+" }.\n"
        return program
    
    def loadUseTry(self, clauses):
        program = "\n"

        # logic
        try_heads = {}
        for idc, clause in enumerate(clauses):
            try_heads[idc] = []
            for idl, literal in enumerate(clause.body):
                try_heads[idc].append(f"try({idc}, {idl+1}, {', '.join([var.value for var in literal.atom.getVariables()])})")
                program += f"try({idc}, {idl+1}, {', '.join([var.value for var in literal.atom.getVariables()])}) :- use({idc}, {idl+1}), {str(literal)}, {', '.join(literal.atom.getTypes())}.\n"
                program += f"try({idc}, {idl+1}, {', '.join([var.value for var in literal.atom.getVariables()])}) :- not use({idc}, {idl+1}), {', '.join(literal.atom.getTypes())}.\n"
        

        for idc, clause in enumerate(clauses):
            program += str(clause.head) + " :- " + f"use({idc}, 0)" + (', ' if clause.head.getArity() != 0 else '')
            if try_heads[idc] != []:
                program += ', '.join(try_head for try_head in try_heads[idc]) + ', '
            program += ', '.join(self.removeDuplicates(clause.getTypes())) + '.\n'

        return program
    
    def loadProgram(self, clauses):
        program = f'#show use/2.\n'
        program += self.loadBackground(self.BG)
        program += self.loadExamples(self.EX)
        program += self.loadChoice(clauses)
        program += self.loadMinimize(clauses)
        program += self.loadUseTry(clauses)
        program += self.loadClauseLevels(clauses)
        return program

    # ---------- ASSIGN TYPES ---------- #
    def assignAtomTypes(self, atom, mode): # modeb / modeh terms
        if atom.predicate != mode.predicate:
            return (False, None)
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
               res = self.assignAtomTypes(term1, term2)
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
    
    # ----- Assing Types for Clause ----- #
    def assignClauseTypes(self, clauses):
        new_clauses = []
        for clause in clauses:
            new_head = None
            new_body = []
            for modeh in self.MH:
                valid, head = self.assignAtomTypes(clause.head, modeh.atom)
                if valid == True:
                    new_head = head
                    break
            for literal in clause.body:
                for modeb in self.MB:
                    valid, new_literal = self.assignAtomTypes(literal.atom, modeb.atom)
                    if valid == True:
                        new_body.append(Literal(new_literal, literal.negation))
                        break
            new_clauses.append(Clause(new_head, new_body))
        return new_clauses
    
    # ---------- CLAUSE OPERATIONS ---------- #
    def revampClauses(self):
        clauses = [clause.generalise() for clause in self.context.getKernel()]
        clauses = self.assignClauseTypes(clauses)
        clauses = self.removeDuplicates(clauses)
        return clauses
    
    def filterClauses(self, clauses):
        self.context.getInterfaceResult(self.context.current_id)
        self.context.writeInterfaceProgram(self.context.current_id, "xhail/output/induction.lp")

        selectors = {}
        best_context = self.context.getInterfaceResult(self.context.current_id)
        if str(best_context) != '[]':
            selectors = {}
            facts = self.context.interfaces[self.context.current_id].parseModel(best_context)
            for fact in facts:
                terms = fact.head.terms
                if int(terms[0].value) in selectors.keys():
                    selectors[int(terms[0].value)].append(int(terms[1].value))
                else:
                    selectors[int(terms[0].value)] = [int(terms[1].value)]  
 
            included_clauses = []
            for key in selectors.keys():
                if 0 in selectors[key]: # head = key
                    selectors[key].remove(0)
                    new_head = clauses[key].head
                    new_body = []
                    for literal in selectors[key]:
                        new_body.append(clauses[key].body[literal-1])
                    new_body = self.removeDuplicates(new_body)
                    new_clause = Clause(new_head, new_body)
                    included_clauses.append(new_clause)
        else:
            print("no solutions")
            return
        return included_clauses
    
    def removeDuplicates(self, objects):
        result = []
        visited = set()
        for object in objects:
            objectStr = str(object)
            if objectStr not in visited:
                visited.add(objectStr)
                result.append(object)
        return result

    # ---------- RUN ---------- #
    def run(self):
        clauses = self.revampClauses()
        program = self.loadProgram(clauses)

        ind_id = self.context.addInterface(program) # 5 second timeout
        self.context.current_id = ind_id

        included_clauses = self.filterClauses(clauses)
        final_clauses = self.removeDuplicates(included_clauses)
        self.context.setHypothesis(final_clauses)