%BACKGROUND%
bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

%NEGATIONS%
not_penguin(A) :- not penguin(A), bird(A).

%EXAMPLES%
#maximize{1@1 : flies(a)}.
:- not flies(a).
#maximize{1@1 : flies(b)}.
:- not flies(b).
#maximize{1@1 : flies(c)}.
:- not flies(c).
#maximize{1@1 : not flies(d)}.
:- flies(d).

%ABDUCIBLES%
0 { abduced_flies(A) : bird(A) } 1000000.
#minimize{1@2, A: abduced_flies(A), bird(A)}.
flies(A) :- abduced_flies(A), bird(A).

