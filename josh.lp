% BACKGROUND
car(car1).
car(car2).
car(car3).

light(a).
light(b).
light(c).

red(a).
amber(b).
green(c).

atlight(car1, a).
atlight(car2, b).
atlight(car3, c).

#example drive(car1, a).
#example drive(car2, b).
#example not drive(car3, c).

#modeh drive(+car, +light).
#modeb atlight(+car, +light).
#modeb not atlight(+car, +light).
#modeb red(+light).
#modeb not red(+light).