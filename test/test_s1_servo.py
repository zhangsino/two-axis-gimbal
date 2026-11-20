# -*- coding: utf-8 -*-
# 第 1 步：单只舵机动作测试（两轴台架版，v2）
# v2 改动：PWM 对象创建时就直接给中位 duty，不再出现"0 us"那一瞬
#
# 用法：Thonny 打开 → 运行；或在 REPL 里 exec 本文件
#
# 安全前提：
#   1. 舵机 5V 用独立电源，GND 与 ESP32 共地
#   2. 手放在电源开关上
#   3. 脉宽只在 1300~1700（±18°）内动，别上 1000/2000
#
# 第 1 步测 A：TARGET = 'A'
# 第 2 步测 B：把这个字母改成 'B'，别的都不动

from machine import Pin, PWM
import time

PIN_A = 6          # 平板侧舵机
PIN_B = 7          # 摇臂侧舵机
TARGET = 'A'

CENTER = 1500      # 中位
STEP = 200         # ±200 us ≈ ±18°（11.11 us/度）
SLOW_MS = 30       # 慢扫步进间隔

D_CENTER = int(CENTER * 65535 // 20000)   # 4915


def mk(pin):
    """建 PWM 时就把占空比设成中位，避免创建瞬间输出 0 us"""
    try:
        return PWM(Pin(pin), freq=50, duty_u16=D_CENTER)
    except TypeError:
        p = PWM(Pin(pin), freq=50)
        p.duty_u16(D_CENTER)
        return p


def us(p, v):
    p.duty_u16(int(v * 65535 // 20000))


print('=== 0. 两只都从中位开始 ===')
pa = mk(PIN_A)
pb = mk(PIN_B)
print('    A duty=%d  B duty=%d   （都应约 4915）' % (pa.duty_u16(), pb.duty_u16()))
print('    接下来 2 s 两只都不该动，盯住 B：')
print('    - 纹丝不动 / 只有轻微吱吱声  -> 正常')
print('    - 猛地摆一下再停 -> 记下它摆到哪边、之后是否停住')
time.sleep(2)

p = pa if TARGET == 'A' else pb

print('=== 1. %s 走 -%d us（%d），停 2 s ===' % (TARGET, STEP, CENTER - STEP))
us(p, CENTER - STEP)
time.sleep(2)
print('    看：往哪边转？大约多少度？另一只是否保持不动？')
us(p, CENTER)
time.sleep(1)

print('=== 2. %s 走 +%d us（%d），停 2 s ===' % (TARGET, STEP, CENTER + STEP))
us(p, CENTER + STEP)
time.sleep(2)
print('    看：是否反方向、角度是否差不多')
us(p, CENTER)
time.sleep(1)

print('=== 3. 慢扫 %d -> %d -> %d，听声音 ===' % (CENTER - STEP, CENTER + STEP, CENTER))
v = CENTER - STEP
while v <= CENTER + STEP:
    us(p, v)
    time.sleep_ms(SLOW_MS)
    v += 10
us(p, CENTER)
print('    应连续均匀；有卡顿/咯咯声/顶住感 -> Ctrl+C')

print('=== 4. 保持中位 10 s，记下两只舵角指向 ===')
time.sleep(10)
print('=== 结束，两只都在 1500 ===')
