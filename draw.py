import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

plt.rcParams['font.family'] = 'PingFang SC'
plt.rcParams['axes.unicode_minus'] = False

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.2), gridspec_kw={'width_ratios':[1.15,1]})

ax1.set_title('俯视图（沿 Z 向下看）', fontsize=15, pad=12)
R_DISC, R_RING_IN, R_RING_OUT = 40, 45, 52
ax1.add_patch(Circle((0,0), R_RING_OUT, fill=False, lw=3.2, color='#333'))
ax1.add_patch(Circle((0,0), R_RING_IN, fill=False, lw=1.2, color='#888', ls='--'))
ax1.add_patch(Circle((0,0), R_DISC, fill=True, fc='#dce9f7', ec='#2b6cb0', lw=2.2, zorder=2))
ax1.text(0, 6, '圆盘 Ø80', ha='center', fontsize=13, color='#2b6cb0')
ax1.text(0, -8, '（背面贴 MPU6050）', ha='center', fontsize=10, color='#2b6cb0')

ax1.add_patch(Rectangle((R_RING_OUT, -13), 23, 26, fc='#f6c6a0', ec='#a05000', lw=1.8, zorder=3))
ax1.text(R_RING_OUT+11.5, 0, 'MG90S\n①', ha='center', va='center', fontsize=10, color='#7a3c00')
ax1.plot([R_DISC, R_RING_OUT+3], [0,0], color='#a05000', lw=2.4, zorder=4)
ax1.text(R_RING_OUT+13, 17, 'X 轴驱动', fontsize=9.5, color='#a05000')

ax1.add_patch(Circle((-R_RING_OUT, 0), 4, fc='#cfd8e3', ec='#555', lw=1.5, zorder=3))
ax1.text(-R_RING_OUT, -11, '支点\n（钢轴+衬套）', ha='center', fontsize=9, color='#444')

for sy, lab in ((1,'U 形架臂（+Y，装舵机②）'), (-1,'U 形架臂（−Y，轴+轴承）')):
    y0 = R_RING_OUT if sy>0 else -R_RING_OUT-9
    ax1.add_patch(Rectangle((-9, y0), 18, 9, fc='#d6d6d6', ec='#555', lw=1.8, zorder=5))
    ax1.text(0, (R_RING_OUT+4.5) if sy>0 else (-R_RING_OUT-4.5), lab, ha='center', fontsize=9, color='#333')

ax1.add_patch(Rectangle((-13, R_RING_OUT+9), 26, 23, fc='#f6c6a0', ec='#a05000', lw=1.8, zorder=6))
ax1.text(0, R_RING_OUT+20.5, 'MG90S ②', ha='center', va='center', fontsize=10, color='#7a3c00')

ax1.annotate('X', xy=(70,0), xytext=(64,0), fontsize=14, color='#c00',
             arrowprops=dict(arrowstyle='-|>', lw=2, color='#c00'))
ax1.annotate('Y', xy=(0,70), xytext=(0,64), fontsize=14, color='#0a0',
             arrowprops=dict(arrowstyle='-|>', lw=2, color='#0a0'))
ax1.set_xlim(-78, 82); ax1.set_ylim(-80, 84); ax1.set_aspect('equal'); ax1.axis('off')

ax2.set_title('侧视图（沿 −Y 看）', fontsize=15, pad=12)
ax2.add_patch(Rectangle((-60, 0), 120, 6, fc='#cfcfcf', ec='#444', lw=1.8))
ax2.text(50, 3, '平台', fontsize=10, va='center', color='#333')
ax2.add_patch(Rectangle((-52, 6), 10, 46, fc='#d6d6d6', ec='#555', lw=1.8))
ax2.text(-47, 29, 'U 支腿', fontsize=9, rotation=90, ha='center', va='center', color='#333')
ax2.add_patch(Rectangle((-46, 52), 92, 10, fc='none', ec='#333', lw=3))
ax2.text(0, 57, '外环', fontsize=10, ha='center', va='center', color='#333')
ax2.plot([-46, -40], [57, 57], color='#555', lw=3)
ax2.text(-58, 66, 'Y 轴', fontsize=10, color='#0a0')
ax2.add_patch(Rectangle((-38, 54.5), 76, 5, fc='#dce9f7', ec='#2b6cb0', lw=1.6))
ax2.text(0, 47, '圆盘（边缘看）', fontsize=9.5, ha='center', color='#2b6cb0')
ax2.add_patch(Rectangle((-11, 50.5), 22, 4, fc='#9ae6b4', ec='#276749', lw=1.4))
ax2.text(0, 45.5, 'MPU6050', fontsize=8.5, ha='center', color='#276749')
ax2.add_patch(Rectangle((32, 48), 24, 26, fc='#f6c6a0', ec='#a05000', lw=1.8))
ax2.text(44, 61, 'MG90S ①', fontsize=9, ha='center', va='center', color='#7a3c00')
xs = [-6, 30, 36, 40, 10, -6, -40, -47, -47]
ys = [50, 50, 58, 70, 74, 74, 74, 74, 8]
ax2.plot(xs, ys, ls='--', lw=1.8, color='#c00')
ax2.annotate('', xy=(-47, 10), xytext=(-47, 66),
             arrowprops=dict(arrowstyle='-|>', lw=1.8, color='#c00', ls='--'))
ax2.text(-22, 77, '线束：6050 → ① → 沿环 → ② → 沿 U 支腿 → 平台', fontsize=9, color='#c00', ha='center')
ax2.set_xlim(-72, 78); ax2.set_ylim(-6, 88); ax2.set_aspect('equal'); ax2.axis('off')

plt.tight_layout()
plt.savefig('gimbal_concept.png', dpi=160, facecolor='white')
print('saved')
