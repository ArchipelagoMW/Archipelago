import typing
from Options import Option, DefaultOnToggle, Range, OptionList


class TotalLocations(Range):
    """Number of location checks which are added to the Risk of Rain playthrough."""
    displayname = "Total Locations"
    range_start = 10
    range_end = 50
    default = 15


class TotalRevivals(Range):
    """Number of `Dio's Best Friend` item put in the item pool."""
    displayname = "Total Revivals Available"
    range_start = 0
    range_end = 10
    default = 4


class ItemPickupStep(Range):
    """Number of items to pick up before an AP Check is completed.
    Setting to 1 means every other pickup.
    Setting to 2 means every third pickup. So on..."""
    displayname = "Item Pickup Step"
    range_start = 0
    range_end = 5
    default = 1


class AllowLunarItems(DefaultOnToggle):
    """Allows Lunar items in the item pool."""
    displayname = "Enable Lunar Item Shuffling"


class StartWithRevive(DefaultOnToggle):
    """Start the game with a `Dio's Best Friend` item."""
    displayname = "Start with a Revive"


class GreenScrap(Range):
    """Weight of Green Scraps in the item pool."""
    displayname = "Green Scraps"
    range_start = 0
    range_end = 100
    default = 15


class RedScrap(Range):
    """Weight of Red Scraps in the item pool."""
    displayname = "Red Scraps"
    range_start = 0
    range_end = 100
    default = 5


class YellowScrap(Range):
    """Weight of yellow scraps in the item pool."""
    displayname = "Yellow Scraps"
    range_start = 0
    range_end = 100
    default = 1


class WhiteScrap(Range):
    """Weight of white scraps in the item pool."""
    displayname = "White Scraps"
    range_start = 0
    range_end = 100
    default = 30


class CommonItem(Range):
    """Weight of common items in the item pool."""
    displayname = "Common Items"
    range_start = 0
    range_end = 100
    default = 75


class UncommonItem(Range):
    """Weight of uncommon items in the item pool."""
    displayname = "Uncommon Items"
    range_start = 0
    range_end = 100
    default = 40


class LegendaryItem(Range):
    """Weight of legendary items in the item pool."""
    displayname = "Legendary Items"
    range_start = 0
    range_end = 100
    default = 10


class BossItem(Range):
    """Weight of boss items in the item pool."""
    displayname = "Boss Items"
    range_start = 0
    range_end = 100
    default = 5


class LunarItem(Range):
    """Weight of lunar items in the item pool."""
    displayname = "Lunar Items"
    range_start = 0
    range_end = 100
    default = 15


class Equipment(Range):
    """Weight of equipment items in the item pool."""
    displayname = "Equipment"
    range_start = 0
    range_end = 100
    default = 25


class WeightPresets(Choice):
    """Preset item weight options."""
    displayname = "Item Weight Preset"
    option_default = 0


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
    "item_pickup_step":     ItemPickupStep,
    "enable_lunar":         AllowLunarItems,
    **ror2_weights
}