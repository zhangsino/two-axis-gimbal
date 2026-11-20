import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

plt.rcParams['font.family'] = 'PingFang SC'
fig = plt.figure(figsize=(13, 9))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('整体结构（示意）：线束从 2 号舵机那条腿下来', fontsize=15, pad=0)

def box(x0,x1,y0,y1,z0,z1,color,alpha=1.0,edge='#333'):
    v = np.array([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],
                  [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]])
    f = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
    ax.add_collection3d(Poly3DCollection(v[f], facecolors=color, alpha=alpha,
                                        edgecolors=edge, linewidths=1.2))

def circle(r,z,n=120):
    t = np.linspace(0,2*np.pi,n)
    return np.c_[r*np.cos(t), r*np.sin(t), np.full(n,z)]

# 底板
box(-70,70,-70,70,0,6,'#cfcfcf')
# U 支腿（±Y）
box(-8,8,54,65,6,62,'#d6d6d6')
box(-8,8,-65,-54,6,62,'#d6d6d6')
# 外环（上下两圈 + 少量竖线示意环体）
for z in (62,71):
    ax.plot(*circle(52,z).T, color='#222', lw=2.2)
    ax.plot(*circle(45,z).T, color='#666', lw=1.0, ls='--')
for a in np.linspace(0,2*np.pi,13)[:-1]:
    ax.plot([52*np.cos(a)]*2,[52*np.sin(a)]*2,[62,71], color='#222', lw=0.9)
# 圆盘
for z in (63.5,68):
    ax.plot(*circle(40,z).T, color='#2b6cb0', lw=1.4)
t = np.linspace(0,2*np.pi,120)
ax.add_collection3d(Poly3DCollection([np.c_[40*np.cos(t),40*np.sin(t),np.full(120,68)]],
                                     facecolors='#dce9f7', alpha=0.75, edgecolors='#2b6cb0'))
# 6050
box(-11,11,-8,8,64.5,68,'#9ae6b4',0.95)
# 舵机1（+X 侧）
box(52,76,-13,13,44,74,'#f6c6a0',0.95)
# 舵机2（+Y 侧）
box(-13,13,65,88,44,74,'#f6c6a0',0.95)

# 线束
pts = np.array([[0,0,69],[-30,0,69],[-42,0,69],[-56,0,68],[-44,36,68],[-14,55,68],
                [0,60,68],[0,60,40],[0,60,12]])
ax.plot(pts[:,0],pts[:,1],pts[:,2], color='#c00', lw=2.6, ls='--')
ax.scatter(pts[-1,0],pts[-1,1],pts[-1,2], color='#c00', s=40)

ax.text(0,0,84,'圆盘 Ø80 + 6050', color='#2b6cb0', fontsize=11, ha='center')
ax.text(64,0,80,'MG90S ①\n(X 轴)', color='#a05000', fontsize=10, ha='center')
ax.text(0,80,80,'MG90S ②\n(Y 轴)', color='#a05000', fontsize=10, ha='center')
ax.text(0,70,25,'线束沿此腿下行\n（该腿固定，不跨关节）', color='#c00', fontsize=10, ha='center')

ax.set_xlim(-80,90); ax.set_ylim(-80,95); ax.set_zlim(0,100)
ax.set_box_aspect((1.6,1.7,1.1))
ax.view_init(elev=22, azim=-58)
ax.set_axis_off()
plt.tight_layout()
plt.savefig('gimbal_iso.png', dpi=160, facecolor='white')
print('ok')
