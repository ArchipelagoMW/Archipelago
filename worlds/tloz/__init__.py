import json
import os
import threading
from pkgutil import get_data

import bsdiff4
from docutils.parsers.rst.directives import encoding

import Utils
import settings
import typing

from typing import NamedTuple, Union, Dict, Any
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from .ItemPool import generate_itempool, starting_weapons, dangerous_weapon_locations
from .Items import item_table, item_prices, item_game_ids
from .Locations import location_table, level_locations, major_locations, shop_locations, all_level_locations, \
    standard_level_locations, shop_price_location_ids, secret_money_ids, location_ids, food_locations, \
    take_any_locations, sword_cave_locations, shop_categories, cave_data_location_start
from .Options import TlozOptions
from .Rom import TLoZDeltaPatch, get_base_rom_path, first_quest_dungeon_items_early, first_quest_dungeon_items_late, \
    cave_type_flags, warp_cave_offset, starting_sword_cave_location_byte, white_sword_pond_location_byte, \
    magical_sword_grave_location_byte, letter_cave_location_byte, TLOZProcedurePatch
from .Rules import set_rules
from .Client import TLOZClient
from .EntranceRandoRules import create_entrance_randomizer_set
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule


class TLoZSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Zelda 1"""
        description = "The Legend of Zelda (U) ROM File"
        copy_to = "Legend of Zelda, The (U) (PRG0) [!].nes"
        md5s = [TLoZDeltaPatch.hash]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
                    true  for operating system default program
        Alternatively, a path to a program to open the .nes file with
        """

    class DisplayMsgs(settings.Bool):
        """Display message inside of Bizhawk"""

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True
    display_msgs: typing.Union[DisplayMsgs, bool] = True


class TLoZWeb(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up The Legend of Zelda for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rosalie and Figment"]
    )

    tutorials = [setup]


class TLoZWorld(World):
    """
    The Legend of Zelda needs almost no introduction. Gather the eight fragments of the
    Triforce of Wisdom, enter Death Mountain, defeat Ganon, and rescue Princess Zelda.
    This randomizer shuffles all the items in the game around, leading to a new adventure
    every time.
    """
    options_dataclass = TlozOptions
    options: TlozOptions
    settings: typing.ClassVar[TLoZSettings]
    game = "The Legend of Zelda"
    topology_present = True
    base_id = 7000
    web = TLoZWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    item_name_groups = {
        'weapons': starting_weapons,
        'swords': {
            "Sword", "White Sword", "Magical Sword"
        },
        "candles": {
            "Candle", "Red Candle"
        },
        "arrows": {
            "Arrow", "Silver Arrow"
        }
    }

    location_name_groups = {
        "Shops": set(shop_locations),
        "Take Any": set(take_any_locations),
        "Sword Caves": set(sword_cave_locations),
        "Level 1": set(level_locations[0]),
        "Level 2": set(level_locations[1]),
        "Level 3": set(level_locations[2]),
        "Level 4": set(level_locations[3]),
        "Level 5": set(level_locations[4]),
        "Level 6": set(level_locations[5]),
        "Level 7": set(level_locations[6]),
        "Level 8": set(level_locations[7]),
        "Level 9": set(level_locations[8])
    }

    for k, v in item_name_to_id.items():
        item_name_to_id[k] = v + base_id

    for k, v in location_name_to_id.items():
        if v is not None:
            location_name_to_id[k] = v + base_id

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.generator_in_use = threading.Event()
        self.rom_name_available_event = threading.Event()
        self.levels = None
        self.filler_items = None
        self.entrance_randomizer_set = None

    def create_item(self, name: str):
        if name == "Power Bracelet":
            return TLoZItem(
                name,
                item_table[name].classification
                    if self.options.EntranceShuffle.value not in [2, 3, 5]
                    else ItemClassification.progression,
                self.item_name_to_id[name],
                self.player)
        return TLoZItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return TLoZItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name, id, parent, event=False):
        return_location = TLoZLocation(self.player, name, id, parent)
        return return_location

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        overworld = Region("Overworld", self.player, self.multiworld)

        self.entrance_randomizer_set = create_entrance_randomizer_set(self)

        self.levels = [None]  # Yes I'm making a one-indexed array in a zero-indexed language. I hate me too.
        for i in range(1, 10):
            level = Region(f"Level {i}", self.player, self.multiworld)
            self.levels.append(level)
            new_entrance = Entrance(self.player, f"Level {i}", overworld)
            entrando_entrance = [screen for screen, entrance in self.entrance_randomizer_set.items() if entrance[1] == f"Level {i}"][0]
            entrando_rule = self.entrance_randomizer_set[entrando_entrance][0]
            new_entrance.connect(level)
            overworld.connect(
                level,
                f"Level {i} Entrance at {entrando_entrance}",
                lambda state, rule=entrando_rule: rule(state, self.player))
            self.multiworld.regions.append(level)

        for i, level in enumerate(level_locations):
            for location in level:
                if self.options.ExpandedPool or "Drop" not in location:
                    self.levels[i + 1].locations.append(
                        self.create_location(location, self.location_name_to_id[location], self.levels[i + 1]))

        for level in range(1, 9):
            boss_event = self.create_location(f"Level {level} Boss Status", None,
                                              self.multiworld.get_region(f"Level {level}", self.player),
                                              True)
            boss_event.show_in_spoiler = False
            self.levels[level].locations.append(boss_event)

        for location in major_locations:
            if location in sword_cave_locations or location == "Letter Cave":
                region = Region(location, self.player, self.multiworld)
                entrando_screen = [screen for screen, entrance in self.entrance_randomizer_set.items() if entrance[1] == location][0]
                entrando_rule = self.entrance_randomizer_set[entrando_screen][0]
                overworld.connect(region, f"Overworld to {entrando_screen}", lambda state, rule=entrando_rule: rule(state, self.player))
                region.locations.append(
                    self.create_location(location, self.location_name_to_id[location], region))
            elif "Take Any" not in location:
                overworld.locations.append(
                    self.create_location(location, self.location_name_to_id[location], overworld))

        if self.options.ExpandedPool:
            entrando_screens = [screen for screen, entrance in self.entrance_randomizer_set.items() if entrance[1] == "Take Any Item"]
            region = Region("Take Any Item", self.player, self.multiworld)
            for screen in entrando_screens:
                screen_region = Region(screen, self.player, self.multiworld)
                entrando_rule = self.entrance_randomizer_set[screen][0]
                screen_region.connect(
                    region,
                    f"{screen_region} to Take Any Item",
                    lambda state, rule=entrando_rule: rule(state, self.player)
                )
                overworld.connect(screen_region, f"Overworld to {screen}", lambda state: True)
            for location in take_any_locations:
                region.locations.append(
                    self.create_location(location, self.location_name_to_id[location], region)
                )

        for shop_category, shop_slots in shop_categories.items():
            screens = [screen for screen, entrance in self.entrance_randomizer_set.items() if entrance[1] == shop_category]
            shop_region = Region(shop_category, self.player, self.multiworld)
            for screen in screens:
                screen_region = Region(screen, self.player, self.multiworld)
                entrando_rule = self.entrance_randomizer_set[screen][0]
                screen_region.connect(
                    shop_region,
                    f"{screen_region} to {shop_category}",
                    lambda state, rule=entrando_rule: rule(state, self.player))
                overworld.connect(screen_region,
                                  f"Overworld {screen}",
                                  lambda state: True
                                  )
            for shop_slot in shop_slots:
                shop_region.locations.append(
                    self.create_location(shop_slot, self.location_name_to_id[shop_slot], shop_region))

        ganon = self.create_location("Ganon", None, self.multiworld.get_region("Level 9", self.player))
        zelda = self.create_location("Zelda", None, self.multiworld.get_region("Level 9", self.player))
        ganon.show_in_spoiler = False
        zelda.show_in_spoiler = False
        self.levels[9].locations.append(ganon)
        self.levels[9].locations.append(zelda)
        begin_game = Entrance(self.player, "Begin Game", menu)
        menu.exits.append(begin_game)
        begin_game.connect(overworld)
        self.multiworld.regions.append(menu)
        self.multiworld.regions.append(overworld)


    def create_items(self):
        # refer to ItemPool.py
        generate_itempool(self)

    # refer to Rules.py
    set_rules = set_rules

    def generate_basic(self):
        ganon = self.multiworld.get_location("Ganon", self.player)
        ganon.place_locked_item(self.create_event("Triforce of Power"))
        add_rule(ganon, lambda state: state.has("Silver Arrow", self.player) and state.has("Bow", self.player))

        self.multiworld.get_location("Zelda", self.player).place_locked_item(self.create_event("Rescued Zelda!"))
        add_rule(self.multiworld.get_location("Zelda", self.player),
                 lambda state: state.has("Triforce of Power", self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Rescued Zelda!", self.player)

    def generate_output(self, output_directory: str):
        try:
            outfilebase = 'AP_' + self.multiworld.seed_name
            outfilepname = f'_P{self.player}'
            outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
            output_filename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.nes')
            self.rom_name_text = f'LOZ{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
            self.rom_name = self.rom_name_text[:0x20]
            self.rom_name.ljust(0x20, "0")
            self.rom_name = str(self.rom_name)
            placement_dict = self.create_placement_file()
            placement_dict["meta"] = {}
            placement_dict["meta"]["rom_name"] = self.rom_name
            placement_dict["meta"]["player_name"] = self.player_name
            placement_dict["meta"]["output_filename"] = output_filename

            # We shuffle the tiers of rupee caves. Caves that shared a value before still will.
            # Easiest to do it here so we have the multiworld's random object
            secret_caves = self.random.sample(sorted(secret_money_ids), 3)
            secret_cave_money_amounts = [20, 50, 100]
            for i, amount in enumerate(secret_cave_money_amounts):
                # Giving approximately double the money to keep grinding down
                amount = amount * self.random.triangular(1.5, 2.5)
                secret_cave_money_amounts[i] = int(amount)
            for i, cave in enumerate(secret_caves):
                placement_dict[cave] = secret_cave_money_amounts[i]

            patch = TLOZProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("placement_file.json", json.dumps(placement_dict).encode("UTF-8"))
            rom_path = os.path.join(
                output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
            )
            patch.write(rom_path)
        finally:
            self.rom_name_available_event.set()

    def create_placement_file(self):
        placement_dict = {}
        for location in self.multiworld.get_filled_locations(self.player):
            if location.item.player == self.player:
                placement_dict[location.name] = location.item.name
            else:
                placement_dict[location.name] = "Rupee"
        entrance_randomizer_set = {}
        for screen, data in self.entrance_randomizer_set.items():
            entrance_randomizer_set[screen] = data[1]
        placement_dict["entrance_randomizer_set"] = entrance_randomizer_set
        return placement_dict

    def modify_multidata(self, multidata: dict):
        import base64
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name, encoding="utf-8")).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        if self.filler_items is None:
            self.filler_items = [item for item in item_table if item_table[item].classification == ItemClassification.filler]
        return self.random.choice(self.filler_items)

    def fill_slot_data(self) -> Dict[str, Any]:
        if self.options.ExpandedPool:
            take_any_left = self.multiworld.get_location("Take Any Item Left", self.player).item
            take_any_middle = self.multiworld.get_location("Take Any Item Middle", self.player).item
            take_any_right = self.multiworld.get_location("Take Any Item Right", self.player).item
            if take_any_left.player == self.player:
                take_any_left = take_any_left.code
            else:
                take_any_left = -1
            if take_any_middle.player == self.player:
                take_any_middle = take_any_middle.code
            else:
                take_any_middle = -1
            if take_any_right.player == self.player:
                take_any_right = take_any_right.code
            else:
                take_any_right = -1

            slot_data = {
                "TakeAnyLeft": take_any_left,
                "TakeAnyMiddle": take_any_middle,
                "TakeAnyRight": take_any_right
            }
        else:
            slot_data = {
                "TakeAnyLeft": -1,
                "TakeAnyMiddle": -1,
                "TakeAnyRight": -1
            }
        return slot_data


class TLoZItem(Item):
    game = 'The Legend of Zelda'


class TLoZLocation(Location):
    game = 'The Legend of Zelda'
