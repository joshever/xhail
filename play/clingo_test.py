import clingo

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
