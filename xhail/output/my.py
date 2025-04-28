import clingo

# Set up Clingo control
ctl = clingo.Control(["0", "--opt-mode=enum"])  # "0" means no limit on models

# Add your ASP program
ctl.add("base", [], """
%ORIGINAL BACKGROUND%
holdsAt(F, T) :- happens(E, S), time(S), time(T), S < T, initiates(E, F, S), not clipped(S, F, T), fluent(F).

clipped(S, F, T) :- happens(E, R), time(S), time(R), time(T), S < R, R < T, terminates(E, F, R).

holdsAt(F, T) :- time(T), not clipped(0, F, T), fluent(F).

time(0..9).

sugar(lactose ; glucose).

event(add(G) ; apply(G)) :- sugar(G).
fluent(available(G)) :- sugar(G).

initiates(add(G), available(G), T) :- sugar(G), time(T), happens(add(G), T).
terminates(apply(G), available(G), T) :- sugar(G), time(T).

:- happens(apply(G), T), time(T), not holdsAt(available(G), T), sugar(G).

happens(add(lactose), 0).
happens(add(glucose), 0).

%TEMPORARY NEGATIONS%
not_holdsAt(V1,V2) :- not holdsAt(V1,V2), fluent(V1), time(V2).

%EXAMPLES%
%#example holdsAt(available(lactose),1)
%#maximize{1@1 : holdsAt(available(lactose),1)}.
:- not holdsAt(available(lactose),1).
%#example holdsAt(available(lactose),2)
%#maximize{1@1 : holdsAt(available(lactose),2)}.
:- not holdsAt(available(lactose),2).
%#example not holdsAt(available(lactose),3)
%#maximize{1@1 : not holdsAt(available(lactose),3)}.
:- holdsAt(available(lactose),3).

%ABDUCIBLES%
%#modeh happens(apply($sugar),+time)
2 { abduced_happens(apply(V1),V2):sugar(V1), time(V2) } 2.
#minimize{1@1,V1, V2: abduced_happens(apply(V1),V2),sugar(V1), time(V2)}.
happens(apply(V1),V2) :- abduced_happens(apply(V1),V2),sugar(V1), time(V2).


#show happens/2.
""")

ctl.ground([("base", [])])

# Set the time limit (in seconds)
ctl.configuration.solve.time_limit = 5  # 5 seconds limit for solving

# Initialize results dictionary and model count limit
max_models = 10  # Limit to 10 models
results = {}

with ctl.solve(yield_=True) as handle:
    for i, model in enumerate(handle):
        # Break if we hit the model limit
        if i >= max_models:
            print(f"Stopped after reaching model limit ({max_models} models).")
            break
        
        atoms = model.symbols(shown=True)
        atom_list = [str(atom) for atom in atoms]
        
        # Read the cost from model.cost
        score = model.cost[0] if model.cost else 0

        if score not in results:
            results[score] = []
        results[score].append(atom_list)

        # Optionally print progress (e.g., number of models processed)
        print(f"Processed {i+1} models so far...")

# After solving, print results sorted by score
for score, models in sorted(results.items()):
    print(f"Score {score}:")
    for model in models:
        print("new model")
        print(f"  {model}")
