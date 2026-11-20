# -*- coding: utf-8 -*-
"""云台 v2 装配图（示意但尺寸可核）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.lines import Line2D

plt.rcParams['font.family'] = 'PingFang SC'
fig = plt.figure(figsize=(17, 10.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1], width_ratios=[1.05, 1],
                      hspace=0.18, wspace=0.12)
axT = fig.add_subplot(gs[0, 0])   # 俯视
axF = fig.add_subplot(gs[0, 1])   # 正视
axN = fig.add_subplot(gs[1, :])   # 说明/尺寸表

def dim_h(ax, x0, x1, y, text, off=0, fs=8):
    ax.annotate('', xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<|-|>', lw=0.8, color='#06c'))
    ax.text((x0+x1)/2, y+off, text, ha='center', va='bottom', fontsize=fs, color='#06c')

def dim_v(ax, y0, y1, x, text, off=0, fs=8):
    ax.annotate('', xy=(x, y0), xytext=(x, y1),
                arrowprops=dict(arrowstyle='<|-|>', lw=0.8, color='#06c'))
    ax.text(x+off, (y0+y1)/2, text, ha='left', va='center', fontsize=fs, color='#06c',
            rotation=90)

# ================= 俯视图 =================
axT.set_title('俯视（Z↑，轴向 X 指向右）', fontsize=13)
axT.add_patch(Circle((0,0), 54, fill=False, lw=2.6, color='#222'))
axT.add_patch(Circle((0,0), 40, fc='#dce9f7', ec='#2b6cb0', lw=1.8, zorder=2))
axT.add_patch(Circle((0,0), 44, fill=False, lw=0.8, ls='--', color='#888'))
# 舵机①（+X）
axT.add_patch(Rectangle((54, -11.95), 22.5, 23.9, fc='#f6c6a0', ec='#a05000', lw=1.4, zorder=4))
axT.add_patch(Rectangle((54, -16.3), 2.8, 32.6, fc='#fbd9bc', ec='#a05000', lw=1.0, zorder=3))
axT.text(65, 0, 'MG90S ①', ha='center', va='center', fontsize=9, color='#7a3c00', zorder=5)
# 舵机②（+Y）
axT.add_patch(Rectangle((-11.95, 77), 23.9, 22.5, fc='#f6c6a0', ec='#a05000', lw=1.4, zorder=4))
axT.add_patch(Rectangle((-16.3, 70), 32.6, 2.8, fc='#fbd9bc', ec='#a05000', lw=1.0, zorder=3))
axT.text(0, 88, 'MG90S ②', ha='center', va='center', fontsize=9, color='#7a3c00', zorder=5)
axT.text(-96, 100, '舵机②：轴沿 −Y\n机身 77→99.5', ha='left', fontsize=7.5, color='#a05000')
# 腿
for sy in (1,-1):
    y0 = 62 if sy>0 else -70
    axT.add_patch(Rectangle((-22, y0), 44, 8, fc='#d6d6d6', ec='#555', lw=1.4, zorder=5))
# 耳板
for sy in (1,-1):
    axT.add_patch(Rectangle((50, 12*sy if sy>0 else -17), 10, 5, fc='#e8e8e8', ec='#555', lw=1.0, zorder=6))
axT.text(55, 20, '耳板 6 厚', fontsize=8, color='#555')
# 轴
axT.plot([-70, 80], [0,0], lw=0.9, ls='-.', color='#c00')
axT.plot([0,0], [-72, 105], lw=0.9, ls='-.', color='#0a0')
axT.text(78, 3, 'X', color='#c00', fontsize=11)
axT.text(3, 100, 'Y', color='#0a0', fontsize=11)
# 尺寸
dim_h(axT, -54, 54, -86, 'Ø108', off=1.5)
dim_h(axT, -16.3, 16.3, 106, '32.6 翼展', off=1.5)
dim_v(axT, 0, 99.5, 96, '99.5', off=1.2)
dim_v(axT, 0, 76.5, 86, '76.5', off=1.2)
axT.text(0, 6, '盘 Ø80', ha='center', fontsize=9.5, color='#2b6cb0')
axT.text(-4, -104, '总 X 137（−60 … +76.5）   总 Y 170（−70 … +99.5）', ha='center', fontsize=8.5, color='#06c')
axT.set_xlim(-100, 110); axT.set_ylim(-112, 124); axT.set_aspect('equal'); axT.axis('off')

# ================= 正视图 =================
axF.set_title('正视（沿 −Y，Z↑）', fontsize=13)
axF.add_patch(Rectangle((-75, 0), 150, 6, fc='#cfcfcf', ec='#444', lw=1.6))
for sx in (1,-1):
    x0 = -22 if sx>0 else 22
    axF.add_patch(Rectangle((-22 if sx<0 else 22, 6), 0, 0, fc='none'))  # placeholder
axF.add_patch(Rectangle((-22, 6), 44, 54, fc='#d6d6d6', ec='#555', lw=1.6))
axF.text(-40, 30, 'U 腿\n(前后重合)', fontsize=8.5, color='#333', ha='center')
# 环（侧视=矩形环）
axF.add_patch(Rectangle((-54, 55), 108, 10, fc='#e8e8e8', ec='#222', lw=2.0))
axF.text(-52, 68.5, '外环 Ø108/Ø88，t=10', fontsize=8.5, color='#333')
# 盘
axF.add_patch(Rectangle((-40, 56), 80, 4, fc='#dce9f7', ec='#2b6cb0', lw=1.4))
# 6050
axF.add_patch(Rectangle((-11, 54.4), 22, 1.6, fc='#9ae6b4', ec='#276749', lw=1.0))
axF.text(-16, 51.5, 'MPU6050（盘背）', fontsize=8, ha='center', color='#276749')
# 舵机①（侧视：高 22.5 沿 X）
axF.add_patch(Rectangle((54, 48.4), 22.5, 12.7, fc='#f6c6a0', ec='#a05000', lw=1.4))
axF.add_patch(Rectangle((54, 36), 2.8, 32.6, fc='#fbd9bc', ec='#a05000', lw=1.0))
axF.text(65, 54.7, '①', fontsize=9, ha='center', va='center', color='#7a3c00')
axF.annotate('', xy=(50, 60), xytext=(54, 60), arrowprops=dict(arrowstyle='-|>', lw=1.4, color='#a05000'))
axF.text(52, 62.5, '舵角', fontsize=7.5, ha='center', color='#a05000', rotation=90)
# 高度尺寸
dim_v(axF, 0, 60, -88, '60 轴高', off=1.2)
dim_v(axF, 0, 67, -78, '67 总高', off=1.2)
dim_h(axF, -75, 75, -10, '150 底板', off=-6)
axF.text(-6, 78, '盘 Z=56…60（轴心 60）', ha='center', fontsize=8.5, color='#2b6cb0')
axF.set_xlim(-100, 100); axF.set_ylim(-16, 80); axF.set_aspect('equal'); axF.axis('off')

# ================= 说明 =================
axN.axis('off')
rows = [
    ['项目', '数值 / 说明'],
    ['外形包络', '137 (X) × 170 (Y) × 67 (Z) mm —— 200 以内'],
    ['内盘', 'Ø80 × 4；+X 耳轴 Ø14 面止于 X=50（贴舵角），−X 耳轴 Ø12 内 Ø3.15 衬套孔'],
    ['外环', 'ID88 / OD108，厚 10；+X 让位缺口 ±12；+X 耳板 6 厚（X 50…60）'],
    ['±Y 耳轴', 'Ø12，伸到 Y=70：+Y 端面锁舵角；−Y 端面 M3 螺钉 + 热熔螺母'],
    ['U 架', '底板 150×150×6；腿 44×8，顶面 Z=60；+Y 腿外侧垫板 7 厚装舵机②'],
    ['俯仰轴 / 横滚轴', 'X 轴、Y 轴：均过 (0,0,60)，正交相交（必须）'],
    ['轴向定位', '+X / +Y 由舵角面限位；−X / −Y 用 M3 螺钉压住轴肩'],
    ['轴承', 'Ø3 钢轴 + 打印衬套（Ø3.15），配合长 10；预留 683ZZ（Ø7×3×3）坑位'],
    ['打印姿态', '盘平放（耳轴横置）；环平放；架底板贴床、腿竖起'],
    ['材料', 'PLA（测试）；壁厚 ≥4 圈；耳板/耳轴根部 R2 圆角'],
    ['五金', 'M2×8 自攻 ×4（舵角）；M2×6 ×2（舵角中心）；M3×20 ×2 + 热熔螺母 ×2；Ø3×20 钢轴 ×2'],
]
tbl = axN.table(cellText=rows[1:], colLabels=rows[0], loc='center', cellLoc='left',
                colWidths=[0.16, 0.8])
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 1.45)
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor('#999')
    if r == 0:
        cell.set_facecolor('#e8eef7')
        cell.set_text_props(weight='bold')

plt.suptitle('两轴找平云台 v2 — 装配图（尺寸单位 mm，示意比例）', fontsize=16, y=0.98)
plt.savefig('gimbal_drawing_v2.png', dpi=150, facecolor='white', bbox_inches='tight')
print('saved gimbal_drawing_v2.png')
