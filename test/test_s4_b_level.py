# -*- coding: utf-8 -*-
# 第 4 步：把舵机 B 走到"平板 roll = 0"的位置并保持
# A 全程停在 1500 不动（pitch 那一点偏先不管）
#
# 用实测灵敏度 12.77 us/° 做粗定位，再靠 6050 读数迭代收
# 软限位 1150~1790（防走到 1800 顶死）
#
# 跑完会一直保持在那，断电或 Ctrl+C 才松

from machine import I2C, Pin, PWM
import time, math, struct

SDA, SCL = 8, 9
PIN_A, PIN_B = 6, 7
CENTER = 1500
GAIN = 12.77           # us/°，B 轴实测
VLO, VHI = 1150, 1790
TOL = 0.4              # |roll| < 0.4° 就停

D = lambda v: int(v * 65535 // 20000)


def mk(pin):
    try:
        return PWM(Pin(pin), freq=50, duty_u16=D(CENTER))
    except TypeError:
        p = PWM(Pin(pin), freq=50)
        p.duty_u16(D(CENTER))
        return p


i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
addr = 0x68
if addr not in i2c.scan():
    print('!! 没有 6050，退出，不动舵机')
    raise SystemExit
i2c.writeto_mem(addr, 0x6B, b'\x00')
time.sleep_ms(100)
i2c.writeto_mem(addr, 0x1A, b'\x03')
i2c.writeto_mem(addr, 0x1B, b'\x08')
i2c.writeto_mem(addr, 0x1C, b'\x08')
time.sleep_ms(100)


def angles(n=6):
    sp = sr = 0.0
    k = 0
    for _ in range(n):
        d = None
        for _ in range(3):
            try:
                d = struct.unpack('>7h', i2c.readfrom_mem(addr, 0x3B, 14))
                break
            except Exception:
                time.sleep_ms(2)
        if d is None:
            continue
        ax, ay, az = d[0], d[1], d[2]
        axg, ayg, azg = ax / 8192.0, ay / 8192.0, az / 8192.0
        sp += math.degrees(math.atan2(ayg, azg))
        sr += math.degrees(math.atan2(-axg, math.sqrt(ayg * ayg + azg * azg)))
        k += 1
        time.sleep_ms(5)
    if k == 0:
        return None, None
    return sp / k, sr / k


pa = mk(PIN_A)
pb = mk(PIN_B)
pa.duty_u16(D(CENTER))
time.sleep_ms(400)

v = CENTER
print('=== 开始：A 固定 1500，B 迭代找 roll=0 ===')
for i in range(10):
    pb.duty_u16(D(v))
    time.sleep_ms(450)
    pitch, roll = angles()
    if pitch is None:
        print('  第 %d 步 IMU 全读失败，跳过' % (i + 1))
        continue
    print('  第 %d 步  B=%4d us   pitch %+7.2f  roll %+7.2f' % (i + 1, v, pitch, roll))
    if abs(roll) < TOL:
        break
    step = int(round(roll * GAIN * 0.85))
    step = max(-100, min(100, step))
    nv = v + step
    if nv > VHI:
        nv = VHI
    if nv < VLO:
        nv = VLO
    if nv == v:
        print('  !! 已经顶到软限位 %d us，roll 还是 %+.2f 度' % (v, roll))
        break
    v = nv

pitch, roll = angles(12)
print('=== 定位完成：B = %d us（%+.2f 度），pitch %+.2f roll %+.2f ===' % (v, (v - 1500) / GAIN, pitch or 0, roll or 0))
print('=== 保持中，别断电 ===')

n = 0
while True:
    time.sleep(15)
    n += 15
    print('  保持中 %3d s  （B 未动）' % n)
