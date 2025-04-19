email(a).
email(b).
email(c).

word(urgent).
word(tax).
word(josh).

contains(a, urgent).
contains(b, tax).
contains(c, urgent).
contains(c, josh).
angry(urgent).
family(josh).

#example spam(a).
#example not spam(b).
#example urgent(c).
#example not spam(c).

#modeh spam(+email).
#modeh urgent(+email).
#modeb contains(+email, -word).
#modeb not contains(+email, -word).
#modeb angry(+word).
#modeb not angry(+word).
#modeb family(+word).
#modeb not family(+word).