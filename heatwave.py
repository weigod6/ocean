import os

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from natsort import natsorted


def read_irregular_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # 将每一行拆分为数据点并添加到数据列表中
            data.append([round(float(item), 2) if item.strip() else None for item in line.strip().split(',')])
    return pd.DataFrame(data)

pth = 'F:/oe_data2'
package_pth = os.listdir(pth)
package_pth = natsorted(package_pth)
mean_sst_pth = 'F:/oe_mean_data'
output_pth = 'F:/oe_90%-mean_data'


file = 'F:/oe_data2/84/0.csv'
df2 = read_irregular_csv('F:/oe_mean_data/84_mean_sst.csv')
df = read_irregular_csv(file)
mean_data =pd.DataFrame()
for e in package_pth:
    files = os.listdir(os.path.join(pth, e))
    files = natsorted(files)
    output_file = os.path.join(output_pth, f'{e}_90%-mean_sst.csv')
    if os.path.exists(output_file):
        continue
    day_mean_data = pd.DataFrame()
    # mean_data = pd.read_csv(os.path.join(mean_sst_pth, f'{e}_mean_sst.csv'), header=None)# 我想在外面读mean_data 因为在里面是重复读了，然后我就把它拿出来，报错
    # print(mean_data.shape)#索引超了QAQ

    for file in files:
        mean_data = pd.read_csv(os.path.join(mean_sst_pth, f'{e}_mean_sst.csv'), header=None)#但是你把它放里面来，就没问题
        # print(mean_data[389])
        file_pth = os.path.join(pth, e, file)
        data = read_irregular_csv(file_pth)
        quantile_90_data = data.iloc[0:32].quantile(0.90)
        index = int(file.split('.')[0])
        print(index)
        mean_sst = mean_data[index]
        mean_data = quantile_90_data - mean_sst
        day_mean_data = pd.concat([day_mean_data, mean_data], axis=1)

    day_mean_data.to_csv(output_file, header=False, index=False)


ddf =df.iloc[0:32].quantile(0.90)-df2[0]

print(ddf)#一个地点，根据1981年-2014年的数据，处理出来的每天的第90分位数温度 - 一个地点每天的平均温度（根据1981年-2014年）

# 0      0.407
# 1      0.429
# 2      0.501
# 3      0.638
# 4      0.704
#        ...
# 361    0.638
# 362    0.757
# 363    0.578
# 364    0.588
# 365    0.611