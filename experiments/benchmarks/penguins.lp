% ============================================================
% Benchmark: Penguins (flies / does not fly)
% ============================================================
% Classic ILP task: learn that birds fly unless they are penguins.
% Expected hypothesis:  flies(V1) :- not penguin(V1).
%
% Source: standard ILP teaching example; see also Ray (2009).
% ============================================================

% Background knowledge
bird(a). bird(b). bird(c).
penguin(d).
bird(X) :- penguin(X).

% Mode declarations
#modeh flies(+bird).
#modeb penguin(+bird).
#modeb not penguin(+bird).

% Examples
#example flies(a).
#example flies(b).
#example flies(c).
#example not flies(d).
