jetson nano

```
sudo nmcli device wifi connect "MyWiFi" password "mypassword123"
```

```
sudo reboot
```

pc

```
nmap -sn 10.42.0.0/24
Starting Nmap 7.80 ( https://nmap.org ) at 2025-07-14 16:27 KST
Nmap scan report for 10.42.0.1
Host is up (0.00023s latency).
Nmap scan report for 10.42.0.198
Host is up (0.013s latency).
Nmap done: 256 IP addresses (2 hosts up) scanned in 15.83 seconds
```

```
ssh soda@10.42.0.198
```

