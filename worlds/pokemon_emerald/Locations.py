import typing
from BaseClasses import Location, Region, Entrance
from .Util import get_data_json

class PokemonEmeraldLocation(Location):
    game: str = "Pokemon Emerald"
    id: int

    def __init__(self, player: int, name: str, id: int, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.id = id

def create_location_name_to_id_map():
    data = get_data_json()

    map = {}
    for item in data["ball_items"]:
        map[item["name"]] = item["flag"]

    return map

def create_ball_item_locations(self, region_map):
    data = get_data_json()

    for item in data["ball_items"]:
        region = region_map[item["map_name"]]
        location = PokemonEmeraldLocation(self.player, item["name"], item["flag"], item["rom_address"], region)
        region.locations.append(location)
