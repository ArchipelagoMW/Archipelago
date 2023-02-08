import typing
from Options import Option, Range, Toggle, Choice


class MaxAnimAppear(Range):
    """Max amount of Animatronics that will appear at once."""
    display_name = "Max Animatronics Appearing"
    range_start = 1
    range_end = 4
    default = 4


class RandoCatalogueUnlocks(Toggle):
    """Turns catalogue unlocks into checks."""
    display_name = "Catalogue Rando"
    default = 1


class ToolUpgradeRando(Toggle):
    """Turns the speed upgrades for the tasks into checks."""
    display_name = "Speed Upgrade Rando"
    default = 0


class NightDifficulty(Choice):
    """Alters mechanics in the Night Mode to make it easier or harder."""
    display_name = "Night Mode Difficulty"
    option_normal = 0
    option_easy = 1
    default = 0


FFPS_options: typing.Dict[str, type(Option)] = {
    "max_animatronics_appearing":                           MaxAnimAppear,
    "catalogue_rando":                           RandoCatalogueUnlocks,
    "night_difficulty":                           NightDifficulty,
    "upgrade_rando":                           ToolUpgradeRando,
}
