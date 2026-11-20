#!/usr/bin/env python3
# v3 舵机-圆盘 耦合示意图（侧面 + 正面），单位 mm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "Heiti SC"]
plt.rcParams["axes.unicode_minus"] = False

Z0 = 70.0           # 输出轴轴线 = 云台滚转轴
ZC = 76.3           # 机身中心（轴在壳体上偏心 6.3）
CASE_L, CASE_D = 23.9, 22.5      # 长(Z) 深(X)
RING_IN, RING_OUT = 44.0, 54.0
FL_X0, FL_HW, FL_HH = 52.0, 46.0, 17.0
WIN_R = 15.0
HUB_TUBE_D, HUB_FL_D = 10.0, 20.0
HORN_X0, HORN_R = 55.5, 11.5
HOLES = [5.08, 7.62, 10.16, 12.70, 15.24]
R_SCREW = 7.62

C_DISC, C_HUB, C_HORN = "#d8d8d8", "#8ec5e8", "#f0a35e"
C_SERVO, C_SLEEVE, C_FLANGE, C_SCREW = "#9a9a9a", "#cfe6cf", "#8fc98f", "#c0392b"


def rect(ax, x0, z0, w, h, color, ec="#333", lw=1.0, alpha=1.0, ls="-", z=2):
    ax.add_patch(Rectangle((x0, z0), w, h, facecolor=color, edgecolor=ec, lw=lw,
                           alpha=alpha, ls=ls, zorder=z))


def mark(ax, x, z, n, fs=11):
    ax.text(x, z, n, fontsize=fs, ha="center", va="center", color="white",
            fontweight="bold", zorder=30,
            bbox=dict(boxstyle="circle,pad=0.28", fc="#37474f", ec="none"))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.0, 9.6))

# ---------------- 左：侧视 ----------------
ax = ax1
ax.set_title("① 侧视（沿 −Y 看）", fontsize=14, pad=8)

rect(ax, 40, 28, 2, 84, C_DISC, z=3)
rect(ax, 55, ZC - 15.35, 33, 30.7, C_SLEEVE, z=1, alpha=.55)
rect(ax, FL_X0, ZC - FL_HH, 3, 2 * FL_HH, C_FLANGE, z=5)
rect(ax, 60, ZC - CASE_L / 2, CASE_D, CASE_L, C_SERVO, z=3)
rect(ax, 56.7, Z0 - 2.4, 3.3, 4.8, "#777", z=4)
rect(ax, HORN_X0, Z0 - HORN_R, 1.2, 2 * HORN_R, C_HORN, z=6)
rect(ax, HORN_X0, Z0 - 3, 2.1, 6, C_HORN, ec="#a5641f", z=7)
rect(ax, 42, Z0 - HUB_TUBE_D / 2, 11, HUB_TUBE_D, C_HUB, z=5)
rect(ax, 53, Z0 - HUB_FL_D / 2, 2.5, HUB_FL_D, C_HUB, z=6)
ax.plot([55, 58], [ZC - 14, ZC - 14], color="#3a7a3a", lw=1.4, ls=(0, (3, 2)), zorder=4)
ax.plot([55, 58], [ZC + 14, ZC + 14], color="#3a7a3a", lw=1.4, ls=(0, (3, 2)), zorder=4)

for zc in (Z0 + R_SCREW, Z0 - R_SCREW):
    ax.plot([51.0, 56.7], [zc, zc], color=C_SCREW, lw=2.4, zorder=12)
    ax.plot([51.0, 51.0], [zc - 1.1, zc + 1.1], color=C_SCREW, lw=2.4, zorder=12)
    ax.plot([38.6, 42.0], [zc, zc], color="#1f6fb4", lw=1.3, ls=(0, (4, 2)), zorder=12)

mark(ax, 58.4, Z0 + 8.6, "1")
mark(ax, 50.6, Z0 + R_SCREW + 3.4, "2")
mark(ax, 47.0, Z0 - 7.0, "3")
mark(ax, 53.5, ZC + 13.0, "4")
mark(ax, 56.1, Z0 - 9.5, "5")

ax.set_xlim(34, 96)
ax.set_ylim(46, 100)
ax.set_aspect("equal")
ax.grid(alpha=.25, lw=.5)
ax.set_xlabel("X (mm)  → 舵机侧")
ax.set_ylabel("Z (mm)")

# ---------------- 右：正面 ----------------
ax = ax2
ax.set_title("② 正面（沿 −X 看，圆盘轮廓虚线）", fontsize=14, pad=8)

ax.add_patch(Circle((0, Z0), RING_OUT, facecolor="#ededed", ec="#999", lw=1.0, zorder=1))
ax.add_patch(Circle((0, Z0), RING_IN, facecolor="white", ec="#999", lw=1.0, zorder=2))
ax.add_patch(Circle((0, Z0), 42.0, facecolor="none", ec="#777", lw=1.2,
                    ls=(0, (5, 3)), zorder=2.5))
rect(ax, -FL_HW, ZC - FL_HH, 2 * FL_HW, 2 * FL_HH, C_FLANGE, z=3, alpha=.92)
ax.add_patch(Circle((0, Z0), WIN_R, facecolor="white", ec="#2e7d32", lw=1.5, zorder=4))
ax.add_patch(Circle((0, Z0), HUB_FL_D / 2, facecolor=C_HUB, ec="#1f6fb4", lw=1.5, zorder=5))
ax.add_patch(Circle((0, Z0), HUB_TUBE_D / 2, facecolor="white", ec="#1f6fb4", lw=1.1, zorder=6))

ax.add_patch(Rectangle((-1.5, Z0 - HORN_R), 3, 2 * HORN_R, facecolor="none",
                       edgecolor=C_HORN, lw=1.8, ls=(0, (5, 3)), zorder=7))
for r in HOLES:
    for zc in (Z0 + r, Z0 - r):
        ax.add_patch(Circle((0, zc), 1.0, facecolor="none", ec=C_HORN, lw=1.0,
                            ls=(0, (3, 2)), zorder=8))
for zc in (Z0 + R_SCREW, Z0 - R_SCREW):
    ax.add_patch(Circle((0, zc), 2.0, facecolor="none", ec="#1f6fb4", lw=2.2, zorder=9))
    ax.add_patch(Circle((0, zc), 1.0, facecolor=C_SCREW, ec="none", alpha=.6, zorder=10))
for yy in (-(RING_IN + 2), RING_IN + 2):
    for zz in (ZC - 8, ZC + 8):
        ax.add_patch(Circle((yy, zz), 1.7, facecolor="white", ec="#2e7d32", lw=1.5, zorder=8))
        ax.add_patch(Circle((yy, zz), 1.25, facecolor="none", ec="#2e7d32", lw=.8,
                            ls=":", zorder=9))

ax.annotate("A", xy=(0, Z0 + R_SCREW + 1.2), xytext=(0, Z0 + R_SCREW + 11.5),
            ha="center", va="center", fontsize=11, color="white", fontweight="bold", zorder=30,
            bbox=dict(boxstyle="circle,pad=0.28", fc="#37474f", ec="none"),
            arrowprops=dict(arrowstyle="-", color="#37474f", lw=1.2))
mark(ax, -10.6, Z0 + 10.6, "B")
mark(ax, 6.0, Z0 - 6.0, "C")
mark(ax, RING_IN + 2, ZC + 8, "D")

ax.set_xlim(-56, 56)
ax.set_ylim(4, 116)
ax.set_aspect("equal")
ax.grid(alpha=.25, lw=.5)
ax.set_xlabel("Y (mm)")
ax.set_ylabel("Z (mm)")

left_txt = (
    "1  舵角先压上花键、中心螺丝拧紧（此时圆盘还没装，手能伸进去）\n"
    "2  M2×5：头贴在轮毂法兰背面，螺丝刀从圆盘背面 Ø4 过孔穿进来，\n"
    "     穿过 11 mm 空隙，拧进舵角第 3 孔（r=7.62）\n"
    "3  扭矩路径：花键 → 舵角 → 2×M2 → 轮毂法兰 → 轮毂管 → 粘接 → 圆盘\n"
    "4  前法兰板 3 厚，与套子立管、两根侧筋是同一件（虚线是侧筋）\n"
    "5  舵角剪成两条臂，沿 ±Z 留到 r=11.5；十字的那对短臂剪掉"
)
right_txt = (
    "A  Ø4 过孔 ×2（打在圆盘上），正好对准舵角第 3 孔 r=7.62\n"
    "B  Ø30 窗口：舵角 r=11.5 在窗口里扫，四周留 3.5\n"
    "C  轮毂法兰 Ø20（M2 头 Ø3.8，r9.5 < r10 才放得下）\n"
    "D  4×M3 @ y±46, z 68.3 / 84.3，拧进环的端面（环 r44–54）"
)
fig.text(0.055, 0.015, left_txt, fontsize=10.2, va="bottom", linespacing=1.55)
fig.text(0.545, 0.015, right_txt, fontsize=10.2, va="bottom", linespacing=1.55)

fig.suptitle("两轴云台 v3 · 舵机与圆盘怎么固定（舵角孔距 0.1\" = 2.54 mm，首孔距中心 0.2\" = 5.08 mm）",
             fontsize=15, y=.975)
fig.tight_layout(rect=[0.01, 0.175, 0.99, 0.945])
out = "/Users/zhangxi/Documents/deepseek-harness/default-workspace/gimbal/v3_coupling.png"
fig.savefig(out, dpi=150)
print("saved", out)
