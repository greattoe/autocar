PC에서 Jetson Nano를 MQTT(Mosquitto 브로커 활용)로 제어하려면, 다음과 같은 구조로 시스템을 구성하면 됩니다:

------

### ✅ 기본 구성

```
css


CopyEdit
[PC(Client/Publisher)] ←→ [Mosquitto Broker] ←→ [Jetson Nano(Client/Subscriber)]
```

- **PC**: 제어 명령을 보내는 Publisher 역할
- **Jetson Nano**: 명령을 받아서 동작하는 Subscriber 역할
- **Mosquitto Broker**: MQTT 메시지를 중계

------

## 1️⃣ Mosquitto 브로커 설치 (PC 또는 Jetson 중 한 곳 또는 제3의 서버)

### 예: PC(Ubuntu)에 Mosquitto 설치

```
bashCopyEditsudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
```

------

## 2️⃣ Jetson Nano에 MQTT 클라이언트 설치

```
bashCopyEditsudo apt update
pip3 install paho-mqtt
```

------

## 3️⃣ Jetson Nano: Subscriber 코드 예시

```
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code %d" % rc)
    client.subscribe("jetson/control")

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

```

------

## 4️⃣ PC에서 명령 전송 (Publisher 역할)

```
bashCopyEditmosquitto_pub -h 192.168.0.100 -t jetson/control -m "led_on"
mosquitto_pub -h 192.168.0.100 -t jetson/control -m "led_off"
```

또는 Python 코드로:

```
pythonCopyEdit# pc_publisher.py
import paho.mqtt.publish as publish

publish.single("jetson/control", "led_on", hostname="192.168.0.100")
```

------

## 5️⃣ 참고 사항

- 브로커를 Jetson Nano에 설치해도 무방함 (`sudo apt install mosquitto`)
- Jetson이나 PC가 동일 네트워크에 있어야 함
- 포트 `1883`은 MQTT 기본 포트이므로 방화벽 확인 필요
- 필요하면 보안(TLS/인증)도 구성 가능

------

## ✅ 요약

| 역할             | 장비           | 설명                                |
| ---------------- | -------------- | ----------------------------------- |
| Mosquitto 브로커 | PC 또는 Jetson | MQTT 메시지 중계                    |
| Publisher        | PC             | 명령을 전송 (`led_on`, `move`, 등)  |
| Subscriber       | Jetson Nano    | 명령 수신 후 GPIO 제어 등 동작 수행 |



------





### ✅ 네트워크 구성 확인

| 장치            | 역할               | IP 주소       |
| --------------- | ------------------ | ------------- |
| **PC**          | Mosquitto 브로커 🟢 | `10.42.0.1`   |
| **Jetson Nano** | MQTT Subscriber 🔵  | `10.42.0.198` |



------

### ✅ 올바른 설정 요약

#### 🟢 PC (Publisher 또는 브로커 실행)

**Mosquitto 브로커 실행 확인:**

```
bash


CopyEdit
sudo systemctl status mosquitto
```

**브로커 테스트용 메시지 전송 (Publisher):**

```
bash


CopyEdit
mosquitto_pub -h 10.42.0.1 -t jetson/control -m "led_off"
```

------

#### 🔵 Jetson Nano (Subscriber 코드)

**Python 코드 예시:**

```
pythonCopyEditimport paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code %d" % rc)
    client.subscribe("jetson/control")

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
```

> 꼭 `strip()`을 사용하여 개행 문자 등으로 인한 비교 실패를 방지하세요.

------

### ✅ Jetson Nano 수동 수신 테스트

```
bash


CopyEdit
mosquitto_sub -h 10.42.0.1 -t jetson/control
```

→ 이 명령어로 `led_off` 메시지가 보이면, Python 코드 문제이고,
 → 메시지가 보이지 않으면 네트워크나 브로커 연결 문제입니다.

------

### 🔒 방화벽(UFW) 설정 확인 (PC 측에서만 필요)

```
bash


CopyEdit
sudo ufw allow 1883
```
