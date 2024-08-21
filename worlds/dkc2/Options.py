from dataclasses import dataclass
import typing

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionDict, DeathLink, PerGameCommonOptions, StartInventoryPool

class StartingLifeCount(Range):
    """
    How many lives to start the game with. 
    Note: This number becomes the new default life count, meaning that it will persist after a game over.
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 99
    default = 5

class StartingKong(Choice):
    """
    kual kong kieres
    """
    display_name = "Starting Kong"
    option_diddy = 0
    option_dixie = 1
    option_both = 2
    default = 0

class Logic(Choice):
    """
    kual dificultad kieres
    """
    display_name = "Logic Setting"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    default = 1

class KONGSanity(Toggle):
    """
    añade kong como checks
    """
    display_name = "KONG-Sanity"


class ShuffleLevels(Toggle):
    """
    mueve niveles
    """
    display_name = "Shuffle Levels"


@dataclass
class DKC2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    starting_life_count: StartingLifeCount
    starting_kong: StartingKong
    logic: Logic
    kongsanity: KONGSanity
    shuffle_levels: ShuffleLevels
