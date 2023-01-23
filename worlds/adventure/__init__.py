import base64
import itertools
import os
from enum import IntFlag
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from BaseClasses import Entrance, Item, ItemClassification, MultiWorld, Region, RegionType, Tutorial
from Main import __version__
from Options import AssembleOptions
from worlds.AutoWorld import WebWorld, World
from Fill import fill_restrictive
from worlds.generic.Rules import add_rule, set_rule
# from .Client import L2ACSNIClient  # noqa: F401
from .Options import adventure_option_definitions
from .Rom import get_base_rom_bytes, get_base_rom_path, AdventureDeltaPatch, apply_basepatch
from .Items import item_table, ItemData, nothing_item_id, event_table, AdventureItem
from .Locations import location_table
from .Offsets import static_item_data_location, items_ram_start, static_item_element_size, item_position_table
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

    @classmethod
    def stage_assert_generate(cls, _multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    def generate_early(self) -> None:
        self.rom_name = \
            bytearray(f"ADVENTURE{__version__.replace('.', '')[:3]}_{self.player}_{self.multiworld.seed}", "utf8")[:21]
        self.rom_name.extend([0] * (21 - len(self.rom_name)))

        self.item_rando_type = self.multiworld.item_rando_type[self.player].value
        self.dragon_slay_check = self.multiworld.dragon_slay_check[self.player].value
        self.trap_bat_check = self.multiworld.trap_bat_check[self.player].value
        self.bat_logic = self.multiworld.bat_logic[self.player].value

        if self.dragon_slay_check == 0:
            item_table["Sword"].classification = ItemClassification.useful

    def create_items(self) -> None:
        for event in map(self.create_item, event_table):
            self.multiworld.itempool.append(event)
        exclude = [item for item in self.multiworld.precollected_items[self.player]]
        for item in map(self.create_item, item_table):
            if item in exclude:
                exclude.remove(item)  # this is destructive. create unique list above
                self.multiworld.itempool.append(self.create_item("nothing"))
            else:
                self.multiworld.itempool.append(item)
        num_locations = len(location_table)
        extra_filler_count = num_locations - len(item_table)
        self.multiworld.itempool += [self.create_item("nothing") for _ in range(extra_filler_count)]

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        self.multiworld.get_location("ChaliceHome", self.player).place_locked_item(
            self.create_event("Victory", ItemClassification.progression))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def pre_fill(self):
        # Place a somewhat random number of empty items (or configured in options) in overworld here, to limit
        # the number of exported empty items and the density of stuff in overworld.
        # TODO - Not sure if that's also
        # TODO - the only way to make items be explicitly local?  In which case I might want to optionally place
        # TODO - the chalice or yellow key, based on options.  Or just set exclusion on one/both for overworld.
        # TODO - Probably better to exclude the locations from generation in the first place instead
        # TODO - of putting nothing items in, except that it would mess up plandos.
        # TODO - looks like I can call fill_restrictive to tell AP to fill a set of locations for
        # TODO - this kind of thing?  That would probably make more sense to do than what I'm doing here
        overworld = self.multiworld.get_region("Overworld", self.player)
        locations_copy = overworld.locations.copy()
        for loc in overworld.locations:
            if loc.item is not None:
                locations_copy.remove(loc)

        unfilled_locations = len(locations_copy)
        filled_locations = len(overworld.locations) - unfilled_locations
        # TODO - move range into options
        force_empty_overworld_count = self.multiworld.random.randint(3, 8)
        nothing_items = list(filter(lambda i: i.name == "nothing", self.multiworld.itempool))
        while force_empty_overworld_count > 0 and len(locations_copy) > 0 and len(nothing_items) > 0:
            force_empty_overworld_count -= 1
            loc = self.multiworld.random.choice(locations_copy)
            item = nothing_items.pop()
            loc.place_locked_item(item)
            locations_copy.remove(loc)
            self.multiworld.itempool.remove(item)

    def generate_output(self, output_directory: str) -> None:
        rom_path: str = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.bin")

        try:
            rom_bytearray = bytearray(apply_basepatch(get_base_rom_bytes()))
            # start and stop indices are offsets in the ROM file, not Adventure ROM addresses (which start at f000)
            # rom_bytearray[0x007FC0:0x007FC0 + 21] = self.rom_name
            # rom_bytearray[0x014308:0x014308 + 1] = self.capsule_starting_level.value.to_bytes(1, "little")
            # TODO - Place local items (traditional mode) and drained items (inactive mode) in correct locations
            # TODO - Place non-local items in room 0 offscreen?  Not sure if that actually would work
            # TODO - Might have to place them in some other dummy room - somewhere the player and bat can't reach
            # TODO - but also isn't visible in the start screen
            # This places the local items (I still need to make it easy to inject the offset data)
            for location in self.multiworld.get_locations(self.player):
                if location.item.player == self.player and \
                        location.item.name != "nothing" and \
                        location.item.code is not None:
                    static_item = static_item_data_location + \
                                  item_table[location.item.name].table_index * static_item_element_size
                    print("placing item: " + location.item.name + " " + hex(static_item))
                    item_ram_address = rom_bytearray[static_item]
                    item_position_data_start = item_position_table + item_ram_address - items_ram_start
                    location_data = location_table[location.name]
                    room_x, room_y = location_data.get_position(self.multiworld.random)

                    rom_bytearray[item_position_data_start:item_position_data_start + 1] = \
                        location_data.room_id.to_bytes(1, "little")
                    rom_bytearray[item_position_data_start + 1: item_position_data_start + 2] = \
                        room_x.to_bytes(1, "little")
                    rom_bytearray[item_position_data_start + 2: item_position_data_start + 3] = \
                        room_y.to_bytes(1, "little")

            # TODO - for all remote items in traditional mode, write that out into a file
            # TODO - for the client to read. It will be in charge of placing the Arch objects in
            # TODO - the room when the player enters.  I can't really fit a lot of them in the rom (or ram) data,
            # TODO - and these are useless without the client anyway

            # TODO - for drained items (where the actual drained item will then be forced local?) we set a bit in
            # TODO - the old black and white color byte to indicate if it should start active, and store the
            # TODO - realtime part of that in an empty ram bit or high/low bit of the room byte or something
            # TODO - If the room byte-bit doesn't slow it down too much, that'd be ideal, it'd use no extra RAM then
            with open(rom_path, "wb") as f:
                f.write(rom_bytearray)
        except Exception as e:
            raise e
        else:
            patch = AdventureDeltaPatch(os.path.splitext(rom_path)[0] + AdventureDeltaPatch.patch_file_ending,
                                        player=self.player, player_name=self.multiworld.player_name[self.player],
                                        patched_path=rom_path)
            patch.write()
        finally:
            if os.path.exists(rom_path):
                print("TODO - Unlink rom file!  Leaving it here pending client implementation.")
                # os.unlink(rom_path)

    # end of ordered Main.py calls

    def create_item(self, name: str) -> Item:
        if name == "nothing":
            return AdventureItem(name, ItemClassification.filler, nothing_item_id, self.player)
        item_data: ItemData = item_table.get(name)
        return AdventureItem(name, item_data.classification, item_data.id, self.player)

    def create_event(self, name: str, classification: ItemClassification) -> Item:
        return AdventureItem(name, classification, None, self.player)

    def get_capsule_cravings_table(self) -> bytes:
        rom: bytes = get_base_rom_bytes()

        if self.capsule_cravings_jp_style:
            number_of_items: int = 467
            items_offset: int = 0x0B4F69
            value_thresholds: List[int] = \
                [200, 500, 600, 800, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 12000, 20000, 25000, 29000, 32000, 33000]
            tier_list: List[List[int]] = [list() for _ in value_thresholds[:-1]]

            for item_id in range(number_of_items):
                pointer: int = int.from_bytes(rom[items_offset + 2 * item_id:items_offset + 2 * item_id + 2], "little")
                if rom[items_offset + pointer] & 0x20 == 0 and rom[items_offset + pointer + 1] & 0x40 == 0:
                    value: int = int.from_bytes(rom[items_offset + pointer + 5:items_offset + pointer + 7], "little")
                    for t in range(len(tier_list)):
                        if value_thresholds[t] <= value < value_thresholds[t + 1]:
                            tier_list[t].append(item_id)
                            break
            tier_sizes: List[int] = [len(tier) for tier in tier_list]

            cravings_table: bytes = b"".join(i.to_bytes(2, "little") for i in itertools.chain(
                *zip(itertools.accumulate((2 * tier_size for tier_size in tier_sizes), initial=0x40), tier_sizes),
                (item_id for tier in tier_list for item_id in tier)))
            assert len(cravings_table) == 470, cravings_table
            return cravings_table
        else:
            return rom[0x0AFF16:0x0AFF16 + 470]

    def get_goal_text_bytes(self) -> bytes:
        goal_text: List[str] = []
        iris: str = f"{self.iris_treasures_required} Iris treasure{'s' if self.iris_treasures_required > 1 else ''}"
        if self.goal == Goal.option_boss:
            goal_text = ["You have to defeat", f"the boss on B{self.final_floor}."]
        elif self.goal == Goal.option_iris_treasure_hunt:
            goal_text = ["You have to find", f"{iris}."]
        elif self.goal == Goal.option_boss_iris_treasure_hunt:
            goal_text = ["You have to retrieve", f"{iris} and", f"defeat the boss on B{self.final_floor}."]
        elif self.goal == Goal.option_final_floor:
            goal_text = [f"You need to get to B{self.final_floor}."]
        assert len(goal_text) <= 4 and all(len(line) <= 28 for line in goal_text), goal_text
        goal_text_bytes = bytes((0x08, *b"\x03".join(line.encode("ascii") for line in goal_text), 0x00))
        return goal_text_bytes + b"\x00" * (147 - len(goal_text_bytes))

    @staticmethod
    def get_node_connection_table() -> bytes:
        class Connect(IntFlag):
            TOP_LEFT = 0b00000001
            LEFT = 0b00000010
            BOTTOM_LEFT = 0b00000100
            TOP = 0b00001000
            BOTTOM = 0b00010000
            TOP_RIGHT = 0b00100000
            RIGHT = 0b01000000
            BOTTOM_RIGHT = 0b10000000

        rom: bytes = get_base_rom_bytes()

        return bytes(rom[0x09D59B + ((n & ~Connect.TOP_LEFT if not n & (Connect.TOP | Connect.LEFT) else n) &
                                     (n & ~Connect.TOP_RIGHT if not n & (Connect.TOP | Connect.RIGHT) else n) &
                                     (n & ~Connect.BOTTOM_LEFT if not n & (Connect.BOTTOM | Connect.LEFT) else n) &
                                     (n & ~Connect.BOTTOM_RIGHT if not n & (Connect.BOTTOM | Connect.RIGHT) else n))]
                     for n in range(256))
