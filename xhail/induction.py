class Induction:
    def __init__(self, model):
        self.model = model
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
    
    def runPhase(self):
        program = ""

        # hypothesis space expansion
        program += "{ use_clause_literl(V1, 0) } :- clause(V1).\n"
        program += "{ use_clause_literl(V1, V2) } :- clause(V1), literal(V1, V2).\n"
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

        model.