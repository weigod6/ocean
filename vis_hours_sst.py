import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap


def vis_sst(filename):
    csv_path = path_name+'/'+filename
    png_path = 'G:/sst_hours_png'+'/' + filename.split('.')[0] + '.png'
    # if(os.path.exists(png_path)):
    #     return
    # 1. 读取CSV文件
    df = pd.read_csv(csv_path, header=None)  # 假设没有标题行
    # df = pd.read_csv(filename, header=None)  # 假设没有标题行
    # 将DataFrame转换为numpy数组
    df.replace(0, np.nan, inplace=True)
    sea_temperature = df.values.astype(float)

    # 2. 创建Basemap对象，设置中心点经度和纬度偏移
    plt.figure(figsize=(12, 6))
    m = Basemap(projection='merc', lon_0=0, lat_0=0, llcrnrlat=-85.0511, urcrnrlat=85.0511, llcrnrlon=0,
                urcrnrlon=360)

    # 3. 绘制海温数据
    # 构造经度和纬度数组
    lons = np.linspace(1.15, 135.05, sea_temperature.shape[1])  # 经度范围
    lats = np.linspace(10, 60.25, sea_temperature.shape[0])  # 纬度范围
    lon, lat = np.meshgrid(lons, lats)  # 创建经纬度网格

    # 将经度和纬度转换为地图投影坐标
    x, y = m(lon, lat)
    vmin = -5
    vmax = 40
    # 绘制海温数据，使用颜色映射来表示海温值
    colors = [
        (40, "#281D69FF"),
        (35, "#554FAAFF"),
        (30, "#4279BFFF"),
        (25, "#4DB094FF"),
        (20, "#5BC94CFF"),
        (15, "#B7DA40FF"),
        (10, "#E1CE39FF"),
        (5, "#E09F41FF"),
        (0, "#DB6C54FF"),
        (-5, "#B73466FF"),
        (-10, "#932929FF"),
        (-15, "#6B1527FF")

    ]

    n_bins = 4096

    cmap_custom = LinearSegmentedColormap.from_list("custom_temperature_cmap", [color[1] for color in colors], N=n_bins)
    cmap_custom.set_bad(color='gray')

    # 绘制海温数据，使用自定义的颜色映射
    pcm = m.pcolormesh(x, y, sea_temperature, cmap=cmap_custom,vmin=vmin, vmax=vmax, shading='auto')

    # 添加标题
    plt.axis('off')

    # 保存图像
    plt.savefig(png_path, bbox_inches='tight', pad_inches=0, transparent=True, dpi=2000)
    # plt.show()
    plt.close()
    # 显示图形


path_name = 'G:/hours_sst'  # 输入要获取文件的根目录
for filename in os.listdir(path_name):
        vis_sst(filename)
