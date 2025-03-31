%% PENGUINS.lp
%%%%%%%%%%%%%%

bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

#modeh flies(+bird).
#modeb penguin(+bird).
#modeb not penguin(+bird).

#example flies(a) =5 @3.
#example flies(b).
#example flies(c).
#example not flies(d).