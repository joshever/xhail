#show use/2.
%BACKGROUND%
bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

%EXAMPLES%
%#maximize{5@1 : flies(a)}.
:- not flies(a).
%#maximize{1@1 : flies(b)}.
:- not flies(b).
%#maximize{1@1 : flies(c)}.
:- not flies(c).
%#maximize{1@1 : not flies(d)}.
:- flies(d).


{ use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).

#minimize{ 1@2 : use(0,0) }.
#minimize{ 1@2 : use(0,1) }.

try(0, 1, V1) :- use(0, 1), not penguin(V1), bird(V1).
try(0, 1, V1) :- not use(0, 1), bird(V1).
flies(V1) :- use(0, 0) , try(0, 1, V1), bird(V1).

:- level(X, Y), not level(X, 0).level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
