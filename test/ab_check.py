# -*- coding: utf-8 -*-
# A/B 单独动作确认：一次只动一只，每次 100 us（约 8-9 度）
#
# 时序：
#   0 s      两只回 1500（会"嗒"一声锁住）
#   3 s      A 从 1500 走到 1600，停 3 s
#   6 s      A 回 1500，停 2 s
#   8 s      B 从 1500 走到 1600，停 3 s
#   11 s     B 回 1500，停 2 s
#   13 s     两只挂 1500 保持 15 s（可以上手摸是否锁住）
#   28 s     结束（结束后舵机会松）

from machine import Pin, PWM
import time

D = lambda v: int(v * 65535 // 20000)

pa = PWM(Pin(6), freq=50)
pa.duty_u16(D(1500))
pb = PWM(Pin(7), freq=50)
pb.duty_u16(D(1500))

print('0s  两只回 1500 —— 应该"嗒"一声锁住')
time.sleep(3)

print('3s  动 A：1500 -> 1600（约 +8 度）')
pa.duty_u16(D(1600))
time.sleep(3)
print('6s  A 回 1500')
pa.duty_u16(D(1500))
time.sleep(2)

print('8s  动 B：1500 -> 1600（约 +8 度）')
pb.duty_u16(D(1600))
time.sleep(3)
print('11s B 回 1500')
pb.duty_u16(D(1500))
time.sleep(2)

print('13s 两只挂 1500，保持 15 s —— 现在用手轻推，应该推不动/有回弹')
time.sleep(15)

print('结束。PWM 释放，舵机会变松')
