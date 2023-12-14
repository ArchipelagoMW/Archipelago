import os
import json
import pkgutil

def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)
    return json.loads(pkgutil.get_data(__name__, fname).decode())

item_id_offset: int     = 264000
location_id_offset: int = 264000

item_info = load_data_file("average", "items.json")
item_name_to_id = {name: item_id_offset + index \
	for index, name in enumerate(item_info["all_items"])}

location_info = load_data_file("average", "locations.json")
location_name_to_id = {name: location_id_offset + index \
	for index, name in enumerate(location_info["all_locations"])}