#example p(1).

q(1,a ;; 2,b ;; 3,c).

number(1..3).

letter(a;b;c).

#modeh p(+number).

#modeb q(+number,-letter).

#modeb not q(+number,-letter).