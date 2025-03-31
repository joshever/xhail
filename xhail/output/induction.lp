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
clause(0).
clause(1).

#minimize{ 1@2 : use(0,0) }.
#minimize{ 1@2 : use(1,0) }.

flies(V1,chocolate) :- use(0, 0), bird(V1), food(chocolate).
flies(V1,vegetables) :- use(1, 0), bird(V1), food(vegetables).

