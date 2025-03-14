%% PENGUINS.lp
%%%%%%%%%%%%%%

#modeh flies(+bird).
#modeb not penguin(+bird).
#modeb creates(-bird, -bird, +bird).

#example flies(a).
#example flies(b).
#example flies(c).
#example not flies(d).
#example not flies(e).
#example not flies(f).

penguin(d).
penguin(e).
bird(a).
bird(b).
bird(c).
bird(X) :- penguin(X).
penguin(Z) :- creates(X, Y, Z), penguin(X), penguin(Y).
creates(d, e, f).

% flies(X) :- bird(X), not penguin(X).