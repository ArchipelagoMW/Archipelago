from typing import Dict, List, Set, Tuple, TextIO

from BaseClasses import Item, MultiWorld, ItemClassification
from .items import item_table, filler_items
from .locations import get_locations, PokemonRBLocation
from ..AutoWorld import World, WebWorld
from .regions import create_regions
from .logic import PokemonLogic
from .options import pokemon_rb_options
from .rom_addresses import rom_addresses
from .text import encode_text
from .rom import generate_output, get_base_rom_bytes, get_base_rom_path, generate_basic
import worlds.pokemon_rb.poke_data as poke_data
import logging


class PokemonRedBlueWorld(World):
    """Pokemon"""
    game = "Pokemon Red - Blue"
    option_definitions = pokemon_rb_options
    remote_items = False
    data_version = 0
    topology_present = False

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in get_locations() if location.type == "Item"}
    item_name_groups = {}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.fly_map = None
        self.fly_map_code = None
        self.extra_badges = {}
        self.type_chart = None
        self.local_poke_data = None
        self.learnsets = None

    def generate_early(self):
        if self.world.badges_needed_for_hm_moves[self.player].value >= 2:
            badges_to_add = ["Soul Badge", "Volcano Badge", "Earth Badge"]
            if self.world.badges_needed_for_hm_moves[self.player].value == 3:
                for _ in range(0, 2):
                    badges_to_add.append(self.world.random.choice(["Boulder Badge", "Cascade Badge", "Thunder Badge",
                                                                   "Rainbow Badge", "Marsh Badge",   "Soul Badge",
                                                                   "Volcano Badge", "Earth Badge"]))
            hm_moves = ["Cut", "Fly", "Surf", "Strength", "Flash"]
            self.world.random.shuffle(hm_moves)
            self.extra_badges = {}
            for badge in badges_to_add:
                self.extra_badges[hm_moves.pop()] = badge

    def generate_basic(self) -> None:
        generate_basic(self)


    def create_items(self) -> None:
        locations = [location for location in get_locations(self.player) if location.type == "Item"]
        item_pool = []
        badgelocs = []
        badges = []
        for location in locations:
            if "Hidden" in location.name and not self.world.randomize_hidden_items[self.player].value:
                continue
            if "Rock Tunnel B1F" in location.region and not self.world.extra_key_items[self.player].value:
                continue
            item = self.create_item(location.original_item)
            if location.event:
                self.world.get_location(location.name, self.player).place_locked_item(item)
            elif ("Badge" not in item.name or self.world.badgesanity[self.player]) and \
                    (item.name != "Oak's Parcel" or self.world.old_man[self.player] != 1):
                #badgelocs.append(self.world.get_location(location.name, self.player))
                #badges.append(item)
            #else:
                item_pool.append(item)

        # self.world.random.shuffle(item_pool)
        # if self.world.extra_key_items[self.player].value:
        #     for item_name in ["Plant Key", "Mansion Key", "Hideout Key", "Safari Pass"]:
        #         item = self.create_item(item_name)
        #         for i, old_item in enumerate(item_pool):
        #             if old_item.classification == ItemClassification.filler:
        #                 item_pool[i] = item
        #                 break
        self.world.random.shuffle(item_pool)

        self.world.itempool += item_pool


    def pre_fill(self):

        if self.world.old_man[self.player].value == 1:
            item = self.create_item("Oak's Parcel")
            locations = []
            for location in self.world.get_locations():
                if location.player == self.player \
                        and location.item is None \
                        and location.can_reach(self.world.state):
                    locations.append(location)
            self.world.random.shuffle(locations)
            location = locations.pop()
            location.place_locked_item(item)
        location = self.world.get_location("Pallet Town - Player's PC", self.player)
        if location.item is None:
            player_items = []
            for item in self.world.itempool:
                if item.player == self.player:
                    player_items.append(item)
            self.world.random.shuffle(player_items)
            location.place_locked_item(player_items[0])
            self.world.itempool.remove(player_items[0])
        if not self.world.badgesanity[self.player].value:
            badges = []
            badgelocs = []
            for badge in ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge",
                          "Marsh Badge", "Volcano Badge", "Earth Badge"]:
                badges.append(self.create_item(badge))
            for loc in ["Pewter Gym - Brock 1", "Cerulean Gym - Misty 1", "Vermilion Gym - Lt. Surge 1",
                          "Celadon Gym - Erika 1", "Fuchsia Gym - Koga 1", "Saffron Gym - Sabrina 1",
                          "Cinnabar Gym - Blaine 1", "Viridian Gym - Giovanni 1"]:
                badgelocs.append(self.world.get_location(loc, self.player))
            state = self.world.get_all_state(False)
            self.world.random.shuffle(badges)
            self.world.random.shuffle(badgelocs)
            from Fill import fill_restrictive
            fill_restrictive(self.world, state, badgelocs, badges, True, True)

        intervene = False
        test_state = self.world.get_all_state(False)
        if not self.world.has_beaten_game(test_state, self.player):
            intervene = True
        elif self.world.accessibility[self.player].current_key != "minimal":
            if not self.world.get_location("Cinnabar Island - Lab Scientist", self.player).can_reach(test_state) or \
                    not self.world.get_location("Route 2 - North Item", self.player).can_reach(test_state):
                intervene = True
        if intervene:
            logging.warning(
                f"HM-compatible Pokémon possibly missing, placing Mew on Route 1 for player {self.player}")
            loc = self.world.get_location("Route 1 - Wild Pokemon - 1", self.player)
            loc.item = self.create_item("Mew")

    def create_regions(self):
        if self.world.free_fly_location[self.player].value:
            fly_map_code = self.world.random.randint(5, 9)
            if fly_map_code == 9:
                fly_map_code = 10
            if fly_map_code == 5:
                fly_map_code = 4
        else:
            fly_map_code = 0
        self.fly_map = ["Pallet Town", "Viridian City", "Pewter City", "Cerulean City", "Lavender Town",
                        "Vermilion City", "Celadon City", "Fuchsia City", "Cinnabar Island", "Indigo Plateau",
                        "Saffron City"][fly_map_code]
        self.fly_map_code = fly_map_code
        create_regions(self.world, self.player)
        self.world.completion_condition[self.player] = lambda state, player=self.player: state.has("Become Champion", player=player)

    def create_item(self, name: str) -> Item:
        return PokemonRBItem(name, self.player)

    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)

    def write_spoiler_header(self, spoiler_handle: TextIO):
        if self.world.free_fly_location[self.player].value:
            spoiler_handle.write('Fly unlocks:                     %s\n' % self.fly_map)
        if self.extra_badges:
            for hm_move, badge in self.extra_badges.items():
                spoiler_handle.write(hm_move + " enabled by: " + (" " * 20)[:20 - len(hm_move)] + badge + "\n")

    def write_spoiler(self, spoiler_handle):
        if self.world.randomize_type_matchup_attacking_types[self.player].value or \
                self.world.randomize_type_matchup_defending_types[self.player].value:
            spoiler_handle.write("\n\nType matchups:\n\n")
            for matchup in self.type_chart:
                spoiler_handle.write(f"{matchup[0]} deals {matchup[2] * 10}% damage to {matchup[1]}\n")


class PokemonRBItem(Item):
    game = "Pokemon Red - Blue"
    type = None
    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(PokemonRBItem, self).__init__(
            name,
            item_data.classification,
            item_data.id, player
        )
