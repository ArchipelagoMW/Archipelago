from BaseClasses import Location
from .Overcooked2Levels import Overcooked2Level, Overcooked2GameWorld


class Overcooked2Location(Location):
    game: str = "Overcooked! 2"


location_name_to_id = dict()
location_id_to_name = dict()
for level in Overcooked2Level():
    if level.world == Overcooked2GameWorld.KEVIN:
        continue # kevin levels currently do not have item locations
    if level.level_id() == 36:
        continue # level 6-6 does not have an item location
    location_name_to_id[level.location_name_completed()] = level.level_id()
    location_id_to_name[level.level_id()] = level.location_name_completed()
