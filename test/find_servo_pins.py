# -*- coding: utf-8 -*-
# 自动找舵机信号脚：逐个脚输出 1500 -> 1600，同时读 IMU 看平板有没有被推动
# 有反应就说明那个脚接着舵机
# 跳过 8/9（I2C）、19/20（USB）、26-37（PSRAM）、0/3/45/46（strapping）、48（板载灯）

from machine import I2C, Pin, PWM
import time, math, struct

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
ADDR = 0x68
i2c.writeto_mem(ADDR, 0x6B, b'\x00')
time.sleep_ms(100)
i2c.writeto_mem(ADDR, 0x1A, b'\x03')
i2c.writeto_mem(ADDR, 0x1B, b'\x08')
i2c.writeto_mem(ADDR, 0x1C, b'\x08')
time.sleep_ms(100)

D = lambda v: int(v * 65535 // 20000)


def ang(n=6):
    sp = sr = 0.0
    k = 0
    for _ in range(n):
        d = struct.unpack('>7h', i2c.readfrom_mem(ADDR, 0x3B, 14))
        ax, ay, az = d[0] / 8192.0, d[1] / 8192.0, d[2] / 8192.0
        sp += math.degrees(math.atan2(ay, az))
        sr += math.degrees(math.atan2(-ax, math.sqrt(ay * ay + az * az)))
        k += 1
        time.sleep_ms(10)
    return sp / k, sr / k


p0, r0 = ang(10)
print('起始 pitch %+.2f roll %+.2f' % (p0, r0))

cands = [6, 7, 1, 2, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21,
         38, 39, 40, 41, 42, 47]

for n in cands:
    try:
        p = PWM(Pin(n), freq=50)
        p.duty_u16(D(1500))
        time.sleep(1.2)
        p1, r1 = ang()
        p.duty_u16(D(1600))
        time.sleep(1.2)
        p2, r2 = ang()
        p.deinit()
    except Exception as e:
        print('GPIO%-2d 出错 %s' % (n, e))
        continue
    dp = p2 - p1
    dr = r2 - r1
    mark = '   <<<<< 有反应' if max(abs(dp), abs(dr)) > 3 else ''
    print('GPIO%-2d  dpitch %+6.2f  droll %+6.2f%s' % (n, dp, dr, mark))

print('扫完')
