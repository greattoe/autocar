import cv2
from pop import Util
Util.enable_imshow()

cam = Util.gstrmer(width=640, height=480)
camera = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)
if not camera.isOpened():
    print("Not found camera")
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("init width: %s, init height: %s" % (width,height))

while True:
    ret, frame = camera.read()
    if not ret:
        break
    cv2.imshow("soda", frame)
camera.release()
cv2.destroyAllWindows()

