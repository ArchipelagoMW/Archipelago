# Factorio technologies are imported from a .json document in /data
from typing import Dict, Set
import json
import Utils

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

    def get_required_technologies(self):
        requirements = set()
        for ingredient in self.ingredients:
            if ingredient in recipe_sources:  # no source likely means starting item
                requirements |= recipe_sources[ingredient]  # technically any, not all, need to improve later
        return requirements

    def build_rule(self):
        ingredient_rules = []
        for ingredient in self.ingredients:
            if ingredient in recipe_sources:
                technologies = recipe_sources[ingredient]  # technologies that unlock the recipe
                ingredient_rules.append(lambda state, technologies=technologies: any(state.has(technology) for technology in technologies))
        ingredient_rules = frozenset(ingredient_rules)
        return lambda state: all(rule(state) for rule in ingredient_rules)

    def __hash__(self):
        return self.factorio_id

class Recipe():
    def __init__(self, name, category, ingredients, products):
        self.name = name
        self.category = category
        self.products = ingredients
        self.ingredients = products

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


recipe_sources = {}  # recipe_name -> technology source

for technology, data in raw.items():
    for recipe in data["unlocks"]:
        recipe_sources.setdefault(recipe, set()).add(technology)


del (raw)
lookup_id_to_name: Dict[int, str] = {item_id: item_name for item_name, item_id in tech_table.items()}


all_recipes = set()
for recipe_name, recipe_data in raw_recipes.items():
    # example:
    # "accumulator":{"ingredients":["iron-plate","battery"],"products":["accumulator"],"category":"crafting"}
    all_recipes.add(Recipe(recipe_name, recipe_data["category"], set(recipe_data["ingredients"]), set(recipe_data["products"])))
