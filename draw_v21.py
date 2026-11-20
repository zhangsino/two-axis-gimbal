# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import numpy as np

plt.rcParams['font.family'] = 'PingFang SC'
C_RING, C_DISC, C_FR, C_HUB = '#e8e8e8', '#dce9f7', '#d6d6d6', '#f7e3c8'
E = '#222'


def dim_h(ax, x0, x1, y, t, fs=8, up=True):
    ax.annotate('', xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<|-|>', lw=0.7, color='#06c'))
    ax.text((x0 + x1) / 2, y + (2 if up else -5), t, ha='center', va='bottom', fontsize=fs, color='#06c')


def dim_v(ax, y0, y1, x, t, fs=8):
    ax.annotate('', xy=(x, y0), xytext=(x, y1),
                arrowprops=dict(arrowstyle='<|-|>', lw=0.7, color='#06c'))
    ax.text(x + 1.5, (y0 + y1) / 2, t, ha='left', va='center', fontsize=fs, color='#06c', rotation=90)


# ==================================================== 图 1：总装
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(16, 8))
ax.set_title('总装 · 俯视（Z↑）', fontsize=13)
ax.add_patch(Circle((0, 0), 54, fill=False, lw=2.6, color=E))
ax.add_patch(Circle((0, 0), 44, fill=False, lw=0.8, ls='--', color='#888'))
ax.add_patch(Circle((0, 0), 40, fc=C_DISC, ec='#2b6cb0', lw=1.6, zorder=2))
ax.add_patch(Rectangle((42, -9), 11.5, 18, fc=C_HUB, ec='#a05a00', lw=1.3, zorder=3))
ax.text(30, 24, 'Hub Ø18', fontsize=7.5, color='#a05a00', ha='center')
ax.add_patch(Rectangle((60, -11.95), 22.5, 23.9, fc='#f6c6a0', ec='#a05000', lw=1.3, zorder=4))
ax.add_patch(Rectangle((60, -16.3), 2.8, 32.6, fc='#fbd9bc', ec='#a05000', lw=0.9, zorder=3))
ax.text(71, 0, 'MG90S ①', fontsize=8.5, ha='center', va='center', color='#7a3c00')
ax.add_patch(Rectangle((-11.95, 69), 23.9, 22.5, fc='#f6c6a0', ec='#a05000', lw=1.3, zorder=4))
ax.add_patch(Rectangle((-16.3, 69), 32.6, 2.8, fc='#fbd9bc', ec='#a05000', lw=0.9, zorder=3))
ax.text(0, 80, 'MG90S ②', fontsize=8.5, ha='center', va='center', color='#7a3c00')
for sy, y0 in ((1, 54.5), (-1, -62.5)):
    ax.add_patch(Rectangle((-22, y0), 44, 8, fc=C_FR, ec='#555', lw=1.3, zorder=5))
for sy in (1, -1):
    y0 = 11 if sy > 0 else -17
    ax.add_patch(Rectangle((50, y0), 10, 6, fc='#efefef', ec='#555', lw=0.9, zorder=6))
ax.plot([-62, 88], [0, 0], lw=0.8, ls='-.', color='#c00')
ax.plot([0, 0], [-72, 96], lw=0.8, ls='-.', color='#0a0')
ax.text(86, 3, 'X', color='#c00', fontsize=11)
ax.text(3, 92, 'Y', color='#0a0', fontsize=11)
dim_h(ax, -54, 54, -78, 'Ø108')
dim_h(ax, -54, 82.5, 100, '136.5')
dim_v(ax, -69, 91.5, 92, '160.5')
ax.text(0, -92, '包络  136.5 × 160.5 × 78', ha='center', fontsize=9.5, color='#06c')
ax.set_xlim(-70, 100); ax.set_ylim(-100, 106); ax.set_aspect('equal'); ax.axis('off')

ax2.set_title('总装 · 正视（沿 −Y，Z↑）', fontsize=13)
ax2.add_patch(Rectangle((-65, 0), 130, 6, fc=C_FR, ec='#444', lw=1.5))
ax2.add_patch(Rectangle((-22, 6), 44, 64, fc=C_FR, ec='#555', lw=1.4))
ax2.add_patch(Rectangle((-54, 64), 108, 10, fc=C_RING, ec=E, lw=2))
ax2.add_patch(Rectangle((-40, 63), 80, 4, fc=C_DISC, ec='#2b6cb0', lw=1.3))
ax2.add_patch(Rectangle((42, 61), 11.5, 18, fc=C_HUB, ec='#a05a00', lw=1.2))
ax2.add_patch(Rectangle((50, 64), 10, 14, fc='#efefef', ec='#555', lw=1.0))
ax2.add_patch(Rectangle((60, 63.65), 22.5, 12.7, fc='#f6c6a0', ec='#a05000', lw=1.3))
ax2.add_patch(Rectangle((60, 53.7), 2.8, 32.6, fc='#fbd9bc', ec='#a05000', lw=0.8))
ax2.plot([-54, 54], [70, 70], lw=0.8, ls='-.', color='#c00')
ax2.text(-30, 80, 'X 轴 Z=70', fontsize=8, color='#c00')

dim_v(ax2, 0, 70, -80, '70')
dim_v(ax2, 0, 78, -70, '78')
dim_h(ax2, -65, 65, -12, '130 底板', up=False)
ax2.text(0, 84, '腿根 R4 · 腿孔 Ø12.3 @Z=70', ha='center', fontsize=8.5, color='#555')
ax2.set_xlim(-92, 90); ax2.set_ylim(-18, 92); ax2.set_aspect('equal'); ax2.axis('off')
plt.tight_layout()
plt.savefig('v21_assembly.png', dpi=150, facecolor='white', bbox_inches='tight')
print('ok assembly')
