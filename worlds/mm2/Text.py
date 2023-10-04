import struct
from typing import Tuple, Dict
from zlib import crc32
from . import Names


MM2_WEAPON_ENCODING: Dict[str, int] = {
    ' ': 0x40,
    'A': 0x41,
    'B': 0x42,
    'C': 0x43,
    'D': 0x44,
    'E': 0x45,
    'F': 0x46,
    'G': 0x47,
    'H': 0x48,
    'I': 0x49,
    'J': 0x4A,
    'K': 0x4B,
    'L': 0x4C,
    'M': 0x4D,
    'N': 0x4E,
    'O': 0x4F,
    'P': 0x50,
    'Q': 0x51,
    'R': 0x52,
    'S': 0x53,
    'T': 0x54,
    'U': 0x55,
    'V': 0x56,
    'W': 0x57,
    'X': 0x58,
    'Y': 0x59,
    'Z': 0x5A,
    # 0x5B is the small r in Dr Light
    '.': 0x5C,
    ',': 0x5D,
    '\'': 0x5E,
    '!': 0x5F,
    '(': 0x60,
    ')': 0x61,
    '#': 0x62,
    '$': 0x63,
    '%': 0x64,
    '&': 0x65,
    '*': 0x66,
    '+': 0x67,
    '/': 0x68,
    '\\': 0x69,
    ':': 0x6A,
    ';': 0x6B,
    '<': 0x6C,
    '>': 0x6D,
    '=': 0x6E,
    '?': 0x6F,
    '@': 0x70,
    '[': 0x71,
    ']': 0x72,
    '^': 0x73,
    '_': 0x74,
    '`': 0x75,
    '{': 0x76,
    '}': 0x77,
    '|': 0x78,
    '~': 0x79,
    '\"': 0x92,
    '-': 0x94,
    '0': 0xA0,
    '1': 0xA1,
    '2': 0xA2,
    '3': 0xA3,
    '4': 0xA4,
    '5': 0xA5,
    '6': 0xA6,
    '7': 0xA7,
    '8': 0xA8,
    '9': 0xA9,
}

HTML_TO_NES: Dict[str, int] = {
    'SNOW': 0x20,
    'LINEN': 0x36,
    'SEASHELL': 0x36,
    'AZURE': 0x3C,
    'LAVENDER': 0x33,
    'WHITE': 0x30,
    'BLACK': 0x0F,
    'GREY': 0x00,
    'GRAY': 0x00,
    'ROYALBLUE': 0x12,
    'BLUE': 0x11,
    'SKYBLUE': 0x21,
    'LIGHTBLUE': 0x31,
    'TURQUOISE': 0x2B,
    'CYAN': 0x2C,
    'AQUAMARINE': 0x3B,
    'DARKGREEN': 0x0A,
    'GREEN': 0x1A,
    'YELLOW': 0x28,
    'GOLD': 0x28,
    'WHEAT': 0x37,
    'TAN': 0x37,
    'CHOCOLATE': 0x07,
    'BROWN': 0x07,
    'SALMON': 0x26,
    'ORANGE': 0x27,
    'CORAL': 0x36,
    'TOMATO': 0x16,
    'RED': 0x16,
    'PINK': 0x25,
    'MAROON': 0x06,
    'MAGENTA': 0x24,
    'FUSCHIA': 0x24,
    'VIOLET': 0x24,
    'PLUM': 0x33,
    'PURPLE': 0x14,
    'THISTLE': 0x34,
    'DARKBLUE': 0x01,
    'SILVER': 0x10,
    'NAVY': 0x02,
    'TEAL': 0x1C,
    'OLIVE': 0x18,
    'LIME': 0x2A,
    'AQUA': 0x2C,
    # can add more as needed
}

MM2_KNOWN_COLORS: Dict[str, Tuple[int, int]] = {
    Names.atomic_fire: (0x28, 0x15),
    Names.air_shooter: (0x20, 0x11),
    Names.leaf_shield: (0x20, 0x19),
    Names.bubble_lead: (0x20, 0x00),
    Names.time_stopper: (0x34, 0x25),
    Names.quick_boomerang: (0x34, 0x14),
    Names.metal_blade: (0x37, 0x18),
    Names.crash_bomber: (0x20, 0x26),
    Names.item_1: (0x20, 0x16),
    Names.item_2: (0x20, 0x16),
    Names.item_3: (0x20, 0x16),
}


def add_color_to_mm2(name: str, color: Tuple[int, int]):
    """
    Add a color combo for Mega Man 2 to recognize as the color to display for a given item.
    For information on available colors: https://www.nesdev.org/wiki/PPU_palettes#2C02
    """
    MM2_KNOWN_COLORS[name] = color


def get_colors_for_item(name: str) -> Tuple[int, int]:
    if name in MM2_KNOWN_COLORS:
        return MM2_KNOWN_COLORS[name]

    check_colors = {color: color in name.upper().replace(" ", '') for color in HTML_TO_NES}
    colors = [color for color in check_colors if check_colors[color]]
    if colors:
        # we have at least one color pattern matched
        if len(colors) > 1:
            # we have at least 2
            color_1 = HTML_TO_NES[colors[0]]
            color_2 = HTML_TO_NES[colors[1]]
        else:
            if HTML_TO_NES[colors[0]] > 0x1F:
                color_1 = HTML_TO_NES[colors[0]]
                color_2 = color_1 - 0x10
            else:
                color_2 = HTML_TO_NES[colors[0]]
                color_1 = color_2 + 0x10
    else:
        # generate hash
        crc_hash = crc32(name.encode('utf-8'))
        colors = struct.pack("I", crc_hash)
        color_1 = colors[0] % 0x3F
        color_2 = colors[1] % 0x3F
        
    if color_1 < color_2:
        temp = color_1
        color_1 = color_2
        color_2 = temp

    if color_1 in [0x0D, 0x0E, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_1 = 0x0F
    if color_2 in [0x0D, 0x0E, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_2 = 0x0F

    return color_1, color_2


class MM2TextEntry:
    def __init__(self, text="", coords=0x0B):
        self.target_area: int = 0x25  # don't change
        self.coords: int = coords  # 0xYX, Y can only be increments of 0x20
        self.text: str = text

    def resolve(self) -> bytes:
        data = bytearray()
        data.append(self.target_area)
        data.append(self.coords)
        data.extend([MM2_WEAPON_ENCODING[x] for x in self.text.upper()])
        data.extend([0x40] * (14 - len(self.text)))
        return data
