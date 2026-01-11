from dataclasses import dataclass
from Options import Choice, Range, Toggle, OptionGroup, DefaultOnToggle, Removed, PerGameCommonOptions, StartInventoryPool, DeathLink

class Goal(Choice):
    """
    Required Goal to complete the seed
    Noah - Clear the game by defeating the final boss, determined by the final boss option
    Generators - Clear the game by clearing a certain number of planets
    Stone Hunt - Clear the game by collecting all of the Elemental Stones.
    """
    #display_name = "Goal"
    option_noah = 0
    option_generators = 1
    option_stones = 2
    default = 0

class NoahAccess(Choice):
    """
    Requirement to access Warship Noah, the game's final dungeon
    Generators - Open up Noah by clearing a certain number of planets
    Warship Keys - Open Noah by collecting 3 Warship Keys from the item pool
    Coordinates -  Opens Noah by collecting the coordinates to Noah from the item pool
    """
    option_generators = 0
    option_keys = 1
    option_coord = 2
    default = 0

class BossGoal(Choice):
    """Determines which final boss should be fought at Noah to complete the game"""
    option_sthertoth = 0
    option_lilith = 1
    option_angel = 2
    default = 0

class RequiredPlanets(Range):
    """Number of generators which need to be destroyed to access Noah or Clear the game depending on other options"""
    display_name = "Required Generators"
    range_start = 1
    range_end = 7
    default = 5
    
class StartingElement(Choice):
    option_fire = 0
    option_ice = 1
    option_wind = 2
    option_earth = 3
    option_lightning = 4
    option_light = 5
    option_dark = 6
    option_random_element = 7
    default = 7

class StartingPlanets(Range):
    """Number of random planets you can visit from the start, you can always visit Alcatraz, Noah will not be included."""
    display_name = "Starting Planets"
    range_start = 1
    range_end = 7
    default = 2

class IncludeKeys(Toggle):
    """If enabled will add 3 Warship Key items into the item pool which each will autocomplete sections of Warship Noah
    but are not necessary to progress, this option will always be set if keys are set to open Warship Noah"""

class IncludeTraps(DefaultOnToggle):
    """If enabled will add negative traps to the item pool"""

class ReduceFood(Toggle):
    """Reduces how much food is required to get Pommy's evolution checks"""

class Shopsanity(Toggle):
    """Adds shop locations into the location pool"""

class Pommysanity(Toggle):
    """Adds pommy transformation locations into the location pool"""

class PommyShop(Toggle):
    """When Shopsanity is enabled, this will place Pommy Gene transformation items onto certain shop locations"""

class PowerupSanity(Toggle):
    """When enabled will include Power Glove and Bomb Kick items as checks"""

class RandomMusic(Toggle):
    """Randomizes the music table every time the client is loaded"""
class RandomSound(Toggle):
    """Randomizes the Sound Effect table every time the client is loaded"""

class RandomEffect(Toggle):
    """Randomizes the Animated Effects, likely pretty unstable for now"""

bomberman_tsa_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        NoahAccess,
        RequiredPlanets,
        BossGoal,
        IncludeKeys,
    ]),
    OptionGroup("Gameplay Options", [
        StartingElement,
        StartingPlanets,
        ReduceFood,
        PowerupSanity,
        Shopsanity,
        Pommysanity,
        PommyShop,
        IncludeTraps,
        DeathLink,
    ]),
    OptionGroup("Randomization Options", [
        RandomMusic,
        RandomSound,
        RandomEffect,

    ]),
]

@dataclass
class BombTSAOptions(PerGameCommonOptions):
    game_goal: Goal
    noah_open : NoahAccess
    planet_required: RequiredPlanets
    noah_boss: BossGoal
    start_element: StartingElement
    start_planet: StartingPlanets
    death_link: DeathLink
    random_music: RandomMusic
    random_sound: RandomSound
    random_efx: RandomEffect
    reduce_food: ReduceFood
    pommysanity: Pommysanity
    shopsanity: Shopsanity
    powersanity: PowerupSanity
    pommyshop: PommyShop
    include_traps: IncludeTraps
    include_warkeys: IncludeKeys