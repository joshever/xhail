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

%NEGATIONS%
not_nextTo(V1,V2) :- not nextTo(V1,V2), location(V1), location(V2).

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

%ABDUCIBLES%
0 { abduced_wins(V1,V2) : player(V1), player(V2) } 1000000.
#minimize{1@2, V1, V2: abduced_wins(V1,V2), player(V1), player(V2)}.
wins(V1,V2) :- abduced_wins(V1,V2), player(V1), player(V2).

