%% PENGUINS.lp
%%%%%%%%%%%%%%

bird(a).
bird(b).
food(chocolate). %fluid
food(vegetables). %fluid

penguin(d). %type bird
penguin(c).
bird(X) :- penguin(X).

#modeh flies(+bird, #food).
#modeb penguin(+bird).
#modeb not penguin(+bird).

#example flies(a, chocolate).
#example flies(b, vegetables).
#example flies(c, vegetables).
#example not flies(d, chocolate).

%flies(+bird, chocolate) :- not penguin(+bird).
%flies(+bird, vegetables).