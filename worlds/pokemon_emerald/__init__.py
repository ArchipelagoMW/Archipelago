from BaseClasses import Region, Entrance
from .Items import create_item_name_to_id_map, create_ball_items, create_hidden_items, create_badge_items
from .Locations import create_location_name_to_id_map, create_ball_item_locations, create_hidden_item_locations, create_badge_locations
from .Options import options
from .Rom import generate_output
from .Util import get_data_json
from ..AutoWorld import World

class PokemonEmeraldWorld(World):
    """
    Desc
    """
    game: str = "Pokemon Emerald"
    option_definitions = options
    topology_present = True

    item_name_to_id = create_item_name_to_id_map()
    location_name_to_id = create_location_name_to_id_map()

    data_version = 4

    def _get_pokemon_emerald_data(self):
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'race': self.multiworld.is_race,
        }

    def create_regions(self):
        region_map = {}
        data = get_data_json()

        for map in data["maps"]:
            region = Region(map["name"], self.player, self.multiworld)
            exit_names = set([map_name for map_name in map["connections"]] + [map_name for map_name in map["warps"]])
            for exit_name in exit_names:
                connection = Entrance(self.player, exit_name, region)
                region.exits.append(connection)
            
            region_map[map["name"]] = region

        for region in region_map.values():
            for connection in region.exits:
                connection.connect(region_map[connection.name])

        menu = Region("Menu", self.player, self.multiworld)
        connection = Entrance(self.player, "New Game", menu)
        menu.exits.append(connection)
        connection.connect(region_map["MAP_LITTLEROOT_TOWN"])
        region_map["Menu"] = menu

        create_ball_item_locations(self, region_map)
        create_hidden_item_locations(self, region_map)
        create_badge_locations(self, region_map)
        self.multiworld.regions += region_map.values()

    def create_items(self):
        self.multiworld.itempool += create_ball_items(self)
        self.multiworld.itempool += create_hidden_items(self)
        self.multiworld.itempool += create_badge_items(self)

    def fill_slot_data(self):
        slot_data = self._get_pokemon_emerald_data()
        for option_name in options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)
