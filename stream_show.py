import cv2
import numpy as np
import requests

# MJPEG 스트림 URL
url = 'http://10.42.0.198:8080/video_feed'

# 스트림 열기
stream = requests.get(url, stream=True)

# 프레임 처리를 위한 바이트 버퍼
bytes_buffer = b''

for chunk in stream.iter_content(chunk_size=1024):
    bytes_buffer += chunk
    a = bytes_buffer.find(b'\xff\xd8')  # JPEG 시작
    b = bytes_buffer.find(b'\xff\xd9')  # JPEG 끝

    if a != -1 and b != -1:
        jpg = bytes_buffer[a:b+2]
        bytes_buffer = bytes_buffer[b+2:]
        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            cv2.imshow('Jetson Stream', img)

        # 종료 키: ESC
        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()

