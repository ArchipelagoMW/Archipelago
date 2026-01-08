"""
Another utilities file, specifically for things relating to the codegen repository.
"""

import json
import os
import typing
import pkgutil

from BaseClasses import ItemClassification

from .merge import merge

BASE_ID = 3235824000

# I reserve some item IDs at the beginning of our slot for elements
# and other items that don't map to CrossCode items
RESERVED_ITEM_IDS = 100

DYNAMIC_ITEM_AREA_OFFSET = 100000

NUM_ITEMS = 676

GENERATED_COMMENT = """WARNING: THIS FILE HAS BEEN GENERATED!
Modifications to this file will not be kept.
If you need to change something here, check out codegen.py and the templates directory.
"""

def get_json_object(package: str, filename: str) -> typing.Any:
    """
    Opens a json file called `filename` in `package` and returns it deserialized as an object.
    """
    file_bytes: bytes | None = pkgutil.get_data(package, filename)
    if file_bytes is None:
        raise RuntimeError(f"Could not access {filename} in {package}")
    file_obj = json.loads(file_bytes.decode())
    return file_obj


def load_json_with_includes(package: str, filename: str, patch: bool = False) -> dict[str, typing.Any]:
    """
    Load a root json object, including any specified files 
    """
    master: dict[str, typing.Any] = get_json_object(package, filename)
    dirname = os.path.dirname(filename)

    if not isinstance(master, dict): # type: ignore
        raise RuntimeError(f"error loading file '{filename} in {package}': root should be an object")

    if "_comment" in master:
        master.pop("_comment")

    if "_includes" not in master:
        return master

    includes = master.pop("_includes")
    for subfilename in includes:
        subfile = load_json_with_includes(package, os.path.join(dirname, subfilename), patch)

        if "_global" in subfile:
            diff = subfile.pop("_global")
            subfile = merge(subfile, diff, patch=True)

        master = merge(master, subfile, patch=False)

    return master


def get_item_classification(item: dict[str, typing.Any]) -> ItemClassification:
    """Deduce the classification of an item based on its item-database entry"""
    if item["type"] == "CONS" or item["type"] == "TRADE":
        return ItemClassification.filler
    if item["type"] == "KEY":
        return ItemClassification.progression
    if item["type"] == "EQUIP":
        return ItemClassification.progression_skip_balancing
    if item["type"] == "TOGGLE":
        if "Booster" in item["name"]["en_US"]:
            return ItemClassification.progression
        return ItemClassification.filler
    raise RuntimeError(f"I don't know how to classify this item: {item['name']}")
