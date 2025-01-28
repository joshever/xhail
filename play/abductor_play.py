
modeh = [{'pred': 'flies', 'n': '*', 'type': 'bird', 'sign': '+'}]

background = [['clause', {'head': {'pred': 'bird', 'term': 'X'}, 'tail': {'pred': 'penguin', 'term': 'X'}}], 
            ['fact', {'pred': 'bird', 'term': 'a'}], 
            ['fact', {'pred': 'bird', 'term': 'b'}], 
            ['fact', {'pred': 'bird', 'term': 'c'}], 
            ['fact', {'pred': 'penguin', 'term': 'd'}]]

examples = [{'pred': 'flies', 'term': 'a'},
            {'pred': 'flies', 'term': 'b'},
            {'pred': 'flies', 'term': 'c'},
            {'pred': 'flies', 'term': 'd', 'negation': True}]

# stage 1
A1 = set()
for mh in modeh:
    fresh_fact = {'pred': mh['pred']+"'", 'term': 'X'}
    A1.add(str(fresh_fact['pred']) + "(" + str(fresh_fact['term']) + ").")

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


