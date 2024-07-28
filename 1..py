import numpy as np
import pandas as pd
import json
from datetime import datetime

file_path = "F:/oe_data2/78/28.csv"
date = '2024-07-01'
date_obj = datetime.strptime(date, "%Y-%m-%d")
day_of_year = date_obj.timetuple().tm_yday
def read_irregular_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # 将每一行拆分为数据点并添加到数据列表中
            data.append([round(float(item), 2) if item.strip() else None for item in line.strip().split(',')])
    return pd.DataFrame(data)
# 确定目标行的索引
start_year = 1982
row_index = int(date.split('-')[0]) - start_year

# 定义一个函数来处理不规则的CSV文

# 读取文件
data = read_irregular_csv(file_path)
data = data.map(lambda x: None if np.isnan(x) else f'{x:.2f}')
# 提取特定行
specific_row = data.iloc[row_index, :].tolist()

# 提取特定列
# 使用iloc获取特定列数据，如果列索引超出范围则返回NaN
specific_column = data.iloc[:, day_of_year - 1] if day_of_year - 1 < len(data.columns) else [float('nan')]*len(data)

# 构建字典并转换为JSON
data_dict = {
    "row": specific_row,
    "column": specific_column.tolist()
}
json_data = json.dumps(data_dict)

print(json_data)
