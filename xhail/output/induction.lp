#show use/2.
%BACKGROUND%
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

%EXAMPLES%
%#maximize{1@1 : drive(car2)}.
:- not drive(car2).
%#maximize{1@1 : drive(car3)}.
:- not drive(car3).
%#maximize{1@1 : not drive(car1)}.
:- drive(car1).
%#maximize{1@1 : drive(car4)}.
:- not drive(car4).
%#maximize{1@1 : drive(car5)}.
:- not drive(car5).


{ use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).
literal(0, 2).
clause(1).
literal(1, 1).
literal(1, 2).
clause(2).
literal(2, 1).
literal(2, 2).

#minimize{ 1@2 : use(0,0) }.
#minimize{ 1@2 : use(0,1) }.
#minimize{ 1@2 : use(0,2) }.
#minimize{ 1@2 : use(1,0) }.
#minimize{ 1@2 : use(1,1) }.
#minimize{ 1@2 : use(1,2) }.
#minimize{ 1@2 : use(2,0) }.
#minimize{ 1@2 : use(2,1) }.
#minimize{ 1@2 : use(2,2) }.

try(0, 1, V1, V2) :- use(0, 1), atlight(V1,V2), car(V1), light(V2).
try(0, 1, V1, V2) :- not use(0, 1), car(V1), light(V2).
try(0, 2, V2) :- use(0, 2), not red(V2), light(V2).
try(0, 2, V2) :- not use(0, 2), light(V2).
try(1, 1, V1, V2) :- use(1, 1), atlight(V1,V2), car(V1), light(V2).
try(1, 1, V1, V2) :- not use(1, 1), car(V1), light(V2).
try(1, 2, V1) :- use(1, 2), emergency(V1), car(V1).
try(1, 2, V1) :- not use(1, 2), car(V1).
try(2, 1, V1) :- use(2, 1), emergency(V1), car(V1).
try(2, 1, V1) :- not use(2, 1), car(V1).
try(2, 2, V1, V2) :- use(2, 2), atlight(V1,V2), car(V1), light(V2).
try(2, 2, V1, V2) :- not use(2, 2), car(V1), light(V2).
drive(V1) :- use(0, 0), try(0, 1, V1, V2), try(0, 2, V2), car(V1), light(V2).
drive(V1) :- use(1, 0), try(1, 1, V1, V2), try(1, 2, V1), car(V1), light(V2).
drive(V1) :- use(2, 0), try(2, 1, V1), try(2, 2, V1, V2), car(V1), light(V2).

:- level(X, Y), not level(X, 0).
level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
level(0,2) :- use(0,2).
level(1,0) :- use(1,0).
level(1,1) :- use(1,1).
level(1,2) :- use(1,2).
level(2,0) :- use(2,0).
level(2,1) :- use(2,1).
level(2,2) :- use(2,2).
