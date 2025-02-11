from dataclasses import dataclass

from Options import PerGameCommonOptions, StartInventoryPool, DeathLink


@dataclass
class NineSolsGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

