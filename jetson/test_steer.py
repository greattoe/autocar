from getchar import Getchar
from pop import Pilot
Car = Pilot.AutoCar()
kb = Getchar()

LEFT = -1
RIGHT = 1
CENTER = 0

key = ''

while True:
    key = kb.getch()
    if key == 'a':
        Car.steering = LEFT
    elif key == 'd':
        Car.steering = RIGHT
    elif key == 's':
        Car.steering = CENTER
    if key == 'w':
        Car.steering = -2
    elif key == 'e':
        Car.steering = 2
    else:
        pass


