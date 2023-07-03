import os
import json
import pkgutil

def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)
    return json.loads(pkgutil.get_data(__name__, fname).decode())



item_info = load_data_file("items.json")
location_info = load_data_file("locations.json")

#item_name_to_id = {name: offset + index \
#	for index, name in enumerate(item_info["all_items"])}


#location_name_to_id = {name: offset + index \
#	for index, name in enumerate(location_info["all_locations"])}