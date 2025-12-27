from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool, Toggle, Range, DeathLinkMixin, DefaultOnToggle, \
    OptionSet


class PlayerCount(Range):
    """
    Select how many players will be playing this world locally.
    If 3 players will be active then change this to 3, etc.
    """

    display_name = "Local Players"
    range_start = 1
    range_end = 4
    default = 1


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
    Choose how you want Obelisks to be randomized.
    None: Obelisks will be placed in their own locations.
    All Obelisks: Obelisks will be shuffled into the item pool.
    """

    display_name = "Obelisks"


class MirrorShards(DefaultOnToggle):
    """
    Choose how you want Mirror Shards to be randomized.
    None: Mirror Shards will be placed in their own locations.
    All Shards: Mirror Shards will be shuffled into the item pool.
    """

    display_name = "Mirror Shards"

class Portals(DefaultOnToggle):
    """
    Level portals will be added to the random pool as items.
    Getting a portal item will unlock access to that level.
    Levels will no longer unlock in succession when clearing the previous level.
    """
    display_name = "Portals"


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
    This value has a minimum based on how many local players you have.
    If you have 3 local players, this will be adjusted to be at least 3.
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


class TrapsChoice(Choice):
    """
    Choose what traps will be put in the item pool.
    All Active: Both Death and Poison Fruit will be added to the item pool.
    Only Death: Death will be added to the item pool.
    Only Fruit: Poison Fruit will be added to the item pool.
    None Active: No Traps will be added to the item pool.
    """

    display_name = "Active Traps"
    option_all_active = 0
    option_only_death = 1
    option_only_fruit = 2
    option_none_active = 3
    default = 0


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
    local_players: PlayerCount
    included_areas: IncludedAreas
    chests_barrels: ChestBarrels
    obelisks: Obelisks
    mirror_shards: MirrorShards
    portals: Portals
    max_difficulty_toggle: MaxDifficultyToggle
    max_difficulty_value: MaxDifficultyRange
    instant_max: InstantMaxDifficulty
    infinite_keys: InfiniteKeys
    permanent_speed: PermaSpeed
    traps_choice: TrapsChoice
    traps_frequency: TrapsFrequency
    local_filler_frequency: LocalFillerFrequency
    unlock_character_one: UnlockCharacterOne
    unlock_character_two: UnlockCharacterTwo
    unlock_character_three: UnlockCharacterThree
    unlock_character_four: UnlockCharacterFour
