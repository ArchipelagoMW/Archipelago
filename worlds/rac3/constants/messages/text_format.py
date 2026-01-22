"""This file contains constants used to format the text displayed in the in-game pop-up messages"""

from BaseClasses import ItemClassification
from worlds.rac3.constants.messages.text_color import RAC3TEXTCOLOR


class RAC3TEXTFORMAT:
    """Enum for the byte value of a given text color"""
    NORMAL = 0x8
    BLUE = 0x9
    GREEN = 0xA
    MAGENTA = 0xB
    WHITE = 0xC
    BLACK = 0xD
    UNUSED_COLOR_1 = 0xE
    UNUSED_COLOR_2 = 0xF


COLOR_NAME_TO_BYTE = {
    RAC3TEXTCOLOR.NORMAL: RAC3TEXTFORMAT.NORMAL,
    RAC3TEXTCOLOR.BLUE: RAC3TEXTFORMAT.BLUE,
    RAC3TEXTCOLOR.GREEN: RAC3TEXTFORMAT.GREEN,
    RAC3TEXTCOLOR.MAGENTA: RAC3TEXTFORMAT.MAGENTA,
    RAC3TEXTCOLOR.WHITE: RAC3TEXTFORMAT.WHITE,
    RAC3TEXTCOLOR.BLACK: RAC3TEXTFORMAT.BLACK,
}
CLASSIFICATION_TO_COLOR = {
    ItemClassification.progression: RAC3TEXTCOLOR.MAGENTA,
    ItemClassification.progression_deprioritized: RAC3TEXTCOLOR.MAGENTA,
    ItemClassification.progression_deprioritized_skip_balancing: RAC3TEXTCOLOR.MAGENTA,
    ItemClassification.progression_skip_balancing: RAC3TEXTCOLOR.MAGENTA,
    ItemClassification.filler: RAC3TEXTCOLOR.WHITE,
    ItemClassification.trap: RAC3TEXTCOLOR.WHITE,
    ItemClassification.useful: RAC3TEXTCOLOR.BLUE,
}
