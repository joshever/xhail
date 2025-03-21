from ..parser.parser import Parser

class Induction:
    def __init__(self, model):
        self.model = model
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
    
    def runPhase(self):
        clauses = [[1,1], [1,1], [1,1]]
        program = "#show use/2.\n" + self.model.getProgram()
        # hypothesis space expansion
        program += "{ use(V1, 0) } :- clause(V1).\n"
        program += "{ use(V1, V2) } :- clause(V1), literal(V1, V2).\n"
        for i, c in enumerate(clauses):
            program += f"clause({i}).\n"
            for j, l in enumerate(c):
                program += f"literal({i},{j}).\n"

        for i, c in enumerate(clauses):
            for j, l in enumerate(c):
                if j == 0:
                    program += f":- not clause_level({i}, 0)"
                else:
                    program += ", clause_level(0, 1)"
            program += ".\n"

        for i, c in enumerate(clauses):
            for j, l in enumerate(c):
                # rule construction
                program += f"clause_level({i}, {j}) :- use({i}, {j}).\n"

        for i, c in enumerate(clauses):
            for j, l in enumerate(c):
                # minimisation
                program += "#minimize{ 1@1 : "+f"use({i},{j})"+" }.\n"

        for i, c in enumerate(clauses):
            program += f"flies(V1) :- use({i}, 0)"
            for j, l in enumerate(c):
                program += f", try({i}, {j}, V1)"
            program += ", bird(V1).\n"
        # logic
        for i, c in enumerate(clauses):
            for j, l in enumerate(c):
                program += f"try({i}, {j}, V1) :- use({i}, {j}), not penguin(V1), bird(V1).\n"
                program += f"try({i}, {j}, V1) :- not use({i}, {j}), bird(V1).\n"

        self.model.setProgram(program)
        self.model.writeProgram()
        self.model.call()
        clingo_models = self.model.getClingoModels()

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

        # only include solution in the final code.