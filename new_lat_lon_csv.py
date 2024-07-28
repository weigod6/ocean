import os
from datetime import datetime as date
import time as t
import numpy as np
import pandas as pd
import netCDF4 as nc

# 定义文件夹路径
input_folder = "recent"
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
            # print(df)
            output_dir = output_folder+f'{i}'
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            output_file = os.path.join(output_dir,f'{j}.csv')
            df.to_csv(output_file, mode='a', header=False, index=False)

    print(nc_file+'已处理')
    # time_units = time_var.units
    # time_calendar = time_var.calendar if 'calendar' in time_var.ncattrs() else 'standard'
    # times = nc.num2date(time_var[:], units=time_units, calendar=time_calendar)
    # times = [date.strptime(str(time), '%Y-%m-%d %H:%M:%S') for time in times]

    # 初始化存储数据的数组
    # current_data = {key: [] for key in set((lat, lon) for lat in range(720) for lon in range(1440))}
    cnt=1
    # for i, time in enumerate(times):
    #     # 提取某一天的 SST 数据
    #     sst_data = sst_var[i, :, :].filled(np.nan)
    #     print(f'读文件进度：{i}/{times.__len__()}')
    #     cnt +=1
    #     # 将 NaN 替换为 'N'，并将数值格式化为字符串
    #     sst_data = np.where(np.isnan(sst_data), 'N', np.round(sst_data, 2).astype(str))
    #
    #     for lat, lon in current_data.keys():
    #         current_data[(lat, lon)].append(sst_data[lat, lon])

    # start = t.perf_counter()
    # count = 1
    # for (lat, lon), values in current_data.items():
    #     print(f'写入文件进度：{count/current_data.items().__len__()*100}%')
    #     count += 1
    #     output_path = os.path.join(output_folder, f"{lat}")
    #     output_file = os.path.join(output_path, f"{lon}.csv")
    #     if not os.path.exists(output_path):
    #         os.makedirs(output_path)
    #     pd.DataFrame([values]).to_csv(output_file, mode='a', header=False, index=False)


