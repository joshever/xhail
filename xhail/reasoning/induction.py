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
                program += f"try({i}, {j}, V1) :- use({i}, {j}), not penguin(V1), bird(V1).\n"
                program += f"try({i}, {j}, V1) :- not use({i}, {j}), bird(V1).\n"

    def runPhase(self):
        # INPUT
        clauses = [clause.generalise() for clause in self.model.getKernel()] # [clause[0]-clause[len(clauses)-1]]
        shape = [len(clause.body) for clause in clauses]
        program = "#show use/2.\n" + self.model.getProgram()
        print([str(clause) for clause in clauses])

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
        #clingo_models = self.model.getClingoModels()


        """
        for cm in clingo_models:
            if str(cm) != "[]":
                strModel = ""
                for fact in cm:
                    strModel += str(fact) + '.\n'
                simpleParser = Parser()
                simpleParser.loadString(strModel)
                facts = simpleParser.parseProgram()
        for fact in facts:
            print([int(str(term)) for term in fact.head.terms])
        """
        # only include solution in the final code.