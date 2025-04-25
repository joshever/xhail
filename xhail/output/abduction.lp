%ORIGINAL BACKGROUND%
p(X) :- q(X,1), q(X,2).
p(X) :- r(X).
s(a).
s(b).
s2(b).
t(1).
t(2).

%TEMPORARY NEGATIONS%

%EXAMPLES%
%#example not p(a)
%#maximize{50@1 : not p(a)}.
:- p(a).
%#example p(b)
%#maximize{100@1 : p(b)}.
:- not p(b).

%ABDUCIBLES%
%#modeh r(+s)
0 { abduced_r(V1):s(V1) } 1000000.
#minimize{1@1,V1: abduced_r(V1),s(V1)}.
r(V1) :- abduced_r(V1),s(V1).
%#modeh q(+s2,+t)
0 { abduced_q(V1,V2):s2(V1), t(V2) } 1000000.
#minimize{1@0,V1, V2: abduced_q(V1,V2),s2(V1), t(V2)}.
q(V1,V2) :- abduced_q(V1,V2),s2(V1), t(V2).

