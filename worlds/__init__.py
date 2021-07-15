import importlib
import os

__all__ = {"lookup_any_item_id_to_name",
           "lookup_any_location_id_to_name",
           "network_data_package"}

# import all submodules to trigger AutoWorldRegister
for file in os.scandir(os.path.dirname(__file__)):
    if file.is_dir():
        importlib.import_module(f".{file.name}", "worlds")

from .AutoWorld import AutoWorldRegister
lookup_any_item_id_to_name = {}
lookup_any_location_id_to_name = {}
games = {}

for world_name, world in AutoWorldRegister.world_types.items():
    games[world_name] = {
        "item_name_to_id" : world.item_name_to_id,
        "location_name_to_id": world.location_name_to_id,
        "version": world.data_version,
        # seems clients don't actually want this. Keeping it here in case someone changes their mind.
        # "item_name_groups": {name: tuple(items) for name, items in world.item_name_groups.items()}
    }
    lookup_any_item_id_to_name.update(world.item_id_to_name)
    lookup_any_location_id_to_name.update(world.location_id_to_name)

network_data_package = {
    "lookup_any_location_id_to_name": lookup_any_location_id_to_name,  # legacy, to be removed
    "lookup_any_item_id_to_name": lookup_any_item_id_to_name,  # legacy, to be removed
    "version": sum(world.data_version for world in AutoWorldRegister.world_types.values()),
    "games": games,
}

import json
with open("datapackagegroups.json", "w") as f:
    json.dump(network_data_package, f, indent=4)
