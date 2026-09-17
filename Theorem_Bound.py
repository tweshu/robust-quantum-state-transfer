import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, Normalize
from mpl_toolkits.mplot3d import Axes3D

mpl.rcParams.update({
    'font.size': 16,         
    'axes.labelsize': 18,     
})

q = np.linspace(0, 1, 200)
f = np.linspace(0, 1, 1000)**15
Q, F = np.meshgrid(q, f)

# Function
Z = 2 * (F ** Q)

norm = Normalize(vmin=0, vmax=2)

ls = LightSource(azdeg=320, altdeg=65)
rgb = ls.shade(
    Z,
    cmap=plt.cm.viridis,
    norm=norm,
    vert_exag=0.4,
    blend_mode='soft'
)

alpha = 0.8  

rgba = rgb.copy()         
rgba[..., 3] = alpha       

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')


surf = ax.plot_surface(
    F, Q, Z,
    facecolors=rgba,
    rstride=2,
    cstride=2,
    linewidth=0,
    edgecolor='none',
    antialiased=False,
    shade=False
)

ax.set_xlim(0, 1)   # f
ax.set_ylim(1, 0)   # q
ax.set_zlim(0, 2)

ax.set_xlabel(r'$|\mathcal{S}|/2^{L-1}$', labelpad=10)
ax.set_ylabel(r'$1/p$', labelpad=10)

ax.view_init(elev=28, azim=230)

dz = 0.4
levels = np.arange(0.0+dz, 2.0 + 1e-9-dz,dz )  # 0, 0.4,..., 2.0

ax.contour(
    F, Q, Z+1e-3,
    levels=levels,
    colors='black',  
    linewidths=1.2,
    alpha=1
)



ridge_color = plt.cm.viridis(norm(2))
eps = 1e-3
dash_style = (0, (2.2, 2.2))

ax.plot(
    np.ones_like(q), q, (2 + eps) * np.ones_like(q),
    color=ridge_color,
    linewidth=4,
    solid_capstyle='round'
)

ax.plot(
    np.ones_like(q), q, (2 + eps) * np.ones_like(q),
    color='black',
    linewidth=2.0,
    linestyle=dash_style,
    alpha=0.75
)

ax.plot(
    f, np.zeros_like(f), (2 + eps) * np.ones_like(f),
    color=ridge_color,
    linewidth=4,
    solid_capstyle='round'
)

ax.plot(
    f, np.zeros_like(f), (2 + eps) * np.ones_like(f),
    color='black',
    linewidth=2.0,
    linestyle=dash_style,
    alpha=0.75
)


for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.set_pane_color((0.97, 0.97, 0.97, 1.0))
    axis._axinfo["grid"]['color'] = (0.75, 0.75, 0.75, 0.45)
    axis._axinfo["grid"]['linewidth'] = 0.6

ax.tick_params(colors='0.25', labelsize=16)

ax.set_zticks([0, 0.4, 0.8, 1.2, 1.6, 2.0])

mappable = plt.cm.ScalarMappable(norm=norm, cmap='viridis')
mappable.set_array(Z)
cbar = fig.colorbar(mappable, ax=ax, shrink=0.55, aspect=12)
cbar.set_label('lower bound')
cbar.set_ticks([0, 1, 2])
cbar.ax.tick_params(labelsize=15)

plt.tight_layout()
plt.show()