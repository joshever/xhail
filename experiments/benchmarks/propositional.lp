% ============================================================
% Benchmark: Propositional (0-arity)
% ============================================================
% Task: learn the minimal rule that covers the positive example
%       using only propositional (0-arity) facts.
%
% Expected hypothesis:  output.
%
% With a single positive example and no negative examples,
% XHAIL's minimization principle (Occam's razor) returns the
% simplest consistent rule: the unconditional fact output.
%
% To force body conditions you need negative examples in worlds
% where the inputs differ — which requires first-order predicates.
%
% This benchmark exercises the 0-arity code path.
% ============================================================

% Background knowledge
input_a.
input_b.

% Mode declarations (0-arity — no type variables)
#modeh output.
#modeb input_a.
#modeb input_b.

% Examples
#example output.
