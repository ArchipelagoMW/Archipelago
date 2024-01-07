from typing import Dict, Tuple, List
from . import Names
from zlib import crc32
import struct

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

palette_pointers: Dict[str, List[int]] = {
    "Mega Buster": [0x3D314],
    "Atomic Fire":  [0x3D318],
    "Air Shooter":  [0x3D31C],
    "Leaf Shield":  [0x3D320],
    "Bubble Lead":  [0x3D324],
    "Quick Boomerang":  [0x3D328],
    "Time Stopper":  [0x3D32C],
    "Metal Blade":  [0x3D330],
    "Crash Bomber":  [0x3D334],
    "Item 1":  [0x3D338],
    "Item 2":  [0x3D33C],
    "Item 3": [0x3D340],
    "Heat Man": [0x34A6, 0x344E7],
    "Air Man": [0x74A6, 0x344EF],
    "Wood Man": [0x344F7],
    "Bubble Man": [0x344FF],
    "Quick Man": [0x34507],
    "Flash Man": [0x174A6, 0x3450F],
    "Metal Man": [0x34517],
    "Crash Man": [0x1F4DC, 0x3451F],
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

    # one final check, make sure we don't have two matching
    if color_1 == color_2:
        color_1 = 0x30  # color 1 to white works with about any paired color

    return color_1, color_2
