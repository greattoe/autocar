import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code %d" % rc)
    client.subscribe("car/control")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip()
    print("Received message: %s" % payload)

    if payload == "led_on":
        print("LED ON command received")
    elif payload == "led_off":
        print("LED OFF command received")
    else:
        print("Unknown command: %s" % payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.42.0.1", 1883, 60)  # PC의 IP 주소로 연결
client.loop_forever()

