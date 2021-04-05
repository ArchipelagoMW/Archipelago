# Factorio technologies are imported from a .json document in /data
from typing import Dict, Set
import json
import Utils

factorio_id = 2 ** 17

source_file = Utils.local_path("data", "factorio", "techs.json")

with open(source_file) as f:
    raw = json.load(f)
tech_table = {}
technology_table = {}
requirements = {}  # tech_name -> Set[required_technologies]


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
            if ingredient in recipe_sources: # no source likely means starting item
                requirements |= recipe_sources[ingredient] # technically any, not all, need to improve later
        return requirements

    def __hash__(self):
        return self.factorio_id


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
