bird(a).
bird(b).
penguin(c).
bird(X) :- penguin(X).

#example flies(a).
#example flies(b).
#example not flies(c).

#modeh flies(+bird) :1 ~ 2.
#modeb penguin(+bird).
#modeb not penguin(+bird).