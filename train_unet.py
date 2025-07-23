import os
import cv2
import numpy as np
from glob import glob
from tqdm import tqdm
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as T

# -------------------------
# U-Net 모델 정의
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
# 커스텀 데이터셋
# -------------------------
class LineSegDataset(Dataset):
    def __init__(self, image_paths, mask_paths):
        self.image_paths = image_paths
        self.mask_paths = mask_paths

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, i):
        image = cv2.imread(self.image_paths[i], cv2.IMREAD_GRAYSCALE)
        mask = cv2.imread(self.mask_paths[i], cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (256, 256))
        mask = cv2.resize(mask, (256, 256))

        image = image.astype(np.float32) / 255.0
        mask = (mask > 127).astype(np.float32)

        image = torch.tensor(image).unsqueeze(0)
        mask = torch.tensor(mask).unsqueeze(0)

        return image, mask


# -------------------------
# 파일명 기준 매칭 유틸
# -------------------------
def get_matching_pairs(image_dir, mask_dir, image_ext=".jpg", mask_ext=".png"):
    image_files = sorted(glob(os.path.join(image_dir, "*" + image_ext)))
    mask_files = sorted(glob(os.path.join(mask_dir, "*" + mask_ext)))

    image_basenames = set(os.path.splitext(os.path.basename(p))[0] for p in image_files)
    mask_basenames = set(os.path.splitext(os.path.basename(p))[0] for p in mask_files)

    common_basenames = sorted(image_basenames & mask_basenames)

    matched_images = [os.path.join(image_dir, name + image_ext) for name in common_basenames]
    matched_masks = [os.path.join(mask_dir, name + mask_ext) for name in common_basenames]

    # 디버깅용 출력
    print("공통 파일 수:", len(common_basenames))
    print("이미지 전용:", sorted(image_basenames - mask_basenames))
    print("마스크 전용:", sorted(mask_basenames - image_basenames))

    return matched_images, matched_masks


# -------------------------
# 학습 루프
# -------------------------
def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    image_paths, mask_paths = get_matching_pairs("dataset/images", "dataset/masks", ".jpg", ".png")
    print("학습용 샘플 수:", len(image_paths))

    dataset = LineSegDataset(image_paths, mask_paths)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    model = UNet().to(device)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(20):
        model.train()
        total_loss = 0

        for images, masks in tqdm(loader):
            images, masks = images.to(device), masks.to(device)

            preds = model(images)
            loss = criterion(preds, masks)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print("Epoch %d - Loss: %.4f" % (epoch + 1, total_loss / len(loader)))

    torch.save(model.state_dict(), "unet_line.pth")
    print("모델 저장 완료: unet_line.pth")


# -------------------------
# 실행 시작점
# -------------------------
if __name__ == "__main__":
    train()

