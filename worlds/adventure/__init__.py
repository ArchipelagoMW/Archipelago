import copy
import math
import os
import typing
from typing import ClassVar, Dict, Optional, Tuple

import settings
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial, LocationProgressType
from Utils import __version__
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, SuffixIdentifier
from .Items import item_table, ItemData, nothing_item_id, event_table, AdventureItem, standard_item_max
from .Locations import location_table, base_location_id, LocationData, get_random_room_in_regions
from .Offsets import static_item_data_location, items_ram_start, static_item_element_size, item_position_table, \
    static_first_dragon_index, connector_port_offset, yorgle_speed_data_location, grundle_speed_data_location, \
    rhindle_speed_data_location, item_ram_addresses, start_castle_values, start_castle_offset
from .Options import DragonRandoType, DifficultySwitchA, DifficultySwitchB, AdventureOptions
from .Regions import create_regions
from .Rom import get_base_rom_bytes, get_base_rom_path, AdventureDeltaPatch, apply_basepatch, AdventureAutoCollectLocation
from .Rules import set_rules

# Adventure
components.append(Component('Adventure Client', 'AdventureClient', file_identifier=SuffixIdentifier('.apadvn')))


class AdventureSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """
        File name of the standard NTSC Adventure rom.
        The licensed "The 80 Classic Games" CD-ROM contains this.
        It may also have a .a26 extension
        """
        copy_to = "ADVNTURE.BIN"
        description = "Adventure ROM File"
        md5s = [AdventureDeltaPatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
        True for operating system default program for '.a26'
        Alternatively, a path to a program to open the .a26 file with (generally EmuHawk for multiworld)
        """

    class RomArgs(str):
        """
        Optional, additional args passed into rom_start before the .bin file
        For example, this can be used to autoload the connector script in BizHawk
        (see BizHawk --lua= option)
        Windows example:
        rom_args: "--lua=C:/ProgramData/Archipelago/data/lua/connector_adventure.lua"
        """

    class DisplayMsgs(settings.Bool):
        """Set this to true to display item received messages in EmuHawk"""

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True
    rom_args: Optional[RomArgs] = " "
    display_msgs: typing.Union[DisplayMsgs, bool] = True


class AdventureWeb(WebWorld):
    theme = "dirt"

    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Adventure for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["JusticePS"]
    )

    setup_fr = Tutorial(
        "Guide de configuration Multimonde",
        "Un guide pour configurer Adventure MultiWorld",
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["TheLynk"]
    )

    tutorials = [setup, setup_fr]


def get_item_position_data_start(table_index: int):
    item_ram_address = item_ram_addresses[table_index]
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

    options_dataclass = AdventureOptions
    settings: ClassVar[AdventureSettings]
    item_name_to_id: ClassVar[Dict[str, int]] = {name: data.id for name, data in item_table.items()}
    location_name_to_id: ClassVar[Dict[str, int]] = {name: data.location_id for name, data in location_table.items()}
    required_client_version: Tuple[int, int, int] = (0, 3, 9)

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name: Optional[bytearray] = bytearray("", "utf8" )
        self.dragon_rooms: [int] = [0x14, 0x19, 0x4]
        self.dragon_slay_check: Optional[int] = 0
        self.connector_multi_slot: Optional[int] = 0
        self.dragon_rando_type: Optional[int] = 0
        self.yorgle_speed: Optional[int] = 2
        self.yorgle_min_speed: Optional[int] = 2
        self.grundle_speed: Optional[int] = 2
        self.grundle_min_speed: Optional[int] = 2
        self.rhindle_speed: Optional[int] = 3
        self.rhindle_min_speed: Optional[int] = 3
        self.difficulty_switch_a: Optional[int] = 0
        self.difficulty_switch_b: Optional[int] = 0
        self.start_castle: Optional[int] = 0
        # dict of item names -> list of speed deltas
        self.dragon_speed_reducer_info: {} = {}
        self.created_items: int = 0

    @classmethod
    def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
        # don't need rom anymore
        pass

    def place_random_dragon(self, dragon_index: int):
        region_list = ["Overworld", "YellowCastle", "BlackCastle", "WhiteCastle"]
        self.dragon_rooms[dragon_index] = get_random_room_in_regions(region_list, self.multiworld.random)

    def generate_early(self) -> None:
        self.rom_name = \
            bytearray(f"ADVENTURE{__version__.replace('.', '')[:3]}_{self.player}_{self.multiworld.seed}", "utf8")[:21]
        self.rom_name.extend([0] * (21 - len(self.rom_name)))

        self.dragon_rando_type = self.options.dragon_rando_type.value
        self.dragon_slay_check = self.options.dragon_slay_check.value
        self.connector_multi_slot = self.options.connector_multi_slot.value
        self.yorgle_speed = self.options.yorgle_speed.value
        self.yorgle_min_speed = self.options.yorgle_min_speed.value
        self.grundle_speed = self.options.grundle_speed.value
        self.grundle_min_speed = self.options.grundle_min_speed.value
        self.rhindle_speed = self.options.rhindle_speed.value
        self.rhindle_min_speed = self.options.rhindle_min_speed.value
        self.difficulty_switch_a = self.options.difficulty_switch_a.value
        self.difficulty_switch_b = self.options.difficulty_switch_b.value
        self.start_castle = self.options.start_castle.value
        self.created_items = 0

        if self.dragon_slay_check == 0:
            item_table["Sword"].classification = ItemClassification.useful
        else:
            item_table["Sword"].classification = ItemClassification.progression
            if self.difficulty_switch_b == DifficultySwitchB.option_hard_with_unlock_item:
                item_table["Right Difficulty Switch"].classification = ItemClassification.progression

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
        for event in map(self.create_item, event_table):
            self.multiworld.itempool.append(event)
        exclude = [item for item in self.multiworld.precollected_items[self.player]]
        self.created_items = 0
        for item in map(self.create_item, item_table):
            if item.code == nothing_item_id:
                continue
            if item in exclude and item.code <= standard_item_max:
                exclude.remove(item)  # this is destructive. create unique list above
            else:
                if item.code <= standard_item_max:
                    self.multiworld.itempool.append(item)
                    self.created_items += 1
        num_locations = len(location_table) - 1  # subtract out the chalice location
        if self.dragon_slay_check == 0:
            num_locations -= 3

        if self.difficulty_switch_a == DifficultySwitchA.option_hard_with_unlock_item:
            self.multiworld.itempool.append(self.create_item("Left Difficulty Switch"))
            self.created_items += 1
        if self.difficulty_switch_b == DifficultySwitchB.option_hard_with_unlock_item:
            self.multiworld.itempool.append(self.create_item("Right Difficulty Switch"))
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
        freeincarnate_max = self.options.freeincarnate_max.value
        actual_freeincarnates = min(extra_filler_count, freeincarnate_max)
        self.multiworld.itempool += [self.create_item("Freeincarnate") for _ in range(actual_freeincarnates)]
        self.created_items += actual_freeincarnates

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
        create_regions(self.options, self.multiworld, self.player, self.dragon_rooms)

    set_rules = set_rules

    def generate_basic(self) -> None:
        self.multiworld.get_location("Chalice Home", self.player).place_locked_item(
            self.create_event("Victory", ItemClassification.progression))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def pre_fill(self):
        # Place empty items in filler locations here, to limit
        # the number of exported empty items and the density of stuff in overworld.
        max_location_count = len(location_table) - 1
        if self.dragon_slay_check == 0:
            max_location_count -= 3

        force_empty_item_count = (max_location_count - self.created_items)
        if force_empty_item_count <= 0:
            return
        overworld = self.multiworld.get_region("Overworld", self.player)
        overworld_locations_copy = overworld.locations.copy()
        all_locations = self.multiworld.get_locations(self.player)

        locations_copy = list(all_locations)
        for loc in all_locations:
            if loc.item is not None or loc.progress_type != LocationProgressType.DEFAULT:
                locations_copy.remove(loc)
                if loc in overworld_locations_copy:
                    overworld_locations_copy.remove(loc)

        # guarantee at least one overworld location, so we can for sure get a key somewhere
        # if too much stuff is plando'd though, just let it go
        if len(overworld_locations_copy) >= 3:
            saved_overworld_loc = self.multiworld.random.choice(overworld_locations_copy)
            locations_copy.remove(saved_overworld_loc)
            overworld_locations_copy.remove(saved_overworld_loc)

            # if we have few items, enforce another overworld slot, fill a hard slot, and ensure we have
            # at least one hard slot available
            if self.created_items < 15:
                hard_locations = []
                for loc in locations_copy:
                    if "Vault" in loc.name or "Credits" in loc.name:
                        hard_locations.append(loc)
                force_empty_item_count -= 1
                loc = self.multiworld.random.choice(hard_locations)
                loc.place_locked_item(self.create_item('nothing'))
                hard_locations.remove(loc)
                locations_copy.remove(loc)

                loc = self.multiworld.random.choice(hard_locations)
                locations_copy.remove(loc)
                hard_locations.remove(loc)

                saved_overworld_loc = self.multiworld.random.choice(overworld_locations_copy)
                locations_copy.remove(saved_overworld_loc)
                overworld_locations_copy.remove(saved_overworld_loc)

            # if we have very few items, fill another two difficult slots
            if self.created_items < 10:
                for i in range(2):
                    force_empty_item_count -= 1
                    loc = self.multiworld.random.choice(hard_locations)
                    loc.place_locked_item(self.create_item('nothing'))
                    hard_locations.remove(loc)
                    locations_copy.remove(loc)

            # for the absolute minimum number of items, enforce a third overworld slot
            if self.created_items <= 7:
                saved_overworld_loc = self.multiworld.random.choice(overworld_locations_copy)
                locations_copy.remove(saved_overworld_loc)
                overworld_locations_copy.remove(saved_overworld_loc)

        # finally, place nothing items
        while force_empty_item_count > 0 and locations_copy:
            force_empty_item_count -= 1
            # prefer somewhat to thin out the overworld.
            if len(overworld_locations_copy) > 0 and self.multiworld.random.randint(0, 10) < 4:
                loc = self.multiworld.random.choice(overworld_locations_copy)
            else:
                loc = self.multiworld.random.choice(locations_copy)
            loc.place_locked_item(self.create_item('nothing'))
            locations_copy.remove(loc)
            if loc in overworld_locations_copy:
                overworld_locations_copy.remove(loc)

    def place_dragons(self, rom_deltas: {int, int}):
        for i in range(3):
            table_index = static_first_dragon_index + i
            item_position_data_start = get_item_position_data_start(table_index)
            rom_deltas[item_position_data_start] = self.dragon_rooms[i]

    def set_dragon_speeds(self, rom_deltas: {int, int}):
        rom_deltas[yorgle_speed_data_location] = self.yorgle_speed
        rom_deltas[grundle_speed_data_location] = self.grundle_speed
        rom_deltas[rhindle_speed_data_location] = self.rhindle_speed

    def set_start_castle(self, rom_deltas):
        start_castle_value = start_castle_values[self.start_castle]
        rom_deltas[start_castle_offset] = start_castle_value

    def generate_output(self, output_directory: str) -> None:
        rom_path: str = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.bin")
        foreign_item_locations: [LocationData] = []
        auto_collect_locations: [AdventureAutoCollectLocation] = []
        local_item_to_location: {int, int} = {}
        bat_no_touch_locs: [LocationData] = []
        bat_logic: int = self.options.bat_logic.value
        try:
            rom_deltas: { int, int } = {}
            self.place_dragons(rom_deltas)
            self.set_dragon_speeds(rom_deltas)
            self.set_start_castle(rom_deltas)
            # start and stop indices are offsets in the ROM file, not Adventure ROM addresses (which start at f000)

            # This places the local items (I still need to make it easy to inject the offset data)
            unplaced_local_items = dict(filter(lambda x: nothing_item_id < x[1].id <= standard_item_max,
                                               item_table.items()))
            for location in self.multiworld.get_locations(self.player):
                # 'nothing' items, which are autocollected when the room is entered
                if location.item.player == self.player and \
                        location.item.name == "nothing":
                    location_data = location_table[location.name]
                    room_id = location_data.get_random_room_id(self.random)
                    auto_collect_locations.append(AdventureAutoCollectLocation(location_data.short_location_id,
                                                                               room_id))
                # standard Adventure items, which are placed in the rom
                elif location.item.player == self.player and \
                        location.item.name != "nothing" and \
                        location.item.code is not None and \
                        location.item.code <= standard_item_max:
                    # I need many of the intermediate values here.
                    item_table_offset = item_table[location.item.name].table_index * static_item_element_size
                    item_ram_address = item_ram_addresses[item_table[location.item.name].table_index]
                    item_position_data_start = item_position_table + item_ram_address - items_ram_start
                    location_data = location_table[location.name]
                    (room_id, room_x, room_y) = \
                        location_data.get_random_position(self.random)
                    if location_data.needs_bat_logic and bat_logic == 0x0:
                        copied_location = copy.copy(location_data)
                        copied_location.local_item = item_ram_address
                        copied_location.room_id = room_id
                        copied_location.room_x = room_x
                        copied_location.room_y = room_y
                        bat_no_touch_locs.append(copied_location)
                    del unplaced_local_items[location.item.name]

                    rom_deltas[item_position_data_start] = room_id
                    rom_deltas[item_position_data_start + 1] = room_x
                    rom_deltas[item_position_data_start + 2] = room_y
                    local_item_to_location[item_table_offset] = self.location_name_to_id[location.name] \
                                                              - base_location_id
                # items from other worlds, and non-standard Adventure items handled by script, like difficulty switches
                elif location.item.code is not None:
                    if location.item.code != nothing_item_id:
                        location_data = copy.copy(location_table[location.name])
                        (room_id, room_x, room_y) = \
                            location_data.get_random_position(self.random)
                        location_data.room_id = room_id
                        location_data.room_x = room_x
                        location_data.room_y = room_y
                        foreign_item_locations.append(location_data)
                        if location_data.needs_bat_logic and bat_logic == 0x0:
                            bat_no_touch_locs.append(location_data)
                    else:
                        location_data = location_table[location.name]
                        room_id = location_data.get_random_room_id(self.random)
                        auto_collect_locations.append(AdventureAutoCollectLocation(location_data.short_location_id,
                                                                                   room_id))
            # Adventure items that are in another world get put in an invalid room until needed
            for unplaced_item_name, unplaced_item in unplaced_local_items.items():
                item_position_data_start = get_item_position_data_start(unplaced_item.table_index)
                rom_deltas[item_position_data_start] = 0xff

            if self.options.connector_multi_slot.value:
                rom_deltas[connector_port_offset] = (self.player & 0xff)
            else:
                rom_deltas[connector_port_offset] = 0
        except Exception as e:
            raise e
        else:
            patch = AdventureDeltaPatch(os.path.splitext(rom_path)[0] + AdventureDeltaPatch.patch_file_ending,
                                        player=self.player, player_name=self.multiworld.player_name[self.player],
                                        locations=foreign_item_locations,
                                        autocollect=auto_collect_locations, local_item_locations=local_item_to_location,
                                        dragon_speed_reducer_info=self.dragon_speed_reducer_info,
                                        diff_a_mode=self.difficulty_switch_a, diff_b_mode=self.difficulty_switch_b,
                                        bat_logic=bat_logic, bat_no_touch_locations=bat_no_touch_locs,
                                        rom_deltas=rom_deltas,
                                        seed_name=bytes(self.multiworld.seed_name, encoding="ascii"))
            patch.write()
        finally:
            if os.path.exists(rom_path):
                os.unlink(rom_path)

    # end of ordered Main.py calls

    def create_item(self, name: str) -> Item:
        item_data: ItemData = item_table[name]
        return AdventureItem(name, item_data.classification, item_data.id, self.player)

    def create_event(self, name: str, classification: ItemClassification) -> Item:
        return AdventureItem(name, classification, None, self.player)
