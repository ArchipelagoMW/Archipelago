from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in ap_skeleton_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class StartingChapter(Choice):
    """
    Determines which chapter you'll start with.
    When you grab choice you'll get the associated number.
    IE: If the player chooses the sewer then when you go to call StartingChapter you'll get 3
    When displaying the options names on the site, _ will become spaces and the word option will go away.
    """
    display_name = "Starting Chapter"
    option_green_hill_zone = 1
    option_romania = 2
    option_the_sewer = 3
    default = 1

class ExtraLocations(Toggle):
    """
    This will enable the extra locations option. Toggle is just true or false.
    """
    display_name = "Add Extra Locations"

class TrapChance(Range):
    """
    Determines the chance for any junk item to become a trap.
    Set it to 0 for no traps.
    Range is in fact a range. You can set the limits and its default.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

class ForcefemTrapWeight(Range):
    """
    The weight of forcefem traps in the trap pool.
    Does really cool stuff to your body.
    """
    display_name = "Forcefem Trap Weight"
    range_start = 0
    range_end = 100
    default = 100

class SpeedChangeTrapWeight(Range):
    """
    The weight of speed change traps in the trap pool.
    Speed change traps change the game speed for x seconds.
    """
    display_name = "Speed Change Trap Weight"
    range_start = 0
    range_end = 100
    default = 25

@dataclass
class APSkeletonOptions(PerGameCommonOptions):
    StartingChapter:            StartingChapter
    ExtraLocations:             ExtraLocations
    TrapChance:                 TrapChance
    ForcefemTrapWeight:         ForcefemTrapWeight
    SpeedChangeTrapWeight:      SpeedChangeTrapWeight

# This is where you organize your options
# Its entirely up to you how you want to organize it
ap_skeleton_option_groups: Dict[str, List[Any]] = {
    "General Options": [StartingChapter, ExtraLocations],
    "Trap Options": [TrapChance, ForcefemTrapWeight, SpeedChangeTrapWeight]
}