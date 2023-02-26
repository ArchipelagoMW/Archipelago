from ..AutoWorld import World
from .Items import PokemonEmeraldItem, create_item_label_to_id_map, get_item_classification
from .Locations import create_location_label_to_id_map, create_locations_with_tags
from .Options import options
from .Regions import create_regions
from .Rom import generate_output
from .Rules import set_default_rules
from .SanityCheck import sanity_check


class PokemonEmeraldWorld(World):
    """
    Desc
    """
    game: str = "Pokemon Emerald"
    option_definitions = options
    topology_present = True

    item_name_to_id = create_item_label_to_id_map()
    location_name_to_id = create_location_label_to_id_map()

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
        create_locations_with_tags(self.multiworld, self.player, ["OverworldItem", "HiddenItem", "Badge", "NpcGift", "HM", "KeyItem", "Rod"])
        set_default_rules(self.multiworld, self.player)


    def generate_basic(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)


    def create_items(self):
        item_ids = []
        for region in self.multiworld.regions:
            if (region.player == self.player):
                item_locations = [location for location in region.locations if not location.id == None] # Filter events
                item_ids += [location.default_item_id for location in item_locations]

        for item_id in item_ids:
            self.multiworld.itempool.append(PokemonEmeraldItem(
                self.item_id_to_name[item_id],
                get_item_classification(item_id),
                item_id,
                self.player
            ))


    def generate_output(self, output_directory: str):
        generate_output(self.multiworld, self.player, output_directory)


    def fill_slot_data(self):
        slot_data = self._get_pokemon_emerald_data()
        for option_name in options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data
