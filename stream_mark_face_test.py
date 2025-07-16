import cv2
import numpy as np
import requests

# MJPEG 스트림 URL
url = 'http://10.42.0.198:8080/video_feed'

# Haar Cascade 얼굴 검출 모델 로드
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print(f"❌ Error: Cannot load Haar cascade from {cascade_path}")
    exit()

# 스트리밍 요청 시작
stream = requests.get(url, stream=True)
if stream.status_code != 200:
    print(f"❌ Failed to connect to {url}")
    exit()

bytes_buffer = b''

try:
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_buffer += chunk
        a = bytes_buffer.find(b'\xff\xd8')  # JPEG 시작
        b = bytes_buffer.find(b'\xff\xd9')  # JPEG 끝

        if a != -1 and b != -1:
            jpg = bytes_buffer[a:b + 2]
            bytes_buffer = bytes_buffer[b + 2:]

            img_array = np.frombuffer(jpg, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if frame is None:
                continue

            # 프레임 크기 변경 (예: 640x480) → 해상도 올림
            frame = cv2.resize(frame, (320, 240))

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,     # 더 민감하게 (기존 1.1 → 1.05)
                minNeighbors=3,       # 이웃 개수 줄여 탐지 폭 약간 넓힘
                minSize=(20, 20)      # 더 작은 얼굴도 탐지
            )

            print(f"👀 Detected faces: {len(faces)}")

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 파란색 BGR

            cv2.imshow("Jetson Nano Stream", frame)

            # ESC 키로 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break

except KeyboardInterrupt:
    print("\n⛔ Stopped by user (KeyboardInterrupt)")

finally:
    cv2.destroyAllWindows()

