from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    PerGameCommonOptions,
    Range,
    Toggle,
    Visibility,
)


class Goal(Choice):
    """
    Pick a Goal to finish the game.
    Hell Castle is the usual finish of the game, being the last stage to beat.
    Volcano and Mountaintop are boss rush stages and are therefore regarded has more difficult stages than Hell Castle.
    """

    display_name = "Goal"
    option_hell_castle = 0
    option_volcano = 1
    option_mountaintop = 2
    option_hell_castle_and_volcano = 3
    option_hell_castle_and_mountaintop = 4
    option_volcano_and_mountaintop = 5
    option_all = 6
    default = 0


class RangerClassRandomizer(Toggle):
    """
    When enabled, start with the Class selected in Class Selector, and unlock other Classes via checks.
    This also starts you off with the Forget Tree, to switch Classes, and Forget is free.
    """

    display_name = "Class Randomizer"


class RangerClassSelector(Choice):
    """
    Selects the Class you start with when Class Randomizer is enabled.
    """

    display_name = "Class Selector"
    option_boxer = "Boxer"
    option_gladiator = "Gladiator"
    option_sniper = "Sniper"
    option_magician = "Magician"
    option_priest = "Priest"
    option_gunner = "Gunner"
    option_whipper = "Whipper"
    option_angel = "Angel"
    default = "random"


class CastleClassUnlocks(Range):
    """
    Minimum number of additional Ranger Classes you must unlock before entering the Castle stage.
    Applies only when Class Randomizer is enabled (your starting class is not counted here).
    """

    display_name = "Classes required for Castle"
    range_start = 0
    range_end = 7
    default = 2


class SubmarineShrineClassUnlocks(Range):
    """
    Minimum number of additional Ranger Classes you must unlock before entering the Submarine Shrine stage.
    Applies only when Class Randomizer is enabled (your starting class is not counted here).
    """

    display_name = "Classes required for Submarine Shrine"
    range_start = 0
    range_end = 7
    default = 3


class PyramidClassUnlocks(Range):
    """
    Minimum number of additional Ranger Classes you must unlock before entering the Pyramid stage.
    Applies only when Class Randomizer is enabled (your starting class is not counted here).
    """

    display_name = "Classes required for Pyramid"
    range_start = 0
    range_end = 7
    default = 4


class IceCastleClassUnlocks(Range):
    """
    Minimum number of additional Ranger Classes you must unlock before entering the Ice Castle stage.
    Applies only when Class Randomizer is enabled (your starting class is not counted here).
    """

    display_name = "Classes required for Ice Castle"
    range_start = 0
    range_end = 7
    default = 5


class HellCastleClassUnlocks(Range):
    """
    Minimum number of additional Ranger Classes you must unlock before entering the Hell Castle stage.
    Applies only when Class Randomizer is enabled (your starting class is not counted here).
    """

    display_name = "Classes required for Hell Castle"
    range_start = 0
    range_end = 7
    default = 6


class CastleMinimumStagesUnlocks(Range):
    """
    Minimum number of pre-Castle stages you must unlock before entering the Castle stage.
    Pre-Castle stages are: Grassland 1-7, Lake, Hill Country 1-3, Forest 1&2, Cavern 1-3 and Castle Gate.
    """

    display_name = "Minimum number of required pre-Castle stages"
    range_start = 0
    range_end = 17
    default = 6


class CastleMaximumStagesUnlocks(Range):
    """
    Maximum number of pre-Castle stages you must unlock before entering the Castle stage.
    Pre-Castle stages are: Grassland 1-7, Lake, Hill Country 1-3, Forest 1&2, Cavern 1-3 and Castle Gate.
    """

    display_name = "Maximum number of required pre-Castle stages"
    range_start = 0
    range_end = 17
    default = 10


class StagesReqForCastle(Range):
    """
    Actual number of required pre-Castle stages to beat.
    Only used for rules and tracking.
    """

    display_name = "Actual number of required pre-Castle stages"
    visibility = Visibility.none
    range_start = 0
    range_end = 17
    default = 6


class SubmarineShrineMinimumStagesUnlocks(Range):
    """
    Minimum number of pre-Submarine Shrine stages you must unlock before entering the Submarine Shrine stage.
    Pre-Submarine Shrine stages are: Seaside 1-4, Submarine 1-4, Mist Grove 1-3 and ???.
    """

    display_name = "Minimum number of required pre-Submarine Shrine stages"
    range_start = 0
    range_end = 12
    default = 4


class SubmarineShrineMaximumStagesUnlocks(Range):
    """
    Maximum number of pre-Submarine Shrine stages you must unlock before entering the Submarine Shrine stage.
    Pre-Submarine Shrine stages are: Seaside 1-4, Submarine 1-4, Mist Grove 1-3 and ???.
    """

    display_name = "Maximum number of required pre-Submarine Shrine stages"
    range_start = 0
    range_end = 12
    default = 7


class StagesReqForSubmarineShrine(Range):
    """
    Actual number of required pre-Submarine Shrine stages to beat.
    Only used for rules and tracking.
    """

    display_name = "Actual number of required pre-Submarine Shrine stages"
    visibility = Visibility.none
    range_start = 0
    range_end = 12
    default = 4


class PyramidMinimumStagesUnlocks(Range):
    """
    Minimum number of pre-Pyramid stages you must unlock before entering the Pyramid stage.
    Pre-Pyramid stages are: Desert 1-8, Oasis and Beach 1-3.
    """

    display_name = "Minimum number of required pre-Pyramid stages"
    range_start = 0
    range_end = 12
    default = 4


class PyramidMaximumStagesUnlocks(Range):
    """
    Maximum number of pre-Pyramid stages you must unlock before entering the Pyramid stage.
    Pre-Pyramid stages are: Desert 1-8, Oasis and Beach 1-3.
    """

    display_name = "Maximum number of required pre-Pyramid stages"
    range_start = 0
    range_end = 12
    default = 7


class StagesReqForPyramid(Range):
    """
    Actual number of required pre-Pyramid stages to beat.
    Only used for rules and tracking.
    """

    display_name = "Actual number of required pre-Pyramid stages"
    visibility = Visibility.none
    range_start = 0
    range_end = 12
    default = 4


class IceCastleMinimumStagesUnlocks(Range):
    """
    Minimum number of pre-Ice Castle stages you must unlock before entering the Ice Castle stage.
    Pre-Ice Castle stages are: Cavern 4-6, Snowfield 1-8, Mountain 1&2 and Frozen Lake.
    """

    display_name = "Minimum number of required pre-Ice Castle stages"
    range_start = 0
    range_end = 14
    default = 5


class IceCastleMaximumStagesUnlocks(Range):
    """
    Maximum number of pre-Ice Castle stages you must unlock before entering the Ice Castle stage.
    Pre-Ice Castle stages are: Cavern 4-6, Snowfield 1-8, Mountain 1&2 and Frozen Lake.
    """

    display_name = "Maximum number of required pre-Ice Castle stages"
    range_start = 0
    range_end = 14
    default = 8


class StagesReqForIceCastle(Range):
    """
    Actual number of required pre-Ice Castle stages to beat.
    Only used for rules and tracking.
    """

    display_name = "Actual number of required pre-Ice Castle stages"
    visibility = Visibility.none
    range_start = 0
    range_end = 14
    default = 5


class HellCastleMinimumStagesUnlocks(Range):
    """
    Minimum number of pre-Hell Castle stages you must unlock before entering the Hell Castle stage.
    Pre-Hell Castle stages are: Snowfield 9, Beach 4, Forest 3-6, !!!, Hell 1-8, Inferno 1-3, Blood Lake, Cavern 7&8 and Hell Gate.
    """

    display_name = "Minimum number of required pre-Hell Castle stages"
    range_start = 0
    range_end = 22
    default = 7


class HellCastleMaximumStagesUnlocks(Range):
    """
    Maximum number of pre-Hell Castle stages you must unlock before entering the Hell Castle stage.
    Pre-Hell Castle stages are: Snowfield 9, Beach 4, Forest 3-6, !!!, Hell 1-8, Inferno 1-3, Blood Lake, Cavern 7&8 and Hell Gate.
    """

    display_name = "Maximum number of required pre-Hell Castle stages"
    range_start = 0
    range_end = 22
    default = 12


class StagesReqForHellCastle(Range):
    """
    Actual number of required pre-Hell Castle stages to beat.
    Only used for rules and tracking.
    """

    display_name = "Actual number of required pre-HellCastle stages"
    visibility = Visibility.none
    range_start = 0
    range_end = 22
    default = 7


class ShuffleBooks(DefaultOnToggle):
    """
    Controls whether buying Books are checks.
    Either Shuffle Books or Shuffle Enemies needs to be turned on.
    """

    display_name = "Shuffle Books"


class ShuffleEnemies(Choice):
    """
    Controls whether enemies drop a check.
    Either Shuffle Enemies or Shuffle Books needs to be turned on.

    common enemies: Every non-boss enemy has a 5% chance to drop.
    boss enemies:   Every boss enemy has a 25% chance to drop.
    both:           Both settings are on.
    """

    display_name = "Shuffle Enemies"
    option_common_enemies = 1
    option_boss_enemies = 2
    option_both = 3
    option_off = 0
    default = 0


class GoldMultiplier(Choice):
    """Multiplies the gold dropped by enemies."""

    display_name = "Gold Multiplier"
    option_1x = 1
    option_2x = 2
    option_5x = 5
    option_10x = 10
    default = 1


class XPMultiplier(Choice):
    """Multiplies the XP gained per enemy killed."""

    display_name = "XP Multiplier"
    option_1x = 1
    option_2x = 2
    option_5x = 5
    option_10x = 10
    default = 1


class DropMultiplier(Choice):
    """Multiplies the chance of enemies dropping an item."""

    display_name = "Drop Multiplier"
    option_1x = 1
    option_2x = 2
    option_5x = 5
    option_10x = 10
    default = 1


class ShopHints(DefaultOnToggle):
    """When enabled, the Book shop will show you what you are buying and it will send out hints for buyable Books."""

    display_name = "Shop Hints"


class BookCostRandomizer(Choice):
    """
    Randomizes the costs of Books.

    vanilla:                  Costs are vanilla (1000*stage number).
    random_balanced:          Costs are randomized, but still balanced.
    random_extreme:           Costs can range between 1-99999.
    random_extreme_expensive: Costs can range between 1-999999. (Not recommended)
    """

    display_name = "Book Cost Randomizer"
    option_vanilla = 0
    option_random_balanced = 1
    option_random_extreme = 2
    option_random_extreme_expensive = 3
    default = 0


class Traps(Choice):
    """Configure if and how many Trap items there are, replacing filler items."""

    display_name = "Traps"
    option_none = 0
    option_some = 1
    option_half = 2
    option_most = 3
    option_all = 4
    default = 0


class RemoveNullCompo(DefaultOnToggle):
    """When enabled, buying weapons from the shop removes the 'cross' compo from the second compo slot"""

    display_name = "Remove Null Compo"


@dataclass
class SROptions(PerGameCommonOptions):
    goal: Goal
    ranger_class_randomizer: RangerClassRandomizer
    ranger_class_selected: RangerClassSelector
    classes_req_for_castle: CastleClassUnlocks
    classes_req_for_submarine_shrine: SubmarineShrineClassUnlocks
    classes_req_for_pyramid: PyramidClassUnlocks
    classes_req_for_ice_castle: IceCastleClassUnlocks
    classes_req_for_hell_castle: HellCastleClassUnlocks
    min_stages_req_for_castle: CastleMinimumStagesUnlocks
    max_stages_req_for_castle: CastleMaximumStagesUnlocks
    stages_req_for_castle: StagesReqForCastle
    min_stages_req_for_submarine_shrine: SubmarineShrineMinimumStagesUnlocks
    max_stages_req_for_submarine_shrine: SubmarineShrineMaximumStagesUnlocks
    stages_req_for_submarine_shrine: StagesReqForSubmarineShrine
    min_stages_req_for_pyramid: PyramidMinimumStagesUnlocks
    max_stages_req_for_pyramid: PyramidMaximumStagesUnlocks
    stages_req_for_pyramid: StagesReqForPyramid
    min_stages_req_for_ice_castle: IceCastleMinimumStagesUnlocks
    max_stages_req_for_ice_castle: IceCastleMaximumStagesUnlocks
    stages_req_for_ice_castle: StagesReqForIceCastle
    min_stages_req_for_hell_castle: HellCastleMinimumStagesUnlocks
    max_stages_req_for_hell_castle: HellCastleMaximumStagesUnlocks
    stages_req_for_hell_castle: StagesReqForHellCastle
    shuffle_books: ShuffleBooks
    shuffle_enemies: ShuffleEnemies
    gold_multiplier: GoldMultiplier
    xp_multiplier: XPMultiplier
    drop_multiplier: DropMultiplier
    shop_hints: ShopHints
    randomize_book_costs: BookCostRandomizer
    traps: Traps
    remove_null_compo: RemoveNullCompo
    death_link: DeathLink
