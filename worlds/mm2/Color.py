import typing
from typing import Dict, Tuple, List, TYPE_CHECKING, Union
from . import Names
from zlib import crc32
import struct
import logging

if TYPE_CHECKING:
    from . import MM2World
    from .Rom import MM2ProcedurePatch

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

MM2_COLORS: Dict[str, Tuple[int, int]] = {
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
    Names.heat_man_stage: (0x28, 0x15),
    Names.air_man_stage: (0x28, 0x11),
    Names.wood_man_stage: (0x36, 0x17),
    Names.bubble_man_stage: (0x30, 0x19),
    Names.quick_man_stage: (0x28, 0x15),
    Names.flash_man_stage: (0x30, 0x12),
    Names.metal_man_stage: (0x28, 0x15),
    Names.crash_man_stage: (0x30, 0x16)
}

MM2_KNOWN_COLORS: Dict[str, Tuple[int, int]] = {
    **MM2_COLORS
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
    "Heat Man": [0x34B6, 0x344F7],
    "Air Man": [0x74B6, 0x344FF],
    "Wood Man": [0xB4EC, 0x34507],
    "Bubble Man": [0xF4B6, 0x3450F],
    "Quick Man": [0x134C8, 0x34517],
    "Flash Man": [0x174B6, 0x3451F],
    "Metal Man": [0x1B4A4, 0x34527],
    "Crash Man": [0x1F4EC, 0x3452F],
}


def add_color_to_mm2(name: str, color: Tuple[int, int]):
    """
    Add a color combo for Mega Man 2 to recognize as the color to display for a given item.
    For information on available colors: https://www.nesdev.org/wiki/PPU_palettes#2C02
    """
    MM2_KNOWN_COLORS[name] = validate_colors(*color)


def extrapolate_color(color: int):
    if color > 0x1F:
        color_1 = color
        color_2 = color_1 - 0x10
    else:
        color_2 = color
        color_1 = color_2 + 0x10
    return color_1, color_2


def validate_colors(color_1: int, color_2: int):
    # Black should be reserved for outlines, a gray should suffice
    if color_1 in [0x0D, 0x0E, 0x0F, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_1 = 0x10
    if color_2 in [0x0D, 0x0E, 0x0F, 0x1E, 0x2E, 0x3E, 0x1F, 0x2F, 0x3F]:
        color_2 = 0x10

    # one final check, make sure we don't have two matching
    if color_1 == color_2:
        color_1 = 0x30  # color 1 to white works with about any paired color

    return color_1, color_2


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
            color_1, color_2 = extrapolate_color(HTML_TO_NES[colors[0]])
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

    color_1, color_2 = validate_colors(color_1, color_2)

    return color_1, color_2


def parse_color(colors: typing.List[str]):
    color_1 = colors[0]
    if color_1.startswith("$"):
        color_1 = int(color_1[1:], 16)
    else:
        # assume it's in our list of colors
        color_1 = HTML_TO_NES[color_1.upper()]

    if len(colors) == 1:
        color_2 = extrapolate_color(color_1)
    else:
        color_2 = colors[1]
        if color_2.startswith("$"):
            color_2 = int(color_2[1:])
        else:
            color_2 = HTML_TO_NES[color_2.upper()]
    return color_1, color_2


def write_palette_shuffle(world: "MM2World", rom: "MM2ProcedurePatch"):
    palette_shuffle: Union[int, str] = world.options.palette_shuffle.value
    palettes_to_write: Dict[str, Tuple[int, int]] = {}
    if isinstance(palette_shuffle, str):
        color_sets = palette_shuffle.split(";")
        if len(color_sets) == 1:
            palette_shuffle = world.options.palette_shuffle.option_none
            # singularity is more correct, but this is faster
        else:
            palette_shuffle = world.options.palette_shuffle.options[color_sets.pop()]
        for color_set in color_sets:
            if "-" in color_set:
                character, colors = color_set.split("-")
                if character.title() not in palette_pointers:
                    logging.warning(f"Player {world.multiworld.get_player_name(world.player)} "
                                    f"attempted to set color for unrecognized option {character}")
                colors = colors.split("|")
                colors = parse_color(colors)
                palettes_to_write[character.title()] = colors
            else:
                # If color is provided with no character, assume singularity
                colors = color_set.split("|")
                colors = parse_color(colors)
                for character in palette_pointers:
                    palettes_to_write[character] = colors
        # Now we handle the real values
    if palette_shuffle != 0:
        if palette_shuffle > 1:
            if palette_shuffle == 3:
                # singularity
                colors = validate_colors(world.random.randint(0, 0x3F), world.random.randint(0, 0x3F))
                for character in palette_pointers:
                    if character not in palettes_to_write:
                        palettes_to_write[character] = colors
            else:
                for character in palette_pointers:
                    if character not in palettes_to_write:
                        colors = validate_colors(world.random.randint(0, 0x3F), world.random.randint(0, 0x3F))
                        palettes_to_write[character] = colors
        else:
            colors = list(MM2_COLORS.values())
            colors.append((0x2C, 0x11))  # Mega Buster
            world.random.shuffle(colors)
            for character in palette_pointers:
                if character not in palettes_to_write:
                    palettes_to_write[character] = colors.pop()

    for character in palettes_to_write:
        for pointer in palette_pointers[character]:
            rom.write_bytes(pointer, bytes(palettes_to_write[character]))

        if character == "Atomic Fire":
            # special case, we need to update Atomic Fire's flashing routine
            rom.write_byte(0x3DE4A, palettes_to_write[character][1])
            rom.write_byte(0x3DE4C, palettes_to_write[character][1])
