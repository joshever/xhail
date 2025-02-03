import clingo

asp_program = """
loves(a, b)
cricket(a)
fun(b) :- cricket(a)
a.
"""

def on_model(model):
    print("Answer Set:", model.symbols(atoms=True))

ctl = clingo.Control()

ctl.add("base", [], asp_program)

ctl.ground([("base", [])])

ctl.solve(on_model=on_model)
