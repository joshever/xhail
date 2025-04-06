from xhail.language.terms import Atom, Clause, Literal, Normal, PlaceMarker

# -------------------------------------- #
# ---------- INDUCTION CLASS ----------- #
# -------------------------------------- #

class Induction:
    def __init__(self, model):
        self.model = model
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.EX = model.EX

    def loadExamples(self, examples):
        examplesProgram = '%EXAMPLES%\n'
        for example in examples:
            examplesProgram += example.createProgram() + '\n'
        return examplesProgram + '\n'
    
    def loadBackground(self, background):
        backgroundProgram = '%BACKGROUND%\n' + '\n'.join([str(b) for b in background]) + '\n'
        return backgroundProgram + '\n'

    # ----- Generate and Load Choice statements ----- #
    def loadChoice(self, clauses):
        program = "\n"
        program += "{ use(V1, 0) } :- clause(V1).\n"
        if self.model.DEPTH != 0 and sum((1 if clause.body != [] else 0) for clause in clauses) > 0:
            program += "{ use(V1, V2) } :- clause(V1), literal(V1, V2).\n"

        for idc, clause in enumerate(clauses):
            program += f"clause({idc}).\n"
            for idl in range(1, len(clause.body)+1):
                program += f"literal({idc}, {idl}).\n"
        return program
    
    # ----- Generate and Load Clause Level statements ----- #
    def loadClauseLevels(self, clauses):
        program = "\n"
        if self.model.DEPTH != 0 and sum((1 if clause.body != [] else 0) for clause in clauses) > 0:
            program += ":- level(X, Y), not level(X, 0).\n"
            for idc, clause in enumerate(clauses):
                # level 0 include not. all levels
                levels = []
                for idl in range(len(clause.body) + 1):
                    levels.append(f"level({idc},{idl})")
                    program += f"level({idc},{idl}) :- use({idc},{idl}).\n"
        return program
    
    # ----- Generate and Load Minimize statements ----- #
    def loadMinimize(self, clauses):
        program = "\n"
        for idc, clause in enumerate(clauses):
            for idl in range(len(clause.body)+1):
                program += "#minimize{ 1@2 : "+f"use({idc},{idl})"+" }.\n"
        return program
    
    # ----- Generate and Load Use/Try statements ----- #
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
            program += str(clause.head) + " :- " + f"use({idc}, 0)" + (', ' if clause.head.arity != 0 else '')
            if try_heads[idc] != []:
                program += ', '.join(try_head for try_head in try_heads[idc]) + ', '
            program += ', '.join(self.uniqueObjects(clause.getTypes())) + '.\n'

        return program

    # ----- Assign Types for Atom ----- #
    def updateAtomTypes(self, atom, mode): # modeb / modeh terms
        if atom.predicate != mode.predicate:
            return (False, None)
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
               res = self.updateAtomTypes(term1, term2)
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
    
    # ----- Remove Duplicates ----- #
    def uniqueObjects(self, objects):
        result = []
        visited = set()
        for object in objects:
            objectStr = str(object)
            if objectStr not in visited:
                visited.add(objectStr)
                result.append(object)
        return result

    def runPhase(self):
        # ----- Prepare Clauses ----- #
        clauses = [clause.generalise() for clause in self.model.getKernel()]
        clauses = self.updateClauseTypes(clauses)
        clauses = self.uniqueObjects(clauses)

        # ----- Constuct Program ----- #
        program = f'#show use/2.\n'
        program += self.loadBackground(self.BG)
        program += self.loadExamples(self.EX)
        program += self.loadChoice(clauses)
        program += self.loadMinimize(clauses)
        program += self.loadUseTry(clauses)
        program += self.loadClauseLevels(clauses)

        # ----- Update Model ----- #
        self.model.setProgram(program)
        self.model.writeProgram("xhail/output/induction.lp")

        selectors = {}
        best_model = self.model.getBestModel()
        if str(best_model) != '[]':
            selectors = {}
            facts = self.model.parseModel(best_model)
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
                    new_body = self.uniqueObjects(new_body)
                    new_clause = Clause(new_head, new_body)
                    included_clauses.append(new_clause)
        else:
            print("no solutions")
            return
        
        final_clauses = self.uniqueObjects(included_clauses)
        self.model.setHypothesis(final_clauses)