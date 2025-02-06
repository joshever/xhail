%BACKGROUND%
#display flies/1.
#display penguin/1.
bird(X) :- penguin(X).
bird(a;b;c).
penguin(d).

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
#minimize{1@1, A: abduced_flies(A), bird(A)}.
flies(A) :- abduced_flies(A), bird(A).
#show abduced_flies/1.
