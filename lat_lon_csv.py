import pandas as pd
import os

# 定义文件夹路径
input_folder = "recent_output_csv"
output_folder = "F:/oe_data/"

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 初始化一个字典来存储缺失值的经纬度
missing_value_coords = set()

# 预处理缺失值
df = pd.read_csv(os.path.join(input_folder, '2021-01-01.csv'), header=None)
for lat in range(720):
    for lon in range(1440):
        if df.iat[lat, lon] == 'N':
            missing_value_coords.add((lat, lon))

# 初始化一个字典来存储当前处理的经纬度数据

i=2021
for j in range(i,2025):
    # 逐个读取CSV文件并处理数据
    current_data = {key: [] for key in set((lat, lon) for lat in range(720) for lon in range(1440)) - missing_value_coords}
    csv_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.csv')])
    print(csv_files)
    for file in csv_files:
        date = file.split('-')[0]  # 提取日期
        if(int(date) != j):
            continue
        print("读取"+file+"数据")

        df = pd.read_csv(os.path.join(input_folder, file), header=None)

        for lat in range(720):
            for lon in range(1440):
                if (lat, lon) in missing_value_coords:
                    continue  # 跳过缺失值对应的经纬度

                current_data[(lat, lon)].append(df.iat[lat, lon])

    # 写入数据到对应文件
    for (lat, lon), values in current_data.items():
        output_path = os.path.join(output_folder,f"{lat}")
        output_file = os.path.join(output_path, f"{lon}.csv")

        if not os.path.exists(output_path):
            os.makedirs(output_path)
        pd.DataFrame([values]).to_csv(output_file,mode='a', header=False, index=False)

print("数据处理完成。")