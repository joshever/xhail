% ============================================================
% Benchmark: Animal Classification (mammal)
% ============================================================
% Task: learn that an animal is a mammal if it has hair and
%       produces milk (characteristic features of Mammalia).
% Expected hypothesis (one or both rules):
%   mammal(V1) :- has_hair(V1).
%   mammal(V1) :- produces_milk(V1).
%
% This benchmark tests multi-body conjunction and feature-based
% classification — a step up from penguins in that two independent
% body predicates can each justify the head.
% ============================================================

% Background knowledge
has_hair(dog).   produces_milk(dog).
has_hair(cat).   produces_milk(cat).
has_hair(bat).   produces_milk(bat).
has_hair(whale). produces_milk(whale).

% Non-mammals (used in negative examples)
lays_eggs(eagle).
lays_eggs(salmon).
cold_blooded(salmon).

% Mode declarations
#modeh mammal(+animal).
#modeb has_hair(+animal).
#modeb produces_milk(+animal).

% Type declarations
animal(dog). animal(cat). animal(bat). animal(whale).
animal(eagle). animal(salmon).

% Examples — positive
#example mammal(dog).
#example mammal(cat).
#example mammal(bat).
#example mammal(whale).

% Examples — negative
#example not mammal(eagle).
#example not mammal(salmon).
