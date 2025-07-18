import sys, time
from pop import Pilot
Car = Pilot.AutoCar()

def main():
    #global front, left, back, right  # for use global variable

    try:
        while True:
            acc_z = Car.getAccel('z')
            gyr_z = Car.getGyro('z')
            print("gyro_z = %s" %gyr_z)
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nProgram Terminated!")
    finally:
        sys.exit()

if __name__ == "__main__":
    main()
