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


1 { use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).
literal(0, 2).
literal(0, 3).
literal(0, 4).
literal(0, 5).
literal(0, 6).
literal(0, 7).
literal(0, 8).
literal(0, 9).
literal(0, 10).
clause(1).
literal(1, 1).
literal(1, 2).
literal(1, 3).
literal(1, 4).
literal(1, 5).
literal(1, 6).
literal(1, 7).
literal(1, 8).
literal(1, 9).
literal(1, 10).
clause(2).
literal(2, 1).
literal(2, 2).
literal(2, 3).
literal(2, 4).
literal(2, 5).
literal(2, 6).
literal(2, 7).
literal(2, 8).
literal(2, 9).
literal(2, 10).

#minimize{ 1@2 : use(0,0) }.
#minimize{ 1@2 : use(0,1) }.
#minimize{ 1@2 : use(0,2) }.
#minimize{ 1@2 : use(0,3) }.
#minimize{ 1@2 : use(0,4) }.
#minimize{ 1@2 : use(0,5) }.
#minimize{ 1@2 : use(0,6) }.
#minimize{ 1@2 : use(0,7) }.
#minimize{ 1@2 : use(0,8) }.
#minimize{ 1@2 : use(0,9) }.
#minimize{ 1@2 : use(0,10) }.
#minimize{ 1@2 : use(1,0) }.
#minimize{ 1@2 : use(1,1) }.
#minimize{ 1@2 : use(1,2) }.
#minimize{ 1@2 : use(1,3) }.
#minimize{ 1@2 : use(1,4) }.
#minimize{ 1@2 : use(1,5) }.
#minimize{ 1@2 : use(1,6) }.
#minimize{ 1@2 : use(1,7) }.
#minimize{ 1@2 : use(1,8) }.
#minimize{ 1@2 : use(1,9) }.
#minimize{ 1@2 : use(1,10) }.
#minimize{ 1@2 : use(2,0) }.
#minimize{ 1@2 : use(2,1) }.
#minimize{ 1@2 : use(2,2) }.
#minimize{ 1@2 : use(2,3) }.
#minimize{ 1@2 : use(2,4) }.
#minimize{ 1@2 : use(2,5) }.
#minimize{ 1@2 : use(2,6) }.
#minimize{ 1@2 : use(2,7) }.
#minimize{ 1@2 : use(2,8) }.
#minimize{ 1@2 : use(2,9) }.
#minimize{ 1@2 : use(2,10) }.

try(0, 1, V1, V2) :- use(0, 1), atlight(V1,V2), car(V1), light(V2).
try(0, 1, V1, V2) :- not use(0, 1), car(V1), light(V2).
try(0, 2, V2) :- use(0, 2), not red(V2), light(V2).
try(0, 2, V2) :- not use(0, 2), light(V2).
try(0, 3, V1, V2) :- use(0, 3), atlight(V1,V2), car(V1), light(V2).
try(0, 3, V1, V2) :- not use(0, 3), car(V1), light(V2).
try(0, 4, V2) :- use(0, 4), not red(V2), light(V2).
try(0, 4, V2) :- not use(0, 4), light(V2).
try(0, 5, V1, V2) :- use(0, 5), atlight(V1,V2), car(V1), light(V2).
try(0, 5, V1, V2) :- not use(0, 5), car(V1), light(V2).
try(0, 6, V2) :- use(0, 6), not red(V2), light(V2).
try(0, 6, V2) :- not use(0, 6), light(V2).
try(0, 7, V1, V2) :- use(0, 7), atlight(V1,V2), car(V1), light(V2).
try(0, 7, V1, V2) :- not use(0, 7), car(V1), light(V2).
try(0, 8, V2) :- use(0, 8), not red(V2), light(V2).
try(0, 8, V2) :- not use(0, 8), light(V2).
try(0, 9, V1, V2) :- use(0, 9), atlight(V1,V2), car(V1), light(V2).
try(0, 9, V1, V2) :- not use(0, 9), car(V1), light(V2).
try(0, 10, V2) :- use(0, 10), not red(V2), light(V2).
try(0, 10, V2) :- not use(0, 10), light(V2).
try(1, 1, V1, V2) :- use(1, 1), atlight(V1,V2), car(V1), light(V2).
try(1, 1, V1, V2) :- not use(1, 1), car(V1), light(V2).
try(1, 2, V1) :- use(1, 2), emergency(V1), car(V1).
try(1, 2, V1) :- not use(1, 2), car(V1).
try(1, 3, V1, V2) :- use(1, 3), atlight(V1,V2), car(V1), light(V2).
try(1, 3, V1, V2) :- not use(1, 3), car(V1), light(V2).
try(1, 4, V1) :- use(1, 4), emergency(V1), car(V1).
try(1, 4, V1) :- not use(1, 4), car(V1).
try(1, 5, V1, V2) :- use(1, 5), atlight(V1,V2), car(V1), light(V2).
try(1, 5, V1, V2) :- not use(1, 5), car(V1), light(V2).
try(1, 6, V1) :- use(1, 6), emergency(V1), car(V1).
try(1, 6, V1) :- not use(1, 6), car(V1).
try(1, 7, V1, V2) :- use(1, 7), atlight(V1,V2), car(V1), light(V2).
try(1, 7, V1, V2) :- not use(1, 7), car(V1), light(V2).
try(1, 8, V1) :- use(1, 8), emergency(V1), car(V1).
try(1, 8, V1) :- not use(1, 8), car(V1).
try(1, 9, V1, V2) :- use(1, 9), atlight(V1,V2), car(V1), light(V2).
try(1, 9, V1, V2) :- not use(1, 9), car(V1), light(V2).
try(1, 10, V1) :- use(1, 10), emergency(V1), car(V1).
try(1, 10, V1) :- not use(1, 10), car(V1).
try(2, 1, V1) :- use(2, 1), emergency(V1), car(V1).
try(2, 1, V1) :- not use(2, 1), car(V1).
try(2, 2, V1, V2) :- use(2, 2), atlight(V1,V2), car(V1), light(V2).
try(2, 2, V1, V2) :- not use(2, 2), car(V1), light(V2).
try(2, 3, V1) :- use(2, 3), emergency(V1), car(V1).
try(2, 3, V1) :- not use(2, 3), car(V1).
try(2, 4, V1, V2) :- use(2, 4), atlight(V1,V2), car(V1), light(V2).
try(2, 4, V1, V2) :- not use(2, 4), car(V1), light(V2).
try(2, 5, V1) :- use(2, 5), emergency(V1), car(V1).
try(2, 5, V1) :- not use(2, 5), car(V1).
try(2, 6, V1, V2) :- use(2, 6), atlight(V1,V2), car(V1), light(V2).
try(2, 6, V1, V2) :- not use(2, 6), car(V1), light(V2).
try(2, 7, V1) :- use(2, 7), emergency(V1), car(V1).
try(2, 7, V1) :- not use(2, 7), car(V1).
try(2, 8, V1, V2) :- use(2, 8), atlight(V1,V2), car(V1), light(V2).
try(2, 8, V1, V2) :- not use(2, 8), car(V1), light(V2).
try(2, 9, V1) :- use(2, 9), emergency(V1), car(V1).
try(2, 9, V1) :- not use(2, 9), car(V1).
try(2, 10, V1, V2) :- use(2, 10), atlight(V1,V2), car(V1), light(V2).
try(2, 10, V1, V2) :- not use(2, 10), car(V1), light(V2).
drive(V1) :- use(0, 0), try(0, 1, V1, V2), try(0, 2, V2), try(0, 3, V1, V2), try(0, 4, V2), try(0, 5, V1, V2), try(0, 6, V2), try(0, 7, V1, V2), try(0, 8, V2), try(0, 9, V1, V2), try(0, 10, V2), car(V1), light(V2).
drive(V1) :- use(1, 0), try(1, 1, V1, V2), try(1, 2, V1), try(1, 3, V1, V2), try(1, 4, V1), try(1, 5, V1, V2), try(1, 6, V1), try(1, 7, V1, V2), try(1, 8, V1), try(1, 9, V1, V2), try(1, 10, V1), car(V1), light(V2).
drive(V1) :- use(2, 0), try(2, 1, V1), try(2, 2, V1, V2), try(2, 3, V1), try(2, 4, V1, V2), try(2, 5, V1), try(2, 6, V1, V2), try(2, 7, V1), try(2, 8, V1, V2), try(2, 9, V1), try(2, 10, V1, V2), car(V1), light(V2).

:- level(X, Y), not level(X, 0).
level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
level(0,2) :- use(0,2).
level(0,3) :- use(0,3).
level(0,4) :- use(0,4).
level(0,5) :- use(0,5).
level(0,6) :- use(0,6).
level(0,7) :- use(0,7).
level(0,8) :- use(0,8).
level(0,9) :- use(0,9).
level(0,10) :- use(0,10).
level(1,0) :- use(1,0).
level(1,1) :- use(1,1).
level(1,2) :- use(1,2).
level(1,3) :- use(1,3).
level(1,4) :- use(1,4).
level(1,5) :- use(1,5).
level(1,6) :- use(1,6).
level(1,7) :- use(1,7).
level(1,8) :- use(1,8).
level(1,9) :- use(1,9).
level(1,10) :- use(1,10).
level(2,0) :- use(2,0).
level(2,1) :- use(2,1).
level(2,2) :- use(2,2).
level(2,3) :- use(2,3).
level(2,4) :- use(2,4).
level(2,5) :- use(2,5).
level(2,6) :- use(2,6).
level(2,7) :- use(2,7).
level(2,8) :- use(2,8).
level(2,9) :- use(2,9).
level(2,10) :- use(2,10).
