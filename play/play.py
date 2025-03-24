import clingo

ctl = clingo.Control()

program = """
#show use/2.
%BACKGROUND%
bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

%EXAMPLES%
#maximize{ 1@1,flies(a) ; 2@1,flies(b) ; 3@1,flies(c) ; 4@1, not_flies(d) }.
:- not flies(a).
:- not flies(b).
:- not flies(c).
:- not not_flies(d).

%ABDUCIBLES%
0 { abduced_flies(A) : bird(A) } 1000000.
#minimize{1@2, A : abduced_flies(A), bird(A)}.
flies(A) :- abduced_flies(A), bird(A).

%NEGATIONS%
not_penguin(A) :- not penguin(A), bird(A).
not_flies(A) :- not flies(A), bird(A).

%COMPRESSION%
0 { use(V1, 0) } 1 :- clause(V1).
0 { use(V1, V2) } 1 :- clause(V1), literal(V1, V2).
clause(0).
literal(0,1).
clause(1).
literal(1,1).
clause(2).
literal(2,1).

:- not clause_level(0, 0), clause_level(0, 1).
:- not clause_level(1, 0), clause_level(0, 1).
:- not clause_level(2, 0), clause_level(0, 1).
clause_level(0, 0) :- use(0, 0).
clause_level(0, 1) :- use(0, 1).
clause_level(1, 0) :- use(1, 0).
clause_level(1, 1) :- use(1, 1).
clause_level(2, 0) :- use(2, 0).
clause_level(2, 1) :- use(2, 1).

#minimize{ 1@0,use(0,0) ; 1@0,use(0,1) ; 2@0,use(1,0) ; 2@0,use(1,1) ; 3@0,use(2,0) ; 3@0,use(2,1)}.

flies(V1) :- use(0, 0), try(0, 1, V1), bird(V1).
flies(V1) :- use(1, 0), try(1, 1, V1), bird(V1).
flies(V1) :- use(2, 0), try(2, 1, V1), bird(V1).

try(0, 1, V1) :- use(0, 1), not penguin(V1), bird(V1).
try(0, 1, V1) :- not use(0, 1), bird(V1).
try(1, 1, V1) :- use(1, 1), not penguin(V1), bird(V1).
try(1, 1, V1) :- not use(1, 1), bird(V1).
try(2, 1, V1) :- use(2, 1), not penguin(V1), bird(V1).
try(2, 1, V1) :- not use(2, 1), bird(V1).

"""

ctl.add("base", [], program)
ctl.ground([("base", [])])

def on_model(model):
    print("Model:", model.symbols(shown=True))
    # Access optimization cost from the model
    if model.optimality_proven:
        print("Optimization Cost:", model.cost)

result = ctl.solve(on_model=on_model)
