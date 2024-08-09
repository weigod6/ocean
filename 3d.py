import os.path
from datetime import datetime, timedelta

import netCDF4 as nc
import pandas as pd
import numpy as np
import xarray as xr
file_path = 'G:/ESC_20230101_20240801.nc'
dataset = nc.Dataset(file_path)


# 获取变量
temperature = dataset.variables['thetao']
time = dataset.variables['time']
depth = dataset.variables['depth']

# 设定开始日期
start_date = datetime(2023, 1, 1)

# 获取时间和深度的长度
num_times = len(time)
num_depths = len(depth)
for d in range(num_depths):
    print(depth[d])
# # 遍历时间和深度
# for t in range(num_times):
#     for d in range(num_depths):
#         # 提取当前时间和深度的海温数据
#         temp_at_time_depth = temperature[t, d, :, :]
#         today_date = start_date + timedelta(days=t)
#         # 在这里可以对temp_at_time_depth进行处理或分析
#         # 例如打印或保存数据
#         output_floder = f'G:/oe_3d_data/{today_date.date()}'
#         if not os.path.exists(output_floder):
#             os.mkdir(output_floder)
#         pd.DataFrame(temp_at_time_depth).round(2).to_csv(os.path.join(output_floder,f'{d}.csv'),header=False,index=False)
#
# # 关闭NetCDF文件
# dataset.close()