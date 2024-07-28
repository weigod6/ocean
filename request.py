import json
from datetime import datetime

import numpy as np
import pandas as pd
from flask import Flask, send_file, request, abort, jsonify
import os

app = Flask(__name__)

# 定义瓦片金字塔文件夹路径
TILESETS = {
    'world_tiles',
    'sst_tiles',
    'ice_tiles'
}

csv_folder = 'output_csv'


def check_csv_file(date):
    date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
    csv_file_path = os.path.join(csv_folder, f'{date_str}.csv')
    return os.path.exists(csv_file_path), csv_file_path


# @app.route('/sst/<string:date>/<int:lon>/<int:lat>', methods=['GET'])
# def get_sst(date, lon, lat):
#     csv_exists, csv_file_path = check_csv_file(date)
#     # 检查文件是否存在
#     if not csv_exists:
#         abort(404, description=f"CSV文件 '{date}' 不存在")
#
#     # 读取CSV文件
#     try:
#         df = pd.read_csv(csv_file_path, header=None)
#     except Exception as e:
#         abort(500, description=f"无法读取CSV文件: {e}")
#
#     # 根据经纬度计算索引
#     lon_index = lon * 4 + 720
#     lat_index = lat * 4 + 360
#
#     # 检查经纬度索引是否在数据范围内
#     if lat_index < 0 or lat_index >= df.shape[0] or lon_index < 0 or lon_index >= df.shape[1]:
#         return f"给定位置 ({lat}, {lon}) 没有可用数据"
#
#     # 获取海表面温度值
#     sst = df.iloc[lat_index, lon_index]
#
#     return str(sst)

def read_irregular_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # 将每一行拆分为数据点并添加到数据列表中
            data.append([round(float(item), 2) if item.strip() else None for item in line.strip().split(',')])
    return pd.DataFrame(data)
@app.route('/tiles/<tileset>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
@app.route('/tiles/<tileset>/<date>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
def get_tile(tileset, level=None, x=None, y=None, date=None):
    if tileset not in TILESETS:
        abort(404, description="Tileset not found")

    tileset_path = 'F:\oe_tiles\\' + tileset

    if date:
        tile_path = os.path.join(tileset_path, date, str(level), f"{x}_{y}.png")
    else:
        tile_path = os.path.join(tileset_path, str(level), f"{x}_{y}.png")

    if not os.path.exists(tile_path):
        abort(404, description="Tile not found" + tile_path)

    return send_file(tile_path)


@app.route('/sst_recent/<string:lat>/<string:lon>/<date>', methods=['GET'])
def get_sst_recent(lat, lon,date):

    lat_index = 360 + int(lat)*4

    lon_index = (1440+int(lon) * 4)%1440

    file_path = f"F:/oe_data2/{lat_index}/{lon_index}.csv"
    # return file_path
    if os.path.exists(file_path):
        # 确定目标行的索引
        start_year = 1982
        row_index = int(date.split('-')[0]) - start_year
        data = read_irregular_csv(file_path)
        data = data.map(lambda x: None if np.isnan(x) else f'{x:.2f}')
        # 提取特定行
        specific_row = data.iloc[row_index, :].tolist()

        # 构建字典并转换为JSON
        data_dict = {
            "row": specific_row,
        }
        json_data = json.dumps(data_dict)

        # json_data = json.dumps(data_dict)
        return json_data
    else:
        return jsonify({'error': 'File not found' + f"{lat_index}/{lon_index}"}), 404

@app.route('/sst_past/<string:lat>/<string:lon>/<date>', methods=['GET'])
def get_sst_past(lat, lon,date):

    lat_index = 360 + int(lat)*4

    lon_index = (1440+int(lon) * 4)%1440

    file_path = f"F:/oe_data2/{lat_index}/{lon_index}.csv"
    # return file_path
    if os.path.exists(file_path):
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_of_year = date_obj.timetuple().tm_yday
        data = read_irregular_csv(file_path)
        data = data.map(lambda x: None if np.isnan(x) else f'{x:.2f}')
        # 提取特定列
        # 使用iloc获取特定列数据，如果列索引超出范围则返回NaN
        specific_column = data.iloc[:, day_of_year - 1].tolist() if day_of_year - 1 < len(data.columns) else [None]*len(data)

        # 构建字典并转换为JSON
        data_dict = {
            "column": specific_column
        }
        json_data = json.dumps(data_dict)

        # json_data = json.dumps(data_dict)
        return json_data
    else:
        return jsonify({'error': 'File not found' + f"{lat_index}/{lon_index}"}), 404


@app.route('/sst_mean/<string:lat>/<string:lon>', methods=['GET'])
def get_sst_mean(lat, lon):

    lat_index = 360 + int(lat)*4

    lon_index = (1440+int(lon) * 4)%1440

    file_path = f"F:/oe_mean_data/{lat_index}_mean_sst.csv"
    # return file_path
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        data = data.map(lambda x: None if np.isnan(x) else f'{x:.2f}')
        # 提取特定列
        # 使用iloc获取特定列数据，如果列索引超出范围则返回NaN
        specific_column = data.iloc[:, lon_index - 1].tolist()

        # 构建字典并转换为JSON
        data_dict = {
            "column": specific_column
        }
        json_data = json.dumps(data_dict)

        return json_data
    else:
        return jsonify({'error': 'File not found' + f"{lat_index}/{lon_index}"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
