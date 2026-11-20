# -*- coding: utf-8 -*-
# 两只舵机停在 1500（舵机自己的 0 位），并持续打印 IMU，方便看当前姿态
from machine import I2C, Pin, PWM
import time, math, struct

D = lambda v: int(v * 65535 // 20000)
pa = PWM(Pin(6), freq=50)
pa.duty_u16(D(1500))
pb = PWM(Pin(7), freq=50)
pb.duty_u16(D(1500))

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
ADDR = 0x68
i2c.writeto_mem(ADDR, 0x6B, b'\x00')
time.sleep_ms(100)
i2c.writeto_mem(ADDR, 0x1A, b'\x03')
i2c.writeto_mem(ADDR, 0x1B, b'\x08')
i2c.writeto_mem(ADDR, 0x1C, b'\x08')
time.sleep_ms(100)

print('两只已停 1500')
time.sleep(1.0)
n = 0
while True:
    try:
        d = struct.unpack('>7h', i2c.readfrom_mem(ADDR, 0x3B, 14))
        ax, ay, az = d[0] / 8192.0, d[1] / 8192.0, d[2] / 8192.0
        p = math.degrees(math.atan2(ay, az))
        r = math.degrees(math.atan2(-ax, math.sqrt(ay * ay + az * az)))
        print('1500/1500  pitch %+6.2f  roll %+6.2f' % (p, r))
    except Exception as e:
        print('读 IMU 失败', e)
    n += 1
    if n >= 1000:
        break
    time.sleep(1.0)
