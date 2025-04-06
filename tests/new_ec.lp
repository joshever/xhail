holdsAt(F, T) :- happens(E, S), time(S), time(T), S < T, initiates(E, F, S), not clipped(S, F, T), fluent(F).

clipped(S, F, T) :- happens(E, R), time(S), time(R), time(T), S < R, R < T, terminates(E, F, R).

holdsAt(F, T) :- time(T), not clipped(0, F, T), fluent(F).


time(0).
time(1).
time(2).
time(3).
time(4).
time(5).
time(6).
time(7).
time(8).
time(9).

sugar(lactose).
sugar(glucose).

event(add(G)) :- sugar(G).
event(apply(G)) :- sugar(G).
fluent(available(G)) :- sugar(G).

initiates(add(G), available(G), T) :- sugar(G), time(T), happens(add(G), T).
terminates(apply(G), available(G), T) :- sugar(G), time(T).

:- happens(apply(G), T), time(T), not holdsAt(available(G), T), sugar(G).

happens(add(lactose), 0).
happens(add(glucose), 0).

%% E. Examples
#example holdsAt(available(lactose), 1).
#example holdsAt(available(lactose), 2).
#example not holdsAt(available(lactose), 3).

%% M. Modes
#modeh happens(apply($sugar),+time) :100.
#modeb holdsAt($fluent,+time).
#modeb not holdsAt($fluent,+time).
