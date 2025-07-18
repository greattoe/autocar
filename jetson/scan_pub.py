'''
if degree <= 60 or degree >= 300:
            +-------------+
            |     0°      |
<-----------+------+------+----------->
          270°    0°     90°
'''
import sys
import time
from pop import LiDAR, Pilot
import paho.mqtt.client as mqtt

# 전역 변수
front = 0
left = 0
back = 0
right = 0

# MQTT 설정
broker_ip = "10.42.0.1"  # 올바른 IP인지 확인
client = mqtt.Client(protocol=mqtt.MQTTv311)  #MQTT 클라이언트 생성

def pub_lidar():
    client.publish("lidar/front", str(front))
    client.publish("lidar/right", str(right))
    client.publish("lidar/back",  str(back))
    client.publish("lidar/left",  str(left))

def main():
    global front, left, back, right

    lidar = LiDAR.Rplidar()
    lidar.connect()
    lidar.startMotor()

    # MQTT 브로커에 연결 (1번만)
    client.connect(broker_ip)

    try:
        print("start piblish lidar topic!")
        while True:
            vectors = lidar.getVectors()
            front = left = back = right = 0

            for v in vectors:
                degree = v[0]
                distance = v[1]

                if (degree <= 10 or degree >= 350):
                    front = distance
                elif 85 <= degree <= 95:
                    right = distance
                elif 175 <= degree <= 185:
                    back = distance
                elif 265 <= degree <= 275:
                    left = distance

            pub_lidar()
            time.sleep(0.1)  # 너무 자주 발행 방지

    except KeyboardInterrupt:
        print("\nProgram Terminated!")
    finally:
        client.disconnect()
        lidar.stopMotor()
        lidar.disconnect()
        sys.exit()

if __name__ == "__main__":
    main()

