import os
import json
import pkgutil

def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])
    return json.loads(pkgutil.get_data(__name__, fname).decode())

# For historical reasons, these values are different.
# They remain different to ensure datapackage consistency.
# Do not separate other games' location and item IDs like this.
item_id_offset: int 	= 45000
location_id_offset: int = 42000

item_info = load_data_file("items.json")
item_name_to_id = {name: item_id_offset + index \
	for index, name in enumerate(item_info["all_items"])}
item_name_to_id["Bee Trap"] = item_id_offset + 100  # historical reasons

location_info = load_data_file("locations.json")
location_name_to_id = {name: location_id_offset + index \
	for index, name in enumerate(location_info["all_locations"])}

exclusion_info = load_data_file("excluded_locations.json")

region_info = load_data_file("regions.json")
