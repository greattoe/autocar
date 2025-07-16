import cv2
import numpy as np
import requests

# MJPEG 스트림 URL
url = 'http://10.42.0.198:8080/video_feed'

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
        src = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)    # Convert from BGR to HSV
         # define range of blue color in HSV
        lower_blue = np.array([100,100,120])          # range of blue
        upper_blue = np.array([150,255,255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)     # color range of blue
        
        res1 = cv2.bitwise_and(src, src, mask=mask)      # apply blue mask
        gray = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)   
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
                
        if largest_contour is not None:
            if largest_area > 500:  # draw only larger than 500
                x, y, width, height = cv2.boundingRect(largest_contour)
                cv2.rectangle(src, (x, y), (x + width, y + height), COLOR, 2)
                center_x = x + width//2
                center_y = y + height//2
                print("center: ( %s, %s )"%(center_x, center_y))
                
        cv2.imshow("Videosrc",src)       # show original src
        
        
        
        
        
        

        if frame is not None:
            cv2.imshow("Jetson Stream", frame)
            
            k = cv2.waitKey(5) & 0xFF
            
            if k == 27:
                break
            
        # ESC 키 누르면 종료
        if cv2.waitKey(1) == 27:
            break

        cv2.destroyAllWindows()

