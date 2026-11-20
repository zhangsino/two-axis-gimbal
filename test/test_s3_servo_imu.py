# -*- coding: utf-8 -*-
# 第 3 步：舵机 + 6050 联动标定
# 目的：一只一只动，看 6050 的 pitch/roll 跟着变多少 —— 判这一轴有没有用、传动是不是 1:1
# 前提：6050 在 8/9 上能扫到 0x68 或 0x69；两只舵机已接好、5V 独立、共地
#
# 现象预告：
#   - 开始 3 s 两只回中，平板应静住
#   - A 从 1300 走到 1700，每步停 0.3 s，共 9 步；串口每步打一行角度
#   - A 回中，静 1 s，换 B 走同样的 9 步
#   - 结尾打印两轴的 "度/100us"，以及这一轴到底改了 pitch 还是 roll
# 判据：
#   - 某一轴走完 400 us（本该 36°），pitch 或 roll 基本不变 -> 这一轴是偏航，无效
#   - 变化量明显不是 36° -> 记下实际值，别套 1:1

from machine import I2C, Pin, PWM
import time, math, struct

SDA, SCL = 8, 9
PIN_A, PIN_B = 6, 7
ADDR_TRY = (0x68, 0x69)

CENTER = 1500
LO, HI, STEP_US = 1300, 1700, 50
SETTLE_MS = 300
SAMPLES = 8

D = lambda v: int(v * 65535 // 20000)


def mk(pin):
    try:
        return PWM(Pin(pin), freq=50, duty_u16=D(CENTER))
    except TypeError:
        p = PWM(Pin(pin), freq=50)
        p.duty_u16(D(CENTER))
        return p


# ---------- IMU ----------
i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
found = i2c.scan()
print('I2C scan:', [hex(a) for a in found])
addr = None
for a in ADDR_TRY:
    if a in found:
        addr = a
        break
if addr is None:
    print('!! 没扫到 6050（0x68/0x69）。先查供电和 SDA/SCL，本程序退出，不动舵机。')
    raise SystemExit

print('addr = 0x%02X  WHO_AM_I = 0x%02X' % (addr, i2c.readfrom_mem(addr, 0x75, 1)[0]))
i2c.writeto_mem(addr, 0x6B, b'\x00')
time.sleep_ms(100)
i2c.writeto_mem(addr, 0x1A, b'\x03')
i2c.writeto_mem(addr, 0x1B, b'\x08')   # ±500 dps
i2c.writeto_mem(addr, 0x1C, b'\x08')   # ±4g
time.sleep_ms(100)


def read14():
    """I2C 偶发 ENODEV，重试 3 次"""
    for _ in range(3):
        try:
            return struct.unpack('>7h', i2c.readfrom_mem(addr, 0x3B, 14))
        except Exception:
            time.sleep_ms(2)
    return None


def angles(n=SAMPLES):
    sp = sr = 0.0
    k = 0
    for _ in range(n):
        d = read14()
        if d is None:
            continue
        ax, ay, az, _t, gx, gy, gz = d
        axg, ayg, azg = ax / 8192.0, ay / 8192.0, az / 8192.0
        sp += math.degrees(math.atan2(ayg, azg))
        sr += math.degrees(math.atan2(-axg, math.sqrt(ayg * ayg + azg * azg)))
        k += 1
        time.sleep_ms(3)
    if k == 0:
        print('  !! 这一步 IMU 全读失败')
        return None, None
    return sp / k, sr / k


# ---------- 舵机 ----------
pa = mk(PIN_A)
pb = mk(PIN_B)
pwm = {'A': pa, 'B': pb}


def sweep(tag, p, lo, hi):
    print('--- %s ---' % ('舵机 %s' % tag))
    rows = []
    v = lo
    while v <= hi:
        p.duty_u16(D(v))
        time.sleep_ms(SETTLE_MS)
        pitch, roll = angles()
        rows.append((v, pitch, roll))
        if pitch is None:
            print('  %s %4d us  <IMU 读失败>' % (tag, v))
        else:
            print('  %s %4d us  pitch %+7.2f  roll %+7.2f' % (tag, v, pitch, roll))
        v += STEP_US
    p.duty_u16(D(CENTER))
    time.sleep_ms(SETTLE_MS)

    rows = [r for r in rows if r[1] is not None]
    if len(rows) < 2:
        print('  !! %s 数据不足' % tag)
        return rows
    # 用首尾差算这一轴的效率
    dp = rows[-1][1] - rows[0][1]
    dr = rows[-1][2] - rows[0][2]
    span = rows[-1][0] - rows[0][0]
    if abs(dp) >= abs(dr):
        print('  => %s 主要改 pitch：%.2f 度 / %d us = %.3f 度/100us（1:1 应 9.0）' % (tag, dp, span, dp * 100.0 / span))
        print('     roll 顺带变了 %.2f 度' % dr)
    else:
        print('  => %s 主要改 roll：%.2f 度 / %d us = %.3f 度/100us（1:1 应 9.0）' % (tag, dr, span, dr * 100.0 / span))
        print('     pitch 顺带变了 %.2f 度' % dp)
    if abs(dp) < 3 and abs(dr) < 3:
        print('  !! 倾角几乎没变：这一轴只带出偏航，在这一台上无效')
    return rows


print('=== 0. 两只回中，静 3 s（此时记下初始 pitch/roll 作为零点）===')
time.sleep(3)
p0, r0 = angles(20)
print('  零点 pitch %+.2f  roll %+.2f' % (p0, r0))

sweep('A', pa, 1300, 1700)
time.sleep(1)
sweep('B', pb, 1350, 1650)

print('=== 结束，两只 1500 ===')
