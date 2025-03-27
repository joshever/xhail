%BACKGROUND%
car(car1).
car(car2).
car(car3).
car(car4).
light(a).
light(b).
light(c).
red(a).
amber(b).
green(c).
atlight(car1,a).
atlight(car2,b).
atlight(car3,c).
atlight(car4,a).
emergency(car4).

%NEGATIONS%
not_atlight(V1,V2) :- not atlight(V1,V2), car(V1), light(V2).
not_red(V1) :- not red(V1), light(V1).
not_emergency(V1) :- not emergency(V1), car(V1).

%EXAMPLES%
#maximize{1@1 : drive(car3)}.
:- not drive(car3).
#maximize{1@1 : drive(car2)}.
:- not drive(car2).
#maximize{1@1 : drive(car4)}.
:- not drive(car4).
#maximize{1@1 : not drive(car1)}.
:- drive(car1).

%ABDUCIBLES%
0 { abduced_drive(V1) : car(V1) } 1000000.
#minimize{1@2, V1: abduced_drive(V1), car(V1)}.
drive(V1) :- abduced_drive(V1), car(V1).

