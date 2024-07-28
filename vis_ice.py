import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap

def vis_sst(filename):
    # csv_path = path_name+'/'+filename
    csv_path = filename
    # 1. 读取CSV文件
    df = pd.read_csv(csv_path, header=None)  # 假设没有标题行

    # 将DataFrame转换为numpy数组
    df.replace('N', np.nan, inplace=True)
    sea_temperature = df.values.astype(float)

    # 2. 创建Basemap对象，设置中心点经度和纬度偏移
    plt.figure(figsize=(12, 6))
    m = Basemap(projection='merc', lon_0=-50, lat_0=50, llcrnrlat=-85.0511, urcrnrlat=85.0511, llcrnrlon=0,
                urcrnrlon=360)

    # 3. 绘制海温数据
    # 构造经度和纬度数组
    lons = np.linspace(-180 + 180, 180 + 180, sea_temperature.shape[1])  # 经度范围
    lats = np.linspace(-90, 90, sea_temperature.shape[0])  # 纬度范围
    lon, lat = np.meshgrid(lons, lats)  # 创建经纬度网格

    # 将经度和纬度转换为地图投影坐标
    x, y = m(lon, lat)

    # 绘制海温数据，使用颜色映射来表示海温值
    colors = [
        (1.1, "#8400FFFF"),
        (1, "#6a00FFFF"),
        (0.95, "#5900FFFF"),
        (0.9, "#4400FFFF"),
        (0.85, "#2a00FFFF"),
        (0.8, "#1900FFFF"),
        (0.75, "#0d00FFFF"),
        (0.7, "#0400FFFF"),
        (0.65, "#0015FFFF"),
        (0.6, "#1D2169FF"),
        (0.55, "#331D69FF"),
        (0.5, "#281D69FF")
    ]
    n_bins = 256

    cmap_custom = LinearSegmentedColormap.from_list("custom_temperature_cmap", [color[1] for color in colors], N=n_bins)


    # 绘制海温数据，使用自定义的颜色映射
    pcm = m.pcolormesh(x, y, sea_temperature, cmap=cmap_custom, shading='auto')
    # 设置背景透明
    fig = plt.gcf()
    fig.patch.set_alpha(0)  # 设置背景透明

    # 调整轴的背景颜色为透明
    ax = plt.gca()
    ax.patch.set_alpha(0)
    # 添加标题
    plt.axis('off')

    # 保存图像
    plt.savefig('ice_png', bbox_inches='tight', pad_inches=0, transparent=False, dpi=1000)

    # 显示图形
    plt.show()

# path_name = 'csv_output'  # 输入要获取文件的根目录
# for filename in os.listdir(path_name):
#     vis_sst(filename)

vis_sst('output_ice_csv/1981-09-21.csv')
