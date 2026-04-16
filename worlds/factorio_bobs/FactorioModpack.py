import json
from functools import cached_property
from pathlib import Path
from typing import FrozenSet, Any

import Utils
from .RecipeEngine import RecipeEngine
from .Technologies import Technology
from .APModpackManager import BaseModpack

MAX_LOCATIONS_PER_SCIENCE_PACK = 999

external_directory_path = Path(Utils.user_path("factorio_mods", "packs"))
if not external_directory_path.exists():
    external_directory_path.mkdir(parents=True)
BaseModpack.modpack_directories.append((external_directory_path,[]))
player_directory_path = Path(Utils.user_path("Players"))
if player_directory_path.exists():
    BaseModpack.modpack_directories.append((player_directory_path,[]))

class FactorioModpack(BaseModpack):
    def __init__(self, packPath: Path, filesystems=None):
        super().__init__(packPath, filesystems)

        self.__technology_table: dict[str, Technology] | None = None
        self.__base_technology_table: dict[str, Technology] | None = None
        self.__progressive_technology_table: dict[str, Technology] | None = None
        self.__tech_to_progressive_lookup: dict[str, str] | None = None
        self.__removed_technologies: set[str] | None = None
        self.__required_technologies: dict[str, FrozenSet[Technology]] | None = None

        self.__recipe_engine: RecipeEngine | None = None

        self.__forced_locations: dict[str, int] | None = None

        self.location_pools: list[list[str]] | None = None

    def _init_pack(self):
        self.recipe_engine.full_init()

    def init_items(self):
        self._add_item("Attack Trap")
        self._add_item("Evolution Trap")
        self._add_item("Teleport Trap")
        self._add_item("Evolution Trap")
        self._add_item("Grenade Trap")
        self._add_item("Cluster Grenade Trap")
        self._add_item("Artillery Trap")
        self._add_item("Atomic Rocket Trap")
        self._add_item("Atomic Cliff Remover Trap")
        self._add_item("Inventory Spill Trap")

        for technology_name, tech in self.technology_table.items():
            self._add_item(technology_name, groups={"Progressive"} if tech.progressive else None)
        self.logger.debug(f"Loaded {len(self.items_to_id)} items")

    def init_locations(self):
        self.location_pools: list[list[str]] = []
        for complexity in range(1, len(self.ordered_science_packs)+1):
            pool = [f"AP-{complexity}-{i}" for i in range(1, MAX_LOCATIONS_PER_SCIENCE_PACK + 1)]
            for location in pool:
                self._add_location(location, groups={f"AP-{complexity}"})
            self.location_pools.append(pool)
        self.logger.debug(f"Loaded {len(self.locations_to_id)} locations")

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
        with self.open_file("Extractor/techs.json") as file:
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

    def __load_world_settings(self):
        with self.open_file("worldSettings.json") as file:
            raw_settings = json.load(file)
        self.__forced_locations: dict[str, int] = {}
        if "forced_locations" in raw_settings:
            for index, location in enumerate(raw_settings["forced_locations"]["start"], start=0):
                self.__forced_locations[location] = index
            for index, location in enumerate(raw_settings["forced_locations"]["end"], start=1):
                self.__forced_locations[location] = -index
            del raw_settings["forced_locations"]

        for key in raw_settings.keys():
            self.logger.error(f"Unknown key in worldSettings.json: {key}")


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
        try:
            with self.open_file("startingItems.json") as file:
                startingItems = json.load(file)
        except FileNotFoundError:
            return set()
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
            with self.open_file("techsOverride.json") as file:
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

    @cached_property
    def default_options(self):
        try:
            with self.open_file("defaultOptions.json") as file:
                default_raw = json.load(file)["default"]
        except FileNotFoundError:
            self.logger.debug("No default options file")
            return {"additional_logic": {}}
        defaults: dict[str, Any] = {"additional_logic": {}}
        if "additional_logic" in default_raw:
            raw_additional_logic = default_raw["additional_logic"]
            for complexity, rules in raw_additional_logic.items():
                match len(rules):
                    case 0:
                        break
                    case 1:
                        defaults["additional_logic"][int(complexity)] = rules[0]
                    case _:
                        defaults["additional_logic"][int(complexity)] = {"and": rules}
            del default_raw["additional_logic"]

        for key in default_raw.keys():
            self.logger.error(f"Unknown key in defaultOptions.json: {key}")
        return defaults

    @cached_property
    def mod_settings(self) -> dict[str, dict[str, Any]]:
        with self.open_file("Extractor/modSettings.json") as file:
            mod_settings_raw = json.load(file)
        return mod_settings_raw

    @property
    def forced_locations(self) -> dict[str, int]:
        if self.__forced_locations is None:
            self.__load_world_settings()
        return self.__forced_locations

    @cached_property
    def world_gen(self):
        world_gen: dict[str, None|int|dict] = {"autoplace_controls": {},
            "seed": None,
        "starting_area": 1,
        "peaceful_mode": False,
        "no_enemies_mode": False,
        "cliff_settings": {
            "name": "cliff",
            "cliff_elevation_0": 10,
            "cliff_elevation_interval": 40,
            "richness": 1
        },
        "property_expression_names": {
            "control-setting:moisture:bias": 0,
            "control-setting:moisture:frequency:multiplier": 1,
            "control-setting:aux:bias": 0,
            "control-setting:aux:frequency:multiplier": 1
        },
        "pollution": {
            "enabled": True,
            "diffusion_ratio": 0.02,
            "ageing": 1,
            "enemy_attack_pollution_consumption_modifier": 1,
            "min_pollution_to_damage_trees": 60,
            "pollution_restored_per_tree_damage": 10
        },
        "enemy_evolution": {
            "enabled": True,
            "time_factor": 40.0e-7,
            "destroy_factor": 200.0e-5,
            "pollution_factor": 9.0e-7
        },
        "enemy_expansion": {
            "enabled": True,
            "max_expansion_distance": 7,
            "settler_group_min_size": 5,
            "settler_group_max_size": 20,
            "min_expansion_cooldown": 14400,
            "max_expansion_cooldown": 216000
        }}
        with self.open_file("Extractor/autoplace.json") as file:
            autoplace_raw = json.load(file)

        for name, settings in autoplace_raw.items():
            if settings["category"] == "resource":
                world_gen["autoplace_controls"][name] = {"frequency": 1, "size": 3, "richness": 6}
            else:
                world_gen["autoplace_controls"][name] = {"frequency": 1, "size": 1, "richness": 1}

        advanced = {"pollution", "enemy_evolution", "enemy_expansion"}
        value = {
            "basic": {k: v for k, v in world_gen.items() if k not in advanced},
            "advanced": {k: v for k, v in world_gen.items() if k in advanced}
        }

        # verify min_values <= max_values
        def optional_min_lte_max(container, min_key, max_key):
            min_val = container.get(min_key, None)
            max_val = container.get(max_key, None)
            if min_val is not None and max_val is not None and min_val > max_val:
                raise ValueError(f"{min_key} can't be bigger than {max_key}")

        enemy_expansion = value["advanced"].get("enemy_expansion", {})
        optional_min_lte_max(enemy_expansion, "settler_group_min_size", "settler_group_max_size")
        optional_min_lte_max(enemy_expansion, "min_expansion_cooldown", "max_expansion_cooldown")
        return value