import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from natsort import natsorted

def PreEquation(T_mean, t):

    weights = [5.8313202e-05, 0, 0.055298265, -0.0034783368, 0.0074266996, -0.014963626, -0.00041481410, -0.0022919620,
               -0.00033422399, -2.5732939e-05, -0.00041481410, 0.0022919620, 0.0074266996, 0.014963626, 0.055298265, 0.0034783368]

    T = T_mean
    for i in range(8):
        T = T - weights[2*i] * np.cos(2 * np.pi * i * t / 8) - weights[2*i+1] * np.sin(2 * np.pi * i * t / 8)
    return T


pth = 'G:/recent_output_csv'
files = os.listdir(pth)
files = natsorted(files)
index = files.index('2024-01-01.csv')
df = []
for e in files[index:]:
    df.append(pd.read_csv(f"G:/recent_output_csv/{e}",header=None).apply(pd.to_numeric,errors='coerce'))
data_sst = np.array(df)[:,400:601,0:541]
original_shape = data_sst.shape
data_sst = data_sst.reshape((*original_shape, 1))
time_point = 8
t = np.array([0, 2, 4, 6])

data_pred = PreEquation(data_sst, t[0])
for j in range(1, 4):
    data_pred = np.concatenate((data_pred, PreEquation(data_sst, t[j])), axis=3)

print(data_pred.shape)
date = datetime(2024,1,1).date()
for j in range(214):
    for i in range(4):
        df = pd.DataFrame(data_pred[j][:, :, i])
        df = df.round(2)
        df.to_csv(f'G:/hours_sst/{date+timedelta(days = j)}_{i * 6}.csv', header=False, index=False)

