import cv2
import numpy as np
import requests
import paho.mqtt.publish as publish

margin_x = 50
margin_y = 30


# MQTT 설정
#broker_ip = "172.20.10.5"  # 핫스팟 연결 시
broker_ip = "192.168.55.100"  # USB 연결 시
topic = "pt/control"

def pub_msg(msg):
    publish.single(topic, msg, hostname=broker_ip)

# MJPEG 스트림 URL
url = 'http://192.168.55.1:8080/video_feed'
#url = 'http://172.20.10.2:8080/video_feed'
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

            src = cv2.resize(frame, (320, 240))
            hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

            # 파란색 범위 설정
            lower_blue = np.array([100, 100, 120])
            upper_blue = np.array([150, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            res = cv2.bitwise_and(src, src, mask=mask)

            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            _, bin = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            largest_contour = None
            largest_area = 0

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > largest_area:
                    largest_area = area
                    largest_contour = cnt

            if largest_contour is not None and largest_area > 500:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center_x = x + w // 2
                center_y = y + h // 2
                print("center: ( %s, %s )" % (center_x, center_y))

                if center_x < 160 - margin_x:
                    pub_msg("left");    print("left")
                elif center_x > 160 + margin_x:
                    pub_msg("right");   print("right")
                else:
                    pass
                if center_y < 120 - margin_y:
                    pub_msg("up");    print("up")
                elif center_y > 120 + margin_y:
                    pub_msg("down");   print("down")
                else:
                    pass

            cv2.imshow("Videosrc", src)
            if cv2.waitKey(5) & 0xFF == 27:
                break

except KeyboardInterrupt:
    print("\n🛑 Stopped by user (KeyboardInterrupt)")

finally:
    cv2.destroyAllWindows()

