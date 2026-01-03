import json
from functools import cached_property
from pathlib import Path

from . import APModpackManager, Technology

MAX_LOCATIONS_PER_SCIENCE_PACK = 999

class FactorioModpack(APModpackManager.BaseModpack):

    def __init__(self, packPath: Path):
        super().__init__(packPath)

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

    @cached_property
    def base_technologies(self) -> dict[str, Technology]:
        with self.open_file("techs.json") as file:
            raw_techs = json.load(file)
        technologies: dict[str, Technology] = {}
        for technology_name, data in raw_techs.items():
            technologies[technology_name] = Technology(
                technology_name,
                modifiers=data.get("modifiers", []),
                unlocks=set(data["unlocks"])
            )
        return technologies

    @cached_property
    def progressive_technologies(self) -> dict[str, Technology]:
        # todo progressive_technologies
        return {}

    @cached_property
    def custom_technologies(self) -> dict[str, Technology]:
        # todo custom_technologies
        return {}

    @cached_property
    def all_technologies(self) -> dict[str, Technology]:
        """includes normal and progressive and custom technologies"""
        all_techs = {}
        all_techs.update(self.base_technologies)
        all_techs.update(self.progressive_technologies)
        all_techs.update(self.custom_technologies)
        return all_techs

    @cached_property
    def ordered_science_packs(self) -> list[str]:
        with self.open_file("sciencePacks.json") as file:
            packs = json.load(file)["sciencePacks"]
        return packs


APModpackManager.modpackType = FactorioModpack
APModpackManager.init_modpacks()