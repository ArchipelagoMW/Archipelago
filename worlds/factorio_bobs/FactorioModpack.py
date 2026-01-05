import json
from functools import cached_property
from pathlib import Path

from . import APModpackManager

MAX_LOCATIONS_PER_SCIENCE_PACK = 999

class FactorioModpack(APModpackManager.BaseModpack):

    def __init__(self, packPath: Path):
        super().__init__(packPath)

        self.__useless_technologies: set[str] | None = None

        self.location_pools: list[list[str]] | None = None

    def init_items(self):
        self._add_item("Attack Trap")
        self._add_item("Evolution Trap")
        self._add_item("Teleport Trap")
        self._add_item("Evolution Trap")
        self._add_item("Cluster Grenade Trap")
        self._add_item("Artillery Trap")
        self._add_item("Atomic Rocket Trap")
        self._add_item("Atomic Cliff Remover Trap")
        self._add_item("Inventory Spill Trap")

        for technology_name in self.all_technologies.keys():
            self._add_item(technology_name)

    def init_locations(self):
        for complexity in range(1, len(self.ordered_science_packs)+1):
            pool = [f"AP-{complexity}-{i}" for i in range(1, MAX_LOCATIONS_PER_SCIENCE_PACK + 1)]
            for location in pool:
                self._add_location(location)
            self.location_pools.append(pool)

    def consistency_checks(self) -> bool:


    @cached_property
    def ordered_science_packs(self) -> list[str]:
        with self.open_file("sciencePacks.json") as file:
            packs = json.load(file)["sciencePacks"]
        return packs
