% ============================================================
% Benchmark: Event Calculus — "Work While Awake"
% ============================================================
% Task: learn WHEN an agent works, given observations of their
%       availability (awake/asleep) and productivity.
%
% The background encodes standard Event Calculus (EC) axioms
% alongside domain facts about when an agent wakes up and sleeps.
% XHAIL must abduce the specific work events, construct a kernel
% via deduction, and generalise to a hypothesis via induction.
%
% Expected hypothesis:
%   happens(work(V1),V2) :- holdsAt(awake(V1),V2).
%
% Interpretation: an agent works at time T if and only if they
% are awake at T.  The negative example (not productive at T=2,
% immediately after waking) rules out the unconditional version.
% ============================================================

% ---- Event Calculus axioms --------------------------------
holdsAt(F,T) :- time(T), time(S), S<T, happens(E,S), initiates(E,F,S), not clipped(S,F,T).
clipped(S,F,T) :- time(S), time(T), time(R), S<R, R<T, happens(E,R), terminates(E,F,R).
holdsAt(F,T) :- time(T), initially(F), not clipped(0,F,T).

% ---- Domain: time and agents ------------------------------
time(0). time(1). time(2). time(3). time(4). time(5). time(6). time(7).
person(alice).

% ---- Background events ------------------------------------
% Alice is asleep initially; wakes at T=2 and sleeps again at T=6.
happens(wake_up(alice), 2).
happens(sleep(alice), 6).

% ---- EC domain axioms -------------------------------------
initiates(wake_up(P), awake(P), T) :- person(P), time(T).
terminates(sleep(P),  awake(P), T) :- person(P), time(T).

% Working initiates a productive state for subsequent time steps.
initiates(work(P), productive(P), T) :- person(P), time(T).

% ---- Examples ---------------------------------------------
% Alice is not awake early; is awake mid-period.
#example not holdsAt(awake(alice), 1).
#example holdsAt(awake(alice), 4).

% Alice becomes productive at T=5 (she worked at T=4 while awake).
% She is NOT productive at T=2 (just woke up — no work yet).
#example holdsAt(productive(alice), 5).
#example not holdsAt(productive(alice), 2).

% ---- Mode declarations ------------------------------------
% '#person' is a ground-constant marker: the specific person name will appear
% literally in the learned hypothesis rather than being generalised to a variable.
#modeh happens(work(#person), +time).
#modeb holdsAt(awake(#person), +time).
