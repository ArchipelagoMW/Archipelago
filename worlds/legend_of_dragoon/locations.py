from dataclasses import dataclass
from .data.shops import shop_locations, ShopType, Shop

SHOP_LOCATION_BASE_ID = 3000000

@dataclass
class ShopLocation:
    name: str
    id: int
    key: str
    slot_index: int
    shop_type: ShopType

SHOP_LOCATIONS = []
current_id = SHOP_LOCATION_BASE_ID

for shop in shop_locations:
    for slot_index in range(shop.slot_count):
        name: str = f"{shop.display_name} - Slot {slot_index + 1}"
        shop_id: int = current_id
        shop_type = shop.shop_type

        SHOP_LOCATIONS.append(ShopLocation(name, shop_id, shop.key, slot_index, shop_type))
        current_id += 1

SHOP_LOCATIONS_BY_KEY = {loc.key: [] for loc in SHOP_LOCATIONS}
for loc in SHOP_LOCATIONS:
    SHOP_LOCATIONS_BY_KEY[loc.key].append(loc)
