from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility
from worlds.tloz_ph.data.Items import ITEMS_DATA


class PhantomHourglassGoal(Choice):
    """
    The goal to accomplish in order to unlock the endgame specified in 'bellum_access'
    - Triforce_door: Open the triforce door on TotOK B6. Leftover from pre-alpha
    - complete_dungeons: complete dungeons to unlock the endgame
    - metal_hunt: collect a specified number of metals to unlock the endgame
    """
    display_name = "goal_requirements"
    option_triforce_door = 0
    option_complete_dungeons = 1
    option_metal_hunt = 2
    default = 1

class PhantomHourglassMetalHuntRequiredMetals(Range):
    """
    Number of metals required to win if metal hunt is enabled
    The item group 'Metals' can be used to specify all metals for generic settings, like local_items
    """
    display_name = "metal_hunt_required"
    range_start = 0
    range_end = 30
    default = 20

class PhantomHourglassMetalHuntTotalMetals(Range):
    """
    Total number of metals in the pool if metals are enabled
    If less than required metals, it is set to the required metal count
    """
    display_name = "metal_hunt_total"
    range_start = 0
    range_end = 30
    default = 25

class PhantomHourglassStartingTime(Range):
    """
    How much time in the Phantom Hourglass Item. There is one in the pool.
    You don't need to have found the Phantom Hourglass for Sand items to work
    """
    display_name = "Phantom Hourglass Starting Time"
    range_start = 0
    range_end = 5999
    default = 600


class PhantomHourglassTimeIncrement(Range):
    """
    How much time to get for each sand of hours upgrade, in seconds. It will try and create more upgrades items than you need.
    You don't need to have found the Phantom Hourglass to make use of the upgrades
    """
    display_name = "Increment for each Sand of Hours"
    range_start = 0
    range_end = 5999
    default = 60


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
    - Hard: Includes some cool unconventional uses of pots, tricky enemy fights and Molida Archery 2000
    - Glitched: Hammer clips, chu camera displacement and clever use of items in logic
    Be careful, using glitches on normal logic can cause key-related softlocks
    Full coverage of tricks included can be found here https://github.com/carrotinator/Archipelago/blob/main/worlds/tloz_ph/docs/tricks_and_skips.md
    """
    display_name = "logic"
    option_normal = 0
    option_hard = 1
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
    Small Key Logic options
    - vanilla: Keys are not randomized
    - in_own_dungeon: Keys can be found in their own dungeon
    - anywhere: Keysanity. Keys can be found anywhere
    You can use the item group "Small Keys" to specify further key options
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
    Max is 6 unless you add Ghost ship and TotOK with their own options below
    If metal hunt is enabled, this only effects what dungeons are excluded or not
    """
    display_name = "dungeons_required"
    range_start = 0
    range_end = 8
    default = 3


class PhantomHourglassBellumAccess(Choice):
    """
    What unlocks after you reach your goal requirement. For bellum options, game completion is sent on entering the credits.
    - spawn_phantoms_on_b13: getting your goal requirement spawns the phantoms on TotOK B13, and killing them gives \
    you bellum access. You will have to run TotOK to the bottom after getting your goal requirement
    - unlock_staircase: getting your goal requirement unlocks the staircase to bellum. The phantoms on B13 spawn by
    default, and killing them unlocks the warp for later
    - warp_to_bellum: getting your goal requirement spawns the warp to bellum in TotOK. The phantoms are spawned by
    default, and the staircase to bellum is blocked off until reaching the goal
    - spawn_bellumbeck: getting your goal requirement spawns the ruins of the ghost ship in the SW quadrant, and you
    can skip bellum 1 and the ghost ship fight
    - win: reaching your goal requirement wins the game
    """
    display_name = "bellum_access"
    option_spawn_phantoms_on_b13 = 0
    option_unlock_staircase = 1
    option_warp_to_bellum = 2
    option_spawn_bellumbeck = 3
    option_win = 4


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


class PhantomHourglassBoatRequiresSeaChart(Toggle):
    """
    If True, heading out to sea from mercay requires the SW sea chart.
    WARNING! If set to False and you travel without a sea chart, you can softlock by crossing to another sea chart.
    Frogs require their sea chart to work
    """
    display_name = "Boat Requires Sea Chart"
    default = 1


class PhantomHourglassFogSettings(Choice):
    """
    Choose when the fog exists in the NW Quadrant
    WARNING! The game crashes if you exit out to the NW quadrant with the spirits out. Enter and exit the ghost ship to remove them
    - no_fog: there's no fog in the NW quadrant. You need all 3 spirits to find the ghost ship
    - vanilla_fog: fog exists until you defeat the ghost ship, you have to take the twisty route to NW
    - open_ghost_ship: fog exists until you beat the ghost ship, and you don't need the spirit items to find it.
    """
    display_name = "Fog Settings"
    option_no_fog = 0
    option_vanilla_fog = 1
    option_open_ghost_ship = 2
    default = 0


class PhantomHourglassRandomizeHarrow(Choice):
    """
    Choose whether to randomize the rng hell checks on harrow island
    If enabled, the hint option with give you hints on entering the island
    """
    display_name = "randomize_harrow"
    option_no_harrow = 0
    option_randomize_with_hints = 1
    option_randomize_without_hints = 2
    default = 0


class PhantomHourglassGhostShipInDungeonPool(Choice):
    """
    Choose whether the ghost ship can be in the dungeon reward pool
    - rescue_tetra: the dungeon reward, if rolled, will be on using the ghost key
    - cubus_sisters: the dungeon reward will be on defeating the cubus sisters
    - false: the ghost ship cannot be rolled for the required dungeon pool
    """
    display_name = "Ghost Ship in Dungeon Pool"
    option_rescue_tetra = 0
    option_cubus_sisters = 1
    option_false = 2
    default = 0


class PhantomHourglassTotokInDungeonPool(Toggle):
    """
    Choose whether the NE Sea Chart chest on B13 of Temple of the Ocean King is in the dungeon reward pool
    """
    display_name = "TotOK in Dungeon Pool"
    default = 0


class PhantomHourglassRandomizeMaskedBeedle(Toggle):
    """
    Choose whether to randomize the masked beedle ship. You may need to change time of day for this.
    Masked beedle appears between 10pm and midnight on weekdays or 10am and noon on weekends.
    """
    auto_display_name = "masked_beedle"
    default = 0


class PhantomHourglassDungeonHints(Choice):
    """
    Receive hints for your required dungeons
    - false: no hints
    - oshus: oshus gives dungeon hints
    - totok: entering totok gives dungeon hints
    """
    display_name = "dungeon_hints"
    option_false = 0
    option_oshus = 1
    option_totok = 2
    default = 1


class PhantomHourglassExcludeNonRequriedDungeons(Toggle):
    """
    Non-required dungeons won't have progression or useful items. Does not apply to TotOK.
    """
    display_name = "exclude_non_required_dungeons"
    default = 1


class PhantomHourglassHintSpiritIsland(Choice):
    """
    Get hints for spirit island upgrades on entering the shrine
    - all: get hints for all upgrades
    - level_two: only get hints for the 2nd level upgrades
    - none: don't receive hints
    """
    display_name = "hint_spirit_island"
    option_all = 0
    option_level_two = 1
    option_none = 2
    default = 0


class PhantomHourglassShopHints(Toggle):
    """
    Get hints for shop items you currently can buy
    Includes island shops, Beedle, masked Beedle and Eddo
    """
    display_name = "hint_shops"
    default = 1


class PhantomHourglassRandomizeDigSpots(Toggle):
    """
    Randomize dig spots that give 100-300 rupees
    """
    display_name = "randomize_rupee_dig_spots"
    default = 1


class PhantomHourglassRandomizeMinigames(Choice):
    """
    Randomize the following minigames:
    - Bannan Cannon Game
    - Molida Archery
    - Dee Ess Goron Game
    - Maze Island Main Rewards
    - Prince of Red Lions Fight
    if the hint option is on, all minigame rewards will be hinted for on entering their scene
    """
    display_name = "randomize_minigames"
    option_no_minigames = 0
    option_randomize_with_hints = 1
    option_randomize_without_hints = 2
    default = 2


class PhantomHourglassSkipOceanFights(Toggle):
    """
    The Massive Eye fight before Goron Island, ice pillars around Isle of Frost and Giant Eye Plant before Bannan trade
    quest item are removed, and cannon isn't required for those locations
    """
    display_name = "skip_ocean_fights"
    default = 0


class PhantomHourglassRandomizeFishing(Choice):
    """
    Adds checks for catching the 6 fish you can catch at sea, and handing in 4 fish to the wayfarer on bannan island.
    The hint option also gives free hints for the catching fish checks on entering the wayfarers hut on bannan island.
    """
    display_name = "randomize_fishing"
    option_no_fish = 0
    option_randomize_with_hints = 1
    option_randomize_without_hints = 2
    default = 0


class PhantomHourglassSpiritGemPacks(Range):
    """
    Instead of having 20 individual spirit gems of each type, you get them in packs of n
    """
    display_name = "spirit_gem_packs"
    range_vanilla = 1
    range_packs_of_4 = 4
    range_start = 1
    range_end = 20
    default = 1


class PhantomHourglassAdditionalSpiritGems(Range):
    """
    Adds additional spirit gems/packs to the pool.
    At 0 there will be exactly enough to get both upgrade locations
    Can cause generation errors if too many locations are excluded
    """
    display_name = "additional_spirit_gems"
    range_start = 0
    range_end = 5
    default = 0


class PhantomHourglassRandomizeSalvage(Choice):
    """
    Randomize all 31 treasure maps and salvage locations!
    Hint option gives you a hint for the location on receiving the map item
    """
    display_name = "randomize_salvage"
    option_no_salvage = 0
    option_randomize_with_hints = 1
    option_randomize_without_hints = 2


class PhantomHourglassZauzRequiredMetals(Range):
    """
    How many rare metals you need to have obtained for zauz to give the phantom blade forging check
    If the value is greater than the number of required dungeons/total metal hunt items, the value will be the number
    of dungeons/total metals
    """
    display_name = "zauz_required_metals"
    range_start = 0
    range_end = 30
    default = 3

class PhantomHourglassAdditionalMetalNames(Choice):
    """
    If there are more than 3 rare metals in the pool, what should the additional items be called?
    - vanilla_only: additional metals are duplicate vanilla metals
    - additional_rare_metal: additional metals are all called "Additional Rare Metal"
    - custom_metals: additional metals are chosen randomly from a pre-defined list of names I made up. The names are
    based on color words ending in "ine". Some examples are "Verdantine", "Lavendine" and "Amberine". Currently there
    30 metal names defined.
    - custom_metals_unique: same as custom metals, but there can only be 1 of each item. Additional metals will be
    named "Additional Rare Metal"
    """
    display_name = "additional_metal_names"
    option_vanilla_only = 0
    option_additional_rare_metal = 1
    option_custom = 2
    option_custom_unique = 3
    default = 1

class PhantomHourglassTimeLogic(Choice):
    """
    Logic Requirements for Sand of Hours in Temple of the Ocean King
    - easy: each check has a time requirement based on walking to each location. Does not take yellow pots into account.
    Expects you to get everything with ~5 minutes
    - medium: half of the easy times. Expects you to get everything with ~2.5 minutes
    - hard: a quarter of the easy times. Expects you to get everything with ~1.25 minutes
    - ph_only_b1: only the phantom hourglass item is required for checks past b1, checks above that are always in logic
    - ph_only_b4: only the phantom hourglass item is required for checks past b4, checks above that are always in logic
    - no_logic: Sand of Hours does not effect logic
    """
    display_name = "ph_time_logic"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_ph_only_b1 = 3
    option_ph_only_b4 = 4
    option_no_logic = 5
    default = 0

class PhantomHourglassHeartLogic(Range):
    """
    How much to value hearts as sand in Temple of the Ocean King, in seconds.
    Counts 2 out of your 3 starting hearts.
    Standing in the open, each heart depletes after 9 seconds.
    Keep in mind that hearts in pots respawn infinitely
    """
    display_name = "ph_heart_time"
    default = 0
    range_start = 0
    range_end = 60

class PhantomHourglassRandomizeBeedlePoints(Choice):
    """
    Adds locations to the five membership cards in Beedle's shop, point items to help reach their thresholds and adds
    the Freebie Card, Complimentary Card and Compliment card to the pool
    Point thresholds are at 0, 20, 50, 100 and 200.
    - no_beedle_points: don't randomize this
    - cards_only: adds the cards to the item pool, but doesn't randomize the membership card
    - randomize: randomizes the beedle membership levels. You will only be logically expected to buy the first level.
    - randomize_with_grinding: randomizes the beedle membership levels. If you have a farmable source of rupees, the
    game can expect you to farm 20 000 rupees and use time travelling to buy out his stock day after day. Don't pick
    unless you know what you're signing up for
    """
    display_name = "randomize_beedle_membership"
    option_no_beedle_points = 0
    option_cards_only = 1
    option_randomize = 2
    option_randomize_with_grinding = 3
    default = 1

@dataclass
class PhantomHourglassOptions(PerGameCommonOptions):
    # Accessibility
    accessibility: ItemsAccessibility

    # Goal
    goal_requirements: PhantomHourglassGoal
    bellum_access: PhantomHourglassBellumAccess

    # Dungeons
    dungeons_required: PhantomHourglassDungeonsRequired
    exclude_non_required_dungeons: PhantomHourglassExcludeNonRequriedDungeons
    ghost_ship_in_dungeon_pool: PhantomHourglassGhostShipInDungeonPool
    totok_in_dungeon_pool: PhantomHourglassTotokInDungeonPool

    # Metal Hunt
    metal_hunt_required: PhantomHourglassMetalHuntRequiredMetals
    metal_hunt_total: PhantomHourglassMetalHuntTotalMetals

    # Logic options
    logic: PhantomHourglassLogic
    phantom_combat_difficulty: PhantomHourglassPhantomCombatDifficulty
    boat_requires_sea_chart: PhantomHourglassBoatRequiresSeaChart

    # Item Randomization
    keysanity: PhantomHourglassKeyRandomization
    randomize_minigames: PhantomHourglassRandomizeMinigames
    randomize_frogs: PhantomHourglassFrogRandomization
    randomize_fishing: PhantomHourglassRandomizeFishing
    randomize_salvage: PhantomHourglassRandomizeSalvage
    randomize_harrow: PhantomHourglassRandomizeHarrow
    randomize_digs: PhantomHourglassRandomizeDigSpots
    randomize_triforce_crest: PhantomHourglassTriforceCrestRandomization
    randomize_beedle_membership: PhantomHourglassRandomizeBeedlePoints
    randomize_masked_beedle: PhantomHourglassRandomizeMaskedBeedle

    # Hint Options
    dungeon_hints: PhantomHourglassDungeonHints
    shop_hints: PhantomHourglassShopHints
    spirit_island_hints: PhantomHourglassHintSpiritIsland

    # World Options
    fog_settings: PhantomHourglassFogSettings
    skip_ocean_fights: PhantomHourglassSkipOceanFights
    zauz_required_metals: PhantomHourglassZauzRequiredMetals

    # Spirit Gem options
    spirit_gem_packs: PhantomHourglassSpiritGemPacks
    additional_spirit_gems: PhantomHourglassAdditionalSpiritGems

    # Phantom Hourglass options
    ph_time_logic: PhantomHourglassTimeLogic
    ph_starting_time: PhantomHourglassStartingTime
    ph_heart_time: PhantomHourglassHeartLogic
    ph_time_increment: PhantomHourglassTimeIncrement

    # Cosmetic
    additional_metal_names: PhantomHourglassAdditionalMetalNames

    # Generic
    start_inventory_from_pool: StartInventoryPool
    remove_items_from_pool: PhantomHourglassRemoveItemsFromPool
    death_link: DeathLink
