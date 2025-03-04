from ..parser.parser import Parser

class Induction:
    def __init__(self, model):
        self.model = model
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
    
    def runPhase(self):
        program = "#show use_clause_literal/2.\n" + self.model.getProgram()
        # hypothesis space expansion
        program += "{ use_clause_literal(V1, 0) } :- clause(V1).\n"
        program += "{ use_clause_literal(V1, V2) } :- clause(V1), literal(V1, V2).\n"
        program += "clause(0).\nliteral(0,1).\n"

        # rule construction
        program += ":- not clause_level(0, 0), clause_level(0, 1).\n"
        program += "clause_level(0, 0) :- use_clause_literal(0, 0).\n"
        program += "clause_level(0, 1) :- use_clause_literal(0, 1).\n"

        # minimisation
        program += "#minimize{ 1@1 : use_clause_literal(0,0) }.\n"
        program += "#minimize{ 1@1 : use_clause_literal(0,1) }.\n"

        # logic
        program += "flies(V1) :- use_clause_literal(0, 0), try_clause_literal(0, 1, V1), bird(V1).\n"
        program += "try_clause_literal(0, 1, V1) :- use_clause_literal(0, 1), not penguin(V1), bird(V1).\n"
        program += "try_clause_literal(0, 1, V1) :- not use_clause_literal(0, 1), bird(V1).\n"

        self.model.setProgram(program)
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