#show use/2.
%BACKGROUND%
holdsAt(F, T) :- happens(E, S), time(S), time(T), S < T, initiates(E, F, S), not clipped(S, F, T), fluent(F).

clipped(S, F, T) :- happens(E, R), time(S), time(R), time(T), S < R, R < T, terminates(E, F, R).

holdsAt(F, T) :- time(T), not clipped(0, F, T), fluent(F).

time(0..9).

sugar(lactose ; glucose).

event(add(G) ; apply(G)) :- sugar(G).
fluent(available(G)) :- sugar(G).

initiates(add(G), available(G), T) :- sugar(G), time(T), happens(add(G), T).
terminates(apply(G), available(G), T) :- sugar(G), time(T).

:- happens(apply(G), T), time(T), not holdsAt(available(G), T), sugar(G).

happens(add(lactose), 0).
happens(add(glucose), 0).

%EXAMPLES%
%#maximize{1@1 : holdsAt(available(lactose),1)}.
:- not holdsAt(available(lactose),1).
%#maximize{1@1 : holdsAt(available(lactose),2)}.
:- not holdsAt(available(lactose),2).
%#maximize{1@1 : not holdsAt(available(lactose),3)}.
:- holdsAt(available(lactose),3).


1 { use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).
literal(0, 2).
clause(1).
literal(1, 1).
literal(1, 2).
clause(2).
literal(2, 1).
literal(2, 2).
clause(3).
literal(3, 1).
literal(3, 2).

#minimize{ 1@2 : use(0,0) }.
#minimize{ 1@2 : use(0,1) }.
#minimize{ 1@2 : use(0,2) }.
#minimize{ 1@2 : use(1,0) }.
#minimize{ 1@2 : use(1,1) }.
#minimize{ 1@2 : use(1,2) }.
#minimize{ 1@2 : use(2,0) }.
#minimize{ 1@2 : use(2,1) }.
#minimize{ 1@2 : use(2,2) }.
#minimize{ 1@2 : use(3,0) }.
#minimize{ 1@2 : use(3,1) }.
#minimize{ 1@2 : use(3,2) }.

try(0, 1, V1) :- use(0, 1), holdsAt(available(lactose),V1), time(V1).
try(0, 1, V1) :- not use(0, 1), time(V1).
try(0, 2, V1) :- use(0, 2), not holdsAt(available(glucose),V1), time(V1).
try(0, 2, V1) :- not use(0, 2), time(V1).
try(1, 1, V1) :- use(1, 1), not holdsAt(available(glucose),V1), time(V1).
try(1, 1, V1) :- not use(1, 1), time(V1).
try(1, 2, V1) :- use(1, 2), holdsAt(available(lactose),V1), time(V1).
try(1, 2, V1) :- not use(1, 2), time(V1).
try(2, 1, V1) :- use(2, 1), holdsAt(available(lactose),V1), time(V1).
try(2, 1, V1) :- not use(2, 1), time(V1).
try(2, 2, V1) :- use(2, 2), holdsAt(available(glucose),V1), time(V1).
try(2, 2, V1) :- not use(2, 2), time(V1).
try(3, 1, V1) :- use(3, 1), holdsAt(available(glucose),V1), time(V1).
try(3, 1, V1) :- not use(3, 1), time(V1).
try(3, 2, V1) :- use(3, 2), holdsAt(available(lactose),V1), time(V1).
try(3, 2, V1) :- not use(3, 2), time(V1).
happens(apply(lactose),V1) :- use(0, 0), try(0, 1, V1), try(0, 2, V1), sugar(lactose), time(V1).
happens(apply(lactose),V1) :- use(1, 0), try(1, 1, V1), try(1, 2, V1), sugar(lactose), time(V1).
happens(apply(glucose),V1) :- use(2, 0), try(2, 1, V1), try(2, 2, V1), sugar(glucose), time(V1).
happens(apply(glucose),V1) :- use(3, 0), try(3, 1, V1), try(3, 2, V1), sugar(glucose), time(V1).

:- level(X, Y), not level(X, 0).
level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
level(0,2) :- use(0,2).
level(1,0) :- use(1,0).
level(1,1) :- use(1,1).
level(1,2) :- use(1,2).
level(2,0) :- use(2,0).
level(2,1) :- use(2,1).
level(2,2) :- use(2,2).
level(3,0) :- use(3,0).
level(3,1) :- use(3,1).
level(3,2) :- use(3,2).
