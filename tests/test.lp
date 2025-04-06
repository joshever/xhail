%% PENGUINS.lp
%%%%%%%%%%%%%%

bird(a).
bird(b).
food(chocolate). %fluid
food(vegetables). %fluid
penguin(d). %type bird
penguin(c).
bird(X) :- penguin(X).

#modeh flies(+bird, eat($food)).
#modeb penguin(+bird).
#modeb not penguin(+bird).

#example flies(a, eat(chocolate)).
#example flies(b, eat(vegetables)).
#example flies(c, eat(vegetables)).
#example not flies(d, eat(chocolate)).

%flies(+bird, chocolate) :- not penguin(+bird).
%flies(+bird, vegetables).
