import cv2, sys, time
import numpy as np
import math
import requests

import paho.mqtt.publish as publish
broker_ip = "10.42.0.1"
topic = "car/control"
msg =''
def pub_msg(msg):
    publish.single(topic, msg, hostname=broker_ip)

# MJPEG 스트림 URL
url = 'http://10.42.0.198:8080/video_feed'
stream = requests.get(url, stream=True)
if stream.status_code != 200:
    print(f"Failed to connect to {url}")
    exit()

bytes_buffer = b''

def get_line_angle(line):
    x1, y1, x2, y2 = line[0]
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)
    vertical_angle = 90 - angle_deg
    return vertical_angle

def extract_roi(frame):
    h, w = frame.shape[:2]
    roi_y1 = int(h * 2 / 3)
    roi_y2 = h
    roi_x1 = int(w * 1 / 4)
    roi_x2 = int(w * 3 / 4)
    roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
    return roi, roi_x1, roi_y1, roi_x2, roi_y2

try:
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_buffer += chunk
        a = bytes_buffer.find(b'\xff\xd8')
        b = bytes_buffer.find(b'\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes_buffer[a:b + 2]
            bytes_buffer = bytes_buffer[b + 2:]

            img_array = np.frombuffer(jpg, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if frame is None:
                continue

            # 리사이즈 (optional)
            frame = cv2.resize(frame, (640, 480))

            # ROI 설정
            roi, roi_x1, roi_y1, roi_x2, roi_y2 = extract_roi(frame)

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, binary = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

            edges = cv2.Canny(binary, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180,
                                    threshold=80, minLineLength=50, maxLineGap=10)

            if lines is not None:
                longest = max(lines, key=lambda l: np.hypot(l[0][2] - l[0][0], l[0][3] - l[0][1]))
                angle = get_line_angle(longest)

                if angle > 90:
                    angle -= 180
                elif angle < -90:
                    angle += 180

                deviation = -angle

                if -40 <= deviation <= 40:
                    x1, y1, x2, y2 = longest[0]
                    cv2.line(frame,
                             (x1 + roi_x1, y1 + roi_y1),
                             (x2 + roi_x1, y2 + roi_y1),
                             (0, 255, 0), 3)

                    cv2.putText(frame, "Slope: %.1f deg" % deviation, (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                if deviation < -15:
                    pub_msg("left2")
                elif deviation < -5:
                    pub_msg("left1")
                elif deviation > 15:
                    pub_msg("right2")
                elif deviation > 5:
                    pub_msg("right1")
                else:
                    pub_msg("straight")

            # ROI 시각화 (하늘색)
            cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 255, 0), 2)

            cv2.imshow("Stream Line Detection", frame)
            # cv2.imshow("Binary", binary)  # 필요 시 활성화

            if cv2.waitKey(5) & 0xFF == 27:
                break

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    cv2.destroyAllWindows()

