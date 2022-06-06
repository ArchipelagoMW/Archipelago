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
    range_end = 75
    default = 50


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required emblems in the item pool with random junk items
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 50


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


class RequiredRank(Choice):
    """
    Determines what minimum Rank is required to send a check for a mission
    """
    display_name = "Required Rank"
    option_e = 0
    option_d = 1
    option_c = 2
    option_b = 3
    option_a = 4
    default = 0


class ChaoGardenDifficulty(Choice):
    """
    Determines up to what difficulty of Chao Garden activities serve as checks
    """
    display_name = "Chao Garden Difficulty"
    option_none = 0
    option_beginner = 1
    option_intermediate = 2
    option_expert = 3


class IncludeChaoKarate(Toggle):
    """
    Determines whether the Chao Karate in included as checks (requires purchase of the "Battle" DLC)
    """
    display_name = "Include Chao Karate"


class ChaoRaceChecks(Choice):
    """
    Determines whether all Chao Races grant checks, or only the Chao Races which grant Chao Toy prizes
    """
    display_name = "Chao Race Checks"
    option_all = 0
    option_prize = 1


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
    "death_link": DeathLink,
    "music_shuffle": MusicShuffle,
    "required_rank": RequiredRank,
    "include_missions": IncludeMissions,
    "emblem_percentage_for_cannons_core": EmblemPercentageForCannonsCore,
    "junk_fill_percentage": JunkFillPercentage,
    "number_of_level_gates": NumberOfLevelGates,
    "level_gate_distribution": LevelGateDistribution,
    "chao_garden_difficulty": ChaoGardenDifficulty,
    "include_chao_karate": IncludeChaoKarate,
    "chao_race_checks": ChaoRaceChecks,
}
