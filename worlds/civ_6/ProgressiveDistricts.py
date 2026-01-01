from typing import Dict, List, Optional

from .Data import get_progressive_districts_data

_flat_progressive_districts: Optional[Dict[str, str]] = {}


def get_flat_progressive_districts() -> Dict[str, str]:
    """Returns a dictionary of all items that are associated with a progressive item.
    Key is the item name ("TECH_WRITING") and the value is the associated progressive
    item ("PROGRESSIVE_CAMPUS")"""
    if _flat_progressive_districts:
        return _flat_progressive_districts

    progressive_districts = get_progressive_districts_data()
    flat_progressive_districts: Dict[str, str] = {}
    for key, value in progressive_districts.items():
        for item in value:
            flat_progressive_districts[item] = key
    return flat_progressive_districts


def convert_items_to_progressive_items(items: List[str]):
    """converts a list of items to instead be their associated progressive item if
    they have one. ["TECH_MINING", "TECH_WRITING"] -> ["TECH_MINING", "PROGRESSIVE_CAMPUS]
    """
    flat_progressive_districts = get_flat_progressive_districts()
    return [flat_progressive_districts.get(item, item) for item in items]


def convert_item_to_progressive_item(item: str):
    """converts an items to instead be its associated progressive item if
    it has one. "TECH_WRITING" ->  "PROGRESSIVE_CAMPUS"""
    flat_progressive_districts = get_flat_progressive_districts()
    return flat_progressive_districts.get(item, item)
