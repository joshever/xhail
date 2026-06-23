% =====================================================================
% Benchmark: Sugar Domain  (Ray 2009, §5 Example 2)
% =====================================================================
% Task: learn priority-ordered sugar consumption.
%       Glucose is preferred; lactose is used only when glucose is gone.
%
% Expected hypothesis:
%   happens(use(glucose),T) :- holdsAt(available(glucose),T).
%   happens(use(lactose),T) :- holdsAt(available(lactose),T),
%                               not holdsAt(available(glucose),T).
% =====================================================================

% ── EC Axioms (A1-A3) ──────────────────────────────────────────────
holdsAt(F,T) :- time(T), time(S), S<T, happens(E,S), initiates(E,F,S), not clipped(S,F,T).
clipped(S,F,T) :- time(S), time(T), time(R), S<R, R<T, happens(E,R), terminates(E,F,R).
holdsAt(F,T) :- time(T), initially(F), not clipped(0,F,T).

% ── Time (T1) ──────────────────────────────────────────────────────
time(0). time(1). time(2). time(3). time(4). time(5).

% ── Domain types (T2) ──────────────────────────────────────────────
sugar(lactose). sugar(glucose).

% ── Initiation / termination (D1-D2) ───────────────────────────────
initiates(add(G), available(G), T) :- sugar(G), time(T).
terminates(use(G), available(G), T) :- sugar(G), time(T).

% ── Integrity constraint: can't use unavailable sugar (D3) ─────────
:- happens(use(G), T), not holdsAt(available(G), T).

% ── Initial events: both sugars added at T=0 (N1-N2) ───────────────
happens(add(lactose), 0).
happens(add(glucose), 0).

% ── Examples (E1-E3) ───────────────────────────────────────────────
% Lactose is available at T=1 and T=2 (glucose used first),
% then consumed at T=2 (unavailable at T=3).
#example holdsAt(available(lactose), 1).
#example holdsAt(available(lactose), 2).
#example not holdsAt(available(lactose), 3).

% Force glucose to be abduced so XHAIL can learn the glucose rule.
% Without this the abduction ignores glucose and only the lactose rule
% is learned.
#example not holdsAt(available(glucose), 2).

% ── Mode declarations (M1-M3) ──────────────────────────────────────
% '#sugar' is a ground marker: lactose / glucose appear literally
%          in the learned hypothesis (not generalised to a variable).
% '+time'  is an input variable ranging over the time type.
#modeh happens(use(#sugar), +time).
#modeb holdsAt(available(#sugar), +time).
#modeb not holdsAt(available(#sugar), +time).
