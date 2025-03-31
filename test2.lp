player(a).
player(b).
player(c).
player(d).
location(l00).
location(l01).
location(l10).
location(l11).

nextTo(l00, l01).
nextTo(l00, l10).
nextTo(l01, l11).
nextTo(l10, l11).

playerAt(a, l00).
playerAt(b, l01).
playerAt(c, l10).
playerAt(d, l11).

#example not wins(a, b).
#example not wins(c, d).
#example not wins(a, c).
#example not wins(b, d).
#example wins(a, d).
#example wins(b, c).

#modeh wins(+player, +player).
#modeb nextTo(+location, +location).
#modeb not nextTo(+location, +location).
#modeb playerAt(+player, -location).