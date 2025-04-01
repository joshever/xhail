%BACKGROUND%
bird(a).
bird(b).
food(chocolate).
food(vegetables).
penguin(d).
penguin(c).
bird(X) :- penguin(X).

%NEGATIONS%
not_penguin(V1) :- not penguin(V1), bird(V1).

%EXAMPLES%
%#maximize{1@1 : flies(a,eat(chocolate))}.
:- not flies(a,eat(chocolate)).
%#maximize{1@1 : flies(b,eat(vegetables))}.
:- not flies(b,eat(vegetables)).
%#maximize{1@1 : flies(c,eat(vegetables))}.
:- not flies(c,eat(vegetables)).
%#maximize{1@1 : not flies(d,eat(chocolate))}.
:- flies(d,eat(chocolate)).

%ABDUCIBLES%
0 { abduced_flies(V1,eat(V2)) : bird(V1), food(V2) } 1000000.
#minimize{1@2, V1, V2: abduced_flies(V1,eat(V2)), bird(V1), food(V2)}.
flies(V1,eat(V2)) :- abduced_flies(V1,eat(V2)), bird(V1), food(V2).

