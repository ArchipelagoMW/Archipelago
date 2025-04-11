from dataclasses import dataclass
from typing import List, Dict, Any
from Options import Toggle, Range, Choice, OptionSet, PerGameCommonOptions, OptionGroup, StartInventory, ProgressionBalancing
from .data import GetAllMapTags, GetExcludedMapTags

#https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

# Number of tracks, medal requirement percentage, target time, percent of map skips

class TargetTime(Range):
    """Determines what time you must drive on a map for it to be considered completed. You can enter any number from 0 - 300.
    
    0   = Bronze Medal
    100 = Silver Medal
    200 = Gold Medal
    300 = Author Medal

    If you choose a value inbetween two medals, your target time will be a mix of two medals. For example, a value of 250 will make your target time halfway between the gold and author medals. A value of 120 will make your target time 20% of the way from the silver medal to the gold medal.

    The the quickest medal equal to or below your target time is made your progression medal.
    """
    display_name = "Target Time Difficulty"
    range_start = 0
    range_end = 300
    default = 240

class MapNumber(Range):
    """Sets the number of maps that you can play."""
    display_name = "Number of Maps"
    range_start = 1
    range_end = 100
    default = 25

class MedalPercentage(Range):
    """The number of progression medals required to win, calculated as a percentage of the total number of maps.
    
    Your progression medal is the quickest medal equal to or below your target time.
    """
    display_name = "Medal Requirement Percentage"
    range_start = 10
    range_end = 100
    default = 60

class SkipPercentage(Range):
    """The number of map skips in the item pool, calculated as a percetage of the total number of maps.
    
    If a map is broken or impossible or you get stuck, use the /skip command in the client to skip the map without using an item.
    """
    display_name = "Map Skip Item Percentage"
    range_start = 0
    range_end = 100
    default = 20

class MapTags(OptionSet):
    """Tags that maps from Trackmania Exchange are allowed to have. If none of these tags are checked, it will default to allowing all tags."""
    display_name = "Allowed TMX Tags"
    valid_keys = GetAllMapTags()

class MapTagsInclusive(Toggle):
    """Enable if maps must have every single tag chosen in Allowed TMX Tags"""
    display_name = "Are TMX Tags Inclusive"

class MapETags(OptionSet):
    """Tags that maps from Trackmania Exchance are *not* allowed to have."""
    display_name = "Excluded TMX Tags"
    valid_keys = GetAllMapTags()
    default = GetExcludedMapTags()


@dataclass
class TrackmaniaOptions(PerGameCommonOptions):
    # start_inventory_from_pool: StartInventory
    # progression_balancing : ProgressionBalancing

    target_time: TargetTime
    map_number: MapNumber
    medal_percentage: MedalPercentage
    skip_percentage: SkipPercentage
    map_tags: MapTags
    map_tags_inclusive: MapTagsInclusive
    map_etags: MapETags


# def create_option_groups() -> List[OptionGroup]:
#     option_group_list: List[OptionGroup] = []
#     for name, options in tm_option_groups.items():
#         option_group_list.append(OptionGroup(name=name, options=options))

#     return option_group_list

# tm_option_groups: Dict[str, List[Any]] = {
#     "General Options": [EndGoal, ShuffleStorybookPages, ShuffleAlpineZiplines, ShuffleSubconPaintings,
#                         ShuffleActContracts, MinPonCost, MaxPonCost, BadgeSellerMinItems, BadgeSellerMaxItems,
#                         LogicDifficulty, NoPaintingSkips, CTRLogic],

#     "Act Options": [ActRandomizer, StartingChapter, LowestChapterCost, HighestChapterCost,
#                     ChapterCostIncrement, ChapterCostMinDifference, FinalChapterMinCost, FinalChapterMaxCost,
#                     FinaleShuffle, ActPlando, ActBlacklist],

#     "Item Options": [StartWithCompassBadge, CompassBadgeMode, RandomizeHatOrder, YarnAvailable, YarnCostMin,
#                      YarnCostMax, MinExtraYarn, HatItems, UmbrellaLogic, MaxExtraTimePieces, YarnBalancePercent,
#                      TimePieceBalancePercent],

#     "Arctic Cruise Options": [EnableDLC1, Tasksanity, TasksanityTaskStep, TasksanityCheckCount,
#                               ShipShapeCustomTaskGoal, ExcludeTour],

#     "Nyakuza Metro Options": [EnableDLC2, MetroMinPonCost, MetroMaxPonCost, NyakuzaThugMinShopItems,
#                               NyakuzaThugMaxShopItems, BaseballBat, NoTicketSkips],

#     "Death Wish Options": [EnableDeathWish, DWTimePieceRequirement, DWShuffle, DWShuffleCountMin, DWShuffleCountMax,
#                            DWEnableBonus, DWAutoCompleteBonuses, DWExcludeAnnoyingContracts, DWExcludeAnnoyingBonuses,
#                            DWExcludeCandles, DeathWishOnly],

#     "Trap Options": [TrapChance, BabyTrapWeight, LaserTrapWeight, ParadeTrapWeight]
# }