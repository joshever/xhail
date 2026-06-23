% =====================================================================
% Benchmark: Epidemic Spread
% =====================================================================
% EC model of disease propagation through a contact network.
% Learn who infects whom and when, based on who is already ill.
%
% Expected hypothesis:
%   happens(infect(bob),   T) :- holdsAt(ill(alice), T).
%   happens(infect(carol), T) :- holdsAt(ill(bob),   T).
%
% Design note: Alice contracts the disease at T=0 via an external event
% (not learned — it is background knowledge), becoming ill from T=1.
% This shifts the infection chain one step forward compared to the
% initially(ill(alice)) design, creating a T=0 window where no one is
% ill yet.  The negative examples #example not holdsAt(ill(bob),1) and
% #example not holdsAt(ill(carol),2) exploit this gap: an unconditional
% (empty-body) infect rule would make bob and carol ill one step earlier,
% violating those negatives.  This forces induction to learn the
% conditional rules rather than the trivially-minimal empty-body form.
% =====================================================================

% ── EC Axioms ──────────────────────────────────────────────────────
holdsAt(F,T) :- time(T), time(S), S<T, happens(E,S), initiates(E,F,S), not clipped(S,F,T).
clipped(S,F,T) :- time(S), time(T), time(R), S<R, R<T, happens(E,R), terminates(E,F,R).
holdsAt(F,T) :- time(T), initially(F), not clipped(0,F,T).

% ── Domain ─────────────────────────────────────────────────────────
time(0). time(1). time(2). time(3). time(4). time(5).
person(alice). person(bob). person(carol).

% ── Causal rules ───────────────────────────────────────────────────
initiates(infect(P),   ill(P), T) :- person(P), time(T).
initiates(contract(P), ill(P), T) :- person(P), time(T).
terminates(recover(P), ill(P), T) :- person(P), time(T).

% ── Background: alice contracts the disease at T=0 (patient zero) ──
% This is fixed background knowledge, NOT part of the learned hypothesis.
% Alice is ill from T=1 onwards (S=0 < T, EC persistence axiom).
happens(contract(alice), 0).

% Alice recovers at T=4; she is not ill at T=5.
happens(recover(alice), 4).

% ── Observations ───────────────────────────────────────────────────
% alice: contracts disease at T=0, ill from T=1
#example holdsAt(ill(alice), 1).
#example holdsAt(ill(alice), 2).
% bob: infected by alice at T=1 (alice ill at T=1), ill from T=2
#example holdsAt(ill(bob),   2).
#example holdsAt(ill(bob),   3).
% carol: infected by bob at T=2 (bob ill at T=2), ill from T=3
#example holdsAt(ill(carol), 3).
% Negative: before infection reaches each person
% These rule out the trivial empty-body hypothesis:
%   happens(infect(bob),V1):- would fire at T=0, making bob ill at T=1.
%   happens(infect(carol),V1):- would fire at T=0/1, making carol ill at T=1/2.
#example not holdsAt(ill(bob),   1).
#example not holdsAt(ill(carol), 2).
% Alice recovers at T=4, not ill at T=5
#example not holdsAt(ill(alice), 5).

% ── Mode declarations ──────────────────────────────────────────────
% '#person' is a ground marker: alice / bob / carol appear literally.
#modeh happens(infect(#person), +time).
#modeb holdsAt(ill(#person), +time).
