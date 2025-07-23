import cv2, sys, os, time
import numpy as np
import math
import requests
import torch
import torch.nn as nn
import paho.mqtt.publish as publish

broker_ip = "10.42.0.1"
topic = "car/control"
cmd = 'mosquitto_pub -h 10.42.0.1 -t car/control -m "stop"'

def pub_msg(msg):
    publish.single(topic, msg, hostname=broker_ip)

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

class UNet(nn.Module):
    def __init__(self):
        super().__init__()
        def CBR(in_ch, out_ch):
            return nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 3, padding=1),
                nn.ReLU(inplace=True),
                nn.Conv2d(out_ch, out_ch, 3, padding=1),
                nn.ReLU(inplace=True)
            )
        self.enc1 = CBR(1, 64)
        self.enc2 = CBR(64, 128)
        self.enc3 = CBR(128, 256)
        self.pool = nn.MaxPool2d(2)
        self.bottleneck = CBR(256, 512)
        self.up3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = CBR(512, 256)
        self.up2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = CBR(256, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = CBR(128, 64)
        self.out = nn.Conv2d(64, 1, 1)

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        b = self.bottleneck(self.pool(e3))
        d3 = self.up3(b)
        d3 = self.dec3(torch.cat([d3, e3], dim=1))
        d2 = self.up2(d3)
        d2 = self.dec2(torch.cat([d2, e2], dim=1))
        d1 = self.up1(d2)
        d1 = self.dec1(torch.cat([d1, e1], dim=1))
        return torch.sigmoid(self.out(d1))

def main():
    model_path = "unet_line.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = UNet().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    url = 'http://192.168.55.1:8080/video_feed'

    try:
        pub_msg("straight")
        pub_msg("forward")

        stream = requests.get(url, stream=True)
        if stream.status_code != 200:
            print("Failed to connect to", url)
            return

        bytes_buffer = b''

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

                frame = cv2.resize(frame, (640, 480))
                roi, roi_x1, roi_y1, roi_x2, roi_y2 = extract_roi(frame)

                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, (256, 256)).astype(np.float32) / 255.0
                tensor = torch.tensor(resized).unsqueeze(0).unsqueeze(0).to(device)

                with torch.no_grad():
                    pred = model(tensor)[0][0].cpu().numpy()

                pred_mask = (pred > 0.5).astype(np.uint8) * 255
                pred_mask = cv2.resize(pred_mask, (roi.shape[1], roi.shape[0]))

                edges = cv2.Canny(pred_mask, 50, 150)
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

                cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 255, 0), 2)
                cv2.imshow("Stream Line Detection", frame)

                if cv2.waitKey(5) & 0xFF == 27:
                    break

    except KeyboardInterrupt:
        os.system(cmd)
        print("\nStopped by user.")

    finally:
        os.system(cmd)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

