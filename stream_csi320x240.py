import cv2
from flask import Flask, Response
import time

app = Flask(__name__)

gst_str = ("nvarguscamerasrc ! "
           "video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! "
           "nvvidconv ! video/x-raw, width=320, height=240, format=BGRx ! "
           "videoconvert ! "
           "video/x-raw, format=BGR ! appsink")

cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)  # 약 10fps로 제한

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<img src="/video_feed">'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

