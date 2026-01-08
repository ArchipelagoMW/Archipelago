"""
Provides the default WorldData instance based on the generated data.
"""

from .common import BASE_ID, DATA_VERSION
from .types.world import WorldData
from .regions import region_packs
from .items import single_items_dict, items_dict, items_by_full_name, keyring_items
from .shops import shop_dict, per_shop_locations, global_shop_locations, shop_unlock_by_id, shop_unlock_by_shop, \
    shop_unlock_by_shop_and_id
from .locations import locations_dict, events_dict, locked_locations, pool_locations, location_groups
from .item_pools import item_pools_template
from .prog_items import progressive_chains, progressive_items
from .vars import variable_definitions

static_world_data = WorldData(
    data_version=DATA_VERSION,
    base_id=BASE_ID,
    region_packs=region_packs,
    locations_dict=locations_dict,
    events_dict=events_dict,
    locked_locations=locked_locations,
    pool_locations=pool_locations,
    location_groups=location_groups,
    single_items_dict=single_items_dict,
    items_dict=items_dict,
    items_by_full_name=items_by_full_name,
    keyring_items=keyring_items,
    shops_dict=shop_dict,
    per_shop_locations=per_shop_locations,
    global_shop_locations=global_shop_locations,
    shop_unlock_by_id=shop_unlock_by_id,
    shop_unlock_by_shop=shop_unlock_by_shop,
    shop_unlock_by_shop_and_id=shop_unlock_by_shop_and_id,
    item_pools_template=item_pools_template,
    progressive_chains=progressive_chains,
    progressive_items=progressive_items,
    variable_definitions=variable_definitions
)
