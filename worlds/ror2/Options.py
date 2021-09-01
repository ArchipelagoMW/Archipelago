import typing
from Options import Option, Toggle, Range


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

class AllowLunarItems(Toggle):
    """Allows Lunar items in the item pool."""
    displayname = "Enable Lunar Item Shuffling"
    default = True

class StartWithRevive(Toggle):
    """Start the game with a `Dio's Best Friend` item."""
    displayname = "Start with a Revive"
    default = True


ror2_options: typing.Dict[str, type(Option)] = {
    "total_locations":      TotalLocations,
    "total_revivals":       TotalRevivals,
    "start_with_revive":    StartWithRevive,
    "item_pickup_step":     ItemPickupStep,
    "enable_lunar":         AllowLunarItems
}
