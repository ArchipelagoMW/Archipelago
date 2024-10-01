import os
import json
import pkgutil

def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)
    return json.loads(pkgutil.get_data(__name__, fname).decode())

location_id_offset: int = 27000

location_info = load_data_file("locations.json")
location_name_to_id = {name: location_id_offset + index \
	for index, name in enumerate(location_info["all_locations"])}

exclusion_info = load_data_file("excluded_locations.json")

region_info = load_data_file("regions.json")
