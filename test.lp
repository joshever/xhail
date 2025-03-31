%% PENGUINS.lp
%%%%%%%%%%%%%%

bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

#modeh flies(+bird) {w=5, p=2}.
#modeb penguin(+bird).
#modeb not penguin(+bird).

#example flies(a).
#example flies(b).
#example flies(c).
#example not flies(d).