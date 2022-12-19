import logging
import os
import threading
from typing import NamedTuple, Union

import bsdiff4

import Utils
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from .ItemPool import generate_itempool, starting_weapons, dangerous_weapon_locations
from .Items import item_table, item_prices, item_game_ids
from .Locations import location_table, level_locations, major_locations, shop_locations, all_level_locations, \
    standard_level_locations, shop_price_location_ids, secret_money_ids, location_ids, food_locations
from .Options import tloz_options
from .Rom import TLoZDeltaPatch, get_base_rom_path, first_quest_dungeon_items_early, first_quest_dungeon_items_late
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule


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
    Triforce of Courage, enter Death Mountain, defeat Ganon, and rescue Princess Zelda.
    This randomizer shuffles all the items in the game around, leading to a new adventure
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

    def create_item(self, name: str):
        return TLoZItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return TLoZItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name, id, parent, event=False):
        return_location = TLoZLocation(self.player, name, id, parent)
        return_location.event = event
        return return_location

    def create_regions(self):
        menu = Region("Menu", None, "Menu", self.player, self.multiworld)
        overworld = Region("Overworld", None, "Overworld", self.player, self.multiworld)
        self.levels = [None]  # Yes I'm making a one-indexed array in a zero-indexed language. I hate me too.
        for i in range(1, 10):
            level = Region(f"Level {i}", None, f"Level {i}", self.player, self.multiworld)
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
            # if self.multiworld.ExpandedPool[self.player] or "Take Any" not in location:
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

#    def create_items(self):


    def set_rules(self):
        # Boss events for a nicer spoiler log play through
        for level in range(1, 9):
            boss = self.multiworld.get_location(f"Level {level} Boss", self.player)
            boss_event = self.multiworld.get_location(f"Level {level} Boss Status", self.player)
            status = self.create_event(f"Boss {level} Defeated")
            boss_event.place_locked_item(status)
            add_rule(boss_event, lambda state: state.can_reach(boss, "Location", self.player))

        # No dungeons without weapons except for the dangerous weapon locations if we're dangerous, no unsafe dungeons
        for i, level in enumerate(self.levels[1:10]):
            for location in level.locations:
                if self.multiworld.StartingPosition[self.player] < 1 or location.name not in dangerous_weapon_locations:
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state: state.has_group("weapons", self.player))
                if i > 0:  # Don't need an extra heart for Level 1
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state: state.has("Heart Container", self.player, i) or
                                           (state.has("Blue Ring", self.player) and
                                            state.has("Heart Container", self.player, int(i / 2))) or
                                           (state.has("Red Ring", self.player) and
                                            state.has("Heart Container", self.player, int(i / 4)))

                             )
        # No requiring anything in a shop until we can farm for money
        for location in shop_locations:
            add_rule(self.multiworld.get_location(location, self.player),
                     lambda state: state.has_group("weapons", self.player))

        # Everything from 4 on up has dark rooms
        for level in self.levels[4:]:
            for location in level.locations:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has_group("candles", self.player)
                                       or (state.has("Magical Rod", self.player) and state.has("Book", self.player)))

        # Everything from 5 on up has gaps
        for level in self.levels[5:]:
            for location in level.locations:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has("Stepladder", self.player))

        add_rule(self.multiworld.get_location("Level 5 Boss", self.player),
                 lambda state: state.has("Recorder", self.player))

        add_rule(self.multiworld.get_location("Level 6 Boss", self.player),
                 lambda state: state.has("Bow", self.player) and state.has_group("arrows", self.player))

        add_rule(self.multiworld.get_location("Level 7 Item (Red Candle)", self.player),
                 lambda state: state.has("Recorder", self.player))
        add_rule(self.multiworld.get_location("Level 7 Boss", self.player),
                 lambda state: state.has("Recorder", self.player))
        if self.multiworld.ExpandedPool[self.player]:
            add_rule(self.multiworld.get_location("Level 7 Key Drop (Stalfos)", self.player),
                     lambda state: state.has("Recorder", self.player))
            add_rule(self.multiworld.get_location("Level 7 Bomb Drop (Digdogger)", self.player),
                     lambda state: state.has("Recorder", self.player))
            add_rule(self.multiworld.get_location("Level 7 Rupee Drop (Dodongos)", self.player),
                     lambda state: state.has("Recorder", self.player))

        for location in food_locations:
            if self.multiworld.ExpandedPool[self.player] or "Drop" not in location:
                add_rule(self.multiworld.get_location(location, self.player),
                         lambda state: state.has("Food", self.player))

        add_rule(self.multiworld.get_location("Level 8 Item (Magical Key)", self.player),
                 lambda state: state.has("Bow", self.player) and state.has_group("arrows", self.player))
        if self.multiworld.ExpandedPool[self.player]:
            add_rule(self.multiworld.get_location("Level 8 Bomb Drop (Darknuts North)", self.player),
                     lambda state: state.has("Bow", self.player) and state.has_group("arrows", self.player))

        for location in self.levels[9].locations:
            add_rule(self.multiworld.get_location(location.name, self.player),
                     lambda state: state.has("Triforce Fragment", self.player, 8) and
                                   state.has_group("swords", self.player))

        add_rule(self.multiworld.get_location("Level 1 Triforce", self.player),
                 lambda state: state.has("Boss 1 Defeated", self.player))

        add_rule(self.multiworld.get_location("Level 2 Triforce", self.player),
                 lambda state: state.has("Boss 2 Defeated", self.player))

        add_rule(self.multiworld.get_location("Level 3 Triforce", self.player),
                 lambda state: state.has("Boss 3 Defeated", self.player))

        add_rule(self.multiworld.get_location("Level 4 Triforce", self.player),
                 lambda state: state.has("Boss 4 Defeated", self.player))

        add_rule(self.multiworld.get_location("Level 5 Triforce", self.player),
                 lambda state: state.has("Boss 5 Defeated", self.player))

        add_rule(self.multiworld.get_location("Level 6 Triforce", self.player),
                 lambda state: state.has("Boss 6 Defeated", self.player))

        add_rule(self.multiworld.get_location("Level 7 Triforce", self.player),
                 lambda state: state.has("Boss 7 Defeated", self.player))

        add_rule(self.multiworld.get_location("Level 8 Triforce", self.player),
                 lambda state: state.has("Boss 8 Defeated", self.player))

        # Sword, raft, and ladder spots
        add_rule(self.multiworld.get_location("White Sword Pond", self.player),
                 lambda state: state.has("Heart Container", self.player, 2))
        add_rule(self.multiworld.get_location("Magical Sword Grave", self.player),
                 lambda state: state.has("Heart Container", self.player, 9))
        add_rule(self.multiworld.get_location("Ocean Heart Container", self.player),
                 lambda state: state.has("Stepladder", self.player))
        # if self.multiworld.StartingPosition[self.player] != 2:
        #     # Don't allow Take Any Items until we can actually get in one
        #     if self.multiworld.ExpandedPool[self.player]:
        #         add_rule(self.multiworld.get_location("Take Any Item Left", self.player),
        #                  lambda state: state.has_group("candles", self.player) or
        #                                state.has("Raft", self.player))
        #         add_rule(self.multiworld.get_location("Take Any Item Middle", self.player),
        #                  lambda state: state.has_group("candles", self.player) or
        #                                state.has("Raft", self.player))
        #         add_rule(self.multiworld.get_location("Take Any Item Right", self.player),
        #                  lambda state: state.has_group("candles", self.player) or
        #                                state.has("Raft", self.player))
        for location in self.levels[4].locations:
            add_rule(self.multiworld.get_location(location.name, self.player),
                     lambda state: state.has("Raft", self.player) or state.has("Recorder", self.player))
        for location in self.levels[7].locations:
            add_rule(self.multiworld.get_location(location.name, self.player),
                     lambda state: state.has("Recorder", self.player))
        for location in self.levels[8].locations:
            add_rule(self.multiworld.get_location(location.name, self.player),
                     lambda state: state.has("Bow", self.player))

        add_rule(self.multiworld.get_location("Potion Shop Item Left", self.player),
                 lambda state: state.has("Letter", self.player))
        # add_rule(self.multiworld.get_location("Potion Shop Item Middle", self.player),
        #          lambda state: state.has("Letter", self.player))
        add_rule(self.multiworld.get_location("Potion Shop Item Right", self.player),
                 lambda state: state.has("Letter", self.player))

        add_rule(self.multiworld.get_location("Shield Shop Item Left", self.player),
                 lambda state: state.has_group("candles", self.player) or
                               state.has("Bomb", self.player))
        add_rule(self.multiworld.get_location("Shield Shop Item Middle", self.player),
                 lambda state: state.has_group("candles", self.player) or
                               state.has("Bomb", self.player))
        add_rule(self.multiworld.get_location("Shield Shop Item Right", self.player),
                 lambda state: state.has_group("candles", self.player) or
                               state.has("Bomb", self.player))

    def generate_basic(self):
        ganon = self.multiworld.get_location("Ganon", self.player)
        ganon.place_locked_item(self.create_event("Triforce of Power"))
        add_rule(ganon, lambda state: state.has("Silver Arrow", self.player) and state.has("Bow", self.player))

        self.multiworld.get_location("Zelda", self.player).place_locked_item(self.create_event("Rescued Zelda!"))
        add_rule(self.multiworld.get_location("Zelda", self.player),
                 lambda state: ganon in state.locations_checked)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Rescued Zelda!", self.player)
        generate_itempool(self)

    def apply_base_patch(self, rom):
        # Remove Triforce check for recorder, so you can always warp.
        # Remove level check for Triforce Fragments (and maps and compasses, but this won't matter)
        # Replace AND #07 TAY with a JSR to free space later in the bank
        # Check if we're picking up a Triforce Fragment. If so, increment the local count
        # In either case, we do the instructions we overwrote with the JSR and then RTS to normal flow
        # N.B.: the location of these instructions in the PRG ROM and where the bank is mapped to
        # do not correspond to each other: while it is not an error that we're jumping to 7EF0,
        # this was calculated by hand, and so if any errors arise it'll likely be here.
        # Reduce variety of boss roars in order to make room for additional dungeon items
        # Remove map/compass check so they're always on
        # Stealing a bit from the boss roars flag, so we can have more dungeon items. This allows us to
        # go past 0x1F items for dungeon drops.
        rom_data = None
        with open("worlds/tloz/z1_base_patch.bsdiff4", "rb") as base_patch:
            rom_data = bsdiff4.patch(rom.read(), base_patch.read())
        rom_data = bytearray(rom_data)
        # Set every item to the new nothing value, but keep room flags. Type 2 boss roars should
        # become type 1 boss roars, so we at least keep the sound of roaring where it should be.
        for i in range(0, 0x7F):
            item = rom_data[first_quest_dungeon_items_early + i]
            if item & 0b00100000:
                rom_data[first_quest_dungeon_items_early + i] = item | 0b01000000
            if item & 0b0000011: # Change all Item 03s to Item 3F, the proper "nothing"
                rom_data[first_quest_dungeon_items_early + i] = item | 0b00111111
            rom_data[first_quest_dungeon_items_early + i] = item & 0b11000000

            item = rom_data[first_quest_dungeon_items_late + i]
            if item & 0b00100000:
                rom_data[first_quest_dungeon_items_late + i] = item | 0b01000000
            if item & 0b00000011:
                rom_data[first_quest_dungeon_items_late + i] = item | 0b00111111
            rom_data[first_quest_dungeon_items_late + i] = item & 0b11000000
        return rom_data

    def apply_randomizer(self):
        with open(get_base_rom_path(), 'rb') as rom:
            rom_data = self.apply_base_patch(rom)
            # Write each location's new data in
            for location in self.multiworld.get_filled_locations():
                # Zelda and Ganon aren't real locations
                if location.name == "Ganon" or location.name == "Zelda":
                    continue

                # Neither are boss defeat events
                if "Status" in location.name:
                    continue

                # We, of course, only care about our own world
                if location.player != self.player:
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
                # if location.name == "Take Any Item Right":
                #     # Same story as above: bit 6 is what makes this a Take Any cave
                #     item_id = item_id | 0b01000000
                rom_data[location_id] = item_id

            # We shuffle the tiers of rupee caves. Caves that shared a value before still will.
            secret_caves = self.multiworld.random.sample(sorted(secret_money_ids), 3)
            secret_cave_money_amounts = [20, 50, 100]
            for i, amount in enumerate(secret_cave_money_amounts):
                # Giving approximately double the money to keep grinding down
                amount = amount * self.multiworld.random.triangular(1.5, 2.5)
                secret_cave_money_amounts[i] = int(amount)
            for i, cave in enumerate(secret_caves):
                rom_data[secret_money_ids[cave]] = secret_cave_money_amounts[i]
            return rom_data

    def generate_output(self, output_directory: str):
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
                               player_name=self.multiworld.player_name[self.player], patched_path=outputFilename)
        self.rom_name_available_event.set()
        patch.write()
        os.unlink(outputFilename)

    def modify_multidata(self, multidata: dict):
        import base64
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        filler_items = [item for item in item_table if item_table[item].classification == ItemClassification.filler]
        return self.multiworld.random.choice(filler_items)


class TLoZItem(Item):
    game = 'The Legend of Zelda'


class TLoZLocation(Location):
    game = 'The Legend of Zelda'


class PlandoItem(NamedTuple):
    item: str
    location: str
    world: Union[bool, str] = False  # False -> own world, True -> not own world
    from_pool: bool = True  # if item should be removed from item pool
    force: str = 'silent'  # false -> warns if item not successfully placed. true -> errors out on failure to place item

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
