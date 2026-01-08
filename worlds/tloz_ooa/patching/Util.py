from .Constants import *
from ..data import ITEMS_DATA


def camel_case(text):
    if len(text) == 0:
        return text
    s = text.replace("-", " ").replace("_", " ").split()
    return s[0] + ''.join(i.capitalize() for i in s[1:])


def get_item_id_and_subid(item_name: str):
    if item_name == "Archipelago Item":
        return 0x41, 0x00
    elif item_name == "Archipelago Progression Item":
        return 0x41, 0x01

    item_data = ITEMS_DATA[item_name]
    item_id = item_data["id"]
    item_subid = item_data["subid"] if "subid" in item_data else 0x00
    return item_id, item_subid


def hex_str(value, size=1):
    if value < 0:
        if size == 1:
            value += 0x100
        elif size == 2:
            value += 0x10000
        else:
            raise Exception("Invalid size (should be 1 or 2)")
    return hex(value)[2:]

def get_available_random_colors_from_sprite_name(sprite_filename: str):
    """
    Parse the sprite filename to detect a potential "accepted colors suffix" which uses the following format:
    mysrite_<COLORS>.bin, where COLORS is a set of letters representing which colors can be rolled as random colors
    for that sprite.
    This was built for people who play with both random sprite & random color, but who want a subset of colors for
    each sprite (e.g. if they play a Tokay, they only want it orange or red).
    """
    CHARACTER_COLORS = {
        "r": "red",
        "g": "green",
        "b": "blue",
        "o": "orange",
    }
    filename_parts = sprite_filename.split("_")
    if len(filename_parts) <= 1:
        return list(CHARACTER_COLORS.values())

    # Get the final part of the filename and remove the ".bin" extension
    suffix = filename_parts[-1][0:-4]
    if len(suffix) > len(CHARACTER_COLORS.values()):
        return list(CHARACTER_COLORS.values())  # Too long, not a color suffix

    return [color for letter, color in CHARACTER_COLORS.items() if letter in suffix]
