import cv2
import numpy as np
import math

def get_line_angle(line):
    x1, y1, x2, y2 = line[0]
    # 각도 계산 (세로선이 기준이므로 90도에서 뺌)
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)
    vertical_angle = 90 - angle_deg
    # 좌측 기울어짐: +, 우측 기울어짐: -
    return vertical_angle

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

        # 회색조로 변환 및 블러
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # 임계값으로 이진화 (어두운 선 검출용)
        _, binary = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        # 캐니 엣지 & 직선 검출
        edges = cv2.Canny(binary, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                                minLineLength=50, maxLineGap=10)

        angle_to_display = None

        if lines is not None:
            # 가장 긴 선 하나 선택
            longest_line = max(lines, key=lambda l: np.hypot(l[0][2] - l[0][0], l[0][3] - l[0][1]))
            angle = get_line_angle(longest_line)

            # 수직 기준으로 -90~+90 범위 제한
            if angle > 90:
                angle -= 180
            elif angle < -90:
                angle += 180

            # 기준이 수직일 때 0, 왼쪽으로 기울면 +, 오른쪽 기울면 -
            deviation = -angle
            angle_to_display = deviation

            # 직선 표시
            x1, y1, x2, y2 = longest_line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # 텍스트 표시 (흰색, Slope)
            cv2.putText(frame, f"Slope: {deviation:.1f} deg", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Line Detection", frame)
        cv2.imshow("Binary", binary)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키 종료
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

