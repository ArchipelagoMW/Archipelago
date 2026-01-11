from typing import Dict, Set

from .data import data

item_groups: Dict[str, Set[str]] = {}
location_groups: Dict[str, Set[str]] = {}

for item in data.items.values():
    for tag in item.tags:
        if tag not in item_groups:
            item_groups[tag] = set()
        item_groups[tag].add(item.name)

for location in data.locations.values():
    for tag in location.tags:
        if tag not in location_groups:
            location_groups[tag] = set()
        location_groups[tag].add(location.name)
