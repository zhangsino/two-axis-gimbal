# -*- coding: utf-8 -*-
"""云台 v2 干涉检查：用参数化实体做扫掠体素检测（1mm 网格）"""
import numpy as np, math, json, itertools

# ---------- 参数（与 Gimbal2Axis.py 保持一致）
DISC_R, DISC_T = 40.0, 4.0
DISC_Z = 63.0                      # 盘体 53..57
TP_R, TP_X = 7.0, (36.0, 42.0)
TN_R, TN_X = 6.0, (-42.0, -36.0)
RING_ID, RING_OD, RING_T = 88.0, 108.0, 10.0
RING_Z = (64.0, 74.0)
EAR_X, EAR_Y, EAR_Z = (50.0, 60.0), (11.0, 17.0), (64.0, 78.0)
YTR_R, YTR_Y = 6.0, (42.0, 62.5)
BASE, BASE_T = 130.0, 6.0
LEG_X, LEG_Y, LEG_Z = 22.0, (54.5, 62.5), (6.0, 70.0)
PAD_X, PAD_Y, PAD_Z = (11.0, 17.0), (62.5, 69.0), (63.0, 77.0)
BOSH_R, BOSH_Y = 8.0, (-69.0, -62.5)
AX_Z = 70.0

# 舵机（MG90S）
S_CASE = (22.5, 23.9, 12.7)        # 沿轴 / 长 / 宽
S_WING_T, S_WING_L = 2.8, 32.6
S_HORN_R, S_HORN_T = 10.0, 2.0
S_SHAFT_R, S_SHAFT_L = 2.4, 4.5


def inside_disc(p):
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    plate = (z >= DISC_Z) & (z <= DISC_Z + DISC_T) & (x * x + y * y <= DISC_R ** 2)
    tp = (x >= TP_X[0]) & (x <= TP_X[1]) & (y * y + (z - AX_Z) ** 2 <= TP_R ** 2)
    tn = (x >= TN_X[0]) & (x <= TN_X[1]) & (y * y + (z - AX_Z) ** 2 <= TN_R ** 2)
    return plate | tp | tn


def inside_ring(p):
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    r = np.sqrt(x * x + y * y)
    body = (r >= RING_ID / 2) & (r <= RING_OD / 2) & (z >= RING_Z[0]) & (z <= RING_Z[1])
    notch = (x >= RING_ID / 2 - 1) & (x <= RING_OD / 2 + 1) & (np.abs(y) <= 12.0)
    ear = (x >= EAR_X[0]) & (x <= EAR_X[1]) & (np.abs(y) >= EAR_Y[0]) & \
          (np.abs(y) <= EAR_Y[1]) & (z >= EAR_Z[0]) & (z <= EAR_Z[1])
    yt = (np.abs(y) >= YTR_Y[0]) & (np.abs(y) <= YTR_Y[1]) & \
         (x * x + (z - AX_Z) ** 2 <= YTR_R ** 2)
    return (body & ~notch) | ear | yt


def inside_frame(p):
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    base = (np.abs(x) <= BASE / 2) & (np.abs(y) <= BASE / 2) & (z >= 0) & (z <= BASE_T)
    leg = (np.abs(x) <= LEG_X) & (np.abs(y) >= LEG_Y[0]) & (np.abs(y) <= LEG_Y[1]) & \
          (z >= LEG_Z[0]) & (z <= LEG_Z[1])
    hole = (x * x + (z - AX_Z) ** 2 <= 6.3 ** 2) & (np.abs(y) >= LEG_Y[0] - 1)
    leg = leg & ~hole
    pad = (np.abs(x) >= PAD_X[0]) & (np.abs(x) <= PAD_X[1]) & \
          (y >= PAD_Y[0]) & (y <= PAD_Y[1]) & (z >= PAD_Z[0]) & (z <= PAD_Z[1])
    bosh = (y >= BOSH_Y[0]) & (y <= BOSH_Y[1]) & (x * x + (z - AX_Z) ** 2 <= BOSH_R ** 2)
    return base | leg | pad | bosh


def inside_hub(p):
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    body = (x >= 42.0) & (x <= 53.5) & (y * y + (z - AX_Z) ** 2 <= 9.0 ** 2)
    pin = (x >= 35.5) & (x <= 42.0) & (y * y + (z - AX_Z) ** 2 <= 4.0 ** 2)
    return body | pin


def inside_servo1(p):
    """固定在外环上，轴沿 -X，机身在 +X 外侧"""
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    x0 = 60.0
    case = (x >= x0) & (x <= x0 + S_CASE[0]) & (np.abs(y) <= S_CASE[1] / 2) & \
           (np.abs(z - AX_Z) <= S_CASE[2] / 2)
    wing = (x >= x0) & (x <= x0 + S_WING_T) & (np.abs(y) <= S_WING_L / 2) & \
           (np.abs(z - AX_Z) <= S_CASE[2] / 2)
    shaft = (x >= x0 - S_SHAFT_L) & (x <= x0) & (y * y + (z - AX_Z) ** 2 <= S_SHAFT_R ** 2)
    horn = (x >= x0 - S_SHAFT_L - S_HORN_T) & (x <= x0 - S_SHAFT_L) & \
           (y * y + (z - AX_Z) ** 2 <= S_HORN_R ** 2)
    return case | wing | shaft | horn


def inside_servo2(p):
    """固定在 U 架 +Y 腿，轴沿 -Y"""
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    y0 = 69.0
    case = (y >= y0) & (y <= y0 + S_CASE[0]) & (np.abs(x) <= S_CASE[1] / 2) & \
           (np.abs(z - AX_Z) <= S_CASE[2] / 2)
    wing = (y >= y0) & (y <= y0 + S_WING_T) & (np.abs(x) <= S_WING_L / 2) & \
           (np.abs(z - AX_Z) <= S_CASE[2] / 2)
    shaft = (y >= y0 - S_SHAFT_L) & (y <= y0) & (x * x + (z - AX_Z) ** 2 <= S_SHAFT_R ** 2)
    horn = (y >= y0 - S_SHAFT_L - S_HORN_T) & (y <= y0 - S_SHAFT_L) & \
           (x * x + (z - AX_Z) ** 2 <= S_HORN_R ** 2)
    return case | wing | shaft | horn


def rot_x(p, deg):
    """绕 X 轴（过 z=AX_Z）旋转"""
    t = math.radians(deg)
    q = p.copy()
    dz = p[:, 2] - AX_Z
    q[:, 1] = p[:, 1] * math.cos(t) - dz * math.sin(t)
    q[:, 2] = p[:, 1] * math.sin(t) + dz * math.cos(t) + AX_Z
    return q


def rot_y(p, deg):
    t = math.radians(deg)
    q = p.copy()
    dz = p[:, 2] - AX_Z
    q[:, 0] = p[:, 0] * math.cos(t) + dz * math.sin(t)
    q[:, 2] = -p[:, 0] * math.sin(t) + dz * math.cos(t) + AX_Z
    return q


def bbox_of(fn_pts):
    return fn_pts.min(axis=0), fn_pts.max(axis=0)


GRID = 1.2


def volume(fn, lo, hi):
    xs = np.arange(lo[0], hi[0] + GRID, GRID)
    ys = np.arange(lo[1], hi[1] + GRID, GRID)
    zs = np.arange(lo[2], hi[2] + GRID, GRID)
    g = np.stack(np.meshgrid(xs, ys, zs, indexing='ij'), -1).reshape(-1, 3)
    return g, bool(fn(g).any())


def overlap(fa, fb, deg=0.0, axis='x'):
    box = np.array([[-70, -75, 0], [95, 95, 72]], float)
    g, _ = volume(lambda p: np.zeros(len(p), bool), box[0], box[1])
    a = rot_x(g, deg) if axis == 'x' else rot_y(g, deg)
    return int((fa(a) & fb(g)).sum())


results = []
for axis, angles in (('x', [-40, -30, -20, -10, 0, 10, 20, 30, 40]),
                     ('y', [-40, -30, -20, -10, 0, 10, 20, 30, 40])):
    for deg in angles:
        if axis == 'x':
            mover = lambda p, d=deg: rot_x(p, d)
            pairs = [('disc', inside_disc, 'ring', inside_ring),
                     ('disc', inside_disc, 'servo1', inside_servo1),
                     ('hub', inside_hub, 'ring', inside_ring),
                     ('hub', inside_hub, 'servo1', inside_servo1)]
        else:
            mover = lambda p, d=deg: rot_y(p, d)
            pairs = [('ring', inside_ring, 'frame', inside_frame),
                     ('ring', inside_ring, 'servo2', inside_servo2),
                     ('servo1', inside_servo1, 'frame', inside_frame)]
        for na, fa, nb, fb in pairs:
            def fa_r(p):
                return fa(mover(p))
            box = np.array([[-70, -75, 0], [95, 95, 72]], float)
            g, _ = volume(lambda p: np.zeros(len(p), bool), box[0], box[1])
            n = int((fa_r(g) & fb(g)).sum())
            results.append({'axis': axis, 'deg': deg, 'a': na, 'b': nb, 'vox': n})

bad = [r for r in results if r['vox'] > 0]
print('总检查组合:', len(results))
print('有干涉的组合:', len(bad))
for r in bad:
    print('  %s 轴 %+d°: %s ↔ %s  %d 体素' % (r['axis'], r['deg'], r['a'], r['b'], r['vox']))

json.dump(results, open('interference.json', 'w'), ensure_ascii=False, indent=1)
