import sys, time
from getchar import Getchar
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

dist = 0.0
DIST2KEEP = 500.0
DIST_TOL  = 100.0

broker_ip = "10.42.0.1"
topic = "car/control"
message =''
def pub_msg(msg):
    publish.single(topic, msg, hostname=broker_ip)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code %d" % rc)
    client.subscribe("lidar/front")

def on_message(client, userdata, msg):
    global dist
    tmp = msg.payload.decode().strip()
    dist = float(tmp)
    print("Received message: %s" % dist)

def main():
    global message
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker_ip, 1883, 60)
        client.loop_start()  # 백그라운드 수신 루프

        while True:
            if dist > DIST2KEEP + DIST_TOL:
                message = "forward"
            elif dist < DIST2KEEP - DIST_TOL:
                message = "backward"
            else:
                message = "stop"
            pub_msg(message)
            time.sleep(0.5)
        client.loop_stop()
    except KeyboardInterrupt:
        print("\nProgram terminated!")
        client.loop_stop()

if __name__ == "__main__":
    main()
