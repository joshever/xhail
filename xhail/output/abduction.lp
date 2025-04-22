%ORIGINAL BACKGROUND%
car(car1).
car(car2).
car(car3).
car(car4).
car(car5).
light(a).
light(b).
light(c).
red(a).
emergency(car4).
emergency(car5).
atlight(car1,a).
atlight(car2,b).
atlight(car3,c).
atlight(car4,a).

%TEMPORARY NEGATIONS%
not_red(V1) :- not red(V1), light(V1).

%EXAMPLES%
%#example drive(car2)
%#maximize{1@1 : drive(car2)}.
:- not drive(car2).
%#example drive(car3)
%#maximize{1@1 : drive(car3)}.
:- not drive(car3).
%#example not drive(car1)
%#maximize{1@1 : not drive(car1)}.
:- drive(car1).
%#example drive(car4)
%#maximize{1@1 : drive(car4)}.
:- not drive(car4).
%#example drive(car5)
%#maximize{1@1 : drive(car5)}.
:- not drive(car5).

%ABDUCIBLES%
%#modeh drive(+car)
0 { abduced_drive(V1):car(V1) } 1000000.
#minimize{1@1,V1: abduced_drive(V1),car(V1)}.
drive(V1) :- abduced_drive(V1),car(V1).

