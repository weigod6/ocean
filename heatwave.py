import os
from datetime import datetime

import pandas as pd
import numpy as np
from natsort import natsorted

input_pth1 = 'F:/y1981-2014_mean_data'
input_pth2 = 'recent_output_csv'
input_pth3 = 'F:/y1981-2014_90%-mean_data'

input_files1 = os.listdir(input_pth1)
input_files2 = os.listdir(input_pth2)
input_files3 = os.listdir(input_pth3)

na_input_files1 = natsorted(input_files1)
na_input_files2 = natsorted(input_files2)
na_input_files3 = natsorted(input_files3)

initial_dfs = []
subtract_dfs = []
divsion_dfs = []

initial_arrays = []
subtract_arrays = []
divsion_arrays = []
begin_date = '2023-12-28'
start_file = begin_date+'.csv'
start_index = na_input_files2.index(start_file)

for file in na_input_files2[start_index:]:
    date_object = datetime.strptime(file.split('.')[0], '%Y-%m-%d').date()
    # 获取该日期是该年的第几天
    day_of_year = date_object.timetuple().tm_yday-1
    date_str = date_object.strftime('%Y-%m-%d')
    input1 = pd.read_csv(os.path.join(input_pth1,f'day{day_of_year}.csv'),header=None).apply(pd.to_numeric,errors='coerce')
    input2 = pd.read_csv(os.path.join(input_pth2,date_str+'.csv'),header=None).apply(pd.to_numeric,errors='coerce')
    input3 = pd.read_csv(os.path.join(input_pth3,f'day{day_of_year}.csv'),header=None).apply(pd.to_numeric,errors='coerce')
    initial_arrays.append(input1.values)
    subtract_arrays.append(input2.values)
    divsion_arrays.append(input3.values)
    if initial_arrays.__len__() < 5:
        continue
    else:
        # 对每个初始数组减去对应的 subtract 数组
        subtracted_arrays = [subtract - initial for initial, subtract in zip(initial_arrays, subtract_arrays)]
        divsioned_arrays = [subtracted / divsion for divsion, subtracted in zip(divsion_arrays, subtracted_arrays)]
        # print(divsioned_arrays)
        # 使用 numpy 的 all 函数查找所有位置在所有数组中都大于 0 的位置
        greater_than_zero_mask = np.all(np.array(divsioned_arrays) > 0, axis=0)
        filtered_arrays = [np.where(greater_than_zero_mask, divsion, 0) for divsion in divsioned_arrays]
        # 将结果转换为 DataFrame，便于查看和保存
        filtered_dfs = [pd.DataFrame(filtered_array, columns=input1.columns).clip(upper=5) for filtered_array in
                        filtered_arrays]
        sst = np.floor(filtered_dfs[4])
        sst.to_csv(f'heatwave/{date_str}.csv', header=False, index=False)
        sea_temperature = sst

        print(sea_temperature)
        initial_arrays = initial_arrays[1:]  # 丢弃第一页
        subtract_arrays = subtract_arrays[1:]  # 丢弃第一页
        divsion_arrays = divsion_arrays[1:]  # 丢弃第一页




