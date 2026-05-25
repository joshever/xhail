import logging

from xhail.language.terms import Atom, Clause, Literal, Normal, PlaceMarker

logger = logging.getLogger(__name__)


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

    # ---------- Generate and Load Choice statements ---------- #
    def loadChoice(self, clauses): # literal 0 == clause head. literal 1 = first clause literal. !!! clause 0 is first clause
        program = "\n"
        program += "{ use(V1, 0) } :- clause(V1).\n"
        program += "{ use(V1, V2) } :- clause(V1), literal(V1, V2).\n"

        for idc, clause in enumerate(clauses):
            program += f"clause({idc}).\n"
            for idl in range(1, len(clause.body)+1):
                program += f"literal({idc}, {idl}).\n"
        return program

    # ---------- Generate and Load Clause Level statements ---------- #
    def loadClauseLevels(self, clauses):
        program = "\n"
        program += ":- level(X, Y), not level(X, 0)."
        for idc, clause in enumerate(clauses):
            # level 0 include not. all levels
            levels = []
            for idl in range(len(clause.body) + 1):
                levels.append(f"level({idc},{idl})")
                program += f"level({idc},{idl}) :- use({idc},{idl}).\n"
        return program

    # ---------- Generate and Load Minimize statements ---------- #
    def loadMinimize(self, clauses):
        program = "\n"
        for idc, clause in enumerate(clauses):
            for idl in range(len(clause.body)+1):
                program += "#minimize{ 1@2 : "+f"use({idc},{idl})"+" }.\n"
        return program

    # ---------- Build a try/N atom, handling 0-arity (propositional) predicates ---------- #
    def _try_term(self, idc: int, idl: int, literal) -> str:
        """Return the try/N atom string for a kernel literal.

        For first-order predicates the atom carries variable arguments, e.g.
        ``try(0, 1, V1)``.  For propositional (0-arity) predicates there are no
        variables, so we emit ``try(0, 1)`` without a trailing comma.
        """
        vars_parts = [var.value for var in literal.atom.getVariables()]
        if vars_parts:
            return f"try({idc}, {idl}, {', '.join(vars_parts)})"
        return f"try({idc}, {idl})"

    # ---------- Generate and Load Use/Try statements ---------- #
    def loadUseTry(self, clauses):
        program = "\n"

        try_heads: dict[int, list[str]] = {}
        for idc, clause in enumerate(clauses):
            try_heads[idc] = []
            for idl, literal in enumerate(clause.body):
                try_term = self._try_term(idc, idl + 1, literal)
                try_heads[idc].append(try_term)
                types = literal.atom.getTypes()
                types_suffix = (", " + ", ".join(types)) if types else ""
                program += (
                    f"{try_term} :- use({idc}, {idl+1}), {str(literal)}{types_suffix}.\n"
                )
                program += (
                    f"{try_term} :- not use({idc}, {idl+1}){types_suffix}.\n"
                )

        for idc, clause in enumerate(clauses):
            clause_types = self.uniqueObjects(clause.getTypes())
            types_suffix = (", " + ", ".join(str(t) for t in clause_types)) if clause_types else ""
            body_parts = [f"use({idc}, 0)"] + try_heads[idc]
            program += f"{str(clause.head)} :- {', '.join(body_parts)}{types_suffix}.\n"

        return program

    # ---------- Assign Types for Atom ---------- #
    def updateAtomTypes(self, atom, mode): # modeb / modeh terms
        if atom.predicate != mode.predicate:
            return (False, None)
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
               res = self.updateTypes(term1, term2)
               if not res[0]:
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

    # ---------- Assing Types for Clause ---------- #
    def updateClauseTypes(self, clauses):
        new_clauses = []
        for clause in clauses:
            new_head = None
            new_body = []
            for modeh in self.MH:
                valid, head = self.updateAtomTypes(clause.head, modeh.atom)
                if valid:
                    new_head = head
                    break
            for literal in clause.body:
                for modeb in self.MB:
                    valid, new_literal = self.updateAtomTypes(literal.atom, modeb.atom)
                    if valid:
                        new_body.append(Literal(new_literal, literal.negation))
                        break
            new_clauses.append(Clause(new_head, new_body))
        return new_clauses

    # ---------- Remove Duplicates ---------- #
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
        # ---------- Prepare Clauses ---------- #
        clauses = [clause.generalise() for clause in self.model.getKernel()]
        clauses = self.updateClauseTypes(clauses)
        clauses = self.uniqueObjects(clauses)

        # ---------- Constuct Program ---------- #
        program = '#show use/2.\n'
        program += self.loadBackground(self.BG)
        program += self.loadExamples(self.EX)
        program += self.loadChoice(clauses)
        program += self.loadMinimize(clauses)
        program += self.loadUseTry(clauses)
        program += self.loadClauseLevels(clauses)

        # ---------- Update Model ---------- #
        self.model.setProgram(program)
        logger.debug("Running induction phase...")

        if self.model.debug_output_dir is not None:
            dest = self.model.debug_output_dir / "induction.lp"
            dest.parent.mkdir(parents=True, exist_ok=True)
            self.model.writeProgram(str(dest))
            logger.debug("Induction program written to %s", dest)

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
                    selectors[key].pop(-1)
                    new_head = clauses[0].head
                    new_body = []
                    for literal in selectors[key]:
                        new_body.append(clauses[key].body[literal-1])
                    new_body = self.uniqueObjects(new_body)
                    new_clause = Clause(new_head, new_body)
                    included_clauses.append(new_clause)
            self.model.setHypothesis(included_clauses)
            logger.info("Learned hypothesis (%d rule(s)):", len(included_clauses))
            for clause in included_clauses:
                logger.info("  %s", clause)
        else:
            self.model.setHypothesis([])
            logger.info("No hypothesis found (induction returned no solution).")
