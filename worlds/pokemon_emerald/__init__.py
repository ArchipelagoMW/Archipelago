from BaseClasses import Region, Entrance, Item, ItemClassification
from .Items import PokemonEmeraldItem, item_table, required_items
from .Locations import PokemonEmeraldLocation, advancement_table, exclusion_table
from .Options import options
from .Rom import generate_output
from ..AutoWorld import World

def create_item_name_to_id():
    map = {
        "Potion": 13,
        "Rare Candy": 68,
    }
    return map

def create_location_name_to_id():
    map = {
        "Route 104: Potion": 1135,
        "Route 104: Hidden Poke Ball": 562,
    }
    return map

class PokemonEmeraldWorld(World):
    """
    Desc
    """
    game: str = "Pokemon Emerald"
    option_definitions = options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}

    data_version = 4

    def _get_pokemon_emerald_data(self):
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'race': self.multiworld.is_race,
        }

    def generate_basic(self):
        # Generate item pool
        itempool = []
        # Add all required progression items
        for (name, num) in required_items.items():
            itempool += [name] * num
        itempool += [self.get_filler_item_name()]
        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]

        self.multiworld.itempool += itempool

    # def set_rules(self):
        # set_rules(self.multiworld, self.player)
        # set_completion_rules(self.multiworld, self.player)

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        game = Region("Game", self.player, self.multiworld)
        game.locations = [PokemonEmeraldLocation(self.player, loc_name, loc_data.rom_address, game)
                           for loc_name, loc_data in advancement_table.items() if loc_data.region == game.name]

        connection = Entrance(self.player, "New Game", menu)
        menu.exits.append(connection)
        connection.connect(game)
        self.multiworld.regions += [menu, game]

    def fill_slot_data(self):
        slot_data = self._get_pokemon_emerald_data()
        for option_name in options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = PokemonEmeraldItem(name,
                                  ItemClassification.progression if item_data.progression else ItemClassification.filler,
                                  item_data.code, self.player)
        return item

    def get_filler_item_name(self) -> str:
        return 'Potion'

    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)