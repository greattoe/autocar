import cv2
import numpy as np
import torch
import torch.nn as nn

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
# 프레임 예측 함수
# -------------------------
def predict_frame(model, frame, device):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (256, 256)).astype(np.float32) / 255.0
    tensor = torch.tensor(resized).unsqueeze(0).unsqueeze(0).to(device)

    with torch.no_grad():
        pred = model(tensor)[0][0].cpu().numpy()

    pred_mask = (pred > 0.5).astype(np.uint8) * 255
    pred_mask = cv2.resize(pred_mask, (frame.shape[1], frame.shape[0]))

    overlay = frame.copy()
    overlay[pred_mask > 127] = [0, 255, 0]  # 초록색 라인 표시

    return pred_mask, overlay


# -------------------------
# 메인 루프
# -------------------------
def main():
    model_path = "unet_line.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = UNet().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Failed to open camera.\n")
        return

    print("Start real-time line prediction (press ESC to quit)...\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.\n")
            break

        mask, overlay = predict_frame(model, frame, device)

        cv2.imshow("Overlay", overlay)
        # cv2.imshow("Mask", mask)  # Debug용

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Camera released and windows destroyed.\n")

if __name__ == "__main__":
    main()

