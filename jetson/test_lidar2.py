'''
if degree <= 60 or degree >= 300:
            +-------------+
            |     0°      |
<-----------+------+------+----------->
          270°    0°     90°
'''

import sys, time
from pop import LiDAR, Pilot

# declare global varable
front = 0
left = 0
back = 0
right = 0

def main():
    global front, left, back, right  # for use global variable

    lidar = LiDAR.Rplidar()
    lidar.connect()
    lidar.startMotor()

    try:
        while True:
            coords = lidar.getXY()

            for c in coords:
                print(c)
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nProgram Terminated!")
        sys.exit()
    finally:
        lidar.stopMotor()
        lidar.disconnect()

if __name__ == "__main__":
    main()

