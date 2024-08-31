from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, DefaultOnToggle

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in sly1_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class StartingEpisode(Choice):
    """
    Determines which episode you will have the intro for at the beginning of the game.
    1 is Tides of Terror
    2 is Sunset Snake Eyes
    3 is Vicious Voodoo
    4 is Fire in the Sky
    """
    display_name = "Starting Episode"
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    default = 1

class IncludeHourglasses(DefaultOnToggle):
    """If enabled, Hourglasses are included in the locations."""
    display_name = "Include Hourglasses"

class AlwaysSpawnHourglasses(Toggle):
    """If enabled, Hourglasses will always be spawned even if the boss is not defeated."""
    display_name = "Always Spawn Hourglasses"

@dataclass
class Sly1Options(PerGameCommonOptions):
    StartingEpisode:            StartingEpisode
    IncludeHourglasses:         IncludeHourglasses
    AlwaysSpawnHourglasses:     AlwaysSpawnHourglasses

sly1_option_groups: Dict[str, List[Any]] = {
    "General Options": [StartingEpisode, IncludeHourglasses, AlwaysSpawnHourglasses]
}