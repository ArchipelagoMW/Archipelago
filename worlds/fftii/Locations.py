from BaseClasses import Location
from .data.logic.Requirement import Requirement
from .data.logic import topologies
from .data.locations import all_regions, monster_location_names, location_sort_list, location_sort_list_names


class FinalFantasyTacticsIILocation(Location):
    game = "Final Fantasy Tactics Ivalice Island"
    logic_rule: list[list[str]]

class LocationData:
    name: str
    id: int
    requirements: list[Requirement]
    battle_level: int

    def __init__(self, name: str, id: int, battle_level):
        self.name = name
        self.id = id
        self.battle_level = battle_level

    def __repr__(self):
        return self.name

id = 1

all_locations: list[LocationData] = list()

for region in all_regions:
    for location in region.locations:
        location_data = LocationData(location.name, id, location.battle_level)
        location_data.requirements = location.requirements
        all_locations.append(location_data)
        id += 1

all_monster_locations = []

for monster in monster_location_names:
    location_data = LocationData(monster, id, 0)
    all_locations.append(location_data)
    all_monster_locations.append(location_data)
    id += 1