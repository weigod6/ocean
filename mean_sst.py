import os
from natsort import natsorted
import pandas as pd


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
output_pth = 'F:/oe_mean_data'

for e in package_pth:
    files = os.listdir(os.path.join(pth,e))
    files = natsorted(files)
    output_file = os.path.join(output_pth, f'{e}_mean_sst.csv')
    if os.path.exists(output_file):
        continue
    print(output_file)
    day_mean_data = pd.DataFrame()
    for file in files:
        file_pth = os.path.join(pth,e,file)
        data = read_irregular_csv(file_pth)
        mean_data = round(data.loc[0:32,:].mean(),2)
        day_mean_data = pd.concat([day_mean_data, mean_data], axis=1)


    day_mean_data.to_csv(output_file,header=False, index=False)


