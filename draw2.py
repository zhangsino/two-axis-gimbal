import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

plt.rcParams['font.family'] = 'PingFang SC'
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_title('侧视图（沿 −Y 方向看）：X 轴俯仰 / Y 轴横滚', fontsize=15, pad=10)

# 平台
ax.add_patch(Rectangle((-70, 0), 140, 7, fc='#cfcfcf', ec='#444', lw=1.8))
ax.annotate('平台（底板）', xy=(45, 7), xytext=(45, 16), fontsize=11, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#666'))
# U 支腿（左侧，静态）
ax.add_patch(Rectangle((-62, 7), 11, 55, fc='#d6d6d6', ec='#555', lw=1.8))
ax.annotate('U 支腿\n（固定）', xy=(-56.5, 40), xytext=(-92, 44), fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#666'))
# 外环截面（绕 Y 轴转）
ax.add_patch(Rectangle((-51, 62), 104, 9, fc='#e8e8e8', ec='#333', lw=2.4))
ax.annotate('外环（绕 Y 轴转动）', xy=(30, 71), xytext=(38, 84), fontsize=11, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#666'))
# Y 轴枢（左端）
ax.add_patch(Circle((-51, 66.5), 3.2, fc='#9aa8b8', ec='#333', lw=1.4, zorder=5))
ax.annotate('Y 轴枢（钢轴+轴承）', xy=(-51, 66.5), xytext=(-88, 78), fontsize=9.5, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#666'))
# 圆盘（边缘看）
ax.add_patch(Rectangle((-40, 63.5), 80, 4.5, fc='#dce9f7', ec='#2b6cb0', lw=1.8, zorder=4))
ax.annotate('圆盘（绕 X 轴俯仰，X 垂直于纸面）', xy=(0, 63.5), xytext=(-2, 36), fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#2b6cb0'), color='#2b6cb0')
# 6050
ax.add_patch(Rectangle((-11, 58.5), 22, 5, fc='#9ae6b4', ec='#276749', lw=1.4, zorder=5))
ax.annotate('MPU6050（盘背面）', xy=(12, 61), xytext=(38, 44), fontsize=9.5, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#276749'), color='#276749')
# 舵机1（右侧，跟外环一起绕 Y 转）
ax.add_patch(Rectangle((53, 47), 26, 30, fc='#f6c6a0', ec='#a05000', lw=1.9, zorder=6))
ax.annotate('MG90S ①\n驱动 X 轴\n（固定在外环上）', xy=(66, 77), xytext=(78, 92), fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#a05000'), color='#7a3c00')
ax.plot([53, 44], [62, 65.8], color='#a05000', lw=2.6, zorder=7)   # 轴伸到盘边
# 舵机2（在 -Y 臂后面，用虚线示意）
ax.add_patch(Rectangle((-70, 47), 8, 22, fc='none', ec='#a05000', lw=1.6, ls='--'))
ax.annotate('MG90S ②（在图后侧，驱动 Y 轴）', xy=(-66, 58), xytext=(-98, 30), fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='-', lw=0.9, color='#a05000'), color='#7a3c00')
# 线束
pts = [(-8, 58.5), (-18, 52), (-40, 50), (-56, 52), (-56, 20), (-56, 12)]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
ax.plot(xs, ys, ls='--', lw=2, color='#c00')
ax.annotate('', xy=(-56, 9), xytext=(-56, 20), arrowprops=dict(arrowstyle='-|>', lw=2, color='#c00'))
ax.annotate('线束：6050 → ① → 沿外环 → ② → 沿 U 支腿 → 平台', xy=(-40, 50), xytext=(-46, 24),
            fontsize=9.5, color='#c00', ha='center')

ax.set_xlim(-105, 100); ax.set_ylim(-6, 100)
ax.set_aspect('equal'); ax.axis('off')
plt.tight_layout()
plt.savefig('gimbal_side.png', dpi=160, facecolor='white')
print('ok')
