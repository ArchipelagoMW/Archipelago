from dataclasses import dataclass, field

from .items import ItemData, ProgressiveItemChain, SingleItemData, ItemPoolEntry
from .locations import LocationData
from .regions import RegionsData
from .shops import ShopData
from .condition import Condition

@dataclass
class WorldData:
    data_version: str
    base_id: int

    # regions.py
    region_packs: dict[str, RegionsData]
    modes: list[str] = field(init=False)

    # locations.py
    locations_dict: dict[str, LocationData]
    events_dict: dict[str, LocationData]
    locked_locations: set[int]
    pool_locations: list[LocationData]
    location_groups: dict[str, set[LocationData]]

    # items.py
    single_items_dict: dict[str, SingleItemData]
    items_dict: dict[tuple[str, int], ItemData]
    items_by_full_name: dict[str, ItemData]
    keyring_items: set[str]

    # shops.py
    shops_dict: dict[str, ShopData]
    per_shop_locations: dict[str, dict[int, LocationData]]
    global_shop_locations: dict[int, LocationData]
    shop_unlock_by_id: dict[int, ItemData]
    shop_unlock_by_shop: dict[str, ItemData]
    shop_unlock_by_shop_and_id: dict[tuple[str, int], ItemData]

    # item_pools.py
    item_pools_template: dict[str, list[ItemPoolEntry]]

    # prog_items.py
    progressive_chains: dict[str, ProgressiveItemChain]
    progressive_items: dict[str, ItemData]

    # vars.py
    variable_definitions: dict[str, dict[str, list[Condition]]]

    def __post_init__(self):
        self.modes = list(self.region_packs.keys())
