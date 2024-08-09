from datetime import datetime

import netCDF4 as nc
import pandas as pd
import numpy as np
import os


def nc_to_csv(nc_file_path, output_dir):
    nc_file_path = package_pth+'/'+nc_file_path
    # 读取 nc 文件
    dataset = nc.Dataset(nc_file_path)

    # 获取时间、纬度、经度和海表温度（sst）变量
    time_var = dataset.variables['time']
    lat_var = dataset.variables['lat']
    lon_var = dataset.variables['lon']
    sst_var = dataset.variables['sst']

    # 将时间变量转换为 datetime 对象
    time_units = time_var.units
    time_calendar = time_var.calendar if 'calendar' in time_var.ncattrs() else 'standard'
    times = nc.num2date(time_var[:], units=time_units, calendar=time_calendar)
    times = [datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S') for time in times]
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 批量处理数据
    for i, time in enumerate(times):
        # 提取某一天的 SST 数据
        sst_data = sst_var[i, :, :].filled(np.nan)

        # 创建 DataFrame
        df = pd.DataFrame(sst_data, index=lat_var[:], columns=lon_var[:])

        # 将 NaN 替换为 'N'
        df = df.applymap(lambda x: 'N' if np.isnan(x) else f'{x:.2f}')
        # 获取列名列表
        columns = list(df.columns)
        new_columns = columns[-720:] + columns[:-720]
        df = df[new_columns]

        # 将 DataFrame 保存为 CSV 文件
        date_str = pd.to_datetime(time).strftime('%Y-%m-%d')
        output_file = os.path.join(output_dir, f'{date_str}.csv')
        df.to_csv(output_file, header=False, index=False)
        print(f'Saved {output_file}')

    # 关闭 nc 文件
    dataset.close()

package_pth = 'nc_data'
# 示例调用
output_dir = 'recent_output_csv'
for filename in os.listdir(package_pth):
    if(int(filename.split('.')[3])>2020):
        nc_to_csv(filename,output_dir)
