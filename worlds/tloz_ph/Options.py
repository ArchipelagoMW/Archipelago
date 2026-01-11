from dataclasses import dataclass
from datetime import datetime
from .data.Entrances import ENTRANCES

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility, OptionGroup, PlandoConnections
from worlds.tloz_ph.data.Items import ITEMS_DATA


class PhantomHourglassGoal(Choice):
    """
    The goal to accomplish in order to unlock the endgame specified in 'bellum_access'
    - Triforce_door: Open the triforce door on TotOK B6. Leftover from pre-alpha
    - defeat_bosses: defeat bosses/collect dungeon rewards to unlock the endgame
    - metal_hunt: collect a specified number of metals to unlock the endgame
    """
    display_name = "goal_requirements"
    option_triforce_door = 0
    option_defeat_bosses = 1
    option_metal_hunt = 2
    default = 1

class PhantomHourglassMetalHuntRequiredMetals(Range):
    """
    Number of metals required to win if metal hunt is enabled
    The item group 'Metals' can be used to specify all metals for generic settings, like local_items
    Setting too high of a value can max the item pool depending on other settings, this will fail generation
    """
    display_name = "metal_hunt_required"
    range_start = 0
    range_end = 50
    default = 20

class PhantomHourglassMetalHuntTotalMetals(Range):
    """
    Total number of metals in the pool if metals are enabled
    If less than required metals, it is set to the required metal count
    Setting too high of a value can max the item pool depending on other settings, this will fail generation
    """
    display_name = "metal_hunt_total"
    range_start = 0
    range_end = 50
    default = 25

class PhantomHourglassStartingTime(Range):
    """
    How much time given by the Phantom Hourglass item. There is one in the pool.
    """
    display_name = "Phantom Hourglass Starting Time"
    range_start = 0
    range_end = 5999
    default = 600

class PhantomHourglassTimeRequiresHourglass(Toggle):
    """
    Whether you need the phantom hourglass to make use of Sand of Hours.
    If false the Phantom Hourglass functions like one big optional time item.
    Hearts still count for time logic if True
    """
    display_name = "ph_required"
    default = 0

class PhantomHourglassTimeIncrement(Range):
    """
    How much time to get for each sand of hours upgrade, in seconds. It will try and create more upgrades items than you need.
    You don't need to have found the Phantom Hourglass to make use of the upgrades
    If you exclude as many locations as possible, and have 30 metal items, generation breaks at 6 seconds
    """
    display_name = "Increment for each Sand of Hours"
    range_start = 1
    range_end = 5999
    default = 60


class PhantomHourglassRemoveItemsFromPool(ItemDict):
    """
    Removes specified amount of given items from the item pool, replacing them with random filler items.
    This option has significant chances to break generation if used carelessly, so test your preset several times
    before using it on long generations. Use at your own risk!
    """
    display_name = "remove_items_from_pool"


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

class PhantomHourglassRandomizeBossKeys(Choice):
    """
    Randomize Boss Keys. Automatically sets boss_key_behaviour to inventory if not vanilla.
    - vanilla: Boss Keys are not randomized
    - in_own_dungeon: Boss Keys can be found in their own dungeon
    - anywhere: Boss Keys can be found anywhere
    """
    display_name = "randomize_boss_keys"
    option_vanilla = 0
    option_in_own_dungeon = 1
    option_anywhere = 2
    default = 0

class PhantomHourglassTriforceCrestRandomization(Toggle):
    """
    When enabled, The Triforce Crest on the big red door in TotOK B6 will turn into an item and be randomized.
    When disabled, the door will always be open
    """
    display_name = "randomize_triforce_crest"
    default = 0


class PhantomHourglassDungeonsRequired(Range):
    """
    How many dungeons/bosses are required to access the endgame.
    Max is 6 unless you add Ghost ship and TotOK with their own options below.
    If metal hunt is enabled, this only effects what dungeons are excluded or not.
    If boss shuffle is on and bosses are in a mixed pool, this will still affect the number of excluded dungeons.
    """
    display_name = "dungeons_required"
    range_start = 0
    range_end = 8
    default = 3


class PhantomHourglassBellumAccess(Choice):
    """
    What unlocks after you reach your goal requirement. For bellum options, game completion is sent on entering the credits.
    - spawn_phantoms_on_b13: getting your goal requirement spawns the phantoms on TotOK B13,
    and killing them gives you bellum access. You will have to run TotOK to the bottom after getting your goal requirement
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
    default = 2


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
    If True, heading out to sea from any island requires the sea chart for the ocean it's connected to.
    WARNING! If set to False and you cross a sea boundary without a sea chart, you can't come back without warping to start.
    This is in logic.
    Sea Charts for the quadrant you are entering are always required to cross the quadrant boundary.
    The chart from the one you are exiting is not.
    Frogs require their sea chart to work.
    Works from all islands and with entrance rando
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
    Choose whether the ghost ship can be in the boss/dungeon reward pool.
    Has *interactions* with boss_shuffle.
    - rescue_tetra: the dungeon reward, if rolled, will be on using the ghost key and climbing the staircase.
    - cubus_sisters: the dungeon reward will be on defeating the Cubus Sisters,
    or whatever boss gets randomized there with boss shuffle.
    - false: the ghost ship cannot be rolled for the required dungeon pool.
    """
    display_name = "Ghost Ship in Dungeon Pool"
    option_rescue_tetra = 0
    option_cubus_sisters = 1
    option_false = 2
    default = 0


class PhantomHourglassTotokInDungeonPool(Toggle):
    """
    Choose whether the NE Sea Chart chest on B13 of Temple of the Ocean King is in the boss/dungeon reward pool
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


class PhantomHourglassDungeonHintLocation(Choice):
    """
    Where to receive dungeon hints etc
    - start: give dungeon hints on starting a new save file
    - oshus: oshus gives dungeon hints
    - totok: entering the totok lobby gives dungeon hints
    """
    display_name = "dungeon_hint_location"
    option_start = 0
    option_oshus = 1
    option_totok = 2
    default = 1

class PhantomHourglassDungeonHintType(Choice):
    """
    Whether the dungeon hint tells you what dungeon is required, or what boss is required
    - no_hints: don't hint for dungeon rewards
    - hint_dungeon: hint the required dungeon, in plain text, to avoid spoiling randomized bosses.
    If bosses are shuffled with other location types, this will not hint for dungeons.
    Use excluded_dungeon_hints instead.
    - hint_boss: hint the required boss reward, as an archipelago hint
    """
    option_no_hints = 0
    option_hint_dungeon = 1
    option_hint_boss = 2
    default = 2

class PhantomHourglassExcludedDungeonHints(Toggle):
    """
    Give hints, in plain text, for the excluded dungeons.
    """
    default = 0

class PhantomHourglassExcludeNonRequriedDungeons(Toggle):
    """
    Non-required dungeons won't have progression or useful items.
    Does not apply to TotOK.
    If you don't require specific bosses, this will still make a number of dungeons barren.
    They will still count towards dungeon completions.
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
    default = 1


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
    - custom_metals_prefer_vanilla: metals will default to vanilla names, and only use custom names if you have more than 3.
    """
    display_name = "additional_metal_names"
    option_vanilla_only = 0
    option_additional_rare_metal = 1
    option_custom = 2
    option_custom_prefer_vanilla = 3
    default = 1

class PhantomHourglassTimeLogic(Choice):
    """
    Logic Requirements for Sand of Hours in Temple of the Ocean King
    - beginner: double the time requirement of easy. Expects you to get everything with ~10 minutes
    - easy: each check has a time requirement based on walking to each location. Does not take yellow pots into account.
    Expects you to get everything with ~5 minutes
    - medium: half of the easy times. Expects you to get everything with ~2.5 minutes
    - hard: a quarter of the easy times. Expects you to get everything with ~1.25 minutes
    - ph_only_b1: only the phantom hourglass item is required for checks past b1, checks above that are always in logic
    - ph_only_b4: only the phantom hourglass item is required for checks past b4, checks above that are always in logic
    - no_logic: Sand of Hours does not effect logic
    """
    display_name = "ph_time_logic"
    option_beginner = -1
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
    - cards_only: adds the Freebie, Comploment and Complimentary cards to the item pool, but doesn't randomize
    Membership thresholds
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

class PhantomHourglassAddItemsToPool(ItemDict):
    """
    Add items to pool. Useful for adding duplicates
    """
    display_name = "add_items_to_pool"

class PhantomHourglassDungeonShortcuts(Toggle):
    """
    Adds shortcuts from the beginning of islands to their dungeons, often by entering the house nearest their port.
    Requires getting the first check in the respective dungeon to activate.
    Disabled automatically with house ER or internal island ER (and dungeon ER until i add support for it)
    """
    display_name = "dungeon_shortcuts"
    default = 0

class PhantomHourglassTotOKCheckpoints(Toggle):
    """
    Redirects the yellow warp portal in the lobby to the deepest floor with a blue warp you've visited.
    Entering that blue warp again will take you one warp portal up the dungeon.
    """
    default = 0
    visibility = Visibility.none

class PhantomHourglassShuffleDungeonEntrances(Choice):
    """
    Shuffle what dungeon entrance leads to which dungeon interior.
    - no_shuffle: don't shuffle dungeon entrances
    - shuffle: shuffle dungeon entrances
    - simple_mixed_pool: shuffles dungeon entrances with other entrance types that have this option
    """
    display_name = "shuffle_dungeon_entrances"
    default = 0
    option_no_shuffle = 0
    option_shuffle = 1
    option_simple_mixed_pool = 2

class PhantomHourglassShuffleIslands(Choice):
    """
    Shuffle what island port leads to which island overworld.
    Does not include ghost ship or travellers ships.
    The sea counts as a neutral island, and thus shuffling on own island will still allow for sea connections anywhere.
    This however, tends to cause generation errors when mixed with other pools, especially if they have lots of dead ends.
    Compatible with boat requires sea chart.
    - no_shuffle: don't shuffle ports
    - shuffle: shuffle ports
    - simple_mixed_pool: shuffles ports with other entrance types that have this option
    """
    display_name = "shuffle_ports"
    default = 0
    option_no_shuffle = 0
    option_shuffle = 1
    option_simple_mixed_pool = 2


class PhantomHourglassShuffleCaves(Choice):
    """
    Shuffle cave entrances. Includes caves, staircases and drop down holes.
    Entrances are coupled and preserve direction unless specified in another option.
    - no_shuffle: don't shuffle caves
    - shuffle: shuffle caves
    - simple_mixed_pool: shuffles caves with other entrance types that have this option
    - shuffle_on_own_island: caves on each island will be shuffled with each other. Overrides the shuffle_between_islands option.
    """
    display_name = "shuffle_caves"
    option_no_shuffle = 0
    option_shuffle = 1
    option_simple_mixed_pool = 2
    option_shuffle_on_own_island = 3
    default = 0

class PhantomHourglassShuffleHouses(Choice):
    """
    Shuffle house entrances. Includes houses, shops, pyramids and Goron houses.
    If houses are alone in their pool, they always preserve directionality, cause GER would otherwise force pair dead ends with each other
    - no_shuffle: don't shuffle houses
    - shuffle: shuffle houses
    - simple_mixed_pool: shuffles houses with other entrance types that have this option
    - shuffle_on_own_island: houses on each island will be shuffled with each other. Overrides the shuffle_between_islands option.
    """
    display_name = "shuffle_houses"
    option_no_shuffle = 0
    option_shuffle = 1
    option_simple_mixed_pool = 2
    option_shuffle_on_own_island = 3
    default = 0

class PhantomHourglassShuffleOverworldTransitions(Choice):
    """
    Shuffle overworld transitions, between the quadrants of islands.
    Different heights and breaks in terrain create separate transitions.
    Entrances are coupled and preserve direction unless specified in another option.
    If glitched logic is enabled, includes out of bounds transitions that are reachable in vanilla (coming soon).
    - no_shuffle: don't shuffle island transitions
    - shuffle: shuffle overworld transitions
    - simple_mixed_pool: shuffles houses with other entrance types that have this option
    - shuffle_on_own_island: overworld transitions on each island will be shuffled with each other. Overrides the shuffle_between_islands option.
    """
    display_name = "shuffle_overworld_transitions"
    option_no_shuffle = 0
    option_shuffle = 1
    option_simple_mixed_pool = 2
    option_shuffle_on_own_island = 3
    default = 0

class PhantomHourglassShuffleBetweenIslands(Choice):
    """
    Either preserve or disregard directionality for entrances shuffled in other options.
    CAUTION: When combined with pools that have a lot of dead ends, it can cause a high chance of generation failure.
    Please test generate before submitting to a public game.
    - shuffle_anywhere: entrances in a pool can connect to other entrances in that pool no matter their island.
    - shuffle_only_on_own_island: entrances in a pool can only connect to other entrances in that pool if they're on the same island.
    - limit_simple_mixed_pool: entrances in the simple_mixed_pool are only shuffled with entrances on their own island. other pools can be shuffled between islands.
    - limit_all_but_simple_mixed_pool: entrances not in the simple_mixed_pool are only shuffled with entrances on their own island. entrances in the simple mixed pool can be shuffled between islands.
    """
    option_shuffle_anywhere = 0
    option_shuffle_only_on_own_island = 1
    option_limit_simple_mixed_pool = 2
    option_limit_all_but_simple_mixed_pool = 3
    default = 0

class PhantomHourglassDecoupleEntrances(Choice):
    """
    Decouples entrances such that entrances are no longer bidirectional.
    Only applies to entrances enabled in other settings.
    CAUTION: High chance of generation failure if combined with the wrong settings.
    - couple_all: don't decouple
    - decouple_all: decouple all enabled entrance shuffles
    """
    option_couple_all = 0
    option_decouple_all = 1
    display_name = "decouple_entrances"
    default = 0

class PhantomHourglassPreserveDirectionality(Choice):
    """
    Either preserve or disregard directionality for entrances shuffled in other options.
    CAUTION: When combined with pools that have a lot of dead ends, it can cause a high chance of generation failure.
    Please test generate before submitting to a public game.
    - preserve: preserve directionality for all shuffled entrances
    - disregard_all: disregard directionality for all shuffled entrances
    - disregard_simple_mixed_pool: disregard directionality for all shuffled entrances is the simple mixed pool, but preserve the others
    - disregard_all_but_simple_mixed_pool: preserve directionality for all shuffled entrances in the simple mixed pool, and disregard directionality for all others.
    """
    option_preserve_all = 0
    option_disregard_all = 1
    option_disregard_simple_mixed_pool = 2
    option_disregard_all_but_simple_mixed_pool = 3

class PhantomHourglassBossKeyBehavior(Choice):
    """
    How boss keys work as items
    - vanilla: boss key has to be carried to the boss door. Not compatible with boss key rando or internal dungeon shuffle.
    - inventory: getting the boss key item automatically opens it's boss door.
    You may need to reload the room if you got the key in the same room as it's door.
    """
    option_vanilla = 0
    option_inventory = 1
    default = 0
    display_name = "boss_key_behavior"

class PhantomHourglassSwitchBehaviour(Choice):
    """
    Modify the behaviour of color switches.
    - vanilla: switches are dungeon local and reset each time you exit that dungeon or save and quit.
    If playing with internal dungeon shuffle, this means that each time you enter a dungeon room the switch state will be in the default state (red).
    - save_per_dungeon: Switch states are dungeon specific, but the game will remember what state you left it in. Fun for internal dungeon randomizer.
    - save_globally: all switches are linked together, and affect all dungeons!
    """
    option_vanilla = 0
    option_save_per_dungeon = 1
    option_save_globally = 2
    default = 0
    display_name = "color_switch_behaviour"
    visibility = Visibility.none

class PhantomHourglassShuffleDungeonTransitions(Choice):
    """
    Shuffle internal rooms in dungeons. Includes Staircases, caves and blue warps.
    Boss rooms are done with a separate option
    If glitched logic is enabled, includes out of bounds transitions that are reachable in vanilla.
    - no_shuffle: don't shuffle island transitions
    - shuffle: shuffle overworld transitions
    - simple_mixed_pool: shuffles houses with other entrance types that have this option
    """
    display_name = "shuffle_dungeons_internally"
    option_no_shuffle = 0
    option_shuffle = 1
    option_simple_mixed_pool = 2
    default = 0
    visibility = Visibility.none

class PhantomHourglassShuffleBosses(Choice):
    """
    Shuffle Boss rooms.
    Dungeon rewards being tied to boss or dungeon is set in a separate option.
    The boss doors of excluded dungeons can still shuffle to required locations if in mixed pool.
    - no_shuffle: don't shuffle island transitions
    - shuffle: shuffle boss rooms amongst each other
    - simple_mixed_pool: shuffles boss rooms with other entrance types that have this option
    """
    display_name = "shuffle_bosses"
    option_no_shuffle = 0
    option_shuffle = 1
    option_simple_mixed_pool = 2
    default = 0

class PhantomHourglassRequireSpecificBosses(Toggle):
    """
    Whether you require specific dungeons/bosses for dungeon goal or if all bosses/dungeon rewards count.
    Setting it to false will put a rare metal on every boss reward location, no matter how many are required or if the dungeon is excluded.
    """
    display_name = "dungeon_reward_type"
    default = 1

class PhantomHourglassEntrancePlando(PlandoConnections):
    """
    Plando entrance connections. Format is a list of dictionaries:
    - entrance: "Entrance Name"
      exit: "Exit Name"
      direction: "Direction"
      percentage: 100
    Direction must be one of 'entrance', 'exit', or 'both', and defaults to 'both' if omitted.
    Percentage is an integer from 1 to 100, and defaults to 100 when omitted.
    Will disconnect entrances for you, and randomize their dangling entrances with each other if their entrance groups allow it.
    """
    display_name = "Transition Plando"
    entrances = frozenset(ENTRANCES.keys())
    exits = frozenset(ENTRANCES.keys())

class PhantomHourglassRandomizePedestalItems(Choice):
    """
    Randomize shape crystals and force gems.
    The randomize options will also create items for the items carried by phantoms.
    The phantom's items won't be removed, and can still be used, but having the abstract items will open them for you no hauling required.
    - vanilla: don't randomize. you have to haul your shapes to their pedestals
    - vanilla_abstract: don't randomize, but the shapes get converted to abstract items that take immediate effect.
    - in_own_dungeon: randomize in own dungeon
    - anywhere: randomize anywhere
    """
    display_name = "Randomize Pedestal Items"
    option_vanilla = 0
    option_vanilla_abstract = 1
    option_in_own_dungeon = 2
    option_anywhere = 3
    default = 0

class PhantomHourglassPedestalOptions(Choice):
    """
    How to randomize pedestal items. Only take effect when pedestal items are randomized.
    open_per_dungeon: one crystal per dungeon, that opens all their pedestals. There are 3 force gems per force gem floor.
    unique_pedestals: creates an item for each pedestal, opening them individually.
    open_globally: There will only be one of each type of crystal/force gem. They will open all pedestals, no matter the dungeon. If randomized in own dungeon, they can end up in any dungeon with a matching pedestal.
    """
    display_name = "Pedestal Item Options"
    option_open_per_dungeon = 0
    option_unique_pedestals = 1
    option_open_globally = 2
    default = 0

@dataclass
class PhantomHourglassOptions(PerGameCommonOptions):
    # Accessibility

    # Goal
    goal_requirements: PhantomHourglassGoal
    bellum_access: PhantomHourglassBellumAccess

    # Dungeons
    dungeons_required: PhantomHourglassDungeonsRequired
    require_specific_bosses: PhantomHourglassRequireSpecificBosses
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
    randomize_pedestal_items: PhantomHourglassRandomizePedestalItems
    randomize_boss_keys: PhantomHourglassRandomizeBossKeys
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
    dungeon_hint_type: PhantomHourglassDungeonHintType
    dungeon_hint_location: PhantomHourglassDungeonHintLocation
    excluded_dungeon_hints: PhantomHourglassExcludedDungeonHints
    shop_hints: PhantomHourglassShopHints
    spirit_island_hints: PhantomHourglassHintSpiritIsland

    # World Options
    boss_key_behaviour: PhantomHourglassBossKeyBehavior
    pedestal_item_options: PhantomHourglassPedestalOptions
    color_switch_behaviour: PhantomHourglassSwitchBehaviour
    fog_settings: PhantomHourglassFogSettings
    skip_ocean_fights: PhantomHourglassSkipOceanFights
    zauz_required_metals: PhantomHourglassZauzRequiredMetals
    dungeon_shortcuts: PhantomHourglassDungeonShortcuts
    totok_checkpoints: PhantomHourglassTotOKCheckpoints

    # Spirit Gem options
    spirit_gem_packs: PhantomHourglassSpiritGemPacks
    additional_spirit_gems: PhantomHourglassAdditionalSpiritGems

    # Phantom Hourglass options
    ph_time_logic: PhantomHourglassTimeLogic
    ph_required: PhantomHourglassTimeRequiresHourglass
    ph_starting_time: PhantomHourglassStartingTime
    ph_heart_time: PhantomHourglassHeartLogic
    ph_time_increment: PhantomHourglassTimeIncrement

    # ER
    shuffle_dungeon_entrances: PhantomHourglassShuffleDungeonEntrances
    shuffle_ports: PhantomHourglassShuffleIslands
    shuffle_caves: PhantomHourglassShuffleCaves
    shuffle_houses: PhantomHourglassShuffleHouses
    shuffle_overworld_transitions: PhantomHourglassShuffleOverworldTransitions
    # Shuffle sea transitions
    shuffle_bosses: PhantomHourglassShuffleBosses
    shuffle_dungeons_internally: PhantomHourglassShuffleDungeonTransitions
    # Shuffle travelling ships
    # Shuffle TotOK internally
    entrance_directionality: PhantomHourglassPreserveDirectionality
    shuffle_between_islands: PhantomHourglassShuffleBetweenIslands
    decouple_entrances: PhantomHourglassDecoupleEntrances
    plando_transitions: PhantomHourglassEntrancePlando

    # Cosmetic
    additional_metal_names: PhantomHourglassAdditionalMetalNames

    # Generic
    accessibility: ItemsAccessibility
    start_inventory_from_pool: StartInventoryPool
    add_items_to_pool: PhantomHourglassAddItemsToPool
    remove_items_from_pool: PhantomHourglassRemoveItemsFromPool
    death_link: DeathLink


ph_option_groups = [
    OptionGroup("Goal Options", [
        PhantomHourglassGoal,
        PhantomHourglassBellumAccess
    ]),
    OptionGroup("Dungeon Options", [
        PhantomHourglassDungeonsRequired,
        PhantomHourglassRequireSpecificBosses,
        PhantomHourglassExcludeNonRequriedDungeons,
        PhantomHourglassGhostShipInDungeonPool,
        PhantomHourglassTotokInDungeonPool
    ]),
    OptionGroup("Metal Hunt Options", [
        PhantomHourglassMetalHuntRequiredMetals,
        PhantomHourglassMetalHuntTotalMetals
    ]),
    OptionGroup("Logic Options", [
        PhantomHourglassLogic,
        PhantomHourglassPhantomCombatDifficulty,
        PhantomHourglassBoatRequiresSeaChart
    ]),
    OptionGroup("Item Randomization Options", [
        PhantomHourglassKeyRandomization,
        PhantomHourglassRandomizePedestalItems,
        PhantomHourglassRandomizeBossKeys,
        PhantomHourglassRandomizeMinigames,
        PhantomHourglassFrogRandomization,
        PhantomHourglassRandomizeFishing,
        PhantomHourglassRandomizeSalvage,
        PhantomHourglassRandomizeHarrow,
        PhantomHourglassRandomizeDigSpots,
        PhantomHourglassTriforceCrestRandomization,
        PhantomHourglassRandomizeBeedlePoints,
        PhantomHourglassRandomizeMaskedBeedle
    ]),
    OptionGroup("Hint Options", [
        PhantomHourglassDungeonHintType,
        PhantomHourglassDungeonHintLocation,
        PhantomHourglassExcludedDungeonHints,
        PhantomHourglassShopHints,
        PhantomHourglassHintSpiritIsland
    ]),
    OptionGroup("World Options", [
        PhantomHourglassFogSettings,
        PhantomHourglassSkipOceanFights,
        PhantomHourglassZauzRequiredMetals,
        PhantomHourglassDungeonShortcuts,
        PhantomHourglassTotOKCheckpoints,
        PhantomHourglassSwitchBehaviour,
        PhantomHourglassBossKeyBehavior,
        PhantomHourglassPedestalOptions
    ]),
    OptionGroup("Spirit Gem Options", [
        PhantomHourglassSpiritGemPacks,
        PhantomHourglassAdditionalSpiritGems
    ]),
    OptionGroup("TotOK Time Options", [
        PhantomHourglassTimeLogic,
        PhantomHourglassTimeRequiresHourglass,
        PhantomHourglassStartingTime,
        PhantomHourglassHeartLogic,
        PhantomHourglassTimeIncrement
    ]),
    OptionGroup("Entrance Randomizer Options", [
        PhantomHourglassShuffleDungeonEntrances,
        PhantomHourglassShuffleIslands,
        PhantomHourglassShuffleCaves,
        PhantomHourglassShuffleHouses,
        PhantomHourglassShuffleOverworldTransitions,
        PhantomHourglassShuffleDungeonTransitions,
        PhantomHourglassShuffleBosses,
        PhantomHourglassPreserveDirectionality,
        PhantomHourglassDecoupleEntrances,
        PhantomHourglassShuffleBetweenIslands,
        PhantomHourglassEntrancePlando
    ]),
    OptionGroup("Cosmetic Options", [
        PhantomHourglassAdditionalMetalNames
    ]),
    OptionGroup("Item & Location Options", [
        PhantomHourglassAddItemsToPool,
        PhantomHourglassRemoveItemsFromPool
    ]),
]


