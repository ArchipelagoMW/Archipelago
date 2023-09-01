import os
import threading
from pkgutil import get_data

import bsdiff4
import Utils
import settings
import typing

from typing import NamedTuple, Union, Dict, Any
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from .ItemPool import generate_itempool, starting_weapons, dangerous_weapon_locations
from .Items import item_table, item_prices, item_game_ids
from .Locations import location_table, level_locations, major_locations, shop_locations, all_level_locations, \
    standard_level_locations, shop_price_location_ids, secret_money_ids, location_ids, food_locations
from .Options import tloz_options
from .Rom import TLoZDeltaPatch, get_base_rom_path, first_quest_dungeon_items_early, first_quest_dungeon_items_late
from .Rules import set_rules
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
        "Multiworld Setup Tutorial",
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
    option_definitions = tloz_options
    settings: typing.ClassVar[TLoZSettings]
    game = "The Legend of Zelda"
    topology_present = False
    data_version = 1
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

    for k, v in item_name_to_id.items():
        item_name_to_id[k] = v + base_id

    for k, v in location_name_to_id.items():
        if v is not None:
            location_name_to_id[k] = v + base_id

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.generator_in_use = threading.Event()
        self.rom_name_available_event = threading.Event()
        self.levels = None
        self.filler_items = None

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def create_item(self, name: str):
        return TLoZItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return TLoZItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name, id, parent, event=False):
        return_location = TLoZLocation(self.player, name, id, parent)
        return_location.event = event
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
                if self.multiworld.ExpandedPool[self.player] or "Drop" not in location:
                    self.levels[i + 1].locations.append(
                        self.create_location(location, self.location_name_to_id[location], self.levels[i + 1]))

        for level in range(1, 9):
            boss_event = self.create_location(f"Level {level} Boss Status", None,
                                              self.multiworld.get_region(f"Level {level}", self.player),
                                              True)
            boss_event.show_in_spoiler = False
            self.levels[level].locations.append(boss_event)

        for location in major_locations:
            if self.multiworld.ExpandedPool[self.player] or "Take Any" not in location:
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
        ganon = self.multiworld.get_location("Ganon", self.player)
        ganon.place_locked_item(self.create_event("Triforce of Power"))
        add_rule(ganon, lambda state: state.has("Silver Arrow", self.player) and state.has("Bow", self.player))

        self.multiworld.get_location("Zelda", self.player).place_locked_item(self.create_event("Rescued Zelda!"))
        add_rule(self.multiworld.get_location("Zelda", self.player),
                 lambda state: ganon in state.locations_checked)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Rescued Zelda!", self.player)

    def apply_base_patch(self, rom):
        # The base patch source is on a different repo, so here's the summary of changes:
        # Remove Triforce check for recorder, so you can always warp.
        # Remove level check for Triforce Fragments (and maps and compasses, but this won't matter)
        # Replace some code with a jump to free space
        # Check if we're picking up a Triforce Fragment. If so, increment the local count
        # In either case, we do the instructions we overwrote with the jump and then return to normal flow
        # Remove map/compass check so they're always on
        # Removing a bit from the boss roars flags, so we can have more dungeon items. This allows us to
        # go past 0x1F items for dungeon items.
        base_patch = get_data(__name__, "z1_base_patch.bsdiff4")
        rom_data = bsdiff4.patch(rom.read(), base_patch)
        rom_data = bytearray(rom_data)
        # Set every item to the new nothing value, but keep room flags. Type 2 boss roars should
        # become type 1 boss roars, so we at least keep the sound of roaring where it should be.
        for i in range(0, 0x7F):
            item = rom_data[first_quest_dungeon_items_early + i]
            if item & 0b00100000:
                rom_data[first_quest_dungeon_items_early + i] = item & 0b11011111
                rom_data[first_quest_dungeon_items_early + i] = item | 0b01000000
            if item & 0b00011111 == 0b00000011: # Change all Item 03s to Item 3F, the proper "nothing"
                rom_data[first_quest_dungeon_items_early + i] = item | 0b00111111

            item = rom_data[first_quest_dungeon_items_late + i]
            if item & 0b00100000:
                rom_data[first_quest_dungeon_items_late + i] = item & 0b11011111
                rom_data[first_quest_dungeon_items_late + i] = item | 0b01000000
            if item & 0b00011111 == 0b00000011:
                rom_data[first_quest_dungeon_items_late + i] = item | 0b00111111
        return rom_data

    def apply_randomizer(self):
        with open(get_base_rom_path(), 'rb') as rom:
            rom_data = self.apply_base_patch(rom)
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
                rom_data[price_location] = item_price
            if location.name == "Take Any Item Right":
                # Same story as above: bit 6 is what makes this a Take Any cave
                item_id = item_id | 0b01000000
            rom_data[location_id] = item_id
        
        # We shuffle the tiers of rupee caves. Caves that shared a value before still will.
        secret_caves = self.multiworld.per_slot_randoms[self.player].sample(sorted(secret_money_ids), 3)
        secret_cave_money_amounts = [20, 50, 100]
        for i, amount in enumerate(secret_cave_money_amounts):
            # Giving approximately double the money to keep grinding down
            amount = amount * self.multiworld.per_slot_randoms[self.player].triangular(1.5, 2.5)
            secret_cave_money_amounts[i] = int(amount)
        for i, cave in enumerate(secret_caves):
            rom_data[secret_money_ids[cave]] = secret_cave_money_amounts[i]
        return rom_data

    def generate_output(self, output_directory: str):
        try:
            patched_rom = self.apply_randomizer()
            outfilebase = 'AP_' + self.multiworld.seed_name
            outfilepname = f'_P{self.player}'
            outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
            outputFilename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.nes')
            self.rom_name_text = f'LOZ{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
            self.romName = bytearray(self.rom_name_text, 'utf8')[:0x20]
            self.romName.extend([0] * (0x20 - len(self.romName)))
            self.rom_name = self.romName
            patched_rom[0x10:0x30] = self.romName
            self.playerName = bytearray(self.multiworld.player_name[self.player], 'utf8')[:0x20]
            self.playerName.extend([0] * (0x20 - len(self.playerName)))
            patched_rom[0x30:0x50] = self.playerName
            patched_filename = os.path.join(output_directory, outputFilename)
            with open(patched_filename, 'wb') as patched_rom_file:
                patched_rom_file.write(patched_rom)
            patch = TLoZDeltaPatch(os.path.splitext(outputFilename)[0] + TLoZDeltaPatch.patch_file_ending,
                                   player=self.player,
                                   player_name=self.multiworld.player_name[self.player],
                                   patched_path=outputFilename)
            patch.write()
            os.unlink(patched_filename)
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
        return self.multiworld.random.choice(self.filler_items)

    def fill_slot_data(self) -> Dict[str, Any]:
        if self.multiworld.ExpandedPool[self.player]:
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
