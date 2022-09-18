import logging
import os
import random
import threading
from typing import NamedTuple, Union

import Utils
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from .Items import item_table
from .Locations import location_table, level_locations
from .Options import tloz_options
from .Rom import TLoZDeltaPatch
from ..AutoWorld import World, WebWorld
from ..generic.Rules import add_rule, set_rule, forbid_item, add_item_rule

class TLoZWeb(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up The Legend of Zelda for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rosalie"]
    )

    tutorials = [setup]


class TLoZWorld(World):
    """
    The Legend of Zelda needs almost no introduction. Gather the eight fragments of the
    Triforce of Courage, enter Death Mountain, defeat Ganon, and rescue Princess Zelda.
    This randomizer shuffles all of the items in the game around, leading to a new adventure
    every time.
    """
    option_definitions = tloz_options
    game = "The Legend of Zelda"
    topology_present = False
    data_version = 1
    base_id = 7000
    web = TLoZWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    item_name_groups = {
        'weapons': {
            "Sword", "White Sword", "Magical Sword", "Magical Rod", "Red Candle"
        },
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

    def create_item(self, name: str):
        return TLoZItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return TLoZItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name, id, parent, event=False):
        return_location = TLoZLocation(self.player, name, id, parent)
        return_location.event = event
        return return_location

    def create_regions(self):
        menu = Region("Menu", None, "Menu", self.player, self.world)
        overworld = Region("Overworld", None, "Overworld", self.player, self.world)
        self.levels = [None]  # Yes I'm making a one-indexed array in a zero-indexed language. I hate me too.
        for i in range(1, 10):
            level = Region(f"Level {i}", None, f"Level {i}", self.player, self.world)
            self.levels.append(level)
            new_entrance = Entrance(self.player, f"Level {i}", overworld)
            new_entrance.connect(level)
            overworld.exits.append(new_entrance)
            self.world.regions.append(level)

        for i, level in enumerate(level_locations):
            for location in level:
                if self.world.ExpandedPool[self.player] or "Drop" not in location:
                    self.levels[i + 1].locations.append(
                        self.create_location(location, self.location_name_to_id[location], self.levels[i + 1]))

        for location in Locations.major_locations:
            overworld.locations.append(
                self.create_location(location, self.location_name_to_id[location], overworld))

        for location in Locations.shop_locations:
            overworld.locations.append(
                self.create_location(location, self.location_name_to_id[location], overworld))

        ganon = self.create_location("Ganon", None, self.world.get_region("Level 9", self.player))
        zelda = self.create_location("Zelda", None, self.world.get_region("Level 9", self.player))
        self.levels[9].locations.append(ganon)
        self.levels[9].locations.append(zelda)
        begin_game = Entrance(self.player, "Begin Game", menu)
        menu.exits.append(begin_game)
        begin_game.connect(overworld)
        self.world.regions.append(menu)
        self.world.regions.append(overworld)

    def create_items(self):
        # We guarantee that there will always be a key, bomb, and potion in an ungated shop.
        reserved_store_slots = random.sample(Locations.shop_locations[0:-3], 3)
        self.world.get_location(
            reserved_store_slots[0],
            self.player
        ).place_locked_item(
            self.world.create_item(
                "Small Key", self.player)
        )
        self.world.get_location(
            reserved_store_slots[1],
            self.player
        ).place_locked_item(
            self.world.create_item("Bomb", self.player))
        self.world.get_location(
            reserved_store_slots[2],
            self.player
        ).place_locked_item(
            self.world.create_item("Water of Life (Red)", self.player))
        start_locked = False
        item_amounts = Items.item_amounts_all
        if not self.world.ExpandedPool[self.player]:
            item_amounts = Items.item_amounts_standard
            self.world.get_location(
                "Take Any Item 1",
                self.player
            ).place_locked_item(self.world.create_item("Water of Life (Red)", self.player))
            self.world.get_location(
                "Take Any Item 3",
                self.player
            ).place_locked_item(self.world.create_item("Heart Container", self.player))
        for item in map(self.create_item, self.item_name_to_id):
            if item.name in item_amounts.keys():
                if self.world.TriforceLocations[self.player] > 0 or item.name != "Triforce Fragment":
                    i = 0
                    for i in range(0, item_amounts[item.name]):
                        self.world.itempool.append(item)
                else:
                    level = 1
                    for i in range(0, item_amounts[item.name]):
                        self.world.get_location(
                            f"Level {level} Triforce",
                            self.player
                        ).place_locked_item(self.world.create_item(item.name, self.player))
                        level = level + 1
            else:
                self.world.itempool.append(item)

    def set_rules(self):
        # If we're doing a safe start, everything past the starting screen requires a weapon.
        if self.world.StartingPosition[self.player] == 0:
            for location in Locations.cave_locations:
                add_rule(self.world.get_location(location, self.player),
                         lambda state: state.has_group("weapons", self.player))
            for location in Locations.major_locations:
                if location != "Starting Sword Cave":
                    add_rule(self.world.get_location(location, self.player),
                             lambda state: state.has_group("weapons", self.player))

        # No dungeons without weapons, no unsafe dungeons
        for i, level in enumerate(self.levels[1:10]):
            for location in level.locations:
                add_rule(self.world.get_location(location.name, self.player),
                         lambda state: state.has_group("weapons", self.player))
                add_rule(self.world.get_location(location.name, self.player),
                         lambda state: state.has("Heart Container", self.player, 3 + i) or
                                       (state.has("Blue Ring", self.player) and
                                        state.has("Heart Container", self.player, int(i / 2))) or
                                       (state.has("Red Ring", self.player) and
                                        state.has("Heart Container", self.player, int(i / 4)))

                         )
        # No requiring anything in a shop until we can farm for money
        # Unless someone likes to live dangerously, of course
        for location in Locations.shop_locations:
            if self.world.StartingPosition[self.player] != 2:
                add_rule(self.world.get_location(location, self.player),
                         lambda state: state.has_group("weapons", self.player))

        # Everything from 4 on up has dark rooms
        for level in self.levels[4:]:
            for location in level.locations:
                add_rule(self.world.get_location(location.name, self.player),
                         lambda state: state.has_group("candles", self.player)
                                       or (state.has("Magical Rod", self.player) and state.has("Book", self.player)))

        # Everything from 5 on up has gaps
        for level in self.levels[5:]:
            for location in level.locations:
                add_rule(self.world.get_location(location.name, self.player),
                         lambda state: state.has("Stepladder", self.player))

        add_rule(self.world.get_location("Level 5 Boss", self.player),
                 lambda state: state.has("Recorder", self.player))
        add_rule(self.world.get_location("Level 6 Boss", self.player),
                 lambda state: state.has("Bow", self.player) and state.has_group("arrows", self.player))
        add_rule(self.world.get_location("Level 7 Item (Red Candle)", self.player),
                 lambda state: state.has("Recorder", self.player))
        add_rule(self.world.get_location("Level 7 Boss", self.player),
                 lambda state: state.has("Recorder", self.player))
        add_rule(self.world.get_location("Level 8 Item (Magical Key)", self.player),
                 lambda state: state.has("Bow", self.player) and state.has_group("arrows", self.player))
        for location in self.levels[9].locations:
            add_rule(self.world.get_location(location.name, self.player),
                     lambda state: state.has("Triforce Fragment", self.player, 8))
        for i in range(1, 9):
            add_rule(self.world.get_location(f"Level {i} Triforce", self.player),
                     lambda state: state.can_reach(f"Level {i} Boss", "Location", self.player))

        # Sword, raft, and ladder spots
        add_rule(self.world.get_location("White Sword Pond", self.player),
                 lambda state: state.has("Heart Container", self.player, 2))
        add_rule(self.world.get_location("Magical Sword Grave", self.player),
                 lambda state: state.has("Heart Container", self.player, 9))
        add_rule(self.world.get_location("Ocean Heart Container", self.player),
                 lambda state: state.has("Stepladder", self.player))
        if self.world.StartingPosition[self.player] != 2:
            # Don't allow Take Any Items until we can actually get in one
            add_rule(self.world.get_location("Take Any Item 1", self.player),
                     lambda state: state.has_group("candles", self.player) or
                                   state.has("Raft", self.player))
            add_rule(self.world.get_location("Take Any Item 2", self.player),
                     lambda state: state.has_group("candles", self.player) or
                                   state.has("Raft", self.player))
            add_rule(self.world.get_location("Take Any Item 3", self.player),
                     lambda state: state.has_group("candles", self.player) or
                                   state.has("Raft", self.player))
        for location in self.levels[4].locations:
            add_rule(self.world.get_location(location.name, self.player),
                     lambda state: state.has("Raft", self.player) or state.has("Recorder", self.player))
        for location in self.levels[7].locations:
            add_rule(self.world.get_location(location.name, self.player),
                     lambda state: state.has("Recorder", self.player))
        for location in self.levels[8].locations:
            add_rule(self.world.get_location(location.name, self.player),
                     lambda state: state.has("Bow", self.player))

        if self.world.TriforceLocations[self.player] == 1:
            for location in location_table.keys():
                if location  not in Locations.all_level_locations:
                    forbid_item(self.world.get_location(location, self.player), "Triforce Fragment", self.player)

        add_rule(self.world.get_location("Potion Shop Item 1", self.player),
                 lambda state: state.has("Letter", self.player))
        add_rule(self.world.get_location("Potion Shop Item 2", self.player),
                 lambda state: state.has("Letter", self.player))
        add_rule(self.world.get_location("Potion Shop Item 3", self.player),
                 lambda state: state.has("Letter", self.player))

        set_rule(self.world.get_region("Menu", self.player), lambda state: True)
        set_rule(self.world.get_region("Overworld", self.player), lambda state: True)

    def generate_basic(self):
        ganon = self.world.get_location("Ganon", self.player)
        ganon.place_locked_item(self.create_event("Defeated Ganon!"))
        add_rule(ganon, lambda state: state.has("Silver Arrow", self.player) and state.has("Bow", self.player))

        self.world.get_location("Zelda", self.player).place_locked_item(self.create_event("Rescued Zelda!"))
        add_rule(self.world.get_location("Zelda", self.player),
                 lambda state: ganon in state.locations_checked)

        self.world.completion_condition[self.player] = lambda state: state.has("Rescued Zelda!", self.player)

    def apply_base_patch(self, rom_data):
        # Remove Triforce check for recorder so you can always warp.
        rom_data[0x60CC:0x60CF] = bytearray([0xA9, 0xFF, 0xEA])

        # Remove level check for Triforce Fragments (and maps and compasses, but this won't matter)
        rom_data[0x6C9B:0x6C9D] = bytearray([0xEA, 0xEA])

        # Replace AND #07 TAY with a JSR to free space later in the bank
        rom_data[0x6CB5:0x6CB8] = bytearray([0x20, 0xF0, 0x7E])

        # Check if we're picking up a Triforce Fragment. If so, increment the local count
        # In either case, we do the instructions we overwrote with the JSR and then RTS to normal flow
        # N.B.: the location of these instructions in the PRG ROM and where the bank is mapped to
        # do not correspond to each other: while it is not an error that we're jumping to 7EF0,
        # this was calculated by hand, and so if any errors arise it'll likely be here.
        rom_data[0x7770:0x777B] = bytearray([0xE0, 0x1B, 0xD0, 0x03, 0xEE, 0x79, 0x06, 0x29, 0x07, 0xAA, 0x60])

        # Remove map/compass check so they're always on
        rom_data[0x17614:0x17617] = bytearray([0xA9, 0xA1, 0x60])

    def apply_randomizer(self):
        with open(Rom.get_base_rom_path(), 'rb') as rom:
            rom_data = bytearray(rom.read())

            self.apply_base_patch(rom_data)

            # Write each location's new data in
            for location in self.world.get_filled_locations():
                # Zelda and Ganon aren't real locations
                if location.name == "Ganon" or location.name == "Zelda":
                    continue

                # We, of course, only care about our own world
                if location.player != self.player:
                    continue

                item = location.item.name
                # Remote items are always gonna look like Rupees.
                if location.item.player != self.player:
                    item = "Rupee"

                item_id = Items.item_game_ids[item]
                location_id = Locations.location_ids[location.name]

                # Shop prices need to be set
                if location.name in Locations.shop_locations:
                    if location.name[-1] == "3":
                        # Final item in stores has bit 6 and 7 set. It's what marks the cave a shop.
                        item_id = item_id | 0b11000000
                    price_location = Locations.shop_price_location_ids[location.name]
                    item_price = Items.item_prices[item]
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
                if location.name == "Take Any Item 3":
                    # Same story as above: bit 6 is what makes this a Take Any cave
                    item_id = item_id | 0b01000000
                if location.name in Locations.all_level_locations:
                    # We want to preserve room flags: darkness and boss roars
                    item_flags = rom_data[location_id] & 0b11100000
                    item_id = item_id | item_flags
                rom_data[location_id] = item_id

            # We shuffle the tiers of rupee caves. Caves that shared a value before still will.
            secret_caves = random.sample(sorted(Locations.secret_money_ids), 3)
            secret_cave_money_amounts = [20, 50, 100]
            for i, amount in enumerate(secret_cave_money_amounts):
                # Giving approximately double the money to keep grinding down
                amount = amount * random.triangular(1.5, 2.5)
                secret_cave_money_amounts[i] = int(amount)
            for i, cave in enumerate(secret_caves):
                rom_data[Locations.secret_money_ids[cave]] = secret_cave_money_amounts[i]
            return rom_data

    def generate_output(self, output_directory: str):
        patched_rom = self.apply_randomizer()
        outfilebase = 'AP_' + self.world.seed_name
        outfilepname = f'_P{self.player}'
        outfilepname += f"_{self.world.get_file_safe_player_name(self.player).replace(' ', '_')}"
        outputFilename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.nes')

        self.rom_name_text = f'LOZ{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.world.seed:11}\0'
        self.romName = bytearray(self.rom_name_text, 'utf8')[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))
        self.rom_name = self.romName
        patched_rom[0x10:0x30] = self.romName

        self.playerName = bytearray(self.world.player_name[self.player], 'utf8')[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))
        patched_rom[0x30:0x50] = self.playerName


        patched_filename = os.path.join(output_directory, outputFilename)

        with open(patched_filename, 'wb') as patched_rom_file:
            patched_rom_file.write(patched_rom)

        patch = TLoZDeltaPatch(os.path.splitext(outputFilename)[0] + TLoZDeltaPatch.patch_file_ending,
                               player=self.player,
                               player_name=self.world.player_name[self.player], patched_path=outputFilename)
        self.rom_name_available_event.set()
        patch.write()

    def modify_multidata(self, multidata: dict):
        import base64
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]


class TLoZItem(Item):
    game = 'The Legend of Zelda'


class TLoZLocation(Location):
    game = 'The Legend of Zelda'


class PlandoItem(NamedTuple):
    item: str
    location: str
    world: Union[bool, str] = False  # False -> own world, True -> not own world
    from_pool: bool = True  # if item should be removed from item pool
    force: str = 'silent'  # false -> warns if item not successfully placed. true -> errors out on failure to place item.

    def warn(self, warning: str):
        if self.force in ['true', 'fail', 'failure', 'none', 'false', 'warn', 'warning']:
            logging.warning(f'{warning}')
        else:
            logging.debug(f'{warning}')

    def failed(self, warning: str, exception=Exception):
        if self.force in ['true', 'fail', 'failure']:
            raise exception(warning)
        else:
            self.warn(warning)


class PlandoConnection(NamedTuple):
    entrance: str
    exit: str
    direction: str  # entrance, exit or both
