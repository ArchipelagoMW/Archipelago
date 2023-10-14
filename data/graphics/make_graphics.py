#!/usr/bin/env python3

import itertools
from pathlib import Path
from typing import Mapping, Sequence
from PIL import Image
import sys


# This script converts a PNG image into the uncompressed 4bpp indexed format
# Wario Land 4 uses. To do that, it uses a .txt file which maps RGB/RGBA colors
# to a 4-bit color index.
#
# The image is converted into 8x8 pixel tiles, which are then stored in a 1D
# array format in row major order, as in the simplified example here:
#
# 00000000 44444444
# 11111111 55555555
# 22222222 66666666
# 33333333 77777777
#
# 88888888 CCCCCCCC
# 99999999 DDDDDDDD
# AAAAAAAA EEEEEEEE
# BBBBBBBB FFFFFFFF


# https://docs.python.org/3.11/library/itertools.html
def batches(iterable, n):
    if n < 1:
        raise ValueError
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def main():
    file_directory = Path(__file__).parent
    in_path = file_directory / f'{sys.argv[1]}.png'
    palette_path = in_path.with_suffix('.txt')
    out_path = in_path.with_suffix('.bin')

    palette: Mapping[Sequence[int], int] = {}
    try:
        with open(palette_path, 'r') as file:
            for line in filter(None, map(str.strip, file.readlines())):
                if line.startswith('--'):
                    continue
                hexstr, gba = line.split(':')
                hexbytes = map(lambda x: int("".join(x), base=16), batches(hexstr[1:], 2))
                if len(hexstr) == 7:
                    hexbytes = itertools.chain(hexbytes, [255])
                gba = int(gba, base=16)
                palette[tuple(hexbytes)] = gba
    except FileNotFoundError:
        # Create the file automatically because we need it anyway and so the
        # script can helpfully list the colors that need to be mapped
        open(palette_path, 'w').close()

    source_image = Image.open(in_path).convert('RGBA')
    width, height = map(lambda x: x // 8, source_image.size)
    pixels = []
    bad_colors = set()
    for row in range(height):
        for column in range(width):
            for y in range(8):
                for x in range(8):
                    color = source_image.getpixel((8 * column + x, 8 * row + y))
                    try:
                        pixels.append(palette[color])
                    except KeyError:
                        bad_colors.add('#' + bytes(color).hex())

    if len(bad_colors) != 0:
        missing_colors = ' \n'.join(sorted(bad_colors))
        raise Exception(f'Not all colors mapped. Missing colors:\n{missing_colors}')

    with open(out_path, 'wb') as out_file:
        out_file.write(bytes(map(lambda p: p[1] << 4 | p[0], batches(pixels, 2))))


if __name__ == '__main__':
    main()
