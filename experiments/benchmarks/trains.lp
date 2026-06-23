% =====================================================================
% Benchmark: Michalski's Trains (simplified, 1969)
% =====================================================================
% The most cited ILP benchmark. Six trains travel east or west.
% Task: learn what makes a train eastbound from car properties.
%
% Expected hypothesis:
%   eastbound(V1) :- has_car(V1, V2), short(V2), triangle_load(V2).
% =====================================================================

% Trains
train(t1). train(t2). train(t3).
train(t4). train(t5). train(t6).

% Cars (each train has two)
has_car(t1,c11). has_car(t1,c12).
has_car(t2,c21). has_car(t2,c22).
has_car(t3,c31). has_car(t3,c32).
has_car(t4,c41). has_car(t4,c42).
has_car(t5,c51). has_car(t5,c52).
has_car(t6,c61). has_car(t6,c62).
car(C) :- has_car(_, C).

% Length
short(c11). short(c21). short(c31). short(c42). short(c61).
long(c12).  long(c22).  long(c32).  long(c41).  long(c51). long(c52). long(c62).

% Shape
rectangle(c11). rectangle(c21). rectangle(c31). rectangle(c42). rectangle(c52).
ellipse(c12).   ellipse(c22).   ellipse(c32).   ellipse(c41).
ellipse(c51).   ellipse(c61).   ellipse(c62).

% Load
triangle_load(c11). triangle_load(c21). triangle_load(c31). triangle_load(c51).
circle_load(c12).   circle_load(c22).   circle_load(c32).
circle_load(c41).   circle_load(c42).   circle_load(c52).
circle_load(c61).   circle_load(c62).

% Mode declarations
% '+train' / '+car' = input variable   '-car' = newly introduced variable
#modeh eastbound(+train).
#modeb has_car(+train, -car).
#modeb short(+car).
#modeb triangle_load(+car).
#modeb rectangle(+car).

% Examples
#example eastbound(t1).
#example eastbound(t2).
#example eastbound(t3).
#example not eastbound(t4).
#example not eastbound(t5).
#example not eastbound(t6).
