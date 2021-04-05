import enum

__all__ = {"lookup_any_item_id_to_name",
           "lookup_any_location_id_to_name",
           "network_data_package",
           "Games"}

from .alttp.Items import lookup_id_to_name as alttp
from .hk.Items import lookup_id_to_name as hk
from .factorio import Technologies
lookup_any_item_id_to_name = {**alttp, **hk, **Technologies.lookup_id_to_name}
assert len(alttp) + len(hk) + len(Technologies.lookup_id_to_name) == len(lookup_any_item_id_to_name)
lookup_any_item_name_to_id = {name: id for id, name in lookup_any_item_id_to_name.items()}


from .alttp import Regions
from .hk import Locations
lookup_any_location_id_to_name = {**Regions.lookup_id_to_name, **Locations.lookup_id_to_name,
                                  **Technologies.lookup_id_to_name}
assert len(Regions.lookup_id_to_name) + len(Locations.lookup_id_to_name) + len(Technologies.lookup_id_to_name) == \
       len(lookup_any_location_id_to_name)
lookup_any_location_name_to_id = {name: id for id, name in lookup_any_location_id_to_name.items()}



network_data_package = {"lookup_any_location_id_to_name": lookup_any_location_id_to_name,
                        "lookup_any_item_id_to_name": lookup_any_item_id_to_name,
                        "version": 2}

@enum.unique
class Games(str, enum.Enum):
    HK = "Hollow Knight"
    LTTP = "A Link to the Past"
    Factorio = "Factorio"

