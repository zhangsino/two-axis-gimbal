#!/usr/bin/env python3
# v3 舵机-圆盘 耦合示意图（侧面 + 正面），单位 mm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "Heiti SC"]
plt.rcParams["axes.unicode_minus"] = False

Z0 = 70.0          # 输出轴轴线 / 云台滚转轴
ZC = 76.3          # 机身中心（轴偏心 6.3）
CASE_L, CASE_T, CASE_D = 23.9, 12.7, 22.5     # 长(Z) 厚(Y) 深(X)
CAV_Y, CAV_Z = 13.7, 24.7                     # 套子内腔
RING_IN, RING_OUT, RING_X0, RING_X1 = 44.0, 54.0, 40.0, 52.0
FL_X0, FL_X1 = 52.0, 55.0                     # 前法兰板
FL_HALF_W, FL_HALF_H = 46.0, 17.0
WIN_R = 15.0
HUB_TUBE_D, HUB_FL_D = 10.0, 20.0             # 轮毂管 Ø10、法兰 Ø20
HORN_X0, HORN_X1 = 55.5, 56.7                 # 舵角
HORN_R = 11.5
HOLES = [5.08, 7.62, 10.16, 12.70, 15.24]
R_SCREW = 7.62

C_DISC   = "#dcdcdc"
C_HUB    = "#8ec5e8"
C_HORN   = "#f0a35e"
C_SERVO  = "#9a9a9a"
C_SLEEVE = "#c8dfc8"
C_FLANGE = "#8fc98f"
C_SCREW  = "#c0392b"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 7.4))


def rect(ax, x0, z0, w, h, color, ec="#333", lw=1.0, alpha=1.0, ls="-", z=2, label=None):
    r = Rectangle((x0, z0), w, h, facecolor=color, edgecolor=ec, lw=lw,
                  alpha=alpha, ls=ls, zorder=z, label=label)
    ax.add_patch(r)
    return r


# ---------------- 左：侧视（沿 -Y 看） ----------------
ax = ax1
ax.set_title("① 侧视（沿 −Y 看）：舵角怎么被拧住", fontsize=13, pad=10)

rect(ax, 40, 28, 2, 84, C_DISC, z=3)                       # 圆盘（边缘一段）
rect(ax, FL_X0, ZC - FL_HALF_H, 3, 2 * FL_HALF_H, C_FLANGE, z=4)   # 前法兰板
rect(ax, 58, ZC - 12.35 - 3, 30, 4.7, C_SLEEVE, z=1, alpha=.5)     # 套子下壁
rect(ax, 58, ZC + 12.35, 30, 3, C_SLEEVE, z=1, alpha=.5)           # 套子上壁
rect(ax, 60, ZC - CASE_L / 2, CASE_D, CASE_L, C_SERVO, z=2)        # 机身
rect(ax, 56.7, Z0 - 2.4, 3.3, 4.8, "#777", z=3)                    # 输出轴
rect(ax, HORN_X0, Z0 - HORN_R, 1.2, 2 * HORN_R, C_HORN, z=5)       # 舵角两臂
rect(ax, HORN_X0, Z0 - 3, 2.1, 6, C_HORN, ec="#a5641f", z=6)       # 舵角中心凸台
rect(ax, 42, Z0 - HUB_TUBE_D / 2, 11, HUB_TUBE_D, C_HUB, z=4)      # 轮毂管
rect(ax, 53, Z0 - HUB_FL_D / 2, 2.5, HUB_FL_D, C_HUB, z=5)         # 轮毂法兰

# 两颗 M2 螺丝（r=7.62，沿 ±Z）
for zc in (Z0 + R_SCREW, Z0 - R_SCREW):
    ax.plot([51.0, 56.7], [zc, zc], color=C_SCREW, lw=2.2, zorder=8)
    ax.plot([51.0, 51.0], [zc - .9, zc + .9], color=C_SCREW, lw=2.2, zorder=8)
    ax.add_patch(Circle((56.6, zc), 1.0, facecolor=C_SCREW, alpha=.25, ec="none", zorder=7))

# 圆盘背面的 Ø4 过孔（螺丝刀从这里进）
for zc in (Z0 + R_SCREW, Z0 - R_SCREW):
    ax.plot([38.8, 42.0], [zc, zc], color="#1f6fb4", lw=1.2, ls=(0, (4, 2)), zorder=9)

ax.annotate("① 舵角先压上花键、\n中心螺丝拧紧", xy=(57.0, Z0 + 3.2),
            xytext=(70, Z0 + 20), fontsize=10.5, color="#8a4b12",
            arrowprops=dict(arrowstyle="->", color="#8a4b12", lw=1.2))
ax.annotate("② M2×5 从圆盘背面\n经 Ø4 过孔穿进去,\n拧进舵角第 3 孔",
            xy=(54.0, Z0 + R_SCREW), xytext=(63, Z0 + 34), fontsize=10.5,
            color=C_SCREW, arrowprops=dict(arrowstyle="->", color=C_SCREW, lw=1.2))
ax.annotate("③ 扭矩：花键→舵角→M2→轮毂法兰→轮毂管→粘接→圆盘",
            xy=(44, Z0 - HUB_TUBE_D / 2), xytext=(35, Z0 - 34), fontsize=10.5,
            color="#1f6fb4", arrowprops=dict(arrowstyle="->", color="#1f6fb4", lw=1.2))
ax.annotate("前法兰板 3 厚\n（与套子一件）", xy=(53.5, ZC + 14), xytext=(34, ZC + 26),
            fontsize=10, color="#2e7d32",
            arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1.0))
ax.annotate("舵角剪成两臂\n留到 r11.5", xy=(56.1, Z0 - HORN_R), xytext=(72, Z0 - 30),
            fontsize=10, color="#8a4b12",
            arrowprops=dict(arrowstyle="->", color="#8a4b12", lw=1.0))
ax.annotate("轮毂 Ø20", xy=(54.0, Z0 - HUB_FL_D / 2), xytext=(62, Z0 - 20),
            fontsize=10, color="#1f6fb4",
            arrowprops=dict(arrowstyle="->", color="#1f6fb4", lw=1.0))

ax.set_xlim(36, 94)
ax.set_ylim(48, 98)
ax.set_aspect("equal")
ax.grid(alpha=.25, lw=.5)
ax.set_xlabel("X (mm)  →舵机侧")
ax.set_ylabel("Z (mm)")

# ---------------- 右：正面（从圆盘侧看 +X） ----------------
ax = ax2
ax.set_title("② 正面（从圆盘一侧看 +X）：孔位", fontsize=13, pad=10)

ax.add_patch(Circle((0, Z0), RING_OUT, facecolor="#eeeeee", ec="#999", lw=1.0, zorder=1))
ax.add_patch(Circle((0, Z0), RING_IN, facecolor="white", ec="#999", lw=1.0, zorder=2))
rect(ax, -FL_HALF_W, ZC - FL_HALF_H, 2 * FL_HALF_W, 2 * FL_HALF_H, C_FLANGE, z=3, alpha=.9)
ax.add_patch(Circle((0, Z0), WIN_R, facecolor="white", ec="#2e7d32", lw=1.4, zorder=4))
ax.add_patch(Circle((0, Z0), HUB_FL_D / 2, facecolor=C_HUB, ec="#1f6fb4", lw=1.4, zorder=5))
ax.add_patch(Circle((0, Z0), HUB_TUBE_D / 2, facecolor="white", ec="#1f6fb4", lw=1.0, zorder=6))

# 舵角两臂（被法兰挡住 → 虚线）
for zc in (Z0 + HORN_R, Z0 - HORN_R):
    pass
ax.add_patch(Rectangle((-1.5, Z0 - HORN_R), 3, 2 * HORN_R, facecolor="none",
                       edgecolor=C_HORN, lw=1.6, ls=(0, (5, 3)), zorder=7))
for r in HOLES:
    for zc in (Z0 + r, Z0 - r):
        ax.add_patch(Circle((0, zc), 1.0, facecolor="none", ec=C_HORN, lw=1.0,
                            ls=(0, (3, 2)), zorder=8))

# 用到的两颗 M2：同时画圆盘 Ø4 过孔 + 舵角 Ø2 孔
for zc in (Z0 + R_SCREW, Z0 - R_SCREW):
    ax.add_patch(Circle((0, zc), 4.0 / 2, facecolor="none", ec="#1f6fb4", lw=2.0, zorder=9))
    ax.add_patch(Circle((0, zc), 2.0 / 2, facecolor=C_SCREW, ec="none", alpha=.55, zorder=10))
    ax.annotate(f"r={R_SCREW}", xy=(0, zc), xytext=(10, zc + 1.5), fontsize=9.5,
                color="#1f6fb4")

# 4 颗 M3 拧进环
for yy in (-(RING_IN + 2), RING_IN + 2):
    for zz in (ZC - 8, ZC + 8):
        ax.add_patch(Circle((yy, zz), 3.4 / 2, facecolor="white", ec="#2e7d32", lw=1.4, zorder=8))
        ax.add_patch(Circle((yy, zz), 2.5 / 2, facecolor="none", ec="#2e7d32", lw=.8, ls=":", zorder=9))

ax.annotate("Ø4 过孔（圆盘上，共 2 个）\n螺丝刀从这里进", xy=(2.0, Z0 + R_SCREW),
            xytext=(16, Z0 + 26), fontsize=10.5, color="#1f6fb4",
            arrowprops=dict(arrowstyle="->", color="#1f6fb4", lw=1.1))
ax.annotate("Ø30 窗口\n（舵角 r11.5 在里面转）", xy=(-10.6, Z0 + 10.6), xytext=(-40, Z0 + 26),
            fontsize=10, color="#2e7d32",
            arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1.0))
ax.annotate("轮毂法兰 Ø20", xy=(-7.0, Z0 + 7.0), xytext=(-40, Z0 - 20),
            fontsize=10, color="#1f6fb4",
            arrowprops=dict(arrowstyle="->", color="#1f6fb4", lw=1.0))
ax.annotate("4×M3 拧进环端面", xy=(-46, ZC + 8), xytext=(-44, ZC - 26),
            fontsize=10, color="#2e7d32",
            arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1.0))
ax.annotate("环 r44–54", xy=(0, Z0 - 49), xytext=(-16, Z0 - 62), fontsize=10,
            color="#666", arrowprops=dict(arrowstyle="->", color="#666", lw=1.0))

ax.set_xlim(-52, 52)
ax.set_ylim(Z0 - 62, Z0 + 46)
ax.set_aspect("equal")
ax.grid(alpha=.25, lw=.5)
ax.set_xlabel("Y (mm)")
ax.set_ylabel("Z (mm)")

fig.suptitle("两轴云台 v3 · 舵机与圆盘的耦合（舵角孔距 0.1\" = 2.54 mm，首孔 5.08 mm）",
             fontsize=14.5, y=.985)
fig.tight_layout(rect=[0, 0, 1, .955])
out = "/Users/zhangxi/Documents/deepseek-harness/default-workspace/gimbal/v3_coupling.png"
fig.savefig(out, dpi=150)
print("saved", out)
