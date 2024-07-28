import os
import warnings

import pandas as pd

# 定义输入输出目录
input_dir = 'recent_output_csv'
output_dir = 'lon_lat_csv'

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 获取所有 CSV 文件的列表
csv_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.csv')])
print(csv_files)
# 确定数据的维度
lat_size = 720
lon_size = 1440

warnings.filterwarnings("ignore")

model_file_path = os.path.join(input_dir, csv_files[0])
model_df = pd.read_csv(model_file_path, header=None)
# 每次处理一个经纬度位置的数据
for lat in range(lat_size):
    for lon in range(lon_size):

        value = model_df.iloc[lat, lon]
        print(lat)
        print(lon)
        if (value == 'N'):
            continue
        data_cache = []

        i=0
        for file in csv_files:
            file_path = os.path.join(input_dir, file)
            df = pd.read_csv(file_path, header=None)
            value = df.iloc[lat, lon]

            i+=1
            data_cache.append(value)

            if(i%365==0):
                output_file = os.path.join(output_dir, f'lat_{lat}_lon_{lon}.csv')
                with open(output_file, 'a') as f:
                    f.write(','.join(map(str, data_cache)) + '\n')
                    data_cache = []



        # 将数据写入对应的文件
        output_file = os.path.join(output_dir, f'lat_{lat}_lon_{lon}.csv')
        with open(output_file, 'a') as f:
            f.write(','.join(map(str, data_cache)) + '\n')


print("数据处理完成！")
