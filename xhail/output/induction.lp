#show use/2.
%BACKGROUND%
car(car1).
car(car2).
car(car3).
light(a).
light(b).
light(c).
red(a).
amber(b).
green(c).
atlight(car1,a).
atlight(car2,b).
atlight(car3,c).

%NEGATIONS%
not_atlight(V1,V2) :- not atlight(V1,V2), car(V1), light(V2).
not_red(V1) :- not red(V1), light(V1).

%EXAMPLES%
#maximize{1@1 : drive(car1,a)}.
:- not drive(car1,a).
#maximize{1@1 : drive(car2,b)}.
:- not drive(car2,b).
#maximize{1@1 : not drive(car3,c)}.
:- drive(car3,c).

%ABDUCIBLES%
0 { abduced_drive(V1,V2) : car(V1), light(V2) } 1000000.
#minimize{1@2, V1, V2: abduced_drive(V1,V2), car(V1), light(V2)}.
drive(V1,V2) :- abduced_drive(V1,V2), car(V1), light(V2).


{ use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).



