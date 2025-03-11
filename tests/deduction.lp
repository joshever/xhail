%% PENGUINS.lp
%%%%%%%%%%%%%%

#modeh flies(+bird).

#modeb penguin(+bird).
#modeb not penguin(+bird).
#modeb creates(+bird, +bird, -bird).
#modeb not creates(-bird, -bird, +bird).

#example flies(c).
#example flies(e).
#example flies(f).
#example not flies(d).
#example not flies(a).
#example not flies(b).

penguin(a).
penguin(b).
bird(c).
bird(e).
bird(f).
bird(X) :- penguin(X).
penguin(Z) :- creates(X, Y, Z), penguin(X), penguin(Y).
creates(a, b, d).

% flies(X) :- bird(X), not penguin(X).