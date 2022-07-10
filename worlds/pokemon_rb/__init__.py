from typing import Dict, List, Set, Tuple, TextIO

from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from .items import item_table, filler_items
from .locations import get_locations
from ..AutoWorld import World, WebWorld
from .regions import create_regions
from .logic import PokemonLogic
from .options import pokemon_rb_options
from .extracted_data import rom_addresses


class PokemonRedBlueWorld(World):
    """Pokemon"""
    game = "Pokemon Red and Blue"
    options = pokemon_rb_options
    remote_items = True
    data_version = 0
    topology_present = True

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in get_locations()}
    item_name_groups = {}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.fly_map = None
        self.fly_map_code = None

    def generate_basic(self) -> None:
        locations = get_locations(self.player)
        item_pool = []
        badgelocs = []
        badges = []
        for location in locations:
            item = self.create_item(location.original_item)
            if location.event:
                self.world.get_location(location.name, self.player).place_locked_item(item)
            elif "Badge" in item.name and self.world.randomize_badges[self.player] != 2:
                if self.world.randomize_badges[self.player] != 2:
                    badgelocs.append(self.world.get_location(location.name, self.player))
                    badges.append(item)
            else:
                item_pool.append(item)
        self.world.itempool += item_pool
        if self.world.randomize_badges[self.player].value == 0:
            for item, location in zip(badges, badgelocs):
                location.place_locked_item(item)
                location.address = None
        elif self.world.randomize_badges[self.player].value == 1:
            state = self.world.get_all_state(False)
            from Fill import fill_restrictive
            fill_restrictive(self.world, state, badgelocs, badges, True, True)

    def create_regions(self):
        if self.world.free_fly_location[self.player].value:
            fly_map_code = self.world.random.randint(3 if self.world.routing[self.player].value else 1, 9)
            if fly_map_code == 9:
                fly_map_code = 10
        else:
            fly_map_code = 0
        fly_list = ["Pallet Town", "Viridian City", "Pewter City", "Cerulean City", "Lavender Town", "Vermilion City",
                    "Celadon City", "Fuchsia City", "Cinnabar Island", "Indigo Plateau", "Saffron City"]
        self.fly_map = fly_list[fly_map_code]
        self.fly_map_code = fly_map_code
        create_regions(self.world, self.player)
        self.world.completion_condition[self.player] = lambda state, player=self.player: state.can_reach("Indigo Plateau", player=player)

    def create_item(self, name: str) -> Item:
        return PokemonRBItem(name, self.player)

    def generate_output(self, output_directory: str):
        with open("c:\\src\\pokered\\pokeblue.gbc", "br") as file:
           data = bytearray(file.read())
        for region in self.world.regions:
            for location in region.locations:
                if location.rom_address:
                    if "Gym - Badge" in location.name:
                        if self.world.badges[self.player].value != 2:
                            badge_instructions = {"Boulder Badge": 0xC6, "Cascade Badge": 0xCE, "Thunder Badge": 0xD6,
                                                  "Rainbow Badge": 0xDE, "Soul Badge": 0xE6, "Marsh Badge": 0xEE,
                                                  "Volcano Badge": 0xF6, "Earth Badge": 0xFE}
                            data[location.rom_address] = badge_instructions[location.item.name]
                    else:
                        data[location.rom_address] = self.item_name_to_id[location.item.name] - 172000000
                    if location.rom_address == rom_addresses['PC_Item'] and location.item.name == "5 Pokeballs":
                        data[location.rom_address] = self.item_name_to_id["Poke Ball"] - 172000000
                        data[rom_addresses['PC_Item_Quantity']] = 5
        data[rom_addresses['Fly_Location']] = self.fly_map_code
        # if self.world.routing[self.player]:
            # patch = bytearray([0x11, 0x1a, 0x00, 0xff, 0x11, 0x1b, 0x00, 0xff, 0x11, 0x04, 0x01, 0xff, 0x11, 0x05, 0x01, 0xff])
            # write_bytes(data, patch, rom_addresses['Option_Seafoam_Exits'])
            # patch = bytearray([0xb3, 0xc7, 0x11, 0x1a, 0xb3, 0xc7, 0x11, 0x1b, 0xa8, 0xc7, 0x11, 0x04, 0xa8, 0xc7, 0x11, 0x05])
            # write_bytes(data, patch, rom_addresses['Option_Seafoam_Entrances'])
        if self.world.badges[self.player].value == 2:
            data[rom_addresses['Options']] &= 1
        if self.world.control_encounters[self.player].value:
            data[rom_addresses['Options']] &= 2
        data[rom_addresses['Option_Badge_Goal']] = self.world.badge_goal[self.player].value - 2
        data[rom_addresses['Option_Viridian_Gym_Badges']] = self.world.badge_goal[self.player].value - 1
        # if self.world.routing[self.player].value:
        #     write_bytes(data, bytearray([item_table['Tea'].id - 172000000, 0x00, 0x00]), rom_addresses['Guard_Drink_List'])
        data[rom_addresses['Option_EXP_Modifier']] = self.world.exp_modifier[self.player].value
        from .data import pokemons
        mons = list(pokemons.values())
        self.world.random.shuffle(mons)
        data[rom_addresses['Title_Mon_First']] = mons.pop()
        for mon in range(0, 16):
            data[rom_addresses['Title_Mons'] + mon] = mons.pop()

        write_bytes(data, self.world.player_name[self.player].encode(), 0xFFF0)
        with open("c:\\src\\pokered\\pokebluep.gbc", "bw") as file:
            file.write(data)

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write('Fly unlocks:                     %s\n' % self.fly_map)


def write_bytes(data, bytes, address):
    for byte in bytes:
        data[address] = byte
        address += 1


class PokemonRBItem(Item):
    game = "Pokemon Red and Blue"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(PokemonRBItem, self).__init__(
            name,
            item_data.classification,
            item_data.id, player
        )
