% =====================================================================
% Benchmark: Grandfather (genealogy chain)
% =====================================================================
% Classic ILP example demonstrating chain reasoning with a
% newly-introduced intermediate variable ('-' marker).
%
% Expected hypothesis:
%   grandfather(V1, V2) :- father(V1, V3), parent(V3, V2).
% =====================================================================

% Family members
male(tom). male(bob). male(jim).
female(liz). female(ann). female(pat).

person(X) :- male(X).
person(X) :- female(X).

% Relationships
parent(tom, bob). parent(tom, liz).
parent(bob, ann). parent(bob, pat).
parent(ann, jim).

father(X, Y) :- parent(X, Y), male(X).

% Mode declarations
% '+' = input variable (must already be known)
% '-' = output variable (newly introduced — enables chaining)
#modeh grandfather(+person, +person).
#modeb father(+person, -person).
#modeb parent(+person, +person).

% Examples
#example grandfather(tom, ann).
#example grandfather(tom, pat).
#example grandfather(bob, jim).
#example not grandfather(tom, bob).
#example not grandfather(tom, liz).
#example not grandfather(bob, ann).
#example not grandfather(ann, jim).
