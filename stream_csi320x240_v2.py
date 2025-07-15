import cv2
from flask import Flask, Response

app = Flask(__name__)

# GStreamer 파이프라인 수정:
# nvjpegenc 플러그인을 추가하여 파이프라인 내에서 하드웨어(GPU) JPEG 인코딩을 수행합니다.
# appsink는 이제 압축된 JPEG 데이터를 받습니다.
gst_str_hw_accelerated = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! "
    "nvvidconv ! "
    "video/x-raw, width=320, height=240, format=BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=I420 ! "
    "nvjpegenc ! "
    "appsink"
)

# 수정된 파이프라인으로 VideoCapture 객체를 생성합니다.
cap = cv2.VideoCapture(gst_str_hw_accelerated, cv2.CAP_GSTREAMER)

def gen_frames():
    """스트리밍을 위한 프레임 생성기 함수"""
    while True:
        # GStreamer 파이프라인으로부터 프레임을 읽습니다.
        success, frame_data = cap.read()
        if not success:
            print("캡처 장치에서 프레임을 읽는 데 실패했습니다.")
            break

        # 파이프라인에서 이미 JPEG으로 인코딩된 데이터가 넘어오므로
        # 별도의 cv2.imencode 과정이 필요 없습니다.
        # frame_data를 바로 바이트로 변환합니다.
        frame_bytes = frame_data.tobytes()

        # HTTP 스트리밍 형식에 맞춰 프레임을 반환합니다.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """비디오 스트리밍 경로"""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """간단한 웹페이지를 렌더링하여 비디오 스트림을 표시합니다."""
    return """
    <html>
      <head>
        <title>하드웨어 가속 비디오 스트리밍</title>
      </head>
      <body>
        <h1>실시간 카메라 스트림</h1>
        <img src="/video_feed" width="320" height="240">
      </body>
    </html>
    """

if __name__ == "__main__":
    if not cap.isOpened():
        print("에러: GStreamer 파이프라인을 열 수 없습니다.")
        print("카메라가 연결되어 있는지, GStreamer 플러그인이 올바르게 설치되었는지 확인하세요.")
    else:
        # 0.0.0.0 호스트를 사용하여 외부에서도 접속할 수 있도록 합니다.
        app.run(host='0.0.0.0', port=8080, threaded=True)
