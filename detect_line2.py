import cv2
import numpy as np
import math

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

def main():
    cap = cv2.VideoCapture(4)

    if not cap.isOpened():
        print("Failed to open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.")
            break

        roi, roi_x1, roi_y1, roi_x2, roi_y2 = extract_roi(frame)

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        edges = cv2.Canny(binary, 50, 150)
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
                # ROI 좌표 기준 → 원본 좌표로 보정
                x1, y1, x2, y2 = longest[0]
                cv2.line(frame,
                         (x1 + roi_x1, y1 + roi_y1),
                         (x2 + roi_x1, y2 + roi_y1),
                         (0, 255, 0), 3)

                cv2.putText(frame, f"Slope: {deviation:.1f} deg", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # ROI 박스 표시 (하늘색)
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 255, 0), 2)

        cv2.imshow("Line Detection", frame)
        # cv2.imshow("Binary", binary)  # 조명보정 결과 확인 시 사용

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

