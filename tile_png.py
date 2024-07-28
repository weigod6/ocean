from PIL import Image
import os
import math


def create_tiles(image_path, tile_size, output_dir, max_zoom):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    full_img = Image.open(image_path)
    width, height = full_img.size

    # 基于最大缩放级别确定图像的目标大小
    max_dim = max(width, height)
    max_zoom_dim = tile_size * (2 ** max_zoom)
    scale_factor = max_zoom_dim / max_dim

    # 调整图像大小以适应最大缩放级别
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    full_img = full_img.resize((new_width, new_height), Image.LANCZOS)

    for zoom in range(max_zoom + 1):
        # 计算当前缩放级别的瓦片数量
        num_tiles = 2 ** zoom
        zoom_dir = os.path.join(output_dir, str(zoom))
        if not os.path.exists(zoom_dir):
            os.makedirs(zoom_dir)

        # 计算每个瓦片的大小（当前缩放级别）
        scaled_tile_size = tile_size * (2 ** (max_zoom - zoom))

        for x in range(num_tiles):
            for y in range(num_tiles):
                left = x * scaled_tile_size
                upper = y * scaled_tile_size
                right = left + scaled_tile_size
                lower = upper + scaled_tile_size

                # 裁剪瓦片并调整大小
                tile = full_img.crop((left, upper, right, lower))
                tile = tile.resize((tile_size, tile_size), Image.LANCZOS)

                # 保存瓦片
                tile_path = os.path.join(zoom_dir, f'{x}_{y}.png')
                tile.save(tile_path)


create_tiles('20000.png', 512, 'tiles', 5)

