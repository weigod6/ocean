import os
import pandas as pd
from natsort import natsorted

pth = 'F:/oe_mean_data'
output_pth = 'F:/y1981-2014_mean_data'
files = os.listdir(pth)
files = natsorted(files)
for i in range(365):
    df = pd.DataFrame()
    for file in files:
        file_pth = os.path.join(pth, file)
        data = pd.read_csv(file_pth, header=None)
        row_data = data.iloc[[i]]
        # 获取列名列表
        columns = list(df.columns)
        new_columns = columns[-720:] + columns[:-720]
        df = df[new_columns]
        df = pd.concat([df, row_data], axis=0)
    df.to_csv(f'{output_pth}/day{i}.csv', header=False, index=False)
