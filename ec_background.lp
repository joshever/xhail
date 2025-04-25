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