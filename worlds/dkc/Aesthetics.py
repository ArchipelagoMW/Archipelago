import struct

from typing import Dict, List
from colorsys import rgb_to_hls, hls_to_rgb
import math

player_palette_set_offsets = {
    "Diddy": 0x3C8422,
    "Diddy Inactive": 0x3C8422 + (0x1E*1),
    "Donkey": 0x3C8422 + (0x1E*4),
    "Donkey Inactive":  0x3C8422 + (0x1E*5),
}

diddy_palettes = {
    "original": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$0455","$087A","$10DF","$3DEF","$7FFF"
    ],
    "original_inactive": [
        "$0866","$0888","$0CAB","$0CEE","$1112","$190F","$2593","$31F9","$3659","$3E99","$0871","$0874","$10B9","$318C","$6739"
    ],
    "original_team_2": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$01D5","$02BA","$039F","$3DEF","$7FFF"
    ],
    "original_team_2_inactive": [
        "$0866","$0888","$0CAB","$0CEE","$1112","$190F","$2593","$31F9","$3659","$3E99","$0571","$0615","$06D9","$318C","$6739"
    ],
    "dkc2_invincible": [
        "$1930","$1D97","$25FE","$2A7F","$32FF","$4AFF","$67FF","$7FFF","$7FFF","$7FFF","$191F","$1D5F","$2DFF","$7FFF","$7FFF"
    ],
    "dkc2_team_2": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$7C06","$7CC9","$7D6F","$3DEF","$7FFF"
    ],
    "dkc2_team_2_inactive": [
        "$0865","$0887","$0C89","$0CCC","$10EF","$14EC","$2150","$29B5","$2DF5","$3635","$5424","$54A7","$550A","$294A","$56B5"
    ],
    "dkc2_frozen": [
        "$5923","$65C7","$766C","$7AAD","$7EEF","$7F51","$7F73","$7F96","$7FB8","$7FDB","$7F0D","$7F2F","$7F71","$7E8B","$7FFF"
    ],
    "dkc2_slow": [
        "$0023","$000A","$0011","$0018","$001F","$00BF","$011F","$017F","$01DF","$023F","$0455","$087A","$10DF","$011F","$7FFF"
    ],
    "dkc2_reversed": [
        "$0C01","$2804","$4028","$5C2C","$7851","$606C","$68B1","$7116","$795B","$7DBF","$5C0B","$6891","$7537","$68B1","$7FFF"
    ],
    "dkc3_kiddy": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$55AB","$6AAD","$7FAF","$3DEF","$7FFF"
    ],
    "dkc3_kiddy_alt": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$2624","$3F09","$57ED","$3DEF","$7FFF"
    ],
    "gb_green": [
        "$08E2","$08E2","$08E2","$1986","$1986","$1986","$0AD1","$0AD1","$0AD1","$0AD1","$1986","$0AD1","$0AD1","$1986","$0AD1"
    ],
    "gb_gray": [
        "$0000","$0000","$0000","$318C","$318C","$318C","$56B5","$56B5","$56B5","$56B5","$318C","$56B5","$56B5","$318C","$56B5"
    ],
    "gbc_retro_blast": [
        "$006D","$006D","$006D","$01DC","$01DC","$01DC","$3AFF","$3AFF","$3AFF","$3AFF","$01DC","$3AFF","$3AFF","$01DC","$3AFF"
    ],
    "golden": [
        "$05B3","$09F4","$0E36","$1277","$16B8","$1AFA","$1F3B","$237C","$27BE","$2BFF","$0658","$1B3C","$2BFF","$0658","$2BFF"
    ],
    "monochrome": [
        "$0842","$18C6","$2529","$39CE","$4E73","$35AD","$4631","$56B5","$6739","$77BD","$2529","$35AD","$4A52","$2529","$7FFF"
    ],
    "sepia": [
        "$0886","$10C9","$190B","$214E","$29B0","$298F","$3E34","$52D8","$5F1A","$6B7C","$150B","$1D4D","$2DB0","$35F2","$7FFF"
    ],
    "smb_mario": [
        "$10D7","$10D7","$10D7","$01CD","$01CD","$01CD","$129D","$129D","$129D","$129D","$01CD","$129D","$129D","$01CD","$129D"
    ],
    "smb_luigi": [
        "$0227","$0227","$0227","$129D","$129D","$129D","$7FFF","$7FFF","$7FFF","$7FFF","$129D","$7FFF","$7FFF","$129D","$7FFF"
    ],
    "toothpaste": [
        "$1C80","$28E0","$3140","$3DA0","$4A00","$5260","$5EC0","$6B20","$7380","$7FE0","$2D6B","$5294","$739C","$7AAB","$7FFF"
    ],
    "whatsapp": [
        "$00C2","$0924","$0D86","$15C8","$1E2B","$228D","$2AEF","$3351","$3793","$3FF5","$228D","$2AEF","$3351","$0D86","$3FF5"
    ],
    "bubblegum": [
        "$182D","$208F","$2CF1","$3533","$4195","$4DD7","$5639","$627B","$6EDD","$7B1F","$208F","$2CF1","$3533","$3516","$7B1F"
    ],
    "retro_frozen": [
        "$5923","$5923","$5923","$7E69","$7E69","$7E69","$7F97","$7F97","$7F97","$7F97","$7E69","$7F97","$7F97","$7E69","$7F97"
    ],
    "retro_reversed": [
        "$3408","$3408","$3408","$6CB3","$6CB3","$6CB3","$7DFC","$7DFC","$7DFC","$7DFC","$6CB3","$7DFC","$7DFC","$6CB3","$7DFC"
    ],
    "retro_slow": [
        "$002D","$002D","$002D","$007F","$007F","$007F","$01BF","$01BF","$01BF","$01BF","$007F","$01BF","$01BF","$007F","$01BF"
    ],
    "rottytops": [
        "$1081","$18C2","$1D02","$2543","$2984","$31C4","$3A05","$3E46","$46A6","$4EE7","$3809","$48AD","$5911","$2984","$7FFF"
    ]

}

donkey_palettes = {
    "original": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$001F","$0010","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "original_inactive": [
        "$0463","$0487","$04AA","$04ED","$0511","$0553","$0595","$0439","$042D","$04AF","$2DB8","$3E18","$4A78","$56D8","$6739"
    ],
    "original_team_2": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$039F","$01D5","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "original_team_2_inactive": [
        "$0463","$0487","$04AA","$04ED","$0511","$0553","$0595","$06D9","$0571","$04AF","$2DB8","$3E18","$4A78","$56D8","$6739"
    ],
    "dkc2_diddy_alt": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$7599","$68CF","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "dkc3_kiddy": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$7AEA","$55AB","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "dkc3_kiddy_alt": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$57ED","$2624","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "black_tie": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$294A","$1084","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "white_tie": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$7FFF","$6318","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "purple_tie": [
        "$0043","$0088","$00CC","$0111","$0155","$0198","$01DA","$7599","$68CF","$00D3","$3A1F","$4A9F","$5F1F","$6F9F","$7FFF"
    ],
    "dkc2_frozen": [
        "$5923","$65C7","$766C","$7AAD","$7EEF","$7F51","$7F73","$7FDB","$65C7","$7F0D","$7F73","$7F96","$7FB8","$7FDB","$7FFF"
    ],
    "dkc2_reversed": [
        "$1003","$3408","$580D","$7C13","$7CB6","$7D59","$7DFC","$7EBD","$580D","$7CB6","$7D58","$7DDA","$7E7C","$7EFE","$7FFF"
    ],
    "dkc2_slow": [
        "$0424","$002D","$0016","$001E","$007F","$013F","$01BF","$007F","$002D","$001E","$08BE","$155F","$1DDF","$267F","$7FFF"
    ],
    "golden": [
        "$05B3","$09F4","$0E36","$1277","$16B8","$1AFA","$1F3B","$2BFF","$0658","$0658","$1F3B","$237C","$27BE","$2BFF","$5FFF"
    ],
    "monochrome": [
        "$1CE7","$2529","$294A","$318C","$39CE","$3DEF","$4631","$6B5A","$2108","$318C","$4631","$5294","$5EF7","$6B5A","$77BD"
    ],
    "gb_green": [
        "$08E2","$08E2","$08E2","$08E2","$1986","$1986","$1986","$0AD1","$08E2","$1986","$1986","$0AD1","$0AD1","$0AD1","$0AD1"
    ],
    "gb_gray": [
        "$0000","$0000","$0000","$0000","$318C","$318C","$318C","$56B5","$0000","$318C","$318C","$56B5","$56B5","$56B5","$56B5"
    ],
    "gbc_retro_blast": [
        "$006D","$006D","$006D","$006D","$01DC","$01DC","$01DC","$3AFF","$006D","$01DC","$01DC","$3AFF","$3AFF","$3AFF","$3AFF"
    ],
}

# Code taken from https://stackoverflow.com/a/69083087
def adjust_color(r, g, b, factor):
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
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
