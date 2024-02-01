from typing import Dict

from Options import Choice, Option, Toggle, Range, DeathLink


class StrawberriesRequired(Range):
    """How many Strawberries you must receive to finish"""
    display_name = "Strawberries Required"
    range_start = 0
    range_end = 30
    default = 20


celeste_64_options: Dict[str, type(Option)] = {
    "death_link": DeathLink,
    "strawberries_required": StrawberriesRequired,
}
