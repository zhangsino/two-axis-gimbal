# -*- coding: utf-8 -*-
# 八方向行程演示：找完零点后，平板依次往 8 个方向倾 30°（顺时针），最后回水平
# 每个方向：倾斜 0.15 s + 停 0.25 s ≈ 0.4 s，整圈约 4 秒
#
# 这一段是开环（直接算脉宽），不闭环：
#   闭环的每周期限幅是 6 us，30° 要走 0.6 s，跟不上你要求的节奏。
#   演示要的是"看得见的行程"，用实测灵敏度换算过去最直接。
#
# 安全：每个轴都限制在 ±40°，实测机构 ±30° 内无限位

from machine import I2C, Pin, PWM
import time, math, struct
import config

D = lambda v: int(v * 65535 // 20000)
GA = config.US_PER_DEG_A
GB = config.US_PER_DEG_B
DA = config.DIR_A
DB = config.DIR_B

i2c = I2C(0, scl=Pin(config.PIN_SCL), sda=Pin(config.PIN_SDA), freq=config.I2C_FREQ)
A = 0x68
i2c.writeto_mem(A, 0x6B, b'\x00'); time.sleep_ms(100)
i2c.writeto_mem(A, 0x1A, b'\x03')
i2c.writeto_mem(A, 0x1B, b'\x08')
i2c.writeto_mem(A, 0x1C, b'\x08')
time.sleep_ms(100)


def rd():
    d = struct.unpack('>7h', i2c.readfrom_mem(A, 0x3B, 14))
    ax, ay, az = d[0] / 8192.0, d[1] / 8192.0, d[2] / 8192.0
    return (math.degrees(math.atan2(ay, az)),
            math.degrees(math.atan2(-ax, math.sqrt(ay * ay + az * az))))


def avg(n=5):
    sp = sr = 0.0
    for _ in range(n):
        p, r = rd()
        sp += p
        sr += r
        time.sleep_ms(4)
    return sp / n, sr / n


try:
    pa = PWM(Pin(config.PIN_SERVO1), freq=50, duty_u16=D(1500))
    pb = PWM(Pin(config.PIN_SERVO2), freq=50, duty_u16=D(1500))
except TypeError:
    pa = PWM(Pin(config.PIN_SERVO1), freq=50); pa.duty_u16(D(1500))
    pb = PWM(Pin(config.PIN_SERVO2), freq=50); pb.duty_u16(D(1500))


def set_us(a, b):
    pa.duty_u16(D(int(a)))
    pb.duty_u16(D(int(b)))


# ---------- 找零点（简版，和 main.py 同法）----------
time.sleep(0.8)
ua = ub = 1500
for i in range(7):
    p, r = avg()
    if abs(p) < 0.35:
        break
    ua = max(1000, min(2000, ua + DA * (0.0 - p) * GA * 0.8))
    set_us(ua, ub)
    time.sleep_ms(600)
for i in range(7):
    p, r = avg()
    if abs(r) < 0.35:
        break
    ub = max(1000, min(2000, ub + DB * (0.0 - r) * GB * 0.8))
    set_us(ua, ub)
    time.sleep_ms(600)
set_us(ua, ub)
time.sleep_ms(300)
print('零点 A %d  B %d' % (ua, ub))

# ---------- 八方向 ----------
TILT = 30.0
RAMP_S = 0.15
HOLD_S = 0.25
LIM = 40.0


def target_us(pitch_t, roll_t):
    pa_us = ua + DA * pitch_t * GA
    pb_us = ub + DB * roll_t * GB
    lo_a, hi_a = ua - LIM * GA, ua + LIM * GA
    lo_b, hi_b = ub - LIM * GB, ub + LIM * GB
    return max(lo_a, min(hi_a, pa_us)), max(lo_b, min(hi_b, pb_us))


def ramp(ca, cb, ta, tb, sec, steps=12):
    for i in range(1, steps + 1):
        f = i / steps
        set_us(ca + (ta - ca) * f, cb + (tb - cb) * f)
        time.sleep_ms(int(sec * 1000 / steps))
    return ta, tb


ca, cb = ua, ub
print('=== 八方向 30° 顺时针 ===')
for deg in (0, 45, 90, 135, 180, 225, 270, 315):
    th = math.radians(deg)
    pt = TILT * math.cos(th)
    rt = TILT * math.sin(th)
    ta, tb = target_us(pt, rt)
    ca, cb = ramp(ca, cb, ta, tb, RAMP_S)
    time.sleep_ms(int(HOLD_S * 1000))
    pm, rm = avg(4)
    print('  %3d°  目标 p%+5.1f r%+5.1f   实测 p%+6.2f r%+6.2f' % (deg, pt, rt, pm, rm))

print('=== 回水平 ===')
ramp(ca, cb, ua, ub, RAMP_S * 2)
time.sleep_ms(400)
pm, rm = avg(8)
print('  回平后 p%+6.2f r%+6.2f' % (pm, rm))
time.sleep_ms(600)
pa.deinit()
pb.deinit()
print('结束，舵机释放')
