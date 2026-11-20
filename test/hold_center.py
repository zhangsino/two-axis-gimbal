# -*- coding: utf-8 -*-
# 临时：两只舵机守在 1500，给接舵机电源用
# 目的：接 5V 的瞬间信号已经是正确的 1500，舵机不会甩
from machine import Pin, PWM
import time

D = lambda v: int(v * 65535 // 20000)
try:
    pa = PWM(Pin(6), freq=50, duty_u16=D(1500))
    pb = PWM(Pin(7), freq=50, duty_u16=D(1500))
except TypeError:
    pa = PWM(Pin(6), freq=50); pa.duty_u16(D(1500))
    pb = PWM(Pin(7), freq=50); pb.duty_u16(D(1500))

print('HOLD: 两只都在 1500，现在可以接舵机 5V 了')
n = 0
while True:
    time.sleep(5)
    n += 5
    print('  holding %d s' % n)
