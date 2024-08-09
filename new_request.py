import pandas as pd
from flask import Flask, send_file, request, abort, jsonify
import os
import opencv

app = Flask(__name__)

# 定义瓦片金字塔文件夹路径
TILESETS = {
    'world_tiles',
    'sst_3d_tiles',
    'ice_tiles'
}

csv_folder = 'output_csv'


def check_csv_file(date):
    date_str = pd.to_datetime(date).strftime('%Y-%m-%d')
    csv_file_path = os.path.join(csv_folder, f'{date_str}.csv')
    return os.path.exists(csv_file_path), csv_file_path

@app.route('/tiles/<tileset>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
@app.route('/tiles/<tileset>/<date>/<int:level>/<int:x>_<int:y>.png', methods=['GET'])
def get_tile(tileset, level=None, x=None, y=None, date=None):
    if tileset not in TILESETS:
        abort(404, description="Tileset not found")

    tileset_path = tileset

    if date:
        tileset_path = tileset_path +'/'+ date

        if os.path.exists(tileset_path):
            tile_path = os.path.join(tileset_path, str(level), f"{x}_{y}.png")
        else:
            # create_tiles('20000.png', 512, 'tiles', 5)
            opencv.create_tiles('recent_sst_png/'+date+'.png',512,'sst_3d_tiles/'+date,5)
            tile_path = os.path.join(tileset_path, str(level), f"{x}_{y}.png")

    else:
        tile_path = os.path.join(tileset_path, str(level), f"{x}_{y}.png")

    if not os.path.exists(tile_path):
        abort(404, description="Tile not found" + tile_path)

    return send_file(tile_path)


@app.route('/sst/<string:lat>/<string:lon>', methods=['GET'])
def get_csv(lat, lon):

    lat_index = 360 + int(lat)*4

    lon_index = 720 + int(lon) * 4

    file_path = f"F:/oe_data/{lat_index}/{lon_index}.csv"
    # return file_path
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found' + f"{lat_index}/{lon_index}"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
