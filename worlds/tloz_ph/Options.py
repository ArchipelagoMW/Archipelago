from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility
from worlds.tloz_ph.data.Items import ITEMS_DATA


class PhantomHourglassGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Triforce_door: Open the triforce door on TotOK B6
    - beat_bellumbeck: beat bellumbeck on the ruins of the ghost ship
    """
    display_name = "Goal"
    option_triforce_door = 0
    option_beat_bellumbeck = 1
    default = 1


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
    display_name = "remove_items_from_pool"
    verify_item_name = False


class PhantomHourglassLogic(Choice):
    """
    Logic options:
    - Normal: Glitches not in logic.
    - Medium: Includes some cool uses of pots aren't hard, bun unconventional
    - Glitched: Hammer clips, chu camera displacement and clever use of items in logic
    Be careful, using glitches on normal logic can cause key-related softlocks
    """
    display_name = "logic"
    option_normal = 0
    option_medium = 1
    option_glitched = 2
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
    display_name = "phantom_combat_difficulty"
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


class PhantomHourglassTriforceCrestRandomization(Toggle):
    """
    When enabled, The Triforce Crest on the big red door in TotOK B6 will turn into an item and be randomized.
    When disabled, the door will always be open
    """
    display_name = "randomize_triforce_crest"
    default = 0


class PhantomHourglassDungeonsRequired(Range):
    """
    How many dungeons are required to access the endgame.
    Currently, there are 2 dungeons implemented
    """
    display_name = "dungeons_required"
    range_start = 0
    range_end = 2
    default = 2


class PhantomHourglassBellumAccess(Choice):
    """
    What unlocks after you reach your dungeon requirement
    - spawn_phantoms_on_b13: getting your goal requirement spawns the phantoms on TotOK B13, and killing them gives
    you bellum access. You will have to run TotOK to the bottom after getting your goal requirement
    - unlock_staircase: getting your goal requirement unlocks the staircase to bellum. The phantoms on B13 spawn by
    default, and killing them unlocks the warp for later
    - warp_to_bellum: getting your goal requirement spawns the warp to bellum in TotOK. The phantoms are spawned by
    default, and the staircase to bellum is blocked off until reaching the goal
    - spawn_bellumbeck: getting your goal requirement spawns the ruins of the ghost ship in the SW quadrant, and you
    can skip bellum 1 and the ghost ship fight
    """
    display_name = "bellum_access"
    option_spawn_phantoms_on_b13 = 0
    option_unlock_staircase = 1
    option_warp_to_bellum = 2
    option_spawn_bellumbeck = 3


class PhantomHourglassFrogRandomization(Choice):
    """
    Ramdomize golden cyclone frogs
    - vanilla: shooting a frog gives their warp spot
    - start_with: start with all warps unlocked. Frogs are not checks. You don't start with cyclone slate unless it's
    in starting_items. You also need their respective sea charts to actually warp.
    - randomize: frog glyphs are random and frogs are checks
    """
    display_name = "randomize_frogs"
    option_vanilla = 0
    option_start_with = 1
    option_randomize = 2
    default = 0


class PhantomHourglassBoatRequriesSeaChart(Toggle):
    """
    If True, heading out to sea from mercay requires the SW sea chart.
    WARNING! If set to False and you travel without a sea chart, you can softlock by crossing to another sea chart.
    Frogs require their sea chart to work
    """
    display_name = "Boat Requires Sea Chart"
    default = 1


@dataclass
class PhantomHourglassOptions(PerGameCommonOptions):
    # Accessibility
    accessibility: ItemsAccessibility

    # Goal
    goal: PhantomHourglassGoal
    dungeons_required: PhantomHourglassDungeonsRequired
    bellum_access: PhantomHourglassBellumAccess

    # Logic options
    logic: PhantomHourglassLogic
    phantom_combat_difficulty: PhantomHourglassPhantomCombatDifficulty
    boat_requires_sea_chart: PhantomHourglassBoatRequriesSeaChart

    # Item Randomization
    keysanity: PhantomHourglassKeyRandomization
    randomize_frogs: PhantomHourglassFrogRandomization
    randomize_triforce_crest: PhantomHourglassTriforceCrestRandomization

    # Phantom Hourglass
    ph_starting_time: PhantomHourglassStartingTime
    ph_time_increment: PhantomHourglassTimeIncrement

    start_inventory_from_pool: StartInventoryPool
    remove_items_from_pool: PhantomHourglassRemoveItemsFromPool
    death_link: DeathLink
