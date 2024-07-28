import numpy as np
import pandas as pd
from scipy.ndimage import zoom
import os


def reshpe(filename):
    # 读取CSV文件
    file_pth = path_name + '/'+filename
    new_file_path = 'recent_csv_output' + '/' + filename
    if(os.path.exists(new_file_path)):
        return
    data = pd.read_csv(file_pth, header=None).values

    # 处理缺失值（N表示的部分）
    data[data == 'N'] = np.nan
    data = data.astype(float)

    # 创建掩码，标记非缺失值的位置
    mask = ~np.isnan(data)

    # 使用掩码和最近邻插值方法填充缺失值
    data_filled = np.where(mask, data, 0)
    zoom_factor = 4

    # 放大掩码和填充后的数据
    data_filled_zoom = zoom(data_filled, zoom_factor, order=1)
    mask_zoom = zoom(mask.astype(float), zoom_factor, order=0)

    # 使用掩码将无效值再次标记为NaN
    interpolated_data = np.where(mask_zoom, data_filled_zoom, np.nan)

    # 降低数据精度并保留两位小数
    interpolated_data = np.around(interpolated_data.astype(np.float32), decimals=2)

    # 将掩码的部分还原成'N'
    result = np.where(np.isnan(interpolated_data), 'N', interpolated_data)
    # 保存结果到新的CSV文件


    pd.DataFrame(result).to_csv(new_file_path, header=None, index=False)


path_name = 'recent_output_csv'  # 输入要获取文件的根目录
for filename in os.listdir(path_name):
    reshpe(filename)
