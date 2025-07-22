import time
import math
import sys
from pop import Pilot

# 전역 yaw 오프셋
yaw_offset = 0.0

def normalize_accel(ax, ay, az):
    scale = 16384.0  # 1g = 16384 기준 (±2g)
    return ax / scale, ay / scale, az / scale

def get_accel_angle(ax, ay, az):
    roll = math.atan2(ay, az) * 180 / math.pi
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180 / math.pi
    return roll, pitch

# === Yaw 오프셋 보정 함수 ===
def calibrate_yaw_offset(Car, samples=100, delay=0.01):
    global yaw_offset
    sum_gz = 0.0
    print("Calibrating yaw offset... Please keep the robot still.")
    for i in range(samples):
        gz = Car.getGyro('z')
        sum_gz += gz
        time.sleep(delay)
    yaw_offset = sum_gz / samples
    print("Yaw offset calibrated: %.4f deg/s" % yaw_offset)

def main():
    global yaw_offset
    Car = Pilot.AutoCar()

    dt = 0.01  # 10ms 루프 주기
    alpha = 0.98  # 상보 필터 계수
    roll, pitch = 0.0, 0.0
    yaw = 0.0

    calibrate_yaw_offset(Car)  # 로봇이 정지 상태일 때 반드시 호출

    try:
        for i in range(1000):  # 약 10초간 루프
            gx = Car.getGyro('x')
            gy = Car.getGyro('y')
            gz = Car.getGyro('z')

            ax = Car.getAccel('x')
            ay = Car.getAccel('y')
            az = Car.getAccel('z')

            acc_roll, acc_pitch = get_accel_angle(ax, ay, az)

            roll = alpha * (roll + gx * dt) + (1 - alpha) * acc_roll
            pitch = alpha * (pitch + gy * dt) + (1 - alpha) * acc_pitch
            yaw += (gz - yaw_offset) * dt  # 오프셋 보정된 yaw 계산

            print("Roll = %.2f, Pitch = %.2f, Yaw = %.2f" % (roll, pitch, yaw))
            time.sleep(dt)

            # 조건: 자이로가 거의 0일 때 정지로 간주 → 재보정
            if abs(gx) < 0.05 and abs(gy) < 0.05 and abs(gz) < 0.05:
                print("Robot is still, recalibrating yaw offset...")
                calibrate_yaw_offset(Car)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        print("Cleaning up pins")

if __name__ == '__main__':
    main()

