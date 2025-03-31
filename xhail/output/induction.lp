#show use/2.
%BACKGROUND%
player(a).
player(b).
player(c).
player(d).
location(l00).
location(l01).
location(l10).
location(l11).
nextTo(l00,l01).
nextTo(l00,l10).
nextTo(l01,l11).
nextTo(l10,l11).
playerAt(a,l00).
playerAt(b,l01).
playerAt(c,l10).
playerAt(d,l11).

%EXAMPLES%
%#maximize{1@1 : not wins(a,b)}.
:- wins(a,b).
%#maximize{1@1 : not wins(c,d)}.
:- wins(c,d).
%#maximize{1@1 : not wins(a,c)}.
:- wins(a,c).
%#maximize{1@1 : not wins(b,d)}.
:- wins(b,d).
%#maximize{1@1 : wins(a,d)}.
:- not wins(a,d).
%#maximize{1@1 : wins(b,c)}.
:- not wins(b,c).


{ use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).
literal(0, 2).
literal(0, 3).
literal(0, 4).
clause(1).
literal(1, 1).
literal(1, 2).
literal(1, 3).
literal(1, 4).
clause(2).
literal(2, 1).
literal(2, 2).
literal(2, 3).
literal(2, 4).
clause(3).
literal(3, 1).
literal(3, 2).
literal(3, 3).
literal(3, 4).
clause(4).
literal(4, 1).
literal(4, 2).
literal(4, 3).
literal(4, 4).
clause(5).
literal(5, 1).
literal(5, 2).
literal(5, 3).
literal(5, 4).
clause(6).
literal(6, 1).
literal(6, 2).
literal(6, 3).
literal(6, 4).
clause(7).
literal(7, 1).
literal(7, 2).
literal(7, 3).
literal(7, 4).
clause(8).
literal(8, 1).
literal(8, 2).
literal(8, 3).
literal(8, 4).
clause(9).
literal(9, 1).
literal(9, 2).
literal(9, 3).
literal(9, 4).
clause(10).
literal(10, 1).
literal(10, 2).
literal(10, 3).
literal(10, 4).
clause(11).
literal(11, 1).
literal(11, 2).
literal(11, 3).
literal(11, 4).
clause(12).
literal(12, 1).
literal(12, 2).
literal(12, 3).
literal(12, 4).
clause(13).
literal(13, 1).
literal(13, 2).
literal(13, 3).
literal(13, 4).
clause(14).
literal(14, 1).
literal(14, 2).
literal(14, 3).
literal(14, 4).
clause(15).
literal(15, 1).
literal(15, 2).
literal(15, 3).
literal(15, 4).
clause(16).
literal(16, 1).
literal(16, 2).
literal(16, 3).
literal(16, 4).
clause(17).
literal(17, 1).
literal(17, 2).
literal(17, 3).
literal(17, 4).
clause(18).
literal(18, 1).
literal(18, 2).
literal(18, 3).
literal(18, 4).
clause(19).
literal(19, 1).
literal(19, 2).
literal(19, 3).
literal(19, 4).
clause(20).
literal(20, 1).
literal(20, 2).
literal(20, 3).
literal(20, 4).
clause(21).
literal(21, 1).
literal(21, 2).
literal(21, 3).
literal(21, 4).
clause(22).
literal(22, 1).
literal(22, 2).
literal(22, 3).
literal(22, 4).
clause(23).
literal(23, 1).
literal(23, 2).
literal(23, 3).
literal(23, 4).
clause(24).
literal(24, 1).
literal(24, 2).
literal(24, 3).
literal(24, 4).
clause(25).
literal(25, 1).
literal(25, 2).
literal(25, 3).
literal(25, 4).
clause(26).
literal(26, 1).
literal(26, 2).
literal(26, 3).
literal(26, 4).
clause(27).
literal(27, 1).
literal(27, 2).
literal(27, 3).
literal(27, 4).
clause(28).
literal(28, 1).
literal(28, 2).
literal(28, 3).
literal(28, 4).
clause(29).
literal(29, 1).
literal(29, 2).
literal(29, 3).
literal(29, 4).

#minimize{ 1@2 : use(0,0) }.
#minimize{ 1@2 : use(0,1) }.
#minimize{ 1@2 : use(0,2) }.
#minimize{ 1@2 : use(0,3) }.
#minimize{ 1@2 : use(0,4) }.
#minimize{ 1@2 : use(1,0) }.
#minimize{ 1@2 : use(1,1) }.
#minimize{ 1@2 : use(1,2) }.
#minimize{ 1@2 : use(1,3) }.
#minimize{ 1@2 : use(1,4) }.
#minimize{ 1@2 : use(2,0) }.
#minimize{ 1@2 : use(2,1) }.
#minimize{ 1@2 : use(2,2) }.
#minimize{ 1@2 : use(2,3) }.
#minimize{ 1@2 : use(2,4) }.
#minimize{ 1@2 : use(3,0) }.
#minimize{ 1@2 : use(3,1) }.
#minimize{ 1@2 : use(3,2) }.
#minimize{ 1@2 : use(3,3) }.
#minimize{ 1@2 : use(3,4) }.
#minimize{ 1@2 : use(4,0) }.
#minimize{ 1@2 : use(4,1) }.
#minimize{ 1@2 : use(4,2) }.
#minimize{ 1@2 : use(4,3) }.
#minimize{ 1@2 : use(4,4) }.
#minimize{ 1@2 : use(5,0) }.
#minimize{ 1@2 : use(5,1) }.
#minimize{ 1@2 : use(5,2) }.
#minimize{ 1@2 : use(5,3) }.
#minimize{ 1@2 : use(5,4) }.
#minimize{ 1@2 : use(6,0) }.
#minimize{ 1@2 : use(6,1) }.
#minimize{ 1@2 : use(6,2) }.
#minimize{ 1@2 : use(6,3) }.
#minimize{ 1@2 : use(6,4) }.
#minimize{ 1@2 : use(7,0) }.
#minimize{ 1@2 : use(7,1) }.
#minimize{ 1@2 : use(7,2) }.
#minimize{ 1@2 : use(7,3) }.
#minimize{ 1@2 : use(7,4) }.
#minimize{ 1@2 : use(8,0) }.
#minimize{ 1@2 : use(8,1) }.
#minimize{ 1@2 : use(8,2) }.
#minimize{ 1@2 : use(8,3) }.
#minimize{ 1@2 : use(8,4) }.
#minimize{ 1@2 : use(9,0) }.
#minimize{ 1@2 : use(9,1) }.
#minimize{ 1@2 : use(9,2) }.
#minimize{ 1@2 : use(9,3) }.
#minimize{ 1@2 : use(9,4) }.
#minimize{ 1@2 : use(10,0) }.
#minimize{ 1@2 : use(10,1) }.
#minimize{ 1@2 : use(10,2) }.
#minimize{ 1@2 : use(10,3) }.
#minimize{ 1@2 : use(10,4) }.
#minimize{ 1@2 : use(11,0) }.
#minimize{ 1@2 : use(11,1) }.
#minimize{ 1@2 : use(11,2) }.
#minimize{ 1@2 : use(11,3) }.
#minimize{ 1@2 : use(11,4) }.
#minimize{ 1@2 : use(12,0) }.
#minimize{ 1@2 : use(12,1) }.
#minimize{ 1@2 : use(12,2) }.
#minimize{ 1@2 : use(12,3) }.
#minimize{ 1@2 : use(12,4) }.
#minimize{ 1@2 : use(13,0) }.
#minimize{ 1@2 : use(13,1) }.
#minimize{ 1@2 : use(13,2) }.
#minimize{ 1@2 : use(13,3) }.
#minimize{ 1@2 : use(13,4) }.
#minimize{ 1@2 : use(14,0) }.
#minimize{ 1@2 : use(14,1) }.
#minimize{ 1@2 : use(14,2) }.
#minimize{ 1@2 : use(14,3) }.
#minimize{ 1@2 : use(14,4) }.
#minimize{ 1@2 : use(15,0) }.
#minimize{ 1@2 : use(15,1) }.
#minimize{ 1@2 : use(15,2) }.
#minimize{ 1@2 : use(15,3) }.
#minimize{ 1@2 : use(15,4) }.
#minimize{ 1@2 : use(16,0) }.
#minimize{ 1@2 : use(16,1) }.
#minimize{ 1@2 : use(16,2) }.
#minimize{ 1@2 : use(16,3) }.
#minimize{ 1@2 : use(16,4) }.
#minimize{ 1@2 : use(17,0) }.
#minimize{ 1@2 : use(17,1) }.
#minimize{ 1@2 : use(17,2) }.
#minimize{ 1@2 : use(17,3) }.
#minimize{ 1@2 : use(17,4) }.
#minimize{ 1@2 : use(18,0) }.
#minimize{ 1@2 : use(18,1) }.
#minimize{ 1@2 : use(18,2) }.
#minimize{ 1@2 : use(18,3) }.
#minimize{ 1@2 : use(18,4) }.
#minimize{ 1@2 : use(19,0) }.
#minimize{ 1@2 : use(19,1) }.
#minimize{ 1@2 : use(19,2) }.
#minimize{ 1@2 : use(19,3) }.
#minimize{ 1@2 : use(19,4) }.
#minimize{ 1@2 : use(20,0) }.
#minimize{ 1@2 : use(20,1) }.
#minimize{ 1@2 : use(20,2) }.
#minimize{ 1@2 : use(20,3) }.
#minimize{ 1@2 : use(20,4) }.
#minimize{ 1@2 : use(21,0) }.
#minimize{ 1@2 : use(21,1) }.
#minimize{ 1@2 : use(21,2) }.
#minimize{ 1@2 : use(21,3) }.
#minimize{ 1@2 : use(21,4) }.
#minimize{ 1@2 : use(22,0) }.
#minimize{ 1@2 : use(22,1) }.
#minimize{ 1@2 : use(22,2) }.
#minimize{ 1@2 : use(22,3) }.
#minimize{ 1@2 : use(22,4) }.
#minimize{ 1@2 : use(23,0) }.
#minimize{ 1@2 : use(23,1) }.
#minimize{ 1@2 : use(23,2) }.
#minimize{ 1@2 : use(23,3) }.
#minimize{ 1@2 : use(23,4) }.
#minimize{ 1@2 : use(24,0) }.
#minimize{ 1@2 : use(24,1) }.
#minimize{ 1@2 : use(24,2) }.
#minimize{ 1@2 : use(24,3) }.
#minimize{ 1@2 : use(24,4) }.
#minimize{ 1@2 : use(25,0) }.
#minimize{ 1@2 : use(25,1) }.
#minimize{ 1@2 : use(25,2) }.
#minimize{ 1@2 : use(25,3) }.
#minimize{ 1@2 : use(25,4) }.
#minimize{ 1@2 : use(26,0) }.
#minimize{ 1@2 : use(26,1) }.
#minimize{ 1@2 : use(26,2) }.
#minimize{ 1@2 : use(26,3) }.
#minimize{ 1@2 : use(26,4) }.
#minimize{ 1@2 : use(27,0) }.
#minimize{ 1@2 : use(27,1) }.
#minimize{ 1@2 : use(27,2) }.
#minimize{ 1@2 : use(27,3) }.
#minimize{ 1@2 : use(27,4) }.
#minimize{ 1@2 : use(28,0) }.
#minimize{ 1@2 : use(28,1) }.
#minimize{ 1@2 : use(28,2) }.
#minimize{ 1@2 : use(28,3) }.
#minimize{ 1@2 : use(28,4) }.
#minimize{ 1@2 : use(29,0) }.
#minimize{ 1@2 : use(29,1) }.
#minimize{ 1@2 : use(29,2) }.
#minimize{ 1@2 : use(29,3) }.
#minimize{ 1@2 : use(29,4) }.

try(0, 1, V4, V2) :- use(0, 1), playerAt(V4,V2), player(V4), location(V2).
try(0, 1, V4, V2) :- not use(0, 1), player(V4), location(V2).
try(0, 2, V3, V1) :- use(0, 2), playerAt(V3,V1), player(V3), location(V1).
try(0, 2, V3, V1) :- not use(0, 2), player(V3), location(V1).
try(0, 3, V4, V2) :- use(0, 3), playerAt(V4,V2), player(V4), location(V2).
try(0, 3, V4, V2) :- not use(0, 3), player(V4), location(V2).
try(0, 4, V3, V1) :- use(0, 4), playerAt(V3,V1), player(V3), location(V1).
try(0, 4, V3, V1) :- not use(0, 4), player(V3), location(V1).
try(1, 1, V4, V2) :- use(1, 1), playerAt(V4,V2), player(V4), location(V2).
try(1, 1, V4, V2) :- not use(1, 1), player(V4), location(V2).
try(1, 2, V3, V1) :- use(1, 2), playerAt(V3,V1), player(V3), location(V1).
try(1, 2, V3, V1) :- not use(1, 2), player(V3), location(V1).
try(1, 3, V4, V2) :- use(1, 3), playerAt(V4,V2), player(V4), location(V2).
try(1, 3, V4, V2) :- not use(1, 3), player(V4), location(V2).
try(1, 4, V2, V2) :- use(1, 4), not nextTo(V2,V2), location(V2), location(V2).
try(1, 4, V2, V2) :- not use(1, 4), location(V2), location(V2).
try(2, 1, V4, V2) :- use(2, 1), playerAt(V4,V2), player(V4), location(V2).
try(2, 1, V4, V2) :- not use(2, 1), player(V4), location(V2).
try(2, 2, V3, V1) :- use(2, 2), playerAt(V3,V1), player(V3), location(V1).
try(2, 2, V3, V1) :- not use(2, 2), player(V3), location(V1).
try(2, 3, V4, V2) :- use(2, 3), playerAt(V4,V2), player(V4), location(V2).
try(2, 3, V4, V2) :- not use(2, 3), player(V4), location(V2).
try(2, 4, V1, V2) :- use(2, 4), not nextTo(V1,V2), location(V1), location(V2).
try(2, 4, V1, V2) :- not use(2, 4), location(V1), location(V2).
try(3, 1, V4, V2) :- use(3, 1), playerAt(V4,V2), player(V4), location(V2).
try(3, 1, V4, V2) :- not use(3, 1), player(V4), location(V2).
try(3, 2, V3, V1) :- use(3, 2), playerAt(V3,V1), player(V3), location(V1).
try(3, 2, V3, V1) :- not use(3, 2), player(V3), location(V1).
try(3, 3, V4, V2) :- use(3, 3), playerAt(V4,V2), player(V4), location(V2).
try(3, 3, V4, V2) :- not use(3, 3), player(V4), location(V2).
try(3, 4, V2, V1) :- use(3, 4), not nextTo(V2,V1), location(V2), location(V1).
try(3, 4, V2, V1) :- not use(3, 4), location(V2), location(V1).
try(4, 1, V4, V2) :- use(4, 1), playerAt(V4,V2), player(V4), location(V2).
try(4, 1, V4, V2) :- not use(4, 1), player(V4), location(V2).
try(4, 2, V3, V1) :- use(4, 2), playerAt(V3,V1), player(V3), location(V1).
try(4, 2, V3, V1) :- not use(4, 2), player(V3), location(V1).
try(4, 3, V4, V2) :- use(4, 3), playerAt(V4,V2), player(V4), location(V2).
try(4, 3, V4, V2) :- not use(4, 3), player(V4), location(V2).
try(4, 4, V1, V1) :- use(4, 4), not nextTo(V1,V1), location(V1), location(V1).
try(4, 4, V1, V1) :- not use(4, 4), location(V1), location(V1).
try(5, 1, V4, V2) :- use(5, 1), playerAt(V4,V2), player(V4), location(V2).
try(5, 1, V4, V2) :- not use(5, 1), player(V4), location(V2).
try(5, 2, V3, V1) :- use(5, 2), playerAt(V3,V1), player(V3), location(V1).
try(5, 2, V3, V1) :- not use(5, 2), player(V3), location(V1).
try(5, 3, V2, V2) :- use(5, 3), not nextTo(V2,V2), location(V2), location(V2).
try(5, 3, V2, V2) :- not use(5, 3), location(V2), location(V2).
try(5, 4, V4, V2) :- use(5, 4), playerAt(V4,V2), player(V4), location(V2).
try(5, 4, V4, V2) :- not use(5, 4), player(V4), location(V2).
try(6, 1, V4, V2) :- use(6, 1), playerAt(V4,V2), player(V4), location(V2).
try(6, 1, V4, V2) :- not use(6, 1), player(V4), location(V2).
try(6, 2, V3, V1) :- use(6, 2), playerAt(V3,V1), player(V3), location(V1).
try(6, 2, V3, V1) :- not use(6, 2), player(V3), location(V1).
try(6, 3, V2, V2) :- use(6, 3), not nextTo(V2,V2), location(V2), location(V2).
try(6, 3, V2, V2) :- not use(6, 3), location(V2), location(V2).
try(6, 4, V3, V1) :- use(6, 4), playerAt(V3,V1), player(V3), location(V1).
try(6, 4, V3, V1) :- not use(6, 4), player(V3), location(V1).
try(7, 1, V4, V2) :- use(7, 1), playerAt(V4,V2), player(V4), location(V2).
try(7, 1, V4, V2) :- not use(7, 1), player(V4), location(V2).
try(7, 2, V3, V1) :- use(7, 2), playerAt(V3,V1), player(V3), location(V1).
try(7, 2, V3, V1) :- not use(7, 2), player(V3), location(V1).
try(7, 3, V2, V2) :- use(7, 3), not nextTo(V2,V2), location(V2), location(V2).
try(7, 3, V2, V2) :- not use(7, 3), location(V2), location(V2).
try(7, 4, V1, V2) :- use(7, 4), not nextTo(V1,V2), location(V1), location(V2).
try(7, 4, V1, V2) :- not use(7, 4), location(V1), location(V2).
try(8, 1, V4, V2) :- use(8, 1), playerAt(V4,V2), player(V4), location(V2).
try(8, 1, V4, V2) :- not use(8, 1), player(V4), location(V2).
try(8, 2, V3, V1) :- use(8, 2), playerAt(V3,V1), player(V3), location(V1).
try(8, 2, V3, V1) :- not use(8, 2), player(V3), location(V1).
try(8, 3, V2, V2) :- use(8, 3), not nextTo(V2,V2), location(V2), location(V2).
try(8, 3, V2, V2) :- not use(8, 3), location(V2), location(V2).
try(8, 4, V2, V1) :- use(8, 4), not nextTo(V2,V1), location(V2), location(V1).
try(8, 4, V2, V1) :- not use(8, 4), location(V2), location(V1).
try(9, 1, V4, V2) :- use(9, 1), playerAt(V4,V2), player(V4), location(V2).
try(9, 1, V4, V2) :- not use(9, 1), player(V4), location(V2).
try(9, 2, V3, V1) :- use(9, 2), playerAt(V3,V1), player(V3), location(V1).
try(9, 2, V3, V1) :- not use(9, 2), player(V3), location(V1).
try(9, 3, V2, V2) :- use(9, 3), not nextTo(V2,V2), location(V2), location(V2).
try(9, 3, V2, V2) :- not use(9, 3), location(V2), location(V2).
try(9, 4, V1, V1) :- use(9, 4), not nextTo(V1,V1), location(V1), location(V1).
try(9, 4, V1, V1) :- not use(9, 4), location(V1), location(V1).
try(10, 1, V4, V2) :- use(10, 1), playerAt(V4,V2), player(V4), location(V2).
try(10, 1, V4, V2) :- not use(10, 1), player(V4), location(V2).
try(10, 2, V3, V1) :- use(10, 2), playerAt(V3,V1), player(V3), location(V1).
try(10, 2, V3, V1) :- not use(10, 2), player(V3), location(V1).
try(10, 3, V1, V2) :- use(10, 3), not nextTo(V1,V2), location(V1), location(V2).
try(10, 3, V1, V2) :- not use(10, 3), location(V1), location(V2).
try(10, 4, V4, V2) :- use(10, 4), playerAt(V4,V2), player(V4), location(V2).
try(10, 4, V4, V2) :- not use(10, 4), player(V4), location(V2).
try(11, 1, V4, V2) :- use(11, 1), playerAt(V4,V2), player(V4), location(V2).
try(11, 1, V4, V2) :- not use(11, 1), player(V4), location(V2).
try(11, 2, V3, V1) :- use(11, 2), playerAt(V3,V1), player(V3), location(V1).
try(11, 2, V3, V1) :- not use(11, 2), player(V3), location(V1).
try(11, 3, V1, V2) :- use(11, 3), not nextTo(V1,V2), location(V1), location(V2).
try(11, 3, V1, V2) :- not use(11, 3), location(V1), location(V2).
try(11, 4, V3, V1) :- use(11, 4), playerAt(V3,V1), player(V3), location(V1).
try(11, 4, V3, V1) :- not use(11, 4), player(V3), location(V1).
try(12, 1, V4, V2) :- use(12, 1), playerAt(V4,V2), player(V4), location(V2).
try(12, 1, V4, V2) :- not use(12, 1), player(V4), location(V2).
try(12, 2, V3, V1) :- use(12, 2), playerAt(V3,V1), player(V3), location(V1).
try(12, 2, V3, V1) :- not use(12, 2), player(V3), location(V1).
try(12, 3, V1, V2) :- use(12, 3), not nextTo(V1,V2), location(V1), location(V2).
try(12, 3, V1, V2) :- not use(12, 3), location(V1), location(V2).
try(12, 4, V2, V2) :- use(12, 4), not nextTo(V2,V2), location(V2), location(V2).
try(12, 4, V2, V2) :- not use(12, 4), location(V2), location(V2).
try(13, 1, V4, V2) :- use(13, 1), playerAt(V4,V2), player(V4), location(V2).
try(13, 1, V4, V2) :- not use(13, 1), player(V4), location(V2).
try(13, 2, V3, V1) :- use(13, 2), playerAt(V3,V1), player(V3), location(V1).
try(13, 2, V3, V1) :- not use(13, 2), player(V3), location(V1).
try(13, 3, V1, V2) :- use(13, 3), not nextTo(V1,V2), location(V1), location(V2).
try(13, 3, V1, V2) :- not use(13, 3), location(V1), location(V2).
try(13, 4, V2, V1) :- use(13, 4), not nextTo(V2,V1), location(V2), location(V1).
try(13, 4, V2, V1) :- not use(13, 4), location(V2), location(V1).
try(14, 1, V4, V2) :- use(14, 1), playerAt(V4,V2), player(V4), location(V2).
try(14, 1, V4, V2) :- not use(14, 1), player(V4), location(V2).
try(14, 2, V3, V1) :- use(14, 2), playerAt(V3,V1), player(V3), location(V1).
try(14, 2, V3, V1) :- not use(14, 2), player(V3), location(V1).
try(14, 3, V1, V2) :- use(14, 3), not nextTo(V1,V2), location(V1), location(V2).
try(14, 3, V1, V2) :- not use(14, 3), location(V1), location(V2).
try(14, 4, V1, V1) :- use(14, 4), not nextTo(V1,V1), location(V1), location(V1).
try(14, 4, V1, V1) :- not use(14, 4), location(V1), location(V1).
try(15, 1, V4, V2) :- use(15, 1), playerAt(V4,V2), player(V4), location(V2).
try(15, 1, V4, V2) :- not use(15, 1), player(V4), location(V2).
try(15, 2, V3, V1) :- use(15, 2), playerAt(V3,V1), player(V3), location(V1).
try(15, 2, V3, V1) :- not use(15, 2), player(V3), location(V1).
try(15, 3, V2, V1) :- use(15, 3), not nextTo(V2,V1), location(V2), location(V1).
try(15, 3, V2, V1) :- not use(15, 3), location(V2), location(V1).
try(15, 4, V4, V2) :- use(15, 4), playerAt(V4,V2), player(V4), location(V2).
try(15, 4, V4, V2) :- not use(15, 4), player(V4), location(V2).
try(16, 1, V4, V2) :- use(16, 1), playerAt(V4,V2), player(V4), location(V2).
try(16, 1, V4, V2) :- not use(16, 1), player(V4), location(V2).
try(16, 2, V3, V1) :- use(16, 2), playerAt(V3,V1), player(V3), location(V1).
try(16, 2, V3, V1) :- not use(16, 2), player(V3), location(V1).
try(16, 3, V2, V1) :- use(16, 3), not nextTo(V2,V1), location(V2), location(V1).
try(16, 3, V2, V1) :- not use(16, 3), location(V2), location(V1).
try(16, 4, V3, V1) :- use(16, 4), playerAt(V3,V1), player(V3), location(V1).
try(16, 4, V3, V1) :- not use(16, 4), player(V3), location(V1).
try(17, 1, V4, V2) :- use(17, 1), playerAt(V4,V2), player(V4), location(V2).
try(17, 1, V4, V2) :- not use(17, 1), player(V4), location(V2).
try(17, 2, V3, V1) :- use(17, 2), playerAt(V3,V1), player(V3), location(V1).
try(17, 2, V3, V1) :- not use(17, 2), player(V3), location(V1).
try(17, 3, V2, V1) :- use(17, 3), not nextTo(V2,V1), location(V2), location(V1).
try(17, 3, V2, V1) :- not use(17, 3), location(V2), location(V1).
try(17, 4, V2, V2) :- use(17, 4), not nextTo(V2,V2), location(V2), location(V2).
try(17, 4, V2, V2) :- not use(17, 4), location(V2), location(V2).
try(18, 1, V4, V2) :- use(18, 1), playerAt(V4,V2), player(V4), location(V2).
try(18, 1, V4, V2) :- not use(18, 1), player(V4), location(V2).
try(18, 2, V3, V1) :- use(18, 2), playerAt(V3,V1), player(V3), location(V1).
try(18, 2, V3, V1) :- not use(18, 2), player(V3), location(V1).
try(18, 3, V2, V1) :- use(18, 3), not nextTo(V2,V1), location(V2), location(V1).
try(18, 3, V2, V1) :- not use(18, 3), location(V2), location(V1).
try(18, 4, V1, V2) :- use(18, 4), not nextTo(V1,V2), location(V1), location(V2).
try(18, 4, V1, V2) :- not use(18, 4), location(V1), location(V2).
try(19, 1, V4, V2) :- use(19, 1), playerAt(V4,V2), player(V4), location(V2).
try(19, 1, V4, V2) :- not use(19, 1), player(V4), location(V2).
try(19, 2, V3, V1) :- use(19, 2), playerAt(V3,V1), player(V3), location(V1).
try(19, 2, V3, V1) :- not use(19, 2), player(V3), location(V1).
try(19, 3, V2, V1) :- use(19, 3), not nextTo(V2,V1), location(V2), location(V1).
try(19, 3, V2, V1) :- not use(19, 3), location(V2), location(V1).
try(19, 4, V1, V1) :- use(19, 4), not nextTo(V1,V1), location(V1), location(V1).
try(19, 4, V1, V1) :- not use(19, 4), location(V1), location(V1).
try(20, 1, V4, V2) :- use(20, 1), playerAt(V4,V2), player(V4), location(V2).
try(20, 1, V4, V2) :- not use(20, 1), player(V4), location(V2).
try(20, 2, V3, V1) :- use(20, 2), playerAt(V3,V1), player(V3), location(V1).
try(20, 2, V3, V1) :- not use(20, 2), player(V3), location(V1).
try(20, 3, V1, V1) :- use(20, 3), not nextTo(V1,V1), location(V1), location(V1).
try(20, 3, V1, V1) :- not use(20, 3), location(V1), location(V1).
try(20, 4, V4, V2) :- use(20, 4), playerAt(V4,V2), player(V4), location(V2).
try(20, 4, V4, V2) :- not use(20, 4), player(V4), location(V2).
try(21, 1, V4, V2) :- use(21, 1), playerAt(V4,V2), player(V4), location(V2).
try(21, 1, V4, V2) :- not use(21, 1), player(V4), location(V2).
try(21, 2, V3, V1) :- use(21, 2), playerAt(V3,V1), player(V3), location(V1).
try(21, 2, V3, V1) :- not use(21, 2), player(V3), location(V1).
try(21, 3, V1, V1) :- use(21, 3), not nextTo(V1,V1), location(V1), location(V1).
try(21, 3, V1, V1) :- not use(21, 3), location(V1), location(V1).
try(21, 4, V3, V1) :- use(21, 4), playerAt(V3,V1), player(V3), location(V1).
try(21, 4, V3, V1) :- not use(21, 4), player(V3), location(V1).
try(22, 1, V4, V2) :- use(22, 1), playerAt(V4,V2), player(V4), location(V2).
try(22, 1, V4, V2) :- not use(22, 1), player(V4), location(V2).
try(22, 2, V3, V1) :- use(22, 2), playerAt(V3,V1), player(V3), location(V1).
try(22, 2, V3, V1) :- not use(22, 2), player(V3), location(V1).
try(22, 3, V1, V1) :- use(22, 3), not nextTo(V1,V1), location(V1), location(V1).
try(22, 3, V1, V1) :- not use(22, 3), location(V1), location(V1).
try(22, 4, V2, V2) :- use(22, 4), not nextTo(V2,V2), location(V2), location(V2).
try(22, 4, V2, V2) :- not use(22, 4), location(V2), location(V2).
try(23, 1, V4, V2) :- use(23, 1), playerAt(V4,V2), player(V4), location(V2).
try(23, 1, V4, V2) :- not use(23, 1), player(V4), location(V2).
try(23, 2, V3, V1) :- use(23, 2), playerAt(V3,V1), player(V3), location(V1).
try(23, 2, V3, V1) :- not use(23, 2), player(V3), location(V1).
try(23, 3, V1, V1) :- use(23, 3), not nextTo(V1,V1), location(V1), location(V1).
try(23, 3, V1, V1) :- not use(23, 3), location(V1), location(V1).
try(23, 4, V1, V2) :- use(23, 4), not nextTo(V1,V2), location(V1), location(V2).
try(23, 4, V1, V2) :- not use(23, 4), location(V1), location(V2).
try(24, 1, V4, V2) :- use(24, 1), playerAt(V4,V2), player(V4), location(V2).
try(24, 1, V4, V2) :- not use(24, 1), player(V4), location(V2).
try(24, 2, V3, V1) :- use(24, 2), playerAt(V3,V1), player(V3), location(V1).
try(24, 2, V3, V1) :- not use(24, 2), player(V3), location(V1).
try(24, 3, V1, V1) :- use(24, 3), not nextTo(V1,V1), location(V1), location(V1).
try(24, 3, V1, V1) :- not use(24, 3), location(V1), location(V1).
try(24, 4, V2, V1) :- use(24, 4), not nextTo(V2,V1), location(V2), location(V1).
try(24, 4, V2, V1) :- not use(24, 4), location(V2), location(V1).
try(25, 1, V4, V2) :- use(25, 1), playerAt(V4,V2), player(V4), location(V2).
try(25, 1, V4, V2) :- not use(25, 1), player(V4), location(V2).
try(25, 2, V2, V2) :- use(25, 2), not nextTo(V2,V2), location(V2), location(V2).
try(25, 2, V2, V2) :- not use(25, 2), location(V2), location(V2).
try(25, 3, V3, V1) :- use(25, 3), playerAt(V3,V1), player(V3), location(V1).
try(25, 3, V3, V1) :- not use(25, 3), player(V3), location(V1).
try(25, 4, V4, V2) :- use(25, 4), playerAt(V4,V2), player(V4), location(V2).
try(25, 4, V4, V2) :- not use(25, 4), player(V4), location(V2).
try(26, 1, V4, V2) :- use(26, 1), playerAt(V4,V2), player(V4), location(V2).
try(26, 1, V4, V2) :- not use(26, 1), player(V4), location(V2).
try(26, 2, V2, V2) :- use(26, 2), not nextTo(V2,V2), location(V2), location(V2).
try(26, 2, V2, V2) :- not use(26, 2), location(V2), location(V2).
try(26, 3, V3, V1) :- use(26, 3), playerAt(V3,V1), player(V3), location(V1).
try(26, 3, V3, V1) :- not use(26, 3), player(V3), location(V1).
try(26, 4, V2, V2) :- use(26, 4), not nextTo(V2,V2), location(V2), location(V2).
try(26, 4, V2, V2) :- not use(26, 4), location(V2), location(V2).
try(27, 1, V4, V2) :- use(27, 1), playerAt(V4,V2), player(V4), location(V2).
try(27, 1, V4, V2) :- not use(27, 1), player(V4), location(V2).
try(27, 2, V2, V2) :- use(27, 2), not nextTo(V2,V2), location(V2), location(V2).
try(27, 2, V2, V2) :- not use(27, 2), location(V2), location(V2).
try(27, 3, V3, V1) :- use(27, 3), playerAt(V3,V1), player(V3), location(V1).
try(27, 3, V3, V1) :- not use(27, 3), player(V3), location(V1).
try(27, 4, V1, V2) :- use(27, 4), not nextTo(V1,V2), location(V1), location(V2).
try(27, 4, V1, V2) :- not use(27, 4), location(V1), location(V2).
try(28, 1, V4, V2) :- use(28, 1), playerAt(V4,V2), player(V4), location(V2).
try(28, 1, V4, V2) :- not use(28, 1), player(V4), location(V2).
try(28, 2, V2, V2) :- use(28, 2), not nextTo(V2,V2), location(V2), location(V2).
try(28, 2, V2, V2) :- not use(28, 2), location(V2), location(V2).
try(28, 3, V3, V1) :- use(28, 3), playerAt(V3,V1), player(V3), location(V1).
try(28, 3, V3, V1) :- not use(28, 3), player(V3), location(V1).
try(28, 4, V2, V1) :- use(28, 4), not nextTo(V2,V1), location(V2), location(V1).
try(28, 4, V2, V1) :- not use(28, 4), location(V2), location(V1).
try(29, 1, V4, V2) :- use(29, 1), playerAt(V4,V2), player(V4), location(V2).
try(29, 1, V4, V2) :- not use(29, 1), player(V4), location(V2).
try(29, 2, V2, V2) :- use(29, 2), not nextTo(V2,V2), location(V2), location(V2).
try(29, 2, V2, V2) :- not use(29, 2), location(V2), location(V2).
try(29, 3, V3, V1) :- use(29, 3), playerAt(V3,V1), player(V3), location(V1).
try(29, 3, V3, V1) :- not use(29, 3), player(V3), location(V1).
try(29, 4, V1, V1) :- use(29, 4), not nextTo(V1,V1), location(V1), location(V1).
try(29, 4, V1, V1) :- not use(29, 4), location(V1), location(V1).
wins(V4,V3) :- use(0, 0) , try(0, 1, V4, V2), try(0, 2, V3, V1), try(0, 3, V4, V2), try(0, 4, V3, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(1, 0) , try(1, 1, V4, V2), try(1, 2, V3, V1), try(1, 3, V4, V2), try(1, 4, V2, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(2, 0) , try(2, 1, V4, V2), try(2, 2, V3, V1), try(2, 3, V4, V2), try(2, 4, V1, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(3, 0) , try(3, 1, V4, V2), try(3, 2, V3, V1), try(3, 3, V4, V2), try(3, 4, V2, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(4, 0) , try(4, 1, V4, V2), try(4, 2, V3, V1), try(4, 3, V4, V2), try(4, 4, V1, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(5, 0) , try(5, 1, V4, V2), try(5, 2, V3, V1), try(5, 3, V2, V2), try(5, 4, V4, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(6, 0) , try(6, 1, V4, V2), try(6, 2, V3, V1), try(6, 3, V2, V2), try(6, 4, V3, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(7, 0) , try(7, 1, V4, V2), try(7, 2, V3, V1), try(7, 3, V2, V2), try(7, 4, V1, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(8, 0) , try(8, 1, V4, V2), try(8, 2, V3, V1), try(8, 3, V2, V2), try(8, 4, V2, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(9, 0) , try(9, 1, V4, V2), try(9, 2, V3, V1), try(9, 3, V2, V2), try(9, 4, V1, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(10, 0) , try(10, 1, V4, V2), try(10, 2, V3, V1), try(10, 3, V1, V2), try(10, 4, V4, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(11, 0) , try(11, 1, V4, V2), try(11, 2, V3, V1), try(11, 3, V1, V2), try(11, 4, V3, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(12, 0) , try(12, 1, V4, V2), try(12, 2, V3, V1), try(12, 3, V1, V2), try(12, 4, V2, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(13, 0) , try(13, 1, V4, V2), try(13, 2, V3, V1), try(13, 3, V1, V2), try(13, 4, V2, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(14, 0) , try(14, 1, V4, V2), try(14, 2, V3, V1), try(14, 3, V1, V2), try(14, 4, V1, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(15, 0) , try(15, 1, V4, V2), try(15, 2, V3, V1), try(15, 3, V2, V1), try(15, 4, V4, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(16, 0) , try(16, 1, V4, V2), try(16, 2, V3, V1), try(16, 3, V2, V1), try(16, 4, V3, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(17, 0) , try(17, 1, V4, V2), try(17, 2, V3, V1), try(17, 3, V2, V1), try(17, 4, V2, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(18, 0) , try(18, 1, V4, V2), try(18, 2, V3, V1), try(18, 3, V2, V1), try(18, 4, V1, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(19, 0) , try(19, 1, V4, V2), try(19, 2, V3, V1), try(19, 3, V2, V1), try(19, 4, V1, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(20, 0) , try(20, 1, V4, V2), try(20, 2, V3, V1), try(20, 3, V1, V1), try(20, 4, V4, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(21, 0) , try(21, 1, V4, V2), try(21, 2, V3, V1), try(21, 3, V1, V1), try(21, 4, V3, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(22, 0) , try(22, 1, V4, V2), try(22, 2, V3, V1), try(22, 3, V1, V1), try(22, 4, V2, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(23, 0) , try(23, 1, V4, V2), try(23, 2, V3, V1), try(23, 3, V1, V1), try(23, 4, V1, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(24, 0) , try(24, 1, V4, V2), try(24, 2, V3, V1), try(24, 3, V1, V1), try(24, 4, V2, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(25, 0) , try(25, 1, V4, V2), try(25, 2, V2, V2), try(25, 3, V3, V1), try(25, 4, V4, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(26, 0) , try(26, 1, V4, V2), try(26, 2, V2, V2), try(26, 3, V3, V1), try(26, 4, V2, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(27, 0) , try(27, 1, V4, V2), try(27, 2, V2, V2), try(27, 3, V3, V1), try(27, 4, V1, V2), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(28, 0) , try(28, 1, V4, V2), try(28, 2, V2, V2), try(28, 3, V3, V1), try(28, 4, V2, V1), player(V4), player(V3), location(V2), location(V1).
wins(V4,V3) :- use(29, 0) , try(29, 1, V4, V2), try(29, 2, V2, V2), try(29, 3, V3, V1), try(29, 4, V1, V1), player(V4), player(V3), location(V2), location(V1).

:- level(X, Y), not level(X, 0).level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
level(0,2) :- use(0,2).
level(0,3) :- use(0,3).
level(0,4) :- use(0,4).
level(1,0) :- use(1,0).
level(1,1) :- use(1,1).
level(1,2) :- use(1,2).
level(1,3) :- use(1,3).
level(1,4) :- use(1,4).
level(2,0) :- use(2,0).
level(2,1) :- use(2,1).
level(2,2) :- use(2,2).
level(2,3) :- use(2,3).
level(2,4) :- use(2,4).
level(3,0) :- use(3,0).
level(3,1) :- use(3,1).
level(3,2) :- use(3,2).
level(3,3) :- use(3,3).
level(3,4) :- use(3,4).
level(4,0) :- use(4,0).
level(4,1) :- use(4,1).
level(4,2) :- use(4,2).
level(4,3) :- use(4,3).
level(4,4) :- use(4,4).
level(5,0) :- use(5,0).
level(5,1) :- use(5,1).
level(5,2) :- use(5,2).
level(5,3) :- use(5,3).
level(5,4) :- use(5,4).
level(6,0) :- use(6,0).
level(6,1) :- use(6,1).
level(6,2) :- use(6,2).
level(6,3) :- use(6,3).
level(6,4) :- use(6,4).
level(7,0) :- use(7,0).
level(7,1) :- use(7,1).
level(7,2) :- use(7,2).
level(7,3) :- use(7,3).
level(7,4) :- use(7,4).
level(8,0) :- use(8,0).
level(8,1) :- use(8,1).
level(8,2) :- use(8,2).
level(8,3) :- use(8,3).
level(8,4) :- use(8,4).
level(9,0) :- use(9,0).
level(9,1) :- use(9,1).
level(9,2) :- use(9,2).
level(9,3) :- use(9,3).
level(9,4) :- use(9,4).
level(10,0) :- use(10,0).
level(10,1) :- use(10,1).
level(10,2) :- use(10,2).
level(10,3) :- use(10,3).
level(10,4) :- use(10,4).
level(11,0) :- use(11,0).
level(11,1) :- use(11,1).
level(11,2) :- use(11,2).
level(11,3) :- use(11,3).
level(11,4) :- use(11,4).
level(12,0) :- use(12,0).
level(12,1) :- use(12,1).
level(12,2) :- use(12,2).
level(12,3) :- use(12,3).
level(12,4) :- use(12,4).
level(13,0) :- use(13,0).
level(13,1) :- use(13,1).
level(13,2) :- use(13,2).
level(13,3) :- use(13,3).
level(13,4) :- use(13,4).
level(14,0) :- use(14,0).
level(14,1) :- use(14,1).
level(14,2) :- use(14,2).
level(14,3) :- use(14,3).
level(14,4) :- use(14,4).
level(15,0) :- use(15,0).
level(15,1) :- use(15,1).
level(15,2) :- use(15,2).
level(15,3) :- use(15,3).
level(15,4) :- use(15,4).
level(16,0) :- use(16,0).
level(16,1) :- use(16,1).
level(16,2) :- use(16,2).
level(16,3) :- use(16,3).
level(16,4) :- use(16,4).
level(17,0) :- use(17,0).
level(17,1) :- use(17,1).
level(17,2) :- use(17,2).
level(17,3) :- use(17,3).
level(17,4) :- use(17,4).
level(18,0) :- use(18,0).
level(18,1) :- use(18,1).
level(18,2) :- use(18,2).
level(18,3) :- use(18,3).
level(18,4) :- use(18,4).
level(19,0) :- use(19,0).
level(19,1) :- use(19,1).
level(19,2) :- use(19,2).
level(19,3) :- use(19,3).
level(19,4) :- use(19,4).
level(20,0) :- use(20,0).
level(20,1) :- use(20,1).
level(20,2) :- use(20,2).
level(20,3) :- use(20,3).
level(20,4) :- use(20,4).
level(21,0) :- use(21,0).
level(21,1) :- use(21,1).
level(21,2) :- use(21,2).
level(21,3) :- use(21,3).
level(21,4) :- use(21,4).
level(22,0) :- use(22,0).
level(22,1) :- use(22,1).
level(22,2) :- use(22,2).
level(22,3) :- use(22,3).
level(22,4) :- use(22,4).
level(23,0) :- use(23,0).
level(23,1) :- use(23,1).
level(23,2) :- use(23,2).
level(23,3) :- use(23,3).
level(23,4) :- use(23,4).
level(24,0) :- use(24,0).
level(24,1) :- use(24,1).
level(24,2) :- use(24,2).
level(24,3) :- use(24,3).
level(24,4) :- use(24,4).
level(25,0) :- use(25,0).
level(25,1) :- use(25,1).
level(25,2) :- use(25,2).
level(25,3) :- use(25,3).
level(25,4) :- use(25,4).
level(26,0) :- use(26,0).
level(26,1) :- use(26,1).
level(26,2) :- use(26,2).
level(26,3) :- use(26,3).
level(26,4) :- use(26,4).
level(27,0) :- use(27,0).
level(27,1) :- use(27,1).
level(27,2) :- use(27,2).
level(27,3) :- use(27,3).
level(27,4) :- use(27,4).
level(28,0) :- use(28,0).
level(28,1) :- use(28,1).
level(28,2) :- use(28,2).
level(28,3) :- use(28,3).
level(28,4) :- use(28,4).
level(29,0) :- use(29,0).
level(29,1) :- use(29,1).
level(29,2) :- use(29,2).
level(29,3) :- use(29,3).
level(29,4) :- use(29,4).
