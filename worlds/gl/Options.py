from Options import StartInventoryPool, PerGameCommonOptions
from dataclasses import dataclass


@dataclass
class GLOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
