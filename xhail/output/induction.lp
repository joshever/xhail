#show use/2.
%BACKGROUND%
p(X) :- q(X,1), q(X,2).
p(X) :- r(X).
s(a).
s(b).
s2(b).
t(1).
t(2).

%EXAMPLES%
%#maximize{50@1 : not p(a)}.
:- p(a).
%#maximize{100@1 : p(b)}.
:- not p(b).


{ use(V1, 0) } :- clause(V1).
clause(0).

#minimize{ 1@2 : use(0,0) }.

q(V1,V2) :- use(0, 0), s2(V1), t(V2).

