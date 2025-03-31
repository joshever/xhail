#show use/2.
%BACKGROUND%
bird(a).
bird(b).
food(chocolate).
food(vegetables).
penguin(d).
penguin(c).
bird(X) :- penguin(X).

%EXAMPLES%
%#maximize{1@1 : flies(a,chocolate)}.
:- not flies(a,chocolate).
%#maximize{1@1 : flies(b,vegetables)}.
:- not flies(b,vegetables).
%#maximize{1@1 : flies(c,vegetables)}.
:- not flies(c,vegetables).
%#maximize{1@1 : not flies(d,chocolate)}.
:- flies(d,chocolate).


{ use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).
clause(1).
literal(1, 1).
clause(2).
literal(2, 1).

#minimize{ 1@2 : use(0,0) }.
#minimize{ 1@2 : use(0,1) }.
#minimize{ 1@2 : use(1,0) }.
#minimize{ 1@2 : use(1,1) }.
#minimize{ 1@2 : use(2,0) }.
#minimize{ 1@2 : use(2,1) }.

try(0, 1, V1) :- use(0, 1), not penguin(V1), bird(V1).
try(0, 1, V1) :- not use(0, 1), bird(V1).
try(1, 1, V1) :- use(1, 1), not penguin(V1), bird(V1).
try(1, 1, V1) :- not use(1, 1), bird(V1).
try(2, 1, V1) :- use(2, 1), penguin(V1), bird(V1).
try(2, 1, V1) :- not use(2, 1), bird(V1).
flies(V1,chocolate) :- use(0, 0), try(0, 1, V1), bird(V1), food(chocolate).
flies(V1,vegetables) :- use(1, 0), try(1, 1, V1), bird(V1), food(vegetables).
flies(V1,vegetables) :- use(2, 0), try(2, 1, V1), bird(V1), food(vegetables).

:- level(X, Y), not level(X, 0).
level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
level(1,0) :- use(1,0).
level(1,1) :- use(1,1).
level(2,0) :- use(2,0).
level(2,1) :- use(2,1).
