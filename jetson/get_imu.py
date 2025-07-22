import time, sys
from pop import Pilot

def main():
    Car = Pilot.AutoCar()

    try:
        while True:
            gyro_x = Car.getGyro('x')
            gyro_y = Car.getGyro('y')
            gyro_z = Car.getGyro('z')
            print("gyro_x = %s, gyro_y = %s, gyro_z = %s." % (gyro_x, gyro_y, gyro_z))

            accelo_x = Car.getAccel('x')
            accelo_y = Car.getAccel('y')
            accelo_z = Car.getAccel('z')
            print("accelo_x = %s, accelo_y = %s, accelo_z = %s." % (accelo_x, accelo_y, accelo_z))

            time.sleep(0.1)  # 100ms 주기

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        print("Cleaning up pins")

if __name__ == '__main__':
    main()

