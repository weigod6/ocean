import cv2
import os
import numpy as np
import schedule
import time

def create_tiles(image_path, tile_size, output_dir, max_zoom):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        print(output_dir)
        os.makedirs(output_dir)
    else:
        return
    # Read the image using OpenCV with alpha channel
    full_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width, channels = full_img.shape

    # Check if the image has an alpha channel, if not add one
    if channels == 3:
        full_img = cv2.cvtColor(full_img, cv2.COLOR_BGR2BGRA)

    # Based on max zoom level, determine the target size of the image
    max_dim = max(width, height)
    max_zoom_dim = tile_size * (2 ** max_zoom)
    scale_factor = max_zoom_dim / max_dim

    # Resize the image to fit the maximum zoom level
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    full_img = cv2.resize(full_img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    for zoom in range(max_zoom + 1):
        # Calculate number of tiles at the current zoom level
        num_tiles = 2 ** zoom
        zoom_dir = os.path.join(output_dir, str(zoom))
        if not os.path.exists(zoom_dir):
            os.makedirs(zoom_dir)

        # Calculate size of each tile at current zoom level
        scaled_tile_size = tile_size * (2 ** (max_zoom - zoom))

        for x in range(num_tiles):
            for y in range(num_tiles):
                left = x * scaled_tile_size
                upper = y * scaled_tile_size
                right = left + scaled_tile_size
                lower = upper + scaled_tile_size

                # Crop the tile from the resized image
                tile = full_img[upper:lower, left:right]

                # If the cropped tile is smaller than the expected size, pad it with transparent pixels
                if tile.shape[0] != scaled_tile_size or tile.shape[1] != scaled_tile_size:
                    padded_tile = np.zeros((scaled_tile_size, scaled_tile_size, 4), dtype=np.uint8)
                    padded_tile[:tile.shape[0], :tile.shape[1]] = tile
                    tile = padded_tile

                # Ensure the tile size matches tile_size (due to rounding issues)
                tile = cv2.resize(tile, (tile_size, tile_size), interpolation=cv2.INTER_LANCZOS4)

                # Save the tile
                tile_path = os.path.join(zoom_dir, f'{x}_{y}.png')
                # print(tile_path)
                cv2.imwrite(tile_path, tile)

path_name = 'recent_sst_png'  # 输入要获取文件的根目录

for filename in os.listdir(path_name):
    create_tiles(path_name + '/' + filename, 512, 'F:oe_tiles/sst_tiles/' + filename.split('.')[0], 5)

print("更新瓦片完成!")