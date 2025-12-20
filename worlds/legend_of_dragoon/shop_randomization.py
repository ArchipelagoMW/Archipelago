from random import Random, choice
from typing import Dict

from . import ITEMS
from .locations import SHOP_LOCATIONS, ShopLocation
from .ap.ap_items import AP_ITEM_POOL, APItem

ShopAssignment = Dict[int, APItem]

def generate_shop_randomization(rng: Random) -> ShopAssignment:
    assignments: ShopAssignment = {}

    available_items = AP_ITEM_POOL.copy()
    rng.shuffle(available_items)

    for i in range(len(available_items), len(SHOP_LOCATIONS)):
        available_items.append(choice(ITEMS))

    print(f"total locations: {len(SHOP_LOCATIONS)}")
    if len(available_items) < len(SHOP_LOCATIONS):
        raise ValueError(f"Not enough AP items({len(available_items)}) for shop slots({len(SHOP_LOCATIONS)})")

    for location, item in zip(SHOP_LOCATIONS, available_items):
        assignments[location.id] = item

    return assignments

def get_item_for_shop_location(
        assignments: ShopAssignment,
        location_id: int,
) -> APItem:
    return assignments[location_id]