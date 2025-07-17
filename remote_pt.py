import sys
from getchar import Getchar
import paho.mqtt.publish as publish
#broker_ip = "10.42.0.1" # hotspot connection
broker_ip = "192.168.55.100" # usb connection
topic = "pt/control"
msg =''
def pub_msg(msg):
    publish.single(topic, msg, hostname=broker_ip)
kb = Getchar()

key = ''

try:
    while True:
        key = kb.getch()
        if key == 'w':
            msg = "up"
        elif key == 's':
            msg = "down"
        elif key == 'a':
            msg = "left"
        elif key == 'd':
            msg = "right"
        elif key == 'q':
            msg = "preset1"
        elif key == 'e':
            msg = "preset2"
        else:
            pass
        pub_msg(msg)
except KeyboardInterrupt:

    sys.exit()
