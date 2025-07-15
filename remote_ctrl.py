from getchar import Getchar
from pop import Pilot
Car = Pilot.AutoCar()
kb = Getchar()

LEFT = -1
CENTER = 0
RIGHT = 1

spd_val = 70

max_spd = 99
min_spd = 0
spd_stp = 5

key = ''

while True:
    key = kb.getch()
    if key == 'a':
        Car.steering = LEFT
    elif key == 'd':
        Car.steering = RIGHT
    elif key == 's':
        Car.steering = CENTER
    elif key == 'w':
        Car.backward()
    elif key == 'x':
        Car.forward()
    elif key == ' ':
        Car.stop()
    elif key == '.': #'>'
        if spd_val + spd_stp <= max_spd:
            spd_val = spd_val + spd_stp
        else:
             spd_val = max_spd
    elif key == ',': #'<'
        if spd_val - spd_stp >= min_spd:
            spd_val = spd_val - spd_stp
        else:
             spd_val = min_spd
             
    Car.setSpeed(spd_val)    
    
