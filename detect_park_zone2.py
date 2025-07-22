import cv2
import numpy as np
import requests
import time

# MJPEG 스트림 URL
url = "http://10.42.0.170:8080/video_feed"
stream = requests.get(url, stream=True)
if stream.status_code != 200:
    print("Failed to connect to %s" % url)
    exit()

bytes_buffer = b''
frame_count = 0  # 저장 프레임 번호용

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

            original = frame.copy()
            h, w = frame.shape[:2]

            # --- 전처리 ---
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, binary = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

            # --- 윤곽선 검출 ---
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            found_any = False

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < 3000:
                    continue

                approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

                # 사각형 후보만 시각화 (너무 조건 제한 없이)
                if len(approx) == 4:
                    cv2.drawContours(original, [approx], -1, (0, 255, 255), 2)  # 노란색
                    found_any = True

                    # 비율, 아래변 길이 분석
                    x, y, w_rect, h_rect = cv2.boundingRect(approx)
                    aspect_ratio = float(w_rect) / h_rect if h_rect != 0 else 0

                    # 아래변 추정: y 값 큰 두 점
                    pts = approx[:, 0, :]
                    pts_sorted = sorted(pts, key=lambda p: p[1], reverse=True)
                    bottom_len = np.linalg.norm(pts_sorted[0] - pts_sorted[1])

                    print("Area=%.1f  Ratio=%.2f  BottomEdge=%.1f" %
                          (area, aspect_ratio, bottom_len))

            # --- 이미지 저장 ---
            filename = "debug_frame_%04d.jpg" % frame_count
            cv2.imwrite(filename, original)
            frame_count += 1

            # --- 화면 표시 ---
            cv2.imshow("Debug Frame", original)
            cv2.imshow("Binary", binary)

            if cv2.waitKey(1) & 0xFF == 27:
                break

except KeyboardInterrupt:
    print("Interrupted")

finally:
    cv2.destroyAllWindows()

