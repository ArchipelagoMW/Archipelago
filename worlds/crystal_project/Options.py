from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions, StartInventoryPool

#"""Goal Options"""
class Goal(Choice):
    """
    Choose what is required to complete the game.
    
    Checking the first sign in the Spawning Meadows will tell you the selected goal.
    
    Astley: Defeat Astley in the New World. A New World Stone will be given to the player after obtaining a certain number of jobs.
    
    True Astley: Defeat Astley but more somehow.

    Clamshells: Collect enough clamshells for the clam lover.
    """
    display_name = "Goal"
    option_astley = 0
    option_true_astley = 1
    option_clamshells = 2
    default = 0

class NewWorldStoneJobQuantity(Range):
    """
    If your goal is Astley, select how many Jobs you need to find before being sent the New World Stone for the final fight.

    (NOTE: Starting Jobs do not count towards this number).
    """
    display_name = "Job count that locks the new world stone"
    range_start = 1
    range_end = 18
    default = 18

class ClamshellsQuantity(Range):
    """
    If your goal is Clamshells, select how many you need to win.
    """
    display_name = "Clamshells needed to win"
    range_start = 1
    range_end = 100
    default = 13
    
class ClamshellsInPool(Range):
    """
    Select how many total Clamshells are in the item pool.  You probably only care if your goal is set to Clamshells.
    """
    display_name = "Clamshells in the pool"
    range_start = 1
    range_end = 100
    default = 19

#"""Location Options"""
class RandomizeJobs(DefaultOnToggle):
    """
    When enabled, Jobs can be found anywhere; when disabled, they are always on crystals.
    """
    display_name = "Randomize Jobs"

class RandomizeStartingJobs(DefaultOnToggle):
    """
    When enabled, you will start with 6 random jobs.
    """
    display_name = "Randomize starting Jobs"

class KillBossesMode(Toggle):
    """
    When enabled, defeating a boss will provide checks.
    """
    display_name = "Kill Bosses Mode"

class Shopsanity(Toggle):
    """
    When enabled, all shop inventories will be replaced with checks. Be prepared, adventurer.
    """
    display_name = "Shopsanity"

class IncludedRegions(Choice):
    """
    Choose which regions will have locations worth checking in them.

    Any Treasures, NPCs, or Crystals outside of this region will not give you checks when you interact with them.

    This can be used to make your game shorter/easier or longer/harder.

    Beginner: Only regions up through the end of Skumparadise will have checks.

    Advanced: Regions up to Salmon Bay will have checks.

    Expert: Regions up to The Deep Sea will have checks. (Note: The Depths will not be included).

    All: Every region is included.
    """
    display_name = "Regions to include in game"
    option_beginner = 0
    option_advanced = 1
    option_expert = 2
    option_all = 3
    default = 3

#"""Progression Options"""
class LevelGating(Toggle):
    """
    When enabled, the parties maximum level will be capped, with items in the pool increasing that cap.
    Areas in the game will be considered out of logic (but still accessible) if the party level cap is below the area level.
    """
    display_name = "Level Gating"

class LevelUpsInPool(Range):
    """
    If level gating is enabled, this will control how many max level ups are in the pool.
    Each max level up increases the max character level by 10, so a value of 5 here is a maximum possible level of 60
    Changing this value to a higher number will allow the player to exceed the default level cap.
    """
    display_name = "Max level ups in the pool"
    range_start = 5
    range_end = 8
    default = 5

class EasyLeveling(Toggle):
    """
    When enabled, characters will not receive reduced exp for being dead or for being a higher level than the fought enemy.
    """
    display_name = "Easy Leveling"

class ProgressiveEquipmentMode(DefaultOnToggle):
    """
    When enabled, each category of weapon and armor will be sent to the player in progressive order from weakest to strongest.

    When disabled, weapons and armor are fully randomized.
    """
    display_name = "Progressive Equipment"

class KeyMode(Choice):
    """
    Choose how keys behave.

    Skeleton Key: Only the Skeleton Key, which can open any locked door, will be in your item pool.

    Key Ring: One check will give all keys needed to complete one dungeon. The Skeleton Key will still be in the pool. NOT IMPLEMENTED

    Vanilla: All vanilla keys will be in the item pool.
    """
    display_name = "Key Mode"
    option_skeleton = 0
    option_key_ring = 1
    option_vanilla = 2
    default = 2

#"""Item Pool Options"""
class StartWithTreasureFinder(DefaultOnToggle):
    """
    When enabled, the player will start with the Treasure Finder in their inventory. When disabled, it will be in the item pool.

    Note: Having the Treasure Finder is required for the in-game minimap to display nearby checks.
    """
    display_name = "Begin with Treasure Finder"

class StartWithMaps(DefaultOnToggle):
    """
    When enabled, the player will start with all maps in their inventory.

    Note: The in-game minimap hides when in an area without its map. The world map will display check location icons but will not draw an area without its map.
    """
    display_name = "Begin with Area Maps"

class IncludeSummonAbilities(DefaultOnToggle):
    """
    When enabled, Summon abilities can be found anywhere; when disabled, they will be in the regular spot.
    """
    display_name = "Include Summoner Abilities in the item pool"
    
class IncludeScholarAbilities(DefaultOnToggle):
    """
    When enabled, Scholar abilities can be found anywhere. They can still be learned as normal from enemies.
    """
    display_name = "Include Scholar Abilities in the item pool"

#"""Bonus Fun"""
class RandomizeMusic(Toggle):
    """
    When enabled, music will be randomized upon connecting to the AP World.
    """
    display_name = "Randomize Music"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    newWorldStoneJobQuantity: NewWorldStoneJobQuantity
    clamshellsQuantity: ClamshellsQuantity
    clamshellsInPool: ClamshellsInPool
    randomizeJobs: RandomizeJobs
    randomizeStartingJobs: RandomizeStartingJobs
    killBossesMode: KillBossesMode
    shopsanity: Shopsanity
    includedRegions: IncludedRegions
    levelGating: LevelGating
    levelUpsInPool: LevelUpsInPool
    easyLeveling: EasyLeveling
    progressiveEquipmentMode: ProgressiveEquipmentMode
    keyMode: KeyMode
    startWithTreasureFinder: StartWithTreasureFinder
    startWithMaps: StartWithMaps
    includeSummonAbilities: IncludeSummonAbilities
    includeScholarAbilities: IncludeScholarAbilities
    randomizeMusic: RandomizeMusic