import json
from functools import cached_property
from pathlib import Path
from typing import FrozenSet

import Utils
from . import APModpackManager, Technology
from .InternalItem import RecipeEngine

MAX_LOCATIONS_PER_SCIENCE_PACK = 999

class FactorioModpack(APModpackManager.BaseModpack):

    def __init__(self, packPath: Path):
        super().__init__(packPath)

        self.__technology_table: dict[str, Technology] | None = None
        self.__base_technology_table: dict[str, Technology] | None = None
        self.__progressive_technology_table: dict[str, Technology] | None = None
        self.__tech_to_progressive_lookup: dict[str, str] | None = None
        self.__removed_technologies: set[str] | None = None
        self.__required_technologies: dict[str, FrozenSet[Technology]] | None = None

        self.__recipe_engine: RecipeEngine | None = None

        self.location_pools: list[list[str]] | None = None

    def _init_pack(self):
        self.recipe_engine.full_init()

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

        for technology_name, tech in self.technology_table.items():
            self._add_item(technology_name, groups={"Progressive"} if tech.progressive else None)

    def init_locations(self):
        for complexity in range(1, len(self.ordered_science_packs)+1):
            pool = [f"AP-{complexity}-{i}" for i in range(1, MAX_LOCATIONS_PER_SCIENCE_PACK + 1)]
            for location in pool:
                self._add_location(location, groups={f"AP-{complexity}"})
            self.location_pools.append(pool)

    def consistency_checks(self) -> None:
        is_consistent = True
        if any(recipe_name not in self.recipe_engine.recipes.keys() for recipe_name in self.start_unlocked_recipes):
            is_consistent = False
            self.logger.exception(f"Unknown Recipe defined. \n"
                                  f"Missing: {tuple(recipe_name for recipe_name in self.start_unlocked_recipes if recipe_name not in self.recipe_engine.recipes.keys())}")

        if not is_consistent:
            raise Exception(f"Modpack {self.packName} consistency check failed.")

    def __init_technologies(self) -> None:
        self.__technology_table: dict[str, Technology] = {}
        with self.open_file("techs.json") as file:
            raw_technologies = json.load(file)
        for technology_name, data in sorted(raw_technologies.items()):
            technology = Technology(
                technology_name,
                self,
                modifiers=data.get("modifiers", []),
                unlocks=set(data["unlocks"]) - self.start_unlocked_recipes,
            )
            self.__technology_table[technology_name] = technology

        self.__required_technologies: dict[str, FrozenSet[Technology]] = (
            Utils.KeyedDefaultDict(lambda ingredient_name:
                                   frozenset(self.recipe_engine.all_ingredients[ingredient_name].all_unlocking_technologies())))
        self.__required_technologies["water"] = frozenset()

        self.__base_technology_table = self.__technology_table.copy()
        self.__progressive_technology_table: dict[str, Technology] = {}

        self.__removed_technologies: set[str] = {tech_name for tech_name, tech in self.__base_technology_table.items()
                                                 if not tech.useful()}

        for root in self.progressive_rows:
            progressive = tuple(
                tech_name for tech_name in self.progressive_rows[root] if tech_name not in self.__removed_technologies)
            if not progressive:
                self.logger.error(f"Useless progressive skipping: {root}, {self.progressive_rows[root]}")
                continue
            assert all(tech in self.__technology_table for tech in progressive), \
                (f"Declared a progressive technology ({root}) without base technology. "
                 f"Missing: f{tuple(tech for tech in progressive if tech not in self.__technology_table)}")
            progressive_technology = Technology(root, self,
                                                tuple(progressive),
                                                modifiers=sorted(set.union(
                                                    *(set(self.__technology_table[tech].modifiers) for tech in progressive)
                                                )),
                                                unlocks=any(self.__technology_table[tech].unlocks for tech in progressive), )
            self.__progressive_technology_table[root] = progressive_technology

        self.__tech_to_progressive_lookup: dict[str, str] = {}
        for progressive in self.__progressive_technology_table.values():
            for technology in progressive.progressive:
                self.__tech_to_progressive_lookup[technology] = progressive.name

        self.__technology_table.update(self.__progressive_technology_table)

    @property
    def required_technologies(self) -> dict[str, FrozenSet[Technology]]:
        if self.__required_technologies is None:
            self.__init_technologies()
        return self.__required_technologies

    @property
    def technology_table(self) -> dict[str, Technology]:
        if self.__technology_table is None:
            self.__init_technologies()
        return self.__technology_table

    @property
    def base_technology_table(self) -> dict[str, Technology]:
        if self.__base_technology_table is None:
            self.__init_technologies()
        return self.__base_technology_table

    @property
    def progressive_technology_table(self) -> dict[str, Technology]:
        if self.__progressive_technology_table is None:
            self.__init_technologies()
        return self.__progressive_technology_table

    @property
    def tech_to_progressive_lookup(self) -> dict[str, str]:
        if self.__tech_to_progressive_lookup is None:
            self.__init_technologies()
        return self.__tech_to_progressive_lookup

    @property
    def removed_technologies(self) -> set[str]:
        if self.__removed_technologies is None:
            self.__init_technologies()
        return self.__removed_technologies

    @cached_property
    def start_unlocked_recipes(self) -> set[str]:
        with self.open_file("startingItems.json") as file:
            startingItems = json.load(file)
        return set(startingItems["recipes"])

    @property
    def free_sample_exclusions(self) -> set[str]:
        return set(self.ordered_science_packs) | {"rocket-part"}

    @cached_property
    def ordered_science_packs(self) -> list[str]:
        with self.open_file("sciencePacks.json") as file:
            packs = list(json.load(file))
        return packs

    @cached_property
    def progressive_rows(self) -> dict[str, tuple[str, ...]]:
        try:
            with self.open_file("progressive.json") as file:
                progressive_raw = json.load(file)
        except FileNotFoundError:
            return {}
        return {name: tuple(techs) for name, techs in progressive_raw.items()}

    @cached_property
    def force_useless_technologies(self) -> dict[str, bool]:
        try:
            with self.open_file("techOverride.json") as file:
                override_raw = json.load(file)
        except FileNotFoundError:
            return {}
        useless_overrides: dict[str, bool] = {}
        for tech_name, overrides in override_raw.items():
            if "useless" in overrides:
                useless_overrides[tech_name] = overrides["useless"]
        return useless_overrides

    @property
    def recipe_engine(self) -> RecipeEngine:
        if self.__recipe_engine is None:
            self.__recipe_engine = RecipeEngine(self)
        return self.__recipe_engine