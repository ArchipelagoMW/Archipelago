from __future__ import annotations
# Factorio technologies are imported from a .json document in /data
from typing import Dict, Set, FrozenSet, Tuple
import os
import json
import string

import Utils
import logging
import functools

from . import Options

factorio_id = 2 ** 17
source_folder = Utils.local_path("data", "factorio")

with open(os.path.join(source_folder, "techs.json")) as f:
    raw = json.load(f)
with open(os.path.join(source_folder, "recipes.json")) as f:
    raw_recipes = json.load(f)
with open(os.path.join(source_folder, "machines.json")) as f:
    raw_machines = json.load(f)
tech_table: Dict[str, int] = {}
technology_table: Dict[str, Technology] = {}

always = lambda state: True


class FactorioElement():
    name: str

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __hash__(self):
        return hash(self.name)


class Technology(FactorioElement):  # maybe make subclass of Location?
    def __init__(self, name: str, ingredients: Set[str], factorio_id: int, progressive: Tuple[str] = ()):
        self.name = name
        self.factorio_id = factorio_id
        self.ingredients = ingredients
        self.progressive = progressive

    def build_rule(self, player: int):
        logging.debug(f"Building rules for {self.name}")

        return lambda state, technologies=technologies: all(state.has(f"Automated {ingredient}", player)
                                                            for ingredient in self.ingredients)

    def get_prior_technologies(self) -> Set[Technology]:
        """Get Technologies that have to precede this one to resolve tree connections."""
        technologies = set()
        for ingredient in self.ingredients:
            technologies |= required_technologies[ingredient]  # technologies that unlock the recipes
        return technologies

    def __hash__(self):
        return self.factorio_id

    def get_custom(self, world, allowed_packs: Set[str], player: int) -> CustomTechnology:
        return CustomTechnology(self, world, allowed_packs, player)


class CustomTechnology(Technology):
    """A particularly configured Technology for a world."""

    def __init__(self, origin: Technology, world, allowed_packs: Set[str], player: int):
        ingredients = origin.ingredients & allowed_packs
        self.player = player
        if origin.name not in world.worlds[player].static_nodes:
            ingredients = list(ingredients)
            ingredients.sort()  # deterministic sample
            ingredients = world.random.sample(ingredients, world.random.randint(1, len(ingredients)))
        super(CustomTechnology, self).__init__(origin.name, ingredients, origin.factorio_id)


class Recipe(FactorioElement):
    name: str
    category: str
    ingredients: Dict[str, int]
    products: Dict[str, int]

    def __init__(self, name: str, category: str, ingredients: Dict[str, int], products: Dict[str, int]):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.products = products

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    @property
    def crafting_machines(self) -> Set[Machine]:
        """crafting machines able to run this recipe"""
        return machines_per_category[self.category]

    @property
    def unlocking_technologies(self) -> Set[Technology]:
        """Unlocked by any of the returned technologies. Empty set indicates a starting recipe."""
        return {technology_table[tech_name] for tech_name in recipe_sources.get(self.name, ())}


class Machine(FactorioElement):
    def __init__(self, name, categories):
        self.name: str = name
        self.categories: set = categories


# recipes and technologies can share names in Factorio
for technology_name in sorted(raw):
    data = raw[technology_name]
    current_ingredients = set(data["ingredients"])
    technology = Technology(technology_name, current_ingredients, factorio_id)
    factorio_id += 1
    tech_table[technology_name] = technology.factorio_id
    technology_table[technology_name] = technology

recipe_sources: Dict[str, str] = {}  # recipe_name -> technology source

for technology, data in raw.items():
    for recipe_name in data["unlocks"]:
        recipe_sources.setdefault(recipe_name, set()).add(technology)

del (raw)

recipes = {}
all_product_sources: Dict[str, Set[Recipe]] = {"character": set()}
# add uranium mining to logic graph. TODO: add to automatic extractor for mod support
raw_recipes["uranium-ore"] = {"ingredients": {"sulfuric-acid": 1}, "products": {"uranium-ore": 1}, "category": "mining"}

for recipe_name, recipe_data in raw_recipes.items():
    # example:
    # "accumulator":{"ingredients":{"iron-plate":2,"battery":5},"products":{"accumulator":1},"category":"crafting"}

    recipe = Recipe(recipe_name, recipe_data["category"], recipe_data["ingredients"], recipe_data["products"])
    recipes[recipe_name] = recipe
    if set(recipe.products).isdisjoint(
            set(recipe.ingredients)) and "empty-barrel" not in recipe.products:  # prevents loop recipes like uranium centrifuging
        for product_name in recipe.products:
            all_product_sources.setdefault(product_name, set()).add(recipe)

del (raw_recipes)

machines: Dict[str, Machine] = {}

for name, categories in raw_machines.items():
    machine = Machine(name, set(categories))
    machines[name] = machine

# add electric mining drill as a crafting machine to resolve uranium-ore
machines["electric-mining-drill"] = Machine("electric-mining-drill", {"mining"})
del (raw_machines)

# build requirements graph for all technology ingredients

all_ingredient_names: Set[str] = set()
for technology in technology_table.values():
    all_ingredient_names |= technology.ingredients


def unlock_just_tech(recipe: Recipe, _done) -> Set[Technology]:
    current_technologies = set()
    current_technologies |= recipe.unlocking_technologies
    for ingredient_name in recipe.ingredients:
        current_technologies |= recursively_get_unlocking_technologies(ingredient_name, _done)
    return current_technologies


def unlock(recipe: Recipe, _done) -> Set[Technology]:
    current_technologies = set()
    current_technologies |= recipe.unlocking_technologies
    for ingredient_name in recipe.ingredients:
        current_technologies |= recursively_get_unlocking_technologies(ingredient_name, _done)
    current_technologies |= required_category_technologies[recipe.category]

    return current_technologies


def recursively_get_unlocking_technologies(ingredient_name, _done=None, unlock_func=unlock_just_tech) -> Set[
    Technology]:
    if _done:
        if ingredient_name in _done:
            return set()
        else:
            _done.add(ingredient_name)
    else:
        _done = {ingredient_name}
    recipes = all_product_sources.get(ingredient_name)
    if not recipes:
        return set()
    current_technologies = set()
    for recipe in recipes:
        current_technologies |= unlock_func(recipe, _done)

    return current_technologies


required_machine_technologies: Dict[str, FrozenSet[Technology]] = {}
for ingredient_name in machines:
    required_machine_technologies[ingredient_name] = frozenset(recursively_get_unlocking_technologies(ingredient_name))

logical_machines = {}
for machine in machines.values():
    logically_useful = True
    for pot_source_machine in machines.values():
        if machine != pot_source_machine \
                and machine.categories.issuperset(pot_source_machine.categories) \
                and required_machine_technologies[machine.name].issuperset(
            required_machine_technologies[pot_source_machine.name]):
            logically_useful = False
            break

    if logically_useful:
        logical_machines[machine.name] = machine

del (required_machine_technologies)

machines_per_category: Dict[str: Set[Machine]] = {}
for machine in logical_machines.values():
    for category in machine.categories:
        machines_per_category.setdefault(category, set()).add(machine)

# required technologies to be able to craft recipes from a certain category
required_category_technologies: Dict[str, FrozenSet[FrozenSet[Technology]]] = {}
for category_name, cat_machines in machines_per_category.items():
    techs = set()
    for machine in cat_machines:
        techs |= recursively_get_unlocking_technologies(machine.name)
    required_category_technologies[category_name] = frozenset(techs)

required_technologies: Dict[str, FrozenSet[Technology]] = {}
for ingredient_name in all_ingredient_names:
    required_technologies[ingredient_name] = frozenset(
        recursively_get_unlocking_technologies(ingredient_name, unlock_func=unlock))

advancement_technologies: Set[str] = set()
for technologies in required_technologies.values():
    advancement_technologies |= {technology.name for technology in technologies}


@functools.lru_cache(10)
def get_rocket_requirements(ingredients: Set[str]) -> Set[str]:
    techs = recursively_get_unlocking_technologies("rocket-silo")
    for ingredient in ingredients:
        techs |= recursively_get_unlocking_technologies(ingredient)
    return {tech.name for tech in techs}


free_sample_blacklist = all_ingredient_names | {"rocket-part"}

rocket_recipes = {
    Options.MaxSciencePack.option_space_science_pack:
        {"rocket-control-unit": 10, "low-density-structure": 10, "rocket-fuel": 10},
    Options.MaxSciencePack.option_utility_science_pack:
        {"speed-module": 10, "steel-plate": 10, "solid-fuel": 10},
    Options.MaxSciencePack.option_production_science_pack:
        {"speed-module": 10, "steel-plate": 10, "solid-fuel": 10},
    Options.MaxSciencePack.option_chemical_science_pack:
        {"advanced-circuit": 10, "steel-plate": 10, "solid-fuel": 10},
    Options.MaxSciencePack.option_military_science_pack:
        {"defender-capsule": 10, "stone-wall": 10, "coal": 10},
    Options.MaxSciencePack.option_logistic_science_pack:
        {"electronic-circuit": 10, "stone-brick": 10, "coal": 10},
    Options.MaxSciencePack.option_automation_science_pack:
        {"copper-cable": 10, "iron-plate": 10, "wood": 10}
}
for products in rocket_recipes.values():
    requirements = get_rocket_requirements(frozenset(products))
    advancement_technologies |= requirements

# progressive technologies
# auto-progressive
progressive_rows = {}
progressive_incs = set()
for tech_name in tech_table:
    if tech_name.endswith("-1"):
        progressive_rows[tech_name] = []
    elif tech_name[-2] == "-" and tech_name[-1] in string.digits:
        progressive_incs.add(tech_name)

for root, progressive in progressive_rows.items():
    seeking = root[:-1]+str(int(root[-1])+1)
    while seeking in progressive_incs:
        progressive.append(seeking)
        progressive_incs.remove(seeking)
        seeking = seeking[:-1]+str(int(seeking[-1])+1)

# make root entry the progressive name
for old_name in set(progressive_rows):
    prog_name = "progressive-" + old_name.rsplit("-", 1)[0]
    progressive_rows[prog_name] = tuple([old_name] + progressive_rows[old_name])
    del(progressive_rows[old_name])

# no -1 start
base_starts = set()
for remnant in progressive_incs:
    if remnant[-1] == "2":
        base_starts.add(remnant[:-2])

for root in base_starts:
    seeking = root+"-2"
    progressive = [root]
    while seeking in progressive_incs:
        progressive.append(seeking)
        seeking = seeking[:-1]+str(int(seeking[-1])+1)
    progressive_rows["progressive-"+root] = tuple(progressive)

# science packs
progressive_rows["progressive-science-pack"] = tuple(sorted(required_technologies,
                                                            key=lambda name: len(required_technologies[name]))[1:] +
                                                     ["space-science-pack"])


# manual progressive
progressive_rows["progressive-processing"] = ("steel-processing",
                                              "oil-processing", "sulfur-processing", "advanced-oil-processing",
                                              "uranium-processing", "nuclear-fuel-reprocessing")
progressive_rows["progressive-rocketry"] = ("rocketry", "explosive-rocketry", "atomic-bomb")
progressive_rows["progressive-vehicle"] = ("automobilism", "tank", "spidertron")
progressive_rows["progressive-train-network"] = ("railway", "fluid-wagon", "automated-rail-transportation", "rail-signals")
progressive_rows["progressive-engine"] = ("engine", "electric-engine")
progressive_rows["progressive-armor"] = ("heavy-armor", "modular-armor", "power-armor", "power-armor-mk2")
progressive_rows["progressive-personal-battery"] = ("battery-equipment", "battery-mk2-equipment")
progressive_rows["progressive-energy-shield"] = ("energy-shield-equipment", "energy-shield-mk2-equipment")
progressive_rows["progressive-wall"] = ("stone-wall", "gate")
progressive_rows["progressive-follower"] = ("defender", "distractor", "destroyer")
progressive_rows["progressive-inserter"] = ("fast-inserter", "stack-inserter")

base_tech_table = tech_table.copy() # without progressive techs
base_technology_table = technology_table.copy()

progressive_tech_table: Dict[str, int] = {}
progressive_technology_table: Dict[str, Technology] = {}

for root in sorted(progressive_rows):
    progressive = progressive_rows[root]
    assert all(tech in tech_table for tech in progressive)
    factorio_id += 1
    progressive_technology = Technology(root, technology_table[progressive_rows[root][0]].ingredients, factorio_id,
                                        progressive)
    progressive_tech_table[root] = progressive_technology.factorio_id
    progressive_technology_table[root] = progressive_technology
    if any(tech in advancement_technologies for tech in progressive):
        advancement_technologies.add(root)

tech_to_progressive_lookup: Dict[str, str] = {}
for technology in progressive_technology_table.values():
    for progressive in technology.progressive:
        tech_to_progressive_lookup[progressive] = technology.name

tech_table.update(progressive_tech_table)
technology_table.update(progressive_technology_table)

# techs that are never progressive
common_tech_table: Dict[str, int] = {tech_name: tech_id for tech_name, tech_id in base_tech_table.items()
                                     if tech_name not in progressive_tech_table}

lookup_id_to_name: Dict[int, str] = {item_id: item_name for item_name, item_id in tech_table.items()}