from . import Locations
from . import Items

BASE_ID = 6000

item_name_to_id = {name: index + BASE_ID for index, name in enumerate(Items.item_table)}
location_name_to_id = {name: index + BASE_ID for index, name in enumerate(Locations.location_table)}
