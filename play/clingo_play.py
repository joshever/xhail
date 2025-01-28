import clingo

asp_program = """
loves(a, b)
cricket(a)
fun(b) :- cricket(a)
a.
"""

# Callback to process the answer sets
def on_model(model):
    print("Answer Set:", model.symbols(atoms=True))

# Create a Clingo Control object
ctl = clingo.Control()

# Load the ASP program
ctl.add("base", [], asp_program)

# Ground the program
ctl.ground([("base", [])])

# Solve the program and process the results
ctl.solve(on_model=on_model)
