import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions


class FishsanityOption(DefaultOnToggle):
    """Include catching all fish"""
    display_name = "Randomize Fish Locations"
    
class SphedasanityOption(DefaultOnToggle):
    """Include completing all spheda"""
    display_name = "Randomize Spheda Locations"
    
class MedalsanityOption(DefaultOnToggle):
    """Include completing all Medals"""
    display_name = "Randomize Medal Locations"
    
class GeoramasanityOption(DefaultOnToggle):
    """Include 100% completing all Georama"""
    display_name = "Randomize Georama Locations"
    
class PhotosanityOption(DefaultOnToggle):
    """Include taking all photos"""
    display_name = "Randomize Photo ideas Locations"
    
class InventionsanityOption(DefaultOnToggle):
    """Include discovering all inventions"""
    display_name = "Randomize invention Locations"
    

class IncludeResourcePacksOption(Range):
    """Adds packs of useful items"""
    display_name = "Number of resource packs to include in the pool"
    range_start = 0
    range_end = 100
    default = 20

class ChapterGoalCountOption(Range):
    """Amount of chapters to complete for the goal"""
    display_name = "Number of chapters that must be completed"
    range_start = 1
    range_end = 8
    default = 4

class ABSMultiplierOption(Range):
    """Multiply ABS by this amount"""
    display_name = "Multiplier for received ABS (weapon exp)"
    range_start = 1
    range_end = 10
    default = 1
    
class GildaMultiplierOption(Range):
    """Multiply Gilda dropped by enemies by this amount"""
    display_name = "Multiplier for enemy-dropped gilda"
    range_start = 1
    range_end = 10
    default = 1

class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class EnableEnemyRandomiserOption(DefaultOnToggle):
    """Randomise all enemies"""
    display_name = "Enable Enemy Randomiser"

@dataclass
class DC2Option(PerGameCommonOptions):
    #fishsanity: FishsanityOption
    #sphedasanity: SphedasanityOption
    #medalsanity: MedalsanityOption
    #georamasanity: GeoramasanityOption
    #photosanity: PhotosanityOption
    #inventionsanity: InventionsanityOption
    resource_pack_count: IncludeResourcePacksOption
    abs_multiplier: ABSMultiplierOption
    gilda_multiplier: GildaMultiplierOption
    guaranteed_items: GuaranteedItemsOption
    enable_enemy_randomiser: EnableEnemyRandomiserOption

