# -*- coding: utf-8 -*-
"""MPU6050 最小驱动（MicroPython）

寄存器依据：MPU-6050 Register Map (RM-MPU-6000A-00)
  0x6B PWR_MGMT_1   0x00 = 唤醒，0x01 = 用陀螺 X 轴时钟
  0x1A CONFIG       DLPF_CFG=3 -> 44 Hz
  0x1B GYRO_CONFIG  FS_SEL=1 -> ±500 °/s，65.5 LSB/(°/s)
  0x1C ACCEL_CONFIG AFS_SEL=1 -> ±4g，8192 LSB/g
  0x3B 起连续 14 字节：ax ay az temp gx gy gz
"""
import struct
import time


class MPU6050:
    ACC_LSB = 8192.0     # ±4g
    GYRO_LSB = 65.5      # ±500 °/s

    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.bias = [0.0, 0.0, 0.0]
        who = self.i2c.readfrom_mem(self.addr, 0x75, 1)[0]
        if who != 0x68:
            raise OSError('MPU6050 not found, WHO_AM_I=0x%02X' % who)
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
        time.sleep_ms(50)
        self.i2c.writeto_mem(self.addr, 0x1A, b'\x03')
        self.i2c.writeto_mem(self.addr, 0x1B, b'\x08')
        self.i2c.writeto_mem(self.addr, 0x1C, b'\x08')

    def read_raw(self):
        d = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        ax, ay, az, _t, gx, gy, gz = struct.unpack('>7h', d)
        return ax, ay, az, gx, gy, gz

    def calibrate(self, n=300):
        """静止状态下取均值做零偏（陀螺 bias + 加速度零点）"""
        sx = sy = sz = 0.0
        ax0 = ay0 = 0.0
        for _ in range(n):
            ax, ay, az, gx, gy, gz = self.read_raw()
            sx += gx
            sy += gy
            sz += gz
            ax0 += ax
            ay0 += ay
            time.sleep_ms(2)
        self.bias = [sx / n / self.GYRO_LSB, sy / n / self.GYRO_LSB, sz / n / self.GYRO_LSB]
        self.acc_bias = [ax0 / n / self.ACC_LSB, ay0 / n / self.ACC_LSB]
        return self.bias

    def read(self):
        """返回 (ax_g, ay_g, az_g, gx_dps, gy_dps, gz_dps)"""
        ax, ay, az, gx, gy, gz = self.read_raw()
        ax = ax / self.ACC_LSB - self.acc_bias[0]
        ay = ay / self.ACC_LSB - self.acc_bias[1]
        az = az / self.ACC_LSB
        gx = gx / self.GYRO_LSB - self.bias[0]
        gy = gy / self.GYRO_LSB - self.bias[1]
        gz = gz / self.GYRO_LSB - self.bias[2]
        return ax, ay, az, gx, gy, gz
