
from xhail.modes import Mode, Modeh
from xhail.terms import Atom, Clause, Constraint, Fact, Literal, Normal, PlaceMarker


M_p = [Modeh(Atom('flies', PlaceMarker('+', 'bird')), '*')]

B = [
    Clause(Atom('bird', Normal('X')), Literal(Atom('penguin', Normal('X')), False)),
    Fact(Atom('bird', Normal('a'))),
    Fact(Atom('bird', Normal('b'))),
    Fact(Atom('bird', Normal('c'))),
    Fact(Atom('penguin', Normal('d'))),
]

E = [
    Fact(Atom('bird', Normal('a'))),
    Fact(Atom('bird', Normal('b'))),
    Fact(Atom('bird', Normal('c'))),
    Constraint(Atom('penguin', Normal('d')), False),
]

# stage 1
A1 = set()
for m in M_p:
    fresh_fact = Fact(Atom(m.s.predicate+'_prime', Normal('X')))
    A1.add(Fact.toString(fresh_fact))

# stage 2
T1 = set()
T1.add("bird(X) :- penguin(X).")
T1.add("bird(a).")
T1.add("bird(b).")
T1.add("bird(c).")
T1.add("penguin(d).")

E = set()
E.add("flies(a).")
E.add("flies(b).")
E.add("flies(c).")
E.add(":- flies(d).")

for fresh_fact in A1:
    type = 'bird'
    pred = 'flies'
    p_clause = {'head': {'pred': pred, 'term': 'X'}, 'tail1': {'pred': pred + "*", 'term': 'X'}, 'tail2': {'pred': pred + "'", 'term': 'X'}}
    p_star_clause = {'head': {'pred': pred+'*', 'term': 'X'}, 'tail': {'pred': type, 'term': 'X'}}
    T1.add(str(p_clause['head']['pred'] + "(" + p_clause['head']['term'] + ")" + ' :- ' + p_clause['tail1']['pred'] + "(" + p_clause['tail1']['term'] + ")" + " , " + p_clause['tail2']['pred'] + "(" + p_clause['tail2']['term'] + ")."))
    T1.add(str(p_star_clause['head']['pred'] + "(" + p_star_clause['head']['term'] + ")" + ' :- ' + p_star_clause['tail']['pred'] + "(" + p_star_clause['tail']['term'] + ")."))

#stage 3 - how do i use clingo to find any solution for (A1, T1, E)
print("A1", A1)
print("T1", T1)
print("E", E)

program = "\n".join(A1 | T1 | E)

import clingo
# Create a Clingo control object
control = clingo.Control()

# Add your program
for line in program.splitlines():  # Split into separate lines
    control.add("base", [], line)

# Ground the program
control.ground([("base", [])])

# Solve the program
with control.solve(yield_=True) as solution:
    for model in solution:
        print(model)


