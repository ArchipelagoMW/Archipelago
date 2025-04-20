from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions, StartInventoryPool

class Goal(Choice):
    """
    Choose what is required to complete the game.
    
    Talking to Nan in <insert correct place name here!> will tell you the selected goal.
    
    Astley: Defeat Astley (add more here).
    
    True Astley: Defeat Astley but more somehow

    Clamshells: Collect enough clamshells for the clam lover
    """
    display_name = "Goal"
    option_astley = 0
    option_true_astley = 1
    option_clamshells = 2
    default = 0
    
class ClamshellsQuantity(Range):
    """If your goal is Clamshells, this is where you select how many you need to win."""
    display_name = "Clamshells needed to win"
    range_start = 1
    range_end = 19
    default = 13

class RandomizeJobs(DefaultOnToggle):
    """
    When enabled, Jobs can be found anywhere, when disabled they are always on crystals.
    """
    display_name = "Randomize Jobs"

class StartWithTreasureFinder(DefaultOnToggle):
    """
    When enabled, the player will start with the treasure finder in their inventory.
    """
    display_name = "Begin with Treasure Finder"

class StartWithMaps(DefaultOnToggle):
    """
    When enabled, the player will start with all of the maps in their inventory.
    """
    display_name = "Begin with Area Maps"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    clamshellsQuantity: ClamshellsQuantity
    randomizeJobs: RandomizeJobs
    startWithTreasureFinder: StartWithTreasureFinder
    startWithMaps: StartWithMaps