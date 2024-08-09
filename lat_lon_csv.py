import os
from datetime import datetime as date
import time as t
import numpy as np
import pandas as pd
import netCDF4 as nc

# 定义文件夹路径
input_folder = "nc_data"
output_folder = "F:/oe_data2/"

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 初始化一个字典来存储当前处理的经纬度数据
nc_files = os.listdir(input_folder)
for nc_file in nc_files:
    dataset = nc.Dataset(os.path.join(input_folder, nc_file))
    sst_var = dataset.variables['sst'][:]
    time_var = dataset.variables['time'][:]
    lat_var = dataset.variables['lat'][:]
    lon_var = dataset.variables['lon'][:]

    for i, lat in enumerate(lat_var):
        for j, lon in enumerate(lon_var):
            sst_time_series = sst_var[:, i, j]
            df = pd.DataFrame(
                sst_time_series
            )
            df = df.transpose()
            output_dir = output_folder+f'{i}'
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            output_file = os.path.join(output_dir,f'{j}.csv')
            df.to_csv(output_file, mode='a', header=False, index=False)

    print(nc_file+'已处理')


