import typing
from BaseClasses import Location
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
    for item in data["hidden_items"]:
        map[item["name"]] = item["flag"]

    return map


def create_badge_locations(self, region_map):
    data = get_data_json()

    badge_items_address = data["misc_rom_addresses"]["gGymBadgeItems"]
    region_map["MAP_RUSTBORO_CITY_GYM"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Stone Badge",
        data["constants"]["items"]["ITEM_BADGE_1"],
        badge_items_address + 0,
        region_map["MAP_RUSTBORO_CITY_GYM"]
    ))
    region_map["MAP_DEWFORD_TOWN_GYM"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Knuckle Badge",
        data["constants"]["items"]["ITEM_BADGE_2"],
        badge_items_address + 2,
        region_map["MAP_DEWFORD_TOWN_GYM"]
    ))
    region_map["MAP_MAUVILLE_CITY_GYM"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Dynamo Badge",
        data["constants"]["items"]["ITEM_BADGE_3"],
        badge_items_address + 4,
        region_map["MAP_MAUVILLE_CITY_GYM"]
    ))
    region_map["MAP_LAVARIDGE_TOWN_GYM_1F"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Heat Badge",
        data["constants"]["items"]["ITEM_BADGE_4"],
        badge_items_address + 6,
        region_map["MAP_LAVARIDGE_TOWN_GYM_1F"]
    ))
    region_map["MAP_PETALBURG_CITY_GYM"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Balance Badge",
        data["constants"]["items"]["ITEM_BADGE_5"],
        badge_items_address + 8,
        region_map["MAP_PETALBURG_CITY_GYM"]
    ))
    region_map["MAP_FORTREE_CITY_GYM"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Feather Badge",
        data["constants"]["items"]["ITEM_BADGE_6"],
        badge_items_address + 10,
        region_map["MAP_FORTREE_CITY_GYM"]
    ))
    region_map["MAP_MOSSDEEP_CITY_GYM"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Mind Badge",
        data["constants"]["items"]["ITEM_BADGE_7"],
        badge_items_address + 12,
        region_map["MAP_MOSSDEEP_CITY_GYM"]
    ))
    region_map["MAP_SOOTOPOLIS_CITY_GYM_1F"].locations.append(PokemonEmeraldLocation(
        self.player,
        "Rain Badge",
        data["constants"]["items"]["ITEM_BADGE_8"],
        badge_items_address + 14,
        region_map["MAP_SOOTOPOLIS_CITY_GYM_1F"]
    ))


def create_ball_item_locations(self, region_map):
    data = get_data_json()

    for item in data["ball_items"]:
        region = region_map[item["map_name"]]
        location = PokemonEmeraldLocation(self.player, item["name"], item["flag"], item["rom_address"], region)
        region.locations.append(location)


def create_hidden_item_locations(self, region_map):
    data = get_data_json()

    for item in data["hidden_items"]:
        region = region_map[item["map_name"]]
        location = PokemonEmeraldLocation(self.player, item["name"], item["flag"], item["rom_address"], region)
        region.locations.append(location)
