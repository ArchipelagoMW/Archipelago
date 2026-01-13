from dataclasses import dataclass
from Options import Choice, OptionGroup, Range, Toggle, DeathLink, PerGameCommonOptions
from .ItemNames import *

class OpenWorld(Toggle):
    """
    If all maps are accessible from the start.
    Default is false, only 1 map from each chapter is accessible and maps are unlocked through completing previous ones.
    If true all maps are accessible from the start. This makes it easier to play but does break intended level progression logic
    """
    display_name = "Open World"

class CutsceneLevels(Toggle):
    """
    Determines whether cutscene maps are added to the map pool
    """
    display_name = "Cutscene Levels"

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

class MotionBlurTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes it a little hard to see
    """
    display_name = motion_blur_trap + " Weight"

class FizzlePortalTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which fizzles ALL portals on the map
    """
    display_name = fizzle_portal_trap + " Weight"

class ButterFingersTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes it a little hard to hold items
    """
    display_name = butter_fingers_trap + " Weight"

class CubeConfettiTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes an explosion of colorful cubes at your feet
    """
    display_name = cube_confetti_trap + " Weight"

class SlipperyFloorTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes Chell slip and slide
    """
    display_name = slippery_floor_trap + " Weight"

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
        OpenWorld,
        CutsceneLevels
    ]),
    OptionGroup("Trap Options", [
        TrapFillPercentage,
        MotionBlurTrapWeight,
        FizzlePortalTrapWeight,
        ButterFingersTrapWeight,
        CubeConfettiTrapWeight,
        SlipperyFloorTrapWeight
    ])
]

portal2_option_presets = {
    "default": {
        "death_link": False,
        "map_layout": "normal",
        "cutscenelevels": True,
    }
}

@dataclass
class Portal2Options(PerGameCommonOptions):
    death_link: DeathLink

    open_world: OpenWorld
    cutscenelevels: CutsceneLevels
    # storyachievementsanity: StoryAchievementSanity
    # monitorsanity: MonitorSanity

    trap_fill_percentage: TrapFillPercentage
    motion_blur_trap_weight: MotionBlurTrapWeight
    fizzle_portal_trap_weight: FizzlePortalTrapWeight
    butter_fingers_trap_weight: ButterFingersTrapWeight
    cube_confetti_trap_weight: CubeConfettiTrapWeight
    slippery_floor_trap_weight: SlipperyFloorTrapWeight
    