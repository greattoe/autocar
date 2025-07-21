### 파이썬에서 사용할 수 있는 AR Marker 라이브러리 설치

코드 출처: https://github.com/MomsFriendlyRobotCompany/ar_markers.git

#### 1. 필수 패키지 설치

```bash
sudo apt install python3-pip python3-setuptools python3-dev git
```

#### 2. ar_markers 저장소 클론

```bash
git clone https://github.com/MomsFriendlyRobotCompany/ar_markers.git
```



#### 3. 추가 의존성 설치

```
pip3 install numpy opencv-python
```



#### 4. `ar_markers` 저장소가 클론된 폴더로 작업 경로변경.

```
cd ~/ar_markers
```



#### 5. `setup.py`를 이용한 설치

```
pip3 install . --user
```



#### 6. 설치 확인

마커 생성 코드 수정

```
gedit ~/ar_markers/bin/ar_markers_generate.py
```

`ar_markers_generate.py` 1행의 `shebang`부분인 `#!/usr/bin/env python`를 `#!/usr/bin/env python3`로 수정한다.

마커 인식 예제 코드 수정

```
gedit ~/ar_markers/bin/ar_markers_scan.py
```

`ar_markers_scan.py`  1행의 `shebang`부분인 `#!/usr/bin/env python`를 `#!/usr/bin/env python3`로 수정한다.





```
python3 ./bin/ar_markers_generate.py --id 1
```

```

{'generate': None, 'id': 1, 'path': '.'}
Generated Marker with ID 1
Done!
```

```
ls
ar_markers           build  LICENSE        pics        tests
ar_markers.egg-info  dev    marker_1.png   readme.rst
bin                  dist   marker_images  setup.py
gnd0@a10sc:~/ar_markers$ ls -al
```

위의`ls`실행 결과를 보면 `marker_1.png`가 생성된 것을 확인할 수 있다.

다음은 탐색기에서 확인한 결과이다. 

![](/home/gnd0/autocar/md/img/result_of_ar_markers_generate.png)



