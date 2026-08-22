import json
import os
import sys

# we use absolute imports here because this code will never be run by the apworld,
# and relative imports fail with "attempted relative import with no known parent package"
from items import items_data
from locations import locations_data
from connections import connections_data


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python worlds/nine_sols/utils/serialize_static_data.py")

        exit()

    folder_path = os.path.join("worlds", "nine_sols", "shared_static_logic")

    # these files won't contain comments, but we'll continue using the "jsonc" extension
    # just so this change isn't coupled to any changes in the mod repo
    items_path = os.path.join(folder_path, "items.jsonc")
    locations_path = os.path.join(folder_path, "locations.jsonc")
    connections_path = os.path.join(folder_path, "connections.jsonc")

    with open(items_path, "w") as items_file:
        json.dump(items_data, items_file)
    with open(locations_path, "w") as locations_file:
        json.dump(locations_data, locations_file)
    with open(connections_path, "w") as connections_file:
        json.dump(connections_data, connections_file)
