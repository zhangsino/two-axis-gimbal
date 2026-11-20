# 舵机单件测试（MicroPython / Thonny 直接运行）
# 接线：棕=GND(共地) 红=5V(独立电源) 橙=信号->GPIO
# 注意：舵机不要从开发板 5V 取电

from machine import Pin, PWM
import time

PIN = 6            # 测第二个舵机时改成 7
SWEEP_MIN = 1000   # 保守行程，先别用 500/2500
SWEEP_MAX = 2000

p = PWM(Pin(PIN), freq=50)

def us(v):
    p.duty_u16(int(v * 65535 // 20000))

def hold(v, sec=1.5, tag=''):
    us(v)
    print('  %4d us  %s' % (v, tag))
    time.sleep(sec)

print('=== 1. 中位（记下舵角指向，4 个要一致）===')
hold(1500, 3, '中位')

print('=== 2. 两侧偏转（看方向是否一致）===')
hold(1200, 2, '应偏向一侧')
hold(1500, 1, '回中')
hold(1800, 2, '应偏向另一侧')
hold(1500, 1, '回中')

print('=== 3. 慢扫，听有没有卡顿/异响/齿跳 ===')
v = SWEEP_MIN
while v <= SWEEP_MAX:
    us(v)
    time.sleep_ms(25)
    v += 10
us(1500)
print('  扫完，回中')

print('=== 4. 断电前保持中位，现在用手轻拨舵角 ===')
print('    感觉自由行程（回差）：记下大约多少度')
print('    正常 <2°，>3° 说明齿隙大，优先当备件')
time.sleep(30)
print('=== 测试结束 ===')
