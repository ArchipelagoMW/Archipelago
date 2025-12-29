from dataclasses import dataclass
from schema import And, Optional, Schema

from Options import Choice, DefaultOnToggle, OptionDict, PerGameCommonOptions, Range, StartInventoryPool, Toggle

from .item_data import jade_items


class ShuffleSolSeals(DefaultOnToggle):
    """Allows the Sol Seal items to be placed on any location in the multiworld, instead of their vanilla locations."""
    display_name = "Shuffle Sol Seals"


class SealsForEigong(Range):
    """The number of Sol Seals needed to open the door in Central Hall to New Kunlun Control Hub, fight Eigong,
    and complete the goal.

    Unlike the vanilla game, you don't need to visit Tiandao Research Center or trigger the 'point of no return'."""
    display_name = "Seals For Eigong"
    range_start = 0
    range_end = 8
    default = 8


class SealsForPrison(Range):
    """The number of Sol Seals needed for Jiequan in Factory (Great Hall) to allow you to 'fight' him,
    do the whole Prison escape sequence, and check most of the locations in Factory (Machine Room).

    Note that you will also need certain progression items for Jiequan to 'fight' you,
    since you can't finish the Prison escape sequence without them.
    Exactly which items you need depends on whether `prevent_weakened_prison_state` is enabled,
    but you can check what you're missing by walking up to F(GH) Jiequan, and it will be some combination of
    Ledge Grab, Grapple, Cloud Leap and Mystic Nymph: Scout Mode.

    Unlike the vanilla game, the real Jiequan fight may be done before or after Prison.
    Also, it does not matter which Sol Seals you've collected, only the total number."""
    display_name = "Seals For Prison"
    range_start = 0
    range_end = 8
    default = 3


class SealsForEthereal(Range):
    """The number of Sol Seals needed for the entrance to Lady Ethereal's soulscape to appear in Cortex Center.
    See also the skip_soulscape_platforming option.

    Unlike the vanilla game, it does not matter which Sol Seals you've collected, only the total number.
    The maximum is 7 instead of 8 because 8 would be incompatible with shuffle_sol_seals: false."""
    display_name = "Seals For Ethereal"
    range_start = 0
    range_end = 7
    default = 4


class SkipSoulscapePlatforming(Toggle):
    """After you collect enough Sol Seals to unlock Lady Ethereal's soulscape (see seals_for_ethereal),
    if this option is enabled, Cortex Center will skip ahead to the state where you can enter her boss fight,
    instead of the long platforming sequence you normally do first.

    This is a .yaml/generation option because it has a small effect on logic: The platforming sequence logically
    requires Tai-Chi Kick, so skipping it allows the Lady Ethereal fight to be in-logic with only Air Dash."""
    display_name = "Skip Soulscape Platforming"


class RandomizeJadeCosts(Toggle):
    """Edit the cost of every jade in this slot to a randomly chosen number between jade_cost_min and jade_cost_max.

    This includes jades which are not Archipelago items.

    As a reminder: you start the game with 2 units of computing power, and there are 8 Computing Unit items to find,
    for a maximum power of 10."""
    display_name = "Randomize Jade Costs"


class JadeCostMin(Range):
    """The minimum possible jade cost. Has no effect if randomize_jade_costs is false."""
    display_name = "Jade Cost Minimum"
    range_start = 0
    range_end = 10
    default = 1


class JadeCostMax(Range):
    """The maximum possible jade cost. Has no effect if randomize_jade_costs is false."""
    display_name = "Jade Cost Maximum"
    range_start = 0
    range_end = 10
    default = 3


class JadeCostPlando(OptionDict):
    """Manually specify the cost of certain jades. For example: { "Stasis Jade": 0, "Steely Jade": 10 }

    The costs may be any integer from 0 to 10, even if jade_cost_min and jade_cost_max are set to a narrower range."""
    schema = Schema({
        Optional(jade_item_name): And(int, lambda n: n >= 0, lambda n: n <= 10)
        for jade_item_name in jade_items
    })
    display_name = "Jade Cost Plando"
    default = {}


class LogicDifficulty(Choice):
    """
    `vanilla` is exactly what it sounds like: You will only be expected to do what the vanilla game required.

    `medium` adds tricks that are easy to execute, once you're aware of them, but may require more effort to notice,
    set up and/or retry after failure. Specifically:
    - "Pseudo Air Dashes" using either a talisman ("T-dash") or Charged Strike ("CS-dash")
    - Using a Cloud Piercer S (or X) arrow to break Charged Strike barriers without Charged Strike
    - Using a Thunder Buster arrow (any level) to break one-way barriers from the "wrong" side
    - "Bow Hover": Press and hold jump, shoot the bow immediately (during the first half of Yi's upward movement) with
    any arrow equipped, and then simply never let go of the jump button until you're done hovering.
    - Using the Swift Runner skill to jump with extra horizontal momentum

    `ledge_storage` adds the following LS-related glitches to logic:
        - slash vault (also called LS "getup") or parry vault (also called LS "vault")
        - parry float/hover
        - moon slash wall slide
    These are harder to explain, so if you would like to learn them, check out the Ledge Storage section of
    Herdingoats' Nine Sols trick video: https://youtu.be/X9aii18KecU?t=766
    To avoid the complications of skill logic, setting up ledge storage with a skull kick is out of logic. Logic will
    assume you're doing the setup with either a Talisman dash, Air Dash, or Cloud Leap.

    Other speedrun tech like respawn manipulation, low gravity, rope storage, invulnerability abuse, dashing
    between lasers, and combinations thereof like fast Sky Tower climb and miner skip are simply out of logic.
    No logic level will expect you to carry transient resources (azure sand, qi charges, ledge storage)
    between areas, or increase your capacity beyond the initial 2 sand and 1 qi.
    Parrying a flying enemy attack to reset platforming moves is only in logic at the one place in TRC
    where the vanilla game gives you a respawning enemy for this specific purpose.
    """
    display_name = "Logic Difficulty"
    option_vanilla = 0
    option_medium = 1
    option_ledge_storage = 2
    default = 0


class FirstRootNode(Choice):
    """
    The first root node you can teleport to from Four Seasons Pavilion after starting a randomized game.
    This is often referred to as your "spawn", although you technically always spawn in FSP.

    Many root nodes are intentionally excluded from this list, usually because if you started there
    no locations would be checkable at the start of the game when you have no items yet.

    Some first_root_nodes will force items to be placed early, since the randomizer would be unbeatable otherwise:
    - galactic_dock early-places one of Nymph or Tai-Chi Kick
    - central_transport_hub early-places Tai-Chi Kick
    - factory_underground early-places one of Air Dash or Cloud Leap
    - inner_warehouse early-places Wall Climb and one of Cloud Leap, Air Dash or Ledge Grab
    - power_reservoir_west early-places one of Cloud Leap, Air Dash or Tai-Chi Kick
    See the descriptions of shuffle_grapple, shuffle_wall_climb and shuffle_ledge_grab for additional cases.
    """
    display_name = "First Root Node"
    default = 0
    option_agrarian_hall = 1
    option_apeman_facility_depths = 2
    option_apeman_facility_monitoring = 0  # default
    option_central_transport_hub = 3
    option_factory_great_hall = 4
    option_factory_underground = 5
    option_galactic_dock = 6
    option_outer_warehouse = 7
    option_grotto_of_scriptures_entry = 8
    option_grotto_of_scriptures_east = 9
    option_grotto_of_scriptures_west = 10
    option_inner_warehouse = 11
    option_lake_yaochi_ruins = 12
    option_power_reservoir_east = 13
    option_power_reservoir_west = 14
    option_radiant_pagoda = 15
    option_yinglong_canal = 16


class ShuffleGrapple(Toggle):
    """Takes away Yi's grapple hook and zipline sliding abilities until you collect the 'Grapple' item.

    If your first_root_node is yinglong_canal, then Grapple will be placed early."""
    display_name = "Shuffle Grapple"


class ShuffleWallClimb(Toggle):
    """Takes away Yi's ability to climb glowing green walls until you collect the 'Wall Climb' item.

    If your first_root_node is apeman_facility_monitoring, then Wall Climb will be placed early."""
    display_name = "Shuffle Wall Climb"


class ShuffleLedgeGrab(Toggle):
    """Takes away Yi's ability to grab onto ledges and pull himself up until you collect the 'Ledge Grab' item.

    If your first_root_node is yinglong_canal, then Ledge Grab will be placed early.

    This is more impactful than it might sound because of 'ledge storage' glitches. See logic_difficulty."""
    display_name = "Shuffle Ledge Grab"


class ShopUnlocks(Choice):
    """
    The condition for unlocking the three shops in Four Seasons Pavilion. That is: Kuafu's shop, Chiyou's shop,
    and Kuafu's extra inventory (visiting Chiyou outside FSP is considered out of logic)

    - vanilla_like_locations means the shops are unlocked by checking AP locations that try to resemble the vanilla
    game's unlock conditions (to the extent feasible in a randomizer).
    In other words: Kuafu's shop is unlocked when you check the "Kuafu's Vital Sanctum" location,
    Chiyou's shop is unlocked when you check the "Factory (GH): Raise the Bridge for Chiyou" location,
    and Kuafu's extra inventory is unlocked at the same time as Chiyou's shop.
    The main change from vanilla is unlocking Chiyou with the bridge location instead of the Prison escape sequence,
    because forcing you to do the entire escape (up to Factory (Underground)) would be far too linear for a randomizer.

    - sol_seals will unlock each shop after a certain number of Sol Seal items have been collected.
    See kuafu_shop_unlock_sol_seals, chiyou_shop_unlock_sol_seals and kuafu_extra_inventory_unlock_sol_seals.

    - unlock_items will add 3 "Progressive Shop Unlock" items to this slot, and unlock the 3 shops as they're found.
    Since these are AP items, you can add them to start_inventory, local_items, and other generic options.
    """
    display_name = "Shop Unlocks"
    default = 0
    option_vanilla_like_locations = 0
    option_sol_seals = 1
    option_unlock_items = 2


class KuafuShopUnlockSolSeals(Range):
    """The number of Sol Seals needed to unlock Kuafu's shop in Four Seasons Pavilion.
    Has no effect unless shop_unlocks is set to sol_seals."""
    display_name = "Kuafu Shop Unlock Sol Seals"
    range_start = 0
    range_end = 8
    default = 1


class ChiyouShopUnlockSolSeals(Range):
    """The number of Sol Seals needed to unlock Chiyou's shop in Four Seasons Pavilion.
    Has no effect unless shop_unlocks is set to sol_seals."""
    display_name = "Chiyou Shop Unlock Sol Seals"
    range_start = 0
    range_end = 8
    default = 3


class KuafuExtraInventoryUnlockSolSeals(Range):
    """The number of Sol Seals needed to unlock Kuafu's extra inventory in Four Seasons Pavilion.
    Has no effect unless shop_unlocks is set to sol_seals."""
    display_name = "Kuafu Extra Inventory Unlock Sol Seals"
    range_start = 0
    range_end = 8
    default = 5


class PreventAnnoyingRunbacks(DefaultOnToggle):
    """If the path to a boss or other difficult arena fight has a shortcut requiring items to open,
    this option makes those items logically required for the fight.
    This prevents the randomizer from potentially forcing you to attempt these fights while they have
    annoyingly long runbacks because you can't open the shortcuts yet.

	Two fights are currently affected by this option:
	- Ji's boss fight and the 3 locations behind it will logically require Mystic Nymph: Scout Mode,
	because nymph can open the shortcut from Grotto (West)'s root node to his boss arena
	- The location "Central Hall: Turrets and Double Axe Robot Room" will logically require Mystic Nymph: Scout Mode,
	because nymph can open the door to the left side of Central Hall
    """


class PreventWeakenedPrisonState(Toggle):
    """After you 'fight' Jiequan in Factory (Great Hall) and get sent to Prison, if this option is enabled,
    Yi will *not* be weakened the way he is in the vanilla game. You'll still be expected to do Prison,
    but this should solve what many players find annoying about it.

    This is a .yaml/generation option because it changes the logic for unlocking Prison."""


# actual Option Groups are specified in the WebWorld in __init__.py for some reason
@dataclass
class NineSolsGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool

    # General Progression
    shuffle_sol_seals: ShuffleSolSeals
    seals_for_eigong: SealsForEigong
    seals_for_prison: SealsForPrison
    prevent_weakened_prison_state: PreventWeakenedPrisonState
    seals_for_ethereal: SealsForEthereal
    skip_soulscape_platforming: SkipSoulscapePlatforming
    prevent_annoying_runbacks: PreventAnnoyingRunbacks

    # Jade Costs
    randomize_jade_costs: RandomizeJadeCosts
    jade_cost_min: JadeCostMin
    jade_cost_max: JadeCostMax
    jade_cost_plando: JadeCostPlando

    # Shop Unlocks
    shop_unlocks: ShopUnlocks
    kuafu_shop_unlock_sol_seals: KuafuShopUnlockSolSeals
    chiyou_shop_unlock_sol_seals: ChiyouShopUnlockSolSeals
    kuafu_extra_inventory_unlock_sol_seals: KuafuExtraInventoryUnlockSolSeals

    # Additional Randomizations
    first_root_node: FirstRootNode
    shuffle_grapple: ShuffleGrapple
    shuffle_wall_climb: ShuffleWallClimb
    shuffle_ledge_grab: ShuffleLedgeGrab
    # skill_tree_randomization
    # shop_randomization
    logic_difficulty: LogicDifficulty
    # entrance_randomization
