import sys
from getchar import Getchar
import paho.mqtt.publish as publish
broker_ip = "10.42.0.1"
topic = "car/control"
msg =''
def pub_msg(msg):
    publish.single(topic, msg, hostname=broker_ip)
kb = Getchar()

key = ''

try:
    while True:
        key = kb.getch()
        if key == 'a':
            msg = "left"
        elif key == 's':
            msg = "center"
        elif key == 'd':
            msg = "right"
        elif key == 'w':
            msg = "forward"
        elif key == 'x':
            msg = "backward"
        elif key == ' ':
            msg = "stop"
        elif key == '.':
            msg = "speed_up"
        elif key == ',':
            msg = "speed_down"
        else:
            pass
        pub_msg(msg)
except KeyboardInterrupt:

    sys.exit()
