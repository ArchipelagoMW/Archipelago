from ..AutoWorld import World
from .Items import create_item_name_to_id_map, get_item_classification, PokemonEmeraldItem
from .Rules import set_default_rules
from .Locations import create_location_name_to_id_map, create_locations_with_tags
from .Options import options
from .Rom import generate_output
from .Regions import create_regions
from .SanityCheck import sanity_check


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
        if (sanity_check() == False): raise AssertionError("Sanity check failed")

        create_regions(self.multiworld, self.player)
        set_default_rules(self.multiworld, self.player)

        create_locations_with_tags(self.multiworld, self.player, ["GroundItem", "HiddenItem", "Badge", "NpcGift"])


    def create_items(self):
        item_ids = []
        for region in self.multiworld.regions:
            if (region.player == self.player):
                item_ids += [location.default_item_id for location in region.locations]
        
        self.multiworld.itempool += [
            PokemonEmeraldItem(self.item_id_to_name[id], get_item_classification(id), id, self.player)
            for id in item_ids
        ]


    def generate_output(self, output_directory: str):
        generate_output(self.multiworld, self.player, output_directory)


    def fill_slot_data(self):
        slot_data = self._get_pokemon_emerald_data()
        for option_name in options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data
