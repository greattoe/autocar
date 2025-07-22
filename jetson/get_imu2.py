import time
import math
import sys
from pop import Pilot

def normalize_accel(ax, ay, az):
    scale = 16384.0  # 1g = 16384 기준 (±2g)
    return ax / scale, ay / scale, az / scale

def get_accel_angle(ax, ay, az):
    roll = math.atan2(ay, az) * 180 / math.pi
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180 / math.pi
    return roll, pitch

def main():
    Car = Pilot.AutoCar()

    dt = 0.01  # 10ms 루프 주기
    alpha = 0.98  # 상보 필터 계수
    roll, pitch = 0.0, 0.0
    yaw = 0.0

    try:
        for i in range(100):  # 100회 반복 (약 1초)
            gx = Car.getGyro('x')  # °/s
            gy = Car.getGyro('y')
            gz = Car.getGyro('z')

            ax = Car.getAccel('x')
            ay = Car.getAccel('y')
            az = Car.getAccel('z')

            acc_roll, acc_pitch = get_accel_angle(ax, ay, az)

            roll = alpha * (roll + gx * dt) + (1 - alpha) * acc_roll
            pitch = alpha * (pitch + gy * dt) + (1 - alpha) * acc_pitch
            yaw = yaw + gz * dt  # yaw는 자이로만 사용

            print("Roll = %.2f, Pitch = %.2f, Yaw = %.2f" % (roll, pitch, yaw))
            time.sleep(dt)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        print("Cleaning up pins")

if __name__ == '__main__':
    main()

