def get_palette(image):
    from ...graphics.palette import Palette

    RGB_CHANNELS = 3
    PALETTE_COLORS = 16

    image_channels = 3
    image_palette = image.getpalette()

    palette = Palette()
    for color_index in range(PALETTE_COLORS):
        data_index = color_index * image_channels
        rgb_data = image_palette[data_index : data_index + RGB_CHANNELS]

        palette.append_rgb(rgb_data)
    return palette

def get_tiles(image):
    from ...graphics.sprite_tile import SpriteTile
    from ...graphics import poses as poses

    image_color_indices = image.getdata()
    tile_indices = poses.PORTRAIT

    TILE_ROWS = len(tile_indices)
    TILE_COLS = len(tile_indices[0])
    PORTRAIT_SPRITE_TILE_COUNT = 25

    tiles_found = set()
    tile_start_pixel = 0
    tiles = [SpriteTile() for tile in range(PORTRAIT_SPRITE_TILE_COUNT)]
    for tile_row in range(TILE_ROWS):
        tile_row_pixel_offset = tile_row * SpriteTile.ROW_COUNT * SpriteTile.COL_COUNT * TILE_COLS
        for tile_col in range(TILE_COLS):
            tile_index = tile_indices[tile_row][tile_col]
            if tile_index == 0xff or tile_index in tiles_found:
                continue

            tiles_found.add(tile_index)

            tile_col_pixel_offset = tile_col * SpriteTile.COL_COUNT
            for pixel_row in range(SpriteTile.ROW_COUNT):
                pixel_row_offset = pixel_row * SpriteTile.COL_COUNT * TILE_COLS
                for pixel_col in range(SpriteTile.COL_COUNT):
                    pixel = tile_row_pixel_offset + tile_col_pixel_offset + pixel_row_offset + pixel_col
                    tiles[tile_index].colors[pixel_row][pixel_col] = image_color_indices[pixel]
    return (tiles, tile_indices)

def write_palette(output_prefix, palette):
    palette.write_ppm(output_prefix + "_pal.ppm")
    with open(output_prefix + ".pal", "wb")as output:
        output.write(bytes(palette.data))

def write_sprite(output_prefix, sprite, tile_indices):
    sprite.write_ppm(output_prefix + "_bin.ppm", tile_indices)
    with open(output_prefix + ".bin", "wb") as output:
        output.write(bytes(sprite.data))

def convert(image_path):
    from PIL import Image
    image = Image.open(image_path)

    import os
    output_prefix = os.path.splitext(image_path)[0]

    palette = get_palette(image)
    write_palette(output_prefix, palette)

    from ...graphics.sprite import Sprite
    tiles, tile_indices = get_tiles(image)
    sprite = Sprite(tiles, palette)
    write_sprite(output_prefix, sprite, tile_indices)

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help = "Path to spritesheet png file to convert")

    args = parser.parse_args()
    convert(args.path)
