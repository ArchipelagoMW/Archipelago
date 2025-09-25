from dataclasses import dataclass
from Options import PerGameCommonOptions, StartInventoryPool


@dataclass
class CCCharlesOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
