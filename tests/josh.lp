% BACKGROUND
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

atlight(car1, a).
atlight(car2, b).
atlight(car3, c).
atlight(car4, a).

#example drive(car2).
#example drive(car3).
#example not drive(car1).
#example drive(car4).
#example drive(car5).

#modeh drive(+car).
#modeb atlight(+car, -light).
#modeb not red(+light).
#modeb emergency(+car).