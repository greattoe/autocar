'''
if degree <= 60 or degree >= 300:
            +-------------+
            |     0°      |
<-----------+------+------+----------->
          270°    0°     90°
'''

import sys
from pop import LiDAR, Pilot

import paho.mqtt.client as mqtt
client = mqtt.Client()

broker_ip = "192.168.55.100" #for usb rndis
# broker_ip = "110.42.0.198" #for usb rndis

def pub_lidar():
    client.connect(broker_ip)

    client.publish("lidar/front", front)
    client.publish("lidar/right", right)
    client.publish("lidar/back",  back)
    client.publish("lidar/left",  left)

    client.disconnect()


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
            vectors = lidar.getVectors()
            # print(len(vectors))
            # initialize dist vars
            front = left = back = right = 0

            for v in vectors:
                degree = v[0]
                distance = v[1]

                # 각 방향별 조건에 따라 가장 가까운 거리 기록
                if (degree <= 10 or degree >= 350):  # Front
                    front = distance #print("distance front = %s" %distance)
                if (degree >= 265 and degree <= 275):  # left
                    left = distance #print("distance left = %s" %distance)
                if (degree >= 175 and degree <= 185):  # back
                    back = distance #print("distance back = %s" %distance)
                if (degree >= 85 and degree <= 95):  # right
                    right = distance #print("distance right = %s" %distance)
                pub_lidar()

    except KeyboardInterrupt:
        print("\nProgram Terminated!")
        sys.exit()
    finally:
        lidar.stopMotor()
        lidar.disconnect()

if __name__ == "__main__":
    main()

