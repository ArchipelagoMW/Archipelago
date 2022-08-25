from BaseClasses import Location
from .Overcooked2Levels import Overcooked2Level


class Overcooked2Location(Location):
    game: str = "Overcooked! 2"


location_name_to_id = dict()
location_id_to_name = dict()
for level in Overcooked2Level():
    location_name_to_id[level.location_name_completed()] = level.level_id()
    location_name_to_id[level.level_id()] = level.location_name_completed()
