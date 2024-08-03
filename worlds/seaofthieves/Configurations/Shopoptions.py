import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class ShopSanity(Choice):
    """Adds a client shop with items for sale"""
    display_name = "Shopsanity"
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4

    default = 1
