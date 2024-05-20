from Options import StartInventoryPool, PerGameCommonOptions, Choice, Toggle
from dataclasses import dataclass


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
    Choose how you want Obelisks to be randomized.
    None: Mirror Shards will be placed in their own locations.
    All Shards: Mirror Shards will be shuffled into the item pool.
    """
    option_none = 0
    option_all_shards = 1
    default = 1


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
    infinite_keys: InfiniteKeys
    permanent_speed: PermaSpeed
    chests_barrels: ChestBarrels
    obelisks: Obelisks
    mirror_shards: MirrorShards
    unlock_character: UnlockCharacter
