from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions

class CutsceneSanity(Toggle):
    """
    Determines whether cutscene maps send location checks
    """
    display_name = "CutsceneSanity"

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

@dataclass
class Portal2Options(PerGameCommonOptions):
    death_link: DeathLink

    cutscenesanity: CutsceneSanity
    # storyachievementsanity: StoryAchievementSanity
    # monitorsanity: MonitorSanity