import time, sys
from pop import Pilot
import paho.mqtt.client as mqtt

Car = Pilot.AutoCar()
SPD_VAL  = 70
SPD_STP  = 5
MAX_SPD  = 99
MIN_SPD  = 0
MESSAGE = ""

Car.setSpeed(SPD_VAL)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code %d" % rc)
    client.subscribe("car/control")

def on_message(client, userdata, msg):
    global MESSAGE
    MESSAGE = msg.payload.decode().strip()
    print("Received message: %s" % MESSAGE)

def main():
    global MESSAGE
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("10.42.0.1", 1883, 60)
        client.loop_start()  # 백그라운드 수신 루프
        print("subscribe  topic & control Autocar Prime!")
        while True:
            if MESSAGE == "forward":
                print("go")
                Car.forward();  MESSAGE = ""
            elif MESSAGE == "backward":
                print("back")
                Car.backward(); MESSAGE = ""
            elif MESSAGE == "stop":
                print("stop")
                Car.stop(); MESSAGE = ""
            elif MESSAGE == "straight":
                print("straight")
                Car.steering = 0; MESSAGE = ""
            elif MESSAGE == "left1":
                print("left1")
                Car.steering = -0.5; MESSAGE = ""
            elif MESSAGE == "left2":
                print("left2")
                Car.steering = -1.0; MESSAGE = ""
            elif MESSAGE == "right1":
                print("right1")
                Car.steering = 0.5; MESSAGE = ""
            elif MESSAGE == "right2":
                print("right2")
                Car.steering = 1.0; MESSAGE = ""
            else:
                pass

            Car.setSpeed(SPD_VAL)
            time.sleep(0.1)

    except KeyboardInterrupt:
        Car.stop()
        sys.exit()

if __name__ == "__main__":
    main()

