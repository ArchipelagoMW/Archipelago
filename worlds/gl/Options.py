from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool, Toggle, Range, DeathLinkMixin, DefaultOnToggle, \
    OptionSet


class IncludedAreas(OptionSet):
    """
    Select which areas will have their locations included in the randomization pool.
    Each selected area's stages and checks will be accessible in your world.
    Unselected areas will not be included in the location pool.
    Mountain is always available and cannot be excluded.
    """
    display_name = "Included Areas"
    valid_keys = ["Castle", "Town", "Ice", "Battlefield"]
    default = ["Castle", "Town", "Ice", "Battlefield"]


class ChestBarrels(Choice):
    """
    Choose how you want Chests and Barrels to be randomized.
    None: Neither Chests nor Barrels will be added as locations.
    All Chests: Chests will be added as locations, Barrels will not.
    All Barrels: Barrels will be added as locations, Chests will not.
    All Both: Both Chests and Barrels will be added as locations.
    """
    display_name = "Chests and Barrels"
    option_none = 0
    option_all_chests = 1
    option_all_barrels = 2
    option_all_both = 3
    default = 3


class Obelisks(DefaultOnToggle):
    """
    Obelisks will be added to the random pool as items.
    Activating all of the obelisks in an area will unlock access to the next.
    Disabling this will lock obelisks in their original locations.
    """

    display_name = "Obelisks"


class MirrorShards(DefaultOnToggle):
    """
    Mirror Shards will be added to the random pool as items.
    Collecting all four mirror shards will unlock access to the Desecrated Temple.
    Disabling this will lock mirror shards in their original locations.
    """

    display_name = "Mirror Shards"


class Portals(DefaultOnToggle):
    """
    Level portals will be added to the random pool as items.
    Getting a portal item will unlock access to that level.
    Levels will no longer unlock in succession when clearing the previous level.
    """
    display_name = "Portals"


class Goal(Choice):
    """
    Choose your objective required to goal.
    Defeat Skorne: Collect all 13 stones to unlock and defeat Skorne in the Underworld.
    Defeat X Bosses: Defeat X number of bosses to goal.
    """

    display_name = "Goal"
    option_defeat_skorne = 1
    option_defeat_x_bosses =2
    default = 1


class BossGoalCount(Range):
    """
    Choose how many bosses you must defeat to goal if 'Defeat X Bosses' is selected as your goal.
    This includes both Temple and Underworld Skorne.
    """

    display_name = "Boss Goal Count"
    range_start = 1
    range_end = 6
    default = 6


class MaxDifficulty(Range):
    """
    Select the difficulty value you want to be the maximum.
    This will affect the ammount of checks in each level as well as enemy strength and number of spawners.

    """

    display_name = "Max Difficulty Value"
    range_start = 1
    range_end = 4
    default = 4


class InstantMaxDifficulty(Toggle):
    """
    All stages will load with their max difficulty on the first run through.
    By default, stages increase in difficulty by 1 at a set interval that changes per zone.
    The starting level for each zone increases gradually as you would progress in vanilla.
    """

    display_name = "Instant Max Difficulty"


class PermaSpeed(Toggle):
    """
    You will be given speed boots with a permanent duration.
    """

    display_name = "Permanent Speed Boots"


class InfiniteKeys(Toggle):
    """
    You will be given an absurd amount of keys.
    """

    display_name = "Infinite Keys"


class IncludedTraps(OptionSet):
    """
    Choose what traps will be put in the item pool.
    Valid Keys: Death, Poison Fruit, Crossbow Shooter, Bomb Thrower, Bomb Runner, Golem
    """

    display_name = "Included Traps"
    valid_keys = ["Death", "Poison Fruit", "Crossbow Shooter", "Bomb Thrower", "Bomb Runner", "Golem"]
    default = ["Death", "Poison Fruit", "Crossbow Shooter", "Bomb Thrower", "Bomb Runner", "Golem"]


class TrapsFrequency(Range):
    """
    Choose the frequency of traps added into the item pool
    This range is a percentage of all items in the pool that will be traps.
    """

    display_name = "Trap Frequency"
    range_start = 1
    range_end = 75
    default = 10


class LocalFillerFrequency(Range):
    """
    Choose the frequency of filler items that will be placed locally in your world.
    This range is a percentage of how many filler items will be locally placed before generation occurs.
    """

    display_name = "Local Filler Frequency"
    range_start = 0
    range_end = 75
    default = 50


class UnlockCharacterOne(Choice):
    """
    Unlock a secret character for Player 1 from the start.
    None: No secret characters will be unlocked.
    Chosen Character: The selected character will be available from a new save.
    """

    option_none = 0
    option_minotaur = 1
    option_falconess = 2
    option_tigress = 3
    option_jackal = 4
    option_sumner = 5
    default = 0


class UnlockCharacterTwo(Choice):
    """
    Unlock a secret character for Player 2 from the start.
    None: No secret characters will be unlocked.
    Chosen Character: The selected character will be available from a new save.
    """

    option_none = 0
    option_minotaur = 1
    option_falconess = 2
    option_tigress = 3
    option_jackal = 4
    option_sumner = 5
    default = 0


class UnlockCharacterThree(Choice):
    """
    Unlock a secret character for Player 3 from the start.
    None: No secret characters will be unlocked.
    Chosen Character: The selected character will be available from a new save.
    """

    option_none = 0
    option_minotaur = 1
    option_falconess = 2
    option_tigress = 3
    option_jackal = 4
    option_sumner = 5
    default = 0


class UnlockCharacterFour(Choice):
    """
    Unlock a secret character for Player 4 from the start.
    None: No secret characters will be unlocked.
    Chosen Character: The selected character will be available from a new save.
    """

    option_none = 0
    option_minotaur = 1
    option_falconess = 2
    option_tigress = 3
    option_jackal = 4
    option_sumner = 5
    default = 0


@dataclass
class GLOptions(DeathLinkMixin, PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    included_areas: IncludedAreas
    chests_barrels: ChestBarrels
    obelisks: Obelisks
    mirror_shards: MirrorShards
    portals: Portals
    goal: Goal
    boss_goal_count: BossGoalCount
    max_difficulty: MaxDifficulty
    instant_max: InstantMaxDifficulty
    infinite_keys: InfiniteKeys
    permanent_speed: PermaSpeed
    included_traps: IncludedTraps
    traps_frequency: TrapsFrequency
    local_filler_frequency: LocalFillerFrequency
    unlock_character_one: UnlockCharacterOne
    unlock_character_two: UnlockCharacterTwo
    unlock_character_three: UnlockCharacterThree
    unlock_character_four: UnlockCharacterFour
