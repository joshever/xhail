#show use/2.
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


{ use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).

level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
:- not level(0,0),level(0,1).

#minimize{ 1@1 : use(0,0) }.
#minimize{ 1@1 : use(0,1) }.

flies(V0) :- use(0, 0), try(0, 1, V0), bird(V0).
try(0, 1, V0) :- use(0, 1), not penguin(V0), bird(V0).
try(0, 1, V0) :- not use(0, 1), bird(V0).
