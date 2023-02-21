from BaseClasses import Region, Entrance
from ..AutoWorld import World
from .Items import create_item_name_to_id_map, get_item_classification, PokemonEmeraldItem
from .Locations import create_location_name_to_id_map, create_locations_with_tags
from .Options import options
from .Rom import generate_output
from .Data import get_regions_data, get_warp_destination_region_name

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
        regions = {}
        regions_data = get_regions_data()

        for region_name, region_data in regions_data.items():
            region = Region(region_name, self.player, self.multiworld)
            warp_destinations = [get_warp_destination_region_name(warp) for warp in region_data.warps]
            warp_destinations = [destination for destination in warp_destinations if not destination == None]
            exit_names = set(region_data.exits + warp_destinations)
            for exit_name in exit_names:
                connection = Entrance(self.player, exit_name, region)
                region.exits.append(connection)
            
            regions[region_name] = region

        for region in regions.values():
            for connection in region.exits:
                connection.connect(regions[connection.name])

        menu = Region("Menu", self.player, self.multiworld)
        connection = Entrance(self.player, "New Game", menu)
        menu.exits.append(connection)
        connection.connect(regions["REGION_LITTLEROOT_TOWN"])
        regions["Menu"] = menu

        create_locations_with_tags(self, regions, ["GroundItem", "HiddenItem", "Badge", "NpcGift"])
        self.multiworld.regions += regions.values()


    def create_items(self):
        item_ids = []
        for region in self.multiworld.regions:
            if (region.player == self.player):
                item_ids += [location.default_item_id for location in region.locations]
        
        self.multiworld.itempool += [
            PokemonEmeraldItem(self.item_id_to_name[id], get_item_classification(id), id, self.player)
            for id in item_ids
        ]


    def fill_slot_data(self):
        slot_data = self._get_pokemon_emerald_data()
        for option_name in options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data


    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)
