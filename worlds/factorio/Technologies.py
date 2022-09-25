from __future__ import annotations

import json
import logging
import os
import string
from sys import getrecursionlimit
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Set, FrozenSet, Tuple, Union, List, Any

import Utils
from . import Options

factorio_id = factorio_base_id = 2 ** 17
# Factorio technologies are imported from a .json document in /data
source_folder = os.path.join(os.path.dirname(__file__), "data")

pool = ThreadPoolExecutor(1)


def load_json_data(data_name: str) -> Union[List[str], Dict[str, Any]]:
    import pkgutil
    return json.loads(pkgutil.get_data(__name__, "data/" + data_name + ".json").decode())

# TODO: Make use of the lab information. (it has info on the science packs)
techs_future = pool.submit(load_json_data, "techs")
recipes_future = pool.submit(load_json_data, "recipes")
resources_future = pool.submit(load_json_data, "resources")
machines_future = pool.submit(load_json_data, "machines")
fluids_future = pool.submit(load_json_data, "fluids")
items_future = pool.submit(load_json_data, "items")
mods_future = pool.submit(load_json_data, "mods")

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
    has_modifier: bool
    factorio_id: int
    name: str
    ingredients: Set[str]
    progressive: Tuple[str]
    unlocks: Union[Set[str], bool]  # bool case is for progressive technologies

    def __init__(self, name: str, ingredients: Set[str], factorio_id: int, progressive: Tuple[str] = (),
                 has_modifier: bool = False, unlocks: Union[Set[str], bool] = None):
        self.name = name
        self.factorio_id = factorio_id
        self.ingredients = ingredients
        self.progressive = progressive
        self.has_modifier = has_modifier
        if unlocks:
            self.unlocks = unlocks
        else:
            self.unlocks = set()

    def build_rule(self, player: int):
        logging.debug(f"Building rules for {self.name}")

        return lambda state: all(state.has(f"Automated {ingredient}", player)
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

    def useful(self) -> bool:
        return self.has_modifier or self.unlocks


class CustomTechnology(Technology):
    """A particularly configured Technology for a world."""

    def __init__(self, origin: Technology, world, allowed_packs: Set[str], player: int):
        ingredients = origin.ingredients & allowed_packs
        if origin.ingredients and not ingredients:
            logging.warning(f"Technology {origin.name} has no vanilla science packs. Custom science packs are not supported.")
        military_allowed = "military-science-pack" in allowed_packs \
                           and ((ingredients & {"chemical-science-pack", "production-science-pack", "utility-science-pack"})
                                or origin.name == "rocket-silo")
        self.player = player
        if origin.name not in world.worlds[player].static_nodes:
            if military_allowed:
                ingredients.add("military-science-pack")
            ingredients = list(ingredients)
            ingredients.sort()  # deterministic sample
            if ingredients:
                ingredients = world.random.sample(ingredients, world.random.randint(1, len(ingredients)))
        elif origin.name == "rocket-silo" and military_allowed:
            ingredients.add("military-science-pack")
        super(CustomTechnology, self).__init__(origin.name, ingredients, origin.factorio_id)


class Recipe(FactorioElement):
    name: str
    category: str
    ingredients: Dict[str, int]
    products: Dict[str, int]
    energy: float
    mining: bool
    unlocked_at_start: bool

    def __init__(self, name: str, category: str, ingredients: Dict[str, int], products: Dict[str, int], energy: float, mining: bool, unlocked_at_start: bool):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.products = products
        self.energy = energy
        self.mining = mining
        self.unlocked_at_start = unlocked_at_start

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    @property
    def crafting_machine(self) -> str:
        """cheapest crafting machine name able to run this recipe"""
        return machine_per_category[self.category]

    @property
    def unlocking_technologies(self) -> Set[Technology]:
        """Unlocked by any of the returned technologies. Empty set indicates a starting recipe."""
        return {technology_table[tech_name] for tech_name in recipe_sources.get(self.name, ())}

    @property
    def recursive_unlocking_technologies(self) -> Set[Technology]:
        base = {technology_table[tech_name] for tech_name in recipe_sources.get(self.name, ())}
        for ingredient in self.ingredients:
            base |= required_technologies[ingredient]
        base |= required_technologies[self.crafting_machine]
        return base

    @property
    def rel_cost(self) -> float:
        ingredients = sum(self.ingredients.values())
        if all(amount == 0 for amount in self.products.values()):
            return float('inf')
        return min(ingredients / amount for product, amount in self.products.items() if amount > 0)

    @property
    def base_cost(self) -> Dict[str, int]:
        ingredients = Counter()
        for ingredient, cost in self.ingredients.items():
            if ingredient in all_product_sources:
                for recipe in all_product_sources[ingredient]:
                    if recipe.ingredients:
                        ingredients.update({name: amount * cost / recipe.products[ingredient] for name, amount in
                                            recipe.base_cost.items()})
                    else:
                        ingredients[ingredient] += recipe.energy * cost / recipe.products[ingredient]
            else:
                ingredients[ingredient] += cost
        return ingredients

    recursion_loop = 0
    max_recursion_loop = 0.85 * getrecursionlimit()

    def detect_recursive_loop(self) -> bool:
        Recipe.recursion_loop += 1
        if Recipe.max_recursion_loop < Recipe.recursion_loop:
            Recipe.recursion_loop = 0
            return True
        for ingredient in self.ingredients.keys():
            if ingredient in all_product_sources:
                for ingredient_recipe in all_product_sources[ingredient]:
                    if ingredient_recipe.ingredients:
                        if ingredient_recipe.detect_recursive_loop():
                            return True
        Recipe.recursion_loop -= 1
        return False

    @property
    def total_energy(self) -> float:
        """Total required energy (crafting time) for single craft"""
        total_energy = (self.energy / machines[self.crafting_machine].speed)
        for ingredient, cost in self.ingredients.items():
            if ingredient in all_product_sources:
                selected_recipe_energy = float('inf')
                for ingredient_recipe in all_product_sources[ingredient]:
                    craft_count = max((n for name, n in ingredient_recipe.products.items() if name == ingredient))
                    recipe_energy = ingredient_recipe.total_energy / craft_count * cost
                    if recipe_energy < selected_recipe_energy:
                        selected_recipe_energy = recipe_energy
                total_energy += selected_recipe_energy
        return total_energy


class Machine(FactorioElement):
    def __init__(self, name, categories, machine_type, speed):
        self.name: str = name
        self.categories: set = categories
        self.machine_type: str = machine_type
        self.speed: float = speed

class Lab(FactorioElement):
    def __init__(self, name, inputs):
        self.name: str = name
        self.inputs: set = inputs


class Mod(FactorioElement):
    def __init__(self, name, version):
        self.name: str = name
        self.version: str = version


class Item(FactorioElement):
    def __init__(self, name, stack_size, stackable, place_result, burnt_result, fuel_value, fuel_category, rocket_launch_products):
        self.name: str = name
        self.stack_size: int = stack_size
        self.stackable: bool = stackable
        self.place_result: str = place_result
        self.burnt_result: str = burnt_result
        self.fuel_value: int = fuel_value
        self.fuel_category: str = fuel_category
        self.rocket_launch_products: Dict[str, int] = rocket_launch_products

class Fluid(FactorioElement):
    def __init__(self, name, default_temperature, max_temperature, heat_capacity):
        self.name: str = name
        if max_temperature == "inf":
            max_temperature = 2**64
        self.default_temperature: int = default_temperature
        self.max_temperature: int = max_temperature
        self.heat_capacity = heat_capacity


items: Dict[str, Item] = {}
for name, item_data in items_future.result().items():
    item = Item(name,
                item_data.get("stack_size"),
                item_data.get("stackable"),
                item_data.get("place_result", None),
                item_data.get("burnt_result", None),
                item_data.get("fuel_value", 0),
                item_data.get("fuel_category", None),
                item_data.get("rocket_launch_products", {}))
    items[name] = item
del items_future

fluids: Dict[str, Fluid] = {}
for name, fluid_data in fluids_future.result().items():
    fluid = Fluid(name,
                  fluid_data.get("default_temperature", 0),
                  fluid_data.get("max_temperature", 0),
                  fluid_data.get("heat_capacity", 1000))
    fluids[name] = fluid
del fluids_future

recipe_sources: Dict[str, Set[str]] = {}  # recipe_name -> technology source

# recipes and technologies can share names in Factorio
for technology_name, data in sorted(techs_future.result().items()):
    current_ingredients = set(data["ingredients"])
    technology = Technology(technology_name, current_ingredients, factorio_id,
                            has_modifier=data["has_modifier"], unlocks=set(data["unlocks"]))
    factorio_id += 1
    tech_table[technology_name] = technology.factorio_id
    technology_table[technology_name] = technology
    for recipe_name in technology.unlocks:
        recipe_sources.setdefault(recipe_name, set()).add(technology_name)

del techs_future

recipes = {}
all_product_sources: Dict[str, Set[Recipe]] = {"character": set()}
# add uranium mining to logic graph. TODO: add to automatic extractor for mod support
raw_recipes = recipes_future.result()
del recipes_future
for resource_name, resource_data in resources_future.result().items():
    raw_recipes[f"mining-{resource_name}"] = {
        "ingredients": {resource_data["required_fluid"]: resource_data["fluid_amount"]}
        if "required_fluid" in resource_data else {},
        "products": {data["name"]: data["amount"] for data in resource_data["products"].values()},
        "energy": resource_data["mining_time"],
        "category": resource_data["category"],
        "mining": True,
        "unlocked_at_start": True
    }
del resources_future

machines: Dict[str, Machine] = {}
labs: Dict[str, Lab] = {}

for name, prototype in machines_future.result().items():
    for machine_type, machine_data in prototype.items():
        if machine_type == "lab":
            lab = Lab(name, machine_data.get("inputs", set()))
            labs[name] = lab
        if machine_type == "offshore-pump":
            fluid = machine_data.get("fluid", None)
            speed = machine_data.get("speed", None)
            if not fluid or not speed:
                continue
            category = f"offshore-pumping-{fluid}-{speed}"
            raw_recipes[category] = {
                "ingredients": {},
                "products": {fluid: (speed*60)},
                "energy": 1,
                "category": category,
                "mining": True,
                "unlocked_at_start": True
            }
            machine = Machine(name, {category}, machine_data.get("type"), 1)
            machines[name] = machine
        if machine_type == "crafting":
            categories = machine_data.get("categories", set())
            if not categories:
                continue
            # TODO: Use speed / fluid_box info
            speed = machine_data.get("speed", 1)
            input_fluid_box = machine_data.get("input_fluid_box", 0)
            output_fluid_box = machine_data.get("output_fluid_box", 0)
            machine = Machine(name, set(categories), machine_data.get("type"), speed)
            machines[name] = machine
        if machine_type == "mining":
            categories = machine_data.get("categories", set())
            if not categories:
                continue
            speed = machine_data.get("speed", 1)
            input_fluid_box = machine_data.get("input_fluid_box", False)  # Can this machine mine resources with required fluids?
            output_fluid_box = machine_data.get("output_fluid_box", False)  # Can this machine mine fluid resources?
            machine = machines.setdefault(name, Machine(name, set(categories), machine_data.get("type"), speed))
            machine.categories |= set(categories)  # character has both crafting and basic-solid
            machine.speed = (machine.speed + speed) / 2
            machines[name] = machine
        if machine_type == "boiler":
            input_fluid = machine_data.get("input_fluid")
            output_fluid = machine_data.get("output_fluid")
            target_temperature = machine_data.get("target_temperature")
            energy_usage = machine_data.get("energy_usage")
            amount = energy_usage / (target_temperature - fluids[input_fluid].get("default_temperature", 15)) / fluids[input_fluid].get("heat_capacity", 1)
            amount *= 60
            amount = int(amount)
            category = f"boiling-{amount}-{input_fluid}-to-{output_fluid}-at-{target_temperature}-degrees-centigrade"
            raw_recipes[category] = {
                "ingredients": {input_fluid: amount},
                "products": {output_fluid: amount},
                "energy": 1,
                "category": category,
                "mining": False,
                "unlocked_at_start": True
            }
            machine = Machine(name, {category}, machine_data.get("type"), 1)
            machines[name] = machine

        # TODO: set up machine/recipe pairs for burners in order to retrieve the burnt_result from items.
        # TODO: set up machine/recipe pairs for retrieving rocket_launch_products from items.



del machines_future

for recipe_name, recipe_data in raw_recipes.items():
    # example:
    # "accumulator":{"ingredients":{"iron-plate":2,"battery":5},"products":{"accumulator":1},"category":"crafting"}
    # FIXME: add mining?
    recipe = Recipe(recipe_name, recipe_data["category"], recipe_data["ingredients"],
                    recipe_data["products"], recipe_data.get("energy", 0), recipe_data.get("mining", False), recipe_data.get("unlocked_at_start", False))
    recipes[recipe_name] = recipe
    if set(recipe.products).isdisjoint(set(recipe.ingredients)):
        for product_name in [product_name for product_name, amount in recipe.products.items() if amount > 0]:
            all_product_sources.setdefault(product_name, set()).add(recipe)
            if recipe.detect_recursive_loop():
                # prevents loop recipes like uranium centrifuging and fluid unbarreling
                all_product_sources.setdefault(product_name, set()).remove(recipe)
                if not all_product_sources[product_name]:
                    del (all_product_sources[product_name])


machines["assembling-machine-1"].categories |= machines["assembling-machine-3"].categories  # mod enables this
machines["assembling-machine-2"].categories |= machines["assembling-machine-3"].categories
# machines["character"].categories.add("basic-crafting")
# charter only knows the categories of "crafting" and "basic-solid" by default.


mods: Dict[str, Mod] = {}

for name, version in mods_future.result().items():
    if name in ["base"]:
        continue
    mod = Mod(name, version)
    mods[name] = mod

del mods_future


# build requirements graph for all technology ingredients

all_ingredient_names: Set[str] = set()
for technology in technology_table.values():
    all_ingredient_names |= technology.ingredients


def unlock_just_tech(recipe: Recipe, _done) -> Set[Technology]:
    if recipe.unlocked_at_start:
        current_technologies = set()
    else:
        current_technologies = recipe.unlocking_technologies
    for ingredient_name in recipe.ingredients:
        current_technologies |= recursively_get_unlocking_technologies(ingredient_name, _done,
                                                                       unlock_func=unlock_just_tech)
    return current_technologies


def unlock(recipe: Recipe, _done) -> Set[Technology]:
    if recipe.unlocked_at_start:
        current_technologies = set()
    else:
        current_technologies = recipe.unlocking_technologies
    for ingredient_name in recipe.ingredients:
        current_technologies |= recursively_get_unlocking_technologies(ingredient_name, _done, unlock_func=unlock)
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
    if ingredient_name == "character":
        required_machine_technologies[ingredient_name] = frozenset()
        continue
    required_machine_technologies[ingredient_name] = frozenset(recursively_get_unlocking_technologies(ingredient_name))
for ingredient_name in labs:
    required_machine_technologies[ingredient_name] = frozenset(recursively_get_unlocking_technologies(ingredient_name))

logical_machines = {}
machine_tech_cost = {}

for category in machines["character"].categories:
    machine_tech_cost[category] = (10000, "character", machines["character"].speed)

for machine in machines.values():
    if machine.name == "character":
        continue
    for category in machine.categories:
        machine_cost = len(required_machine_technologies[machine.name])
        if machine.machine_type == "character" and not machine_cost:
            machine_cost = 10000
        if category in machine_tech_cost:
            current_cost, current_machine, current_speed = machine_tech_cost.get(category)
            if machine_cost < current_cost or (machine_cost == current_cost and machine.speed > current_speed):
                machine_tech_cost[category] = machine_cost, machine.name, machine.speed
        else:
            machine_tech_cost[category] = machine_cost, machine.name, machine.speed

machine_per_category: Dict[str: str] = {}
for category, (cost, machine_name, speed) in machine_tech_cost.items():
    machine_per_category[category] = machine_name

del machine_tech_cost

# required technologies to be able to craft recipes from a certain category
required_category_technologies: Dict[str, FrozenSet[FrozenSet[Technology]]] = {}
for category_name, machine_name in machine_per_category.items():
    techs = set()
    techs |= recursively_get_unlocking_technologies(machine_name)
    if category_name in machines["character"].categories and techs:
        # Character crafting/mining categories always have no tech assigned.
        techs = set()
        machine_per_category[category_name] = "character"
    required_category_technologies[category_name] = frozenset(techs)

required_technologies: Dict[str, FrozenSet[Technology]] = Utils.KeyedDefaultDict(lambda ingredient_name: frozenset(
    recursively_get_unlocking_technologies(ingredient_name, unlock_func=unlock)))


def get_rocket_requirements(silo_recipe: Recipe, part_recipe: Recipe, satellite_recipe: Recipe) -> Set[str]:
    techs = set()
    if silo_recipe:
        for ingredient in silo_recipe.ingredients:
            techs |= recursively_get_unlocking_technologies(ingredient)
    for ingredient in part_recipe.ingredients:
        techs |= recursively_get_unlocking_technologies(ingredient)
    if satellite_recipe:
        techs |= satellite_recipe.unlocking_technologies
        for ingredient in satellite_recipe.ingredients:
            techs |= recursively_get_unlocking_technologies(ingredient)
    return {tech.name for tech in techs}


free_sample_exclusions: Set[str] = all_ingredient_names | {"rocket-part"}

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
    seeking = root + "-2"
    progressive = [root]
    while seeking in progressive_incs:
        progressive.append(seeking)
        seeking = seeking[:-1] + str(int(seeking[-1]) + 1)
    progressive_rows["progressive-" + root] = tuple(progressive)

# science packs
progressive_rows["progressive-science-pack"] = tuple(Options.MaxSciencePack.get_ordered_science_packs())[1:]

# manual progressive
progressive_rows["progressive-processing"] = (
    "steel-processing",
    "oil-processing", "sulfur-processing", "advanced-oil-processing", "coal-liquefaction",
    "uranium-processing", "kovarex-enrichment-process", "nuclear-fuel-reprocessing")
progressive_rows["progressive-rocketry"] = ("rocketry", "explosive-rocketry", "atomic-bomb")
progressive_rows["progressive-vehicle"] = ("automobilism", "tank", "spidertron")
progressive_rows["progressive-train-network"] = ("railway", "fluid-wagon",
                                                 "automated-rail-transportation", "rail-signals")
progressive_rows["progressive-engine"] = ("engine", "electric-engine")
progressive_rows["progressive-armor"] = ("heavy-armor", "modular-armor", "power-armor", "power-armor-mk2")
progressive_rows["progressive-personal-battery"] = ("battery-equipment", "battery-mk2-equipment")
progressive_rows["progressive-energy-shield"] = ("energy-shield-equipment", "energy-shield-mk2-equipment")
progressive_rows["progressive-wall"] = ("stone-wall", "gate")
progressive_rows["progressive-follower"] = ("defender", "distractor", "destroyer")
progressive_rows["progressive-inserter"] = ("fast-inserter", "stack-inserter")

sorted_rows = sorted(progressive_rows)
# to keep ID mappings the same.
# If there's a breaking change at some point, then this should be moved in with the sorted ordering
progressive_rows["progressive-turret"] = ("gun-turret", "laser-turret")
sorted_rows.append("progressive-turret")
progressive_rows["progressive-flamethrower"] = ("flamethrower",)  # leaving out flammables, as they do nothing
sorted_rows.append("progressive-flamethrower")
progressive_rows["progressive-personal-roboport-equipment"] = ("personal-roboport-equipment",
                                                               "personal-roboport-mk2-equipment")
sorted_rows.append("progressive-personal-roboport-equipment")
# integrate into
source_target_mapping: Dict[str, str] = {
    "progressive-braking-force": "progressive-train-network",
    "progressive-inserter-capacity-bonus": "progressive-inserter",
    "progressive-refined-flammables": "progressive-flamethrower"
}

for source, target in source_target_mapping.items():
    progressive_rows[target] += progressive_rows[source]

base_tech_table = tech_table.copy()  # without progressive techs
base_technology_table = technology_table.copy()

progressive_tech_table: Dict[str, int] = {}
progressive_technology_table: Dict[str, Technology] = {}

for root in sorted_rows:
    progressive = progressive_rows[root]
    assert all(tech in tech_table for tech in progressive), "declared a progressive technology without base technology"
    factorio_id += 1
    progressive_technology = Technology(root, technology_table[progressive_rows[root][0]].ingredients, factorio_id,
                                        progressive,
                                        has_modifier=any(technology_table[tech].has_modifier for tech in progressive),
                                        unlocks=any(technology_table[tech].unlocks for tech in progressive))
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

useless_technologies: Set[str] = {tech_name for tech_name in common_tech_table
                                  if not technology_table[tech_name].useful()}

lookup_id_to_name: Dict[int, str] = {item_id: item_name for item_name, item_id in tech_table.items()}

rel_cost = {}
for name, recipe in {name: recipe for name, recipe in recipes.items() if recipe.mining and not recipe.ingredients}.items():
    machine = machines[machine_per_category[recipe.category]]
    cost = recipe.energy / machine.speed
    for product_name, amount in recipe.products.items():
        rel_cost[product_name] = cost / amount


def get_estimated_difficulty(recipe: Recipe):
    base_ingredients = recipe.base_cost
    cost = 0

    for ingredient_name, amount in base_ingredients.items():
        cost += rel_cost.get(ingredient_name, 1000) * amount
    return cost


for name, recipe in {name: recipe for name, recipe in recipes.items() if recipe.mining and recipe.ingredients}.items():
    machine = machines[machine_per_category[recipe.category]]
    cost = (recipe.energy / machine.speed) + get_estimated_difficulty(recipe)
    for product_name, amount in recipe.products.items():
        rel_cost[product_name] = cost / amount

exclusion_list: Set[str] = all_ingredient_names | {"rocket-part", "used-up-uranium-fuel-cell"}


@Utils.cache_argsless
def get_science_pack_pools() -> Dict[str, Set[str]]:
    science_pack_pools: Dict[str, Set[str]] = {}
    already_taken = exclusion_list.copy()
    current_difficulty = 5
    for science_pack in Options.MaxSciencePack.get_ordered_science_packs():
        current = science_pack_pools[science_pack] = set()
        for name, recipe in recipes.items():
            if (science_pack != "automation-science-pack" or not recipe.recursive_unlocking_technologies) \
                    and get_estimated_difficulty(recipe) < current_difficulty:
                current |= set(recipe.products)

        if science_pack == "automation-science-pack":
            # Can't handcraft automation science if fluids end up in its recipe, making the seed impossible.
            current -= set(fluids)

        current -= already_taken
        already_taken |= current
        current_difficulty *= 2

    return science_pack_pools


non_stacking_items: Set[str] = {name for name, item in items.items() if not item.stackable}
stacking_items: Set[str] = set(items) - non_stacking_items
valid_ingredients: Set[str] = stacking_items | set(fluids)

# cleanup async helpers
pool.shutdown()
del pool
