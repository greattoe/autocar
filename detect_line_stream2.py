import cv2
import numpy as np
import torch
import torch.nn as nn
import requests

# -------------------------
# UNet 모델 정의
# -------------------------
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

# -------------------------
# 마스크 및 기울기 계산 함수
# -------------------------
def get_mask_and_angle(model, frame, device):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (256, 256)).astype(np.float32) / 255.0
    tensor = torch.tensor(resized).unsqueeze(0).unsqueeze(0).to(device)

    with torch.no_grad():
        pred = model(tensor)[0][0].cpu().numpy()

    pred_mask = (pred > 0.5).astype(np.uint8) * 255
    pred_mask = cv2.resize(pred_mask, (frame.shape[1], frame.shape[0]))

    # 윤곽선 추출
    contours, _ = cv2.findContours(pred_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    angle_deg = None

    overlay = frame.copy()
    if contours:
        largest = max(contours, key=cv2.contourArea)
        if len(largest) >= 2:
            # 직선 피팅
            vx, vy, x0, y0 = cv2.fitLine(largest, cv2.DIST_L2, 0, 0.01, 0.01)
            angle_rad = np.arctan2(vx, vy)
            angle_deg = 90 - np.degrees(angle_rad)  # 수직 기준으로 회전

            # 선 그리기
            h, w = pred_mask.shape
            x1 = int(x0 - vx * 1000)
            y1 = int(y0 - vy * 1000)
            x2 = int(x0 + vx * 1000)
            y2 = int(y0 + vy * 1000)
            cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # 텍스트 출력
            cv2.putText(overlay, "Angle: %.1f deg" % angle_deg, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    return pred_mask, overlay, angle_deg

# -------------------------
# 메인 루프 (스트리밍)
# -------------------------
def main():
    model_path = "unet_line.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = UNet().to(device)
    state_dict = torch.load(model_path, map_location=device, weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()

    url = 'http://192.168.0.19:8080/video_feed'
    stream = requests.get(url, stream=True)
    if stream.status_code != 200:
        print("Failed to connect to %s" % url)
        return

    bytes_buffer = b''

    print("Start MJPEG stream with line detection (ESC to quit)...\n")

    for chunk in stream.iter_content(chunk_size=1024):
        bytes_buffer += chunk
        a = bytes_buffer.find(b'\xff\xd8')
        b = bytes_buffer.find(b'\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes_buffer[a:b+2]
            bytes_buffer = bytes_buffer[b+2:]

            img_array = np.frombuffer(jpg, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is None:
                continue

            mask, overlay, angle = get_mask_and_angle(model, frame, device)
            cv2.imshow("Overlay", overlay)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cv2.destroyAllWindows()
    print("Stream ended.\n")

if __name__ == "__main__":
    main()

