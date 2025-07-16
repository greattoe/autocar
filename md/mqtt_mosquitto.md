**MQTT**(**M**essage **Q**ueuing **T**elemetry **T**ransport)

**IoT 장치 간 통신을 위한 경량 메시지 프로토콜**입니다.

##### 특징:

- **Publish / Subscribe** 구조
- **경량**(Lightweight): 저전력, 저대역폭 환경에 적합
- **QoS**(전송 신뢰도) 지원: 0, 1, 2 단계
- **TCP 기반**, 포트: `1883` (일반), `8883` (TLS)

**Mosquitto는 MQTT 브로커**입니다.
 즉, **MQTT 메시지를 중계하는 서버 프로그램**입니다.

##### ✅ 역할:

- **Publisher**가 보내는 메시지를 받아
- 적절한 **Subscriber**에게 전달합니다.

##### 📌 특징:

- Eclipse 재단에서 관리하는 오픈소스 프로젝트
- 매우 가볍고 빠름
- 시스템 서비스로 실행 가능 (`systemd`, `init.d`)
- 설정 파일: `/etc/mosquitto/mosquitto.conf`



PC에서 Jetson Nano를 MQTT(Mosquitto 브로커 활용)로 제어하려면, 다음과 같은 구조로 시스템을 구성하면 됩니다:

------

### ✅ 기본 구성

```css
[PC(Client/Publisher)] ←→ [Mosquitto Broker] ←→ [Jetson Nano(Client/Subscriber)]
```

- **PC**: 제어 명령을 보내는 Publisher 역할 및 메시지를 중계하는 Broker 역할
- **Jetson Nano**: 명령을 받아서 동작하는 Subscriber 역할

------

### 1️⃣ Mosquitto 브로커 설치 (PC 또는 Jetson 중 한 곳 또는 제3의 서버)

#### 예: PC(Ubuntu)에 Mosquitto 설치

```
sudo apt install mosquitto
```

#### 예: PC(Ubuntu)에 Mosquitto-client 설치


```
sudo apt install mosquitto-clients
```

#### Mosquitto MQTT 브로커 서비스 자동시작 설정

```
sudo systemctl enable mosquitto
```

#### 2️⃣ Jetson Nano에 MQTT 클라이언트 설치

```
pip3 install paho-mqtt
```

#### MQTT Mosquitto 테스트

------

USB연결을 이용할 경우 PC의 IP는 `192.168.55.100`, 젯슨나노의 IP는 `192.168.55.1`이 할당된다. Mosquitto를 PC에 설치했으므로 브로커 주소는 `192.168.55.100`이다. 테스트를 위해 다음 명령을 실행한다.

**Jetson**에서

```
mosquitto_sub -h 192.168.55.100 -t jetson/control -m
```



**PC**에서 다음 명령을 실행하면

```
mosquitto_pub -h 192.168.55.100 -t jetson/control -m "tilt_up"
```

`mosquitto_sub -h 192.168.55.100 -t jetson/control -m`을 구동해 둔Jetson 쪽 터미널에 아래와 같이 해당 메세지가 출력된다.

```
mosquitto_sub -h 192.168.55.100 -t jetson/control
tilt_up
```

다시 **PC**에서 다음 명령을 실행하면

```
mosquitto_pub -h 192.168.55.100 -t jetson/control -m "tilt_down"
```

`mosquitto_sub -h 192.168.55.100 -t jetson/control`을 구동해 둔**Jetson** 쪽 터미널에 아래와 같이 해당 메세지가 출력된다.

```
mosquitto_sub -h 192.168.55.100 -t jetson/control
tilt_up
tilt_down
```












### 3️⃣ Jetson Nano: Subscriber 코드 예시

```
pythonCopyEdit# jetson_subscriber.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("jetson/control")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    if msg.payload.decode() == "led_on":
        print("LED ON command received")
        # GPIO 제어나 실행 코드 삽입
    elif msg.payload.decode() == "led_off":
        print("LED OFF command received")
        # GPIO 제어 OFF

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.100", 1883, 60)  # Mosquitto 브로커 IP

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







**[목록 열기](../README.md)** 
