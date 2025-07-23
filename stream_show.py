import cv2
import numpy as np
import requests

# MJPEG 스트림 URL
url = 'http://10.42.0.66:8080/video_feed'

# 스트리밍 요청 시작
stream = requests.get(url, stream=True)
if stream.status_code != 200:
    print("Failed to connect to %s" % url)
    exit()

bytes_buffer = b''

for chunk in stream.iter_content(chunk_size=1024):
    bytes_buffer += chunk
    a = bytes_buffer.find(b'\xff\xd8')  # JPEG 시작
    b = bytes_buffer.find(b'\xff\xd9')  # JPEG 끝

    if a != -1 and b != -1:
        jpg = bytes_buffer[a:b+2]
        bytes_buffer = bytes_buffer[b+2:]

        img_array = np.frombuffer(jpg, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        
        
        

        if frame is not None:
            cv2.imshow("Jetson Stream", frame)

        # ESC 키 누르면 종료
        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()

