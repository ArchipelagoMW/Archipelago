"""Update data script
This script can be used to assign new ids for the items and locations in the CSV file. It also regenerates the items
based on the resource packs.

To run the script, use `python -m worlds.stardew_valley.scripts.update_data` from the repository root.
"""

import csv
import itertools
from pathlib import Path
from typing import List

from worlds.stardew_valley import LocationData
from worlds.stardew_valley.items import load_item_csv, Group, ItemData
from worlds.stardew_valley.locations import load_location_csv

RESOURCE_PACK_CODE_OFFSET = 5000
script_folder = Path(__file__)


def write_item_csv(items: List[ItemData]):
    with open((script_folder.parent.parent / "data/items.csv").resolve(), "w", newline="") as file:
        writer = csv.DictWriter(file, ["id", "name", "classification", "groups"])
        writer.writeheader()
        for item in items:
            item_dict = {
                "id": item.code_without_offset,
                "name": item.name,
                "classification": item.classification.name,
                "groups": ",".join(sorted(group.name for group in item.groups))
            }
            writer.writerow(item_dict)


def write_location_csv(locations: List[LocationData]):
    with open((script_folder.parent.parent / "data/locations.csv").resolve(), "w", newline="") as file:
        write = csv.DictWriter(file, ["id", "region", "name", "tags"])
        write.writeheader()
        for location in locations:
            location_dict = {
                "id": location.code_without_offset,
                "name": location.name,
                "region": location.region,
                "tags": ",".join(sorted(group.name for group in location.tags))
            }
            write.writerow(location_dict)


if __name__ == "__main__":
    loaded_items = load_item_csv()

    item_counter = itertools.count(max(item.code_without_offset
                                       for item in loaded_items
                                       if Group.RESOURCE_PACK not in item.groups
                                       and item.code_without_offset is not None) + 1)

    resource_pack_counter = itertools.count(max(item.code_without_offset
                                       for item in loaded_items
                                       if Group.RESOURCE_PACK in item.groups
                                       and item.code_without_offset is not None) + 1)
    items_to_write = []
    for item in loaded_items:
        if item.code_without_offset is None:
            if Group.RESOURCE_PACK in item.groups:
                new_code = next(resource_pack_counter)
            else:
                new_code = next(item_counter)
            items_to_write.append(ItemData(new_code, item.name, item.classification, item.groups))
            continue

        items_to_write.append(item)

    write_item_csv(items_to_write)

    loaded_locations = load_location_csv()
    location_counter = itertools.count(max(location.code_without_offset
                                           for location in loaded_locations
                                           if location.code_without_offset is not None) + 1)

    locations_to_write = []
    for location in loaded_locations:
        if location.code_without_offset is None:
            locations_to_write.append(
                LocationData(next(location_counter), location.region, location.name, location.tags))
            continue

        locations_to_write.append(location)

    write_location_csv(locations_to_write)
