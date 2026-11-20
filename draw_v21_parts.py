# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

plt.rcParams['font.family'] = 'PingFang SC'
fig, axs = plt.subplots(2, 2, figsize=(16, 11))
(ax1, ax2), (ax3, ax4) = axs

def notes(ax, lines, x=0.02, y=0.02):
    ax.text(x, y, '\n'.join(lines), transform=ax.transAxes, fontsize=8.6,
            va='bottom', ha='left', family='PingFang SC',
            bbox=dict(fc='#f7f9fc', ec='#cbd5e0', lw=0.6, pad=5))

# ---------------- 内盘 ----------------
ax1.set_title('① Disc 内盘（俯视，打印姿态）', fontsize=12)
ax1.add_patch(Circle((0,0), 40, fc='#dce9f7', ec='#2b6cb0', lw=1.8))
ax1.add_patch(Circle((0,0), 40, fc='none', ec='#2b6cb0', lw=0.6, ls=':'))
ax1.add_patch(Rectangle((36,-7), 6, 14, fc='#c9dcf2', ec='#2b6cb0', lw=1.2))
ax1.add_patch(Rectangle((-42,-6), 6, 12, fc='#c9dcf2', ec='#2b6cb0', lw=1.2))
ax1.add_patch(Rectangle((-11,-8.5), 22, 17, fc='none', ec='#276749', lw=1.1, ls='--'))
ax1.text(0, 0, '6050 槽 22×17×1.7', fontsize=7.5, ha='center', va='center', color='#276749')
ax1.annotate('+X 凸台 Ø14\n36→42，中心 Ø8.2×7 插座', xy=(42,0), xytext=(46,-26), fontsize=7.5,
             color='#2b6cb0', arrowprops=dict(arrowstyle='-', lw=0.7))
ax1.annotate('−X 耳轴 Ø12\n−42→−36，M3 螺母孔 Ø4.6×6', xy=(-42,0), xytext=(-78,22), fontsize=7.5,
             color='#2b6cb0', arrowprops=dict(arrowstyle='-', lw=0.7))
ax1.text(0, -52, 'Ø80 · 板厚 4 · 耳轴轴线离板面 7', ha='center', fontsize=9, color='#2b6cb0')
ax1.set_xlim(-88, 62); ax1.set_ylim(-60, 50); ax1.set_aspect('equal'); ax1.axis('off')

# ---------------- 外环 ----------------
ax2.set_title('② Ring 外环（俯视，打印姿态）', fontsize=12)
ax2.add_patch(Circle((0,0), 54, fc='none', ec='#222', lw=2.4))
ax2.add_patch(Circle((0,0), 44, fc='none', ec='#888', lw=0.8, ls='--'))
ax2.add_patch(Rectangle((44,-12), 11, 24, fc='white', ec='none'))
ax2.add_patch(Rectangle((50,11), 10, 6, fc='#efefef', ec='#555', lw=1.0))
ax2.add_patch(Rectangle((50,-17), 10, 6, fc='#efefef', ec='#555', lw=1.0))
ax2.add_patch(Rectangle((44,-6), 18.5, 12, fc='#dde6f2', ec='#06c', lw=0.9))
ax2.add_patch(Rectangle((-6,44), 12, 18.5, fc='#dde6f2', ec='#06c', lw=0.9))
ax2.add_patch(Rectangle((-6,-62.5), 12, 18.5, fc='#dde6f2', ec='#06c', lw=0.9))
ax2.annotate('+X 让位缺口 ±12\n(x 43…55)', xy=(50,12), xytext=(56,32), fontsize=7.5,
             arrowprops=dict(arrowstyle='-', lw=0.7))
ax2.annotate('耳板 10×6×14\nM2 预孔 Ø1.6 @Y±14.3', xy=(55,14), xytext=(52,-34), fontsize=7.5,
             arrowprops=dict(arrowstyle='-', lw=0.7))
ax2.annotate('+Y 耳轴 Ø12→62.5\n端面 2×Ø2.2 (舵角)', xy=(0,55), xytext=(-72,70), fontsize=7.5,
             arrowprops=dict(arrowstyle='-', lw=0.7))
ax2.text(0, -76, 'Ø108 / Ø88 · 厚 10 · 轴线离底面 6', ha='center', fontsize=9, color='#2b6cb0')
ax2.set_xlim(-90, 80); ax2.set_ylim(-84, 84); ax2.set_aspect('equal'); ax2.axis('off')

# ---------------- U 架 ----------------
ax3.set_title('③ Frame U 架（正视，打印姿态）', fontsize=12)
ax3.add_patch(Rectangle((-65,0), 130, 6, fc='#d6d6d6', ec='#444', lw=1.6))
ax3.add_patch(Rectangle((-22,6), 44, 64, fc='#d6d6d6', ec='#555', lw=1.4))
ax3.add_patch(Polygon([[-28,6],[-22,6],[-22,18]], closed=True, fc='#c4c4c4', ec='#555', lw=0.8))
ax3.add_patch(Polygon([[28,6],[22,6],[22,18]], closed=True, fc='#c4c4c4', ec='#555', lw=0.8))
ax3.add_patch(Circle((0,70), 6.15, fc='white', ec='#06c', lw=1.2))
ax3.add_patch(Rectangle((11,63), 6, 14, fc='#efefef', ec='#555', lw=1.0))
ax3.add_patch(Rectangle((-17,63), 6, 14, fc='#efefef', ec='#555', lw=1.0))
ax3.annotate('−Y 侧 Ø16 垫块（在图后）\nØ3.4 过孔，M3 压轴肩', xy=(-6,70), xytext=(-64,84),
             fontsize=7.5, color='#06c', arrowprops=dict(arrowstyle='-', lw=0.7))
ax3.annotate('腿孔 Ø12.3 @Z=70', xy=(4,70), xytext=(26,80), fontsize=8, arrowprops=dict(arrowstyle='-', lw=0.7))
ax3.annotate('+Y 舵机耳板\nX±(11…17) Y62.5…69 Z63…77\nM2 预孔 Ø1.6 @Z=70', xy=(14,70), xytext=(30,48),
             fontsize=7.5, arrowprops=dict(arrowstyle='-', lw=0.7))
ax3.annotate('腿根 R4', xy=(-24,10), xytext=(-58,24), fontsize=8, arrowprops=dict(arrowstyle='-', lw=0.7))
ax3.text(0, 92, '底板 130×130×6 · 腿 44×8 · 腿顶 Z=70', ha='center', fontsize=9, color='#2b6cb0')
ax3.set_xlim(-72, 78); ax3.set_ylim(-24, 100); ax3.set_aspect('equal'); ax3.axis('off')

# ---------------- 轮毂 ----------------
ax4.set_title('④ Hub 轮毂（剖面，打印姿态）', fontsize=12)
ax4.add_patch(Rectangle((-9,0), 18, 11.5, fc='#f7e3c8', ec='#a05a00', lw=1.5))
ax4.add_patch(Rectangle((-4,11.5), 8, 6.5, fc='#f7e3c8', ec='#a05a00', lw=1.5))
for x in (7,-7):
    ax4.plot([x,x],[0,5.5], color='#c00', lw=1.6, ls='--')
ax4.annotate('2×Ø2.2 深 5\n(舵角 M2)', xy=(7,3), xytext=(16,2), fontsize=8,
             arrowprops=dict(arrowstyle='-', lw=0.7), color='#c00')
ax4.annotate('Ø8×6.5 销\n插进盘 Ø8.2 插座', xy=(0,14), xytext=(14,16), fontsize=8,
             arrowprops=dict(arrowstyle='-', lw=0.7), color='#a05a00')
ax4.annotate('Ø18', xy=(-9,5), xytext=(-24,5), fontsize=9, color='#06c',
             arrowprops=dict(arrowstyle='-', lw=0.6))
ax4.text(0, -8, 'Ø18 × 11.5 + Ø8 × 6.5', ha='center', fontsize=9, color='#2b6cb0')
ax4.text(0, -16, '端面 x=53.5 贴舵角；销端 x=35.5', ha='center', fontsize=8, color='#555')
ax4.set_xlim(-30, 40); ax4.set_ylim(-22, 26); ax4.set_aspect('equal'); ax4.axis('off')

plt.suptitle('两轴找平云台 v2.1 — 零件图（单位 mm）', fontsize=15, y=0.98)
plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig('v21_parts.png', dpi=150, facecolor='white', bbox_inches='tight')
print('ok parts')
