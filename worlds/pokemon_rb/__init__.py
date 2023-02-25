from typing import TextIO
import os
import logging
from copy import deepcopy

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from Fill import fill_restrictive, FillError, sweep_from_pool
from ..AutoWorld import World, WebWorld
from ..generic.Rules import add_item_rule
from .items import item_table, item_groups
from .locations import location_data, PokemonRBLocation
from .regions import create_regions
from .logic import PokemonLogic
from .options import pokemon_rb_options
from .rom_addresses import rom_addresses
from .text import encode_text
from .rom import generate_output, get_base_rom_bytes, get_base_rom_path, process_pokemon_data, process_wild_pokemon,\
    process_static_pokemon
from .rules import set_rules

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
    """Pokémon Red and Pokémon Blue are the original monster-collecting turn-based RPGs.  Explore the Kanto region with
    your Pokémon, catch more than 150 unique creatures, earn badges from the region's Gym Leaders, and challenge the
    Elite Four to become the champion!"""
    # -MuffinJets#4559
    game = "Pokemon Red and Blue"
    option_definitions = pokemon_rb_options

    data_version = 5
    required_client_version = (0, 3, 7)

    topology_present = False

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in location_data if location.type == "Item"}
    item_name_groups = item_groups

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
        self.type_chart = None
        self.traps = None

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        versions = set()
        for player in multiworld.player_ids:
            if multiworld.worlds[player].game == "Pokemon Red and Blue":
                versions.add(multiworld.game_version[player].current_key)
        for version in versions:
            if not os.path.exists(get_base_rom_path(version)):
                raise FileNotFoundError(get_base_rom_path(version))

    def generate_early(self):
        def encode_name(name, t):
            try:
                if len(encode_text(name)) > 7:
                    raise IndexError(f"{t} name too long for player {self.multiworld.player_name[self.player]}. Must be 7 characters or fewer.")
                return encode_text(name, length=8, whitespace="@", safety=True)
            except KeyError as e:
                raise KeyError(f"Invalid character(s) in {t} name for player {self.multiworld.player_name[self.player]}") from e
        if self.multiworld.trainer_name[self.player] == "choose_in_game":
            self.trainer_name = "choose_in_game"
        else:
            self.trainer_name = encode_name(self.multiworld.trainer_name[self.player].value, "Player")
        if self.multiworld.rival_name[self.player] == "choose_in_game":
            self.rival_name = "choose_in_game"
        else:
            self.rival_name = encode_name(self.multiworld.rival_name[self.player].value, "Rival")

        if len(self.multiworld.player_name[self.player].encode()) > 16:
            raise Exception(f"Player name too long for {self.multiworld.get_player_name(self.player)}. Player name cannot exceed 16 bytes for Pokémon Red and Blue.")

        if self.multiworld.badges_needed_for_hm_moves[self.player].value >= 2:
            badges_to_add = ["Marsh Badge", "Volcano Badge", "Earth Badge"]
            if self.multiworld.badges_needed_for_hm_moves[self.player].value == 3:
                badges = ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Marsh Badge",
                          "Soul Badge", "Volcano Badge", "Earth Badge"]
                self.multiworld.random.shuffle(badges)
                badges_to_add += [badges.pop(), badges.pop()]
            hm_moves = ["Cut", "Fly", "Surf", "Strength", "Flash"]
            self.multiworld.random.shuffle(hm_moves)
            self.extra_badges = {}
            for badge in badges_to_add:
                self.extra_badges[hm_moves.pop()] = badge

        process_pokemon_data(self)

        if self.multiworld.randomize_type_chart[self.player] == "vanilla":
            chart = deepcopy(poke_data.type_chart)
        elif self.multiworld.randomize_type_chart[self.player] == "randomize":
            types = poke_data.type_names.values()
            matchups = []
            for type1 in types:
                for type2 in types:
                    matchups.append([type1, type2])
            self.multiworld.random.shuffle(matchups)
            immunities = self.multiworld.immunity_matchups[self.player].value
            super_effectives = self.multiworld.super_effective_matchups[self.player].value
            not_very_effectives = self.multiworld.not_very_effective_matchups[self.player].value
            normals = self.multiworld.normal_matchups[self.player].value
            while super_effectives + not_very_effectives + normals < 225 - immunities:
                super_effectives += self.multiworld.super_effective_matchups[self.player].value
                not_very_effectives += self.multiworld.not_very_effective_matchups[self.player].value
                normals += self.multiworld.normal_matchups[self.player].value
            if super_effectives + not_very_effectives + normals > 225 - immunities:
                total = super_effectives + not_very_effectives + normals
                excess = total - (225 - immunities)
                subtract_amounts = (
                    int((excess / (super_effectives + not_very_effectives + normals)) * super_effectives),
                    int((excess / (super_effectives + not_very_effectives + normals)) * not_very_effectives),
                    int((excess / (super_effectives + not_very_effectives + normals)) * normals))
                super_effectives -= subtract_amounts[0]
                not_very_effectives -= subtract_amounts[1]
                normals -= subtract_amounts[2]
                while super_effectives + not_very_effectives + normals > 225 - immunities:
                    r = self.multiworld.random.randint(0, 2)
                    if r == 0:
                        super_effectives -= 1
                    elif r == 1:
                        not_very_effectives -= 1
                    else:
                        normals -= 1
            chart = []
            for matchup_list, matchup_value in zip([immunities, normals, super_effectives, not_very_effectives],
                                                   [0, 10, 20, 5]):
                for _ in range(matchup_list):
                    matchup = matchups.pop()
                    matchup.append(matchup_value)
                    chart.append(matchup)
        elif self.multiworld.randomize_type_chart[self.player] == "chaos":
            types = poke_data.type_names.values()
            matchups = []
            for type1 in types:
                for type2 in types:
                    matchups.append([type1, type2])
            chart = []
            values = list(range(21))
            self.multiworld.random.shuffle(matchups)
            self.multiworld.random.shuffle(values)
            for matchup in matchups:
                value = values.pop(0)
                values.append(value)
                matchup.append(value)
                chart.append(matchup)
        # sort so that super-effective matchups occur first, to prevent dual "not very effective" / "super effective"
        # matchups from leading to damage being ultimately divided by 2 and then multiplied by 2, which can lead to
        # damage being reduced by 1 which leads to a "not very effective" message appearing due to my changes
        # to the way effectiveness messages are generated.
        self.type_chart = sorted(chart, key=lambda matchup: -matchup[2])

    def create_items(self) -> None:
        start_inventory = self.multiworld.start_inventory[self.player].value.copy()
        if self.multiworld.randomize_pokedex[self.player] == "start_with":
            start_inventory["Pokedex"] = 1
            self.multiworld.push_precollected(self.create_item("Pokedex"))
        locations = [location for location in location_data if location.type == "Item"]
        item_pool = []
        for location in locations:
            if not location.inclusion(self.multiworld, self.player):
                continue
            if location.original_item in self.multiworld.start_inventory[self.player].value and \
                    location.original_item in item_groups["Unique"]:
                start_inventory[location.original_item] -= 1
                item = self.create_filler()
            elif location.original_item is None:
                item = self.create_filler()
            else:
                item = self.create_item(location.original_item)
                combined_traps = self.multiworld.poison_trap_weight[self.player].value + self.multiworld.fire_trap_weight[self.player].value + self.multiworld.paralyze_trap_weight[self.player].value + self.multiworld.ice_trap_weight[self.player].value
                if (item.classification == ItemClassification.filler and self.multiworld.random.randint(1, 100)
                        <= self.multiworld.trap_percentage[self.player].value and combined_traps != 0):
                    item = self.create_item(self.select_trap())
            if location.event:
                self.multiworld.get_location(location.name, self.player).place_locked_item(item)
            elif "Badge" not in item.name or self.multiworld.badgesanity[self.player].value:
                item_pool.append(item)

        self.multiworld.random.shuffle(item_pool)

        self.multiworld.itempool += item_pool

    def pre_fill(self) -> None:

        process_wild_pokemon(self)
        process_static_pokemon(self)

        if self.multiworld.old_man[self.player].value == 1:
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1

        if not self.multiworld.badgesanity[self.player].value:
            self.multiworld.non_local_items[self.player].value -= self.item_name_groups["Badges"]
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
                        badgelocs.append(self.multiworld.get_location(loc, self.player))
                    state = self.multiworld.get_all_state(False)
                    self.multiworld.random.shuffle(badges)
                    self.multiworld.random.shuffle(badgelocs)
                    fill_restrictive(self.multiworld, state, badgelocs.copy(), badges, True, True)
                except FillError:
                    for location in badgelocs:
                        location.item = None
                    continue
                break
            else:
                raise FillError(f"Failed to place badges for player {self.player}")

        locs = [self.multiworld.get_location("Fossil - Choice A", self.player),
                self.multiworld.get_location("Fossil - Choice B", self.player)]
        for loc in locs:
            add_item_rule(loc, lambda i: i.advancement or i.name in self.item_name_groups["Unique"]
                                         or i.name == "Master Ball")

        loc = self.multiworld.get_location("Pallet Town - Player's PC", self.player)
        if loc.item is None:
            locs.append(loc)

        for loc in locs:
            unplaced_items = []
            if loc.name in self.multiworld.priority_locations[self.player].value:
                add_item_rule(loc, lambda i: i.advancement)
            for item in reversed(self.multiworld.itempool):
                if item.player == self.player and loc.can_fill(self.multiworld.state, item, False):
                    self.multiworld.itempool.remove(item)
                    state = sweep_from_pool(self.multiworld.state, self.multiworld.itempool + unplaced_items)
                    if state.can_reach(loc, "Location", self.player):
                        loc.place_locked_item(item)
                        break
                    else:
                        unplaced_items.append(item)
            self.multiworld.itempool += unplaced_items

        intervene = False
        test_state = self.multiworld.get_all_state(False)
        if not test_state.pokemon_rb_can_surf(self.player) or not test_state.pokemon_rb_can_strength(self.player):
            intervene = True
        elif self.multiworld.accessibility[self.player].current_key != "minimal":
            if not test_state.pokemon_rb_can_cut(self.player) or not test_state.pokemon_rb_can_flash(self.player):
                intervene = True
        if intervene:
            # the way this is handled will be improved significantly in the future when I add options to
            # let you choose the exact weights for HM compatibility
            logging.warning(
                f"HM-compatible Pokémon possibly missing, placing Mew on Route 1 for player {self.player}")
            loc = self.multiworld.get_location("Route 1 - Wild Pokemon - 1", self.player)
            loc.item = self.create_item("Mew")

    def create_regions(self):
        if self.multiworld.free_fly_location[self.player].value:
            if self.multiworld.old_man[self.player].value == 0:
                fly_map_code = self.multiworld.random.randint(1, 9)
            else:
                fly_map_code = self.multiworld.random.randint(5, 9)
                if fly_map_code == 5:
                    fly_map_code = 4
            if fly_map_code == 9:
                fly_map_code = 10
        else:
            fly_map_code = 0
        self.fly_map = ["Pallet Town", "Viridian City", "Pewter City", "Cerulean City", "Lavender Town",
                        "Vermilion City", "Celadon City", "Fuchsia City", "Cinnabar Island", "Indigo Plateau",
                        "Saffron City"][fly_map_code]
        self.fly_map_code = fly_map_code
        create_regions(self.multiworld, self.player)
        self.multiworld.completion_condition[self.player] = lambda state, player=self.player: state.has("Become Champion", player=player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        return PokemonRBItem(name, self.player)

    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)

    def write_spoiler_header(self, spoiler_handle: TextIO):
        if self.multiworld.free_fly_location[self.player].value:
            spoiler_handle.write('Fly unlocks:                     %s\n' % self.fly_map)
        if self.extra_badges:
            for hm_move, badge in self.extra_badges.items():
                spoiler_handle.write(hm_move + " enabled by: " + (" " * 20)[:20 - len(hm_move)] + badge + "\n")

    def write_spoiler(self, spoiler_handle):
        if self.multiworld.randomize_type_chart[self.player].value:
            spoiler_handle.write(f"\n\nType matchups ({self.multiworld.player_name[self.player]}):\n\n")
            for matchup in self.type_chart:
                spoiler_handle.write(f"{matchup[0]} deals {matchup[2] * 10}% damage to {matchup[1]}\n")

    def get_filler_item_name(self) -> str:
        combined_traps = self.multiworld.poison_trap_weight[self.player].value + self.multiworld.fire_trap_weight[self.player].value + self.multiworld.paralyze_trap_weight[self.player].value + self.multiworld.ice_trap_weight[self.player].value
        if self.multiworld.random.randint(1, 100) <= self.multiworld.trap_percentage[self.player].value and combined_traps != 0:
            return self.select_trap()

        return self.multiworld.random.choice([item for item in item_table if item_table[
            item].classification == ItemClassification.filler and item not in item_groups["Vending Machine Drinks"] +
                                              item_groups["Unique"]])

    def select_trap(self):
        if self.traps is None:
            self.traps = []
            self.traps += ["Poison Trap"] * self.multiworld.poison_trap_weight[self.player].value
            self.traps += ["Fire Trap"] * self.multiworld.fire_trap_weight[self.player].value
            self.traps += ["Paralyze Trap"] * self.multiworld.paralyze_trap_weight[self.player].value
            self.traps += ["Ice Trap"] * self.multiworld.ice_trap_weight[self.player].value
        return self.multiworld.random.choice(self.traps)

    def fill_slot_data(self) -> dict:
        return {
            "second_fossil_check_condition": self.multiworld.second_fossil_check_condition[self.player].value,
            "require_item_finder": self.multiworld.require_item_finder[self.player].value,
            "randomize_hidden_items": self.multiworld.randomize_hidden_items[self.player].value,
            "badges_needed_for_hm_moves": self.multiworld.badges_needed_for_hm_moves[self.player].value,
            "oaks_aide_rt_2": self.multiworld.oaks_aide_rt_2[self.player].value,
            "oaks_aide_rt_11": self.multiworld.oaks_aide_rt_11[self.player].value,
            "oaks_aide_rt_15": self.multiworld.oaks_aide_rt_15[self.player].value,
            "extra_key_items": self.multiworld.extra_key_items[self.player].value,
            "extra_strength_boulders": self.multiworld.extra_strength_boulders[self.player].value,
            "tea": self.multiworld.tea[self.player].value,
            "old_man": self.multiworld.old_man[self.player].value,
            "elite_four_condition": self.multiworld.elite_four_condition[self.player].value,
            "victory_road_condition": self.multiworld.victory_road_condition[self.player].value,
            "viridian_gym_condition": self.multiworld.viridian_gym_condition[self.player].value,
            "cerulean_cave_condition": self.multiworld.cerulean_cave_condition[self.player].value,
            "free_fly_map": self.fly_map_code,
            "extra_badges": self.extra_badges,
            "type_chart": self.type_chart,
            "randomize_pokedex": self.multiworld.randomize_pokedex[self.player].value,
            "trainersanity": self.multiworld.trainersanity[self.player].value,
            "death_link": self.multiworld.death_link[self.player].value
        }


class PokemonRBItem(Item):
    game = "Pokemon Red and Blue"
    type = None

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(PokemonRBItem, self).__init__(
            name,
            item_data.classification,
            item_data.id, player
        )
