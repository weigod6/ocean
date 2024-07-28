import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
# 创建 Basemap 对象，设置中心点经度和纬度偏移
plt.figure(figsize=(12, 6))
m = Basemap(projection='merc', lon_0=-50, lat_0=50, llcrnrlat=-85.0511, urcrnrlat=85.0511, llcrnrlon=-180, urcrnrlon=180, resolution='i')

# 绘制海岸线和国界
m.drawcoastlines(linewidth=0.05, antialiased=True, linestyle='solid', color='w', zorder=10)
m.drawcountries()

# 填充陆地颜色为灰色，并将湖泊也设为透明
m.fillcontinents(color='gray', lake_color='gray', zorder=0)

# 构造经度和纬度数组
lons = np.linspace(-180, 180, 1440)  # 经度范围
lats = np.linspace(-90, 90, 720)    # 纬度范围
lon, lat = np.meshgrid(lons, lats)  # 创建经纬度网格

# 将经度和纬度转换为地图投影坐标
x, y = m(lon, lat)

# 设置背景透明
fig = plt.gcf()
fig.patch.set_alpha(0)  # 设置背景透明

# 调整轴的背景颜色为透明
ax = plt.gca()
ax.patch.set_alpha(0)
plt.axis('off')
# # 保存图像
# plt.savefig('1000.png', bbox_inches='tight', pad_inches=0, transparent=True, dpi=2000)

# 显示图形
plt.show()
