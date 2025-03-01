import struct

from typing import Dict, List
from colorsys import rgb_to_hls, hls_to_rgb
import math

player_palette_set_offsets = {
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
}

diddy_palettes = {
    "original": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$0455","$087A","$10DF","$3DEF","$7FFF"
    ],
    "original_inactive": [
        "$0865","$0887","$0C89","$0CCC","$10EF","$14EC","$2150","$29B5","$2DF5","$3635","$084E","$0871","$0C95","$294A","$6B5A"
    ],
    "original_invincible": [
        "$1930","$1D97","$25FE","$2A7F","$32FF","$4AFF","$67FF","$7FFF","$7FFF","$7FFF","$191F","$1D5F","$2DFF","$7FFF","$7FFF"
    ],
    "original_frozen": [
        "$5923","$65C7","$766C","$7AAD","$7EEF","$7F51","$7F73","$7F96","$7FB8","$7FDB","$7F0D","$7F2F","$7F71","$7E8B","$7FFF"
    ],
    "original_slow": [
        "$0023","$000A","$0011","$0018","$001F","$00BF","$011F","$017F","$01DF","$023F","$0455","$087A","$10DF","$011F","$7FFF"
    ],
    "original_reversed": [
        "$0C01","$2804","$4028","$5C2C","$7851","$606C","$68B1","$7116","$795B","$7DBF","$5C0B","$6891","$7537","$68B1","$7FFF"
    ],
    "original_team_2": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$7C06","$7CC9","$7D6F","$3DEF","$7FFF"
    ],
    "original_team_2_inactive": [
        "$0865","$0887","$0C89","$0CCC","$10EF","$14EC","$2150","$29B5","$2DF5","$3635","$5424","$54A7","$550A","$294A","$56B5"
    ],
    "dkc_alt": [
        "$0466","$088A","$0CCD","$0D12","$1156","$1D52","$2DD9","$3A7F","$46DF","$4F5F","$01D5","$02BA","$039F","$3DEF","$7FFF"
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

dixie_palettes = {
    "original": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$0DAF","$1698","$2BFF","$24B2","$30F9","$497F","$0200","$7FFF"
    ],
    "original_inactive": [
        "$0444","$0487","$08AB","$08F1","$2172","$31F5","$3A75","$0D2A","$11D0","$1EB5","$188C","$24B1","$3115","$0561","$6B5A"
    ],
    "original_invincible": [
        "$14CC","$1598","$1A3F","$22FF","$6BFF","$7FFF","$7FFF","$2BBF","$3BFF","$63FF","$55DF","$725F","$7F3F","$13E4","$7FFF"
    ],
    "original_frozen": [
        "$5923","$6DE8","$7ECE","$7F11","$7F54","$7F97","$7FDB","$7E69","$7EED","$7F71","$7E06","$7EAB","$7F71","$7E8B","$7FFF"
    ],
    "original_slow": [
        "$0424","$002D","$0016","$001E","$007F","$013F","$01BF","$0016","$013C","$01BF","$00FB","$015D","$01BF","$015D","$7FFF"
    ],
    "original_reversed": [
        "$1003","$3408","$580D","$7C13","$7CB6","$7D59","$7DFC","$580D","$6D35","$7DFC","$580D","$6CB3","$7D59","$6CB3","$7FFF"
    ],
    "original_team_2": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$0C6F","$14B8","$295F","$3809","$50CF","$6995","$0240","$7FFF"
    ],
    "original_team_2_inactive": [
        "$0444","$0487","$08AB","$08F1","$2172","$31F5","$3A75","$0C6A","$1090","$1CF5","$2827","$348A","$452E","$0581","$6B5A"
    ],
    "dkc2_inverted": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$24B2","$30F9","$497F","$0DAF","$1698","$2BFF","$0200","$7FFF"
    ],
    "dkc2_team_2_inverted": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$3809","$50CF","$6995","$0C6F","$14B8","$295F","$0240","$7FFF"
    ],
    "dkc3_alt": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$0DAF","$1698","$2BFF","$40A9","$5530","$6DD6","$0200","$7FFF"
    ],
    "dkc3_alt_inverted": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$40A9","$5530","$6DD6","$0DAF","$1698","$2BFF","$0200","$7FFF"
    ],
    "gb_green": [
        "$08E2","$1986","$1986","$1986","$0AD1","$0AD1","$0AD1","$1986","$1986","$0AD1","$08E2","$08E2","$08E2","$08E2","$0AD1"
    ],
    "gb_grey": [
        "$0000","$318C","$318C","$318C","$56B5","$56B5","$56B5","$318C","$318C","$56B5","$0000","$0000","$0000","$0000","$56B5"
    ],
    "gbc_retro_blast": [
        "$006D","$01DC","$01DC","$01DC","$3AFF","$3AFF","$3AFF","$01DC","$01DC","$3AFF","$006D","$006D","$006D","$006D","$3AFF"
    ],
    "gba_blue": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$0430","$00BB","$2D7E","$48A3","$6582","$7E60","$04ED","$7FFF"
    ],
    "gba_green": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$28AA","$4110","$55F5","$0164","$0288","$036B","$04ED","$7FFF"
    ],
    "smb_mario": [
        "$10D7","$01CD","$01CD","$01CD","$129D","$129D","$129D","$01CD","$01CD","$129D","$10D7","$10D7","$10D7","$10D7","$129D"
    ],
    "smb_luigi": [
        "$0227","$129D","$129D","$129D","$7FFF","$7FFF","$7FFF","$129D","$129D","$7FFF","$0227","$0227","$0227","$0227","$7FFF"
    ],
    "golden": [
        "$05B3","$0615","$0657","$06B9","$06FA","$075C","$079E","$0658","$1B3C","$2BFF","$0658","$1B3C","$2BFF","$0658","$2BFF"
    ],
    "monochrome": [
        "$0842","$18C6","$2529","$39CE","$4E73","$6739","$77BD","$35AD","$5294","$77BD","$2529","$35AD","$4A52","$2529","$7FFF"
    ],
    "sepia": [
        "$0444","$10C8","$1D2D","$2DD1","$4675","$5F3A","$73BE","$29B0","$4696","$73BD","$1D2D","$29B0","$4255","$1D2D","$7FFF"
    ],
    "rottytops": [
        "$1081","$1CE2","$2543","$31C4","$3A25","$4686","$4EE7","$0164","$0288","$036B","$3809","$50CF","$6995","$001F","$7FFF"
    ],
    "miku": [
        "$14A0","$2D60","$4200","$5EE0","$4E75","$633B","$73BF","$4200","$62E0","$7360","$3149","$41CD","$66F6","$7E8B","$7FDD"
    ],
    "teto": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$0016","$109B","$211F","$1CE2","$2963","$35C4","$04ED","$7FFF"
    ],
    "sakura": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$04F1","$05D8","$029F","$1084","$2108","$2D6B","$7AAB","$7FFF"
    ],
    "nagisa": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$04F1","$05D8","$029F","$44C4","$4966","$4E08","$029F","$7FFF"
    ],
    "gothic": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$3809","$50CF","$6995","$1084","$2108","$2D6B","$0000","$7FFF"
    ],
    "toothpaste": [
        "$1C80","$2D20","$3DA0","$4E40","$5EC0","$6F60","$7FE0","$6A00","$7700","$7FE0","$2D6B","$5294","$739C","$7AAB","$7FFF"
    ],
    "whatsapp": [
        "$00C2","$0D45","$15C8","$226C","$2AEF","$3772","$3FF5","$15C8","$2AEF","$3FF5","$15C8","$2AEF","$3FF5","$15C8","$3FF5"
    ],
    "boca": [
        "$0424","$048A","$04F1","$095A","$2E1B","$46FF","$5BBF","$0DAF","$1698","$2BFF","$4000","$6000","$7C00","$0200","$7FFF"
    ],
    "bubblegum": [
        "$182D","$28D0","$3533","$45B6","$5639","$6A9C","$7B1F","$208F","$3974","$5639","$208F","$2D12","$3974","$28D0","$7B1F"
    ],
    "retro_frozen": [
        "$5923","$7E69","$7E69","$7E69","$7F97","$7F97","$7F97","$7E69","$7E69","$7F97","$5923","$5923","$5923","$5923","$7F97"
    ],
    "retro_reversed": [
        "$3408","$6CB3","$6CB3","$6CB3","$7DFC","$7DFC","$7DFC","$6CB3","$6CB3","$7DFC","$3408","$3408","$3408","$3408","$7DFC"
    ],
    "retro_slow": [
        "$002D","$007F","$007F","$007F","$01BF","$01BF","$01BF","$007F","$007F","$01BF","$002D","$002D","$002D","$002D","$01BF"
    ]
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
