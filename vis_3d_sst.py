import os

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
def vis_3d_sst(input_pth,filename):
    file_pth = os.path.join(input_pth,filename)
    df = pd.read_csv(file_pth,header=None)

    output_pth = os.path.join(output_floder,input_pth.split('\\')[1])
    if not os.path.exists(output_pth):
        os.mkdir(output_pth)
    # 创建图形
    plt.figure(figsize=(12, 6))
    m = Basemap(projection='merc', lon_0=-50, lat_0=50, llcrnrlat=-85.0511, urcrnrlat=85.0511, llcrnrlon=0,
                urcrnrlon=360)
    sea_temperature = df.values.astype(float)
    lons = np.linspace(109.375+180, 117.50+180, sea_temperature.shape[1])  # 经度范围
    lats = np.linspace(11.55, 21.50, sea_temperature.shape[0])  # 纬度范围
    lon, lat = np.meshgrid(lons, lats)  # 创建经纬度网格
    x, y = m(lon, lat)
    # cmap_custom = plt.cm.coolwarm
    # cmap_custom.set_bad(color='gray')
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
    vmin = -15
    vmax = 40
    n_bins = 2048

    cmap_custom = LinearSegmentedColormap.from_list("custom_temperature_cmap", [color[1] for color in colors], N=n_bins)
    cmap_custom.set_bad(color='gray')
    pcm = m.pcolormesh(x, y, sea_temperature, cmap=cmap_custom,vmax=vmax,vmin=vmin, shading='auto')
    output_name = filename.split('.')[0]
    plt.axis('off')
    plt.savefig(f'{output_pth}/{output_name}.png', bbox_inches='tight', pad_inches=0, transparent=True, dpi=1024)

    # plt.show()
    plt.close()

input_floder = 'G:/oe_3d_data'
output_floder = 'G:/oe_3d_png'

for input_file in os.listdir(input_floder):
   input_pack = os.path.join(input_floder,input_file)
   for e in os.listdir(input_pack):
       vis_3d_sst(input_pack,e)

