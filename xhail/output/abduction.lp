%BACKGROUND%
p(X) :- q(X,1), q(X,2).
p(X) :- r(X).
s(a).
s(b).
s2(b).
t(1).
t(2).

%NEGATIONS%

%EXAMPLES%
%#maximize{50@1 : not p(a)}.
:- p(a).
%#maximize{100@1 : p(b)}.
:- not p(b).

%ABDUCIBLES%
0 { abduced_r(V1):s(V1) } 1000000.
#minimize{0@1,V1: abduced_r(V1),s(V1)}.
r(V1) :- abduced_r(V1),s(V1).
0 { abduced_q(V1,V2):s2(V1), t(V2) } 1000000.
#minimize{0@1,V1, V2: abduced_q(V1,V2),s2(V1), t(V2)}.
q(V1,V2) :- abduced_q(V1,V2),s2(V1), t(V2).

