# -*- coding: utf-8 -*-
# 敲击测试：两只舵机轮流在 1500<->1600 之间摆，看舵角本体动不动
# 注意：看舵机本体（输出轴上的舵角），不要看平板
from machine import Pin, PWM
import time

D = lambda v: int(v * 65535 // 20000)
pa = PWM(Pin(6), freq=50)
pa.duty_u16(D(1500))
pb = PWM(Pin(7), freq=50)
pb.duty_u16(D(1500))
time.sleep(0.5)

for rnd in range(4):
    print('===== 第 %d 轮：现在动 A（GPIO6）=====' % (rnd + 1))
    for v in (1600, 1500):
        pa.duty_u16(D(v))
        time.sleep(1.5)
    print('===== 第 %d 轮：现在动 B（GPIO7）=====' % (rnd + 1))
    for v in (1600, 1500):
        pb.duty_u16(D(v))
        time.sleep(1.5)

pa.duty_u16(D(1500))
pb.duty_u16(D(1500))
print('===== 结束，两只 1500 =====')
