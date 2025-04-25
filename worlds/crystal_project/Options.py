from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions, StartInventoryPool

class Goal(Choice):
    """
    Choose what is required to complete the game.
    
    Checking the first sign in the Spawning Meadows will tell you the selected goal.
    
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
    range_end = 100
    default = 13
    
class ClamshellsInPool(Range):
    """This determines how many clamshells end up in the pool.  You probably only care if your goal is set to clamshells."""
    display_name = "Clamshells in the pool"
    range_start = 1
    range_end = 100
    default = 19

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

class IncludedRegions(Choice):
    """
    Choose which regions will have locations worth checking in them.
    
    Any treasures, npcs, and crystals outside of this region will not give you checks when you interact with them.

    This can be used to make your game shorter/easier or longer/harder.
    
    Beginner: Only regions up through the end of Skumparadise will have checks.
    
    Advanced: Regions up to Salmon Bay will have checks

    Expert: Regions up to the deep sea will have checks (note the depths will not be included)

    All: Every region is included
    """
    display_name = "Regions to include in game"
    option_beginner = 0
    option_advanced = 1
    option_expert = 2
    option_all = 3
    default = 3

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    clamshellsQuantity: ClamshellsQuantity
    clamshellsInPool: ClamshellsInPool
    randomizeJobs: RandomizeJobs
    startWithTreasureFinder: StartWithTreasureFinder
    startWithMaps: StartWithMaps
    includedRegions: IncludedRegions