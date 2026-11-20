# MPU6050 筛选测试：零偏 + 倾角
from machine import I2C, Pin
import time, math, struct

SDA, SCL = 8, 9
i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
found = i2c.scan()
print('I2C scan:', found)
if 0x68 not in found and 0x69 not in found:
    print('!! 没找到 6050：查 VCC/GND/SDA/SCL，VCC 要 3.3V')
    raise SystemExit
addr = 0x68 if 0x68 in found else 0x69
print('addr = 0x%02X' % addr)
print('WHO_AM_I = 0x%02X (正品/兼容 6050 应为 0x68)' % i2c.readfrom_mem(addr, 0x75, 1)[0])

i2c.writeto_mem(addr, 0x6B, b'\x00')
time.sleep_ms(100)
i2c.writeto_mem(addr, 0x1A, b'\x03')
i2c.writeto_mem(addr, 0x1B, b'\x08')
i2c.writeto_mem(addr, 0x1C, b'\x08')
time.sleep_ms(100)

def raw():
    d = i2c.readfrom_mem(addr, 0x3B, 14)
    return struct.unpack('>7h', d)

print('--- 静置采样 200 次，别碰它 ---')
sgx = sgy = sgz = 0.0
mx = my = mz = 0.0
N = 200
for _ in range(N):
    ax, ay, az, t, gx, gy, gz = raw()
    x, y, z = gx / 65.5, gy / 65.5, gz / 65.5
    sgx += x * x; sgy += y * y; sgz += z * z
    mx += x; my += y; mz += z
    time.sleep_ms(10)
mx /= N; my /= N; mz /= N
sdx = math.sqrt(sgx / N - mx * mx)
sdy = math.sqrt(sgy / N - my * my)
sdz = math.sqrt(sgz / N - mz * mz)
print('零偏  x=%+.2f  y=%+.2f  z=%+.2f  deg/s' % (mx, my, mz))
print('噪声  x=%.2f  y=%.2f  z=%.2f  deg/s' % (sdx, sdy, sdz))
worst = max(abs(mx), abs(my))
if worst < 2:   print('判定：好件（零偏 < 2 deg/s）')
elif worst < 5: print('判定：可用（2~5 deg/s，固件里扣掉）')
else:           print('判定：换一片（> 5 deg/s）')

print('--- 现在倾斜它，看角度（10 秒）---')
for _ in range(50):
    ax, ay, az, t, gx, gy, gz = raw()
    axg, ayg, azg = ax / 8192.0, ay / 8192.0, az / 8192.0
    pitch = math.degrees(math.atan2(ayg, azg))
    roll = math.degrees(math.atan2(-axg, math.sqrt(ayg * ayg + azg * azg)))
    print('  pitch %+6.1f  roll %+6.1f' % (pitch, roll))
    time.sleep_ms(200)
print('=== 结束 ===')
