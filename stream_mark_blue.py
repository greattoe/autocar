import cv2
import numpy as np
import requests

url = 'http://10.42.0.198:8080/video_feed'

stream = requests.get(url, stream=True)
if stream.status_code != 200:
    print("Failed to connect to %s" % url)
    exit()

bytes_buffer = b''

try:
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_buffer += chunk
        a = bytes_buffer.find(b'\xff\xd8')  # JPEG start
        b = bytes_buffer.find(b'\xff\xd9')  # JPEG end

        if a != -1 and b != -1:
            jpg = bytes_buffer[a:b + 2]
            bytes_buffer = bytes_buffer[b + 2:]

            img_array = np.frombuffer(jpg, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if frame is None:
                continue

            src = frame.copy()
            hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

            lower_blue = np.array([100, 100, 120])
            upper_blue = np.array([150, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            res = cv2.bitwise_and(src, src, mask=mask)

            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            _, bin = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            largest_contour = None
            largest_area = 0
            COLOR = (0, 255, 0)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > largest_area:
                    largest_area = area
                    largest_contour = cnt

            if largest_contour is not None and largest_area > 500:
                x, y, width, height = cv2.boundingRect(largest_contour)
                cv2.rectangle(src, (x, y), (x + width, y + height), COLOR, 2)
                center_x = x + width // 2
                center_y = y + height // 2
                print("center: ( %d, %d )" % (center_x, center_y))

            cv2.imshow("Videosrc", src)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

except KeyboardInterrupt:
    print("Stopped by user (KeyboardInterrupt)")

finally:
    cap = None
    cv2.destroyAllWindows()

