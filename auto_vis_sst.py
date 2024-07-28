import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import schedule
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
import time

from scipy.ndimage import zoom


def vis_sst(filename):
    csv_path = path_name+'/'+filename
    png_path = 'recent_sst_png/' + filename.split('.')[0] + '.png'
    if(os.path.exists(png_path)):
        return
    # 1. 读取CSV文件
    df = pd.read_csv(csv_path, header=None)  # 假设没有标题行
    # data = pd.read_csv(csv_path, header=None).values
    #
    # # 处理缺失值（N表示的部分）
    # data[data == 'N'] = np.nan
    # data = data.astype(float)

    # # 创建掩码，标记非缺失值的位置
    # mask = ~np.isnan(data)
    #
    # # 使用掩码和最近邻插值方法填充缺失值
    # data_filled = np.where(mask, data, 0)
    # zoom_factor = 4
    #
    # # 放大掩码和填充后的数据
    # data_filled_zoom = zoom(data_filled, zoom_factor, order=1)
    # mask_zoom = zoom(mask.astype(float), zoom_factor, order=0)
    #
    # # 使用掩码将无效值再次标记为NaN
    # interpolated_data = np.where(mask_zoom, data_filled_zoom, np.nan)
    #
    # # 降低数据精度并保留两位小数
    # interpolated_data = np.around(interpolated_data.astype(np.float32), decimals=2)
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
    n_bins = 256

    cmap_custom = LinearSegmentedColormap.from_list("custom_temperature_cmap", [color[1] for color in colors], N=n_bins)
    cmap_custom.set_bad(color='gray')

    # 绘制海温数据，使用自定义的颜色映射
    pcm = m.pcolormesh(x, y, sea_temperature, cmap=cmap_custom, shading='auto')

    # 添加标题
    plt.axis('off')

    # 保存图像
    plt.savefig(png_path, bbox_inches='tight', pad_inches=0, transparent=False, dpi=2000)
    print("vis"+png_path)
    plt.close()
    # 显示图形


path_name = 'recent_output_csv'  # 输入要获取文件的根目录

for filename in os.listdir(path_name):
    vis_sst(filename)

print("更新图片完成！")