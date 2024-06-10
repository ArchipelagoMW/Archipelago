from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool, Toggle, Range


class ChestBarrels(Choice):
    """
    Choose how you want Chests and Barrels to be randomized.
    None: Neither Chests nor Barrels will be added as locations.
    All Chests: Chests will be added as locations, Barrels will not.
    All Barrels: Barrels will be added as locations, Chests will not.
    All Both: Both Chests and Barrels will be added as locations.
    """

    option_none = 0
    option_all_chests = 1
    option_all_barrels = 2
    option_all_both = 3
    default = 3


class Obelisks(Choice):
    """
    Choose how you want Obelisks to be randomized.
    None: Obelisks will be placed in their own locations.
    All Obelisks: Obelisks will be shuffled into the item pool.
    """

    option_none = 0
    option_all_obelisks = 1
    default = 1


class MirrorShards(Choice):
    """
    Choose how you want Mirror Shards to be randomized.
    None: Mirror Shards will be placed in their own locations.
    All Shards: Mirror Shards will be shuffled into the item pool.
    """

    option_none = 0
    option_all_shards = 1
    default = 1


class MaxDifficultyToggle(Toggle):
    """
    Set all stages to have a maximum difficulty.
    All locations with a difficulty higher than what is set will be excluded from the pool of locations.
    Default max difficulty is 4.
    """

    display_name = "Change Max Difficulty"


class MaxDifficultyRange(Range):
    """
    Select the difficulty value you want to be the maximum.
    This does nothing if Change Max Difficulty is set to false.
    """

    display_name = "Max Difficulty Value"
    range_start = 1
    range_end = 4
    default = 4


class InstantMaxDifficulty(Toggle):
    """
    All stages will load with their max difficulty on the first run through.
    By default, stages increase in difficulty by 1 every 5 player levels.
    The starting level for each area increases gradually as you would progress in vanilla.
    """

    display_name = "Change Max Difficulty"


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


class UnlockCharacter(Choice):
    """
    Unlock a secret character from the start.
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
class GLOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    chests_barrels: ChestBarrels
    obelisks: Obelisks
    mirror_shards: MirrorShards
    max_difficulty_toggle: MaxDifficultyToggle
    max_difficulty_value: MaxDifficultyRange
    instant_max: InstantMaxDifficulty
    unlock_character: UnlockCharacter
    infinite_keys: InfiniteKeys
    permanent_speed: PermaSpeed
