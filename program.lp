flies(c).
flies'(X).
flies(a).
<- flies(d).
penguin(d).
bird(X) :- penguin(X).
flies(X):-flies*(X),flies'(X).
flies(b).
bird(c).
bird(a).
bird(b).
flies*(X):-bird(X).