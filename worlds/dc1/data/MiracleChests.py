import json
import pkgutil
from typing import List

from worlds.dc1 import DarkCloudItem, DarkCloudLocation

locations = json.loads(pkgutil.get_data(__name__, "miracle_locations.json").decode())

def create_miracle_items() -> List["DarkCloudItem"]:
    items = []



    return items

def create_norune_mc_locs() -> List[DarkCloudLocation]:
    mc_locations = []

    norune_locs = locations[0]

    return mc_locations