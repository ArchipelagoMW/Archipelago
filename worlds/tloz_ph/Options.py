from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility
from worlds.tloz_ph.data.Items import ITEMS_DATA


class PhantomHourglassGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Beat Bellum: Kill bellum at the bottom of TotOK
    """
    display_name = "Goal"

    option_beat_bellum = 0

    default = 0

class PhantomHourglassStartingTime(Range):
    """
    How much time to start with in your Phantom Hourglass, in minutes
    """
    display_name = "Phantom Hourglass Starting Time"
    range_start = 0.01
    range_end = 30
    default = 10

class PhantomHourglassRemoveItemsFromPool(ItemDict):
    """
    Removes specified amount of given items from the item pool, replacing them with random filler items.
    This option has significant chances to break generation if used carelessly, so test your preset several times
    before using it on long generations. Use at your own risk!
    """
    display_name = "Remove Items from Pool"
    verify_item_name = False

@dataclass
class PhantomHourglassOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    start_inventory_from_pool: StartInventoryPool
    goal: PhantomHourglassGoal
    ph_starting_time: PhantomHourglassStartingTime
    remove_items_from_pool: PhantomHourglassRemoveItemsFromPool
    death_link: DeathLink

