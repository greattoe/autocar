from getchar import Getchar
from pop import Pilot

Car = Pilot.AutoCar()
kb = Getchar()

pan  = 90
tilt =  0
pan_prv  = 90
tilt_prv =  0
key = ''

def set_pt(p_val, t_val):
    global pan, tilt, pan_prv, tilt_prv
    if pan != pan_prv or tilt != tilt_prv:
        print("pan = %s, tilt = %s" % (pan, tilt))
        Car.camPan(p_val)
        Car.camTilt(t_val)
        pan_prv = pan
        tilt_prv = tilt

def main():
    global pan, tilt
    print("### P/T Control Test!")
    try:
        while True:
            key = kb.getch()
            if key == 'w':
                if tilt + 5 <= 90:
                    tilt += 5
                else:
                    tilt = 200
            elif key == 's':
                if tilt - 5 >= -15:
                    tilt -= 5
                else:
                    tilt = -15
            elif key == 'a':
                if pan - 5 >= 0:
                    pan -= 5
                else:
                    pan = 0
            elif key == 'd':
                if pan + 5 <= 180:
                    pan += 5
                else:
                    pan = 180

            set_pt(pan, tilt)

    except KeyboardInterrupt:
        print("\nProgram Terminated!")

if __name__ == "__main__":
    main()

