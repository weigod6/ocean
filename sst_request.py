from flask import Flask, request, abort
import pandas as pd
import os

app = Flask(__name__)

# 假设CSV文件存放在output_csv文件夹下
csv_folder = 'output_csv'

# 辅助函数：检查CSV文件是否存在
def check_csv_file(date):
    date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
    csv_file_path = os.path.join(csv_folder, f'{date_str}.csv')
    return os.path.exists(csv_file_path), csv_file_path

@app.route('/sst/<string:date>/<int:lon>/<int:lat>', methods=['GET'])
def get_sst(date, lon, lat):
    csv_exists, csv_file_path = check_csv_file(date)
    # 检查文件是否存在
    if not csv_exists:

        abort(404, description=f"CSV文件 '{date}' 不存在")

    # 读取CSV文件
    try:
        df = pd.read_csv(csv_file_path, header=None)
    except Exception as e:
        abort(500, description=f"无法读取CSV文件: {e}")

    # 根据经纬度计算索引
    lon_index = lon * 4 + 720
    lat_index = lat * 4 + 360

    # 检查经纬度索引是否在数据范围内
    if lat_index < 0 or lat_index >= df.shape[0] or lon_index < 0 or lon_index >= df.shape[1]:
        return f"给定位置 ({lat}, {lon}) 没有可用数据"

    # 获取海表面温度值
    sst = df.iloc[lat_index, lon_index]

    return str(sst)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
