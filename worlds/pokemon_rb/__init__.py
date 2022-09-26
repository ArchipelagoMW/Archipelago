from typing import TextIO
import os
import logging

from BaseClasses import Item, MultiWorld, Tutorial
from Fill import fill_restrictive, FillError
from .items import item_table, filler_items
from .locations import get_locations, PokemonRBLocation
from ..AutoWorld import World, WebWorld
from .regions import create_regions
from .logic import PokemonLogic
from .options import pokemon_rb_options
from .rom_addresses import rom_addresses
from .text import encode_text
from .rom import generate_output, get_base_rom_bytes, get_base_rom_path, process_pokemon_data, process_wild_pokemon,\
    process_static_pokemon

import worlds.pokemon_rb.poke_data as poke_data


class PokemonWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokemon Red and Blue with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
    )]


class PokemonRedBlueWorld(World):
    """Pokémon Red and Pokémon Blue introduce legions of gamers to the world of Kanto, where the likes of Charmander,
    Pikachu, and Mewtwo were first discovered. Through exciting exploration, battles, and trades, Trainers are able to
    access 150 Pokémon."""
    game = "Pokemon Red - Blue"
    option_definitions = pokemon_rb_options
    remote_items = False
    data_version = 1
    topology_present = False

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in get_locations() if location.type == "Item"}
    item_name_groups = {}

    web = PokemonWebWorld()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.fly_map = None
        self.fly_map_code = None
        self.extra_badges = {}
        self.type_chart = None
        self.local_poke_data = None
        self.learnsets = None
        self.trainer_name = None
        self.rival_name = None

    @classmethod
    def stage_assert_generate(cls, world):
        versions = set()
        for player in world.player_ids:
            if world.worlds[player].game == "Pokemon Red - Blue":
                versions.add(world.game_version[player].current_key)
        for version in versions:
            if not os.path.exists(get_base_rom_path(version)):
                raise FileNotFoundError(get_base_rom_path(version))

    def generate_early(self):
        def encode_name(name, t):
            try:
                if len(encode_text(name)) > 7:
                    raise IndexError(f"{t} name too long for player {self.world.player_name[self.player]}. Must be 7 characters or fewer.")
                return encode_text(name, length=8, whitespace="@", safety=True)
            except KeyError as e:
                raise KeyError(f"Invalid character(s) in {t} name for player {self.world.player_name[self.player]}") from e
        self.trainer_name = encode_name(self.world.trainer_name[self.player].value, "Player")
        self.rival_name = encode_name(self.world.rival_name[self.player].value, "Rival")

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

    def create_items(self) -> None:
        locations = [location for location in get_locations(self.player) if location.type == "Item"]
        item_pool = []
        for location in locations:
            if "Hidden" in location.name and not self.world.randomize_hidden_items[self.player].value:
                continue
            if "Rock Tunnel B1F" in location.region and not self.world.extra_key_items[self.player].value:
                continue
            if location.name == "Celadon City - Mansion Lady" and not self.world.tea[self.player].value:
                continue
            item = self.create_item(location.original_item)
            if location.event:
                self.world.get_location(location.name, self.player).place_locked_item(item)
            elif ("Badge" not in item.name or self.world.badgesanity[self.player].value) and \
                    (item.name != "Oak's Parcel" or self.world.old_man[self.player].value != 1):
                item_pool.append(item)
        self.world.random.shuffle(item_pool)

        self.world.itempool += item_pool

        process_pokemon_data(self)  # strange place for this, but it is the only place that works

    def pre_fill(self):

        process_wild_pokemon(self)
        process_static_pokemon(self)

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
        local_locs = ["Pallet Town - Player's PC", "Fossil - Choice A", "Fossil - Choice B"]
        player_items = []
        for item in self.world.itempool:
            if item.player == self.player:
                player_items.append(item)
        self.world.random.shuffle(player_items)
        for location_name in local_locs:
            location = self.world.get_location(location_name, self.player)
            if location.item is None:
                location.place_locked_item(player_items[0])
                self.world.itempool.remove(player_items.pop(0))
        if not self.world.badgesanity[self.player].value:
            for i in range(5):
                try:
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
                    fill_restrictive(self.world, state, badgelocs.copy(), badges.copy(), True, True)
                except FillError:
                    for location in badgelocs:
                        location.item = None
                    continue
                break
            else:
                raise FillError(f"Failed to place badges for player {self.player}")
        intervene = False
        test_state = self.world.get_all_state(False)
        if not test_state.pokemon_rb_can_surf(self.player) or not test_state.pokemon_rb_can_strength(self.player):
            intervene = True
        elif self.world.accessibility[self.player].current_key != "minimal":
            if not test_state.pokemon_rb_can_cut(self.player) or not test_state.pokemon_rb_can_flash(self.player):
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
        if self.world.randomize_type_matchup_types[self.player].value or \
                self.world.randomize_type_matchup_type_effectiveness[self.player].value:
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
