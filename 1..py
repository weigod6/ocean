import csv
import json
import os


import numpy as np
import pandas as pd
from natsort import natsorted

from datetime import datetime, timedelta
import pandas as pd
import scipy.io
date_object = datetime.now().date()
day_of_year = date_object.timetuple().tm_yday - 1
begin_day = datetime(2024,1,1)
data = scipy.io.loadmat('G:/nc_data/Pred_hours_SST.mat')
for j in range(day_of_year):
    for i in range(4):
        df = pd.DataFrame(data['sst'][j, :, :, i])
        df.to_csv(f'G:/hours/{begin_day+timedelta(days=j)}_{i}.csv', header=False, index=False)


# def read_irregular_csv(file_path):
#     data = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             # 将每一行拆分为数据点并添加到数据列表中
#             data.append([round(float(item), 2) if item.strip() else None for item in line.strip().split(',')])
#     return pd.DataFrame(data)
#
# def is_leap_year(year):
#     return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
#
#
# date = '2023-12-31'
# file_path = f"F:/oe_data2/81/0.csv"
# start_year = 1982
# row_index = int(date.split('-')[0]) - start_year
# data = read_irregular_csv(file_path)
# data = data.map(lambda x: None if np.isnan(x) else f'{x:.2f}')
# date_obj = datetime.strptime(date, "%Y-%m-%d")
# day_of_year = date_obj.timetuple().tm_yday
#
# past_7 =[]
# fut_7 = []
# next=365 if is_leap_year(int(date.split('-')[0])+1) else 366
# last=365 if is_leap_year(int(date.split('-')[0])-1) else 366
# if day_of_year < 7:
#     if row_index-1<0 :
#         past_7 = [None]*(8 - day_of_year) + data.iloc[row_index,0: day_of_year].tolist()
#     else:
#         past_7 = data.iloc[row_index - 1, last - 8 + day_of_year:last].tolist() + data.iloc[row_index,0: day_of_year].tolist()
#     fut_7 = data.iloc[row_index,day_of_year+1:day_of_year+8].tolist()
# elif day_of_year+7 > next:
#     st = (day_of_year+7)%next
#     past_7 = data.iloc[row_index,day_of_year-7:day_of_year].tolist()
#     if row_index+1 > int(datetime.now().strftime('%G'))-start_year:
#         fut_7 = data.iloc[row_index,day_of_year-1:next].tolist()+[None]*st
#     else:
#         fut_7 = data.iloc[row_index,day_of_year-1:next].tolist()+data.iloc[row_index+1, 0: st].tolist()
# else:
#     past_7 = data.iloc[row_index, day_of_year - 7:day_of_year+1].tolist()
#     fut_7 = data.iloc[row_index, day_of_year + 1:day_of_year + 8].tolist()
# # 提取特定行
# specific_row =past_7+fut_7
#
# # 构建字典并转换为JSON
# data_dict = {
#     "row": specific_row,
# }
# json_data = json.dumps(data_dict)

# df.iloc[-1] = [1,2,3]+[None]*(366-3)
# print(df)
# pd.DataFrame([1])
# pd.DataFrame(df).to_csv(input_file,header=False,index=False)
# pd.DataFrame([11]).to_csv(input_file,mode='a', header=False, index=False)
