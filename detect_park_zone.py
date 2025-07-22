import cv2
import numpy as np
import requests

# MJPEG 스트림 URL
url = "http://10.42.0.170:8080//video_feed"
stream = requests.get(url, stream=True)
if stream.status_code != 200:
    print("Failed to connect to %s" % url)
    exit()

bytes_buffer = b''

try:
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_buffer += chunk
        a = bytes_buffer.find(b'\xff\xd8')  # JPEG 시작
        b = bytes_buffer.find(b'\xff\xd9')  # JPEG 끝

        if a != -1 and b != -1:
            jpg = bytes_buffer[a:b+2]
            bytes_buffer = bytes_buffer[b+2:]

            img_array = np.frombuffer(jpg, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if frame is None:
                continue

            # --- 처리 시작 ---
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, binary = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 5000:  # 너무 작은 노이즈 제거
                    approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
                    if len(approx) == 4 and cv2.isContourConvex(approx):
                        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
                        cv2.putText(frame, "Parking Zone", tuple(approx[0][0]), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (0, 255, 0), 2)

            cv2.imshow("Parking Detection", frame)
            cv2.imshow("Binary", binary)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
                break

except KeyboardInterrupt:
    print("Interrupted")

finally:
    cv2.destroyAllWindows()

