from dataclasses import dataclass
from typing import Dict

from Options import Choice, Option, Toggle, Range, DeathLink, PerGameCommonOptions


class StrawberriesRequired(Range):
    """How many Strawberries you must receive to finish"""
    display_name = "Strawberries Required"
    range_start = 0
    range_end = 20
    default = 15


@dataclass
class Celeste64Options(PerGameCommonOptions):
    death_link: DeathLink
    strawberries_required: StrawberriesRequired
