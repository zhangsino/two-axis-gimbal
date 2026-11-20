# -*- coding: utf-8 -*-
"""单轴补偿器（2026-11-18 重写版，干净重来）

与旧版的区别：阻尼用陀螺角速度，不再拿角度差分去估。
  角度差分在 100 Hz 下噪声约 10°/s，为了不抖只能把阻尼压得很小，
  结果阻尼形同虚设——一被推动就来回摆。陀螺噪声约 0.05°/s。

控制律：增量式
    us += DIR * (KP*误差 - KD*角速度) * 灵敏度
    每周期最多 SLEW us

保留的保护只有两条：
  1. 每周期限幅：走一小步，不猛冲
  2. 堵转：推了不动就停手（计数会衰减，不会永久锁死）

没有：死区、滞回、位置限制、零点缓存。
"""


class Axis:
    def __init__(self, name, us_per_deg, direction, center_us, lo_us, hi_us,
                 kp=0.15, kd=0.15, slew=8, stall_us=250):
        self.name = name
        self.us_per_deg = us_per_deg
        self.direction = direction
        self.center = center_us
        self.lo = lo_us
        self.hi = hi_us
        self.kp = kp
        self.kd = kd
        self.slew = slew
        self.stall_us = stall_us
        self.setpoint = 0.0
        self.us = center_us
        self.last_err = 0.0
        self.stuck = 0.0
        self.last_angle = None
        self.last_step = 0
        self.win_cnt = 0
        self.win_angle = None
        self.win_us = None

    def _clamp(self, v):
        if v > self.hi:
            return self.hi
        if v < self.lo:
            return self.lo
        return v

    def update(self, angle, rate):
        """angle: 度   rate: 度/秒（陀螺，已扣零偏）"""
        err = self.setpoint - angle
        self.last_err = err

        # 堵转：推了不动就停手（计数会衰减）
        self.stuck = max(0.0, self.stuck - 2.0)
        if self.last_angle is not None:
            if abs(angle - self.last_angle) > 0.6:
                self.stuck = 0.0
            else:
                self.stuck += abs(self.last_step)
        self.last_angle = angle

        # 慢速累积也要能判出来：1 秒窗口内脉宽变了 150 us、角度却几乎没变
        self.win_cnt += 1
        if self.win_cnt >= 100:
            if self.win_angle is not None:
                if abs(angle - self.win_angle) < 1.0 and abs(self.us - self.win_us) > 150:
                    self.stuck = self.stall_us + 1
            self.win_angle = angle
            self.win_us = self.us
            self.win_cnt = 0

        if self.stuck > self.stall_us:
            self.last_step = 0
            return self.us

        # 比例拉回 + 陀螺阻尼
        damp = self.kd * rate
        if damp > 6.0:
            damp = 6.0
        elif damp < -6.0:
            damp = -6.0
        step = self.direction * (self.kp * err - damp) * self.us_per_deg
        if step > self.slew:
            step = self.slew
        elif step < -self.slew:
            step = -self.slew

        before = self.us
        self.us = self._clamp(self.us + step)
        self.last_step = self.us - before
        return self.us
