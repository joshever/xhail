import clingo

# Define the logic program with abduction for flies_prime(X)
program = """
bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

flies(a).
flies(b).
flies(c).
not flies(d).

flies(X) :- flies_prime(X), flies_star(X).
flies_star(X) :- bird(X).
"""

# Create a Clingo control object
ctl = clingo.Control()

# Add the logic program to the control object
ctl.add("base", [], program)

# Ground the program (transform it into a propositional form)
ctl.ground([("base", [])])

# Solve and print the answer sets, specifically focusing on flies_prime(X)
with ctl.solve(yield_=True) as solver:
    for model in solver:
        # Output the flies_prime(X) values found in the answer set
        flies_prime_values = [atom for atom in model.symbols(shown=True) if atom.name == "flies_prime"]
        print("Possible flies_prime(X) values:", flies_prime_values)
    
    # Debug: Output all the atoms in the model
    print("All atoms in the model:", [atom for atom in model.symbols(shown=True)])
