import cv2
from flask import Flask, Response

app = Flask(__name__)

# GStreamer 파이프라인 (640x480, 30fps, 하드웨어 JPEG 인코딩)
gst_str_hw_accelerated = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! "
    "nvvidconv ! "
    "video/x-raw, width=640, height=480, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! "
    "appsink"
)

# VideoCapture 객체 생성
cap = cv2.VideoCapture(gst_str_hw_accelerated, cv2.CAP_GSTREAMER)

def gen_frames():
    """스트리밍을 위한 프레임 생성기 함수"""
    while True:
        success, frame = cap.read()
        if not success or frame is None:
            print("⚠️ 프레임을 읽지 못했습니다. 다시 시도합니다...")
            continue  # 중단하지 않고 계속 시도

        # 프레임을 JPEG으로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("⚠️ JPEG 인코딩 실패")
            continue

        frame_bytes = buffer.tobytes()

        # MJPEG 형식으로 HTTP 응답 구성
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
      <head>
        <title>실시간 카메라 스트리밍</title>
      </head>
      <body>
        <h1>Jetson 카메라 스트림 (640x480)</h1>
        <img src="/video_feed" width="640" height="480">
      </body>
    </html>
    """

if __name__ == "__main__":
    if not cap.isOpened():
        print(" 에러: GStreamer 파이프라인을 열 수 없습니다.")
        exit(1)
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

