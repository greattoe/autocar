## 머신러닝을 이용한 라인 검출

불규칙한 패턴의 회색조 배경으로부터 검정색 라인 검출 구현과 같은 작업과 같이 전통적인 영상처리 기법만으로는 한계가 있는 경우에 적용해 볼 수 닜는 방법이 **딥러닝 기반 분할(Segmentation)** 방법이다.

### 1. 데이터 준비

#### 수집

- 다양한 배경 조건에서 **검은 선이 존재하는 이미지와 없는 이미지**를 충분히 수집합니다.
- 조명, 각도, 배경 패턴에 변화를 주는 것이 중요합니다.

#### 라벨링 (지도 학습의 경우)

- 각 이미지에 대해 **검은 선의 위치를 마스크 이미지로 생성**합니다.
- 예시:
  - 입력 이미지: `gray_background_01.jpg`
  - 마스크 이미지: `gray_background_01_mask.png` (검은 선만 흰색(255), 나머지는 검정(0))

> Tip: `Labelme`, `CVAT`, `Supervisely` 같은 도구로 쉽게 라벨링할 수 있습니다.

------

### 2. 방법 선택

#### 방법 1: U-Net 기반 Semantic Segmentation (추천)

- **U-Net**은 의료 영상 등에서 라인/경계 검출에 강력한 성능을 보입니다.
- 작은 데이터셋으로도 좋은 결과를 낼 수 있습니다.

##### 간단한 모델 구조

```
plaintextCopyEditInput Image (H, W, 1)
   ↓
Convolution + MaxPooling (인코더)
   ↓
Bottleneck
   ↓
UpSampling + Convolution (디코더)
   ↓
Output Mask (H, W, 1)
```

------

#### 방법 2: 전이 학습 기반 모델 활용

- **DeepLabV3+**, **SegFormer**, **U^2-Net** 등 사전 학습된 세그멘테이션 모델을 사용하고,
- 자신의 데이터셋으로 **fine-tuning**.

------

### 3. 학습 과정

- 입력: 회색조 이미지 (또는 3채널 이미지로 변환)
- 출력: 라인 마스크
- 손실함수: Binary Cross Entropy 또는 Dice Loss
- 평가: IoU (Intersection over Union), F1 Score

------

### 4. 후처리

- 모델의 출력 마스크에서:
  - 작은 노이즈 제거 (Morphology, 연결성 분석 등)
  - `cv2.findContours()` 또는 `cv2.HoughLinesP()`로 선 검출

------

### 5. 대안 (비지도 / 약지도)

- **Background Subtraction + Clustering (KMeans, GMM)**: 배경 모델링 후 라인만 분리
- **Autoencoder 기반 이상 검출**: 배경만 학습 → 선이 있는 부분은 복원되지 않아 차이로 검출

------

### 결론

| 방법                          | 특징                             | 적합성 |
| ----------------------------- | -------------------------------- | ------ |
| U-Net                         | 구조가 간단하고 성능 좋음        | ★★★★☆  |
| DeepLabV3+                    | 더 강력한 모델이지만 데이터 필요 | ★★★★☆  |
| Autoencoder                   | 비지도 학습, 라벨링 불필요       | ★★☆☆☆  |
| Rule-based (Canny, Threshold) | 라인-배경 구분 명확할 때만       | ★☆☆☆☆  |



------



















**[목록 열기](../README.md)** 
