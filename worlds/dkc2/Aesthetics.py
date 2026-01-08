import struct

from typing import Dict, List
from colorsys import rgb_to_hls, hls_to_rgb
import math

palette_set_offsets = {
    "Diddy": 0x3D6484,
    "Diddy Inactive": 0x3D6484 + (0x1E*1),
    "Diddy Invincible": 0x3D6484 + (0x1E*7),
    "Diddy Frozen": 0x3D6484 + (0x1E*4),
    "Diddy Reversed": 0x3D6484 + (0x1E*6),
    "Diddy Slow": 0x3D6484 + (0x1E*5), 
    "Dixie": 0x3D6484 + (0x1E*8),
    "Dixie Inactive":  0x3D6484 + (0x1E*9),
    "Dixie Invincible": 0x3D6484 + (0x1E*15),
    "Dixie Frozen": 0x3D6484 + (0x1E*12),
    "Dixie Reversed": 0x3D6484 + (0x1E*14),
    "Dixie Slow": 0x3D6484 + (0x1E*13),
    "Rambi": 0x3D6D12,
    "Enguarde": 0x3D6F4C,
    "Squitter": 0x3D66A0,
    "Rattly": 0x3D67EA,
    "Squawks": 0x3D6826,
    "Quawks": 0x3D6844,
}

# Code taken from https://stackoverflow.com/a/69083087
def adjust_color(r, g, b, factor):
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    # Scale both luminescence and saturation but don't adjust hue
    l = max(min(l * factor, 1.0), 0.0)
    s = max(min(s * factor * 2.0/3.0, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)
    
def lighten_color(r, g, b, factor=0.25):
    return adjust_color(r, g, b, 1 + factor)
    
def darken_color(r, g, b, factor=0.25):
    return adjust_color(r, g, b, 1 - factor)

def get_palette_bytes(palette: Dict[str, List], adjust: int = 0) -> bytearray:
    output_data = bytearray()
    for hexcol in palette:
        if hexcol.startswith("$"):
            hexcol = hexcol.replace("$", "")
            colint = int(hexcol, 16)
            if adjust != 0:
                col = bgr555_to_rgb888(colint)
                if adjust > 0:
                    col = lighten_color(col[0], col[1], col[2], adjust / 100)
                else:
                    col = darken_color(col[0], col[1], col[2], abs(adjust / 100))
                byte_data = rgb888_to_bgr555(col[0], col[1], col[2])
                output_data.extend(bytearray(byte_data))
            else:
                output_data.extend(bytearray(struct.pack("H", colint)))
        else:
            if hexcol.startswith("#"):
                hexcol = hexcol.replace("#", "")
            colint = int(hexcol, 16)
            col = ((colint & 0xFF0000) >> 16, (colint & 0xFF00) >> 8, colint & 0xFF)
            col = tuple(x for x in col)
            if adjust > 0:
                col = lighten_color(col[0], col[1], col[2])
            elif adjust < 0:
                col = darken_color(col[0], col[1], col[2])
            byte_data = rgb888_to_bgr555(col[0], col[1], col[2])
            output_data.extend(bytearray(byte_data))
    return output_data

def rgb888_to_bgr555(red, green, blue) -> bytes:
    red = red >> 3
    green = green >> 3
    blue = blue >> 3
    outcol = (blue << 10) + (green << 5) + red
    return struct.pack("H", outcol)
    
def bgr555_to_rgb888(color: int) -> tuple:
    blue = ((color & 0x7C00) >> 10) << 3
    green = ((color & 0x03E0) >> 5) << 3
    red = (color & 0x001F) << 3
    red += math.floor(red / 32)
    green += math.floor(green / 32)
    blue += math.floor(blue / 32)
    return (red, green, blue)
