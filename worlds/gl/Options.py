from Options import StartInventoryPool, PerGameCommonOptions, Choice
from dataclasses import dataclass

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


@dataclass
class GLOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    chests_barrels: ChestBarrels
    obelisks: Obelisks
    mirror_shards: MirrorShards
