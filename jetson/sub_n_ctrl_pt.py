import time, sys
import paho.mqtt.client as mqtt

from pop import Pilot
Car = Pilot.AutoCar()

LEFT     = -1
RIGHT    = 1
CENTER   = 0
SPD_VAL  = 70
SPD_STP  = 5
MAX_SPD  = 99
MIN_SPD  = 0
MESSAGE = ""

pan = pan_prv = 90;   tilt = tilt_prv = 0

Car.setSpeed(SPD_VAL)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code %d" % rc)
    client.subscribe("pt/control")

def on_message(client, userdata, msg):
    global MESSAGE
    MESSAGE = msg.payload.decode().strip()
    print("Received message: %s" % MESSAGE)

def set_pt(p_val, t_val):
    Car.camPan(p_val)
    Car.camTilt(t_val)
    if pan != pan_prv or tilt != tilt_prv:
        print("pan = %s, tilt = %s" %(pan, tilt))
    else:   pass

def main():
    global MESSAGE, pan, tilt, pan_prv, tilt_prv
    try:
        set_pt(pan, tilt)
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("192.168.55.100", 1883, 60)
        client.loop_start()  # 백그라운드 수신 루프

        while True:
            if MESSAGE == "up":
                print("up"); MESSAGE = ""
                if tilt + 5 <= 200:
                    tilt = tilt + 5
                else:
                    tilt = 200
            elif MESSAGE == "down":
                print("down"); MESSAGE = ""
                if tilt - 5 >= -30:
                    tilt = tilt - 5
                else:
                    tilt = -30
            if MESSAGE == "left":
                print("left"); MESSAGE = ""
                if pan - 5 >= 0:
                    pan = pan - 5
                else:
                    pan = 0
            elif MESSAGE == "right":
                print("right"); MESSAGE = ""
                if pan + 5 <= 180:
                    pan = pan + 5
                else:
                    pan = 180
            elif MESSAGE == "preset1":
                print("preset1"); MESSAGE = ""
                pan = 90; tilt = 0
            elif MESSAGE == "preset2":
                print("preset2"); MESSAGE = ""
                pan = 90; tilt = -30
            else:
                pass
            set_pt(pan, tilt)
            pan_prv = pan; tilt_prv = tilt
            time.sleep(0.1)

    except KeyboardInterrupt:
        Car.stop()
        sys.exit()

if __name__ == "__main__":
    main()

