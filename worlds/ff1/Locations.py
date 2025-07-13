import json
import pkgutil
from typing import Dict, NamedTuple, List, Optional

from BaseClasses import Region, Location, MultiWorld

EventId: Optional[int] = None
CHAOS_TERMINATED_EVENT = 'Terminated Chaos'


class LocationData(NamedTuple):
    name: str
    address: int


class FF1Locations:
    _location_table: List[LocationData] = []
    _location_table_lookup: Dict[str, LocationData] = {}

    def _populate_item_table_from_data(self):
        file = pkgutil.get_data(__name__, "data/locations.json")
        locations = json.loads(file)
        # Hardcode progression and categories for now
        self._location_table = [LocationData(name, code) for name, code in locations.items()]
        self._location_table_lookup = {item.name: item for item in self._location_table}

    def _get_location_table(self) -> List[LocationData]:
        if not self._location_table or not self._location_table_lookup:
            self._populate_item_table_from_data()
        return self._location_table

    def _get_location_table_lookup(self) -> Dict[str, LocationData]:
        if not self._location_table or not self._location_table_lookup:
            self._populate_item_table_from_data()
        return self._location_table_lookup

    def get_location_name_to_address_dict(self) -> Dict[str, int]:
        data = {name: location.address for name, location in self._get_location_table_lookup().items()}
        data[CHAOS_TERMINATED_EVENT] = EventId
        return data

    @staticmethod
    def create_menu_region(player: int, locations: Dict[str, int],
                           rules: Dict[str, List[List[str]]], world: MultiWorld) -> Region:
        menu_region = Region("Menu", player, world)
        for name, address in locations.items():
            location = Location(player, name, address, menu_region)
            ## TODO REMOVE WHEN LOGIC FOR TOFR IS CORRECT
            if "ToFR" in name:
                rules_list = [["Rod", "Cube", "Lute", "Key", "Chime", "Oxyale",
                               "Ship", "Canoe", "Floater", "Canal",
                               "Crown", "Crystal", "Herb", "Tnt", "Adamant", "Slab", "Ruby", "Bottle"]]
                location.access_rule = generate_rule(rules_list, player)
            elif name in rules:
                rules_list = rules[name]
                location.access_rule = generate_rule(rules_list, player)
            menu_region.locations.append(location)

        return menu_region


def generate_rule(rules_list, player):
    def x(state):
        for rule in rules_list:
            current_state = True
            for item in rule:
                if not state.has(item, player):
                    current_state = False
                    break
            if current_state:
                return True
        return False
    return x
