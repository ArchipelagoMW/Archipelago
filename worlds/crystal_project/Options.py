from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions, StartInventoryPool

class Goal(Choice):
    """
    Choose what is required to complete the game.
    
    Checking the first sign in the Spawning Meadows will tell you the selected goal.
    
    Astley: Defeat Astley in the new world. A new world stone will be given to the player after obtaining a certain number of jobs.
    
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

class RandomizeStartingJobs(DefaultOnToggle):
    """
    When enabled, you will start with 6 random jobs.
    """
    display_name = "Randomize starting Jobs"

class NewWorldStoneJobQuantity(Range):
    """If your goal is Astley, this is where you select how many jobs you need to find before being sent the new world stone (NOTE: the starting jobs do not count towards this number)."""
    display_name = "Job count that locks the new world stone"
    range_start = 1
    range_end = 18
    default = 18

class EasyLeveling(DefaultOnToggle):
    """
    When enabled, characters will not recieve reduced exp for being dead nor for being a higher level than the fought enemy.
    """
    display_name = "Easy Leveling"

class RandomizeMusic(DefaultOnToggle):
    """
    When enabled, music will be randomized upon connecting to the AP World.
    """
    display_name = "Randomize Music"

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

class ProgressiveEquipmentMode(DefaultOnToggle):
    """
    When enabled, each category of weapon and armor will be sent to the player in progressive order from weakest to strongest.

    When disabled, weapons and armor are fully randomized.
    """
    display_name = "Progressive Equipment"

class KeyMode(Choice):
    """
    Choose how keys behave.
    
    Skeleton Key: Only the skeleton key which can open any locked door will be in your item pool.
    
    Key Ring: One check will give all the keys needed to complete one dungeon, the skeleton key will still be in the pool NOT IMPLEMENTED

    Vanilla: All vanilla keys will be included in checks
    """
    display_name = "Key Mode"
    option_skeleton = 0
    option_key_ring = 1
    option_vanilla = 2
    default = 2

class KillBossesMode(DefaultOnToggle):
    """
    When enabled, defeating a boss will provide checks.
    """
    display_name = "Kill Bosses Mode"

class IncludeSummonAbilities(DefaultOnToggle):
    """
    When enabled, Summon abilities can be found anywhere, when disabled they will be in the regular spot.
    """
    display_name = "Include Summoner Abilities in the item pool"
    
class IncludeScholarAbilities(DefaultOnToggle):
    """
    When enabled, Scholar abilities can be found anywhere, they can still be learned as normal from enemies.
    """
    display_name = "Include Scholar Abilities in the item pool"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    clamshellsQuantity: ClamshellsQuantity
    clamshellsInPool: ClamshellsInPool
    randomizeJobs: RandomizeJobs
    randomizeStartingJobs: RandomizeStartingJobs
    newWorldStoneJobQuantity: NewWorldStoneJobQuantity
    easyLeveling: EasyLeveling
    randomizeMusic: RandomizeMusic
    startWithTreasureFinder: StartWithTreasureFinder
    startWithMaps: StartWithMaps
    includedRegions: IncludedRegions
    progressiveEquipmentMode: ProgressiveEquipmentMode
    keyMode: KeyMode
    killBossesMode: KillBossesMode
    includeSummonAbilities: IncludeSummonAbilities
    includeScholarAbilities: IncludeScholarAbilities