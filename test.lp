%% PENGUINS.lp
%%%%%%%%%%%%%%

bird(X) :- penguin(X).
bird(a).
bird(b).
bird(c).
penguin(d).

#modeh flies(+bird) :1~10 =4 @2.
#modeb penguin(+bird) :2 =5 @2.
#modeb not penguin(+bird) :2.

#example flies(a) =5 @3.
#example flies(b).
#example flies(c).
#example not flies(d).