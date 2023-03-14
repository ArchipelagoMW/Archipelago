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
    process_static_pokemon, process_move_data
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

    data_version = 7
    required_client_version = (0, 3, 9)

    topology_present = False

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in location_data if location.type == "Item"
                           and location.address is not None}
    item_name_groups = item_groups

    web = PokemonWebWorld()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.fly_map = None
        self.fly_map_code = None
        self.extra_badges = {}
        self.type_chart = None
        self.local_poke_data = None
        self.local_move_data = None
        self.local_tms = None
        self.learnsets = None
        self.trainer_name = None
        self.rival_name = None
        self.type_chart = None
        self.traps = None
        self.trade_mons = {}

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

        if (self.multiworld.dexsanity[self.player] and self.multiworld.accessibility[self.player] == "locations"
                and (self.multiworld.catch_em_all[self.player] != "all_pokemon"
                     or self.multiworld.randomize_wild_pokemon[self.player] == "vanilla"
                     or self.multiworld.randomize_legendary_pokemon[self.player] != "any")):
            self.multiworld.accessibility[self.player] = self.multiworld.accessibility[self.player].from_text("items")

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

        process_move_data(self)
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
        self.multiworld.early_items[self.player]["Exp. All"] = 1

    def create_items(self) -> None:
        start_inventory = self.multiworld.start_inventory[self.player].value.copy()
        if self.multiworld.randomize_pokedex[self.player] == "start_with":
            start_inventory["Pokedex"] = 1
            self.multiworld.push_precollected(self.create_item("Pokedex"))

        locations = [location for location in location_data if location.type == "Item"]
        item_pool = []
        combined_traps = (self.multiworld.poison_trap_weight[self.player].value
                          + self.multiworld.fire_trap_weight[self.player].value
                          + self.multiworld.paralyze_trap_weight[self.player].value
                          + self.multiworld.ice_trap_weight[self.player].value)
        for location in locations:
            if not location.inclusion(self.multiworld, self.player):
                continue
            if location.original_item in self.multiworld.start_inventory[self.player].value and \
                    location.original_item in item_groups["Unique"]:
                start_inventory[location.original_item] -= 1
                item = self.create_filler()
            elif location.original_item is None:
                item = self.create_filler()
            elif location.original_item == "Pokedex":
                if self.multiworld.randomize_pokedex[self.player] == "vanilla":
                    self.multiworld.get_location(location.name, self.player).event = True
                    location.event = True
                item = self.create_item("Pokedex")
            elif location.original_item.startswith("TM"):
                if self.multiworld.randomize_tm_moves[self.player]:
                    item = self.create_item(location.original_item.split(" ")[0])
                else:
                    item = self.create_item(location.original_item)
            else:
                item = self.create_item(location.original_item)
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
        pokemon_locs = [location.name for location in location_data if location.type != "Item"]
        for location in self.multiworld.get_locations(self.player):
            if location.name in pokemon_locs:
                 location.show_in_spoiler = False

        def intervene(move):
            accessible_slots = [loc for loc in self.multiworld.get_reachable_locations(test_state, self.player) if loc.type == "Wild Encounter"]
            move_bit = pow(2, poke_data.hm_moves.index(move) + 2)
            viable_mons = [mon for mon in self.local_poke_data if self.local_poke_data[mon]["tms"][6] & move_bit]
            placed_mons = [slot.item.name for slot in accessible_slots]
            # this sort method doesn't seem to work if you reference the same list being sorted in the lambda
            placed_mons_copy = placed_mons.copy()
            placed_mons.sort(key=lambda i: placed_mons_copy.count(i))
            placed_mon = placed_mons.pop()
            if self.multiworld.area_1_to_1_mapping[self.player]:
                zone = " - ".join(placed_mon.split(" - ")[:-1])
                replace_slots = [slot for slot in accessible_slots if slot.name.startswith(zone) and slot.item.name ==
                                 placed_mon]
            else:
                replace_slots = [self.multiworld.random.choice([slot for slot in accessible_slots if slot.item.name ==
                                                               placed_mon])]
            replace_mon = self.multiworld.random.choice(viable_mons)
            for replace_slot in replace_slots:
                replace_slot.item = self.create_item(replace_mon)
        last_intervene = None
        while True:
            intervene_move = None
            test_state = self.multiworld.get_all_state(False)
            if not self.multiworld.badgesanity[self.player]:
                for badge in ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge",
                              "Marsh Badge", "Volcano Badge", "Earth Badge"]:
                    test_state.collect(self.create_item(badge))
            if not test_state.pokemon_rb_can_surf(self.player):
                intervene_move = "Surf"
            if not test_state.pokemon_rb_can_strength(self.player):
                intervene_move = "Strength"
            # cut may not be needed if accessibility is minimal, unless you need all 8 badges and badgesanity is off,
            # as you will require cut to access celadon gyn
            if (self.multiworld.accessibility[self.player] != "minimal" or ((not
                self.multiworld.badgesanity[self.player]) and max(self.multiworld.elite_four_condition[self.player],
                                                                 self.multiworld.victory_road_condition[self.player]) > 7)):
                if not test_state.pokemon_rb_can_cut(self.player):
                    intervene_move = "Cut"
            if (self.multiworld.accessibility[self.player].current_key != "minimal" and
                (self.multiworld.trainersanity[self.player] or self.multiworld.extra_key_items[self.player])):
                if not test_state.pokemon_rb_can_flash(self.player):
                    intervene_move = "Flash"
            if intervene_move:
                if intervene_move == last_intervene:
                    raise Exception(f"Caught in infinite loop attempting to ensure {intervene_move} is available to player {self.player}")
                intervene(intervene_move)
                last_intervene = intervene_move
            else:
                break

        if self.multiworld.old_man[self.player] == "early_parcel":
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1
            if self.multiworld.dexsanity[self.player]:
                for location in [self.multiworld.get_location(f"Pokedex - {mon}", self.player)
                                 for mon in poke_data.pokemon_data.keys()]:
                    add_item_rule(location, lambda item: item.name != "Oak's Parcel" or item.player != self.player)

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

        # Place local items in some locations to prevent save-scumming. Also Oak's PC to prevent an "AP Item" from
        # entering the player's inventory.

        locs = {self.multiworld.get_location("Fossil - Choice A", self.player),
                self.multiworld.get_location("Fossil - Choice B", self.player)}

        if self.multiworld.dexsanity[self.player]:
            for mon in ([" ".join(self.multiworld.get_location(
                    f"Pallet Town - Starter {i}", self.player).item.name.split(" ")[1:]) for i in range(1, 4)]
                    + [" ".join(self.multiworld.get_location(
                    f"Fighting Dojo - Gift {i}", self.player).item.name.split(" ")[1:]) for i in range(1, 3)]):
                loc = self.multiworld.get_location(f"Pokedex - {mon}", self.player)
                if loc.item is None:
                    locs.add(loc)

        loc = self.multiworld.get_location("Pallet Town - Player's PC", self.player)
        if loc.item is None:
            locs.add(loc)

        for loc in sorted(locs):
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
        spoiler_handle.write(f"\n\nPokémon locations ({self.multiworld.player_name[self.player]}):\n\n")
        pokemon_locs = [location.name for location in location_data if location.type != "Item"]
        for location in self.multiworld.get_locations(self.player):
            if location.name in pokemon_locs:
                spoiler_handle.write(location.name + ": " + location.item.name + "\n")


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

    def extend_hint_information(self, hint_data):
        if self.multiworld.dexsanity[self.player]:
            hint_data[self.player] = {}
            mon_locations = {mon: set() for mon in poke_data.pokemon_data.keys()}
            for loc in location_data: #self.multiworld.get_locations(self.player):
                if loc.type in ["Wild Encounter", "Static Pokemon", "Legendary Pokemon", "Missable Pokemon"]:
                    mon = self.multiworld.get_location(loc.name, self.player).item.name
                    if mon.startswith("Static ") or mon.startswith("Missable "):
                        mon = " ".join(mon.split(" ")[1:])
                    mon_locations[mon].add(loc.name.split(" -")[0])
            for mon in mon_locations:
                if mon_locations[mon]:
                    hint_data[self.player][self.multiworld.get_location(f"Pokedex - {mon}", self.player).address] = \
                        ", ".join(mon_locations[mon])

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
            "death_link": self.multiworld.death_link[self.player].value,
            "prizesanity": self.multiworld.prizesanity[self.player].value
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
