from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice

class IncludeHourglasses(Choice):
    """If enabled, Hourglasses are included in the locations"""
    display_name = "Include Hourglasses"

class AlwaysSpawnHourglasses(Choice):
    """If enabled, Hourglasses will always be spawned even if the boss is not defeated"""
    display_name = "Always Spawn Hourglasses"

@dataclass
class Sly1Options(PerGameCommonOptions):
    IncludeHourglasses:         IncludeHourglasses
    AlwaysSpawnHourglasses:     AlwaysSpawnHourglasses