from __future__ import annotations

import string
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Set, FrozenSet, Tuple, Union, List, Optional

import Utils
from . import FactorioOptions
from .FactorioUtils import FactorioElement, load_json_data
from .InternalItem import raw_recipes, Recipe, InternalItem, recipe_sources, mining_with_fluid_sources, \
    machine_per_category, all_ingredients, valid_ingredients, artifacts, invalid_ingredients

factorio_tech_id = factorio_base_id = 2 ** 17

pool = ThreadPoolExecutor(1)

all_science_packs: set[str] = set(FactorioOptions.MaxSciencePack.get_ordered_science_packs())

techs_future = pool.submit(load_json_data, "techs")

tech_table: Dict[str, int] = {}
technology_table: Dict[str, Technology] = {}

start_unlocked_recipes = {
    "bob-burner-lab",
    "copper-cable",
    "small-electric-pole",
    "bob-burner-generator",
    "pipe",
    "pipe-to-ground",
    "offshore-pump",
    "boiler",
    "bob-steam-inserter",
    "bob-steam-mining-drill",
    "bob-steam-assembling-machine",
    "bob-copper-pipe",
    "bob-copper-pipe-to-ground",
    "bob-stone-pipe",
    "bob-stone-pipe-to-ground",
    "stone-wall",
    "bob-basic-underground-belt",
    "bob-basic-splitter",
    "automation-science-pack",
}

assert all(recipe_name in raw_recipes for recipe_name in start_unlocked_recipes), ("Unknown Recipe defined.",
            f"Missing: f{tuple(recipe_name for recipe_name in start_unlocked_recipes if recipe_name not in raw_recipes)}")

def always(state) -> bool:
    return True

class Technology(FactorioElement):  # maybe make subclass of Location?
    factorio_id: int
    progressive: Tuple[str, ...]
    unlocks: Union[Set[str], bool]  # bool case is for progressive technologies
    modifiers: list[str]

    def __init__(self, technology_name: str, factorio_id: int, progressive: Tuple[str, ...] = (),
                 modifiers: list[str] = None, unlocks: Union[Set[str], bool] = None):
        self.name = technology_name
        self.factorio_id = factorio_id
        self.progressive = progressive
        if modifiers is None:
            modifiers = []
        self.modifiers =  modifiers
        if unlocks:
            self.unlocks = unlocks
        else:
            self.unlocks = set()

    def __hash__(self):
        return self.factorio_id

    @property
    def has_modifier(self) -> bool:
        return bool(self.modifiers)

    def get_custom(self, world, allowed_packs: Set[str], player: int) -> CustomTechnology:
        return CustomTechnology(self, world, allowed_packs, player)

    def useful(self) -> bool:
        return self.has_modifier or self.unlocks


class CustomTechnology(Technology):
    """A particularly configured Technology for a world."""
    ingredients: Set[str]

    def __init__(self, origin: Technology, world, allowed_packs: Set[str], player: int):
        ingredients = allowed_packs
        self.player = player
        if origin.name not in world.special_nodes:
            ingredients = set(world.random.sample(list(ingredients), world.random.randint(1, len(ingredients))))
        self.ingredients = ingredients
        super(CustomTechnology, self).__init__(origin.name, origin.factorio_id)

    def get_prior_technologies(self) -> Set[Technology]:
        """Get Technologies that have to precede this one to resolve tree connections."""
        technologies = set()
        for ingredient in self.ingredients:
            technologies |= required_technologies[ingredient]  # technologies that unlock the recipes
        return technologies


def unlock_just_tech(recipe: Recipe, _done) -> Set[Technology]:
    current_technologies = recipe.unlocking_technologies
    for ingredient in recipe.ingredients:
        current_technologies |= recursively_get_unlocking_technologies(ingredient, _done,
                                                                       unlock_func=unlock_just_tech)
    return current_technologies


def unlock(recipe: Recipe, _done) -> Set[Technology]:
    current_technologies = recipe.unlocking_technologies
    for ingredient in recipe.ingredients:
        current_technologies |= recursively_get_unlocking_technologies(ingredient, _done, unlock_func=unlock)
    current_technologies |= machine_per_category[recipe.category].all_unlocking_technologies()

    return current_technologies


def recursively_get_unlocking_technologies(ingredient: InternalItem, _done=None, unlock_func=unlock_just_tech) -> Set[
    Technology]:
    if _done:
        if ingredient in _done:
            return set()
        else:
            _done.add(ingredient)
    else:
        _done = {ingredient}
    if ingredient is None:
        return set()
    ingredient.get_raw_ingredients()
    recipe = ingredient.best_recipe
    if not recipe:
        return set()
    current_technologies = unlock_func(recipe, _done)

    return current_technologies

# recipes and technologies can share names in Factorio
for technology_name, data in sorted(techs_future.result().items()):
    technology = Technology(
        technology_name,
        factorio_tech_id,
        modifiers=data.get("modifiers", []),
        unlocks=set(data["unlocks"]) - start_unlocked_recipes,
    )
    factorio_tech_id += 1
    tech_table[technology_name] = technology.factorio_id
    technology_table[technology_name] = technology
    for recipe_name in technology.unlocks:
        recipe_sources.setdefault(recipe_name, set()).add(technology_name)
    if "mining-with-fluid" in technology.modifiers:
        mining_with_fluid_sources.add(technology_name)
del techs_future

# required_machine_technologies: Dict[str, FrozenSet[Technology]] = {}
# for name, machine in machines.items():
#     required_machine_technologies[name] = frozenset(recursively_get_unlocking_technologies(machine.item))
#
# logical_machines = {}
# machine_tech_cost = {}
# for machine in machines.values():
#     for category in machine.categories:
#         current_cost, current_machine = machine_tech_cost.get(category, (10000, "character"))
#         machine_cost = len(required_machine_technologies[machine.name])
#         if machine_cost < current_cost:
#             machine_tech_cost[category] = machine_cost, machine.name
#
# machine_per_category: Dict[str: Machine] = {}
# for category, (cost, machine_name) in machine_tech_cost.items():
#     machine_per_category[category] = machines[machine_name]
#
# del machine_tech_cost

# required technologies to be able to craft recipes from a certain category
# required_category_technologies: Dict[str, FrozenSet[FrozenSet[Technology]]] = {}
# for category_name, machine in machine_per_category.items():
#     techs = set()
#     techs |= machine.all_unlocking_technologies()
#     required_category_technologies[category_name] = frozenset(techs)

# required_technologies: Dict[str, FrozenSet[Technology]] = Utils.KeyedDefaultDict(lambda ingredient_name: frozenset(
#     recursively_get_unlocking_technologies(ingredient_name, unlock_func=unlock)))
required_technologies: Dict[str, FrozenSet[Technology]] = (
    Utils.KeyedDefaultDict(lambda ingredient_name:
                           frozenset(all_ingredients[ingredient_name].all_unlocking_technologies())))
required_technologies["water"] = frozenset()

free_sample_exclusions: Set[str] = all_science_packs | {"rocket-part"}

# progressive technologies
# auto-progressive
progressive_rows: Dict[str, Union[List[str], Tuple[str, ...]]] = {}
progressive_incs = set()
for tech_name in tech_table:
    if tech_name.endswith("-1"):
        progressive_rows[tech_name] = []
    elif tech_name[-2] == "-" and tech_name[-1] in string.digits:
        progressive_incs.add(tech_name)

for root, progressive in progressive_rows.items():
    seeking = root[:-1] + str(int(root[-1]) + 1)
    while seeking in progressive_incs:
        progressive.append(seeking)
        progressive_incs.remove(seeking)
        seeking = seeking[:-1] + str(int(seeking[-1]) + 1)

# make root entry the progressive name
for old_name in set(progressive_rows):
    prog_name = "progressive-" + old_name.rsplit("-", 1)[0]
    progressive_rows[prog_name] = tuple([old_name] + progressive_rows[old_name])
    del (progressive_rows[old_name])

# no -1 start
base_starts = set()
for remnant in progressive_incs:
    if remnant[-1] == "2":
        base_starts.add(remnant[:-2])

for root in base_starts:
    if root not in tech_table:
        root = root.replace("bob-", "")

    if root in tech_table:
        seeking = root + "-2"
        progressive = [root]
        while seeking in progressive_incs:
            progressive.append(seeking)
            progressive_incs.remove(seeking)
            seeking = seeking[:-1] + str(int(seeking[-1]) + 1)
        seeking = "bob-" + seeking
        while seeking in progressive_incs:
            progressive.append(seeking)
            progressive_incs.remove(seeking)
            seeking = seeking[:-1] + str(int(seeking[-1]) + 1)
        progressive_rows["progressive-" + root] = tuple(progressive)

# science packs
progressive_rows["progressive-science-pack"] = tuple(FactorioOptions.MaxSciencePack.get_ordered_science_packs())[1:]
progressive_rows["progressive-science-pack"] = (progressive_rows["progressive-science-pack"][:6]
                                                + ("bob-alien-research",)
                                                + progressive_rows["progressive-science-pack"][-1:])

# manual progressive
# progressive_rows["progressive-processing"] = (
#     "steel-processing",
#     "oil-processing", "sulfur-processing", "advanced-oil-processing", "coal-liquefaction",
#     "uranium-processing", "kovarex-enrichment-process", "nuclear-fuel-reprocessing")
progressive_rows["progressive-rocketry"] = ("rocketry", "explosive-rocketry", "atomic-bomb")
progressive_rows["progressive-car"] = ("automobilism", "tank", "bob-tanks-2", "bob-tanks-3")
# progressive_rows["progressive-fluid-handling"] = ("fluid-handling", "fluid-wagon")
# progressive_rows["progressive-train-network"] = ("railway", "automated-rail-transportation")
progressive_rows["progressive-engine"] = ("engine", "electric-engine")
progressive_rows["progressive-armor"] = ("heavy-armor", "modular-armor", "power-armor", "power-armor-mk2",
                                         "bob-power-armor-3", "bob-power-armor-4", "bob-power-armor-5")
progressive_rows["progressive-personal-battery"] = ("battery-equipment", "battery-mk2-equipment",
                                                    "bob-battery-equipment-3", "bob-battery-equipment-4",
                                                    "bob-battery-equipment-5", "bob-battery-equipment-6")
progressive_rows["progressive-energy-shield"] = ("energy-shield-equipment", "energy-shield-mk2-equipment",
                                                 "bob-energy-shield-equipment-3", "bob-energy-shield-equipment-4",
                                                 "bob-energy-shield-equipment-5", "bob-energy-shield-equipment-6")
progressive_rows["progressive-wall"] = ("stone-wall", "gate", "bob-reinforced-wall")
progressive_rows["progressive-follower"] = ("defender", "distractor", "destroyer", "bob-laser-robot")
# progressive_rows["progressive-turret"] = ("gun-turret", "laser-turret")
progressive_rows["progressive-flamethrower"] = ("flamethrower",)  # leaving out flammables, as they do nothing
del progressive_rows["progressive-bob-personal-roboport-modular-equipment"]
progressive_rows["progressive-personal-roboport-equipment"] = ("personal-roboport-equipment",
                                                               "bob-personal-roboport-modular-equipment-1",
                                                               "personal-roboport-mk2-equipment",
                                                               "bob-personal-roboport-modular-equipment-2",
                                                               "bob-personal-roboport-mk3-equipment",
                                                               "bob-personal-roboport-modular-equipment-3",
                                                               "bob-personal-roboport-mk4-equipment",
                                                               "bob-personal-roboport-modular-equipment-4",)
# bobs manual progressives
progressive_rows["progressive-logistics"] = ("logistics-0",) + progressive_rows["progressive-logistics"]

progressive_rows["progressive-artillery"] = ("artillery", "bob-artillery-turret-2", "bob-artillery-wagon-2",
                                             "bob-artillery-turret-3", "bob-artillery-wagon-3")
del progressive_rows["progressive-bob-steam-engine"]
progressive_rows["progressive-steam-power"] = ("steam-power", "bob-steam-engine-1", "bob-boiler-2",
                                               "bob-steam-engine-2", "bob-boiler-3", "bob-steam-engine-3",
                                               "bob-boiler-4", "bob-steam-engine-4", "bob-boiler-5",
                                               "bob-steam-engine-5")
progressive_rows["progressive-bob-centrifuge"] = ("bob-centrifuge-2", "bob-centrifuge-3")
progressive_rows["progressive-bob-distillery"] = ("bob-distillery-2", "bob-distillery-3", "bob-distillery-4",
                                                  "bob-distillery-5")
progressive_rows["progressive-bob-drills"] = ("bob-drills-2", "bob-drills-3", "bob-drills-4", "bob-drills-5")
del progressive_rows["progressive-electric-energy-distribution"]
progressive_rows["progressive-electric-pole"] = ("electric-energy-distribution-1",
                                                 "bob-electric-pole-2",
                                                 "bob-electric-pole-3",
                                                 "bob-electric-pole-4")
progressive_rows["progressive-substation"] = ("electric-energy-distribution-2",
                                              "bob-electric-substation-2",
                                              "bob-electric-substation-3",
                                              "bob-electric-substation-4")
progressive_rows["progressive-bob-electrolyser"] = ("bob-electrolyser-2", "bob-electrolyser-3", "bob-electrolyser-4",
                                                    "bob-electrolyser-5")
progressive_rows["progressive-turrets"] = ("gun-turret", "bob-turrets-2", "bob-turrets-3", "bob-turrets-4",
                                           "bob-turrets-5")
progressive_rows["progressive-laser-turrets"] = ("laser-turret", "bob-laser-turrets-2", "bob-laser-turrets-3",
                                                 "bob-laser-turrets-4", "bob-laser-turrets-5")
progressive_rows["progressive-pumpjacks"] = ("oil-gathering", "bob-pumpjacks-2", "bob-pumpjacks-3", "bob-pumpjacks-4")
progressive_rows["progressive-spidertron"] = ("bob-walking-vehicle", "bob-tankotron", "spidertron",
                                              "bob-logistic-spidertron", "bob-heavy-spidertron")
del progressive_rows["progressive-bulk-inserter"]
progressive_rows["progressive-inserter"] = ("fast-inserter", "bulk-inserter",
                                            "bob-express-inserter", "bob-bulk-inserter-2",
                                            "bob-turbo-inserter", "bob-bulk-inserter-3",
                                            "bob-ultimate-inserter", "bob-bulk-inserter-4")
del progressive_rows["progressive-bob-area-drills"]
del progressive_rows["progressive-bob-drills"]
progressive_rows["progressive-mining-drills"] = ("electric-mining-drill", "bob-area-drills-1",
                                                 "bob-drills-2", "bob-area-drills-2",
                                                 "bob-drills-3", "bob-area-drills-3",
                                                 "bob-drills-4", "bob-area-drills-4",
                                                 "bob-drills-5")
progressive_rows["progressive-circuits"] = ("electronics", "bob-electronics", "advanced-circuit", "processing-unit",
                                            "bob-advanced-processing-unit")
del progressive_rows["progressive-bob-long-inserters"]
del progressive_rows["progressive-bob-more-inserters"]
progressive_rows["progressive-bob-adjustable-inserters"] = ("bob-long-inserters-1", "bob-near-inserters",
                                                            "bob-more-inserters-1", "bob-long-inserters-2",
                                                            "bob-more-inserters-2")
del progressive_rows["progressive-advanced-material-processing"]
del progressive_rows["progressive-bob-multi-purpose-furnace"]
del progressive_rows["progressive-bob-chemical-processing"]
progressive_rows["progressive-furnaces"] = ("bob-alloy-processing", "bob-chemical-processing-1",
                                            "advanced-material-processing", "bob-steel-mixing-furnace",
                                            "bob-steel-chemical-furnace", "bob-fluid-mixing-furnace",
                                            "bob-fluid-chemical-furnace", "advanced-material-processing-2",
                                            "bob-electric-mixing-furnace", "bob-electric-chemical-furnace",
                                            "advanced-material-processing-3", "bob-multi-purpose-furnace-1",
                                            "advanced-material-processing-4", "bob-multi-purpose-furnace-2")
progressive_rows["progressive-worker-robots-storage"] += ("bob-infinite-worker-robots-storage-4",)
del progressive_rows["progressive-bob-vehicle-roboport-equipment"]
del progressive_rows["progressive-bob-vehicle-roboport-modular-equipment"]
progressive_rows["progressive-bob-vehicle-roboport-equipment"] = ("bob-vehicle-roboport-equipment-1",
                                                                  "bob-vehicle-roboport-modular-equipment-1",
                                                                  "bob-vehicle-roboport-equipment-2",
                                                                  "bob-vehicle-roboport-modular-equipment-2",
                                                                  "bob-vehicle-roboport-equipment-3",
                                                                  "bob-vehicle-roboport-modular-equipment-3",
                                                                  "bob-vehicle-roboport-equipment-4",
                                                                  "bob-vehicle-roboport-modular-equipment-4")
del progressive_rows["progressive-bob-robots"]
progressive_rows["progressive-robots"] = ("construction-robotics", "logistic-robotics",
                                          "bob-robots-1", "bob-robots-2", "bob-robots-3", "bob-robots-4")
progressive_rows["progressive-lab"] = ("bob-burner-lab", "bob-lab", "bob-advanced-research")

sorted_rows = sorted(progressive_rows)

# integrate into
source_target_mapping: Dict[str, str] = {
    # "progressive-braking-force": "progressive-train-network",
    # "progressive-inserter-capacity-bonus": "progressive-inserter",
    "progressive-refined-flammables": "progressive-flamethrower",
    "progressive-bob-electrolyser": "progressive-bob-electrolysis",
}

for source, target in source_target_mapping.items():
    progressive_rows[target] += progressive_rows[source]

base_tech_table = tech_table.copy()  # without progressive techs
base_technology_table = technology_table.copy()

progressive_tech_table: Dict[str, int] = {}
progressive_technology_table: Dict[str, Technology] = {}

useless_technologies: Set[str] = {tech_name for tech_name in base_tech_table
                                  if not technology_table[tech_name].useful()}
useless_technologies.remove("bob-long-inserters-1")
useless_technologies.remove("bob-long-inserters-2")
useless_technologies.remove("bob-more-inserters-1")
useless_technologies.remove("bob-more-inserters-2")
useless_technologies.remove("bob-near-inserters")

for root in sorted_rows:
    progressive = tuple(tech_name for tech_name in progressive_rows[root] if tech_name not in useless_technologies)
    if not progressive:
        print(f"Useless progressive skipping: {root}, {progressive_rows[root]}")
        continue
    assert all(tech in tech_table for tech in progressive), \
        (f"Declared a progressive technology ({root}) without base technology. "
         f"Missing: f{tuple(tech for tech in progressive if tech not in tech_table)}")
    factorio_tech_id += 1
    progressive_technology = Technology(root, factorio_tech_id,
                                        tuple(progressive),
                                        modifiers=sorted(set.union(
                                            *(set(technology_table[tech].modifiers) for tech in progressive)
                                        )),
                                        unlocks=any(technology_table[tech].unlocks for tech in progressive),)
    progressive_tech_table[root] = progressive_technology.factorio_id
    progressive_technology_table[root] = progressive_technology

tech_to_progressive_lookup: Dict[str, str] = {}
for technology in progressive_technology_table.values():
    if technology.name not in source_target_mapping:
        for progressive in technology.progressive:
            tech_to_progressive_lookup[progressive] = technology.name

tech_table.update(progressive_tech_table)
technology_table.update(progressive_technology_table)

# techs that are never progressive
common_tech_table: Dict[str, int] = {tech_name: tech_id for tech_name, tech_id in base_tech_table.items()
                                     if tech_name not in progressive_tech_table}

# exclusion_list: Set[str] = all_science_packs | {"rocket-part", "used-up-uranium-fuel-cell"}

excluded_automation_ingredients: Set[str] = {"bob-diamond-ore",
                                            "bob-amethyst-ore",
                                            "bob-emerald-ore",
                                            "bob-topaz-ore",
                                            "bob-sapphire-ore",
                                            "bob-ruby-ore",
                                            "bob-bauxite-ore",
                                            "bob-silver-ore",
                                            "bob-gold-ore",
                                            "bob-zinc-ore",
                                            "bob-tungsten-ore",
                                            "bob-nickel-ore",
                                            "bob-rutile-ore", }.union(artifacts)

def get_ordered_items(key: Callable[[InternalItem], int] = lambda item: item.get_score()) -> tuple[set[InternalItem], List[InternalItem]]:
    science_packs = FactorioOptions.MaxSciencePack.get_ordered_science_packs()
    valid_items = set(x for x in valid_ingredients.values() if all(raw.name not in invalid_ingredients for raw in x.get_raw_ingredients().keys())
                                                            and x.name not in science_packs)
    starting_pool = set()
    for item in valid_items:
        if not item.all_unlocking_technologies() and not item.is_fluid and all(raw.name not in excluded_automation_ingredients for raw in item.get_raw_ingredients().keys()):
            starting_pool.add(item)

    valid_items.difference_update(starting_pool)
    ordered_items: list[InternalItem] = list(sorted(valid_items, key=key))
    return starting_pool, ordered_items

@Utils.cache_argsless
def get_science_pack_pools() -> Dict[str, List[InternalItem]]:
    science_pack_pools: Dict[str, Set[InternalItem]] = {}
    # already_taken = exclusion_list.copy()
    already_taken = set()
    current_difficulty = 5
    science_packs = FactorioOptions.MaxSciencePack.get_ordered_science_packs()
    for science_pack in science_packs:
        current = science_pack_pools[science_pack] = set()
        for name, item in valid_ingredients.items():
            if (item.name not in science_packs
                    and not (science_pack == "automation-science-pack"
                             and (item.all_unlocking_technologies()
                                  or item.is_fluid
                                  or any(raw.name in excluded_automation_ingredients for raw in item.get_raw_ingredients().keys())))
                    and item not in already_taken
                    and item.get_score() < current_difficulty):
                current.add(item)

        if science_pack == "logistic-science-pack":
            current.add(all_ingredients["steam"])

        already_taken |= current
        current_difficulty *= 2

    sorted_pools: Dict[str, List[InternalItem]] = {science: list(sorted(sci_pool, key=lambda item: item.name))
                                                   for science, sci_pool in science_pack_pools.items()}

    for science in science_packs:
        print(f"{science}: {sorted_pools[science]}")

    return sorted_pools


# cleanup async helpers
pool.shutdown()
del pool
del factorio_tech_id
