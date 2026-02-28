from typing import Dict, NamedTuple, Optional
import re

from BaseClasses import Location
from .archi_defs import loc_data_table
from .Regions import region_data_table

bl2_base_id: int = 2388000

class Borderlands2Location(Location):
    game = "Borderlands 2"


# class Borderlands2LocationData(NamedTuple):
#     region: str
#     address: Optional[int] = None
#     description: Optional[str] = None

# def get_region_from_loc_name(loc_name):
#     exception_loc = region_exceptions.get(loc_name)
#     if exception_loc is not None:
#         return exception_loc

#     pieces = re.split(r'[ :]', loc_name)

#     if len(pieces) <= 2:
#         return "Sanctuary"

#     second_word = pieces[1]
#     if second_word in region_data_table.keys():
#         return second_word

#     # variant_translation = region_name_variants.get(second_word)
#     # if variant_translation in region_data_table.keys():
#     #     return variant_translation

#     print("didn't find region for loc: " + loc_name)
#     return "AridNexusBoneyard"


# location_data_table: Dict[str, Borderlands2LocationData] = {
#     name: Borderlands2LocationData(region=get_region_from_loc_name(name), address=bl2_base_id + loc_id, description="")
#     for name, loc_id in loc_name_to_id.items()
# }

location_data_table = loc_data_table

start_id = bl2_base_id + 1

location_name_to_id = {name: start_id + i for i, name in enumerate(loc_data_table.keys())}
location_descriptions = {name: data.description for name, data in loc_data_table.items()}
