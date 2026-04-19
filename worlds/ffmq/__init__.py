import random

import base64
import threading
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from .Regions import create_regions, location_table, set_rules, rooms
from .Items import item_table, item_groups, create_items, FFMQItem, fillers
from .Output import generate_output
from .Options import FFMQOptions
from .Client import FFMQClient
from .RoomsGenerator import generate_rooms


class FFMQWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy Mystic Quest with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
        )
    
    setup_fr = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Artea"]
        )
    
    tutorials = [setup_en, setup_fr]
    game_info_languages = ["en", "fr"]


class FFMQWorld(World):
    """Final Fantasy: Mystic Quest is a simple, humorous RPG for the Super Nintendo. You travel across four continents,
    linked in the middle of the world by the Focus Tower, which has been locked by four magical coins. Make your way to
    the bottom of the Focus Tower, then straight up through the top!"""
    # -Giga Otomia

    game = "Final Fantasy Mystic Quest"

    item_name_to_id = {name: data.id for name, data in item_table.items() if data.id is not None}
    location_name_to_id = location_table
    options_dataclass = FFMQOptions
    options: FFMQOptions

    topology_present = True

    item_name_groups = item_groups

    generate_output = generate_output
    create_items = create_items
    create_regions = create_regions
    set_rules = set_rules
    
    web = FFMQWebWorld()
    # settings: FFMQSettings

    ut_can_gen_without_yaml = True
    glitches_item_name = "ut_glitch"

    def __init__(self, world, player: int):
        self.rom_name_available_event = threading.Event()
        self.rom_name = None
        self.rooms = None
        self.hint_data = []
        self.ut = False
        self.finished_hint_data_collection = threading.Event()
        self.map_shuffle_seed = None
        super().__init__(world, player)

    def generate_early(self):
        if self.options.enemies_scaling_lower.value > self.options.enemies_scaling_upper.value:
            self.options.enemies_scaling_lower.value, self.options.enemies_scaling_upper.value = \
                self.options.enemies_scaling_upper.value, self.options.enemies_scaling_lower.value
        if self.options.bosses_scaling_lower.value > self.options.bosses_scaling_upper.value:
            self.options.bosses_scaling_lower.value, self.options.bosses_scaling_upper.value = \
                self.options.bosses_scaling_upper.value, self.options.bosses_scaling_lower.value
        if hasattr(self.multiworld, "re_gen_passthrough") and self.game in self.multiworld.re_gen_passthrough:
            self.ut = True
            for key, value in self.multiworld.re_gen_passthrough[self.game].items():
                if hasattr(self.options, key):
                    getattr(self.options, key).value = value
        else:
            if self.options.map_shuffle_seed.value.isdigit():
                self.map_shuffle_seed = self.options.map_shuffle_seed.value
            elif self.options.map_shuffle_seed.value != "random":
                self.map_shuffle_seed = int(hash(self.options.map_shuffle_seed.value)) + int(self.multiworld.seed)
            else:
                self.map_shuffle_seed = self.random.randint(0, 0xFFFFFFFF)

    @classmethod
    def stage_generate_early(cls, multiworld):
        for world in multiworld.get_game_worlds("Final Fantasy Mystic Quest"):
            shuffle_random = random.Random()
            shuffle_random.seed(world.map_shuffle_seed)
            map_shuffle = world.options.map_shuffle.value
            crest_shuffle = world.options.crest_shuffle.value
            battlefield_shuffle = world.options.shuffle_battlefield_rewards.value
            companion_shuffle = world.options.companions_locations.value
            kaeli_mom = world.options.kaelis_mom_fight_minotaur.value
            overworld_shuffle = world.options.overworld_shuffle.value
            world.rooms = generate_rooms(world.random, map_shuffle, crest_shuffle, battlefield_shuffle,
                                         companion_shuffle, kaeli_mom, overworld_shuffle)

    def create_item(self, name: str):
        return FFMQItem(name, self.player)

    def collect_item(self, state, item, remove=False):
        if not item.advancement:
            return None
        if "Progressive" in item.name:
            i = item.code - 256
            if remove:
                if state.has(self.item_id_to_name[i+2], self.player):
                    return self.item_id_to_name[i+2]
                if state.has(self.item_id_to_name[i+1], self.player):
                    return self.item_id_to_name[i+1]
                return self.item_id_to_name[i]
            
            if state.has(self.item_id_to_name[i+2], self.player):
                return self.item_id_to_name[i+2]
            if state.has(self.item_id_to_name[i+1], self.player):
                return self.item_id_to_name[i+2]
            if state.has(self.item_id_to_name[i], self.player):
                return self.item_id_to_name[i+1]
            return self.item_id_to_name[i]
        return item.name

    @classmethod
    def stage_generate_output(cls, multiworld, output_directory):
        for location in multiworld.get_filled_locations():
            # The externalplacements.yaml file is only supposed to contain items placed outside the player's game,
            # and checking that items are non-local takes care of filtering out events.
            if (location.item.game == "Final Fantasy Mystic Quest"
                    and location.player != location.item.player and location.item.name not in fillers):
                multiworld.worlds[location.item.player].hint_data.append(location)

        for world in multiworld.get_game_worlds("Final Fantasy Mystic Quest"):
            world.finished_hint_data_collection.set()

    def modify_multidata(self, multidata):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            payload = multidata["connect_names"][self.multiworld.player_name[self.player]]
            multidata["connect_names"][new_name] = payload

    def get_filler_item_name(self):
        r = self.multiworld.random.randint(0, 201)
        for item, count in fillers.items():
            r -= count
            r -= fillers[item]
            if r <= 0:
                return item

    def extend_hint_information(self, hint_data):
        hint_data[self.player] = {}
        if self.options.map_shuffle:
            single_location_regions = ["Subregion Volcano Battlefield", "Subregion Mac's Ship", "Subregion Doom Castle"]
            for subregion in ["Subregion Foresta", "Subregion Aquaria", "Subregion Frozen Fields", "Subregion Fireburg",
                              "Subregion Volcano Battlefield", "Subregion Windia", "Subregion Mac's Ship",
                              "Subregion Doom Castle"]:
                region = self.multiworld.get_region(subregion, self.player)
                for location in region.locations:
                    if location.address and self.options.overworld_shuffle:
                        hint_data[self.player][location.address] = (subregion.split("Subregion ")[-1]
                                                                    + (" Region" if subregion not in
                                                                       single_location_regions else ""))
                for overworld_spot in region.exits:
                    if ("Subregion" in overworld_spot.connected_region.name or
                            overworld_spot.name == "Overworld - Mac Ship Doom" or "Focus Tower" in overworld_spot.name
                            or "Doom Castle" in overworld_spot.name or overworld_spot.name == "Overworld - Giant Tree"):
                        continue
                    exits = list(overworld_spot.connected_region.exits) + [overworld_spot]
                    checked_regions = set()
                    while exits:
                        exit_check = exits.pop()
                        if (exit_check.connected_region not in checked_regions and "Subregion" not in
                                exit_check.connected_region.name):
                            checked_regions.add(exit_check.connected_region)
                            exits.extend(exit_check.connected_region.exits)
                            for location in exit_check.connected_region.locations:
                                if location.address:
                                    hint = []
                                    if self.options.overworld_shuffle:
                                        hint.append((subregion.split("Subregion ")[-1] + (" Region" if subregion not
                                                    in single_location_regions else "")))
                                    if self.options.map_shuffle:
                                        hint.append(overworld_spot.name.split("Overworld - ")[-1].replace("Pazuzu",
                                            "Pazuzu's"))
                                    hint = " - ".join(hint).replace(" - Mac Ship", "")
                                    if location.address in hint_data[self.player]:
                                        hint_data[self.player][location.address] += f"/{hint}"
                                    else:
                                        hint_data[self.player][location.address] = hint

    def fill_slot_data(self):
        ret = self.options.as_dict("logic", "sky_coin_mode", "shattered_sky_coin_quantity", "map_shuffle",
                                   "overworld_shuffle", "crest_shuffle", "shuffle_battlefield_rewards",
                                   "companions_locations", "kaelis_mom_fight_minotaur")
        ret["map_shuffle_seed"] = self.map_shuffle_seed
        return ret

    @staticmethod
    def interpret_slot_data(slot_data):
        return slot_data
