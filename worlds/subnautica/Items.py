import json
import os

with open(os.path.join(os.path.dirname(__file__), 'items.json'), 'r') as file:
    item_table = json.loads(file.read())

lookup_id_to_name = {}
lookup_name_to_item = {}
for item in item_table:
    lookup_id_to_name[item["id"]] = item["name"]
    lookup_name_to_item[item["name"]] = item

lookup_id_to_name[None] = "Victory"

lookup_name_to_id = {name: id for id, name in lookup_id_to_name.items()}