import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def plot_global_temperature(csv_file_path):
    # 读取 gzipped CSV 文件
    df = pd.read_csv(csv_file_path, header=None, low_memory=False)


    # 将 'N' 替换为 NaN
    # df.replace('N', np.nan, inplace=True)
    # df= df.where(df>=-2)
    # # 将数据转换为浮点数
    # data = df.values.astype(float)
    # data = data.round(2)
    # print(data)
    data = df.values
    # 设置颜色映射范围
    vmin = 0  # 最小温度值，可以根据实际数据范围调整
    vmax = 11  # 最大温度值，可以根据实际数据范围调整

    # 准备绘图
    plt.figure(figsize=(12, 6))

    # 创建图像
    # cmap_custom = plt.cm.coolwarm
    # cmap_custom.set_bad(color='gray')

    cmap = plt.get_cmap('OrRd',10)
    cmap.set_bad(color='black')  # 设置缺失值为黑色
    colors = [
        (34, "#281D69FF"),
        (32, "#554FAAFF"),
        (28, "#4279BFFF"),
        (24, "#4DB094FF"),
        (20, "#5BC94CFF"),
        (16, "#B7DA40FF"),
        (12, "#E1CE39FF"),
        (10, "#E09F41FF"),
        (8, "#DB6C54FF"),
        (4, "#B73466FF"),
        (0, "#932929FF"),
        (-2, "#6B1527FF")

    ]
    n_bins = 20000

    cmap_custom = LinearSegmentedColormap.from_list("custom_temperature_cmap", [color[1] for color in colors], N=n_bins)
    cmap_custom.set_bad(color='gray')
    # 使用imshow绘制图像，设置颜色映射范围
    plt.imshow(data, origin='lower', cmap=cmap, vmin=vmin, vmax=vmax, interpolation='nearest')

    # 移除坐标轴
    plt.axis('off')

    # 保存图像，确保没有白色边缘
    # plt.savefig(f'{csv_file_path}.png', dpi=2048, bbox_inches='tight', pad_inches=0)
    plt.show()
    plt.close()


# 示例调用
# for j in range(4):
#     for i in range(4):
#         csv_file_path1 = f'hours/{j}_{i}.csv'
#         plot_global_temperature(csv_file_path1)
# csv_file_path2 = 'output_csv/2024-02-17.csv'
# csv_file_path3 = 'output_csv/2024-05-25.csv'


plot_global_temperature('heatwave_data/2024-01-01.csv')
# plot_global_temperature(csv_file_path3)
