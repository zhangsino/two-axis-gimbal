# -*- coding: utf-8 -*-
# 云台配置（2026-11-18 重写版）
# 改这里就够了

# ---------------- 引脚
PIN_SERVO_A = 6      # 平板中心，改 pitch
PIN_SERVO_B = 7      # 摇臂，改 roll
PIN_SDA = 8
PIN_SCL = 9
I2C_FREQ = 400000
MPU_ADDR = 0x68

# ---------------- 舵机
CENTER_US = 1500
PWM_MIN_US = 500
PWM_MAX_US = 2500

# ---------------- 实测灵敏度（us / 度）
US_PER_DEG_A = 11.27   # 8.875 度/100us
US_PER_DEG_B = 12.45   # 8.033 度/100us

# ---------------- 方向（实测定）
# A：脉宽增大 -> pitch 增大
# B：脉宽增大 -> roll 减小
DIR_A = 1
DIR_B = -1

# ---------------- 陀螺轴向（2026-11-18 实测）
# 转 A 时 gx 响应 +78.7 °/s -> pitch 角速度 = gx
# 转 B 时 gy 响应 -52.5 °/s -> roll  角速度 = gy
GYRO_IDX_A = 0       # 0=x 1=y 2=z
GYRO_IDX_B = 1
GYRO_SIGN_A = 1
GYRO_SIGN_B = 1

# ---------------- 控制
LOOP_MS = 10         # 100 Hz
KP = 0.15            # 每周期补正 15% 的误差
KD = 0.15            # 阻尼系数（秒），陀螺干净了才敢给这么大
SLEW_US = 8          # 每周期最多改 8 us（约 0.7°/步）
STALL_US = 250       # 推了这么多 us 角度还不动，判定堵转
ALPHA = 0.98         # 互补滤波：越大越信陀螺

# ---------------- 找零点
SEARCH_GAIN = 0.8
SEARCH_ITERS = 8
SEARCH_SPAN_DEG = 60.0
SEARCH_SETTLE_MS = 700

# ---------------- 演示
DEMO_ON = True
DEMO_TILT_DEG = 25.0
DEMO_TURN_S = 3.6
DEMO_STEP_MS = 20

# ---------------- 遥测
TELEM_HZ = 10
