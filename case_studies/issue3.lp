#example p(1).
q(1,a).
q(2,b).
q(3,c).

number(1).
number(2).
number(3).

letter(a).
letter(b).
letter(c).

#modeh p(+number).

#modeb q(+number,-letter).

#modeb not q(+number,-letter).