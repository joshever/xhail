%BACKGROUND%
bird(a).
bird(b).
bird(c).
bird(d).
bird(e).
bird(f).
bird(X) :- penguin(X).
penguin(Z) :- creates(X,Y,Z), penguin(X), penguin(Y).
creates(d,e,f).
penguin(a).
penguin(b).
bird(a).
bird(b).
bird(c).
penguin(a).
penguin(b).
penguin(c).
creates(a,b,c).

%EXAMPLES%
#maximize{1@1 : flies(d)}.
:- not flies(d).
#maximize{1@1 : flies(e)}.
:- not flies(e).
#maximize{1@1 : flies(f)}.
:- not flies(f).
#maximize{1@1 : not flies(c)}.
:- flies(c).

%ABDUCIBLES%
0 { abduced_flies(A) : bird(A) } 1000000.
#minimize{1@1, A: abduced_flies(A), bird(A)}.
flies(A) :- abduced_flies(A), bird(A).
0 { abduced_penguin(A) : bird(A) } 1000000.
#minimize{1@1, A: abduced_penguin(A), bird(A)}.
penguin(A) :- abduced_penguin(A), bird(A).

%NEGATIONS%
not_penguin(A) :- not penguin(A), bird(A).
not_creates(A, B, C) :- not creates(A, B, C), bird(A, B, C).
not_penguin(A) :- not penguin(A), bird(A).
not_creates(A, B, C) :- not creates(A, B, C), bird(A, B, C).
