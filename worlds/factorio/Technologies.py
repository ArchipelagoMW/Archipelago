# Factorio technologies are imported from a .json document in /data
from typing import Dict, Set, FrozenSet
import json
import Utils
import logging

factorio_id = 2 ** 17

source_file = Utils.local_path("data", "factorio", "techs.json")
recipe_source_file = Utils.local_path("data", "factorio", "recipes.json")
with open(source_file) as f:
    raw = json.load(f)
with open(recipe_source_file) as f:
    raw_recipes = json.load(f)
tech_table = {}
technology_table = {}


class Technology():  # maybe make subclass of Location?
    def __init__(self, name, ingredients):
        self.name = name
        global factorio_id
        self.factorio_id = factorio_id
        factorio_id += 1
        self.ingredients = ingredients

    def build_rule(self, allowed_packs, player: int):
        logging.debug(f"Building rules for {self.name}")
        ingredient_rules = []
        for ingredient in self.ingredients:
            if ingredient in allowed_packs:
                logging.debug(f"Building rules for ingredient {ingredient}")
                technologies = required_technologies[ingredient]  # technologies that unlock the recipes
                if technologies:
                    logging.debug(f"Required Technologies: {technologies}")
                    ingredient_rules.append(
                        lambda state, technologies=technologies: all(state.has(technology.name, player)
                                                                     for technology in technologies))
        ingredient_rules = frozenset(ingredient_rules)
        return lambda state: all(rule(state) for rule in ingredient_rules)

    def __hash__(self):
        return self.factorio_id

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class Recipe():
    def __init__(self, name, category, ingredients, products):
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.products = products

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    @property
    def unlocking_technologies(self) -> Set[Technology]:
        """Unlocked by any of the returned technologies. Empty set indicates a starting recipe."""
        return {technology_table[tech_name] for tech_name in recipe_sources.get(self.name, ())}


# recipes and technologies can share names in Factorio
for technology_name in sorted(raw):
    data = raw[technology_name]

    factorio_id += 1
    # not used yet
    # if data["requires"]:
    #     requirements[technology] = set(data["requires"])
    current_ingredients = set(data["ingredients"])
    technology = Technology(technology_name, current_ingredients)
    tech_table[technology_name] = technology.factorio_id
    technology_table[technology_name] = technology

recipe_sources: Dict[str, str] = {}  # recipe_name -> technology source

for technology, data in raw.items():
    for recipe_name in data["unlocks"]:
        recipe_sources.setdefault(recipe_name, set()).add(technology)

del (raw)
lookup_id_to_name: Dict[int, str] = {item_id: item_name for item_name, item_id in tech_table.items()}

all_recipes: Dict[str, Recipe] = {}
all_product_sources: Dict[str, Recipe] = {}
for recipe_name, recipe_data in raw_recipes.items():
    # example:
    # "accumulator":{"ingredients":["iron-plate","battery"],"products":["accumulator"],"category":"crafting"}

    recipe = Recipe(recipe_name, recipe_data["category"], set(recipe_data["ingredients"]), set(recipe_data["products"]))
    if recipe.products != recipe.ingredients:  # prevents loop recipes like uranium centrifuging
        all_recipes[recipe_name] = recipe
        for product_name in recipe.products:
            all_product_sources[product_name] = recipe

# build requirements graph for all technology ingredients

all_ingredient_names: Set[str] = set()
for technology in technology_table.values():
    all_ingredient_names |= technology.ingredients


def recursively_get_unlocking_technologies(ingredient_name, _done=None) -> Set[Technology]:
    if _done:
        if ingredient_name in _done:
            return set()
        else:
            _done.add(ingredient_name)
    else:
        _done = set(ingredient_name)
    recipe = all_product_sources.get(ingredient_name)
    if not recipe:
        return set()
    current_technologies = recipe.unlocking_technologies.copy()
    for ingredient_name in recipe.ingredients:
        current_technologies |= recursively_get_unlocking_technologies(ingredient_name, _done)
    return current_technologies


required_technologies: Dict[str, FrozenSet[Technology]] = {}
for ingredient_name in all_ingredient_names:
    required_technologies[ingredient_name] = frozenset(recursively_get_unlocking_technologies(ingredient_name))

advancement_technologies: Set[str] = set()
for technologies in required_technologies.values():
    advancement_technologies |= {technology.name for technology in technologies}
