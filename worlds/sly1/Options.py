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
    """
    display_name = "Starting Episode"
    option_tides_of_terror = 1
    option_sunset_snake_eyes = 2
    option_vicious_voodoo = 3
    option_fire_in_the_sky = 4
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