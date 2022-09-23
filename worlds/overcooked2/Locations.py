from BaseClasses import Location
from .Overcooked2Levels import Overcooked2Level


class Overcooked2Location(Location):
    game: str = "Overcooked! 2"


oc2_location_name_to_id = dict()
oc2_location_id_to_name = dict()
for level in Overcooked2Level():
    if level.level_id == 36:
        continue  # level 6-6 does not have an item location
    oc2_location_name_to_id[level.location_name_item] = level.level_id
    oc2_location_id_to_name[level.level_id] = level.location_name_item
