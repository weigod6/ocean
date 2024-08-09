import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
# 读取CSV文件
def vis_heatwave(file_pth) :
    file_pth = os.path.join(file_pack,file_pth)
    data = pd.read_csv(file_pth, header=None)  # 修改为你的文件名

    plt.figure(figsize=(12, 6))
    m = Basemap(projection='merc', lon_0=-50, lat_0=50, llcrnrlat=-85.0511, urcrnrlat=85.0511, llcrnrlon=0,
                urcrnrlon=360)
    data.replace(0, np.nan, inplace=True)
    level = np.floor(data)
    # print(level)
    # 3. 绘制海温数据
    # 构造经度和纬度数组
    lons = np.linspace(-180 + 180, 180 + 180, level.shape[1])  # 经度范围
    lats = np.linspace(-90, 90, level.shape[0])  # 纬度范围
    lon, lat = np.meshgrid(lons, lats)  # 创建经纬度网格

    # 将经度和纬度转换为地图投影坐标
    x, y = m(lon, lat)

    colors_map = [
        (1, "#ffa841"),
        (2, "#b34400"),
        (3, "#b32000"),
        (4, "#ef0e00"),
        (5, "#3c0400")
    ]
    cmap_custom = LinearSegmentedColormap.from_list("custom_temperature_cmap", [color[1] for color in colors_map])
    cmap_custom.set_bad(color='w')
    plt.axis('off')
    pcm = m.pcolormesh(x, y, level, cmap=cmap_custom, shading='auto')
    plt.savefig(f"F:{file_pth.split('.')[0]}.png", bbox_inches='tight', pad_inches=0, transparent=False, dpi=2000)

    # 显示图像
    # plt.show()
    plt.close()

file_pack = 'heatwave_data'
for e in os.listdir(file_pack):
    vis_heatwave(e)