from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in hexcells_infinite_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

# class StartingChapter(Choice):
#     """
#     Determines which chapter you'll start with.
#     When you grab choice you'll get the associated number.
#     IE: If the player chooses the sewer then when you go to call StartingChapter you'll get 3
#     When displaying the options names on the site, _ will become spaces and the word option will go away.
#     """
#     display_name = "Starting Chapter"
#     option_green_hill_zone = 1
#     option_romania = 2
#     option_the_sewer = 3
#     default = 1

# class ExtraLocations(Toggle):
#     """
#     This will enable the extra locations option. Toggle is just true or false.
#     """
#     display_name = "Add Extra Locations"

# class TrapChance(Range):
#     """
#     Determines the chance for any junk item to become a trap.
#     Set it to 0 for no traps.
#     Range is in fact a range. You can set the limits and its default.
#     """
#     display_name = "Trap Chance"
#     range_start = 0
#     range_end = 100
#     default = 0

# class ForcefemTrapWeight(Range):
#     """
#     The weight of forcefem traps in the trap pool.
#     Does really cool stuff to your body.
#     """
#     display_name = "Forcefem Trap Weight"
#     range_start = 0
#     range_end = 100
#     default = 100

# class SpeedChangeTrapWeight(Range):
#     """
#     The weight of speed change traps in the trap pool.
#     Speed change traps change the game speed for x seconds.
#     """
#     display_name = "Speed Change Trap Weight"
#     range_start = 0
#     range_end = 100
#     default = 25


class RequirePerfectClears(Toggle):
    """
    This determines if levels need to be cleared with no mistakes to send out an item. 
    """
    display_name = "Require Perfect Clears"

class PuzzleOptions(Choice):
    """
    This determines how puzzles will be randomized.
    Vanilla: No puzzle randomization, all puzzles are as they are in the base game.
    Randomized: Every level has a randomly generated puzzle.
    True Randomized: Every level has a randomly generated puzzle, that is re-randomized if you leave the level.
    """
    display_name = "Puzzle Options"
    option_vanilla = 1
    option_randomized = 2
    option_true_randomized = 3
    default = 1


class EnableShields(Toggle):
    """
    When enabled, puzzle solves that involve mistakes will give 1 shield (max of 1 shield). Shields are used to block mistakes on future levels. This pairs well with True Randomization. 
    """
    display_name = "Enable Shields"

    
class LevelUnlockType(Choice):
    """
    This determines how levels will be unlocked.
    Vanilla: Levels are unlocked in groups of 6, with 6 groups total.
    Individual: Levels are unlocked individually, with individual gem amount requirements.
    """
    display_name = "Level Unlock Type"
    option_vanilla = 1
    option_individual = 2
    default = 1

@dataclass
class HexcellsInfiniteOptions(PerGameCommonOptions):

    # StartingChapter:            StartingChapter
    # ExtraLocations:             ExtraLocations
    # TrapChance:                 TrapChance
    # ForcefemTrapWeight:         ForcefemTrapWeight
    # SpeedChangeTrapWeight:      SpeedChangeTrapWeight
    RequirePerfectClears:         RequirePerfectClears
    PuzzleOptions:                PuzzleOptions
    EnableShields:                EnableShields
    LevelUnlockType:              LevelUnlockType


# # This is where you organize your options
# # Its entirely up to you how you want to organize it
hexcells_infinite_option_groups: Dict[str, List[Any]] = {
    "General Options": [RequirePerfectClears, PuzzleOptions, EnableShields, LevelUnlockType],
    # "Trap Options": [TrapChance, ForcefemTrapWeight, SpeedChangeTrapWeight]
}