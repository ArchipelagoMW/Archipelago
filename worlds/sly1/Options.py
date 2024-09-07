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
    option_tide_of_terror = 1
    option_sunset_snake_eyes = 2
    option_vicious_voodoo = 3
    option_fire_in_the_sky = 4
    option_all = 6
    default = 1

class AvoidEarlyBK(Toggle):
    """
    Determines if you will start with 1 key for your chosen starting episode.
    If all is selected, you are given 1 key for a random episode.
    """
    display_name = "Avoid Early BK"

class IncludeHourglasses(Toggle):
    """
    If enabled, Hourglasses are included in the locations.
    If Hourglasses are disabled then there are more items than locations for this game alone.
    """
    display_name = "Include Hourglasses"

@dataclass
class Sly1Options(PerGameCommonOptions):
    StartingEpisode:            StartingEpisode
    IncludeHourglasses:         IncludeHourglasses
    AvoidEarlyBK:               AvoidEarlyBK

sly1_option_groups: Dict[str, List[Any]] = {
    "General Options": [StartingEpisode, IncludeHourglasses]
}

slot_data_options: List[str] = {
    "StartingEpisode",
    "IncludeHourglasses",
    "AvoidEarlyBK"
}