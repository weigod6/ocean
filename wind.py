import numpy as np
import netCDF4 as nc
import json


# 读取NC文件
file_path = 'adaptor.mars.internal-1720766284.1175368-14547-5-c9eea5a0-24d5-408a-b99b-c1b7caf6fda0.nc'
dataset = nc.Dataset(file_path)

# 获取变量名
print(dataset.variables.keys())

# 提取U和V分量数据
u10 = dataset.variables['u10'][:]
v10 = dataset.variables['v10'][:]

# 提取经纬度
lats = dataset.variables['latitude'][:]
lons = dataset.variables['longitude'][:]

# 应用scale_factor和add_offset
u10 = u10 * dataset.variables['u10'].scale_factor + dataset.variables['u10'].add_offset
v10 = v10 * dataset.variables['v10'].scale_factor + dataset.variables['v10'].add_offset

# 关闭文件
dataset.close()

# 打印数据的形状以确认读取成功
print('u10 shape:', u10.shape)
print('v10 shape:', v10.shape)
print('lats shape:', lats.shape)
print('lons shape:', lons.shape)

# 选择一个时间步长进行可视化，例如第0个时间步长
u10_0 = u10[0, :, :]
v10_0 = v10[0, :, :]




data = {
    'latitude': lats.tolist(),
    'longitude': lons.tolist(),
    'u10': u10_0.tolist(),
    'v10': v10_0.tolist()
}

# 将数据保存为JSON文件
with open('wind_data.json', 'w') as f:
    json.dump(data, f)
