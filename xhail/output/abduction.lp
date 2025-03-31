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
%#maximize{1@1 : flies(a,chocolate)}.
:- not flies(a,chocolate).
%#maximize{1@1 : flies(b,vegetables)}.
:- not flies(b,vegetables).
%#maximize{1@1 : flies(c,vegetables)}.
:- not flies(c,vegetables).
%#maximize{1@1 : not flies(d,chocolate)}.
:- flies(d,chocolate).

%ABDUCIBLES%
0 { abduced_flies(V1,V2) : bird(V1), food(V2) } 1000000.
#minimize{1@2, V1, V2: abduced_flies(V1,V2), bird(V1), food(V2)}.
flies(V1,V2) :- abduced_flies(V1,V2), bird(V1), food(V2).

