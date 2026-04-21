import sys
from typing import TYPE_CHECKING
from . import names
from zlib import crc32
import struct
import logging

if TYPE_CHECKING:
    from . import MM3World
    from .rom import MM3ProcedurePatch

HTML_TO_NES: dict[str, int] = {
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

MM3_COLORS: dict[str, tuple[int, int]] = {
    names.gemini_laser: (0x30, 0x21),
    names.needle_cannon: (0x30, 0x17),
    names.hard_knuckle: (0x10, 0x01),
    names.magnet_missile: (0x10, 0x16),
    names.top_spin: (0x36, 0x00),
    names.search_snake: (0x30, 0x19),
    names.rush_coil: (0x30, 0x15),
    names.spark_shock: (0x30, 0x26),
    names.rush_marine: (0x30, 0x15),
    names.shadow_blade: (0x34, 0x14),
    names.rush_jet: (0x30, 0x15),
    names.needle_man_stage: (0x3C, 0x11),
    names.magnet_man_stage: (0x30, 0x15),
    names.gemini_man_stage: (0x30, 0x21),
    names.hard_man_stage: (0x10, 0xC),
    names.top_man_stage: (0x30, 0x26),
    names.snake_man_stage: (0x30, 0x29),
    names.spark_man_stage: (0x30, 0x26),
    names.shadow_man_stage: (0x30, 0x11),
    names.doc_needle_stage: (0x27, 0x15),
    names.doc_gemini_stage: (0x27, 0x15),
    names.doc_spark_stage: (0x27, 0x15),
    names.doc_shadow_stage: (0x27, 0x15),
}

MM3_KNOWN_COLORS: dict[str, tuple[int, int]] = {
    **MM3_COLORS,
    # Metroid series
    "Varia Suit": (0x27, 0x16),
    "Gravity Suit": (0x14, 0x16),
    "Phazon Suit": (0x06, 0x1D),
    # Street Fighter, technically
    "Hadouken": (0x3C, 0x11),
    "Shoryuken": (0x38, 0x16),
    # X Series
    "Z-Saber": (0x20, 0x16),
    "Helmet Upgrade": (0x20, 0x01),
    "Body Upgrade": (0x20, 0x01),
    "Arms Upgrade": (0x20, 0x01),
    "Plasma Shot Upgrade": (0x20, 0x01),
    "Stock Charge Upgrade": (0x20, 0x01),
    "Legs Upgrade": (0x20, 0x01),
    # X1
    "Homing Torpedo": (0x3D, 0x37),
    "Chameleon Sting": (0x3B, 0x1A),
    "Rolling Shield": (0x3A, 0x25),
    "Fire Wave": (0x37, 0x26),
    "Storm Tornado": (0x34, 0x14),
    "Electric Spark": (0x3D, 0x28),
    "Boomerang Cutter": (0x3B, 0x2D),
    "Shotgun Ice": (0x28, 0x2C),
    # X2
    "Crystal Hunter": (0x33, 0x21),
    "Bubble Splash": (0x35, 0x28),
    "Spin Wheel": (0x34, 0x1B),
    "Silk Shot": (0x3B, 0x27),
    "Sonic Slicer": (0x27, 0x01),
    "Strike Chain": (0x30, 0x23),
    "Magnet Mine": (0x28, 0x2D),
    "Speed Burner": (0x31, 0x16),
    # X3
    "Acid Burst": (0x28, 0x2A),
    "Tornado Fang": (0x28, 0x2C),
    "Triad Thunder": (0x2B, 0x23),
    "Spinning Blade": (0x20, 0x16),
    "Ray Splasher": (0x28, 0x17),
    "Gravity Well": (0x38, 0x14),
    "Parasitic Bomb": (0x31, 0x28),
    "Frost Shield": (0x23, 0x2C),
    # X4
    "Lightning Web": (0x3D, 0x28),
    "Aiming Laser": (0x2C, 0x14),
    "Double Cyclone": (0x28, 0x1A),
    "Rising Fire": (0x20, 0x16),
    "Ground Hunter": (0x2C, 0x15),
    "Soul Body": (0x37, 0x27),
    "Twin Slasher": (0x28, 0x00),
    "Frost Tower": (0x3D, 0x2C),
}

if "worlds.mm2" in sys.modules:
    # is this the proper way to do this? who knows!
    try:
        mm2 = sys.modules["worlds.mm2"]
        MM3_KNOWN_COLORS.update(mm2.color.MM2_COLORS)
        for item in MM3_COLORS:
            mm2.color.add_color_to_mm2(item, MM3_COLORS[item])
    except AttributeError:
        # pass through if an old MM2 is found
        pass

palette_pointers: dict[str, list[int]] = {
    "Mega Buster": [0x7C8A8, 0x4650],
    "Gemini Laser": [0x4654],
    "Needle Cannon": [0x4658],
    "Hard Knuckle": [0x465C],
    "Magnet Missile": [0x4660],
    "Top Spin": [0x4664],
    "Search Snake": [0x4668],
    "Rush Coil": [0x466C],
    "Spark Shock": [0x4670],
    "Rush Marine": [0x4674],
    "Shadow Blade": [0x4678],
    "Rush Jet": [0x467C],
    "Needle Man": [0x216C],
    "Magnet Man": [0x215C],
    "Gemini Man": [0x217C],
    "Hard Man": [0x2164],
    "Top Man": [0x2194],
    "Snake Man": [0x2174],
    "Spark Man": [0x2184],
    "Shadow Man": [0x218C],
    "Doc Robot": [0x20B8]
}


def add_color_to_mm3(name: str, color: tuple[int, int]) -> None:
    """
    Add a color combo for Mega Man 3 to recognize as the color to display for a given item.
    For information on available colors: https://www.nesdev.org/wiki/PPU_palettes#2C02
    """
    MM3_KNOWN_COLORS[name] = validate_colors(*color)


def extrapolate_color(color: int) -> tuple[int, int]:
    if color > 0x1F:
        color_1 = color
        color_2 = color_1 - 0x10
    else:
        color_2 = color
        color_1 = color_2 + 0x10
    return color_1, color_2


def validate_colors(color_1: int, color_2: int, allow_match: bool = False) -> tuple[int, int]:
    # Black should be reserved for outlines, a gray should suffice
    if color_1 in [0x0D, 0x0E, 0x0F, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_1 = 0x10
    if color_2 in [0x0D, 0x0E, 0x0F, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_2 = 0x10

    # one final check, make sure we don't have two matching
    if not allow_match and color_1 == color_2:
        color_1 = 0x30  # color 1 to white works with about any paired color

    return color_1, color_2


def expand_colors(color_1: int, color_2: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    if color_2 >= 0x30:
        color_a = color_b = color_2
    else:
        color_a = color_2 + 0x10
        color_b = color_2

    if color_1 < 0x10:
        color_c = color_1 + 0x10
        color_d = color_1
        color_e = color_1 + 0x20
    elif color_1 >= 0x30:
        color_c = color_1 - 0x10
        color_d = color_1 - 0x20
        color_e = color_1
    else:
        color_c = color_1
        color_d = color_1 - 0x10
        color_e = color_1 + 0x10

    return (0x30, color_a, color_b), (color_d, color_e, color_c)


def get_colors_for_item(name: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    if name in MM3_KNOWN_COLORS:
        return expand_colors(*MM3_KNOWN_COLORS[name])

    check_colors = {color: color in name.upper().replace(" ", '') for color in HTML_TO_NES}
    colors = [color for color in check_colors if check_colors[color]]
    if colors:
        # we have at least one color pattern matched
        if len(colors) > 1:
            # we have at least 2
            color_1 = HTML_TO_NES[colors[0]]
            color_2 = HTML_TO_NES[colors[1]]
        else:
            color_1, color_2 = extrapolate_color(HTML_TO_NES[colors[0]])
    else:
        # generate hash
        crc_hash = crc32(name.encode('utf-8'))
        hash_color = struct.pack("I", crc_hash)
        color_1 = hash_color[0] % 0x3F
        color_2 = hash_color[1] % 0x3F

        if color_1 < color_2:
            temp = color_1
            color_1 = color_2
            color_2 = temp

    color_1, color_2 = validate_colors(color_1, color_2)

    return expand_colors(color_1, color_2)


def parse_color(colors: list[str]) -> tuple[int, int]:
    color_a = colors[0]
    if color_a.startswith("$"):
        color_1 = int(color_a[1:], 16)
    else:
        # assume it's in our list of colors
        color_1 = HTML_TO_NES[color_a.upper()]

    if len(colors) == 1:
        color_1, color_2 = extrapolate_color(color_1)
    else:
        color_b = colors[1]
        if color_b.startswith("$"):
            color_2 = int(color_b[1:], 16)
        else:
            color_2 = HTML_TO_NES[color_b.upper()]
    return color_1, color_2


def write_palette_shuffle(world: "MM3World", rom: "MM3ProcedurePatch") -> None:
    palette_shuffle: int | str = world.options.palette_shuffle.value
    palettes_to_write: dict[str, tuple[int, int]] = {}
    if isinstance(palette_shuffle, str):
        color_sets = palette_shuffle.split(";")
        if len(color_sets) == 1:
            palette_shuffle = world.options.palette_shuffle.option_none
            # singularity is more correct, but this is faster
        else:
            palette_shuffle = world.options.palette_shuffle.options[color_sets.pop()]
        for color_set in color_sets:
            if "-" in color_set:
                character, color = color_set.split("-")
                if character.title() not in palette_pointers:
                    logging.warning(f"Player {world.player_name} "
                                    f"attempted to set color for unrecognized option {character}")
                colors = color.split("|")
                real_colors = validate_colors(*parse_color(colors), allow_match=True)
                palettes_to_write[character.title()] = real_colors
            else:
                # If color is provided with no character, assume singularity
                colors = color_set.split("|")
                real_colors = validate_colors(*parse_color(colors), allow_match=True)
                for character in palette_pointers:
                    palettes_to_write[character] = real_colors
        # Now we handle the real values
    if palette_shuffle != 0:
        if palette_shuffle > 1:
            if palette_shuffle == 3:
                # singularity
                real_colors = validate_colors(world.random.randint(0, 0x3F), world.random.randint(0, 0x3F))
                for character in palette_pointers:
                    if character not in palettes_to_write:
                        palettes_to_write[character] = real_colors
            else:
                for character in palette_pointers:
                    if character not in palettes_to_write:
                        real_colors = validate_colors(world.random.randint(0, 0x3F), world.random.randint(0, 0x3F))
                        palettes_to_write[character] = real_colors
        else:
            shuffled_colors = list(MM3_COLORS.values())[:-3]  # only include one Doc Robot
            shuffled_colors.append((0x2C, 0x11))  # Mega Buster
            world.random.shuffle(shuffled_colors)
            for character in palette_pointers:
                if character not in palettes_to_write:
                    palettes_to_write[character] = shuffled_colors.pop()

    for character in palettes_to_write:
        for pointer in palette_pointers[character]:
            rom.write_bytes(pointer + 2, bytes(palettes_to_write[character]))
