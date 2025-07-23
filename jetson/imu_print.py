import time
import math

# 실제 라이브러리를 임포트합니다.
from pop import Pilot

# --- 1. 상수 정의 ---
GYRO_SCALE_FACTOR = 131.0
# [수정!] 가속도계의 신뢰도를 낮추어 정지 상태의 안정성을 높입니다.
COMPLEMENTARY_FILTER_ALPHA = 0.99998

# --- 2. 하드웨어 객체 생성 ---
try:
    Car = Pilot.AutoCar()
    print("✔ AutoCar 객체 생성 성공!")
except Exception as e:
    print(f"✘ 오류: AutoCar 객체 생성 실패. ({e})")
    exit()

# --- 3. IMU 보정 함수 (시간 기반으로 수정된 올바른 버전) ---
def calibrate_imu():
    """[수정!] IMU의 바이어스를 '정확히 2초 동안' 측정하여 반환"""
    print("\nIMU 보정을 시작합니다. 2초간 차량을 완벽히 정지시켜주세요...")
    gyro_z_readings = []
    accel_x_readings = []
    accel_y_readings = []
    
    start_time = time.time()
    while time.time() - start_time < 2.0: # 2초가 지날 때까지 루프 실행
        gyro_z_readings.append(Car.getGyro('z'))
        accel_x_readings.append(Car.getAccel('x'))
        accel_y_readings.append(Car.getAccel('y'))
        time.sleep(0.01) # 짧은 간격으로 최대한 많이 측정

    # 혹시 2초간 측정이 안됐을 경우를 대비한 안전장치
    if not gyro_z_readings:
        print("✘ 오류: 2초간 IMU 데이터를 읽지 못했습니다.")
        return None

    biases = {
        'gyro_z': sum(gyro_z_readings) / len(gyro_z_readings),
        'accel_x': sum(accel_x_readings) / len(accel_x_readings),
        'accel_y': sum(accel_y_readings) / len(accel_y_readings)
    }
    print("✔ IMU 보정 완료!")
    return biases

# --- 4. 메인 실행 루프 ---
try:
    imu_biases = calibrate_imu()
    if imu_biases is None:
        raise SystemExit("프로그램을 종료합니다.")

    print("\n========================================")
    print("==      IMU 실시간 각도 모니터      ==")
    print("==    (Ctrl+C를 눌러 종료합니다)    ==")
    print("========================================")
    print("\n차량을 손으로 좌우로 돌려보며 각도 변화를 확인하세요.")

    current_angle = 0.0
    last_time = time.time()

    while True:
        current_time = time.time()
        dt = current_time - last_time
        if dt <= 0:
            last_time = current_time
            continue
        last_time = current_time

        raw_gyro_z = Car.getGyro('z') - imu_biases['gyro_z']
        raw_accel_x = Car.getAccel('x') - imu_biases['accel_x']
        raw_accel_y = Car.getAccel('y') - imu_biases['accel_y']

        gyro_angle_change = (raw_gyro_z / GYRO_SCALE_FACTOR) * dt
        accel_angle = math.degrees(math.atan2(raw_accel_y, -raw_accel_x))

        current_angle = COMPLEMENTARY_FILTER_ALPHA * (current_angle + gyro_angle_change) \
                      + (1.0 - COMPLEMENTARY_FILTER_ALPHA) * accel_angle
        
        print(f"\r계산된 현재 각도: {current_angle:>7.2f}°", end="")
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\n\n프로그램을 종료합니다.")
except Exception as e:
    print(f"\n오류 발생: {e}")
