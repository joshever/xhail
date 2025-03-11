%BACKGROUND%
penguin(a).
penguin(b).
bird(c).
bird(e).
bird(f).
bird(X) :- penguin(X).
penguin(Z) :- creates(X,Y,Z), penguin(X), penguin(Y).
creates(a,b,d).
%EXAMPLES%
#maximize{1@1 : flies(c)}.
:- not flies(c).
#maximize{1@1 : flies(e)}.
:- not flies(e).
#maximize{1@1 : flies(f)}.
:- not flies(f).
#maximize{1@1 : not flies(d)}.
:- flies(d).
#maximize{1@1 : not flies(a)}.
:- flies(a).
#maximize{1@1 : not flies(b)}.
:- flies(b).

%ABDUCIBLES%
0 { abduced_flies(A) : bird(A) } 1000000.
#minimize{1@1, A: abduced_flies(A), bird(A)}.
flies(A) :- abduced_flies(A), bird(A).
