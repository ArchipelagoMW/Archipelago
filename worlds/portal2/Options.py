from dataclasses import dataclass
from Options import Choice, LocationSet, OptionGroup, Range, Toggle, DeathLink, PerGameCommonOptions
from .ItemNames import *

class GameMode(Choice):
    """
    What map generation and logic options are set:
    normal -> Each chapter is randomised with it's own maps
    chaotic -> Any map can be in any chapter
    open_world -> maps appear in the correct order in the game and are all playable from the start
    """
    display_name = "Game Mode"
    option_normal = 0
    option_chaotic = 1
    option_open_world = 2
    default = 0
    
class EarlyPlayabilityPercentage(Range):
    """
    What percentage of starting maps are in the first round of map selection
    Minimum of 60 -> Over half of the starting maps are available from the get go, slightly slower start
    Maximum of 100 -> All starting maps are available from the get go, a very quick start
    """
    display_name = "Early Playability Percentage"
    range_start = 60
    range_end = 100
    default = 75  
    
class RemoveLocations(LocationSet):
    """
    Which maps will be removed entirly from the map pool.
    Different from Excluded Locations as Removed Locations will not be playable
    during the game. Excluded Locations are still in the map pool.
    """
    display_name = "Removed Locations"

class CutsceneLevels(Toggle):
    """
    Determines whether cutscene maps are added to the map pool
    """
    display_name = "Cutscene Levels"
    

class LogicDifficulty(Choice):
    """
    If logic should be for the average player or for an experienced glitch speedrunner
    normal -> assumes you have everything required to beat the level
    speedrunner -> assumes you know difficult speedrun techniques for the whole game including some sla tricks, experimental
    (if you don't speedrun the game don't choose this option)
    """
    display_name = "Logic Difficulty"
    option_normal = 0
    option_speedrunner = 1
    default = 0

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

class WheatleyMonitors(Toggle):
    """
    Determines whether breaking Wheatly monitors will send location checks
    """
    display_name = "Wheatley Monitors"
    
class RatmanDens(Toggle):
    """
    Determines whether locating Ratman Dens will send location checks
    """
    display_name = "Ratman Dens"

portal2_option_groups = [
    OptionGroup("Location Options", [
        GameMode,
        EarlyPlayabilityPercentage,
        LogicDifficulty,
        RemoveLocations,
        CutsceneLevels,
        WheatleyMonitors,
        RatmanDens,
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

    game_mode: GameMode
    cutscene_levels: CutsceneLevels
    remove_locations: RemoveLocations
    early_playability_percentage: EarlyPlayabilityPercentage
    logic_difficulty: LogicDifficulty
    # storyachievementsanity: StoryAchievementSanity
    wheatley_monitors: WheatleyMonitors
    ratman_dens: RatmanDens

    trap_fill_percentage: TrapFillPercentage
    motion_blur_trap_weight: MotionBlurTrapWeight
    fizzle_portal_trap_weight: FizzlePortalTrapWeight
    butter_fingers_trap_weight: ButterFingersTrapWeight
    cube_confetti_trap_weight: CubeConfettiTrapWeight
    slippery_floor_trap_weight: SlipperyFloorTrapWeight
    