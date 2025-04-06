p(X) :- q(X, 1), q(X, 2).

p(X) :- r(X).

s(a). 
s(b). 
s2(b).

t(1). 
t(2).

#modeh r(+s) =0.

#modeh q(+s2, +t) =0.

#example not p(a)=50.

#example p(b)=100.