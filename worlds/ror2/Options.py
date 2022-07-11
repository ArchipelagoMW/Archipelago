import typing
from Options import Option, DefaultOnToggle, Range, Choice


class TotalLocations(Range):
    """Number of location checks which are added to the Risk of Rain playthrough."""
    display_name = "Total Locations"
    range_start = 10
    range_end = 500
    default = 20


class TotalRevivals(Range):
    """Total Percentage of `Dio's Best Friend` item put in the item pool."""
    display_name = "Total Percentage Revivals Available"
    range_start = 0
    range_end = 10
    default = 4


class ItemPickupStep(Range):
    """Number of items to pick up before an AP Check is completed.
    Setting to 1 means every other pickup.
    Setting to 2 means every third pickup. So on..."""
    display_name = "Item Pickup Step"
    range_start = 0
    range_end = 5
    default = 2


class AllowLunarItems(DefaultOnToggle):
    """Allows Lunar items in the item pool."""
    display_name = "Enable Lunar Item Shuffling"


class StartWithRevive(DefaultOnToggle):
    """Start the game with a `Dio's Best Friend` item."""
    display_name = "Start with a Revive"
    
class FinalStageDeath(DefaultOnToggle):
    """Death on the final boss stage counts as a win."""
    display_name = "Final Stage Death is Win"


class GreenScrap(Range):
    """Weight of Green Scraps in the item pool."""
    display_name = "Green Scraps"
    range_start = 0
    range_end = 100
    default = 16


class RedScrap(Range):
    """Weight of Red Scraps in the item pool."""
    display_name = "Red Scraps"
    range_start = 0
    range_end = 100
    default = 4


class YellowScrap(Range):
    """Weight of yellow scraps in the item pool."""
    display_name = "Yellow Scraps"
    range_start = 0
    range_end = 100
    default = 1


class WhiteScrap(Range):
    """Weight of white scraps in the item pool."""
    display_name = "White Scraps"
    range_start = 0
    range_end = 100
    default = 32


class CommonItem(Range):
    """Weight of common items in the item pool."""
    display_name = "Common Items"
    range_start = 0
    range_end = 100
    default = 64


class UncommonItem(Range):
    """Weight of uncommon items in the item pool."""
    display_name = "Uncommon Items"
    range_start = 0
    range_end = 100
    default = 32


class LegendaryItem(Range):
    """Weight of legendary items in the item pool."""
    display_name = "Legendary Items"
    range_start = 0
    range_end = 100
    default = 8


class BossItem(Range):
    """Weight of boss items in the item pool."""
    display_name = "Boss Items"
    range_start = 0
    range_end = 100
    default = 4


class LunarItem(Range):
    """Weight of lunar items in the item pool."""
    display_name = "Lunar Items"
    range_start = 0
    range_end = 100
    default = 16


class Equipment(Range):
    """Weight of equipment items in the item pool."""
    display_name = "Equipment"
    range_start = 0
    range_end = 100
    default = 32


class ItemPoolPresetToggle(DefaultOnToggle):
    """Will use the item weight presets when set to true, otherwise will use the custom set item pool weights."""
    display_name = "Item Weight Presets"

class ItemWeights(Choice):
    """Preset choices for determining the weights of the item pool.<br>
    New is a test for a potential adjustment to the default weights.<br>
    Uncommon puts a large number of uncommon items in the pool.<br>
    Legendary puts a large number of legendary items in the pool.<br>
    Lunartic makes everything a lunar item.<br>
    Chaos generates the pool completely at random with rarer items having a slight cap to prevent this option being too easy.<br>
    No Scraps removes all scrap items from the item pool.<br>
    Even generates the item pool with every item having an even weight.<br>
    Scraps Only will be only scrap items in the item pool."""
    display_name = "Item Weights"
    option_default = 0
    option_new = 1
    option_uncommon = 2
    option_legendary = 3
    option_lunartic = 4
    option_chaos = 5
    option_no_scraps = 6
    option_even = 7
    option_scraps_only = 8

#define a dictionary for the weights of the generated item pool.
ror2_weights: typing.Dict[str, type(Option)] = {
    "green_scrap":          GreenScrap,
    "red_scrap":            RedScrap,
    "yellow_scrap":         YellowScrap,
    "white_scrap":          WhiteScrap,
    "common_item":          CommonItem,
    "uncommon_item":        UncommonItem,
    "legendary_item":       LegendaryItem,
    "boss_item":            BossItem,
    "lunar_item":           LunarItem,
    "equipment":            Equipment
}

ror2_options: typing.Dict[str, type(Option)] = {
    "total_locations":      TotalLocations,
    "total_revivals":       TotalRevivals,
    "start_with_revive":    StartWithRevive,
    "final_stage_death":    FinalStageDeath,
    "item_pickup_step":     ItemPickupStep,
    "enable_lunar":         AllowLunarItems,
    "item_weights":         ItemWeights,
    "item_pool_presets":    ItemPoolPresetToggle,
    **ror2_weights
}
