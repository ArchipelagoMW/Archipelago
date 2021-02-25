__all__ = {"lookup_any_item_id_to_name",
           "lookup_any_location_id_to_name"}

from .alttp.Items import lookup_id_to_name as alttp
from .hk.Items import lookup_id_to_name as hk
lookup_any_item_id_to_name = {**alttp, **hk}


from .alttp import Regions
from .hk import Locations
lookup_any_location_id_to_name = {**Regions.lookup_id_to_name, **Locations.lookup_id_to_name}

network_data_package = {"lookup_any_location_id_to_name": lookup_any_location_id_to_name,
                        "lookup_any_item_id_to_name": lookup_any_item_id_to_name,
                        "version": 1}
