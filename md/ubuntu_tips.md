#### 아두이노 개발환경 1.8.19 설치

<a href = "https://downloads.arduino.cc/arduino-1.8.19-linux64.tar.xz?_gl=1*1tdqadx*_up*MQ..*_ga*MTEzMTE4OTQ5Ni4xNzQwNzI0OTI0*_ga_NEXN8H46L5*MTc0MDcyNDkyMS4xLjEuMTc0MDcyNTI1OS4wLjAuNDExOTU4NDk5">설치파일 다운로드</a>

위 다운로드 링크를 클릭하여 `arduino-1.8.19-linux64.tar`파일을 다운로드 후, 압축을 해제하면, `arduino-1.8.19-linux64`폴더 하위에 `arduino-1.8.19`폴더가 있고, 그 안에 `install.sh`쉘 스크립트 파일이 있다. 명령 창에서 해당 쉘 스크립트를 `sudo`권한으로 실행한다. 

```
cd Downloads/arduino-1.8.19-linux64/arduino-1.8.19/
```



```
sudo sh install.sh 
[sudo] password for $USER: 
Adding desktop shortcut, menu item and file associations for Arduino IDE...

 done!
```









#### 시리얼포트 접근 권한 설정

터미널에서 `id`명령 실행 시 `20(dialout)`그룹명 출력 여부 확인.

```
 id
uid=1000(gnd0) gid=1000(gnd0) groups=1000(gnd0),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),132(lxd),133(sambashare)
```

`20(dialout)`이 출력되지 않을 경우 다음 명령(dialout 그룹에 현재 로그인 되어 있는 사용자를 추가 하는 명령) 실행.

```
sudo usermod -a -G dialout $USER
```

위 명령이 반영되려면 컴퓨터를 재시작해야 한다. 재시작 후, 다시 터미널 창에서 id`명령을 실행한다.

```
id
uid=1000(gnd0) gid=1000(gnd0) groups=1000(gnd0),4(adm),20(dialout),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),132(lxd),133(sambashare)
```

​	`20(dialout)`이 추가된 것을 확인할 수 있다.





- **마우스 포인터 크기 변경**

  `Settings - Universal Access - Cursor Size`에서 변경할 수 있다. 

  ![](./img/settings_universial_access_cursor_size.png)

  ![](./img/cursor_size.png)

- **바탕화면에 인터넷 바로가기 생성**

  ​	

  바로가기 대상 URL이 `http://google.com`이라면, `~/Desktop/`경로에 `google.desktop`파일을 다음과 같이 작성 후, 저장한다. 

  ```
  [Desktop Entry]
  Name=Google
  Icon=google-chrome
  Type=Application
  Exec=google-chrome http://google.com
  ```

  `Icon`항목에 적어 줄 수 있는 어플리케이션은 `/usr/share/applications`에서 찾을 수 있다.

  ![](./img/choose_application4icon.png)

  바탕화면에서  `google.desktop`파일을 찾아 컨텍스트 메뉴에서 `Allow Launching`을 선택해 준다.

  ![](./img/allow_launching.png)

   `google.desktop`파일의 아이콘이 다음과 같이 바뀐 것을 확인 후, 더블클릭하여 실행 결과를 확인한다. 

​	![](./img/after_allow_launching.png)



- **grub 메뉴 편집을 위한 Grub Custermizer**

  

설치

```
sudo apt install grub-customizer
```



실행

윈도우 키를 눌러 나타난 탐색 화면에서 `gru`를 타이핑하면 `grub-customizer`실행 아이콘이 나타난다.

![](/home/gnd0/Documents/md/img/find_grub_custermizer.png)



#### 크롬 2025년 업데이트 후, 한글모드에서 키보드 입력오류(space, back space, enter 일부 기호 및 숫자 키) 발생할 경우.

크롬 삭제 후, 2024년 버전의 크롬 설치.



크롬 삭제:

```bash
sudo apt-get remove --purge google-chrome-stable
```



남아 있는 의존성 패키지 삭제:

```bash
udo apt-get autoremove
```

크롬 설정 파일 삭제:

```bash
rm -rf ~/.config/google-chrome
rm -rf ~/.cache/google-chrome
```

크롬 관련 캐시 및 데이터 파일 삭제:

```bash
sudo rm -rf /opt/google/chrome
sudo rm -rf /usr/local/google
```

크롬 다운로드

https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/



#### `nautilus` 탐색기 컨텍스트 메뉴에 의 `Open Terminator Here`메뉴 추가

`nautilus-open-terminal`제거

```bash
sudo apt remove nautilus-open-terminal
```



 사용자 정의 Nautilus 확장 스크립트 만들기

폴더생성

```bash
mkdir -p ~/.local/share/nautilus/scripts
```

스크립트 작성

```bash
gedit ~/.local/share/nautilus/scripts/Open\ Terminator\ Here
```

다음 내용으로 작성 , 저장, 종료

```sh
#!/bin/bash
terminator --working-directory="$PWD"

```



 실행 권한 부여

```bash
chmod +x ~/.local/share/nautilus/scripts/Open\ Terminator\ Here
```



`nautilus` 재시작

```bash
nautilus -q
```



탐색기에서 `~/.local/share/nautilus/scripts`폴더를 열어보면 다음과 같이 표시된다.

![](/home/gnd0/Documents/md/img/dot_local_share_nautilus_script.png)

필요한 `shell script`를 이 위치에 작성 후, 실행 속성을 부여하면, `nautilus`탐색기의 컨텍스트 메뉴에 해당메뉴가 나타난다는 것을 유추할 수 있다.

이미지 파일을 `pinta`로 여는 스크립트를 추가해 보자.

스크립트 작성

```bash
gedit ~/.local/share/nautilus/scripts/Open\ in\ Pinta
```



다음 내용으로 작성 , 저장, 종료


```sh
#!/bin/bash

# 하나 이상의 파일을 선택한 경우 반복해서 pinta로 열기
for file in "$@"; do
    pinta "$file" &
done

```



현재상태 확인

```
ls -l  ~/.local/share/nautilus/scripts/Open\ in\ Pinta
```

```
-rw-rw-r-- 1 gnd0 gnd0 135  6월 23 09:42 '/home/gnd0/.local/share/nautilus/scripts/Open in Pinta'
```



실행 권한 부여

```bash
chmod +x ~/.local/share/nautilus/scripts/Open\ in\ Pinta

```



현재상태 확인

```
ls -l  ~/.local/share/nautilus/scripts/Open\ in\ Pinta
```

```
-rwxrwxr-x 1 gnd0 gnd0 135  6월 23 09:42 '/home/gnd0/.local/share/nautilus/scripts/Open in Pinta'
```

 `-rw-rw-r--`부분이 `-rwxrwxr-x`와 같이 실행속성 `x`가 추가된 것을 알 수 있다. 



`nautilus` 재시작

```bash
nautilus -q
```



`nautilus`탐색기를 실행 후 이미지파일에서 마우스 우측버튼을 클릭하여 메뉴 추가 확인.

![](/home/gnd0/Documents/md/img/add_menu2nautilus_context_menu.png)



#### 컨텍스트 메뉴를 포함한 화면 캡쳐를 위한 지연 캡쳐

5초 후 캡쳐

```
gnome-screenshot -d 5
```



**`bash`로 기본`shell`변경**

일시적 변경

```
bash
```

지속적 변경

```
chsh -s /bin/bash
```

로그아웃 후 로그인하면 적용됨.

확인

```
echo $SHELL
/bin/bash
```



cli환경에서의 WiFi 연결

연결할 SSID가 **`nt930`** 이고 그 password가**`raspberry`** 인 경우

```
sudo nmcli device wifi connect "nt930" password "raspberry"
Device 'wlan0' successfully activated with '0391bfec-a95c-464c-917e-8a3cb6ea51bd'.

```



SD카드의 이미지 백업(사용중인 공간만)

#### 방법 1: `pishrink` (ext4 루트파티션 최소화 후 이미지 생성)

**장점:** SD카드 전체가 아닌 실제 사용 중인 ext4 영역만 백업. `.img` 크기 최소화 가능.
 **적합 대상:** Raspberry Pi 등에서 추출한 `.img`를 백업할 때 매우 유용.

**① 전체 이미지 만들기 (1회만)**

**SD카드 디바이스 이름**을 알아내기위해 `lsblk`실행

```bash
lsblk
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
loop0         7:0    0     4K  1 loop /snap/bare/5
loop1         7:1    0  55.5M  1 loop /snap/core18/2887
loop2         7:2    0  73.9M  1 loop /snap/core22/2010
loop3         7:3    0  63.8M  1 loop /snap/core20/2599
loop4         7:4    0  63.3M  1 loop /snap/core20/1828
loop5         7:5    0  73.9M  1 loop /snap/core22/2045
loop6         7:6    0   133M  1 loop /snap/typora/96
loop7         7:7    0 346.3M  1 loop /snap/gnome-3-38-2004/119
loop8         7:8    0  66.8M  1 loop /snap/core24/1006
loop9         7:9    0 321.1M  1 loop /snap/vlc/3777
loop10        7:10   0  50.9M  1 loop /snap/snapd/24718
loop11        7:11   0 290.8M  1 loop /snap/mesa-2404/887
loop12        7:12   0    46M  1 loop /snap/snap-store/638
loop13        7:13   0 589.6M  1 loop /snap/gnome-46-2404/117
loop14        7:14   0 233.6M  1 loop /snap/rpi-imager/709
loop15        7:15   0  49.3M  1 loop /snap/snapd/24792
loop16        7:16   0  12.2M  1 loop /snap/snap-store/1216
loop17        7:17   0   516M  1 loop /snap/gnome-42-2204/202
loop18        7:18   0  91.7M  1 loop /snap/gtk-common-themes/1535
loop19        7:19   0 349.7M  1 loop /snap/gnome-3-38-2004/143
loop20        7:20   0  66.8M  1 loop /snap/core24/1055
sda           8:0    1  29.8G  0 disk 
├─sda1        8:1    1  29.5G  0 part /media/gnd0/a5de35f9-f0d3-4993-8814-fe17ad
├─sda2        8:2    1    64M  0 part 
├─sda3        8:3    1    64M  0 part 
├─sda4        8:4    1   448K  0 part 
├─sda5        8:5    1   448K  0 part 
├─sda6        8:6    1    63M  0 part 
├─sda7        8:7    1   512K  0 part 
├─sda8        8:8    1   256K  0 part 
├─sda9        8:9    1   256K  0 part 
├─sda10       8:10   1   100M  0 part 
└─sda11       8:11   1    18K  0 part 
nvme0n1     259:0    0 953.9G  0 disk 
├─nvme0n1p1 259:1    0   260M  0 part /boot/efi
├─nvme0n1p2 259:2    0    16M  0 part 
├─nvme0n1p3 259:3    0 277.6G  0 part 
├─nvme0n1p4 259:4    0   922M  0 part 
├─nvme0n1p5 259:5    0   512G  0 part 
├─nvme0n1p6 259:6    0 144.3G  0 part /
├─nvme0n1p7 259:7    0  17.9G  0 part 
└─nvme0n1p8 259:8    0     1G  0 part
```



위 `lsblk` 출력에서, **SD 카드 디바이스가 `/dev/sda`**인 것을 알 수 있다.

## 

- `sda1`, `sda2`, … 는 **파티션**입니다. 전체 디바이스인 `/dev/sda`를 사용해야 부팅 영역까지 포함한 백업 가능

- 백업 작업을 위해 SD카드의 마운트 해제

  ```bash
  sudo umount /dev/sda*
  [sudo] password for gnd0: 
  umount: /dev/sda: not mounted.
  umount: /dev/sda10: not mounted.
  umount: /dev/sda11: not mounted.
  umount: /dev/sda2: not mounted.
  umount: /dev/sda3: not mounted.
  umount: /dev/sda4: not mounted.
  umount: /dev/sda5: not mounted.
  umount: /dev/sda6: not mounted.
  umount: /dev/sda7: not mounted.
  umount: /dev/sda8: not mounted.
  umount: /dev/sda9: not mounted.
  ```

`/dev/sda`전체 이미지 백업

```bash
sudo dd if=/dev/sda of=~/sdcard_backup.img bs=4M status=progress
31843155968 bytes (32 GB, 30 GiB) copied, 356 s, 89.4 MB/s 
7612+0 records in
7612+0 records out
31927042048 bytes (32 GB, 30 GiB) copied, 357.353 s, 89.3 MB/s
```

**② pishrink 설치**



```
git clone https://github.com/Drewsif/PiShrink.git
```

```
cd PiShrink
```

```
sudo chmod +x pishrink.sh
```

**③ 이미지 최소화**

```
dd if=~/min_img4jetson.img of=/dev/sdX bs=4M status=progressls *.img -al
-rw-r--r-- 1 root root 31927042048  7월 17 07:21 sdcard_backup.img
```

```
sudo ./pishrink.sh ./sdcard_backup.img ./min_img4jetson.img
[sudo] password for gnd0: 
PiShrink v24.10.23 - https://github.com/Drewsif/PiShrink

pishrink.sh: Copying ./sdcard_backup.img to ./min_img4jetson.img...
pishrink.sh: Gathering data
Creating new /etc/rc.local
pishrink.sh: Checking filesystem
/dev/loop21: 310792/1925760 files (0.1% non-contiguous), 4840061/7718395 blocks
resize2fs 1.45.5 (07-Jan-2020)
pishrink.sh: Shrinking filesystem
resize2fs 1.45.5 (07-Jan-2020)
Resizing the filesystem on /dev/loop21 to 5133898 (4k) blocks.
Begin pass 2 (max = 20323)
Relocating blocks             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Begin pass 3 (max = 236)
Scanning inode table          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Begin pass 4 (max = 39900)
Updating inode references     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
The filesystem on /dev/loop21 is now 5133898 (4k) blocks long.

pishrink.sh: Zeroing any free space left
pishrink.sh: Zeroed 1.3G
pishrink.sh: Shrinking partition
pishrink.sh: Truncating image
pishrink.sh: Shrunk ./min_img4jetson.img from 30G to 20G
```

```
ls *.img -al
-rw-r--r-- 1 root root 21340922368  7월 17 07:36 min_img4jetson.img
-rw-r--r-- 1 root root 31927042048  7월 17 07:21 sdcard_backup.img
```



**④ 복원**

```
sudo dd if=~/min_img4jetson.img of=/dev/sda bs=4M status=progress
[sudo] password for gnd0: 
21323841536 bytes (21 GB, 20 GiB) copied, 1207 s, 17.7 MB/s
5088+1 records in
5088+1 records out
21340922368 bytes (21 GB, 20 GiB) copied, 1207.72 s, 17.7 MB/s
gnd0@nt930:~$ sync
```



복원 작업이 종료되면 젯슨 나노 보드에서 정상부팅 확인 후, 필요에 따라루트 파티션 확장.







[튜토리얼 목록](../../README.md) 