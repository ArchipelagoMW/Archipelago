from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility
from worlds.tloz_ph.data.Items import ITEMS_DATA


class PhantomHourglassGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Triforce_door: Open the triforce door on TotOK B6
    """
    display_name = "Goal"
    option_triforce_door = 0
    default = 0


class PhantomHourglassStartingTime(Range):
    """
    How much time to start with in your Phantom Hourglass, in minutes
    """
    display_name = "Phantom Hourglass Starting Time"
    range_start = 0
    range_end = 30
    default = 10


class PhantomHourglassTimeIncrement(Range):
    """
    How much time to get for each sand of hours upgrade, in minutes
    """
    display_name = "Increment for each Sand of Hours"
    range_start = 0
    range_end = 30
    default = 1


class PhantomHourglassRemoveItemsFromPool(ItemDict):
    """
    Removes specified amount of given items from the item pool, replacing them with random filler items.
    This option has significant chances to break generation if used carelessly, so test your preset several times
    before using it on long generations. Use at your own risk!
    """
    display_name = "Remove Items from Pool"
    verify_item_name = False


class PhantomHourglassLogic(Choice):
    """
    Logic options:
    - Normal: Glitches not in logic.
    - Glitched: Hammer clips, chu camera displacement and clever use of items in logic
    Be careful, using glitches on normal logic can cause key-related softlocks
    """
    display_name = "Logic Settings"
    option_normal = 0
    option_glitched = 1
    default = 0


class PhantomHourglassPhantomCombatDifficulty(Choice):
    """
    Option for what you need to kill phantoms in logic
    - require_phantom_sword: need phantom sword
    - require_traps: need a pit trap or boulder
    - require_stun: require a method of stunning, and an open pit to push into. Includes bow, hammer,
    and sword + 2 progressive spirits of power
    - require_weapon: all of the above plus grappling hook
    """
    display_name = "Phantom Kill Requirements"
    option_require_phantom_sword = 0
    option_require_traps = 1
    option_require_stun = 2
    option_require_weapon = 3
    default = 0


class PhantomHourglassKeyRandomization(Choice):
    """
    Small Key Logic options:
    - vanilla: Keys are not randomized
    - in_own_dungeon: Keys can be found in their own dungeon
    - anywhere: Keysanity. Keys can be found anywhere
    """
    display_name = "Key Settings"
    option_vanilla = 0
    option_in_own_dungeon = 1
    option_anywhere = 2
    default = 1

@dataclass
class PhantomHourglassOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    goal: PhantomHourglassGoal
    start_inventory_from_pool: StartInventoryPool
    logic: PhantomHourglassLogic

    # Dungeon Options
    keysanity: PhantomHourglassKeyRandomization
    phantom_combat_difficulty: PhantomHourglassPhantomCombatDifficulty
    ph_starting_time: PhantomHourglassStartingTime
    ph_time_increment: PhantomHourglassTimeIncrement

    remove_items_from_pool: PhantomHourglassRemoveItemsFromPool
    death_link: DeathLink
