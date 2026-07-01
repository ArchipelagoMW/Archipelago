import os
import threading

import Utils
import settings
import typing

from typing import NamedTuple, Union, Dict, Any
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from .ItemPool import generate_itempool, starting_weapons, dangerous_weapon_locations
from .Items import item_table, item_prices, item_game_ids
from .Locations import location_table, level_locations, major_locations, shop_locations, all_level_locations, \
    standard_level_locations, shop_price_location_ids, secret_money_ids, location_ids, food_locations, \
    take_any_locations, sword_cave_locations
from .Options import TlozOptions
from .Rom import TLoZProcedurePatch
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld
from worlds.Files import APTokenTypes
from worlds.generic.Rules import add_rule


class TLoZSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Zelda 1"""
        description = "The Legend of Zelda (U) ROM File"
        copy_to = "Legend of Zelda, The (U) (PRG0) [!].nes"
        md5s = [TLoZProcedurePatch.hash]

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
    topology_present = False
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

    def create_item(self, name: str):
        return TLoZItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return TLoZItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name, id, parent, event=False):
        return_location = TLoZLocation(self.player, name, id, parent)
        return return_location

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        overworld = Region("Overworld", self.player, self.multiworld)
        self.levels = [None]  # Yes I'm making a one-indexed array in a zero-indexed language. I hate me too.
        for i in range(1, 10):
            level = Region(f"Level {i}", self.player, self.multiworld)
            self.levels.append(level)
            new_entrance = Entrance(self.player, f"Level {i}", overworld)
            new_entrance.connect(level)
            overworld.exits.append(new_entrance)
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
            if self.options.ExpandedPool or "Take Any" not in location:
                overworld.locations.append(
                    self.create_location(location, self.location_name_to_id[location], overworld))

        for location in shop_locations:
            overworld.locations.append(
                self.create_location(location, self.location_name_to_id[location], overworld))

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
        pass


    def place_items(self, patch: TLoZProcedurePatch):
        # Write each location's new data in
        for location in self.multiworld.get_filled_locations(self.player):
            # Zelda and Ganon aren't real locations
            if location.name == "Ganon" or location.name == "Zelda":
                continue

            # Neither are boss defeat events
            if "Status" in location.name:
                continue

            item = location.item.name
            # Remote items are always going to look like Rupees.
            if location.item.player != self.player:
                item = "Rupee"

            item_id = item_game_ids[item]
            location_id = location_ids[location.name]

            # Shop prices need to be set
            if location.name in shop_locations:
                if location.name[-5:] == "Right":
                    # Final item in stores has bit 6 and 7 set. It's what marks the cave a shop.
                    item_id = item_id | 0b11000000
                price_location = shop_price_location_ids[location.name]
                item_price = item_prices[item]
                if item == "Rupee":
                    item_class = location.item.classification
                    if item_class == ItemClassification.progression:
                        item_price = item_price * 2
                    elif item_class == ItemClassification.useful:
                        item_price = item_price // 2
                    elif item_class == ItemClassification.filler:
                        item_price = item_price // 2
                    elif item_class == ItemClassification.trap:
                        item_price = item_price * 2
                patch.write_token(APTokenTypes.WRITE, price_location, item_price.to_bytes(1, "little"))
            if location.name == "Take Any Item Right":
                # Same story as above: bit 6 is what makes this a Take Any cave
                item_id = item_id | 0b01000000
            patch.write_token(APTokenTypes.WRITE, location_id, item_id.to_bytes(1, "little"))

        # We shuffle the tiers of rupee caves. Caves that shared a value before still will.
        secret_caves = self.random.sample(sorted(secret_money_ids), 3)
        secret_cave_money_amounts = [20, 50, 100]
        for i, amount in enumerate(secret_cave_money_amounts):
            # Giving approximately double the money to keep grinding down
            amount = amount * self.random.triangular(1.5, 2.5)
            secret_cave_money_amounts[i] = int(amount)
        for i, cave in enumerate(secret_caves):
            patch.write_token(APTokenTypes.WRITE, secret_money_ids[cave],
                              secret_cave_money_amounts[i].to_bytes(1, "little"))

    def generate_output(self, output_directory: str):
        try:
            patch = TLoZProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            self.place_items(patch)
            self.rom_name_text = f'LOZ{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
            self.romName = bytearray(self.rom_name_text, 'utf8')[:0x20]
            self.romName.extend([0] * (0x20 - len(self.romName)))
            self.rom_name = self.romName
            patch.write_token(APTokenTypes.WRITE, 0x10, bytes(self.romName))
            self.playerName = bytearray(self.multiworld.player_name[self.player], 'utf8')[:0x20]
            self.playerName.extend([0] * (0x20 - len(self.playerName)))
            patch.write_token(APTokenTypes.WRITE, 0x30, bytes(self.playerName))
            patch.write_file("token_patch.bin", patch.get_token_binary())
            outfilebase = 'AP_' + self.multiworld.seed_name
            outfilepname = f'_P{self.player}'
            outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
            patch.write(os.path.join(output_directory, f'{outfilebase}{outfilepname}{patch.patch_file_ending}'))
        finally:
            self.rom_name_available_event.set()

    def modify_multidata(self, multidata: dict):
        import base64
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
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
