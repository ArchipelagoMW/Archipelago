# Factorio technologies are imported from a .json document in /data
from typing import Dict
import os
import json

import Utils

factorio_id = 2**17

source_file = Utils.local_path("data", "factorio", "techs.json")

with open(source_file) as f:
    raw = json.load(f)
tech_table = {}

requirements = {}
ingredients = {}
all_ingredients = set()

# TODO: export this dynamically, or filter it during export
starting_ingredient_recipes = {"automation-science-pack"}

# recipes and technologies can share names in Factorio
for technology in sorted(raw):
    data = raw[technology]
    tech_table[technology] = factorio_id
    factorio_id += 1
    if data["requires"]:
        requirements[technology] = set(data["requires"])
    current_ingredients = set(data["ingredients"])-starting_ingredient_recipes
    if current_ingredients:
        all_ingredients |= current_ingredients
        ingredients[technology] = {"recipe-"+ingredient for ingredient in current_ingredients}

recipe_sources = {}

for technology, data in raw.items():
    recipe_source = all_ingredients & set(data["unlocks"])
    for recipe in recipe_source:
        recipe_sources["recipe-"+recipe] = technology

all_ingredients_recipe = {"recipe-"+ingredient for ingredient in all_ingredients}
del(raw)
lookup_id_to_name: Dict[int, str] = {item_id: item_name for item_name, item_id in tech_table.items()}