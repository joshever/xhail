% BACKGROUND
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

atlight(car1, a).
atlight(car2, b).
atlight(car3, c).
atlight(car4, a).
emergency(car4).

#example drive(car3).
#example drive(car2).
#example drive(car4).
#example not drive(car1).

#modeh drive(+car).
#modeb atlight(+car, -light).
#modeb not atlight(+car, -light).
#modeb red(+light).
#modeb not red(+light).
#modeb emergency(+car).
#modeb not emergency(+car).