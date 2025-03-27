#show use/2.
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


{ use(V1, 0) } :- clause(V1).
{ use(V1, V2) } :- clause(V1), literal(V1, V2).
clause(0).
literal(0, 1).
literal(0, 2).
literal(0, 3).
clause(1).
literal(1, 1).
literal(1, 2).
literal(1, 3).
clause(2).
literal(2, 1).
literal(2, 2).
literal(2, 3).
clause(3).
literal(3, 1).
literal(3, 2).
literal(3, 3).
clause(4).
literal(4, 1).
literal(4, 2).
literal(4, 3).
clause(5).
literal(5, 1).
literal(5, 2).
literal(5, 3).
clause(6).
literal(6, 1).
literal(6, 2).
literal(6, 3).
clause(7).
literal(7, 1).
literal(7, 2).
literal(7, 3).
clause(8).
literal(8, 1).
literal(8, 2).
literal(8, 3).
clause(9).
literal(9, 1).
literal(9, 2).
literal(9, 3).
clause(10).
literal(10, 1).
literal(10, 2).
literal(10, 3).
clause(11).
literal(11, 1).
literal(11, 2).
literal(11, 3).
clause(12).
literal(12, 1).
literal(12, 2).
literal(12, 3).
clause(13).
literal(13, 1).
literal(13, 2).
literal(13, 3).
clause(14).
literal(14, 1).
literal(14, 2).
literal(14, 3).
clause(15).
literal(15, 1).
literal(15, 2).
literal(15, 3).
clause(16).
literal(16, 1).
literal(16, 2).
literal(16, 3).
clause(17).
literal(17, 1).
literal(17, 2).
literal(17, 3).
clause(18).
literal(18, 1).
literal(18, 2).
literal(18, 3).
clause(19).
literal(19, 1).
literal(19, 2).
literal(19, 3).
clause(20).
literal(20, 1).
literal(20, 2).
literal(20, 3).
clause(21).
literal(21, 1).
literal(21, 2).
literal(21, 3).
clause(22).
literal(22, 1).
literal(22, 2).
literal(22, 3).
clause(23).
literal(23, 1).
literal(23, 2).
literal(23, 3).
clause(24).
literal(24, 1).
literal(24, 2).
literal(24, 3).
clause(25).
literal(25, 1).
literal(25, 2).
literal(25, 3).
clause(26).
literal(26, 1).
literal(26, 2).
literal(26, 3).
clause(27).
literal(27, 1).
literal(27, 2).
literal(27, 3).
clause(28).
literal(28, 1).
literal(28, 2).
literal(28, 3).
clause(29).
literal(29, 1).
literal(29, 2).
literal(29, 3).
clause(30).
literal(30, 1).
literal(30, 2).
literal(30, 3).
clause(31).
literal(31, 1).
literal(31, 2).
literal(31, 3).
clause(32).
literal(32, 1).
literal(32, 2).
literal(32, 3).
clause(33).
literal(33, 1).
literal(33, 2).
literal(33, 3).
clause(34).
literal(34, 1).
literal(34, 2).
literal(34, 3).
clause(35).
literal(35, 1).
literal(35, 2).
literal(35, 3).
clause(36).
literal(36, 1).
literal(36, 2).
literal(36, 3).
clause(37).
literal(37, 1).
literal(37, 2).
literal(37, 3).
clause(38).
literal(38, 1).
literal(38, 2).
literal(38, 3).
clause(39).
literal(39, 1).
literal(39, 2).
literal(39, 3).
clause(40).
literal(40, 1).
literal(40, 2).
literal(40, 3).
clause(41).
literal(41, 1).
literal(41, 2).
literal(41, 3).
clause(42).
literal(42, 1).
literal(42, 2).
literal(42, 3).
clause(43).
literal(43, 1).
literal(43, 2).
literal(43, 3).
clause(44).
literal(44, 1).
literal(44, 2).
literal(44, 3).
clause(45).
literal(45, 1).
literal(45, 2).
literal(45, 3).
clause(46).
literal(46, 1).
literal(46, 2).
literal(46, 3).
clause(47).
literal(47, 1).
literal(47, 2).
literal(47, 3).
clause(48).
literal(48, 1).
literal(48, 2).
literal(48, 3).
clause(49).
literal(49, 1).
literal(49, 2).
literal(49, 3).
clause(50).
literal(50, 1).
literal(50, 2).
literal(50, 3).
clause(51).
literal(51, 1).
literal(51, 2).
literal(51, 3).
clause(52).
literal(52, 1).
literal(52, 2).
literal(52, 3).
clause(53).
literal(53, 1).
literal(53, 2).
literal(53, 3).
clause(54).
literal(54, 1).
literal(54, 2).
literal(54, 3).
clause(55).
literal(55, 1).
literal(55, 2).
literal(55, 3).
clause(56).
literal(56, 1).
literal(56, 2).
literal(56, 3).
clause(57).
literal(57, 1).
literal(57, 2).
literal(57, 3).
clause(58).
literal(58, 1).
literal(58, 2).
literal(58, 3).
clause(59).
literal(59, 1).
literal(59, 2).
literal(59, 3).
clause(60).
literal(60, 1).
literal(60, 2).
literal(60, 3).
clause(61).
literal(61, 1).
literal(61, 2).
literal(61, 3).
clause(62).
literal(62, 1).
literal(62, 2).
literal(62, 3).
clause(63).
literal(63, 1).
literal(63, 2).
literal(63, 3).
clause(64).
literal(64, 1).
literal(64, 2).
literal(64, 3).
clause(65).
literal(65, 1).
literal(65, 2).
literal(65, 3).
clause(66).
literal(66, 1).
literal(66, 2).
literal(66, 3).
clause(67).
literal(67, 1).
literal(67, 2).
literal(67, 3).
clause(68).
literal(68, 1).
literal(68, 2).
literal(68, 3).
clause(69).
literal(69, 1).
literal(69, 2).
literal(69, 3).
clause(70).
literal(70, 1).
literal(70, 2).
literal(70, 3).
clause(71).
literal(71, 1).
literal(71, 2).
literal(71, 3).
clause(72).
literal(72, 1).
literal(72, 2).
literal(72, 3).
clause(73).
literal(73, 1).
literal(73, 2).
literal(73, 3).
clause(74).
literal(74, 1).
literal(74, 2).
literal(74, 3).
clause(75).
literal(75, 1).
literal(75, 2).
literal(75, 3).
clause(76).
literal(76, 1).
literal(76, 2).
literal(76, 3).
clause(77).
literal(77, 1).
literal(77, 2).
literal(77, 3).
clause(78).
literal(78, 1).
literal(78, 2).
literal(78, 3).
clause(79).
literal(79, 1).
literal(79, 2).
literal(79, 3).
clause(80).
literal(80, 1).
literal(80, 2).
literal(80, 3).
clause(81).
literal(81, 1).
literal(81, 2).
literal(81, 3).
clause(82).
literal(82, 1).
literal(82, 2).
literal(82, 3).
clause(83).
literal(83, 1).
literal(83, 2).
literal(83, 3).
clause(84).
literal(84, 1).
literal(84, 2).
literal(84, 3).
clause(85).
literal(85, 1).
literal(85, 2).
literal(85, 3).
clause(86).
literal(86, 1).
literal(86, 2).
literal(86, 3).
clause(87).
literal(87, 1).
literal(87, 2).
literal(87, 3).
clause(88).
literal(88, 1).
literal(88, 2).
literal(88, 3).
clause(89).
literal(89, 1).
literal(89, 2).
literal(89, 3).
clause(90).
literal(90, 1).
literal(90, 2).
literal(90, 3).
clause(91).
literal(91, 1).
literal(91, 2).
literal(91, 3).
clause(92).
literal(92, 1).
literal(92, 2).
literal(92, 3).
clause(93).
literal(93, 1).
literal(93, 2).
literal(93, 3).
clause(94).
literal(94, 1).
literal(94, 2).
literal(94, 3).
clause(95).
literal(95, 1).
literal(95, 2).
literal(95, 3).
clause(96).
literal(96, 1).
literal(96, 2).
literal(96, 3).
clause(97).
literal(97, 1).
literal(97, 2).
literal(97, 3).
clause(98).
literal(98, 1).
literal(98, 2).
literal(98, 3).
clause(99).
literal(99, 1).
literal(99, 2).
literal(99, 3).
clause(100).
literal(100, 1).
literal(100, 2).
literal(100, 3).
clause(101).
literal(101, 1).
literal(101, 2).
literal(101, 3).
clause(102).
literal(102, 1).
literal(102, 2).
literal(102, 3).
clause(103).
literal(103, 1).
literal(103, 2).
literal(103, 3).
clause(104).
literal(104, 1).
literal(104, 2).
literal(104, 3).
clause(105).
literal(105, 1).
literal(105, 2).
literal(105, 3).
clause(106).
literal(106, 1).
literal(106, 2).
literal(106, 3).
clause(107).
literal(107, 1).
literal(107, 2).
literal(107, 3).

level(0,0) :- use(0,0).
level(0,1) :- use(0,1).
level(0,2) :- use(0,2).
level(0,3) :- use(0,3).
:- not level(0,0),level(0,1),level(0,2),level(0,3).
level(1,0) :- use(1,0).
level(1,1) :- use(1,1).
level(1,2) :- use(1,2).
level(1,3) :- use(1,3).
:- not level(1,0),level(1,1),level(1,2),level(1,3).
level(2,0) :- use(2,0).
level(2,1) :- use(2,1).
level(2,2) :- use(2,2).
level(2,3) :- use(2,3).
:- not level(2,0),level(2,1),level(2,2),level(2,3).
level(3,0) :- use(3,0).
level(3,1) :- use(3,1).
level(3,2) :- use(3,2).
level(3,3) :- use(3,3).
:- not level(3,0),level(3,1),level(3,2),level(3,3).
level(4,0) :- use(4,0).
level(4,1) :- use(4,1).
level(4,2) :- use(4,2).
level(4,3) :- use(4,3).
:- not level(4,0),level(4,1),level(4,2),level(4,3).
level(5,0) :- use(5,0).
level(5,1) :- use(5,1).
level(5,2) :- use(5,2).
level(5,3) :- use(5,3).
:- not level(5,0),level(5,1),level(5,2),level(5,3).
level(6,0) :- use(6,0).
level(6,1) :- use(6,1).
level(6,2) :- use(6,2).
level(6,3) :- use(6,3).
:- not level(6,0),level(6,1),level(6,2),level(6,3).
level(7,0) :- use(7,0).
level(7,1) :- use(7,1).
level(7,2) :- use(7,2).
level(7,3) :- use(7,3).
:- not level(7,0),level(7,1),level(7,2),level(7,3).
level(8,0) :- use(8,0).
level(8,1) :- use(8,1).
level(8,2) :- use(8,2).
level(8,3) :- use(8,3).
:- not level(8,0),level(8,1),level(8,2),level(8,3).
level(9,0) :- use(9,0).
level(9,1) :- use(9,1).
level(9,2) :- use(9,2).
level(9,3) :- use(9,3).
:- not level(9,0),level(9,1),level(9,2),level(9,3).
level(10,0) :- use(10,0).
level(10,1) :- use(10,1).
level(10,2) :- use(10,2).
level(10,3) :- use(10,3).
:- not level(10,0),level(10,1),level(10,2),level(10,3).
level(11,0) :- use(11,0).
level(11,1) :- use(11,1).
level(11,2) :- use(11,2).
level(11,3) :- use(11,3).
:- not level(11,0),level(11,1),level(11,2),level(11,3).
level(12,0) :- use(12,0).
level(12,1) :- use(12,1).
level(12,2) :- use(12,2).
level(12,3) :- use(12,3).
:- not level(12,0),level(12,1),level(12,2),level(12,3).
level(13,0) :- use(13,0).
level(13,1) :- use(13,1).
level(13,2) :- use(13,2).
level(13,3) :- use(13,3).
:- not level(13,0),level(13,1),level(13,2),level(13,3).
level(14,0) :- use(14,0).
level(14,1) :- use(14,1).
level(14,2) :- use(14,2).
level(14,3) :- use(14,3).
:- not level(14,0),level(14,1),level(14,2),level(14,3).
level(15,0) :- use(15,0).
level(15,1) :- use(15,1).
level(15,2) :- use(15,2).
level(15,3) :- use(15,3).
:- not level(15,0),level(15,1),level(15,2),level(15,3).
level(16,0) :- use(16,0).
level(16,1) :- use(16,1).
level(16,2) :- use(16,2).
level(16,3) :- use(16,3).
:- not level(16,0),level(16,1),level(16,2),level(16,3).
level(17,0) :- use(17,0).
level(17,1) :- use(17,1).
level(17,2) :- use(17,2).
level(17,3) :- use(17,3).
:- not level(17,0),level(17,1),level(17,2),level(17,3).
level(18,0) :- use(18,0).
level(18,1) :- use(18,1).
level(18,2) :- use(18,2).
level(18,3) :- use(18,3).
:- not level(18,0),level(18,1),level(18,2),level(18,3).
level(19,0) :- use(19,0).
level(19,1) :- use(19,1).
level(19,2) :- use(19,2).
level(19,3) :- use(19,3).
:- not level(19,0),level(19,1),level(19,2),level(19,3).
level(20,0) :- use(20,0).
level(20,1) :- use(20,1).
level(20,2) :- use(20,2).
level(20,3) :- use(20,3).
:- not level(20,0),level(20,1),level(20,2),level(20,3).
level(21,0) :- use(21,0).
level(21,1) :- use(21,1).
level(21,2) :- use(21,2).
level(21,3) :- use(21,3).
:- not level(21,0),level(21,1),level(21,2),level(21,3).
level(22,0) :- use(22,0).
level(22,1) :- use(22,1).
level(22,2) :- use(22,2).
level(22,3) :- use(22,3).
:- not level(22,0),level(22,1),level(22,2),level(22,3).
level(23,0) :- use(23,0).
level(23,1) :- use(23,1).
level(23,2) :- use(23,2).
level(23,3) :- use(23,3).
:- not level(23,0),level(23,1),level(23,2),level(23,3).
level(24,0) :- use(24,0).
level(24,1) :- use(24,1).
level(24,2) :- use(24,2).
level(24,3) :- use(24,3).
:- not level(24,0),level(24,1),level(24,2),level(24,3).
level(25,0) :- use(25,0).
level(25,1) :- use(25,1).
level(25,2) :- use(25,2).
level(25,3) :- use(25,3).
:- not level(25,0),level(25,1),level(25,2),level(25,3).
level(26,0) :- use(26,0).
level(26,1) :- use(26,1).
level(26,2) :- use(26,2).
level(26,3) :- use(26,3).
:- not level(26,0),level(26,1),level(26,2),level(26,3).
level(27,0) :- use(27,0).
level(27,1) :- use(27,1).
level(27,2) :- use(27,2).
level(27,3) :- use(27,3).
:- not level(27,0),level(27,1),level(27,2),level(27,3).
level(28,0) :- use(28,0).
level(28,1) :- use(28,1).
level(28,2) :- use(28,2).
level(28,3) :- use(28,3).
:- not level(28,0),level(28,1),level(28,2),level(28,3).
level(29,0) :- use(29,0).
level(29,1) :- use(29,1).
level(29,2) :- use(29,2).
level(29,3) :- use(29,3).
:- not level(29,0),level(29,1),level(29,2),level(29,3).
level(30,0) :- use(30,0).
level(30,1) :- use(30,1).
level(30,2) :- use(30,2).
level(30,3) :- use(30,3).
:- not level(30,0),level(30,1),level(30,2),level(30,3).
level(31,0) :- use(31,0).
level(31,1) :- use(31,1).
level(31,2) :- use(31,2).
level(31,3) :- use(31,3).
:- not level(31,0),level(31,1),level(31,2),level(31,3).
level(32,0) :- use(32,0).
level(32,1) :- use(32,1).
level(32,2) :- use(32,2).
level(32,3) :- use(32,3).
:- not level(32,0),level(32,1),level(32,2),level(32,3).
level(33,0) :- use(33,0).
level(33,1) :- use(33,1).
level(33,2) :- use(33,2).
level(33,3) :- use(33,3).
:- not level(33,0),level(33,1),level(33,2),level(33,3).
level(34,0) :- use(34,0).
level(34,1) :- use(34,1).
level(34,2) :- use(34,2).
level(34,3) :- use(34,3).
:- not level(34,0),level(34,1),level(34,2),level(34,3).
level(35,0) :- use(35,0).
level(35,1) :- use(35,1).
level(35,2) :- use(35,2).
level(35,3) :- use(35,3).
:- not level(35,0),level(35,1),level(35,2),level(35,3).
level(36,0) :- use(36,0).
level(36,1) :- use(36,1).
level(36,2) :- use(36,2).
level(36,3) :- use(36,3).
:- not level(36,0),level(36,1),level(36,2),level(36,3).
level(37,0) :- use(37,0).
level(37,1) :- use(37,1).
level(37,2) :- use(37,2).
level(37,3) :- use(37,3).
:- not level(37,0),level(37,1),level(37,2),level(37,3).
level(38,0) :- use(38,0).
level(38,1) :- use(38,1).
level(38,2) :- use(38,2).
level(38,3) :- use(38,3).
:- not level(38,0),level(38,1),level(38,2),level(38,3).
level(39,0) :- use(39,0).
level(39,1) :- use(39,1).
level(39,2) :- use(39,2).
level(39,3) :- use(39,3).
:- not level(39,0),level(39,1),level(39,2),level(39,3).
level(40,0) :- use(40,0).
level(40,1) :- use(40,1).
level(40,2) :- use(40,2).
level(40,3) :- use(40,3).
:- not level(40,0),level(40,1),level(40,2),level(40,3).
level(41,0) :- use(41,0).
level(41,1) :- use(41,1).
level(41,2) :- use(41,2).
level(41,3) :- use(41,3).
:- not level(41,0),level(41,1),level(41,2),level(41,3).
level(42,0) :- use(42,0).
level(42,1) :- use(42,1).
level(42,2) :- use(42,2).
level(42,3) :- use(42,3).
:- not level(42,0),level(42,1),level(42,2),level(42,3).
level(43,0) :- use(43,0).
level(43,1) :- use(43,1).
level(43,2) :- use(43,2).
level(43,3) :- use(43,3).
:- not level(43,0),level(43,1),level(43,2),level(43,3).
level(44,0) :- use(44,0).
level(44,1) :- use(44,1).
level(44,2) :- use(44,2).
level(44,3) :- use(44,3).
:- not level(44,0),level(44,1),level(44,2),level(44,3).
level(45,0) :- use(45,0).
level(45,1) :- use(45,1).
level(45,2) :- use(45,2).
level(45,3) :- use(45,3).
:- not level(45,0),level(45,1),level(45,2),level(45,3).
level(46,0) :- use(46,0).
level(46,1) :- use(46,1).
level(46,2) :- use(46,2).
level(46,3) :- use(46,3).
:- not level(46,0),level(46,1),level(46,2),level(46,3).
level(47,0) :- use(47,0).
level(47,1) :- use(47,1).
level(47,2) :- use(47,2).
level(47,3) :- use(47,3).
:- not level(47,0),level(47,1),level(47,2),level(47,3).
level(48,0) :- use(48,0).
level(48,1) :- use(48,1).
level(48,2) :- use(48,2).
level(48,3) :- use(48,3).
:- not level(48,0),level(48,1),level(48,2),level(48,3).
level(49,0) :- use(49,0).
level(49,1) :- use(49,1).
level(49,2) :- use(49,2).
level(49,3) :- use(49,3).
:- not level(49,0),level(49,1),level(49,2),level(49,3).
level(50,0) :- use(50,0).
level(50,1) :- use(50,1).
level(50,2) :- use(50,2).
level(50,3) :- use(50,3).
:- not level(50,0),level(50,1),level(50,2),level(50,3).
level(51,0) :- use(51,0).
level(51,1) :- use(51,1).
level(51,2) :- use(51,2).
level(51,3) :- use(51,3).
:- not level(51,0),level(51,1),level(51,2),level(51,3).
level(52,0) :- use(52,0).
level(52,1) :- use(52,1).
level(52,2) :- use(52,2).
level(52,3) :- use(52,3).
:- not level(52,0),level(52,1),level(52,2),level(52,3).
level(53,0) :- use(53,0).
level(53,1) :- use(53,1).
level(53,2) :- use(53,2).
level(53,3) :- use(53,3).
:- not level(53,0),level(53,1),level(53,2),level(53,3).
level(54,0) :- use(54,0).
level(54,1) :- use(54,1).
level(54,2) :- use(54,2).
level(54,3) :- use(54,3).
:- not level(54,0),level(54,1),level(54,2),level(54,3).
level(55,0) :- use(55,0).
level(55,1) :- use(55,1).
level(55,2) :- use(55,2).
level(55,3) :- use(55,3).
:- not level(55,0),level(55,1),level(55,2),level(55,3).
level(56,0) :- use(56,0).
level(56,1) :- use(56,1).
level(56,2) :- use(56,2).
level(56,3) :- use(56,3).
:- not level(56,0),level(56,1),level(56,2),level(56,3).
level(57,0) :- use(57,0).
level(57,1) :- use(57,1).
level(57,2) :- use(57,2).
level(57,3) :- use(57,3).
:- not level(57,0),level(57,1),level(57,2),level(57,3).
level(58,0) :- use(58,0).
level(58,1) :- use(58,1).
level(58,2) :- use(58,2).
level(58,3) :- use(58,3).
:- not level(58,0),level(58,1),level(58,2),level(58,3).
level(59,0) :- use(59,0).
level(59,1) :- use(59,1).
level(59,2) :- use(59,2).
level(59,3) :- use(59,3).
:- not level(59,0),level(59,1),level(59,2),level(59,3).
level(60,0) :- use(60,0).
level(60,1) :- use(60,1).
level(60,2) :- use(60,2).
level(60,3) :- use(60,3).
:- not level(60,0),level(60,1),level(60,2),level(60,3).
level(61,0) :- use(61,0).
level(61,1) :- use(61,1).
level(61,2) :- use(61,2).
level(61,3) :- use(61,3).
:- not level(61,0),level(61,1),level(61,2),level(61,3).
level(62,0) :- use(62,0).
level(62,1) :- use(62,1).
level(62,2) :- use(62,2).
level(62,3) :- use(62,3).
:- not level(62,0),level(62,1),level(62,2),level(62,3).
level(63,0) :- use(63,0).
level(63,1) :- use(63,1).
level(63,2) :- use(63,2).
level(63,3) :- use(63,3).
:- not level(63,0),level(63,1),level(63,2),level(63,3).
level(64,0) :- use(64,0).
level(64,1) :- use(64,1).
level(64,2) :- use(64,2).
level(64,3) :- use(64,3).
:- not level(64,0),level(64,1),level(64,2),level(64,3).
level(65,0) :- use(65,0).
level(65,1) :- use(65,1).
level(65,2) :- use(65,2).
level(65,3) :- use(65,3).
:- not level(65,0),level(65,1),level(65,2),level(65,3).
level(66,0) :- use(66,0).
level(66,1) :- use(66,1).
level(66,2) :- use(66,2).
level(66,3) :- use(66,3).
:- not level(66,0),level(66,1),level(66,2),level(66,3).
level(67,0) :- use(67,0).
level(67,1) :- use(67,1).
level(67,2) :- use(67,2).
level(67,3) :- use(67,3).
:- not level(67,0),level(67,1),level(67,2),level(67,3).
level(68,0) :- use(68,0).
level(68,1) :- use(68,1).
level(68,2) :- use(68,2).
level(68,3) :- use(68,3).
:- not level(68,0),level(68,1),level(68,2),level(68,3).
level(69,0) :- use(69,0).
level(69,1) :- use(69,1).
level(69,2) :- use(69,2).
level(69,3) :- use(69,3).
:- not level(69,0),level(69,1),level(69,2),level(69,3).
level(70,0) :- use(70,0).
level(70,1) :- use(70,1).
level(70,2) :- use(70,2).
level(70,3) :- use(70,3).
:- not level(70,0),level(70,1),level(70,2),level(70,3).
level(71,0) :- use(71,0).
level(71,1) :- use(71,1).
level(71,2) :- use(71,2).
level(71,3) :- use(71,3).
:- not level(71,0),level(71,1),level(71,2),level(71,3).
level(72,0) :- use(72,0).
level(72,1) :- use(72,1).
level(72,2) :- use(72,2).
level(72,3) :- use(72,3).
:- not level(72,0),level(72,1),level(72,2),level(72,3).
level(73,0) :- use(73,0).
level(73,1) :- use(73,1).
level(73,2) :- use(73,2).
level(73,3) :- use(73,3).
:- not level(73,0),level(73,1),level(73,2),level(73,3).
level(74,0) :- use(74,0).
level(74,1) :- use(74,1).
level(74,2) :- use(74,2).
level(74,3) :- use(74,3).
:- not level(74,0),level(74,1),level(74,2),level(74,3).
level(75,0) :- use(75,0).
level(75,1) :- use(75,1).
level(75,2) :- use(75,2).
level(75,3) :- use(75,3).
:- not level(75,0),level(75,1),level(75,2),level(75,3).
level(76,0) :- use(76,0).
level(76,1) :- use(76,1).
level(76,2) :- use(76,2).
level(76,3) :- use(76,3).
:- not level(76,0),level(76,1),level(76,2),level(76,3).
level(77,0) :- use(77,0).
level(77,1) :- use(77,1).
level(77,2) :- use(77,2).
level(77,3) :- use(77,3).
:- not level(77,0),level(77,1),level(77,2),level(77,3).
level(78,0) :- use(78,0).
level(78,1) :- use(78,1).
level(78,2) :- use(78,2).
level(78,3) :- use(78,3).
:- not level(78,0),level(78,1),level(78,2),level(78,3).
level(79,0) :- use(79,0).
level(79,1) :- use(79,1).
level(79,2) :- use(79,2).
level(79,3) :- use(79,3).
:- not level(79,0),level(79,1),level(79,2),level(79,3).
level(80,0) :- use(80,0).
level(80,1) :- use(80,1).
level(80,2) :- use(80,2).
level(80,3) :- use(80,3).
:- not level(80,0),level(80,1),level(80,2),level(80,3).
level(81,0) :- use(81,0).
level(81,1) :- use(81,1).
level(81,2) :- use(81,2).
level(81,3) :- use(81,3).
:- not level(81,0),level(81,1),level(81,2),level(81,3).
level(82,0) :- use(82,0).
level(82,1) :- use(82,1).
level(82,2) :- use(82,2).
level(82,3) :- use(82,3).
:- not level(82,0),level(82,1),level(82,2),level(82,3).
level(83,0) :- use(83,0).
level(83,1) :- use(83,1).
level(83,2) :- use(83,2).
level(83,3) :- use(83,3).
:- not level(83,0),level(83,1),level(83,2),level(83,3).
level(84,0) :- use(84,0).
level(84,1) :- use(84,1).
level(84,2) :- use(84,2).
level(84,3) :- use(84,3).
:- not level(84,0),level(84,1),level(84,2),level(84,3).
level(85,0) :- use(85,0).
level(85,1) :- use(85,1).
level(85,2) :- use(85,2).
level(85,3) :- use(85,3).
:- not level(85,0),level(85,1),level(85,2),level(85,3).
level(86,0) :- use(86,0).
level(86,1) :- use(86,1).
level(86,2) :- use(86,2).
level(86,3) :- use(86,3).
:- not level(86,0),level(86,1),level(86,2),level(86,3).
level(87,0) :- use(87,0).
level(87,1) :- use(87,1).
level(87,2) :- use(87,2).
level(87,3) :- use(87,3).
:- not level(87,0),level(87,1),level(87,2),level(87,3).
level(88,0) :- use(88,0).
level(88,1) :- use(88,1).
level(88,2) :- use(88,2).
level(88,3) :- use(88,3).
:- not level(88,0),level(88,1),level(88,2),level(88,3).
level(89,0) :- use(89,0).
level(89,1) :- use(89,1).
level(89,2) :- use(89,2).
level(89,3) :- use(89,3).
:- not level(89,0),level(89,1),level(89,2),level(89,3).
level(90,0) :- use(90,0).
level(90,1) :- use(90,1).
level(90,2) :- use(90,2).
level(90,3) :- use(90,3).
:- not level(90,0),level(90,1),level(90,2),level(90,3).
level(91,0) :- use(91,0).
level(91,1) :- use(91,1).
level(91,2) :- use(91,2).
level(91,3) :- use(91,3).
:- not level(91,0),level(91,1),level(91,2),level(91,3).
level(92,0) :- use(92,0).
level(92,1) :- use(92,1).
level(92,2) :- use(92,2).
level(92,3) :- use(92,3).
:- not level(92,0),level(92,1),level(92,2),level(92,3).
level(93,0) :- use(93,0).
level(93,1) :- use(93,1).
level(93,2) :- use(93,2).
level(93,3) :- use(93,3).
:- not level(93,0),level(93,1),level(93,2),level(93,3).
level(94,0) :- use(94,0).
level(94,1) :- use(94,1).
level(94,2) :- use(94,2).
level(94,3) :- use(94,3).
:- not level(94,0),level(94,1),level(94,2),level(94,3).
level(95,0) :- use(95,0).
level(95,1) :- use(95,1).
level(95,2) :- use(95,2).
level(95,3) :- use(95,3).
:- not level(95,0),level(95,1),level(95,2),level(95,3).
level(96,0) :- use(96,0).
level(96,1) :- use(96,1).
level(96,2) :- use(96,2).
level(96,3) :- use(96,3).
:- not level(96,0),level(96,1),level(96,2),level(96,3).
level(97,0) :- use(97,0).
level(97,1) :- use(97,1).
level(97,2) :- use(97,2).
level(97,3) :- use(97,3).
:- not level(97,0),level(97,1),level(97,2),level(97,3).
level(98,0) :- use(98,0).
level(98,1) :- use(98,1).
level(98,2) :- use(98,2).
level(98,3) :- use(98,3).
:- not level(98,0),level(98,1),level(98,2),level(98,3).
level(99,0) :- use(99,0).
level(99,1) :- use(99,1).
level(99,2) :- use(99,2).
level(99,3) :- use(99,3).
:- not level(99,0),level(99,1),level(99,2),level(99,3).
level(100,0) :- use(100,0).
level(100,1) :- use(100,1).
level(100,2) :- use(100,2).
level(100,3) :- use(100,3).
:- not level(100,0),level(100,1),level(100,2),level(100,3).
level(101,0) :- use(101,0).
level(101,1) :- use(101,1).
level(101,2) :- use(101,2).
level(101,3) :- use(101,3).
:- not level(101,0),level(101,1),level(101,2),level(101,3).
level(102,0) :- use(102,0).
level(102,1) :- use(102,1).
level(102,2) :- use(102,2).
level(102,3) :- use(102,3).
:- not level(102,0),level(102,1),level(102,2),level(102,3).
level(103,0) :- use(103,0).
level(103,1) :- use(103,1).
level(103,2) :- use(103,2).
level(103,3) :- use(103,3).
:- not level(103,0),level(103,1),level(103,2),level(103,3).
level(104,0) :- use(104,0).
level(104,1) :- use(104,1).
level(104,2) :- use(104,2).
level(104,3) :- use(104,3).
:- not level(104,0),level(104,1),level(104,2),level(104,3).
level(105,0) :- use(105,0).
level(105,1) :- use(105,1).
level(105,2) :- use(105,2).
level(105,3) :- use(105,3).
:- not level(105,0),level(105,1),level(105,2),level(105,3).
level(106,0) :- use(106,0).
level(106,1) :- use(106,1).
level(106,2) :- use(106,2).
level(106,3) :- use(106,3).
:- not level(106,0),level(106,1),level(106,2),level(106,3).
level(107,0) :- use(107,0).
level(107,1) :- use(107,1).
level(107,2) :- use(107,2).
level(107,3) :- use(107,3).
:- not level(107,0),level(107,1),level(107,2),level(107,3).

#minimize{ 2@1 : use(0,0) }.
#minimize{ 2@1 : use(0,1) }.
#minimize{ 2@1 : use(0,2) }.
#minimize{ 2@1 : use(0,3) }.
#minimize{ 2@1 : use(1,0) }.
#minimize{ 2@1 : use(1,1) }.
#minimize{ 2@1 : use(1,2) }.
#minimize{ 2@1 : use(1,3) }.
#minimize{ 2@1 : use(2,0) }.
#minimize{ 2@1 : use(2,1) }.
#minimize{ 2@1 : use(2,2) }.
#minimize{ 2@1 : use(2,3) }.
#minimize{ 2@1 : use(3,0) }.
#minimize{ 2@1 : use(3,1) }.
#minimize{ 2@1 : use(3,2) }.
#minimize{ 2@1 : use(3,3) }.
#minimize{ 2@1 : use(4,0) }.
#minimize{ 2@1 : use(4,1) }.
#minimize{ 2@1 : use(4,2) }.
#minimize{ 2@1 : use(4,3) }.
#minimize{ 2@1 : use(5,0) }.
#minimize{ 2@1 : use(5,1) }.
#minimize{ 2@1 : use(5,2) }.
#minimize{ 2@1 : use(5,3) }.
#minimize{ 2@1 : use(6,0) }.
#minimize{ 2@1 : use(6,1) }.
#minimize{ 2@1 : use(6,2) }.
#minimize{ 2@1 : use(6,3) }.
#minimize{ 2@1 : use(7,0) }.
#minimize{ 2@1 : use(7,1) }.
#minimize{ 2@1 : use(7,2) }.
#minimize{ 2@1 : use(7,3) }.
#minimize{ 2@1 : use(8,0) }.
#minimize{ 2@1 : use(8,1) }.
#minimize{ 2@1 : use(8,2) }.
#minimize{ 2@1 : use(8,3) }.
#minimize{ 2@1 : use(9,0) }.
#minimize{ 2@1 : use(9,1) }.
#minimize{ 2@1 : use(9,2) }.
#minimize{ 2@1 : use(9,3) }.
#minimize{ 2@1 : use(10,0) }.
#minimize{ 2@1 : use(10,1) }.
#minimize{ 2@1 : use(10,2) }.
#minimize{ 2@1 : use(10,3) }.
#minimize{ 2@1 : use(11,0) }.
#minimize{ 2@1 : use(11,1) }.
#minimize{ 2@1 : use(11,2) }.
#minimize{ 2@1 : use(11,3) }.
#minimize{ 2@1 : use(12,0) }.
#minimize{ 2@1 : use(12,1) }.
#minimize{ 2@1 : use(12,2) }.
#minimize{ 2@1 : use(12,3) }.
#minimize{ 2@1 : use(13,0) }.
#minimize{ 2@1 : use(13,1) }.
#minimize{ 2@1 : use(13,2) }.
#minimize{ 2@1 : use(13,3) }.
#minimize{ 2@1 : use(14,0) }.
#minimize{ 2@1 : use(14,1) }.
#minimize{ 2@1 : use(14,2) }.
#minimize{ 2@1 : use(14,3) }.
#minimize{ 2@1 : use(15,0) }.
#minimize{ 2@1 : use(15,1) }.
#minimize{ 2@1 : use(15,2) }.
#minimize{ 2@1 : use(15,3) }.
#minimize{ 2@1 : use(16,0) }.
#minimize{ 2@1 : use(16,1) }.
#minimize{ 2@1 : use(16,2) }.
#minimize{ 2@1 : use(16,3) }.
#minimize{ 2@1 : use(17,0) }.
#minimize{ 2@1 : use(17,1) }.
#minimize{ 2@1 : use(17,2) }.
#minimize{ 2@1 : use(17,3) }.
#minimize{ 2@1 : use(18,0) }.
#minimize{ 2@1 : use(18,1) }.
#minimize{ 2@1 : use(18,2) }.
#minimize{ 2@1 : use(18,3) }.
#minimize{ 2@1 : use(19,0) }.
#minimize{ 2@1 : use(19,1) }.
#minimize{ 2@1 : use(19,2) }.
#minimize{ 2@1 : use(19,3) }.
#minimize{ 2@1 : use(20,0) }.
#minimize{ 2@1 : use(20,1) }.
#minimize{ 2@1 : use(20,2) }.
#minimize{ 2@1 : use(20,3) }.
#minimize{ 2@1 : use(21,0) }.
#minimize{ 2@1 : use(21,1) }.
#minimize{ 2@1 : use(21,2) }.
#minimize{ 2@1 : use(21,3) }.
#minimize{ 2@1 : use(22,0) }.
#minimize{ 2@1 : use(22,1) }.
#minimize{ 2@1 : use(22,2) }.
#minimize{ 2@1 : use(22,3) }.
#minimize{ 2@1 : use(23,0) }.
#minimize{ 2@1 : use(23,1) }.
#minimize{ 2@1 : use(23,2) }.
#minimize{ 2@1 : use(23,3) }.
#minimize{ 2@1 : use(24,0) }.
#minimize{ 2@1 : use(24,1) }.
#minimize{ 2@1 : use(24,2) }.
#minimize{ 2@1 : use(24,3) }.
#minimize{ 2@1 : use(25,0) }.
#minimize{ 2@1 : use(25,1) }.
#minimize{ 2@1 : use(25,2) }.
#minimize{ 2@1 : use(25,3) }.
#minimize{ 2@1 : use(26,0) }.
#minimize{ 2@1 : use(26,1) }.
#minimize{ 2@1 : use(26,2) }.
#minimize{ 2@1 : use(26,3) }.
#minimize{ 2@1 : use(27,0) }.
#minimize{ 2@1 : use(27,1) }.
#minimize{ 2@1 : use(27,2) }.
#minimize{ 2@1 : use(27,3) }.
#minimize{ 2@1 : use(28,0) }.
#minimize{ 2@1 : use(28,1) }.
#minimize{ 2@1 : use(28,2) }.
#minimize{ 2@1 : use(28,3) }.
#minimize{ 2@1 : use(29,0) }.
#minimize{ 2@1 : use(29,1) }.
#minimize{ 2@1 : use(29,2) }.
#minimize{ 2@1 : use(29,3) }.
#minimize{ 2@1 : use(30,0) }.
#minimize{ 2@1 : use(30,1) }.
#minimize{ 2@1 : use(30,2) }.
#minimize{ 2@1 : use(30,3) }.
#minimize{ 2@1 : use(31,0) }.
#minimize{ 2@1 : use(31,1) }.
#minimize{ 2@1 : use(31,2) }.
#minimize{ 2@1 : use(31,3) }.
#minimize{ 2@1 : use(32,0) }.
#minimize{ 2@1 : use(32,1) }.
#minimize{ 2@1 : use(32,2) }.
#minimize{ 2@1 : use(32,3) }.
#minimize{ 2@1 : use(33,0) }.
#minimize{ 2@1 : use(33,1) }.
#minimize{ 2@1 : use(33,2) }.
#minimize{ 2@1 : use(33,3) }.
#minimize{ 2@1 : use(34,0) }.
#minimize{ 2@1 : use(34,1) }.
#minimize{ 2@1 : use(34,2) }.
#minimize{ 2@1 : use(34,3) }.
#minimize{ 2@1 : use(35,0) }.
#minimize{ 2@1 : use(35,1) }.
#minimize{ 2@1 : use(35,2) }.
#minimize{ 2@1 : use(35,3) }.
#minimize{ 2@1 : use(36,0) }.
#minimize{ 2@1 : use(36,1) }.
#minimize{ 2@1 : use(36,2) }.
#minimize{ 2@1 : use(36,3) }.
#minimize{ 2@1 : use(37,0) }.
#minimize{ 2@1 : use(37,1) }.
#minimize{ 2@1 : use(37,2) }.
#minimize{ 2@1 : use(37,3) }.
#minimize{ 2@1 : use(38,0) }.
#minimize{ 2@1 : use(38,1) }.
#minimize{ 2@1 : use(38,2) }.
#minimize{ 2@1 : use(38,3) }.
#minimize{ 2@1 : use(39,0) }.
#minimize{ 2@1 : use(39,1) }.
#minimize{ 2@1 : use(39,2) }.
#minimize{ 2@1 : use(39,3) }.
#minimize{ 2@1 : use(40,0) }.
#minimize{ 2@1 : use(40,1) }.
#minimize{ 2@1 : use(40,2) }.
#minimize{ 2@1 : use(40,3) }.
#minimize{ 2@1 : use(41,0) }.
#minimize{ 2@1 : use(41,1) }.
#minimize{ 2@1 : use(41,2) }.
#minimize{ 2@1 : use(41,3) }.
#minimize{ 2@1 : use(42,0) }.
#minimize{ 2@1 : use(42,1) }.
#minimize{ 2@1 : use(42,2) }.
#minimize{ 2@1 : use(42,3) }.
#minimize{ 2@1 : use(43,0) }.
#minimize{ 2@1 : use(43,1) }.
#minimize{ 2@1 : use(43,2) }.
#minimize{ 2@1 : use(43,3) }.
#minimize{ 2@1 : use(44,0) }.
#minimize{ 2@1 : use(44,1) }.
#minimize{ 2@1 : use(44,2) }.
#minimize{ 2@1 : use(44,3) }.
#minimize{ 2@1 : use(45,0) }.
#minimize{ 2@1 : use(45,1) }.
#minimize{ 2@1 : use(45,2) }.
#minimize{ 2@1 : use(45,3) }.
#minimize{ 2@1 : use(46,0) }.
#minimize{ 2@1 : use(46,1) }.
#minimize{ 2@1 : use(46,2) }.
#minimize{ 2@1 : use(46,3) }.
#minimize{ 2@1 : use(47,0) }.
#minimize{ 2@1 : use(47,1) }.
#minimize{ 2@1 : use(47,2) }.
#minimize{ 2@1 : use(47,3) }.
#minimize{ 2@1 : use(48,0) }.
#minimize{ 2@1 : use(48,1) }.
#minimize{ 2@1 : use(48,2) }.
#minimize{ 2@1 : use(48,3) }.
#minimize{ 2@1 : use(49,0) }.
#minimize{ 2@1 : use(49,1) }.
#minimize{ 2@1 : use(49,2) }.
#minimize{ 2@1 : use(49,3) }.
#minimize{ 2@1 : use(50,0) }.
#minimize{ 2@1 : use(50,1) }.
#minimize{ 2@1 : use(50,2) }.
#minimize{ 2@1 : use(50,3) }.
#minimize{ 2@1 : use(51,0) }.
#minimize{ 2@1 : use(51,1) }.
#minimize{ 2@1 : use(51,2) }.
#minimize{ 2@1 : use(51,3) }.
#minimize{ 2@1 : use(52,0) }.
#minimize{ 2@1 : use(52,1) }.
#minimize{ 2@1 : use(52,2) }.
#minimize{ 2@1 : use(52,3) }.
#minimize{ 2@1 : use(53,0) }.
#minimize{ 2@1 : use(53,1) }.
#minimize{ 2@1 : use(53,2) }.
#minimize{ 2@1 : use(53,3) }.
#minimize{ 2@1 : use(54,0) }.
#minimize{ 2@1 : use(54,1) }.
#minimize{ 2@1 : use(54,2) }.
#minimize{ 2@1 : use(54,3) }.
#minimize{ 2@1 : use(55,0) }.
#minimize{ 2@1 : use(55,1) }.
#minimize{ 2@1 : use(55,2) }.
#minimize{ 2@1 : use(55,3) }.
#minimize{ 2@1 : use(56,0) }.
#minimize{ 2@1 : use(56,1) }.
#minimize{ 2@1 : use(56,2) }.
#minimize{ 2@1 : use(56,3) }.
#minimize{ 2@1 : use(57,0) }.
#minimize{ 2@1 : use(57,1) }.
#minimize{ 2@1 : use(57,2) }.
#minimize{ 2@1 : use(57,3) }.
#minimize{ 2@1 : use(58,0) }.
#minimize{ 2@1 : use(58,1) }.
#minimize{ 2@1 : use(58,2) }.
#minimize{ 2@1 : use(58,3) }.
#minimize{ 2@1 : use(59,0) }.
#minimize{ 2@1 : use(59,1) }.
#minimize{ 2@1 : use(59,2) }.
#minimize{ 2@1 : use(59,3) }.
#minimize{ 2@1 : use(60,0) }.
#minimize{ 2@1 : use(60,1) }.
#minimize{ 2@1 : use(60,2) }.
#minimize{ 2@1 : use(60,3) }.
#minimize{ 2@1 : use(61,0) }.
#minimize{ 2@1 : use(61,1) }.
#minimize{ 2@1 : use(61,2) }.
#minimize{ 2@1 : use(61,3) }.
#minimize{ 2@1 : use(62,0) }.
#minimize{ 2@1 : use(62,1) }.
#minimize{ 2@1 : use(62,2) }.
#minimize{ 2@1 : use(62,3) }.
#minimize{ 2@1 : use(63,0) }.
#minimize{ 2@1 : use(63,1) }.
#minimize{ 2@1 : use(63,2) }.
#minimize{ 2@1 : use(63,3) }.
#minimize{ 2@1 : use(64,0) }.
#minimize{ 2@1 : use(64,1) }.
#minimize{ 2@1 : use(64,2) }.
#minimize{ 2@1 : use(64,3) }.
#minimize{ 2@1 : use(65,0) }.
#minimize{ 2@1 : use(65,1) }.
#minimize{ 2@1 : use(65,2) }.
#minimize{ 2@1 : use(65,3) }.
#minimize{ 2@1 : use(66,0) }.
#minimize{ 2@1 : use(66,1) }.
#minimize{ 2@1 : use(66,2) }.
#minimize{ 2@1 : use(66,3) }.
#minimize{ 2@1 : use(67,0) }.
#minimize{ 2@1 : use(67,1) }.
#minimize{ 2@1 : use(67,2) }.
#minimize{ 2@1 : use(67,3) }.
#minimize{ 2@1 : use(68,0) }.
#minimize{ 2@1 : use(68,1) }.
#minimize{ 2@1 : use(68,2) }.
#minimize{ 2@1 : use(68,3) }.
#minimize{ 2@1 : use(69,0) }.
#minimize{ 2@1 : use(69,1) }.
#minimize{ 2@1 : use(69,2) }.
#minimize{ 2@1 : use(69,3) }.
#minimize{ 2@1 : use(70,0) }.
#minimize{ 2@1 : use(70,1) }.
#minimize{ 2@1 : use(70,2) }.
#minimize{ 2@1 : use(70,3) }.
#minimize{ 2@1 : use(71,0) }.
#minimize{ 2@1 : use(71,1) }.
#minimize{ 2@1 : use(71,2) }.
#minimize{ 2@1 : use(71,3) }.
#minimize{ 2@1 : use(72,0) }.
#minimize{ 2@1 : use(72,1) }.
#minimize{ 2@1 : use(72,2) }.
#minimize{ 2@1 : use(72,3) }.
#minimize{ 2@1 : use(73,0) }.
#minimize{ 2@1 : use(73,1) }.
#minimize{ 2@1 : use(73,2) }.
#minimize{ 2@1 : use(73,3) }.
#minimize{ 2@1 : use(74,0) }.
#minimize{ 2@1 : use(74,1) }.
#minimize{ 2@1 : use(74,2) }.
#minimize{ 2@1 : use(74,3) }.
#minimize{ 2@1 : use(75,0) }.
#minimize{ 2@1 : use(75,1) }.
#minimize{ 2@1 : use(75,2) }.
#minimize{ 2@1 : use(75,3) }.
#minimize{ 2@1 : use(76,0) }.
#minimize{ 2@1 : use(76,1) }.
#minimize{ 2@1 : use(76,2) }.
#minimize{ 2@1 : use(76,3) }.
#minimize{ 2@1 : use(77,0) }.
#minimize{ 2@1 : use(77,1) }.
#minimize{ 2@1 : use(77,2) }.
#minimize{ 2@1 : use(77,3) }.
#minimize{ 2@1 : use(78,0) }.
#minimize{ 2@1 : use(78,1) }.
#minimize{ 2@1 : use(78,2) }.
#minimize{ 2@1 : use(78,3) }.
#minimize{ 2@1 : use(79,0) }.
#minimize{ 2@1 : use(79,1) }.
#minimize{ 2@1 : use(79,2) }.
#minimize{ 2@1 : use(79,3) }.
#minimize{ 2@1 : use(80,0) }.
#minimize{ 2@1 : use(80,1) }.
#minimize{ 2@1 : use(80,2) }.
#minimize{ 2@1 : use(80,3) }.
#minimize{ 2@1 : use(81,0) }.
#minimize{ 2@1 : use(81,1) }.
#minimize{ 2@1 : use(81,2) }.
#minimize{ 2@1 : use(81,3) }.
#minimize{ 2@1 : use(82,0) }.
#minimize{ 2@1 : use(82,1) }.
#minimize{ 2@1 : use(82,2) }.
#minimize{ 2@1 : use(82,3) }.
#minimize{ 2@1 : use(83,0) }.
#minimize{ 2@1 : use(83,1) }.
#minimize{ 2@1 : use(83,2) }.
#minimize{ 2@1 : use(83,3) }.
#minimize{ 2@1 : use(84,0) }.
#minimize{ 2@1 : use(84,1) }.
#minimize{ 2@1 : use(84,2) }.
#minimize{ 2@1 : use(84,3) }.
#minimize{ 2@1 : use(85,0) }.
#minimize{ 2@1 : use(85,1) }.
#minimize{ 2@1 : use(85,2) }.
#minimize{ 2@1 : use(85,3) }.
#minimize{ 2@1 : use(86,0) }.
#minimize{ 2@1 : use(86,1) }.
#minimize{ 2@1 : use(86,2) }.
#minimize{ 2@1 : use(86,3) }.
#minimize{ 2@1 : use(87,0) }.
#minimize{ 2@1 : use(87,1) }.
#minimize{ 2@1 : use(87,2) }.
#minimize{ 2@1 : use(87,3) }.
#minimize{ 2@1 : use(88,0) }.
#minimize{ 2@1 : use(88,1) }.
#minimize{ 2@1 : use(88,2) }.
#minimize{ 2@1 : use(88,3) }.
#minimize{ 2@1 : use(89,0) }.
#minimize{ 2@1 : use(89,1) }.
#minimize{ 2@1 : use(89,2) }.
#minimize{ 2@1 : use(89,3) }.
#minimize{ 2@1 : use(90,0) }.
#minimize{ 2@1 : use(90,1) }.
#minimize{ 2@1 : use(90,2) }.
#minimize{ 2@1 : use(90,3) }.
#minimize{ 2@1 : use(91,0) }.
#minimize{ 2@1 : use(91,1) }.
#minimize{ 2@1 : use(91,2) }.
#minimize{ 2@1 : use(91,3) }.
#minimize{ 2@1 : use(92,0) }.
#minimize{ 2@1 : use(92,1) }.
#minimize{ 2@1 : use(92,2) }.
#minimize{ 2@1 : use(92,3) }.
#minimize{ 2@1 : use(93,0) }.
#minimize{ 2@1 : use(93,1) }.
#minimize{ 2@1 : use(93,2) }.
#minimize{ 2@1 : use(93,3) }.
#minimize{ 2@1 : use(94,0) }.
#minimize{ 2@1 : use(94,1) }.
#minimize{ 2@1 : use(94,2) }.
#minimize{ 2@1 : use(94,3) }.
#minimize{ 2@1 : use(95,0) }.
#minimize{ 2@1 : use(95,1) }.
#minimize{ 2@1 : use(95,2) }.
#minimize{ 2@1 : use(95,3) }.
#minimize{ 2@1 : use(96,0) }.
#minimize{ 2@1 : use(96,1) }.
#minimize{ 2@1 : use(96,2) }.
#minimize{ 2@1 : use(96,3) }.
#minimize{ 2@1 : use(97,0) }.
#minimize{ 2@1 : use(97,1) }.
#minimize{ 2@1 : use(97,2) }.
#minimize{ 2@1 : use(97,3) }.
#minimize{ 2@1 : use(98,0) }.
#minimize{ 2@1 : use(98,1) }.
#minimize{ 2@1 : use(98,2) }.
#minimize{ 2@1 : use(98,3) }.
#minimize{ 2@1 : use(99,0) }.
#minimize{ 2@1 : use(99,1) }.
#minimize{ 2@1 : use(99,2) }.
#minimize{ 2@1 : use(99,3) }.
#minimize{ 2@1 : use(100,0) }.
#minimize{ 2@1 : use(100,1) }.
#minimize{ 2@1 : use(100,2) }.
#minimize{ 2@1 : use(100,3) }.
#minimize{ 2@1 : use(101,0) }.
#minimize{ 2@1 : use(101,1) }.
#minimize{ 2@1 : use(101,2) }.
#minimize{ 2@1 : use(101,3) }.
#minimize{ 2@1 : use(102,0) }.
#minimize{ 2@1 : use(102,1) }.
#minimize{ 2@1 : use(102,2) }.
#minimize{ 2@1 : use(102,3) }.
#minimize{ 2@1 : use(103,0) }.
#minimize{ 2@1 : use(103,1) }.
#minimize{ 2@1 : use(103,2) }.
#minimize{ 2@1 : use(103,3) }.
#minimize{ 2@1 : use(104,0) }.
#minimize{ 2@1 : use(104,1) }.
#minimize{ 2@1 : use(104,2) }.
#minimize{ 2@1 : use(104,3) }.
#minimize{ 2@1 : use(105,0) }.
#minimize{ 2@1 : use(105,1) }.
#minimize{ 2@1 : use(105,2) }.
#minimize{ 2@1 : use(105,3) }.
#minimize{ 2@1 : use(106,0) }.
#minimize{ 2@1 : use(106,1) }.
#minimize{ 2@1 : use(106,2) }.
#minimize{ 2@1 : use(106,3) }.
#minimize{ 2@1 : use(107,0) }.
#minimize{ 2@1 : use(107,1) }.
#minimize{ 2@1 : use(107,2) }.
#minimize{ 2@1 : use(107,3) }.

try(0, 1, V3, V2) :- use(0, 1), atlight(V3,V2), car(V3), light(V2).
try(0, 1, V3, V2) :- not use(0, 1), car(V3), light(V2).
try(0, 2, V1) :- use(0, 2), red(V1), light(V1).
try(0, 2, V1) :- not use(0, 2), light(V1).
try(0, 3, V3, V2) :- use(0, 3), atlight(V3,V2), car(V3), light(V2).
try(0, 3, V3, V2) :- not use(0, 3), car(V3), light(V2).
try(1, 1, V3, V2) :- use(1, 1), atlight(V3,V2), car(V3), light(V2).
try(1, 1, V3, V2) :- not use(1, 1), car(V3), light(V2).
try(1, 2, V1) :- use(1, 2), red(V1), light(V1).
try(1, 2, V1) :- not use(1, 2), light(V1).
try(1, 3, V3, V1) :- use(1, 3), not atlight(V3,V1), car(V3), light(V1).
try(1, 3, V3, V1) :- not use(1, 3), car(V3), light(V1).
try(2, 1, V3, V2) :- use(2, 1), atlight(V3,V2), car(V3), light(V2).
try(2, 1, V3, V2) :- not use(2, 1), car(V3), light(V2).
try(2, 2, V1) :- use(2, 2), red(V1), light(V1).
try(2, 2, V1) :- not use(2, 2), light(V1).
try(2, 3, V3, V4) :- use(2, 3), not atlight(V3,V4), car(V3), light(V4).
try(2, 3, V3, V4) :- not use(2, 3), car(V3), light(V4).
try(3, 1, V3, V2) :- use(3, 1), atlight(V3,V2), car(V3), light(V2).
try(3, 1, V3, V2) :- not use(3, 1), car(V3), light(V2).
try(3, 2, V1) :- use(3, 2), red(V1), light(V1).
try(3, 2, V1) :- not use(3, 2), light(V1).
try(3, 3, V2) :- use(3, 3), not red(V2), light(V2).
try(3, 3, V2) :- not use(3, 3), light(V2).
try(4, 1, V3, V2) :- use(4, 1), atlight(V3,V2), car(V3), light(V2).
try(4, 1, V3, V2) :- not use(4, 1), car(V3), light(V2).
try(4, 2, V1) :- use(4, 2), red(V1), light(V1).
try(4, 2, V1) :- not use(4, 2), light(V1).
try(4, 3, V4) :- use(4, 3), not red(V4), light(V4).
try(4, 3, V4) :- not use(4, 3), light(V4).
try(5, 1, V3, V2) :- use(5, 1), atlight(V3,V2), car(V3), light(V2).
try(5, 1, V3, V2) :- not use(5, 1), car(V3), light(V2).
try(5, 2, V1) :- use(5, 2), red(V1), light(V1).
try(5, 2, V1) :- not use(5, 2), light(V1).
try(5, 3, V3) :- use(5, 3), not emergency(V3), car(V3).
try(5, 3, V3) :- not use(5, 3), car(V3).
try(6, 1, V3, V2) :- use(6, 1), atlight(V3,V2), car(V3), light(V2).
try(6, 1, V3, V2) :- not use(6, 1), car(V3), light(V2).
try(6, 2, V3, V1) :- use(6, 2), not atlight(V3,V1), car(V3), light(V1).
try(6, 2, V3, V1) :- not use(6, 2), car(V3), light(V1).
try(6, 3, V3, V2) :- use(6, 3), atlight(V3,V2), car(V3), light(V2).
try(6, 3, V3, V2) :- not use(6, 3), car(V3), light(V2).
try(7, 1, V3, V2) :- use(7, 1), atlight(V3,V2), car(V3), light(V2).
try(7, 1, V3, V2) :- not use(7, 1), car(V3), light(V2).
try(7, 2, V3, V1) :- use(7, 2), not atlight(V3,V1), car(V3), light(V1).
try(7, 2, V3, V1) :- not use(7, 2), car(V3), light(V1).
try(7, 3, V1) :- use(7, 3), red(V1), light(V1).
try(7, 3, V1) :- not use(7, 3), light(V1).
try(8, 1, V3, V2) :- use(8, 1), atlight(V3,V2), car(V3), light(V2).
try(8, 1, V3, V2) :- not use(8, 1), car(V3), light(V2).
try(8, 2, V3, V1) :- use(8, 2), not atlight(V3,V1), car(V3), light(V1).
try(8, 2, V3, V1) :- not use(8, 2), car(V3), light(V1).
try(8, 3, V3, V4) :- use(8, 3), not atlight(V3,V4), car(V3), light(V4).
try(8, 3, V3, V4) :- not use(8, 3), car(V3), light(V4).
try(9, 1, V3, V2) :- use(9, 1), atlight(V3,V2), car(V3), light(V2).
try(9, 1, V3, V2) :- not use(9, 1), car(V3), light(V2).
try(9, 2, V3, V1) :- use(9, 2), not atlight(V3,V1), car(V3), light(V1).
try(9, 2, V3, V1) :- not use(9, 2), car(V3), light(V1).
try(9, 3, V2) :- use(9, 3), not red(V2), light(V2).
try(9, 3, V2) :- not use(9, 3), light(V2).
try(10, 1, V3, V2) :- use(10, 1), atlight(V3,V2), car(V3), light(V2).
try(10, 1, V3, V2) :- not use(10, 1), car(V3), light(V2).
try(10, 2, V3, V1) :- use(10, 2), not atlight(V3,V1), car(V3), light(V1).
try(10, 2, V3, V1) :- not use(10, 2), car(V3), light(V1).
try(10, 3, V4) :- use(10, 3), not red(V4), light(V4).
try(10, 3, V4) :- not use(10, 3), light(V4).
try(11, 1, V3, V2) :- use(11, 1), atlight(V3,V2), car(V3), light(V2).
try(11, 1, V3, V2) :- not use(11, 1), car(V3), light(V2).
try(11, 2, V3, V1) :- use(11, 2), not atlight(V3,V1), car(V3), light(V1).
try(11, 2, V3, V1) :- not use(11, 2), car(V3), light(V1).
try(11, 3, V3) :- use(11, 3), not emergency(V3), car(V3).
try(11, 3, V3) :- not use(11, 3), car(V3).
try(12, 1, V2, V1) :- use(12, 1), atlight(V2,V1), car(V2), light(V1).
try(12, 1, V2, V1) :- not use(12, 1), car(V2), light(V1).
try(12, 2, V2, V3) :- use(12, 2), not atlight(V2,V3), car(V2), light(V3).
try(12, 2, V2, V3) :- not use(12, 2), car(V2), light(V3).
try(12, 3, V2, V1) :- use(12, 3), atlight(V2,V1), car(V2), light(V1).
try(12, 3, V2, V1) :- not use(12, 3), car(V2), light(V1).
try(13, 1, V3, V2) :- use(13, 1), atlight(V3,V2), car(V3), light(V2).
try(13, 1, V3, V2) :- not use(13, 1), car(V3), light(V2).
try(13, 2, V3, V4) :- use(13, 2), not atlight(V3,V4), car(V3), light(V4).
try(13, 2, V3, V4) :- not use(13, 2), car(V3), light(V4).
try(13, 3, V1) :- use(13, 3), red(V1), light(V1).
try(13, 3, V1) :- not use(13, 3), light(V1).
try(14, 1, V3, V2) :- use(14, 1), atlight(V3,V2), car(V3), light(V2).
try(14, 1, V3, V2) :- not use(14, 1), car(V3), light(V2).
try(14, 2, V3, V4) :- use(14, 2), not atlight(V3,V4), car(V3), light(V4).
try(14, 2, V3, V4) :- not use(14, 2), car(V3), light(V4).
try(14, 3, V3, V1) :- use(14, 3), not atlight(V3,V1), car(V3), light(V1).
try(14, 3, V3, V1) :- not use(14, 3), car(V3), light(V1).
try(15, 1, V2, V1) :- use(15, 1), atlight(V2,V1), car(V2), light(V1).
try(15, 1, V2, V1) :- not use(15, 1), car(V2), light(V1).
try(15, 2, V2, V3) :- use(15, 2), not atlight(V2,V3), car(V2), light(V3).
try(15, 2, V2, V3) :- not use(15, 2), car(V2), light(V3).
try(15, 3, V1) :- use(15, 3), not red(V1), light(V1).
try(15, 3, V1) :- not use(15, 3), light(V1).
try(16, 1, V2, V1) :- use(16, 1), atlight(V2,V1), car(V2), light(V1).
try(16, 1, V2, V1) :- not use(16, 1), car(V2), light(V1).
try(16, 2, V2, V3) :- use(16, 2), not atlight(V2,V3), car(V2), light(V3).
try(16, 2, V2, V3) :- not use(16, 2), car(V2), light(V3).
try(16, 3, V3) :- use(16, 3), not red(V3), light(V3).
try(16, 3, V3) :- not use(16, 3), light(V3).
try(17, 1, V2, V1) :- use(17, 1), atlight(V2,V1), car(V2), light(V1).
try(17, 1, V2, V1) :- not use(17, 1), car(V2), light(V1).
try(17, 2, V2, V3) :- use(17, 2), not atlight(V2,V3), car(V2), light(V3).
try(17, 2, V2, V3) :- not use(17, 2), car(V2), light(V3).
try(17, 3, V2) :- use(17, 3), not emergency(V2), car(V2).
try(17, 3, V2) :- not use(17, 3), car(V2).
try(18, 1, V2, V1) :- use(18, 1), atlight(V2,V1), car(V2), light(V1).
try(18, 1, V2, V1) :- not use(18, 1), car(V2), light(V1).
try(18, 2, V1) :- use(18, 2), not red(V1), light(V1).
try(18, 2, V1) :- not use(18, 2), light(V1).
try(18, 3, V2, V1) :- use(18, 3), atlight(V2,V1), car(V2), light(V1).
try(18, 3, V2, V1) :- not use(18, 3), car(V2), light(V1).
try(19, 1, V3, V2) :- use(19, 1), atlight(V3,V2), car(V3), light(V2).
try(19, 1, V3, V2) :- not use(19, 1), car(V3), light(V2).
try(19, 2, V2) :- use(19, 2), not red(V2), light(V2).
try(19, 2, V2) :- not use(19, 2), light(V2).
try(19, 3, V1) :- use(19, 3), red(V1), light(V1).
try(19, 3, V1) :- not use(19, 3), light(V1).
try(20, 1, V3, V2) :- use(20, 1), atlight(V3,V2), car(V3), light(V2).
try(20, 1, V3, V2) :- not use(20, 1), car(V3), light(V2).
try(20, 2, V2) :- use(20, 2), not red(V2), light(V2).
try(20, 2, V2) :- not use(20, 2), light(V2).
try(20, 3, V3, V1) :- use(20, 3), not atlight(V3,V1), car(V3), light(V1).
try(20, 3, V3, V1) :- not use(20, 3), car(V3), light(V1).
try(21, 1, V2, V1) :- use(21, 1), atlight(V2,V1), car(V2), light(V1).
try(21, 1, V2, V1) :- not use(21, 1), car(V2), light(V1).
try(21, 2, V1) :- use(21, 2), not red(V1), light(V1).
try(21, 2, V1) :- not use(21, 2), light(V1).
try(21, 3, V2, V3) :- use(21, 3), not atlight(V2,V3), car(V2), light(V3).
try(21, 3, V2, V3) :- not use(21, 3), car(V2), light(V3).
try(22, 1, V2, V1) :- use(22, 1), atlight(V2,V1), car(V2), light(V1).
try(22, 1, V2, V1) :- not use(22, 1), car(V2), light(V1).
try(22, 2, V1) :- use(22, 2), not red(V1), light(V1).
try(22, 2, V1) :- not use(22, 2), light(V1).
try(22, 3, V3) :- use(22, 3), not red(V3), light(V3).
try(22, 3, V3) :- not use(22, 3), light(V3).
try(23, 1, V2, V1) :- use(23, 1), atlight(V2,V1), car(V2), light(V1).
try(23, 1, V2, V1) :- not use(23, 1), car(V2), light(V1).
try(23, 2, V1) :- use(23, 2), not red(V1), light(V1).
try(23, 2, V1) :- not use(23, 2), light(V1).
try(23, 3, V2) :- use(23, 3), not emergency(V2), car(V2).
try(23, 3, V2) :- not use(23, 3), car(V2).
try(24, 1, V2, V1) :- use(24, 1), atlight(V2,V1), car(V2), light(V1).
try(24, 1, V2, V1) :- not use(24, 1), car(V2), light(V1).
try(24, 2, V3) :- use(24, 2), not red(V3), light(V3).
try(24, 2, V3) :- not use(24, 2), light(V3).
try(24, 3, V2, V1) :- use(24, 3), atlight(V2,V1), car(V2), light(V1).
try(24, 3, V2, V1) :- not use(24, 3), car(V2), light(V1).
try(25, 1, V3, V2) :- use(25, 1), atlight(V3,V2), car(V3), light(V2).
try(25, 1, V3, V2) :- not use(25, 1), car(V3), light(V2).
try(25, 2, V4) :- use(25, 2), not red(V4), light(V4).
try(25, 2, V4) :- not use(25, 2), light(V4).
try(25, 3, V1) :- use(25, 3), red(V1), light(V1).
try(25, 3, V1) :- not use(25, 3), light(V1).
try(26, 1, V3, V2) :- use(26, 1), atlight(V3,V2), car(V3), light(V2).
try(26, 1, V3, V2) :- not use(26, 1), car(V3), light(V2).
try(26, 2, V4) :- use(26, 2), not red(V4), light(V4).
try(26, 2, V4) :- not use(26, 2), light(V4).
try(26, 3, V3, V1) :- use(26, 3), not atlight(V3,V1), car(V3), light(V1).
try(26, 3, V3, V1) :- not use(26, 3), car(V3), light(V1).
try(27, 1, V2, V1) :- use(27, 1), atlight(V2,V1), car(V2), light(V1).
try(27, 1, V2, V1) :- not use(27, 1), car(V2), light(V1).
try(27, 2, V3) :- use(27, 2), not red(V3), light(V3).
try(27, 2, V3) :- not use(27, 2), light(V3).
try(27, 3, V2, V3) :- use(27, 3), not atlight(V2,V3), car(V2), light(V3).
try(27, 3, V2, V3) :- not use(27, 3), car(V2), light(V3).
try(28, 1, V2, V1) :- use(28, 1), atlight(V2,V1), car(V2), light(V1).
try(28, 1, V2, V1) :- not use(28, 1), car(V2), light(V1).
try(28, 2, V3) :- use(28, 2), not red(V3), light(V3).
try(28, 2, V3) :- not use(28, 2), light(V3).
try(28, 3, V1) :- use(28, 3), not red(V1), light(V1).
try(28, 3, V1) :- not use(28, 3), light(V1).
try(29, 1, V2, V1) :- use(29, 1), atlight(V2,V1), car(V2), light(V1).
try(29, 1, V2, V1) :- not use(29, 1), car(V2), light(V1).
try(29, 2, V3) :- use(29, 2), not red(V3), light(V3).
try(29, 2, V3) :- not use(29, 2), light(V3).
try(29, 3, V2) :- use(29, 3), not emergency(V2), car(V2).
try(29, 3, V2) :- not use(29, 3), car(V2).
try(30, 1, V2, V1) :- use(30, 1), atlight(V2,V1), car(V2), light(V1).
try(30, 1, V2, V1) :- not use(30, 1), car(V2), light(V1).
try(30, 2, V2) :- use(30, 2), not emergency(V2), car(V2).
try(30, 2, V2) :- not use(30, 2), car(V2).
try(30, 3, V2, V1) :- use(30, 3), atlight(V2,V1), car(V2), light(V1).
try(30, 3, V2, V1) :- not use(30, 3), car(V2), light(V1).
try(31, 1, V3, V2) :- use(31, 1), atlight(V3,V2), car(V3), light(V2).
try(31, 1, V3, V2) :- not use(31, 1), car(V3), light(V2).
try(31, 2, V3) :- use(31, 2), not emergency(V3), car(V3).
try(31, 2, V3) :- not use(31, 2), car(V3).
try(31, 3, V1) :- use(31, 3), red(V1), light(V1).
try(31, 3, V1) :- not use(31, 3), light(V1).
try(32, 1, V3, V2) :- use(32, 1), atlight(V3,V2), car(V3), light(V2).
try(32, 1, V3, V2) :- not use(32, 1), car(V3), light(V2).
try(32, 2, V3) :- use(32, 2), not emergency(V3), car(V3).
try(32, 2, V3) :- not use(32, 2), car(V3).
try(32, 3, V3, V1) :- use(32, 3), not atlight(V3,V1), car(V3), light(V1).
try(32, 3, V3, V1) :- not use(32, 3), car(V3), light(V1).
try(33, 1, V2, V1) :- use(33, 1), atlight(V2,V1), car(V2), light(V1).
try(33, 1, V2, V1) :- not use(33, 1), car(V2), light(V1).
try(33, 2, V2) :- use(33, 2), not emergency(V2), car(V2).
try(33, 2, V2) :- not use(33, 2), car(V2).
try(33, 3, V2, V3) :- use(33, 3), not atlight(V2,V3), car(V2), light(V3).
try(33, 3, V2, V3) :- not use(33, 3), car(V2), light(V3).
try(34, 1, V2, V1) :- use(34, 1), atlight(V2,V1), car(V2), light(V1).
try(34, 1, V2, V1) :- not use(34, 1), car(V2), light(V1).
try(34, 2, V2) :- use(34, 2), not emergency(V2), car(V2).
try(34, 2, V2) :- not use(34, 2), car(V2).
try(34, 3, V1) :- use(34, 3), not red(V1), light(V1).
try(34, 3, V1) :- not use(34, 3), light(V1).
try(35, 1, V2, V1) :- use(35, 1), atlight(V2,V1), car(V2), light(V1).
try(35, 1, V2, V1) :- not use(35, 1), car(V2), light(V1).
try(35, 2, V2) :- use(35, 2), not emergency(V2), car(V2).
try(35, 2, V2) :- not use(35, 2), car(V2).
try(35, 3, V3) :- use(35, 3), not red(V3), light(V3).
try(35, 3, V3) :- not use(35, 3), light(V3).
try(36, 1, V2, V1) :- use(36, 1), not atlight(V2,V1), car(V2), light(V1).
try(36, 1, V2, V1) :- not use(36, 1), car(V2), light(V1).
try(36, 2, V2, V3) :- use(36, 2), atlight(V2,V3), car(V2), light(V3).
try(36, 2, V2, V3) :- not use(36, 2), car(V2), light(V3).
try(36, 3, V1) :- use(36, 3), red(V1), light(V1).
try(36, 3, V1) :- not use(36, 3), light(V1).
try(37, 1, V2, V1) :- use(37, 1), not atlight(V2,V1), car(V2), light(V1).
try(37, 1, V2, V1) :- not use(37, 1), car(V2), light(V1).
try(37, 2, V2, V3) :- use(37, 2), atlight(V2,V3), car(V2), light(V3).
try(37, 2, V2, V3) :- not use(37, 2), car(V2), light(V3).
try(37, 3, V2, V1) :- use(37, 3), not atlight(V2,V1), car(V2), light(V1).
try(37, 3, V2, V1) :- not use(37, 3), car(V2), light(V1).
try(38, 1, V3, V2) :- use(38, 1), not atlight(V3,V2), car(V3), light(V2).
try(38, 1, V3, V2) :- not use(38, 1), car(V3), light(V2).
try(38, 2, V3, V4) :- use(38, 2), atlight(V3,V4), car(V3), light(V4).
try(38, 2, V3, V4) :- not use(38, 2), car(V3), light(V4).
try(38, 3, V3, V1) :- use(38, 3), not atlight(V3,V1), car(V3), light(V1).
try(38, 3, V3, V1) :- not use(38, 3), car(V3), light(V1).
try(39, 1, V2, V1) :- use(39, 1), not atlight(V2,V1), car(V2), light(V1).
try(39, 1, V2, V1) :- not use(39, 1), car(V2), light(V1).
try(39, 2, V2, V3) :- use(39, 2), atlight(V2,V3), car(V2), light(V3).
try(39, 2, V2, V3) :- not use(39, 2), car(V2), light(V3).
try(39, 3, V3) :- use(39, 3), not red(V3), light(V3).
try(39, 3, V3) :- not use(39, 3), light(V3).
try(40, 1, V3, V2) :- use(40, 1), not atlight(V3,V2), car(V3), light(V2).
try(40, 1, V3, V2) :- not use(40, 1), car(V3), light(V2).
try(40, 2, V3, V4) :- use(40, 2), atlight(V3,V4), car(V3), light(V4).
try(40, 2, V3, V4) :- not use(40, 2), car(V3), light(V4).
try(40, 3, V1) :- use(40, 3), not red(V1), light(V1).
try(40, 3, V1) :- not use(40, 3), light(V1).
try(41, 1, V2, V1) :- use(41, 1), not atlight(V2,V1), car(V2), light(V1).
try(41, 1, V2, V1) :- not use(41, 1), car(V2), light(V1).
try(41, 2, V2, V3) :- use(41, 2), atlight(V2,V3), car(V2), light(V3).
try(41, 2, V2, V3) :- not use(41, 2), car(V2), light(V3).
try(41, 3, V2) :- use(41, 3), not emergency(V2), car(V2).
try(41, 3, V2) :- not use(41, 3), car(V2).
try(42, 1, V4, V5) :- use(42, 1), atlight(V4,V5), car(V4), light(V5).
try(42, 1, V4, V5) :- not use(42, 1), car(V4), light(V5).
try(42, 2, V1) :- use(42, 2), red(V1), light(V1).
try(42, 2, V1) :- not use(42, 2), light(V1).
try(42, 3, V3, V2) :- use(42, 3), atlight(V3,V2), car(V3), light(V2).
try(42, 3, V3, V2) :- not use(42, 3), car(V3), light(V2).
try(43, 1, V4, V3) :- use(43, 1), atlight(V4,V3), car(V4), light(V3).
try(43, 1, V4, V3) :- not use(43, 1), car(V4), light(V3).
try(43, 2, V1) :- use(43, 2), red(V1), light(V1).
try(43, 2, V1) :- not use(43, 2), light(V1).
try(43, 3, V2, V1) :- use(43, 3), not atlight(V2,V1), car(V2), light(V1).
try(43, 3, V2, V1) :- not use(43, 3), car(V2), light(V1).
try(44, 1, V4, V3) :- use(44, 1), atlight(V4,V3), car(V4), light(V3).
try(44, 1, V4, V3) :- not use(44, 1), car(V4), light(V3).
try(44, 2, V1) :- use(44, 2), red(V1), light(V1).
try(44, 2, V1) :- not use(44, 2), light(V1).
try(44, 3, V2, V3) :- use(44, 3), not atlight(V2,V3), car(V2), light(V3).
try(44, 3, V2, V3) :- not use(44, 3), car(V2), light(V3).
try(45, 1, V4, V3) :- use(45, 1), atlight(V4,V3), car(V4), light(V3).
try(45, 1, V4, V3) :- not use(45, 1), car(V4), light(V3).
try(45, 2, V1) :- use(45, 2), red(V1), light(V1).
try(45, 2, V1) :- not use(45, 2), light(V1).
try(45, 3, V2) :- use(45, 3), not emergency(V2), car(V2).
try(45, 3, V2) :- not use(45, 3), car(V2).
try(46, 1, V1, V3) :- use(46, 1), atlight(V1,V3), car(V1), light(V3).
try(46, 1, V1, V3) :- not use(46, 1), car(V1), light(V3).
try(46, 2, V1, V2) :- use(46, 2), not atlight(V1,V2), car(V1), light(V2).
try(46, 2, V1, V2) :- not use(46, 2), car(V1), light(V2).
try(46, 3, V1, V3) :- use(46, 3), atlight(V1,V3), car(V1), light(V3).
try(46, 3, V1, V3) :- not use(46, 3), car(V1), light(V3).
try(47, 1, V1, V3) :- use(47, 1), atlight(V1,V3), car(V1), light(V3).
try(47, 1, V1, V3) :- not use(47, 1), car(V1), light(V3).
try(47, 2, V1, V2) :- use(47, 2), not atlight(V1,V2), car(V1), light(V2).
try(47, 2, V1, V2) :- not use(47, 2), car(V1), light(V2).
try(47, 3, V2) :- use(47, 3), red(V2), light(V2).
try(47, 3, V2) :- not use(47, 3), light(V2).
try(48, 1, V1, V3) :- use(48, 1), atlight(V1,V3), car(V1), light(V3).
try(48, 1, V1, V3) :- not use(48, 1), car(V1), light(V3).
try(48, 2, V1, V2) :- use(48, 2), not atlight(V1,V2), car(V1), light(V2).
try(48, 2, V1, V2) :- not use(48, 2), car(V1), light(V2).
try(48, 3, V1, V4) :- use(48, 3), not atlight(V1,V4), car(V1), light(V4).
try(48, 3, V1, V4) :- not use(48, 3), car(V1), light(V4).
try(49, 1, V1, V3) :- use(49, 1), atlight(V1,V3), car(V1), light(V3).
try(49, 1, V1, V3) :- not use(49, 1), car(V1), light(V3).
try(49, 2, V1, V2) :- use(49, 2), not atlight(V1,V2), car(V1), light(V2).
try(49, 2, V1, V2) :- not use(49, 2), car(V1), light(V2).
try(49, 3, V4) :- use(49, 3), not red(V4), light(V4).
try(49, 3, V4) :- not use(49, 3), light(V4).
try(50, 1, V1, V3) :- use(50, 1), atlight(V1,V3), car(V1), light(V3).
try(50, 1, V1, V3) :- not use(50, 1), car(V1), light(V3).
try(50, 2, V1, V2) :- use(50, 2), not atlight(V1,V2), car(V1), light(V2).
try(50, 2, V1, V2) :- not use(50, 2), car(V1), light(V2).
try(50, 3, V3) :- use(50, 3), not red(V3), light(V3).
try(50, 3, V3) :- not use(50, 3), light(V3).
try(51, 1, V1, V3) :- use(51, 1), atlight(V1,V3), car(V1), light(V3).
try(51, 1, V1, V3) :- not use(51, 1), car(V1), light(V3).
try(51, 2, V1, V2) :- use(51, 2), not atlight(V1,V2), car(V1), light(V2).
try(51, 2, V1, V2) :- not use(51, 2), car(V1), light(V2).
try(51, 3, V1) :- use(51, 3), not emergency(V1), car(V1).
try(51, 3, V1) :- not use(51, 3), car(V1).
try(52, 1, V1, V4) :- use(52, 1), atlight(V1,V4), car(V1), light(V4).
try(52, 1, V1, V4) :- not use(52, 1), car(V1), light(V4).
try(52, 2, V1, V3) :- use(52, 2), not atlight(V1,V3), car(V1), light(V3).
try(52, 2, V1, V3) :- not use(52, 2), car(V1), light(V3).
try(52, 3, V2) :- use(52, 3), red(V2), light(V2).
try(52, 3, V2) :- not use(52, 3), light(V2).
try(53, 1, V1, V4) :- use(53, 1), atlight(V1,V4), car(V1), light(V4).
try(53, 1, V1, V4) :- not use(53, 1), car(V1), light(V4).
try(53, 2, V1, V3) :- use(53, 2), not atlight(V1,V3), car(V1), light(V3).
try(53, 2, V1, V3) :- not use(53, 2), car(V1), light(V3).
try(53, 3, V1, V2) :- use(53, 3), not atlight(V1,V2), car(V1), light(V2).
try(53, 3, V1, V2) :- not use(53, 3), car(V1), light(V2).
try(54, 1, V1, V3) :- use(54, 1), atlight(V1,V3), car(V1), light(V3).
try(54, 1, V1, V3) :- not use(54, 1), car(V1), light(V3).
try(54, 2, V1, V2) :- use(54, 2), not atlight(V1,V2), car(V1), light(V2).
try(54, 2, V1, V2) :- not use(54, 2), car(V1), light(V2).
try(54, 3, V2) :- use(54, 3), not red(V2), light(V2).
try(54, 3, V2) :- not use(54, 3), light(V2).
try(55, 1, V3, V2) :- use(55, 1), atlight(V3,V2), car(V3), light(V2).
try(55, 1, V3, V2) :- not use(55, 1), car(V3), light(V2).
try(55, 2, V2) :- use(55, 2), not red(V2), light(V2).
try(55, 2, V2) :- not use(55, 2), light(V2).
try(55, 3, V1, V4) :- use(55, 3), atlight(V1,V4), car(V1), light(V4).
try(55, 3, V1, V4) :- not use(55, 3), car(V1), light(V4).
try(56, 1, V4, V3) :- use(56, 1), atlight(V4,V3), car(V4), light(V3).
try(56, 1, V4, V3) :- not use(56, 1), car(V4), light(V3).
try(56, 2, V3) :- use(56, 2), not red(V3), light(V3).
try(56, 2, V3) :- not use(56, 2), light(V3).
try(56, 3, V1, V2) :- use(56, 3), not atlight(V1,V2), car(V1), light(V2).
try(56, 3, V1, V2) :- not use(56, 3), car(V1), light(V2).
try(57, 1, V3, V2) :- use(57, 1), atlight(V3,V2), car(V3), light(V2).
try(57, 1, V3, V2) :- not use(57, 1), car(V3), light(V2).
try(57, 2, V2) :- use(57, 2), not red(V2), light(V2).
try(57, 2, V2) :- not use(57, 2), light(V2).
try(57, 3, V1, V2) :- use(57, 3), not atlight(V1,V2), car(V1), light(V2).
try(57, 3, V1, V2) :- not use(57, 3), car(V1), light(V2).
try(58, 1, V3, V2) :- use(58, 1), atlight(V3,V2), car(V3), light(V2).
try(58, 1, V3, V2) :- not use(58, 1), car(V3), light(V2).
try(58, 2, V2) :- use(58, 2), not red(V2), light(V2).
try(58, 2, V2) :- not use(58, 2), light(V2).
try(58, 3, V1) :- use(58, 3), not emergency(V1), car(V1).
try(58, 3, V1) :- not use(58, 3), car(V1).
try(59, 1, V3, V2) :- use(59, 1), atlight(V3,V2), car(V3), light(V2).
try(59, 1, V3, V2) :- not use(59, 1), car(V3), light(V2).
try(59, 2, V4) :- use(59, 2), not red(V4), light(V4).
try(59, 2, V4) :- not use(59, 2), light(V4).
try(59, 3, V1, V4) :- use(59, 3), atlight(V1,V4), car(V1), light(V4).
try(59, 3, V1, V4) :- not use(59, 3), car(V1), light(V4).
try(60, 1, V4, V5) :- use(60, 1), atlight(V4,V5), car(V4), light(V5).
try(60, 1, V4, V5) :- not use(60, 1), car(V4), light(V5).
try(60, 2, V2) :- use(60, 2), not red(V2), light(V2).
try(60, 2, V2) :- not use(60, 2), light(V2).
try(60, 3, V3, V1) :- use(60, 3), not atlight(V3,V1), car(V3), light(V1).
try(60, 3, V3, V1) :- not use(60, 3), car(V3), light(V1).
try(61, 1, V3, V2) :- use(61, 1), atlight(V3,V2), car(V3), light(V2).
try(61, 1, V3, V2) :- not use(61, 1), car(V3), light(V2).
try(61, 2, V4) :- use(61, 2), not red(V4), light(V4).
try(61, 2, V4) :- not use(61, 2), light(V4).
try(61, 3, V1, V2) :- use(61, 3), not atlight(V1,V2), car(V1), light(V2).
try(61, 3, V1, V2) :- not use(61, 3), car(V1), light(V2).
try(62, 1, V3, V2) :- use(62, 1), atlight(V3,V2), car(V3), light(V2).
try(62, 1, V3, V2) :- not use(62, 1), car(V3), light(V2).
try(62, 2, V4) :- use(62, 2), not red(V4), light(V4).
try(62, 2, V4) :- not use(62, 2), light(V4).
try(62, 3, V1) :- use(62, 3), not emergency(V1), car(V1).
try(62, 3, V1) :- not use(62, 3), car(V1).
try(63, 1, V1, V2) :- use(63, 1), atlight(V1,V2), car(V1), light(V2).
try(63, 1, V1, V2) :- not use(63, 1), car(V1), light(V2).
try(63, 2, V1) :- use(63, 2), not emergency(V1), car(V1).
try(63, 2, V1) :- not use(63, 2), car(V1).
try(63, 3, V1, V2) :- use(63, 3), atlight(V1,V2), car(V1), light(V2).
try(63, 3, V1, V2) :- not use(63, 3), car(V1), light(V2).
try(64, 1, V1, V3) :- use(64, 1), atlight(V1,V3), car(V1), light(V3).
try(64, 1, V1, V3) :- not use(64, 1), car(V1), light(V3).
try(64, 2, V1) :- use(64, 2), not emergency(V1), car(V1).
try(64, 2, V1) :- not use(64, 2), car(V1).
try(64, 3, V2) :- use(64, 3), red(V2), light(V2).
try(64, 3, V2) :- not use(64, 3), light(V2).
try(65, 1, V1, V3) :- use(65, 1), atlight(V1,V3), car(V1), light(V3).
try(65, 1, V1, V3) :- not use(65, 1), car(V1), light(V3).
try(65, 2, V1) :- use(65, 2), not emergency(V1), car(V1).
try(65, 2, V1) :- not use(65, 2), car(V1).
try(65, 3, V1, V2) :- use(65, 3), not atlight(V1,V2), car(V1), light(V2).
try(65, 3, V1, V2) :- not use(65, 3), car(V1), light(V2).
try(66, 1, V1, V3) :- use(66, 1), atlight(V1,V3), car(V1), light(V3).
try(66, 1, V1, V3) :- not use(66, 1), car(V1), light(V3).
try(66, 2, V1) :- use(66, 2), not emergency(V1), car(V1).
try(66, 2, V1) :- not use(66, 2), car(V1).
try(66, 3, V2) :- use(66, 3), not red(V2), light(V2).
try(66, 3, V2) :- not use(66, 3), light(V2).
try(67, 1, V1, V2) :- use(67, 1), atlight(V1,V2), car(V1), light(V2).
try(67, 1, V1, V2) :- not use(67, 1), car(V1), light(V2).
try(67, 2, V1) :- use(67, 2), not emergency(V1), car(V1).
try(67, 2, V1) :- not use(67, 2), car(V1).
try(67, 3, V2) :- use(67, 3), not red(V2), light(V2).
try(67, 3, V2) :- not use(67, 3), light(V2).
try(68, 1, V1, V2) :- use(68, 1), not atlight(V1,V2), car(V1), light(V2).
try(68, 1, V1, V2) :- not use(68, 1), car(V1), light(V2).
try(68, 2, V1, V3) :- use(68, 2), atlight(V1,V3), car(V1), light(V3).
try(68, 2, V1, V3) :- not use(68, 2), car(V1), light(V3).
try(68, 3, V2) :- use(68, 3), red(V2), light(V2).
try(68, 3, V2) :- not use(68, 3), light(V2).
try(69, 1, V1, V2) :- use(69, 1), not atlight(V1,V2), car(V1), light(V2).
try(69, 1, V1, V2) :- not use(69, 1), car(V1), light(V2).
try(69, 2, V1, V3) :- use(69, 2), atlight(V1,V3), car(V1), light(V3).
try(69, 2, V1, V3) :- not use(69, 2), car(V1), light(V3).
try(69, 3, V1, V2) :- use(69, 3), not atlight(V1,V2), car(V1), light(V2).
try(69, 3, V1, V2) :- not use(69, 3), car(V1), light(V2).
try(70, 1, V1, V2) :- use(70, 1), not atlight(V1,V2), car(V1), light(V2).
try(70, 1, V1, V2) :- not use(70, 1), car(V1), light(V2).
try(70, 2, V1, V3) :- use(70, 2), atlight(V1,V3), car(V1), light(V3).
try(70, 2, V1, V3) :- not use(70, 2), car(V1), light(V3).
try(70, 3, V1, V4) :- use(70, 3), not atlight(V1,V4), car(V1), light(V4).
try(70, 3, V1, V4) :- not use(70, 3), car(V1), light(V4).
try(71, 1, V1, V2) :- use(71, 1), not atlight(V1,V2), car(V1), light(V2).
try(71, 1, V1, V2) :- not use(71, 1), car(V1), light(V2).
try(71, 2, V1, V3) :- use(71, 2), atlight(V1,V3), car(V1), light(V3).
try(71, 2, V1, V3) :- not use(71, 2), car(V1), light(V3).
try(71, 3, V4) :- use(71, 3), not red(V4), light(V4).
try(71, 3, V4) :- not use(71, 3), light(V4).
try(72, 1, V1, V2) :- use(72, 1), not atlight(V1,V2), car(V1), light(V2).
try(72, 1, V1, V2) :- not use(72, 1), car(V1), light(V2).
try(72, 2, V1, V3) :- use(72, 2), atlight(V1,V3), car(V1), light(V3).
try(72, 2, V1, V3) :- not use(72, 2), car(V1), light(V3).
try(72, 3, V3) :- use(72, 3), not red(V3), light(V3).
try(72, 3, V3) :- not use(72, 3), light(V3).
try(73, 1, V1, V2) :- use(73, 1), not atlight(V1,V2), car(V1), light(V2).
try(73, 1, V1, V2) :- not use(73, 1), car(V1), light(V2).
try(73, 2, V1, V3) :- use(73, 2), atlight(V1,V3), car(V1), light(V3).
try(73, 2, V1, V3) :- not use(73, 2), car(V1), light(V3).
try(73, 3, V1) :- use(73, 3), not emergency(V1), car(V1).
try(73, 3, V1) :- not use(73, 3), car(V1).
try(74, 1, V3, V2) :- use(74, 1), atlight(V3,V2), car(V3), light(V2).
try(74, 1, V3, V2) :- not use(74, 1), car(V3), light(V2).
try(74, 2, V1) :- use(74, 2), red(V1), light(V1).
try(74, 2, V1) :- not use(74, 2), light(V1).
try(74, 3, V4, V1) :- use(74, 3), atlight(V4,V1), car(V4), light(V1).
try(74, 3, V4, V1) :- not use(74, 3), car(V4), light(V1).
try(75, 1, V3, V2) :- use(75, 1), atlight(V3,V2), car(V3), light(V2).
try(75, 1, V3, V2) :- not use(75, 1), car(V3), light(V2).
try(75, 2, V1) :- use(75, 2), red(V1), light(V1).
try(75, 2, V1) :- not use(75, 2), light(V1).
try(75, 3, V4) :- use(75, 3), emergency(V4), car(V4).
try(75, 3, V4) :- not use(75, 3), car(V4).
try(76, 1, V3, V2) :- use(76, 1), atlight(V3,V2), car(V3), light(V2).
try(76, 1, V3, V2) :- not use(76, 1), car(V3), light(V2).
try(76, 2, V1) :- use(76, 2), red(V1), light(V1).
try(76, 2, V1) :- not use(76, 2), light(V1).
try(76, 3, V4, V2) :- use(76, 3), not atlight(V4,V2), car(V4), light(V2).
try(76, 3, V4, V2) :- not use(76, 3), car(V4), light(V2).
try(77, 1, V4, V5) :- use(77, 1), atlight(V4,V5), car(V4), light(V5).
try(77, 1, V4, V5) :- not use(77, 1), car(V4), light(V5).
try(77, 2, V1) :- use(77, 2), red(V1), light(V1).
try(77, 2, V1) :- not use(77, 2), light(V1).
try(77, 3, V2, V3) :- use(77, 3), not atlight(V2,V3), car(V2), light(V3).
try(77, 3, V2, V3) :- not use(77, 3), car(V2), light(V3).
try(78, 1, V2, V1) :- use(78, 1), atlight(V2,V1), car(V2), light(V1).
try(78, 1, V2, V1) :- not use(78, 1), car(V2), light(V1).
try(78, 2, V2) :- use(78, 2), emergency(V2), car(V2).
try(78, 2, V2) :- not use(78, 2), car(V2).
try(78, 3, V2, V1) :- use(78, 3), atlight(V2,V1), car(V2), light(V1).
try(78, 3, V2, V1) :- not use(78, 3), car(V2), light(V1).
try(79, 1, V2, V1) :- use(79, 1), atlight(V2,V1), car(V2), light(V1).
try(79, 1, V2, V1) :- not use(79, 1), car(V2), light(V1).
try(79, 2, V2) :- use(79, 2), emergency(V2), car(V2).
try(79, 2, V2) :- not use(79, 2), car(V2).
try(79, 3, V1) :- use(79, 3), red(V1), light(V1).
try(79, 3, V1) :- not use(79, 3), light(V1).
try(80, 1, V3, V2) :- use(80, 1), atlight(V3,V2), car(V3), light(V2).
try(80, 1, V3, V2) :- not use(80, 1), car(V3), light(V2).
try(80, 2, V3) :- use(80, 2), emergency(V3), car(V3).
try(80, 2, V3) :- not use(80, 2), car(V3).
try(80, 3, V3, V1) :- use(80, 3), not atlight(V3,V1), car(V3), light(V1).
try(80, 3, V3, V1) :- not use(80, 3), car(V3), light(V1).
try(81, 1, V3, V1) :- use(81, 1), atlight(V3,V1), car(V3), light(V1).
try(81, 1, V3, V1) :- not use(81, 1), car(V3), light(V1).
try(81, 2, V3) :- use(81, 2), emergency(V3), car(V3).
try(81, 2, V3) :- not use(81, 2), car(V3).
try(81, 3, V3, V2) :- use(81, 3), not atlight(V3,V2), car(V3), light(V2).
try(81, 3, V3, V2) :- not use(81, 3), car(V3), light(V2).
try(82, 1, V3, V2) :- use(82, 1), atlight(V3,V2), car(V3), light(V2).
try(82, 1, V3, V2) :- not use(82, 1), car(V3), light(V2).
try(82, 2, V3) :- use(82, 2), emergency(V3), car(V3).
try(82, 2, V3) :- not use(82, 2), car(V3).
try(82, 3, V1) :- use(82, 3), not red(V1), light(V1).
try(82, 3, V1) :- not use(82, 3), light(V1).
try(83, 1, V3, V1) :- use(83, 1), atlight(V3,V1), car(V3), light(V1).
try(83, 1, V3, V1) :- not use(83, 1), car(V3), light(V1).
try(83, 2, V3) :- use(83, 2), emergency(V3), car(V3).
try(83, 2, V3) :- not use(83, 2), car(V3).
try(83, 3, V2) :- use(83, 3), not red(V2), light(V2).
try(83, 3, V2) :- not use(83, 3), light(V2).
try(84, 1, V3, V2) :- use(84, 1), atlight(V3,V2), car(V3), light(V2).
try(84, 1, V3, V2) :- not use(84, 1), car(V3), light(V2).
try(84, 2, V3, V1) :- use(84, 2), not atlight(V3,V1), car(V3), light(V1).
try(84, 2, V3, V1) :- not use(84, 2), car(V3), light(V1).
try(84, 3, V2) :- use(84, 3), red(V2), light(V2).
try(84, 3, V2) :- not use(84, 3), light(V2).
try(85, 1, V3, V2) :- use(85, 1), atlight(V3,V2), car(V3), light(V2).
try(85, 1, V3, V2) :- not use(85, 1), car(V3), light(V2).
try(85, 2, V3, V1) :- use(85, 2), not atlight(V3,V1), car(V3), light(V1).
try(85, 2, V3, V1) :- not use(85, 2), car(V3), light(V1).
try(85, 3, V3) :- use(85, 3), emergency(V3), car(V3).
try(85, 3, V3) :- not use(85, 3), car(V3).
try(86, 1, V4, V2) :- use(86, 1), atlight(V4,V2), car(V4), light(V2).
try(86, 1, V4, V2) :- not use(86, 1), car(V4), light(V2).
try(86, 2, V4, V1) :- use(86, 2), not atlight(V4,V1), car(V4), light(V1).
try(86, 2, V4, V1) :- not use(86, 2), car(V4), light(V1).
try(86, 3, V4, V3) :- use(86, 3), not atlight(V4,V3), car(V4), light(V3).
try(86, 3, V4, V3) :- not use(86, 3), car(V4), light(V3).
try(87, 1, V3, V2) :- use(87, 1), atlight(V3,V2), car(V3), light(V2).
try(87, 1, V3, V2) :- not use(87, 1), car(V3), light(V2).
try(87, 2, V3, V1) :- use(87, 2), not atlight(V3,V1), car(V3), light(V1).
try(87, 2, V3, V1) :- not use(87, 2), car(V3), light(V1).
try(87, 3, V1) :- use(87, 3), not red(V1), light(V1).
try(87, 3, V1) :- not use(87, 3), light(V1).
try(88, 1, V4, V2) :- use(88, 1), atlight(V4,V2), car(V4), light(V2).
try(88, 1, V4, V2) :- not use(88, 1), car(V4), light(V2).
try(88, 2, V4, V1) :- use(88, 2), not atlight(V4,V1), car(V4), light(V1).
try(88, 2, V4, V1) :- not use(88, 2), car(V4), light(V1).
try(88, 3, V3) :- use(88, 3), not red(V3), light(V3).
try(88, 3, V3) :- not use(88, 3), light(V3).
try(89, 1, V3, V1) :- use(89, 1), atlight(V3,V1), car(V3), light(V1).
try(89, 1, V3, V1) :- not use(89, 1), car(V3), light(V1).
try(89, 2, V3, V2) :- use(89, 2), not atlight(V3,V2), car(V3), light(V2).
try(89, 2, V3, V2) :- not use(89, 2), car(V3), light(V2).
try(89, 3, V3, V1) :- use(89, 3), atlight(V3,V1), car(V3), light(V1).
try(89, 3, V3, V1) :- not use(89, 3), car(V3), light(V1).
try(90, 1, V3, V1) :- use(90, 1), atlight(V3,V1), car(V3), light(V1).
try(90, 1, V3, V1) :- not use(90, 1), car(V3), light(V1).
try(90, 2, V3, V2) :- use(90, 2), not atlight(V3,V2), car(V3), light(V2).
try(90, 2, V3, V2) :- not use(90, 2), car(V3), light(V2).
try(90, 3, V1) :- use(90, 3), red(V1), light(V1).
try(90, 3, V1) :- not use(90, 3), light(V1).
try(91, 1, V3, V1) :- use(91, 1), atlight(V3,V1), car(V3), light(V1).
try(91, 1, V3, V1) :- not use(91, 1), car(V3), light(V1).
try(91, 2, V3, V2) :- use(91, 2), not atlight(V3,V2), car(V3), light(V2).
try(91, 2, V3, V2) :- not use(91, 2), car(V3), light(V2).
try(91, 3, V3) :- use(91, 3), emergency(V3), car(V3).
try(91, 3, V3) :- not use(91, 3), car(V3).
try(92, 1, V4, V2) :- use(92, 1), atlight(V4,V2), car(V4), light(V2).
try(92, 1, V4, V2) :- not use(92, 1), car(V4), light(V2).
try(92, 2, V4, V3) :- use(92, 2), not atlight(V4,V3), car(V4), light(V3).
try(92, 2, V4, V3) :- not use(92, 2), car(V4), light(V3).
try(92, 3, V4, V1) :- use(92, 3), not atlight(V4,V1), car(V4), light(V1).
try(92, 3, V4, V1) :- not use(92, 3), car(V4), light(V1).
try(93, 1, V4, V2) :- use(93, 1), atlight(V4,V2), car(V4), light(V2).
try(93, 1, V4, V2) :- not use(93, 1), car(V4), light(V2).
try(93, 2, V4, V3) :- use(93, 2), not atlight(V4,V3), car(V4), light(V3).
try(93, 2, V4, V3) :- not use(93, 2), car(V4), light(V3).
try(93, 3, V1) :- use(93, 3), not red(V1), light(V1).
try(93, 3, V1) :- not use(93, 3), light(V1).
try(94, 1, V3, V1) :- use(94, 1), atlight(V3,V1), car(V3), light(V1).
try(94, 1, V3, V1) :- not use(94, 1), car(V3), light(V1).
try(94, 2, V3, V2) :- use(94, 2), not atlight(V3,V2), car(V3), light(V2).
try(94, 2, V3, V2) :- not use(94, 2), car(V3), light(V2).
try(94, 3, V2) :- use(94, 3), not red(V2), light(V2).
try(94, 3, V2) :- not use(94, 3), light(V2).
try(95, 1, V3, V2) :- use(95, 1), atlight(V3,V2), car(V3), light(V2).
try(95, 1, V3, V2) :- not use(95, 1), car(V3), light(V2).
try(95, 2, V2) :- use(95, 2), not red(V2), light(V2).
try(95, 2, V2) :- not use(95, 2), light(V2).
try(95, 3, V4, V1) :- use(95, 3), atlight(V4,V1), car(V4), light(V1).
try(95, 3, V4, V1) :- not use(95, 3), car(V4), light(V1).
try(96, 1, V2, V1) :- use(96, 1), atlight(V2,V1), car(V2), light(V1).
try(96, 1, V2, V1) :- not use(96, 1), car(V2), light(V1).
try(96, 2, V1) :- use(96, 2), not red(V1), light(V1).
try(96, 2, V1) :- not use(96, 2), light(V1).
try(96, 3, V3) :- use(96, 3), emergency(V3), car(V3).
try(96, 3, V3) :- not use(96, 3), car(V3).
try(97, 1, V2, V1) :- use(97, 1), atlight(V2,V1), car(V2), light(V1).
try(97, 1, V2, V1) :- not use(97, 1), car(V2), light(V1).
try(97, 2, V1) :- use(97, 2), not red(V1), light(V1).
try(97, 2, V1) :- not use(97, 2), light(V1).
try(97, 3, V3, V1) :- use(97, 3), not atlight(V3,V1), car(V3), light(V1).
try(97, 3, V3, V1) :- not use(97, 3), car(V3), light(V1).
try(98, 1, V3, V2) :- use(98, 1), atlight(V3,V2), car(V3), light(V2).
try(98, 1, V3, V2) :- not use(98, 1), car(V3), light(V2).
try(98, 2, V2) :- use(98, 2), not red(V2), light(V2).
try(98, 2, V2) :- not use(98, 2), light(V2).
try(98, 3, V4, V1) :- use(98, 3), not atlight(V4,V1), car(V4), light(V1).
try(98, 3, V4, V1) :- not use(98, 3), car(V4), light(V1).
try(99, 1, V4, V5) :- use(99, 1), atlight(V4,V5), car(V4), light(V5).
try(99, 1, V4, V5) :- not use(99, 1), car(V4), light(V5).
try(99, 2, V3) :- use(99, 2), not red(V3), light(V3).
try(99, 2, V3) :- not use(99, 2), light(V3).
try(99, 3, V2, V1) :- use(99, 3), atlight(V2,V1), car(V2), light(V1).
try(99, 3, V2, V1) :- not use(99, 3), car(V2), light(V1).
try(100, 1, V3, V2) :- use(100, 1), atlight(V3,V2), car(V3), light(V2).
try(100, 1, V3, V2) :- not use(100, 1), car(V3), light(V2).
try(100, 2, V4) :- use(100, 2), not red(V4), light(V4).
try(100, 2, V4) :- not use(100, 2), light(V4).
try(100, 3, V1) :- use(100, 3), emergency(V1), car(V1).
try(100, 3, V1) :- not use(100, 3), car(V1).
try(101, 1, V3, V2) :- use(101, 1), atlight(V3,V2), car(V3), light(V2).
try(101, 1, V3, V2) :- not use(101, 1), car(V3), light(V2).
try(101, 2, V4) :- use(101, 2), not red(V4), light(V4).
try(101, 2, V4) :- not use(101, 2), light(V4).
try(101, 3, V1, V4) :- use(101, 3), not atlight(V1,V4), car(V1), light(V4).
try(101, 3, V1, V4) :- not use(101, 3), car(V1), light(V4).
try(102, 1, V1) :- use(102, 1), red(V1), light(V1).
try(102, 1, V1) :- not use(102, 1), light(V1).
try(102, 2, V2, V1) :- use(102, 2), atlight(V2,V1), car(V2), light(V1).
try(102, 2, V2, V1) :- not use(102, 2), car(V2), light(V1).
try(102, 3, V1) :- use(102, 3), red(V1), light(V1).
try(102, 3, V1) :- not use(102, 3), light(V1).
try(103, 1, V1) :- use(103, 1), red(V1), light(V1).
try(103, 1, V1) :- not use(103, 1), light(V1).
try(103, 2, V2, V1) :- use(103, 2), atlight(V2,V1), car(V2), light(V1).
try(103, 2, V2, V1) :- not use(103, 2), car(V2), light(V1).
try(103, 3, V2) :- use(103, 3), emergency(V2), car(V2).
try(103, 3, V2) :- not use(103, 3), car(V2).
try(104, 1, V2) :- use(104, 1), red(V2), light(V2).
try(104, 1, V2) :- not use(104, 1), light(V2).
try(104, 2, V3, V2) :- use(104, 2), atlight(V3,V2), car(V3), light(V2).
try(104, 2, V3, V2) :- not use(104, 2), car(V3), light(V2).
try(104, 3, V3, V1) :- use(104, 3), not atlight(V3,V1), car(V3), light(V1).
try(104, 3, V3, V1) :- not use(104, 3), car(V3), light(V1).
try(105, 1, V1) :- use(105, 1), red(V1), light(V1).
try(105, 1, V1) :- not use(105, 1), light(V1).
try(105, 2, V3, V1) :- use(105, 2), atlight(V3,V1), car(V3), light(V1).
try(105, 2, V3, V1) :- not use(105, 2), car(V3), light(V1).
try(105, 3, V3, V2) :- use(105, 3), not atlight(V3,V2), car(V3), light(V2).
try(105, 3, V3, V2) :- not use(105, 3), car(V3), light(V2).
try(106, 1, V2) :- use(106, 1), red(V2), light(V2).
try(106, 1, V2) :- not use(106, 1), light(V2).
try(106, 2, V3, V2) :- use(106, 2), atlight(V3,V2), car(V3), light(V2).
try(106, 2, V3, V2) :- not use(106, 2), car(V3), light(V2).
try(106, 3, V1) :- use(106, 3), not red(V1), light(V1).
try(106, 3, V1) :- not use(106, 3), light(V1).
try(107, 1, V1) :- use(107, 1), red(V1), light(V1).
try(107, 1, V1) :- not use(107, 1), light(V1).
try(107, 2, V3, V1) :- use(107, 2), atlight(V3,V1), car(V3), light(V1).
try(107, 2, V3, V1) :- not use(107, 2), car(V3), light(V1).
try(107, 3, V2) :- use(107, 3), not red(V2), light(V2).
try(107, 3, V2) :- not use(107, 3), light(V2).
drive(V3) :- use(0, 0) , try(0, 1, V3, V2), try(0, 2, V1), try(0, 3, V3, V2), car(V3), light(V2), light(V1).
drive(V3) :- use(1, 0) , try(1, 1, V3, V2), try(1, 2, V1), try(1, 3, V3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(2, 0) , try(2, 1, V3, V2), try(2, 2, V1), try(2, 3, V3, V4), car(V3), light(V2), light(V1), light(V4).
drive(V3) :- use(3, 0) , try(3, 1, V3, V2), try(3, 2, V1), try(3, 3, V2), car(V3), light(V2), light(V1).
drive(V3) :- use(4, 0) , try(4, 1, V3, V2), try(4, 2, V1), try(4, 3, V4), car(V3), light(V2), light(V1), light(V4).
drive(V3) :- use(5, 0) , try(5, 1, V3, V2), try(5, 2, V1), try(5, 3, V3), car(V3), light(V2), light(V1).
drive(V3) :- use(6, 0) , try(6, 1, V3, V2), try(6, 2, V3, V1), try(6, 3, V3, V2), car(V3), light(V2), light(V1).
drive(V3) :- use(7, 0) , try(7, 1, V3, V2), try(7, 2, V3, V1), try(7, 3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(8, 0) , try(8, 1, V3, V2), try(8, 2, V3, V1), try(8, 3, V3, V4), car(V3), light(V2), light(V1), light(V4).
drive(V3) :- use(9, 0) , try(9, 1, V3, V2), try(9, 2, V3, V1), try(9, 3, V2), car(V3), light(V2), light(V1).
drive(V3) :- use(10, 0) , try(10, 1, V3, V2), try(10, 2, V3, V1), try(10, 3, V4), car(V3), light(V2), light(V1), light(V4).
drive(V3) :- use(11, 0) , try(11, 1, V3, V2), try(11, 2, V3, V1), try(11, 3, V3), car(V3), light(V2), light(V1).
drive(V2) :- use(12, 0) , try(12, 1, V2, V1), try(12, 2, V2, V3), try(12, 3, V2, V1), car(V2), light(V1), light(V3).
drive(V3) :- use(13, 0) , try(13, 1, V3, V2), try(13, 2, V3, V4), try(13, 3, V1), car(V3), light(V2), light(V4), light(V1).
drive(V3) :- use(14, 0) , try(14, 1, V3, V2), try(14, 2, V3, V4), try(14, 3, V3, V1), car(V3), light(V2), light(V4), light(V1).
drive(V2) :- use(15, 0) , try(15, 1, V2, V1), try(15, 2, V2, V3), try(15, 3, V1), car(V2), light(V1), light(V3).
drive(V2) :- use(16, 0) , try(16, 1, V2, V1), try(16, 2, V2, V3), try(16, 3, V3), car(V2), light(V1), light(V3).
drive(V2) :- use(17, 0) , try(17, 1, V2, V1), try(17, 2, V2, V3), try(17, 3, V2), car(V2), light(V1), light(V3).
drive(V2) :- use(18, 0) , try(18, 1, V2, V1), try(18, 2, V1), try(18, 3, V2, V1), car(V2), light(V1).
drive(V3) :- use(19, 0) , try(19, 1, V3, V2), try(19, 2, V2), try(19, 3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(20, 0) , try(20, 1, V3, V2), try(20, 2, V2), try(20, 3, V3, V1), car(V3), light(V2), light(V1).
drive(V2) :- use(21, 0) , try(21, 1, V2, V1), try(21, 2, V1), try(21, 3, V2, V3), car(V2), light(V1), light(V3).
drive(V2) :- use(22, 0) , try(22, 1, V2, V1), try(22, 2, V1), try(22, 3, V3), car(V2), light(V1), light(V3).
drive(V2) :- use(23, 0) , try(23, 1, V2, V1), try(23, 2, V1), try(23, 3, V2), car(V2), light(V1).
drive(V2) :- use(24, 0) , try(24, 1, V2, V1), try(24, 2, V3), try(24, 3, V2, V1), car(V2), light(V1), light(V3).
drive(V3) :- use(25, 0) , try(25, 1, V3, V2), try(25, 2, V4), try(25, 3, V1), car(V3), light(V2), light(V4), light(V1).
drive(V3) :- use(26, 0) , try(26, 1, V3, V2), try(26, 2, V4), try(26, 3, V3, V1), car(V3), light(V2), light(V4), light(V1).
drive(V2) :- use(27, 0) , try(27, 1, V2, V1), try(27, 2, V3), try(27, 3, V2, V3), car(V2), light(V1), light(V3).
drive(V2) :- use(28, 0) , try(28, 1, V2, V1), try(28, 2, V3), try(28, 3, V1), car(V2), light(V1), light(V3).
drive(V2) :- use(29, 0) , try(29, 1, V2, V1), try(29, 2, V3), try(29, 3, V2), car(V2), light(V1), light(V3).
drive(V2) :- use(30, 0) , try(30, 1, V2, V1), try(30, 2, V2), try(30, 3, V2, V1), car(V2), light(V1).
drive(V3) :- use(31, 0) , try(31, 1, V3, V2), try(31, 2, V3), try(31, 3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(32, 0) , try(32, 1, V3, V2), try(32, 2, V3), try(32, 3, V3, V1), car(V3), light(V2), light(V1).
drive(V2) :- use(33, 0) , try(33, 1, V2, V1), try(33, 2, V2), try(33, 3, V2, V3), car(V2), light(V1), light(V3).
drive(V2) :- use(34, 0) , try(34, 1, V2, V1), try(34, 2, V2), try(34, 3, V1), car(V2), light(V1).
drive(V2) :- use(35, 0) , try(35, 1, V2, V1), try(35, 2, V2), try(35, 3, V3), car(V2), light(V1), light(V3).
drive(V2) :- use(36, 0) , try(36, 1, V2, V1), try(36, 2, V2, V3), try(36, 3, V1), car(V2), light(V1), light(V3).
drive(V2) :- use(37, 0) , try(37, 1, V2, V1), try(37, 2, V2, V3), try(37, 3, V2, V1), car(V2), light(V1), light(V3).
drive(V3) :- use(38, 0) , try(38, 1, V3, V2), try(38, 2, V3, V4), try(38, 3, V3, V1), car(V3), light(V2), light(V4), light(V1).
drive(V2) :- use(39, 0) , try(39, 1, V2, V1), try(39, 2, V2, V3), try(39, 3, V3), car(V2), light(V1), light(V3).
drive(V3) :- use(40, 0) , try(40, 1, V3, V2), try(40, 2, V3, V4), try(40, 3, V1), car(V3), light(V2), light(V4), light(V1).
drive(V2) :- use(41, 0) , try(41, 1, V2, V1), try(41, 2, V2, V3), try(41, 3, V2), car(V2), light(V1), light(V3).
drive(V4) :- use(42, 0) , try(42, 1, V4, V5), try(42, 2, V1), try(42, 3, V3, V2), car(V4), light(V5), light(V1), car(V3), light(V2).
drive(V4) :- use(43, 0) , try(43, 1, V4, V3), try(43, 2, V1), try(43, 3, V2, V1), car(V4), light(V3), light(V1), car(V2).
drive(V4) :- use(44, 0) , try(44, 1, V4, V3), try(44, 2, V1), try(44, 3, V2, V3), car(V4), light(V3), light(V1), car(V2).
drive(V4) :- use(45, 0) , try(45, 1, V4, V3), try(45, 2, V1), try(45, 3, V2), car(V4), light(V3), light(V1), car(V2).
drive(V1) :- use(46, 0) , try(46, 1, V1, V3), try(46, 2, V1, V2), try(46, 3, V1, V3), car(V1), light(V3), light(V2).
drive(V1) :- use(47, 0) , try(47, 1, V1, V3), try(47, 2, V1, V2), try(47, 3, V2), car(V1), light(V3), light(V2).
drive(V1) :- use(48, 0) , try(48, 1, V1, V3), try(48, 2, V1, V2), try(48, 3, V1, V4), car(V1), light(V3), light(V2), light(V4).
drive(V1) :- use(49, 0) , try(49, 1, V1, V3), try(49, 2, V1, V2), try(49, 3, V4), car(V1), light(V3), light(V2), light(V4).
drive(V1) :- use(50, 0) , try(50, 1, V1, V3), try(50, 2, V1, V2), try(50, 3, V3), car(V1), light(V3), light(V2).
drive(V1) :- use(51, 0) , try(51, 1, V1, V3), try(51, 2, V1, V2), try(51, 3, V1), car(V1), light(V3), light(V2).
drive(V1) :- use(52, 0) , try(52, 1, V1, V4), try(52, 2, V1, V3), try(52, 3, V2), car(V1), light(V4), light(V3), light(V2).
drive(V1) :- use(53, 0) , try(53, 1, V1, V4), try(53, 2, V1, V3), try(53, 3, V1, V2), car(V1), light(V4), light(V3), light(V2).
drive(V1) :- use(54, 0) , try(54, 1, V1, V3), try(54, 2, V1, V2), try(54, 3, V2), car(V1), light(V3), light(V2).
drive(V3) :- use(55, 0) , try(55, 1, V3, V2), try(55, 2, V2), try(55, 3, V1, V4), car(V3), light(V2), car(V1), light(V4).
drive(V4) :- use(56, 0) , try(56, 1, V4, V3), try(56, 2, V3), try(56, 3, V1, V2), car(V4), light(V3), car(V1), light(V2).
drive(V3) :- use(57, 0) , try(57, 1, V3, V2), try(57, 2, V2), try(57, 3, V1, V2), car(V3), light(V2), car(V1).
drive(V3) :- use(58, 0) , try(58, 1, V3, V2), try(58, 2, V2), try(58, 3, V1), car(V3), light(V2), car(V1).
drive(V3) :- use(59, 0) , try(59, 1, V3, V2), try(59, 2, V4), try(59, 3, V1, V4), car(V3), light(V2), light(V4), car(V1).
drive(V4) :- use(60, 0) , try(60, 1, V4, V5), try(60, 2, V2), try(60, 3, V3, V1), car(V4), light(V5), light(V2), car(V3), light(V1).
drive(V3) :- use(61, 0) , try(61, 1, V3, V2), try(61, 2, V4), try(61, 3, V1, V2), car(V3), light(V2), light(V4), car(V1).
drive(V3) :- use(62, 0) , try(62, 1, V3, V2), try(62, 2, V4), try(62, 3, V1), car(V3), light(V2), light(V4), car(V1).
drive(V1) :- use(63, 0) , try(63, 1, V1, V2), try(63, 2, V1), try(63, 3, V1, V2), car(V1), light(V2).
drive(V1) :- use(64, 0) , try(64, 1, V1, V3), try(64, 2, V1), try(64, 3, V2), car(V1), light(V3), light(V2).
drive(V1) :- use(65, 0) , try(65, 1, V1, V3), try(65, 2, V1), try(65, 3, V1, V2), car(V1), light(V3), light(V2).
drive(V1) :- use(66, 0) , try(66, 1, V1, V3), try(66, 2, V1), try(66, 3, V2), car(V1), light(V3), light(V2).
drive(V1) :- use(67, 0) , try(67, 1, V1, V2), try(67, 2, V1), try(67, 3, V2), car(V1), light(V2).
drive(V1) :- use(68, 0) , try(68, 1, V1, V2), try(68, 2, V1, V3), try(68, 3, V2), car(V1), light(V2), light(V3).
drive(V1) :- use(69, 0) , try(69, 1, V1, V2), try(69, 2, V1, V3), try(69, 3, V1, V2), car(V1), light(V2), light(V3).
drive(V1) :- use(70, 0) , try(70, 1, V1, V2), try(70, 2, V1, V3), try(70, 3, V1, V4), car(V1), light(V2), light(V3), light(V4).
drive(V1) :- use(71, 0) , try(71, 1, V1, V2), try(71, 2, V1, V3), try(71, 3, V4), car(V1), light(V2), light(V3), light(V4).
drive(V1) :- use(72, 0) , try(72, 1, V1, V2), try(72, 2, V1, V3), try(72, 3, V3), car(V1), light(V2), light(V3).
drive(V1) :- use(73, 0) , try(73, 1, V1, V2), try(73, 2, V1, V3), try(73, 3, V1), car(V1), light(V2), light(V3).
drive(V3) :- use(74, 0) , try(74, 1, V3, V2), try(74, 2, V1), try(74, 3, V4, V1), car(V3), light(V2), light(V1), car(V4).
drive(V3) :- use(75, 0) , try(75, 1, V3, V2), try(75, 2, V1), try(75, 3, V4), car(V3), light(V2), light(V1), car(V4).
drive(V3) :- use(76, 0) , try(76, 1, V3, V2), try(76, 2, V1), try(76, 3, V4, V2), car(V3), light(V2), light(V1), car(V4).
drive(V4) :- use(77, 0) , try(77, 1, V4, V5), try(77, 2, V1), try(77, 3, V2, V3), car(V4), light(V5), light(V1), car(V2), light(V3).
drive(V2) :- use(78, 0) , try(78, 1, V2, V1), try(78, 2, V2), try(78, 3, V2, V1), car(V2), light(V1).
drive(V2) :- use(79, 0) , try(79, 1, V2, V1), try(79, 2, V2), try(79, 3, V1), car(V2), light(V1).
drive(V3) :- use(80, 0) , try(80, 1, V3, V2), try(80, 2, V3), try(80, 3, V3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(81, 0) , try(81, 1, V3, V1), try(81, 2, V3), try(81, 3, V3, V2), car(V3), light(V1), light(V2).
drive(V3) :- use(82, 0) , try(82, 1, V3, V2), try(82, 2, V3), try(82, 3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(83, 0) , try(83, 1, V3, V1), try(83, 2, V3), try(83, 3, V2), car(V3), light(V1), light(V2).
drive(V3) :- use(84, 0) , try(84, 1, V3, V2), try(84, 2, V3, V1), try(84, 3, V2), car(V3), light(V2), light(V1).
drive(V3) :- use(85, 0) , try(85, 1, V3, V2), try(85, 2, V3, V1), try(85, 3, V3), car(V3), light(V2), light(V1).
drive(V4) :- use(86, 0) , try(86, 1, V4, V2), try(86, 2, V4, V1), try(86, 3, V4, V3), car(V4), light(V2), light(V1), light(V3).
drive(V3) :- use(87, 0) , try(87, 1, V3, V2), try(87, 2, V3, V1), try(87, 3, V1), car(V3), light(V2), light(V1).
drive(V4) :- use(88, 0) , try(88, 1, V4, V2), try(88, 2, V4, V1), try(88, 3, V3), car(V4), light(V2), light(V1), light(V3).
drive(V3) :- use(89, 0) , try(89, 1, V3, V1), try(89, 2, V3, V2), try(89, 3, V3, V1), car(V3), light(V1), light(V2).
drive(V3) :- use(90, 0) , try(90, 1, V3, V1), try(90, 2, V3, V2), try(90, 3, V1), car(V3), light(V1), light(V2).
drive(V3) :- use(91, 0) , try(91, 1, V3, V1), try(91, 2, V3, V2), try(91, 3, V3), car(V3), light(V1), light(V2).
drive(V4) :- use(92, 0) , try(92, 1, V4, V2), try(92, 2, V4, V3), try(92, 3, V4, V1), car(V4), light(V2), light(V3), light(V1).
drive(V4) :- use(93, 0) , try(93, 1, V4, V2), try(93, 2, V4, V3), try(93, 3, V1), car(V4), light(V2), light(V3), light(V1).
drive(V3) :- use(94, 0) , try(94, 1, V3, V1), try(94, 2, V3, V2), try(94, 3, V2), car(V3), light(V1), light(V2).
drive(V3) :- use(95, 0) , try(95, 1, V3, V2), try(95, 2, V2), try(95, 3, V4, V1), car(V3), light(V2), car(V4), light(V1).
drive(V2) :- use(96, 0) , try(96, 1, V2, V1), try(96, 2, V1), try(96, 3, V3), car(V2), light(V1), car(V3).
drive(V2) :- use(97, 0) , try(97, 1, V2, V1), try(97, 2, V1), try(97, 3, V3, V1), car(V2), light(V1), car(V3).
drive(V3) :- use(98, 0) , try(98, 1, V3, V2), try(98, 2, V2), try(98, 3, V4, V1), car(V3), light(V2), car(V4), light(V1).
drive(V4) :- use(99, 0) , try(99, 1, V4, V5), try(99, 2, V3), try(99, 3, V2, V1), car(V4), light(V5), light(V3), car(V2), light(V1).
drive(V3) :- use(100, 0) , try(100, 1, V3, V2), try(100, 2, V4), try(100, 3, V1), car(V3), light(V2), light(V4), car(V1).
drive(V3) :- use(101, 0) , try(101, 1, V3, V2), try(101, 2, V4), try(101, 3, V1, V4), car(V3), light(V2), light(V4), car(V1).
drive(V2) :- use(102, 0) , try(102, 1, V1), try(102, 2, V2, V1), try(102, 3, V1), car(V2), light(V1).
drive(V2) :- use(103, 0) , try(103, 1, V1), try(103, 2, V2, V1), try(103, 3, V2), car(V2), light(V1).
drive(V3) :- use(104, 0) , try(104, 1, V2), try(104, 2, V3, V2), try(104, 3, V3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(105, 0) , try(105, 1, V1), try(105, 2, V3, V1), try(105, 3, V3, V2), car(V3), light(V1), light(V2).
drive(V3) :- use(106, 0) , try(106, 1, V2), try(106, 2, V3, V2), try(106, 3, V1), car(V3), light(V2), light(V1).
drive(V3) :- use(107, 0) , try(107, 1, V1), try(107, 2, V3, V1), try(107, 3, V2), car(V3), light(V1), light(V2).
