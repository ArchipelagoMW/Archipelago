import typing

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionList

class IncludeMissions(Range):
    """
    Allows logic to place items in a range of Missions for each level
    Each mission setting includes lower settings
    1: Base Story Missions
    2: 100 Ring Missions
    3: Lost Chao Missions
    4: Timer Missions
    5: Hard Mode Missions
    """
    display_name = "Include Missions"
    range_start = 1
    range_end = 5
    default = 2

class EmblemPercentageForCannonsCore(Range):
    """
    Allows logic to gate the final mission behind a number of Emblems
    """
    display_name = "Emblem Percentage for Cannons Core"
    range_start = 0
    range_end = 100
    default = 60

class NumberOfLevelGates(Range):
    """
    Allows logic to gate some levels behind emblem requirements
    """
    display_name = "Number of Level Gates"
    range_start = 0
    range_end = 5
    default = 3

class LevelGateDistribution(Choice):
    """
    Determines how levels are distributed between level gate regions
    Early: Earlier regions will have more levels than later regions
    Even: Levels will be evenly distributed between all regions
    Late: Later regions will have more levels than earlier regions
    """
    display_name = "Level Gate Distribution"
    option_early = 0
    option_even = 1
    option_late = 2
    default = 1

class MusicShuffle(Choice):
    """
    What type of Music Shuffle is used
    Off: No music is shuffled.
    Levels: Level music is shuffled.
    Full: Level, Menu, and Additional music is shuffled.
    """
    display_name = "Music Shuffle Type"
    option_none = 0
    option_levels = 1
    option_full = 2
    default = 0


sa2b_options: typing.Dict[str, type(Option)] = {
    "DeathLink":                        DeathLink,
    "MusicShuffle":                     MusicShuffle,
    "IncludeMissions":                  IncludeMissions,
    "EmblemPercentageForCannonsCore":   EmblemPercentageForCannonsCore,
    "NumberOfLevelGates":               NumberOfLevelGates,
    "LevelGateDistribution":            LevelGateDistribution,
}
