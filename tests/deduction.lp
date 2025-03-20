%% PENGUINS.lp
%%%%%%%%%%%%%%

#modeh flies(+bird).
#modeb not penguin(+bird).
#modeb penguin(+bird).
#modeb creates(+bird, +bird, -bird).
#modeb not creates(+bird, +bird, -bird).

#example flies(d).
#example flies(e).
#example flies(f).
#example not flies(c).

bird(a).
bird(b).
bird(c).
bird(d).
bird(e).
bird(f).


bird(X) :- penguin(X).
penguin(Z) :- creates(X, Y, Z), penguin(X), penguin(Y).
creates(d, e, f).
penguin(a).
penguin(b).

% flies(X) :- bird(X), not penguin(X).





#modeh penguin(+bird).

#modeb penguin(+bird).

#modeb not penguin(+bird).
#modeb creates(+bird, +bird, -bird).
#modeb not creates(+bird, +bird, -bird).

bird(a).
bird(b).
bird(c).


penguin(a).
penguin(b).
penguin(c).
creates(a, b, c).
