## AIoT AutoCar Prime 활용 실습


>
>1. **[CLI환경에서의 WiFi연결](./md/how2connect_wifi_cli_env.md)**
>2. [PC 인터넷 연결 공유를 통한**Jetson 인터넷 연결**](./md/how2connect_jetson2internet.md) 
>3. **[MQTT Mosquitto](./md/mqtt_mosquitto.md)** 









**Jetson**의 `/etc/rc.local`편집

```
sudo nano /etc/rc.local
```

```
#!/bin/bash
sleep 10

/usr/sbin/nvpmodel -m 0

/usr/bin/jetson_clocks

/bin/echo 255 > /sys/devices/pwm-fan/target_pwm

exit 0

```

