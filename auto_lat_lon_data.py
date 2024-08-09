import os
from datetime import datetime

import numpy as np
import pandas as pd
import netCDF4 as nc

def read_irregular_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # 将每一行拆分为数据点并添加到数据列表中
            data.append([round(float(item), 2) if item.strip() else None for item in line.strip().split(',')])
    return pd.DataFrame(data)


# 定义文件夹路径
input_folder = "nc_data"
output_folder = "F:/oe_data2/"

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

date = datetime.now().strftime('%G')
file = os.path.join(input_folder,f'sst.day.mean.{date}.nc')

dataset = nc.Dataset(file)
sst_var = dataset.variables['sst'][:]
lat_var = dataset.variables['lat'][:]
lon_var = dataset.variables['lon'][:]
for i, lat in enumerate(lat_var):
    for j, lon in enumerate(lon_var):
        sst_time_series = sst_var[:, i, j].tolist()
        all_none = all(item is None for item in sst_time_series)
        if all_none:
            continue
        df = pd.DataFrame(
            sst_time_series
        )
        df = df.transpose()
        df.replace(np.nan,None,inplace=True)
        input_dir = output_folder+f'{i}'
        input_file = os.path.join(input_dir,f'{j}.csv')
        input_data = read_irregular_csv(input_file)

        # 计算所需的长度
        required_length = input_data.shape[1]

        # 获取 sst_time_series 的当前长度
        current_length = len(sst_time_series)

        # 如果 sst_time_series 过长，截断它
        if current_length > required_length:
            new_row_data = sst_time_series[:required_length]
        # 如果 sst_time_series 过短，扩展它
        else:
            new_row_data = sst_time_series + [None] * (required_length - current_length)

        # 设置 DataFrame 的最后一行
        input_data.iloc[-1] = new_row_data

        pd.DataFrame(input_data).to_csv(input_file,header=False,index=False)
    if i % 10 == 0:
        print(f'已更新到{i}')
print(file+'已处理')

