import json
import math
from datetime import datetime
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import pandas as pd
from flask import Flask, send_file, request, abort, jsonify
import os
from natsort import natsorted
app = Flask(__name__)

# 定义瓦片金字塔文件夹路径
TILESETS = {
    'world_tiles',
    'sst_3d_tiles',
    'heatwave_tiles',
    'sst_tiles'
}

csv_folder = 'output_csv'


def load_sea_boundaries(file_path):
    return gpd.read_file(file_path)

def check_csv_file(date):
    date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
    csv_file_path = os.path.join(csv_folder, f'{date_str}.csv')
    return os.path.exists(csv_file_path), csv_file_path


def read_irregular_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # 将每一行拆分为数据点并添加到数据列表中
            data.append([round(float(item), 2) if item.strip() else None for item in line.strip().split(',')])
    return pd.DataFrame(data)

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_newest_date():
    files = os.listdir('G:/recent_output_csv')
    na_files = natsorted(files)
    return na_files[-1].split('.')[0]



gpkg_file = "goas_v01.gpkg"

# 加载海域边界数据（假设数据集中包含多个图层，根据需要选择图层）
sea_boundaries = load_sea_boundaries(gpkg_file)
# 定义各个海域的GeoJSON文件路径
geojson_files = {
    "黄海": "sea_bound/yellow.geojson",
    "渤海": "sea_bound/bohai.geojson",
    "东海": "sea_bound/dong.geojson",
    "南海": "sea_bound/nan.geojson"
}
sea_boundaries.loc[sea_boundaries['name'] == 'Southern Ocean', 'name'] = '南冰洋'
sea_boundaries.loc[sea_boundaries['name'] == 'South Atlantic Ocean', 'name'] = '大西洋'
sea_boundaries.loc[sea_boundaries['name'] == 'South Pacific Ocean', 'name'] = '太平洋'
sea_boundaries.loc[sea_boundaries['name'] == 'North Pacific Ocean', 'name'] = '太平洋'
sea_boundaries.loc[sea_boundaries['name'] == 'South China and Easter Archipelagic Seas', 'name'] = '中国南海及东部群岛海'
sea_boundaries.loc[sea_boundaries['name'] == 'Indian Ocean', 'name'] = '印度洋'
sea_boundaries.loc[sea_boundaries['name'] == 'Mediterranean Region', 'name'] = '地中海地区'
sea_boundaries.loc[sea_boundaries['name'] == 'Baltic Sea', 'name'] = '波罗的海'
sea_boundaries.loc[sea_boundaries['name'] == 'North Atlantic Ocean', 'name'] = '大西洋'
sea_boundaries.loc[sea_boundaries['name'] == 'Arctic Ocean', 'name'] = '北冰洋'

sea_boundaries1 = {name: load_sea_boundaries(path) for name, path in geojson_files.items()}

# 判断经纬度是否在海域内
def find_sea_region(latitude, longitude):
    point = Point(longitude, latitude)
    for sea_name, sea_boundary in sea_boundaries1.items():
        if any(geom.contains(point) for geom in sea_boundary.geometry):
            return sea_name

    for index, row in sea_boundaries.iterrows():
        if row['geometry'].contains(point):
            return row['name']
    return "未知海域或陆地"


@app.route('/information/<string:lat>/<string:lon>', methods=['GET'])
def get_inf(lat,lon):
    with open('data.txt', 'r', encoding='utf-8') as file:
        data = json.load(file)
    sea_name = find_sea_region(lat, lon)
    if sea_name =='黄海' or sea_name =='渤海':
        sea_name = '黄渤海'
    if sea_name != '未知海域或陆地':
        return data[sea_name]
    else:
        abort(404)
@app.route('/init/<int:sign>', methods=['GET'])
def get_date(sign):
    if sign == 1:
        return get_newest_date()
    else:
        abort(404)

@app.route('/tiles/<tileset>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
@app.route('/tiles/<tileset>/<date>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
def get_tile(tileset, level=None, x=None, y=None, date=None):
    if tileset not in TILESETS:
        abort(404, description="Tileset not found")

    tileset_path = 'G:/oe_tiles/' + tileset

    if date:
        # if tileset == 'sst_3d_tiles':
        # tile_path = os.path.join('oe_tiles/sst_3d_tiles/0', str(level), f"{x}_{y}.png")
        # else:
        tile_path = os.path.join(tileset_path, date, str(level), f"{x}_{y}.png")
    else:
        tile_path = os.path.join(tileset_path, str(level), f"{x}_{y}.png")

    if not os.path.exists(tile_path):
        abort(404, description="Tile not found" + tile_path)

    return send_file(tile_path)

@app.route('/sst_3d/<date>/<int:depth>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
def get_sst_3d(date, depth,level,x,y):
    path = f'G:/oe_tiles/3d_tiles/{date}/{depth}/{level}/{x}_{y}.png'
    if not os.path.exists(path):
        abort(404, description="data not found" + path)
    else:
        return send_file(path)

@app.route('/sst_hours/<date>/<int:hour>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
def get_sst_hours(date, hour,level,x,y):
    path = f'G:/oe_tiles/hours_tiles/{date}_{hour}/{level}/{x}_{y}.png'
    if not os.path.exists(path):
        abort(404, description="data not found" + path)
    else:
        return send_file(path)
@app.route('/sst_recent/<string:lat>/<string:lon>/<date>', methods=['GET'])
def get_sst_recent(lat, lon,date):

    lat_index = 360 + int(lat)*4

    lon_index = (1440+int(lon) * 4)%1440

    file_path = f"G:/over_the_years_data/{lat_index}/{lon_index}.csv"
    # return file_path
    if os.path.exists(file_path):
        # 确定目标行的索引
        start_year = 1982
        row_index = int(date.split('-')[0]) - start_year
        data = read_irregular_csv(file_path)
        data = data.map(lambda x: None if np.isnan(x) else f'{x:.2f}')


        pre_file_path = f"G:/pre_csv_ana_data/{lat_index}.csv"
        newest_date = get_newest_date()
        newest_date_obj = datetime.strptime(newest_date, "%Y-%m-%d")
        newest_day_of_year = newest_date_obj.timetuple().tm_yday
        pre_data = pd.read_csv(pre_file_path, header=None)
        pre_data.replace(0, None, inplace=True)
        df = pre_data.iloc[:, (lon_index + 720) % 1440]
        data.iloc[-1, newest_day_of_year:newest_day_of_year + 7] = pd.DataFrame(df).T

        # 提取特定行
        specific_row = data.iloc[row_index, :].tolist()

        # 构建字典并转换为JSON
        data_dict = {
            "row": specific_row,
        }
        json_data = json.dumps(data_dict)

        return json_data
    else:
        return jsonify({'error': 'File not found' + f"{lat_index}/{lon_index}"}), 404

@app.route('/sst_past/<string:lat>/<string:lon>/<date>', methods=['GET'])
def get_sst_past(lat, lon,date):


    lat_index = 360 + int(lat)*4

    lon_index = (1440+int(lon) * 4)%1440

    file_path = f"G:/over_the_years_data/{lat_index}/{lon_index}.csv"
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

    file_path = f"G:/oe_mean_data/{lat_index}_mean_sst.csv"
    # return file_path
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
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


@app.route('/sst_15/<string:lat>/<string:lon>/<date>', methods=['GET'])
def get_sst_15(lat, lon,date):

    lat_index = 360 + int(lat)*4

    lon_index = (1440+int(lon) * 4)%1440

    file_path = f"G:/over_the_years_data/{lat_index}/{lon_index}.csv"

    pre_file_path = f"G:/pre_csv_ana_data/{lat_index}.csv"
    if os.path.exists(file_path) and os.path.exists(pre_file_path):
        # 确定目标行的索引
        start_year = 1982
        row_index = int(date.split('-')[0]) - start_year
        data = read_irregular_csv(file_path)

        # data = data.map(lambda x: None if np.isnan(x) else f'{x:.2f}')
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_of_year = date_obj.timetuple().tm_yday-1
        #

        newest_date = get_newest_date()
        newest_date_obj = datetime.strptime(newest_date, "%Y-%m-%d")
        newest_day_of_year = newest_date_obj.timetuple().tm_yday
        pre_data = pd.read_csv(pre_file_path, header=None)
        pre_data.replace(0, None, inplace=True)
        df = pre_data.iloc[:, (lon_index+720)%1440]
        data.iloc[-1, newest_day_of_year:newest_day_of_year + 7] = pd.DataFrame(df).T

        past_7 = []
        fut_7 = []
        last = 365
        next = 365
        if is_leap_year(int(date.split('-')[0]) - 1):
            last = 366
        if is_leap_year(int(date.split('-')[0]) + 1):
            next = 366
        if day_of_year < 7:
            if row_index - 1 < 0:
                past_7 = [None] * (8 - day_of_year) + data.iloc[row_index, 0: day_of_year].tolist()
            else:
                past_7 = data.iloc[row_index - 1, last - 8 + day_of_year:last].tolist() + data.iloc[row_index,
                                                                                          0: day_of_year].tolist()
            fut_7 = data.iloc[row_index, day_of_year + 1:day_of_year + 8].tolist()
        elif day_of_year + 7 > next:
            st = (day_of_year + 7) % next
            past_7 = data.iloc[row_index, day_of_year - 7:day_of_year].tolist()
            if row_index + 1 > int(datetime.now().strftime('%G')) - start_year:
                fut_7 = data.iloc[row_index, day_of_year - 1:next].tolist() + [None] * st
            else:
                fut_7 = data.iloc[row_index, day_of_year - 1:next].tolist() + data.iloc[row_index + 1, 0: st].tolist()
        else:
            past_7 = data.iloc[row_index, day_of_year - 7:day_of_year + 1].tolist()
            fut_7 = data.iloc[row_index, day_of_year + 1:day_of_year + 8].tolist()
        # 提取特定行
        specific_row = past_7 + fut_7
        # 构建字典并转换为JSON

        new_list = [None if math.isnan(x) else x for x in specific_row]
        data_dict = {
            "row": new_list
        }
        json_data = json.dumps(data_dict)
        return json_data
    else:
        return jsonify({'error': 'File not found' + f"{lat_index}/{lon_index}"}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
