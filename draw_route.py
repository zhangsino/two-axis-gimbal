import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
import numpy as np

plt.rcParams['font.family'] = 'PingFang SC'
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(15, 7), gridspec_kw={'width_ratios':[1.25,1]})

# ---------- 俯视：线路走向 ----------
ax.set_title('俯视：线束走向（① ~ ⑤）', fontsize=14, pad=10)
ax.add_patch(Circle((0,0), 52, fill=False, lw=3, color='#333'))
ax.add_patch(Circle((0,0), 40, fc='#dce9f7', ec='#2b6cb0', lw=2, zorder=2))
ax.text(0, 12, '圆盘 Ø80', ha='center', fontsize=12, color='#2b6cb0')
# 舵机1
ax.add_patch(Rectangle((52,-13), 24, 26, fc='#f6c6a0', ec='#a05000', lw=1.6, zorder=3))
ax.text(64, 0, '①', ha='center', va='center', fontsize=13, color='#7a3c00', zorder=4)
# 支点
ax.add_patch(Circle((-52,0), 4, fc='#cfd8e3', ec='#555', lw=1.2, zorder=3))
# U 腿
for sy in (1,-1):
    y0 = 52 if sy>0 else -65
    ax.add_patch(Rectangle((-8, y0), 16, 13, fc='#d6d6d6', ec='#555', lw=1.6, zorder=5))
# 舵机2
ax.add_patch(Rectangle((-13, 65), 26, 23, fc='#f6c6a0', ec='#a05000', lw=1.6, zorder=6))
ax.text(0, 76, '②', ha='center', va='center', fontsize=13, color='#7a3c00', zorder=7)

# 路径
p = [(0,0), (-26,0), (-40,0), (-52,-4), (-56,-26), (-40,-44), (-6,-52),
     (0,-46), (0,-30)]
# ① 盘 -> 1号舵机方向（在盘背面，走 X 轴负向到支点侧？这里按用户：先到 1 号电机）
# 实际走向: 盘中心 -> 盘边缘(+X, 1号舵机侧) 需绕开, 用下方路径表示
path1 = [(0,-6), (30,-6), (46,-4), (52,0)]
ax.annotate('', xy=(52,0), xytext=(30,-6),
            arrowprops=dict(arrowstyle='-|>', lw=2.4, color='#c00'))
ax.text(38, -14, '① 6050 → 1 号舵机', color='#c00', fontsize=9.5, ha='center')

# 沿外环走 (从 1 号舵机 -> 2 号舵机)，沿外环外侧
th = np.linspace(np.radians(6), np.radians(88), 60)
ax.plot(57*np.cos(th), 57*np.sin(th), ls='--', lw=2.4, color='#c00')
ax.annotate('', xy=(57*np.cos(np.radians(88)), 57*np.sin(np.radians(88))),
            xytext=(57*np.cos(np.radians(80)), 57*np.sin(np.radians(80))),
            arrowprops=dict(arrowstyle='-|>', lw=2.4, color='#c00'))
ax.text(46, 40, '② 沿外环', color='#c00', fontsize=9.5, rotation=42)

# 到 2 号舵机
ax.plot([3, 0], [57, 66], ls='--', lw=2.4, color='#c00')
ax.annotate('', xy=(0, 66), xytext=(3, 57),
            arrowprops=dict(arrowstyle='-|>', lw=2.4, color='#c00'))
ax.text(14, 62, '③ 汇入 2 号舵机', color='#c00', fontsize=9.5)

# 松弛环标记
for (x,y) in [(50,4), (3,58)]:
    ax.add_patch(Circle((x,y), 5.5, fill=False, ec='#c00', lw=1.2, ls=':'))
ax.text(56, 10, '松弛环', color='#c00', fontsize=8.5)
ax.text(9, 52, '松弛环', color='#c00', fontsize=8.5)

ax.text(0, -78, '④ 从 2 号舵机那条腿竖直下到平台 ⑤', ha='center', fontsize=10.5, color='#c00')
ax.set_xlim(-70, 82); ax.set_ylim(-84, 92); ax.set_aspect('equal'); ax.axis('off')

# ---------- 竖直下落 ----------
ax2.set_title('竖直段：沿 2 号舵机的 U 腿下行', fontsize=14, pad=10)
ax2.add_patch(Rectangle((-46, 0), 92, 6, fc='#cfcfcf', ec='#444', lw=1.6))
ax2.text(0, -8, '平台', ha='center', fontsize=10, color='#444')
# 腿
ax2.add_patch(Rectangle((-9, 6), 18, 56, fc='#d6d6d6', ec='#555', lw=1.6))
ax2.text(-16, 34, 'U 腿\n（固定）', ha='center', fontsize=9.5, color='#333')
# 舵机2
ax2.add_patch(Rectangle((-26, 62), 52, 26, fc='#f6c6a0', ec='#a05000', lw=1.6))
ax2.text(0, 75, 'MG90S ②', ha='center', va='center', fontsize=11, color='#7a3c00')
# 线：从舵机下方沿腿侧走，带固定卡与一段松弛
xs = [0, 0, 14, 14, 12, 12, 12]
ys = [62, 56, 52, 40, 34, 20, 7]
ax2.plot(xs, ys, ls='-', lw=2.6, color='#c00')
ax2.annotate('', xy=(12, 7), xytext=(12, 20),
             arrowprops=dict(arrowstyle='-|>', lw=2.6, color='#c00'))
for y in (50, 26):
    ax2.add_patch(Rectangle((10, y-2), 6, 4, fc='#888', ec='none'))
ax2.text(22, 50, '扎带/卡槽固定', fontsize=8.5, color='#555')
ax2.text(22, 33, '松弛段', fontsize=8.5, color='#c00')
ax2.text(0, 92, '2 号舵机机身不动 → 这一段全程不跨关节', ha='center', fontsize=10, color='#c00')
ax2.set_xlim(-50, 55); ax2.set_ylim(-14, 98); ax2.set_aspect('equal'); ax2.axis('off')

plt.tight_layout()
plt.savefig('gimbal_route.png', dpi=160, facecolor='white')
print('ok')
