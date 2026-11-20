# -*- coding: utf-8 -*-
# 受控阶跃测试：没人碰机构，只改设定值，看闭环会不会自己摆
import time, math, struct
from machine import I2C, Pin, PWM
import config, ctrl

D = lambda v: int(v * 65535 // 20000)
def clamp(v, lo, hi): return lo if v < lo else (hi if v > hi else v)

i2c = I2C(0, scl=Pin(config.PIN_SCL), sda=Pin(config.PIN_SDA), freq=config.I2C_FREQ)
A = config.MPU_ADDR
i2c.writeto_mem(A, 0x6B, b'\x00'); time.sleep_ms(100)
i2c.writeto_mem(A, 0x1A, b'\x03'); i2c.writeto_mem(A, 0x1B, b'\x08'); i2c.writeto_mem(A, 0x1C, b'\x08')
time.sleep_ms(100)

def sample():
    d = struct.unpack('>7h', i2c.readfrom_mem(A, 0x3B, 14))
    ax, ay, az = d[0]/8192.0, d[1]/8192.0, d[2]/8192.0
    n = math.sqrt(ay*ay+az*az) or 1e-6
    return (math.degrees(math.atan2(ay, az)),
            math.degrees(math.atan2(-ax, n)),
            d[4]/65.5, d[5]/65.5)

# 陀螺零偏
bx = by = 0.0
for _ in range(60):
    s = sample(); bx += s[2]; by += s[3]; time.sleep_ms(10)
bx /= 60; by /= 60
print('陀螺零偏 gx %+.2f gy %+.2f' % (bx, by))

pa = PWM(Pin(config.PIN_SERVO_A), freq=50); pa.duty_u16(D(1500))
pb = PWM(Pin(config.PIN_SERVO_B), freq=50); pb.duty_u16(D(1500))
time.sleep(1.0)

# 找零点
ua = ub = 1500
for ax_ in ('A', 'B'):
    for i in range(8):
        ps = []; rs = []
        for _ in range(5):
            s = sample(); ps.append(s[0]); rs.append(s[1]); time.sleep_ms(8)
        p = sum(ps)/len(ps); r = sum(rs)/len(rs)
        ang = p if ax_ == 'A' else r
        if abs(ang) < 0.35:
            break
        if ax_ == 'A':
            ua = clamp(ua + config.DIR_A*(0-ang)*config.US_PER_DEG_A*0.8, 900, 2100)
            pa.duty_u16(D(ua))
        else:
            ub = clamp(ub + config.DIR_B*(0-ang)*config.US_PER_DEG_B*0.8, 900, 2100)
            pb.duty_u16(D(ub))
        time.sleep_ms(700)
print('零点 A %d B %d' % (ua, ub))

aa = ctrl.Axis('A', config.US_PER_DEG_A, config.DIR_A, ua, 500, 2500,
               kp=config.KP, kd=config.KD, slew=config.SLEW_US, stall_us=config.STALL_US)
ab = ctrl.Axis('B', config.US_PER_DEG_B, config.DIR_B, ub, 500, 2500,
               kp=config.KP, kd=config.KD, slew=config.SLEW_US, stall_us=config.STALL_US)

plan = [(0,0.0,0.0),(3000,8.0,0.0),(8000,0.0,0.0),(12000,0.0,8.0),(17000,0.0,0.0),(21000,0.0,0.0)]
dt = config.LOOP_MS/1000.0
t0 = time.ticks_ms()
idx = 0
pf = rf = None
print('t_ms  pitch   roll   A_us  B_us')
try:
    while True:
        now = time.ticks_diff(time.ticks_ms(), t0)
        while idx+1 < len(plan) and now >= plan[idx+1][0]:
            idx += 1
            print('--- %5d 设定 pitch %+.1f roll %+.1f ---' % plan[idx])
        aa.setpoint = plan[idx][1]; ab.setpoint = plan[idx][2]
        s = sample()
        gx = s[2]-bx; gy = s[3]-by
        if pf is None: pf, rf = s[0], s[1]
        else:
            pf = config.ALPHA*(pf+gx*dt) + (1-config.ALPHA)*s[0]
            rf = config.ALPHA*(rf+gy*dt) + (1-config.ALPHA)*s[1]
        u1 = aa.update(pf, gx); u2 = ab.update(rf, gy)
        pa.duty_u16(D(u1)); pb.duty_u16(D(u2))
        if now % 100 < config.LOOP_MS:
            print('%5d %+7.2f %+7.2f %5d %5d' % (now, pf, rf, u1, u2))
        if now > 22000:
            break
        used = time.ticks_diff(time.ticks_ms(), t0) - now
        if used < config.LOOP_MS:
            time.sleep_ms(config.LOOP_MS-used)
finally:
    pa.deinit(); pb.deinit()
    print('结束')
