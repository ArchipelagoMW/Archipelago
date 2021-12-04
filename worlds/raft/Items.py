import json
import os

with open(os.path.join(os.path.dirname(__file__), 'items.json'), 'r') as file:
    item_table = json.loads(file.read())

lookup_id_to_name = {}
lookup_name_to_item = {}
advancement_item_names = set()
non_advancement_item_names = set()

for item in item_table:
    item_name = item["name"]
    lookup_id_to_name[item["id"]] = item_name
    lookup_name_to_item[item_name] = item
    if item["progression"]:
        advancement_item_names.add(item_name)
    else:
        non_advancement_item_names.add(item_name)

lookup_id_to_name[None] = "Victory"

lookup_name_to_id = {name: id for id, name in lookup_id_to_name.items()}