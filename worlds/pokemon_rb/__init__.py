import os
import settings
import typing
import threading
import base64
import random
from copy import deepcopy
from typing import TextIO

from Utils import __version__
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, LocationProgressType
from Fill import fill_restrictive, FillError, sweep_from_pool
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_item_rule
from .items import item_table, item_groups
from .locations import location_data, PokemonRBLocation
from .regions import create_regions
from .options import PokemonRBOptions
from .rom_addresses import rom_addresses
from .text import encode_text
from .rom import generate_output, get_base_rom_bytes, get_base_rom_path, RedDeltaPatch, BlueDeltaPatch
from .pokemon import process_pokemon_data, process_move_data, verify_hm_moves
from .encounters import process_pokemon_locations, process_trainer_data
from .rules import set_rules
from .level_scaling import level_scaling
from . import logic
from . import poke_data
from . import client


class PokemonSettings(settings.Group):
    class RedRomFile(settings.UserFilePath):
        """File names of the Pokemon Red and Blue roms"""
        description = "Pokemon Red (UE) ROM File"
        copy_to = "Pokemon Red (UE) [S][!].gb"
        md5s = [RedDeltaPatch.hash]

    class BlueRomFile(settings.UserFilePath):
        description = "Pokemon Blue (UE) ROM File"
        copy_to = "Pokemon Blue (UE) [S][!].gb"
        md5s = [BlueDeltaPatch.hash]

    red_rom_file: RedRomFile = RedRomFile(RedRomFile.copy_to)
    blue_rom_file: BlueRomFile = BlueRomFile(BlueRomFile.copy_to)


class PokemonWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Red and Blue with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
    )

    setup_es = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Español",
        "setup_es.md",
        "setup/es",
        ["Shiny"]
    )

    tutorials = [setup_en, setup_es]


class PokemonRedBlueWorld(World):
    """Pokémon Red and Pokémon Blue are the original monster-collecting turn-based RPGs.  Explore the Kanto region with
    your Pokémon, catch more than 150 unique creatures, earn badges from the region's Gym Leaders, and challenge the
    Elite Four to become the champion!"""
    # -MuffinJets#4559
    game = "Pokemon Red and Blue"

    options_dataclass = PokemonRBOptions
    options: PokemonRBOptions

    settings: typing.ClassVar[PokemonSettings]

    required_client_version = (0, 4, 2)

    topology_present = True

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in location_data if location.type == "Item"
                           and location.address is not None}
    item_name_groups = item_groups

    web = PokemonWebWorld()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.item_pool = []
        self.total_key_items = None
        self.fly_map = None
        self.fly_map_code = None
        self.town_map_fly_map = None
        self.town_map_fly_map_code = None
        self.extra_badges = {}
        self.type_chart = None
        self.local_poke_data = None
        self.local_move_data = None
        self.local_tms = None
        self.learnsets = None
        self.trainer_name = None
        self.rival_name = None
        self.traps = None
        self.trade_mons = {}
        self.finished_level_scaling = threading.Event()
        self.dexsanity_table = []
        self.trainersanity_table = []
        self.local_locs = []

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        versions = set()
        for player in multiworld.player_ids:
            if multiworld.worlds[player].game == "Pokemon Red and Blue":
                versions.add(multiworld.worlds[player].options.game_version.current_key)
        for version in versions:
            if not os.path.exists(get_base_rom_path(version)):
                raise FileNotFoundError(get_base_rom_path(version))

    @classmethod
    def stage_generate_early(cls, multiworld: MultiWorld):

        seed_groups = {}
        pokemon_rb_worlds = multiworld.get_game_worlds("Pokemon Red and Blue")

        for world in pokemon_rb_worlds:
            if not (world.options.type_chart_seed.value.isdigit() or world.options.type_chart_seed.value == "random"):
                seed_groups[world.options.type_chart_seed.value] = seed_groups.get(world.options.type_chart_seed.value,
                                                                                   []) + [world]

        copy_chart_worlds = {}

        for worlds in seed_groups.values():
            chosen_world = multiworld.random.choice(worlds)
            for world in worlds:
                if world is not chosen_world:
                    copy_chart_worlds[world.player] = chosen_world

        for world in pokemon_rb_worlds:
            if world.player in copy_chart_worlds:
                continue
            tc_random = world.random
            if world.options.type_chart_seed.value.isdigit():
                tc_random = random.Random()
                tc_random.seed(int(world.options.type_chart_seed.value))

            if world.options.randomize_type_chart == "vanilla":
                chart = deepcopy(poke_data.type_chart)
            elif world.options.randomize_type_chart == "randomize":
                types = poke_data.type_names.values()
                matchups = []
                for type1 in types:
                    for type2 in types:
                        matchups.append([type1, type2])
                tc_random.shuffle(matchups)
                immunities = world.options.immunity_matchups.value
                super_effectives = world.options.super_effective_matchups.value
                not_very_effectives = world.options.not_very_effective_matchups.value
                normals = world.options.normal_matchups.value
                while super_effectives + not_very_effectives + normals < 225 - immunities:
                    if super_effectives == not_very_effectives == normals == 0:
                        super_effectives = 225
                        not_very_effectives = 225
                        normals = 225
                    else:
                        super_effectives += world.options.super_effective_matchups.value
                        not_very_effectives += world.options.not_very_effective_matchups.value
                        normals += world.options.normal_matchups.value
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
                        r = tc_random.randint(0, 2)
                        if r == 0 and super_effectives:
                            super_effectives -= 1
                        elif r == 1 and not_very_effectives:
                            not_very_effectives -= 1
                        elif normals:
                            normals -= 1
                chart = []
                for matchup_list, matchup_value in zip([immunities, normals, super_effectives, not_very_effectives],
                                                       [0, 10, 20, 5]):
                    for _ in range(matchup_list):
                        matchup = matchups.pop()
                        matchup.append(matchup_value)
                        chart.append(matchup)
            elif world.options.randomize_type_chart == "chaos":
                types = poke_data.type_names.values()
                matchups = []
                for type1 in types:
                    for type2 in types:
                        matchups.append([type1, type2])
                chart = []
                values = list(range(21))
                tc_random.shuffle(matchups)
                tc_random.shuffle(values)
                for matchup in matchups:
                    value = values.pop(0)
                    values.append(value)
                    matchup.append(value)
                    chart.append(matchup)
            # sort so that super-effective matchups occur first, to prevent dual "not very effective" / "super effective"
            # matchups from leading to damage being ultimately divided by 2 and then multiplied by 2, which can lead to
            # damage being reduced by 1 which leads to a "not very effective" message appearing due to my changes
            # to the way effectiveness messages are generated.
            world.type_chart = sorted(chart, key=lambda matchup: -matchup[2])

        for player in copy_chart_worlds:
            multiworld.worlds[player].type_chart = copy_chart_worlds[player].type_chart

    def generate_early(self):
        def encode_name(name, t):
            try:
                if len(encode_text(name)) > 7:
                    raise IndexError(f"{t} name too long for player {self.multiworld.player_name[self.player]}. Must be 7 characters or fewer.")
                return encode_text(name, length=8, whitespace="@", safety=True)
            except KeyError as e:
                raise KeyError(f"Invalid character(s) in {t} name for player {self.multiworld.player_name[self.player]}") from e
        if self.options.trainer_name == "choose_in_game":
            self.trainer_name = "choose_in_game"
        else:
            self.trainer_name = encode_name(self.options.trainer_name.value, "Player")
        if self.options.rival_name == "choose_in_game":
            self.rival_name = "choose_in_game"
        else:
            self.rival_name = encode_name(self.options.rival_name.value, "Rival")

        if not self.options.badgesanity:
            self.options.non_local_items.value -= self.item_name_groups["Badges"]

        if self.options.key_items_only:
            self.options.trainersanity.value = 0
            self.options.dexsanity.value = 0
            self.options.randomize_hidden_items = \
                self.options.randomize_hidden_items.from_text("off")

        if self.options.badges_needed_for_hm_moves.value >= 2:
            badges_to_add = ["Marsh Badge", "Volcano Badge", "Earth Badge"]
            if self.options.badges_needed_for_hm_moves.value == 3:
                badges = ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Marsh Badge",
                          "Soul Badge", "Volcano Badge", "Earth Badge"]
                self.random.shuffle(badges)
                badges_to_add += [badges.pop(), badges.pop()]
            hm_moves = ["Cut", "Fly", "Surf", "Strength", "Flash"]
            self.random.shuffle(hm_moves)
            self.extra_badges = {}
            for badge in badges_to_add:
                self.extra_badges[hm_moves.pop()] = badge

        process_move_data(self)
        process_pokemon_data(self)

        self.dexsanity_table = [
            *(True for _ in range(round(self.options.dexsanity.value))),
            *(False for _ in range(151 - round(self.options.dexsanity.value)))
        ]
        self.random.shuffle(self.dexsanity_table)

        self.trainersanity_table = [
            *(True for _ in range(self.options.trainersanity.value)),
            *(False for _ in range(317 - self.options.trainersanity.value))
        ]
        self.random.shuffle(self.trainersanity_table)

    def create_items(self):
        self.multiworld.itempool += self.item_pool

    @classmethod
    def stage_fill_hook(cls, multiworld, progitempool, usefulitempool, filleritempool, fill_locations):
        locs = []
        for world in multiworld.get_game_worlds("Pokemon Red and Blue"):
            locs += world.local_locs
        for loc in sorted(locs):
            if loc.item:
                continue
            itempool = progitempool + usefulitempool + filleritempool
            multiworld.random.shuffle(itempool)
            unplaced_items = []
            for i, item in enumerate(itempool):
                if item.player == loc.player and loc.can_fill(multiworld.state, item, False):
                    if item.advancement:
                        pool = progitempool
                    elif item.useful:
                        pool = usefulitempool
                    else:
                        pool = filleritempool
                    for i, check_item in enumerate(pool):
                        if item is check_item:
                            pool.pop(i)
                            break
                    if item.advancement:
                        state = sweep_from_pool(multiworld.state, progitempool + unplaced_items)
                    if (not item.advancement) or state.can_reach(loc, "Location", loc.player):
                        multiworld.push_item(loc, item, False)
                        fill_locations.remove(loc)
                        break
                    else:
                        unplaced_items.append(item)
            else:
                raise FillError(f"Pokemon Red and Blue local item fill failed for player {loc.player}: could not place {item.name}")
            progitempool += [item for item in unplaced_items if item.advancement]
            usefulitempool += [item for item in unplaced_items if item.useful]
            filleritempool += [item for item in unplaced_items if (not item.advancement) and (not item.useful)]

    def fill_hook(self, progitempool, usefulitempool, filleritempool, fill_locations):
        if not self.options.badgesanity:
            # Door Shuffle options besides Simple place badges during door shuffling
            if self.options.door_shuffle in ("off", "simple"):
                badges = [item for item in progitempool if "Badge" in item.name and item.player == self.player]
                for badge in badges:
                    self.multiworld.itempool.remove(badge)
                    progitempool.remove(badge)
                for attempt in range(6):
                    badgelocs = [
                        self.multiworld.get_location(loc, self.player) for loc in [
                            "Pewter Gym - Brock Prize", "Cerulean Gym - Misty Prize",
                            "Vermilion Gym - Lt. Surge Prize", "Celadon Gym - Erika Prize",
                            "Fuchsia Gym - Koga Prize", "Saffron Gym - Sabrina Prize",
                            "Cinnabar Gym - Blaine Prize", "Viridian Gym - Giovanni Prize"
                        ] if self.multiworld.get_location(loc, self.player).item is None]
                    state = self.multiworld.get_all_state(False)
                    # Give it two tries to place badges with wild Pokemon and learnsets as-is.
                    # If it can't, then try with all Pokemon collected, and we'll try to fix HM move availability after.
                    if attempt > 1:
                        for mon in poke_data.pokemon_data.keys():
                            state.collect(self.create_item(mon), True)
                    state.sweep_for_advancements()
                    self.random.shuffle(badges)
                    self.random.shuffle(badgelocs)
                    badgelocs_copy = badgelocs.copy()
                    # allow_partial so that unplaced badges aren't lost, for debugging purposes
                    fill_restrictive(self.multiworld, state, badgelocs_copy, badges, True, True, allow_partial=True)
                    if len(badges) > 8 - len(badgelocs):
                        for location in badgelocs:
                            if location.item:
                                badges.append(location.item)
                                location.item = None
                        continue
                    else:
                        for location in badgelocs:
                            if location.item:
                                fill_locations.remove(location)
                        progitempool += badges
                        break
                else:
                    raise FillError(f"Failed to place badges for player {self.player}")
            verify_hm_moves(self.multiworld, self, self.player)

        if self.options.key_items_only:
            return

        tms = [item for item in usefulitempool + filleritempool if item.name.startswith("TM") and (item.player ==
               self.player or (item.player in self.multiworld.groups and self.player in
                               self.multiworld.groups[item.player]["players"]))]
        if len(tms) > 7:
            for gym_leader in (("Pewter Gym", "Brock"), ("Cerulean Gym", "Misty"), ("Vermilion Gym", "Lt. Surge"),
                               ("Celadon Gym-C", "Erika"), ("Fuchsia Gym", "Koga"), ("Saffron Gym-C", "Sabrina"),
                               ("Cinnabar Gym", "Blaine"), ("Viridian Gym", "Giovanni")):
                loc = self.multiworld.get_location(f"{gym_leader[0].split('-')[0]} - {gym_leader[1]} TM",
                                                   self.player)
                if loc.item:
                    continue
                for party in self.multiworld.get_location(gym_leader[0] + " - Trainer Parties", self.player).party_data:
                    if party["party_address"] == \
                            f"Trainer_Party_{gym_leader[1].replace('. ', '').replace('Giovanni', 'Viridian_Gym_Giovanni')}_A":
                        mon = party["party"][-1]
                        learnable_tms = [tm for tm in tms if self.local_poke_data[mon]["tms"][
                            int((int(tm.name[2:4]) - 1) / 8)] & 1 << ((int(tm.name[2:4]) - 1) % 8)]
                        if not learnable_tms:
                            learnable_tms = tms
                        tm = self.random.choice(learnable_tms)

                        loc.place_locked_item(tm)
                        fill_locations.remove(loc)
                        tms.remove(tm)
                        if tm.useful:
                            usefulitempool.remove(tm)
                        else:
                            filleritempool.remove(tm)
                        break
                else:
                    raise Exception("Missing Gym Leader data")

    def pre_fill(self) -> None:
        process_pokemon_locations(self)
        process_trainer_data(self)
        locs = [location.name for location in location_data if location.type != "Item"]
        for location in self.multiworld.get_locations(self.player):
            if location.name in locs:
                location.show_in_spoiler = False
        verify_hm_moves(self.multiworld, self, self.player)

        # Delete evolution events for Pokémon that are not in logic in an all_state so that accessibility check does not
        # fail. Re-use test_state from previous final loop.
        all_state = self.multiworld.get_all_state(False)
        evolutions_region = self.multiworld.get_region("Evolution", self.player)
        for location in evolutions_region.locations.copy():
            if not all_state.can_reach(location, player=self.player):
                evolutions_region.locations.remove(location)

        if self.options.old_man == "early_parcel":
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1
            if self.options.dexsanity:
                for i, mon in enumerate(poke_data.pokemon_data):
                    if self.dexsanity_table[i]:
                        location = self.multiworld.get_location(f"Pokedex - {mon}", self.player)
                        add_item_rule(location, lambda item: item.name != "Oak's Parcel" or item.player != self.player)

        # Place local items in some locations to prevent save-scumming. Also Oak's PC to prevent an "AP Item" from
        # entering the player's inventory.

        locs = {self.multiworld.get_location("Fossil - Choice A", self.player),
                self.multiworld.get_location("Fossil - Choice B", self.player)}

        if not self.options.key_items_only:
            rule = None
            if self.options.fossil_check_item_types == "key_items":
                rule = lambda i: i.advancement
            elif self.options.fossil_check_item_types == "unique_items":
                rule = lambda i: i.name in item_groups["Unique"]
            elif self.options.fossil_check_item_types == "no_key_items":
                rule = lambda i: not i.advancement
            if rule:
                for loc in locs:
                    add_item_rule(loc, rule)

        for mon in ([" ".join(self.multiworld.get_location(
                f"Oak's Lab - Starter {i}", self.player).item.name.split(" ")[1:]) for i in range(1, 4)]
                + [" ".join(self.multiworld.get_location(
                f"Saffron Fighting Dojo - Gift {i}", self.player).item.name.split(" ")[1:]) for i in range(1, 3)]
                + ["Vaporeon", "Jolteon", "Flareon"]):
            if self.dexsanity_table[poke_data.pokemon_dex[mon] - 1]:
                loc = self.multiworld.get_location(f"Pokedex - {mon}", self.player)
                if loc.item is None:
                    locs.add(loc)

        if not self.options.key_items_only:
            loc = self.multiworld.get_location("Player's House 2F - Player's PC", self.player)
            if loc.item is None:
                locs.add(loc)

        for loc in sorted(locs):
            if loc.name in self.options.priority_locations.value:
                add_item_rule(loc, lambda i: i.advancement)
            add_item_rule(loc, lambda i: i.player == self.player)
            if self.options.old_man == "early_parcel" and loc.name != "Player's House 2F - Player's PC":
                add_item_rule(loc, lambda i: i.name != "Oak's Parcel")

        self.local_locs = locs

        all_state = self.multiworld.get_all_state(False)

        reachable_mons = set()
        for mon in poke_data.pokemon_data:
            if all_state.has(mon, self.player) or all_state.has(f"Static {mon}", self.player):
                reachable_mons.add(mon)

        # The large number of wild Pokemon can make sweeping for events time-consuming, and is especially bad in
        # the spoiler playthrough calculation because it removes each advancement item one at a time to verify
        # if the game is beatable without it. We go through each zone and flag any duplicates as useful.
        # Especially with area 1-to-1 mapping / vanilla wild Pokémon, this should cut down significantly on wasted time.
        for region in self.multiworld.get_regions(self.player):
            region_mons = set()
            for location in region.locations:
                if "Wild Pokemon" in location.name:
                    if location.item.name in region_mons:
                        location.item.classification = ItemClassification.useful
                    else:
                        region_mons.add(location.item.name)

        self.options.elite_four_pokedex_condition.total = \
            int((len(reachable_mons) / 100) * self.options.elite_four_pokedex_condition.value)

        if self.options.accessibility == "full":
            balls = [self.create_item(ball) for ball in ["Poke Ball", "Great Ball", "Ultra Ball"]]
            traps = [self.create_item(trap) for trap in item_groups["Traps"]]
            locations = [location for location in self.multiworld.get_locations(self.player) if "Pokedex - " in
                         location.name]
            pokedex = self.multiworld.get_region("Pokedex", self.player)
            remove_items = 0

            for location in locations:
                if not location.can_reach(all_state):
                    pokedex.locations.remove(location)
                    if location in self.local_locs:
                        self.local_locs.remove(location)
                    self.dexsanity_table[poke_data.pokemon_dex[location.name.split(" - ")[1]] - 1] = False
                    remove_items += 1

            for _ in range(remove_items):
                balls.append(balls.pop(0))
                for ball in balls:
                    try:
                        self.multiworld.itempool.remove(ball)
                    except ValueError:
                        continue
                    else:
                        break
                else:
                    self.random.shuffle(traps)
                    for trap in traps:
                        try:
                            self.multiworld.itempool.remove(trap)
                        except ValueError:
                            continue
                        else:
                            break
                    else:
                        raise Exception("Failed to remove corresponding item while deleting unreachable Dexsanity location")

    @classmethod
    def stage_post_fill(cls, multiworld):
        # Convert all but one of each instance of a wild Pokemon to useful classification.
        # This cuts down on time spent calculating the spoiler playthrough.
        found_mons = set()
        for sphere in multiworld.get_spheres():
            mon_locations_in_sphere = {}
            for location in sphere:
                if (location.game == location.item.game == "Pokemon Red and Blue"
                        and (location.item.name in poke_data.pokemon_data.keys() or "Static " in location.item.name)
                        and location.item.advancement):
                    key = (location.player, location.item.name)
                    if key in found_mons:
                        location.item.classification = ItemClassification.useful
                    else:
                        mon_locations_in_sphere.setdefault(key, []).append(location)
            for key, mon_locations in mon_locations_in_sphere.items():
                found_mons.add(key)
                if len(mon_locations) > 1:
                    # Sort for deterministic results.
                    mon_locations.sort()
                    # Convert all but the first to useful classification.
                    for location in mon_locations[1:]:
                        location.item.classification = ItemClassification.useful

    def create_regions(self):
        if (self.options.old_man == "vanilla" or
                self.options.door_shuffle in ("full", "insanity")):
            fly_map_codes = self.random.sample(range(2, 11), 2)
        elif (self.options.door_shuffle == "simple" or
                self.options.route_3_condition == "boulder_badge" or
              (self.options.route_3_condition == "any_badge" and
               self.options.badgesanity)):
            fly_map_codes = self.random.sample(range(3, 11), 2)

        else:
            fly_map_codes = self.random.sample([4, 6, 7, 8, 9, 10], 2)
        if self.options.free_fly_location:
            fly_map_code = fly_map_codes[0]
        else:
            fly_map_code = 0
        if self.options.town_map_fly_location:
            town_map_fly_map_code = fly_map_codes[1]
        else:
            town_map_fly_map_code = 0
        fly_maps = ["Pallet Town", "Viridian City", "Pewter City", "Cerulean City", "Lavender Town",
                    "Vermilion City", "Celadon City", "Fuchsia City", "Cinnabar Island", "Indigo Plateau",
                    "Saffron City"]
        self.fly_map = fly_maps[fly_map_code]
        self.town_map_fly_map = fly_maps[town_map_fly_map_code]
        self.fly_map_code = fly_map_code
        self.town_map_fly_map_code = town_map_fly_map_code

        create_regions(self)
        self.multiworld.completion_condition[self.player] = lambda state, player=self.player: state.has("Become Champion", player=player)

    def set_rules(self):
        set_rules(self.multiworld, self, self.player)

    def create_item(self, name: str) -> Item:
        return PokemonRBItem(name, self.player)

    @classmethod
    def stage_generate_output(cls, multiworld, output_directory):
        level_scaling(multiworld)

    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)

    def modify_multidata(self, multidata: dict):
        rom_name = bytearray(f'AP{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                             'utf8')[:21]
        rom_name.extend([0] * (21 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"Cerulean Cave Total Key Items:   {self.options.cerulean_cave_key_items_condition.total}\n")
        spoiler_handle.write(f"Elite Four Total Key Items:      {self.options.elite_four_key_items_condition.total}\n")
        spoiler_handle.write(f"Elite Four Total Pokemon:        {self.options.elite_four_pokedex_condition.total}\n")
        if self.options.free_fly_location:
            spoiler_handle.write(f"Free Fly Location:               {self.fly_map}\n")
        if self.options.town_map_fly_location:
            spoiler_handle.write(f"Town Map Fly Location:           {self.town_map_fly_map}\n")
        if self.extra_badges:
            for hm_move, badge in self.extra_badges.items():
                spoiler_handle.write(hm_move + " enabled by: " + (" " * 20)[:20 - len(hm_move)] + badge + "\n")

    def write_spoiler(self, spoiler_handle):
        if self.options.randomize_type_chart:
            spoiler_handle.write(f"\n\nType matchups ({self.multiworld.player_name[self.player]}):\n\n")
            for matchup in self.type_chart:
                spoiler_handle.write(f"{matchup[0]} deals {matchup[2] * 10}% damage to {matchup[1]}\n")
        spoiler_handle.write(f"\n\nPokémon locations ({self.multiworld.player_name[self.player]}):\n\n")
        pokemon_locs = [location.name for location in location_data if location.type not in ("Item", "Trainer Parties")]
        for location in self.multiworld.get_locations(self.player):
            if location.name in pokemon_locs:
                spoiler_handle.write(location.name + ": " + location.item.name + "\n")

    def get_filler_item_name(self) -> str:
        combined_traps = (self.options.poison_trap_weight.value
                          + self.options.fire_trap_weight.value
                          + self.options.paralyze_trap_weight.value
                          + self.options.ice_trap_weight.value
                          + self.options.sleep_trap_weight.value)
        if (combined_traps > 0 and
                self.random.randint(1, 100) <= self.options.trap_percentage.value):
            return self.select_trap()
        banned_items = item_groups["Unique"]
        if (((not self.options.tea) or "Saffron City" not in [self.fly_map, self.town_map_fly_map])
                and (not self.options.door_shuffle)):
            # under these conditions, you should never be able to reach the Copycat or Pokémon Tower without being
            # able to reach the Celadon Department Store, so Poké Dolls would not allow early access to anything
            banned_items.append("Poke Doll")
        if not self.options.tea:
            banned_items += item_groups["Vending Machine Drinks"]
        return self.random.choice([item for item in item_table if item_table[item].id and item_table[
            item].classification == ItemClassification.filler and item not in banned_items])

    def select_trap(self):
        if self.traps is None:
            self.traps = []
            self.traps += ["Poison Trap"] * self.options.poison_trap_weight.value
            self.traps += ["Fire Trap"] * self.options.fire_trap_weight.value
            self.traps += ["Paralyze Trap"] * self.options.paralyze_trap_weight.value
            self.traps += ["Ice Trap"] * self.options.ice_trap_weight.value
            self.traps += ["Sleep Trap"] * self.options.sleep_trap_weight.value
        return self.random.choice(self.traps)

    def extend_hint_information(self, hint_data):
        if self.options.dexsanity or self.options.door_shuffle:
            hint_data[self.player] = {}
        if self.options.dexsanity:
            mon_locations = {mon: set() for mon in poke_data.pokemon_data.keys()}
            for loc in location_data:
                if loc.type in ["Wild Encounter", "Static Pokemon", "Legendary Pokemon", "Missable Pokemon"]:
                    mon = self.multiworld.get_location(loc.name, self.player).item.name
                    if mon.startswith("Static ") or mon.startswith("Missable "):
                        mon = " ".join(mon.split(" ")[1:])
                    mon_locations[mon].add(loc.name.split(" -")[0])
            for i, mon in enumerate(mon_locations):
                if self.dexsanity_table[i] and mon_locations[mon]:
                    hint_data[self.player][self.multiworld.get_location(f"Pokedex - {mon}", self.player).address] =\
                        ", ".join(mon_locations[mon])

        if self.options.door_shuffle:
            for location in self.multiworld.get_locations(self.player):
                if location.parent_region.entrance_hint and location.address:
                    hint_data[self.player][location.address] = location.parent_region.entrance_hint

    def fill_slot_data(self) -> dict:
        ret = {
            "second_fossil_check_condition": self.options.second_fossil_check_condition.value,
            "require_item_finder": self.options.require_item_finder.value,
            "randomize_hidden_items": self.options.randomize_hidden_items.value,
            "badges_needed_for_hm_moves": self.options.badges_needed_for_hm_moves.value,
            "oaks_aide_rt_2": self.options.oaks_aide_rt_2.value,
            "oaks_aide_rt_11": self.options.oaks_aide_rt_11.value,
            "oaks_aide_rt_15": self.options.oaks_aide_rt_15.value,
            "extra_key_items": self.options.extra_key_items.value,
            "extra_strength_boulders": self.options.extra_strength_boulders.value,
            "tea": self.options.tea.value,
            "old_man": self.options.old_man.value,
            "elite_four_badges_condition": self.options.elite_four_badges_condition.value,
            "elite_four_key_items_condition": self.options.elite_four_key_items_condition.total,
            "elite_four_pokedex_condition": self.options.elite_four_pokedex_condition.total,
            "victory_road_condition": self.options.victory_road_condition.value,
            "route_22_gate_condition": self.options.route_22_gate_condition.value,
            "route_3_condition": self.options.route_3_condition.value,
            "robbed_house_officer": self.options.robbed_house_officer.value,
            "viridian_gym_condition": self.options.viridian_gym_condition.value,
            "cerulean_cave_badges_condition": self.options.cerulean_cave_badges_condition.value,
            "cerulean_cave_key_items_condition": self.options.cerulean_cave_key_items_condition.total,
            "free_fly_map": self.fly_map_code,
            "town_map_fly_map": self.town_map_fly_map_code,
            "extra_badges": self.extra_badges,
            "randomize_pokedex": self.options.randomize_pokedex.value,
            "trainersanity": self.options.trainersanity.value,
            "death_link": self.options.death_link.value,
            "prizesanity": self.options.prizesanity.value,
            "key_items_only": self.options.key_items_only.value,
            "poke_doll_skip": self.options.poke_doll_skip.value,
            "bicycle_gate_skips": self.options.bicycle_gate_skips.value,
            "stonesanity": self.options.stonesanity.value,
            "door_shuffle": self.options.door_shuffle.value,
            "warp_tile_shuffle": self.options.warp_tile_shuffle.value,
            "dark_rock_tunnel_logic": self.options.dark_rock_tunnel_logic.value,
            "split_card_key": self.options.split_card_key.value,
            "all_elevators_locked": self.options.all_elevators_locked.value,
            "require_pokedex": self.options.require_pokedex.value,
            "area_1_to_1_mapping": self.options.area_1_to_1_mapping.value,
            "blind_trainers": self.options.blind_trainers.value,
            "v5_update": True,

        }
        if self.options.type_chart_seed == "random" or self.options.type_chart_seed.value.isdigit():
            ret["type_chart"] = self.type_chart

        return ret

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
