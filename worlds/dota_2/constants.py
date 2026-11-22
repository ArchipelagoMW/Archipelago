import json
from importlib import resources

# Ids of these items in data/ids.json
DOTA2_BASE_ID = 770_1540

PROGRESSIVE_GROUP_UNLOCK_ID = DOTA2_BASE_ID
PRIMORDIAL_FRAGMENT_ID = DOTA2_BASE_ID + 1
FILLER_ITEM_ID = DOTA2_BASE_ID + 2
# Most hero groups a seed can have (option hero_groups). Groups past the original 7 have their locations at the end.
MAX_HERO_GROUPS = 30
ORIGINAL_HERO_GROUPS = 7


def world_version() -> str:
    """This apworld's version (archipelago.json), sent in slot_data so the client can tell an older seed."""
    with resources.files(__package__).joinpath("archipelago.json").open("r", encoding="utf-8") as f:
        return json.load(f)["world_version"]
