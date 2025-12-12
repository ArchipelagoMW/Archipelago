from dataclasses import dataclass
from Options import Choice, OptionGroup, Range, Toggle, DeathLink, PerGameCommonOptions

portal2_option_presets = {
    
}

class CutsceneSanity(Toggle):
    """
    Determines whether cutscene maps send location checks
    """
    display_name = "CutsceneSanity"

class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0

class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2



# class StoryAchievementSanity(Toggle):
#     """
#     Determines whether completing story achievements send location checks
#     """
#     display_name = "StoryAchievementSanity"

# class MonitorSanity(Toggle):
#     """
#     Determines whether breaking Wheatly monitors send location checks
#     """
#     display_name = "MonitorSanity"

portal2_option_groups = [
    OptionGroup("Location Options", [
        CutsceneSanity
    ]),
    OptionGroup("Trap Options", [
        TrapFillPercentage
    ])
]

@dataclass
class Portal2Options(PerGameCommonOptions):
    death_link: DeathLink

    cutscenesanity: CutsceneSanity
    # storyachievementsanity: StoryAchievementSanity
    # monitorsanity: MonitorSanity