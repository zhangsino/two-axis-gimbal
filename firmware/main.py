# -*- coding: utf-8 -*-
"""两轴自调平（2026-11-18 重写版）

流程：校准陀螺零偏 → 找零点 → 圆锥演示 → 100 Hz 闭环

姿态解算用互补滤波：
    角度 = 0.98 × (上一角度 + 陀螺角速度×dt) + 0.02 × 加速度倾角
    陀螺负责快、加速度计负责不漂。

陀螺轴向（实测）：pitch 用 gx，roll 用 gy。

退出：Ctrl+C。退出时 PWM 释放，舵机失去保持，平板会掉。
"""

import time
import math
import struct
from machine import I2C, Pin, PWM

import config
import ctrl


def D(v):
    return int(v * 65535 // 20000)


def clamp(v, lo, hi):
    return lo if v < lo else (hi if v > hi else v)


def mk(pin, us):
    """建 PWM 后立刻给占空比。

    不要用 PWM(pin, freq=50, duty_u16=...) 这种带关键字的写法：
    2026-11-18 在固件 v1.19.1 上实测，一路用关键字、一路用普通构造，
    两路都会失效（舵机完全不动）。统一用普通构造就正常。
    代价是创建瞬间有几微秒的 0 us，紧跟着赋值，影响可以忽略。
    """
    p = PWM(Pin(pin), freq=50)
    p.duty_u16(D(us))
    return p


# ---------------- IMU ----------------
i2c = I2C(0, scl=Pin(config.PIN_SCL), sda=Pin(config.PIN_SDA), freq=config.I2C_FREQ)
found = i2c.scan()
ADDR = config.MPU_ADDR if config.MPU_ADDR in found else (0x69 if 0x69 in found else None)
if ADDR is None:
    print('!! 没扫到 6050，查 SDA/SCL 和供电')
    raise SystemExit

i2c.writeto_mem(ADDR, 0x6B, b'\x00')
time.sleep_ms(100)
i2c.writeto_mem(ADDR, 0x1A, b'\x03')      # DLPF 44Hz
i2c.writeto_mem(ADDR, 0x1B, b'\x08')      # ±500 dps
i2c.writeto_mem(ADDR, 0x1C, b'\x08')      # ±4g
time.sleep_ms(100)
print('6050 0x%02X  WHO_AM_I=0x%02X' % (ADDR, i2c.readfrom_mem(ADDR, 0x75, 1)[0]))


def read14():
    for _ in range(3):
        try:
            return struct.unpack('>7h', i2c.readfrom_mem(ADDR, 0x3B, 14))
        except Exception:
            time.sleep_ms(2)
    return None


def sample():
    """返回 (pitch_acc, roll_acc, gx, gy, gz)，单位度 / 度每秒；失败返回 None"""
    d = read14()
    if d is None:
        return None
    ax, ay, az = d[0] / 8192.0, d[1] / 8192.0, d[2] / 8192.0
    n = math.sqrt(ay * ay + az * az)
    pitch = math.degrees(math.atan2(ay, az))
    roll = math.degrees(math.atan2(-ax, n if n > 1e-6 else 1e-6))
    return pitch, roll, d[4] / 65.5, d[5] / 65.5, d[6] / 65.5


def avg_angle(n=8):
    sp = sr = 0.0
    k = 0
    for _ in range(n):
        s = sample()
        if s is None:
            continue
        sp += s[0]
        sr += s[1]
        k += 1
        time.sleep_ms(5)
    if k == 0:
        return None, None
    return sp / k, sr / k


# ---------------- 陀螺零偏 ----------------
print('=== 陀螺零偏校正（保持不动 1 秒）===')
time.sleep(1.0)
gx0 = gy0 = 0.0
k = 0
for _ in range(100):
    s = sample()
    if s is None:
        continue
    gx0 += s[2]
    gy0 += s[3]
    k += 1
    time.sleep_ms(10)
gx0 /= max(k, 1)
gy0 /= max(k, 1)
print('  零偏 gx %+.2f  gy %+.2f °/s' % (gx0, gy0))

# ---------------- 舵机 ----------------
pa = mk(config.PIN_SERVO_A, config.CENTER_US)
pb = mk(config.PIN_SERVO_B, config.CENTER_US)
time.sleep_ms(300)

# ---------------- 找零点 ----------------
print('=== 找零点（A 找 pitch=0，B 找 roll=0）===')
ua = ub = config.CENTER_US
span_a = int(config.SEARCH_SPAN_DEG * config.US_PER_DEG_A)
span_b = int(config.SEARCH_SPAN_DEG * config.US_PER_DEG_B)

for axis in ('A', 'B'):
    for i in range(config.SEARCH_ITERS):
        p, r = avg_angle(5)
        if p is None:
            print('  IMU 读失败，跳过')
            break
        ang = p if axis == 'A' else r
        err = 0.0 - ang
        print('  %s 第%d次  %s=%+6.2f  误差 %+6.2f  脉宽 %d' % (axis, i + 1, axis, ang, err, ua if axis == 'A' else ub))
        if abs(err) < 0.35:
            print('  %s 到位' % axis)
            break
        if axis == 'A':
            ua = clamp(ua + config.DIR_A * err * config.US_PER_DEG_A * config.SEARCH_GAIN,
                       config.CENTER_US - span_a, config.CENTER_US + span_a)
            pa.duty_u16(D(ua))
        else:
            ub = clamp(ub + config.DIR_B * err * config.US_PER_DEG_B * config.SEARCH_GAIN,
                       config.CENTER_US - span_b, config.CENTER_US + span_b)
            pb.duty_u16(D(ub))
        time.sleep_ms(config.SEARCH_SETTLE_MS)

print('  零点：A %d  B %d' % (ua, ub))
pa.duty_u16(D(ua))
pb.duty_u16(D(ub))
time.sleep_ms(300)

# ---------------- 演示 ----------------
if config.DEMO_ON:
    N = max(16, int(config.DEMO_TURN_S * 1000 / config.DEMO_STEP_MS))
    print('=== 圆锥演示：%.0f°，%.1f s 一圈 ===' % (config.DEMO_TILT_DEG, config.DEMO_TURN_S))
    for i in range(N + 1):
        f = i / N
        th = 2 * math.pi * f
        if f < 0.15:
            amp = config.DEMO_TILT_DEG * f / 0.15
        elif f > 0.85:
            amp = config.DEMO_TILT_DEG * (1 - f) / 0.15
        else:
            amp = config.DEMO_TILT_DEG
        pt = amp * math.cos(th)
        rt = amp * math.sin(th)
        pa.duty_u16(D(clamp(int(ua + config.DIR_A * pt * config.US_PER_DEG_A),
                            config.PWM_MIN_US, config.PWM_MAX_US)))
        pb.duty_u16(D(clamp(int(ub + config.DIR_B * rt * config.US_PER_DEG_B),
                            config.PWM_MIN_US, config.PWM_MAX_US)))
        time.sleep_ms(config.DEMO_STEP_MS)
    pa.duty_u16(D(ua))
    pb.duty_u16(D(ub))
    time.sleep_ms(300)
    print('=== 演示结束，进入自稳 ===')

# ---------------- 闭环 ----------------
axis_a = ctrl.Axis('A', config.US_PER_DEG_A, config.DIR_A, ua,
                   config.PWM_MIN_US, config.PWM_MAX_US,
                   kp=config.KP, kd=config.KD, slew=config.SLEW_US, stall_us=config.STALL_US)
axis_b = ctrl.Axis('B', config.US_PER_DEG_B, config.DIR_B, ub,
                   config.PWM_MIN_US, config.PWM_MAX_US,
                   kp=config.KP, kd=config.KD, slew=config.SLEW_US, stall_us=config.STALL_US)
axis_a.setpoint = 0.0
axis_b.setpoint = 0.0

dt = config.LOOP_MS / 1000.0
telem_ms = int(1000 / config.TELEM_HZ) if config.TELEM_HZ else 0
pitch_f = roll_f = None
t_tel = time.ticks_ms()
n = 0
bad = 0

print('=== 闭环开始（Ctrl+C 退出）===')
try:
    while True:
        t0 = time.ticks_ms()
        s = sample()
        if s is None:
            bad += 1
            if bad > 20:
                print('!! IMU 一直读失败')
                break
            time.sleep_ms(config.LOOP_MS)
            continue
        bad = 0
        p_acc, r_acc, gx, gy, gz = s
        gx -= gx0
        gy -= gy0

        if pitch_f is None:
            pitch_f, roll_f = p_acc, r_acc
        else:
            a = config.ALPHA
            pitch_f = a * (pitch_f + gx * dt) + (1 - a) * p_acc
            roll_f = a * (roll_f + gy * dt) + (1 - a) * r_acc

        ua = axis_a.update(pitch_f, gx)
        ub = axis_b.update(roll_f, gy)
        pa.duty_u16(D(ua))
        pb.duty_u16(D(ub))
        n += 1

        if telem_ms:
            t = time.ticks_ms()
            if time.ticks_diff(t, t_tel) >= telem_ms:
                t_tel = t
                print('pitch %+6.2f  roll %+6.2f | A %4d (%+6.2f)  B %4d (%+6.2f) | n=%d'
                      % (pitch_f, roll_f, ua, axis_a.last_err, ub, axis_b.last_err, n))

        used = time.ticks_diff(time.ticks_ms(), t0)
        if used < config.LOOP_MS:
            time.sleep_ms(config.LOOP_MS - used)
except KeyboardInterrupt:
    print('\n=== 手动停止 ===')
finally:
    try:
        pa.deinit()
        pb.deinit()
    except Exception:
        pass
    print('PWM 已释放')
