% =====================================================================
% Benchmark: Blocks World
% =====================================================================
% EC-based planning domain. Learn the precondition for picking up
% a block: the block must be clear (nothing on top of it).
%
% Expected hypothesis:
%   happens(pick_up(a), T) :- holdsAt(clear(a), T).
%   happens(pick_up(c), T) :- holdsAt(clear(c), T).
%   (b is never clear, so it never gets picked up)
% =====================================================================

% EC axioms
holdsAt(F,T) :- time(T), time(S), S<T, happens(E,S), initiates(E,F,S), not clipped(S,F,T).
clipped(S,F,T) :- time(S), time(T), time(R), S<R, R<T, happens(E,R), terminates(E,F,R).
holdsAt(F,T) :- time(T), initially(F), not clipped(0,F,T).

time(0). time(1). time(2). time(3).
block(a). block(b). block(c).

% Picking up a block makes it held and removes its clear status
initiates(pick_up(B), holding(B), T) :- block(B), time(T).
terminates(pick_up(B), clear(B),   T) :- block(B), time(T).

% Integrity constraint: can only pick up a clear block
:- happens(pick_up(B), T), not holdsAt(clear(B), T).

% Initial state: A on B on table; C on table.  A and C are clear; B is not.
initially(clear(a)).
initially(clear(c)).
initially(on(a, b)).
initially(on(b, table)).
initially(on(c, table)).

% Observations
#example holdsAt(holding(a), 1).
#example holdsAt(holding(c), 3).
#example not holdsAt(holding(b), 1).

% Mode declarations
% '#block' is a ground marker: a / b / c appear literally in the hypothesis.
#modeh happens(pick_up(#block), +time).
#modeb holdsAt(clear(#block), +time).
