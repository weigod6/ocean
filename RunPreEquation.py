
import numpy as np
import netCDF4 as nc
import scipy


##目的：利用数据反演每3个小时的动态。
##目的：利用数据反演每3个小时的动态。

def PreEquation(T_mean, t):

    weights = [5.8313202e-05, 0, 0.055298265, -0.0034783368, 0.0074266996, -0.014963626, -0.00041481410, -0.0022919620,
               -0.00033422399, -2.5732939e-05, -0.00041481410, 0.0022919620, 0.0074266996, 0.014963626, 0.055298265, 0.0034783368]

    T = T_mean
    for i in range(8):
        T = T - weights[2*i] * np.cos(2 * np.pi * i * t / 8) - weights[2*i+1] * np.sin(2 * np.pi * i * t / 8)
    return T



data_20 = nc.Dataset("recent/sst.day.mean.2024.nc")  # (200,720,1440)----(t,y,x)  # ##输入
data_sst = np.array(data_20['sst'])[:, 400:601, 720:1241]  # 输入限制经纬度
original_shape = data_sst.shape
data_sst = data_sst.reshape((*original_shape, 1))
time_point = 8
t = np.array([0, 2, 4, 6])

data_pred = PreEquation(data_sst, t[0])
for j in range(1, 4):
    data_pred = np.concatenate((data_pred, PreEquation(data_sst, t[j])), axis=3)

scipy.io.savemat('Pred_hours_SST.mat', {'sst': data_pred})

