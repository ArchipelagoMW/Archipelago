import jsonc
import os
import pickle
import sys
from hash_file import hash_file


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python worlds/lingo/utils/pickle_static_data.py")

        exit()

    folder_path = os.path.join("worlds", "outer_wilds", "shared_static_logic")
    items_path = os.path.join(folder_path, "items.jsonc")
    locations_path = os.path.join(folder_path, "locations.jsonc")
    connections_path = os.path.join(folder_path, "connections.jsonc")

    with open(items_path, "r") as items_file:
        items = jsonc.load(items_file)
    with open(locations_path, "r") as locations_file:
        locations = jsonc.load(locations_file)
    with open(connections_path, "r") as connections_file:
        connections = jsonc.load(connections_file)

    hashes = {
        "ITEMS": hash_file(items_path),
        "LOCATIONS": hash_file(locations_path),
        "CONNECTIONS": hash_file(connections_path),
    }

    pickle_data = {
        "HASHES": hashes,
        "ITEMS": items,
        "LOCATIONS": locations,
        "CONNECTIONS": connections,
    }

    with open(os.path.join(folder_path, "static_logic.pickle"), "wb") as file:
        pickle.dump(pickle_data, file)
