import base64
import itertools
import math
import os
from enum import IntFlag
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from BaseClasses import Entrance, Item, ItemClassification, MultiWorld, Region, Tutorial, \
    LocationProgressType
from Main import __version__
from Options import AssembleOptions
from worlds.AutoWorld import WebWorld, World
from Fill import fill_restrictive
from worlds.generic.Rules import add_rule, set_rule
# from .Client import L2ACSNIClient  # noqa: F401
from .Options import adventure_option_definitions, DragonRandoType, DifficultySwitchA
from .Rom import get_base_rom_bytes, get_base_rom_path, AdventureDeltaPatch, apply_basepatch, \
    AdventureAutoCollectLocation
from .Items import item_table, ItemData, nothing_item_id, event_table, AdventureItem, standard_item_max
from .Locations import location_table, base_location_id, LocationData, get_random_room_in_regions
from .Offsets import static_item_data_location, items_ram_start, static_item_element_size, item_position_table, \
    static_first_dragon_index, connector_port_offset, yorgle_speed_data_location, grundle_speed_data_location, \
    rhindle_speed_data_location
from .Regions import create_regions
from .Rules import set_rules


class AdventureWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Adventure for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["word_fcuk"]
    )]
    theme = "dirt"


def get_item_position_data_start(rom_bytearray: bytearray, table_index: int):
    item_table_offset = table_index * static_item_element_size
    static_item = static_item_data_location + item_table_offset
    item_ram_address = rom_bytearray[static_item]
    return item_position_table + item_ram_address - items_ram_start


class AdventureWorld(World):
    """
    Adventure for the Atari 2600 is an early graphical adventure game.
    Find the enchanted chalice and return it to the yellow castle,
    using magic items to enter hidden rooms, retrieve out of
    reach items, or defeat the three dragons.  Beware the bat
    who likes to steal your equipment!
    """
    game: ClassVar[str] = "Adventure"
    web: ClassVar[WebWorld] = AdventureWeb()

    option_definitions: ClassVar[Dict[str, AssembleOptions]] = adventure_option_definitions
    item_name_to_id: ClassVar[Dict[str, int]] = {name: data.id for name, data in item_table.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = {name: data.location_id for name, data in location_table.items()}
    # # item_name_groups: ClassVar[Dict[str, Set[str]]] = {
    # #   "Blue chest items": {name for name, data in adventure_item_table.items() if data.type is ItemType.BLUE_CHEST},
    # # }
    data_version: ClassVar[int] = 0
    required_client_version: Tuple[int, int, int] = (0, 3, 6)

    # adventure specific properties
    rom_name: Optional[bytearray]

    # definitely a bunch of things I COULD put in here, but right now won't
    item_rando_type: Optional[int]
    dragon_slay_check: Optional[int]
    trap_bat_check: Optional[int]
    bat_logic: Optional[int]
    freeincarnate_max: Optional[int]
    dragon_rando_type: Optional[int]
    connector_multi_slot: Optional[int]
    yorgle_speed: Optional[int]
    yorgle_min_speed: Optional[int]
    grundle_speed: Optional[int]
    grundle_min_speed: Optional[int]
    rhindle_speed: Optional[int]
    rhindle_min_speed: Optional[int]
    difficulty_switch_a: Optional[int]
    difficulty_switch_b: Optional[int]

    dragon_rooms: [str]
    created_items: int

    # dict of item names -> list of speed deltas
    dragon_speed_reducer_info: {}

    @classmethod
    def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    def place_random_dragon(self, dragon_index: int):
        region_list = ["Overworld", "YellowCastle", "BlackCastle", "WhiteCastle"]
        self.dragon_rooms[dragon_index] = get_random_room_in_regions(region_list, self.multiworld.random)

    def generate_early(self) -> None:
        self.rom_name = \
            bytearray(f"ADVENTURE{__version__.replace('.', '')[:3]}_{self.player}_{self.multiworld.seed}", "utf8")[:21]
        self.rom_name.extend([0] * (21 - len(self.rom_name)))

        self.item_rando_type = self.multiworld.item_rando_type[self.player].value
        self.dragon_slay_check = self.multiworld.dragon_slay_check[self.player].value
        self.trap_bat_check = self.multiworld.trap_bat_check[self.player].value
        self.bat_logic = self.multiworld.bat_logic[self.player].value
        self.freeincarnate_max = self.multiworld.freeincarnate_max[self.player].value
        self.dragon_rando_type = self.multiworld.dragon_rando_type[self.player].value
        self.connector_multi_slot = self.multiworld.connector_multi_slot[self.player].value
        self.yorgle_speed = self.multiworld.yorgle_speed[self.player].value
        self.yorgle_min_speed = self.multiworld.yorgle_min_speed[self.player].value
        self.grundle_speed = self.multiworld.grundle_speed[self.player].value
        self.grundle_min_speed = self.multiworld.grundle_min_speed[self.player].value
        self.rhindle_speed = self.multiworld.rhindle_speed[self.player].value
        self.rhindle_min_speed = self.multiworld.rhindle_min_speed[self.player].value
        self.difficulty_switch_a = self.multiworld.difficulty_switch_a[self.player].value
        self.difficulty_switch_b = self.multiworld.difficulty_switch_b[self.player].value
        self.created_items = 0

        if self.dragon_slay_check == 0:
            item_table["Sword"].classification = ItemClassification.useful
        else:
            item_table["Sword"].classification = ItemClassification.progression

        self.dragon_rooms = [0x14, 0x19, 0x4]
        if self.dragon_rando_type == DragonRandoType.option_shuffle:
            self.multiworld.random.shuffle(self.dragon_rooms)
        elif self.dragon_rando_type == DragonRandoType.option_overworldplus:
            dragon_indices = [0, 1, 2]
            overworld_forced_index = self.multiworld.random.choice(dragon_indices)
            dragon_indices.remove(overworld_forced_index)
            region_list = ["Overworld"]
            self.dragon_rooms[overworld_forced_index] = get_random_room_in_regions(region_list, self.multiworld.random)
            self.place_random_dragon(dragon_indices[0])
            self.place_random_dragon(dragon_indices[1])
        elif self.dragon_rando_type == DragonRandoType.option_randomized:
            self.place_random_dragon(0)
            self.place_random_dragon(1)
            self.place_random_dragon(2)

    def create_items(self) -> None:
        self.item_name_to_id["nothing"] = nothing_item_id
        self.item_id_to_name[nothing_item_id] = "nothing"
        for event in map(self.create_item, event_table):
            self.multiworld.itempool.append(event)
        exclude = [item for item in self.multiworld.precollected_items[self.player]]
        self.created_items = 0
        for item in map(self.create_item, item_table):
            if item in exclude and item.code <= standard_item_max:
                exclude.remove(item)  # this is destructive. create unique list above
                self.multiworld.itempool.append(self.create_item("nothing"))
                self.created_items += 1
            else:
                if item.code <= standard_item_max:
                    self.multiworld.itempool.append(item)
                    self.created_items += 1
        num_locations = len(location_table) - 1  # subtract out the chalice location

        if self.difficulty_switch_a == DifficultySwitchA.option_hard_with_unlock_item:
            self.multiworld.itempool.append(self.create_item("Difficulty Switch A"))
            self.created_items += 1
        if self.difficulty_switch_b == DifficultySwitchA.option_hard_with_unlock_item:
            self.multiworld.itempool.append(self.create_item("Difficulty Switch B"))
            self.created_items += 1

        extra_filler_count = num_locations - self.created_items
        self.dragon_speed_reducer_info = {}
        # make sure yorgle doesn't take 2 if there's not enough for the others to get at least one
        if extra_filler_count <= 4:
            extra_filler_count = 1
        self.create_dragon_slow_items(self.yorgle_min_speed, self.yorgle_speed, "Slow Yorgle", extra_filler_count)
        extra_filler_count = num_locations - self.created_items

        if extra_filler_count <= 3:
            extra_filler_count = 1
        self.create_dragon_slow_items(self.grundle_min_speed, self.grundle_speed, "Slow Grundle", extra_filler_count)
        extra_filler_count = num_locations - self.created_items

        self.create_dragon_slow_items(self.rhindle_min_speed, self.rhindle_speed, "Slow Rhindle", extra_filler_count)
        extra_filler_count = num_locations - self.created_items

        # traps would probably go here, if enabled

        actual_freeincarnates = min(extra_filler_count, self.freeincarnate_max)
        self.multiworld.itempool += [self.create_item("Freeincarnate") for _ in range(actual_freeincarnates)]
        self.created_items += actual_freeincarnates

        extra_filler_count = num_locations - self.created_items
        self.multiworld.itempool += [self.create_item("nothing") for _ in range(extra_filler_count)]


    def create_dragon_slow_items(self, min_speed: int, speed: int, item_name: str, maximum_items: int):
        if min_speed < speed:
            delta = speed - min_speed
            if delta > 2 and maximum_items >= 2:
                self.multiworld.itempool.append(self.create_item(item_name))
                self.multiworld.itempool.append(self.create_item(item_name))
                speed_with_one = speed - math.floor(delta / 2)
                self.dragon_speed_reducer_info[item_table[item_name].id] = [speed_with_one, min_speed]
                self.created_items += 2
            elif maximum_items >= 1:
                self.multiworld.itempool.append(self.create_item(item_name))
                self.dragon_speed_reducer_info[item_table[item_name].id] = [min_speed]
                self.created_items += 1

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        self.multiworld.get_location("Chalice Home", self.player).place_locked_item(
            self.create_event("Victory", ItemClassification.progression))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def pre_fill(self):
        # Place empty items in filler locations here, to limit
        # the number of exported empty items and the density of stuff in overworld.
        overworld = self.multiworld.get_region("Overworld", self.player)
        overworld_locations_copy = overworld.locations.copy()
        all_locations = self.multiworld.get_locations(self.player)
        total_location_count = len(all_locations)
        locations_copy = all_locations.copy()
        for loc in all_locations:
            if loc.item is not None or loc.progress_type != LocationProgressType.DEFAULT:
                locations_copy.remove(loc)
                if loc in overworld_locations_copy:
                    overworld_locations_copy.remove(loc)

        # unfilled_locations = len(locations_copy)
        # filled_locations = len(overworld.locations) - unfilled_locations
        force_empty_item_count = (total_location_count - self.created_items)
        nothing_items = list(filter(lambda i: i.name == "nothing", self.multiworld.itempool))
        # guarantee at least one overworld location, so we can for sure get a key somewhere
        saved_overworld_loc = self.multiworld.random.choice(overworld_locations_copy)
        locations_copy.remove(saved_overworld_loc)
        overworld_locations_copy.remove(saved_overworld_loc)
        while force_empty_item_count > 0 and len(locations_copy) > 0 and len(nothing_items) > 0:
            force_empty_item_count -= 1
            # prefer somewhat to thin out the overworld.
            if len(overworld_locations_copy) > 0 and self.multiworld.random.randint(0, 10) < 4:
                loc = self.multiworld.random.choice(overworld_locations_copy)
            else:
                loc = self.multiworld.random.choice(locations_copy)
            item = nothing_items.pop()
            loc.place_locked_item(item)
            locations_copy.remove(loc)
            if loc in overworld_locations_copy:
                overworld_locations_copy.remove(loc)
            self.multiworld.itempool.remove(item)

    def place_dragons(self, rom_bytearray: bytearray):
        for i in range(3):
            table_index = static_first_dragon_index + i
            item_position_data_start = get_item_position_data_start(rom_bytearray, table_index)
            rom_bytearray[item_position_data_start:item_position_data_start + 1] = \
                self.dragon_rooms[i].to_bytes(1, "little")

    def set_dragon_speeds(self, rom_bytearray: bytearray):
        rom_bytearray[yorgle_speed_data_location:yorgle_speed_data_location + 1] = \
            self.yorgle_speed.to_bytes(1, "little")
        rom_bytearray[grundle_speed_data_location:grundle_speed_data_location + 1] = \
            self.grundle_speed.to_bytes(1, "little")
        rom_bytearray[rhindle_speed_data_location:rhindle_speed_data_location + 1] = \
            self.rhindle_speed.to_bytes(1, "little")

    def generate_output(self, output_directory: str) -> None:
        rom_path: str = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.bin")
        foreign_item_locations: [LocationData] = []
        auto_collect_locations: [AdventureAutoCollectLocation] = []
        local_item_to_location: {int, int} = {}
        try:
            rom_bytearray = bytearray(apply_basepatch(get_base_rom_bytes()))
            self.place_dragons(rom_bytearray)
            self.set_dragon_speeds(rom_bytearray)
            # start and stop indices are offsets in the ROM file, not Adventure ROM addresses (which start at f000)

            # This places the local items (I still need to make it easy to inject the offset data)
            unplaced_local_items = dict(filter(lambda x: x[1].id <= standard_item_max, item_table.items()))
            for location in self.multiworld.get_locations(self.player):
                # 'nothing' items, which are autocollected when the room is entered
                if location.item.player == self.player and \
                        location.item.name == "nothing":
                    location_data = location_table[location.name]
                    auto_collect_locations.append(AdventureAutoCollectLocation(location_data.short_location_id,
                                                                               location_data.room_id))
                # standard Adventure items, which are placed in the rom
                elif location.item.player == self.player and \
                        location.item.name != "nothing" and \
                        location.item.code is not None and \
                        location.item.code <= standard_item_max:
                    # I need many of the intermediate values here.
                    item_table_offset = item_table[location.item.name].table_index * static_item_element_size
                    static_item = static_item_data_location + item_table_offset
                    item_ram_address = rom_bytearray[static_item]
                    item_position_data_start = item_position_table + item_ram_address - items_ram_start
                    location_data = location_table[location.name]
                    room_x, room_y = location_data.get_position(self.multiworld.per_slot_randoms[self.player])

                    del unplaced_local_items[location.item.name]

                    rom_bytearray[item_position_data_start:item_position_data_start + 1] = \
                        location_data.room_id.to_bytes(1, "little")
                    rom_bytearray[item_position_data_start + 1: item_position_data_start + 2] = \
                        room_x.to_bytes(1, "little")
                    rom_bytearray[item_position_data_start + 2: item_position_data_start + 3] = \
                        room_y.to_bytes(1, "little")
                    local_item_to_location[item_table_offset] = self.location_name_to_id[location.name] \
                                                              - base_location_id
                # items from other worlds, and non-standard Adventure items handled by script, like difficulty switches
                elif location.item.code is not None:
                    if location.item.code != nothing_item_id:
                        location_data = location_table[location.name]
                        foreign_item_locations.append(location_data)
                    else:
                        location_data = location_table[location.name]
                        auto_collect_locations.append(AdventureAutoCollectLocation(location_data.short_location_id,
                                                                                   location_data.room_id))
            # Adventure items that are in another world get put in an invalid room until needed
            for unplaced_item_name, unplaced_item in unplaced_local_items.items():
                item_position_data_start = get_item_position_data_start(rom_bytearray, unplaced_item.table_index)
                rom_bytearray[item_position_data_start:item_position_data_start + 1] = 0xff.to_bytes(1, "little")

            if self.connector_multi_slot:
                rom_bytearray[connector_port_offset:connector_port_offset + 1] = \
                    (self.player & 0xff).to_bytes(1, "little")
            else:
                rom_bytearray[connector_port_offset:connector_port_offset + 1] = (0).to_bytes(1, "little")
            with open(rom_path, "wb") as f:
                f.write(rom_bytearray)
        except Exception as e:
            raise e
        else:
            patch = AdventureDeltaPatch(os.path.splitext(rom_path)[0] + AdventureDeltaPatch.patch_file_ending,
                                        player=self.player, player_name=self.multiworld.player_name[self.player],
                                        patched_path=rom_path, locations=foreign_item_locations,
                                        autocollect=auto_collect_locations, local_item_locations=local_item_to_location,
                                        dragon_speed_reducer_info=self.dragon_speed_reducer_info,
                                        diff_a_mode=self.difficulty_switch_a, diff_b_mode=self.difficulty_switch_b,
                                        bat_logic=self.bat_logic,
                                        seed_name=bytes(self.multiworld.seed_name, encoding="ascii"))
            patch.write()
        finally:
            if os.path.exists(rom_path):
                os.unlink(rom_path)

    # end of ordered Main.py calls

    def create_item(self, name: str) -> Item:
        if name == "nothing":
            return AdventureItem(name, ItemClassification.filler, nothing_item_id, self.player)
        item_data: ItemData = item_table.get(name)
        return AdventureItem(name, item_data.classification, item_data.id, self.player)

    def create_event(self, name: str, classification: ItemClassification) -> Item:
        return AdventureItem(name, classification, None, self.player)
