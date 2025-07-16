**PC**에서의 **`ifconfig`실행 결과**

```
ifconfig
enx2ab1a1ba45da: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether 2a:b1:a1:ba:45:da  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.55.100  netmask 255.255.255.0  broadcast 192.168.55.255
        inet6 fe80::594a:348d:3c9d:b78  prefixlen 64  scopeid 0x20<link>
        ether c2:6e:cd:be:65:5d  txqueuelen 1000  (Ethernet)
        RX packets 1854  bytes 645278 (645.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1986  bytes 326550 (326.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 52040  bytes 5396446 (5.3 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 52040  bytes 5396446 (5.3 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlo1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.2.18.230  netmask 255.255.254.0  broadcast 10.2.19.255
        inet6 fe80::e66e:430c:94f6:2a35  prefixlen 64  scopeid 0x20<link>
        ether 8c:17:59:d3:dd:4e  txqueuelen 1000  (Ethernet)
        RX packets 8750154  bytes 11238706010 (11.2 GB)
        RX errors 0  dropped 1310  overruns 0  frame 0
        TX packets 1464313  bytes 517578913 (517.5 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```



**Jetson**에서의 **`ifconfig`실행 결과**

```
ifconfig                                                
ap0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500                       
        inet 192.168.2.1  netmask 255.255.255.0  broadcast 192.168.2.255        
        inet6 fe80::a66b:b6ff:fe07:126b  prefixlen 64  scopeid 0x20<link>       
        ether a4:6b:b6:07:12:6b  txqueuelen 1000  (Ethernet)                    
        RX packets 0  bytes 0 (0.0 B)                                           
        RX errors 0  dropped 0  overruns 0  frame 0                             
        TX packets 111  bytes 24958 (24.9 KB)                                   
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0              
                                                                                
eth0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500                              
        inet 192.168.101.101  netmask 255.255.255.0  broadcast 192.168.101.255  
        ether 48:b0:2d:3d:44:7f  txqueuelen 1000  (Ethernet)                    
        RX packets 0  bytes 0 (0.0 B)                                           
        RX errors 0  dropped 0  overruns 0  frame 0                             
        TX packets 0  bytes 0 (0.0 B)                                           
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0              
        device interrupt 150  base 0xe000                                       
                                                                                
l4tbr0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500                    
        inet 192.168.55.1  netmask 255.255.255.0  broadcast 192.168.55.255      
        inet6 fe80::28b1:a1ff:feba:45d9  prefixlen 64  scopeid 0x20<link>       
        inet6 fe80::1  prefixlen 128  scopeid 0x20<link>                        
        ether 2a:b1:a1:ba:45:d9  txqueuelen 1000  (Ethernet)                    
        RX packets 1594  bytes 224089 (224.0 KB)
        RX errors 0  dropped 8  overruns 0  frame 0
        TX packets 1625  bytes 404760 (404.7 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```



현재 상황을 요약하면 다음과 같습니다:

- **PC ↔ 젯슨나노**는 USB 연결 (호스트 PC의 `eth0` = `192.168.55.100`, 젯슨의 `l4tbr0` = `192.168.55.1`)
- **PC ↔ 인터넷**은 Wi-Fi (`wlo1` = `10.2.18.230`)
- **젯슨 나노는 인터넷에 연결되어 있지 않음**

------

### 🎯 목표:

**PC를 통해 젯슨 나노가 인터넷에 접속하도록 만들기**
 즉, **PC를 NAT 게이트웨이처럼 동작**하게 하고, 젯슨 나노가 USB 이더넷 경유로 인터넷을 사용할 수 있게 해야 함.

------

## ✅ 해결 방법 (Ubuntu PC 기준)

### 1. PC에서 IP 포워딩 활성화

```bash
bash


CopyEdit
sudo sysctl -w net.ipv4.ip_forward=1
```

영구 설정:

```bash
bashCopyEditsudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
sudo sysctl -p
```

------

### 2. PC에서 NAT (MASQUERADE) 설정 (wlo1 → eth0/l4tbr0)

```bash
bashCopyEditsudo iptables -t nat -A POSTROUTING -o wlo1 -j MASQUERADE
sudo iptables -A FORWARD -i wlo1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlo1 -j ACCEPT
```

(※ `eth0`은 PC 입장에서 젯슨 나노가 연결된 USB 인터페이스입니다. 확인해보면 실제 이름은 `enx2ab1a1ba45da`일 수 있으니 맞게 수정해야 함)

------

### 3. 젯슨 나노에 **게이트웨이와 DNS 설정**

젯슨 나노에서 다음 명령을 실행:

```bash
sudo ip route add default via 192.168.55.100
```

```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```



### 4. 인터넷 확인

젯슨 나노에서:

```bash
ping 8.8.8.8     # IP 통신 가능 여부 확인
```

```bash
ping google.com  # DNS까지 정상 작동 확인
```

---


## ⚠️ 참고

`iptables` 설정 유지를 위해  `iptables-persistent` 패키지를 설치

```bash
sudo apt install iptables-persistent
```

현재 `iptables` 규칙 저장

```
sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null
```

------

### 💡 요약

1. PC에서 IP 포워딩 켜기
2. PC에서 `wlo1` → `USB 이더넷` NAT 설정
3. 젯슨 나노에 default gateway와 DNS 설정
4. 젯슨에서 인터넷 접속 확인



