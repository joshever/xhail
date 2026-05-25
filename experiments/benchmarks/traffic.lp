% ============================================================
% Benchmark: Traffic Light (stop)
% ============================================================
% Task: learn that a car must stop when the light is red.
% Expected hypothesis:  stop(V1) :- red(V1).
%
% A minimal real-world classification rule.  Note: XHAIL currently
% handles a single #modeh predicate per run; multi-head tasks (e.g.
% also learning "go :- green") are a known limitation and are tracked
% as a future extension (see XHAIL_AUDIT_AND_ROADMAP.md).
% ============================================================

% Background knowledge
red(light1).
red(light3).
green(light2).
green(light4).

% Mode declarations — single head predicate
#modeh stop(+light).
#modeb red(+light).
#modeb green(+light).

% Type declarations
light(light1). light(light2). light(light3). light(light4).

% Examples
#example stop(light1).
#example stop(light3).
#example not stop(light2).
#example not stop(light4).
