from BaseClasses import Location
from .Data import get_data


class PokemonEmeraldLocation(Location):
    game: str = "Pokemon Emerald"
    id: int
    default_item_id: int

    def __init__(self, player: int, name: str, default_item_id: int, id: int, address: int, parent):
        super().__init__(player, name, address, parent)
        self.id = id
        self.default_item_id = default_item_id


def create_location_name_to_id_map():
    data = get_data()

    map = {}
    for map_data in data.values():
        for item_data in map_data.locations:
            map[item_data.name] = item_data.flag

    return map


def create_locations_with_tags(self, region_map, tags):
    data = get_data()
    tags = set(tags)

    for map_name, map_data in data.items():
        region = region_map[map_name]
        for location_data in [location for location in map_data.locations if len(tags & location.tags) > 0]:
            location = PokemonEmeraldLocation(self.player, location_data.name, location_data.default_item, location_data.flag, location_data.rom_address, region)
            if ("Badge" in location_data.tags):
                print(location)
            region.locations.append(location)
