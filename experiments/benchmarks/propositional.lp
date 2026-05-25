% ============================================================
% Benchmark: Propositional Circuit (0-arity)
% ============================================================
% Task: learn that output is true when both inputs are active
%       (logical AND), using only propositional facts (no variables).
%
% Expected hypothesis:  output :- input_a, input_b.
%
% This benchmark specifically exercises the 0-arity (propositional)
% code path that was previously broken by a trailing-comma bug in
% the induction phase (fixed in Phase 3).
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
