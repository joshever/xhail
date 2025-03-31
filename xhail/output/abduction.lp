%BACKGROUND%
bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

%NEGATIONS%
not_penguin(V1) :- not penguin(V1), bird(V1).

%EXAMPLES%
%#maximize{5@1 : flies(a)}.
:- not flies(a).
%#maximize{1@1 : flies(b)}.
:- not flies(b).
%#maximize{1@1 : flies(c)}.
:- not flies(c).
%#maximize{1@1 : not flies(d)}.
:- flies(d).

%ABDUCIBLES%
0 { abduced_flies(V1) : bird(V1) } 1000000.
#minimize{1@2, V1: abduced_flies(V1), bird(V1)}.
flies(V1) :- abduced_flies(V1), bird(V1).

