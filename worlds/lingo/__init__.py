"""
Archipelago init file for Lingo
"""
import typing

from BaseClasses import Region, Location, MultiWorld, Item, Entrance, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .static_logic import StaticLingoLogic, Room, RoomEntrance
from .items import LingoItem, StaticLingoItems
from .locations import LingoLocation, StaticLingoLocations
from .Options import lingo_options, get_option_value
from .testing import LingoTestOptions
from worlds.generic.Rules import set_rule
from .player_logic import LingoPlayerLogic
from .regions import create_regions
from math import floor


class LingoWebWorld(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Lingo with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["hatkirby"]
    )]


class LingoWorld(World):
    """
    Lingo is a first person indie puzzle game in the vein of The Witness. You find yourself in a mazelike, non-Euclidean
    world filled with 800 word puzzles that use a variety of different mechanics.
    """
    game = "Lingo"
    web = LingoWebWorld()

    base_id = 444400
    topology_present = True
    data_version = 1

    static_logic = StaticLingoLogic()
    static_items = StaticLingoItems(base_id)
    static_locat = StaticLingoLocations(base_id)
    option_definitions = lingo_options

    item_name_to_id = {
        name: data.code for name, data in static_items.ALL_ITEM_TABLE.items()
    }
    location_name_to_id = {
        name: data.code for name, data in static_locat.ALL_LOCATION_TABLE.items()
        if data.code is not None
    }

    # This is just used for unit testing. It should remain at the default values for actual play.
    test_options: LingoTestOptions = LingoTestOptions()

    def generate_early(self):
        self.player_logic = LingoPlayerLogic(self.multiworld, self.player, self.static_logic, self.test_options)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.static_logic, self.player_logic)

    def create_items(self):
        pool = [self.create_item(name) for name in self.player_logic.REAL_ITEMS]

        if self.player_logic.FORCED_GOOD_ITEM != "":
            new_item = self.create_item(self.player_logic.FORCED_GOOD_ITEM)
            location_obj = self.multiworld.get_location("Starting Room - HI", self.player)
            location_obj.place_locked_item(new_item)

        item_difference = len(self.player_logic.REAL_LOCATIONS) - len(pool)
        if item_difference:
            trap_percentage = get_option_value(self.multiworld, self.player, "trap_percentage")
            traps = int(item_difference * trap_percentage / 100.0)
            non_traps = item_difference - traps

            if non_traps:
                skip_percentage = get_option_value(self.multiworld, self.player, "puzzle_skip_percentage")
                skips = int(non_traps * skip_percentage / 100.0)
                non_skips = non_traps - skips

                for i in range(0, non_skips):
                    pool.append(self.create_item("Nothing"))

                for i in range(0, skips):
                    pool.append(self.create_item("Puzzle Skip"))

            if traps:
                traps_list = ["Slowness Trap", "Iceland Trap", "Atbash Trap"]

                for i in range(0, traps):
                    pool.append(self.create_item(traps_list[i % len(traps_list)]))

        self.multiworld.itempool += pool

    def create_item(self, name: str) -> Item:
        item = StaticLingoItems.ALL_ITEM_TABLE[name]
        return LingoItem(name, item.classification, item.code, player=self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        slot_data = {"seed": self.multiworld.per_slot_randoms[self.player].randint(0, 1000000)}

        for option_name in ["death_link", "victory_condition", "shuffle_colors", "shuffle_doors", "shuffle_paintings",
                            "shuffle_panels", "mastery_achievements", "level_2_requirement", "reduce_checks"]:
            slot_data[option_name] = get_option_value(self.multiworld, self.player, option_name)

        if get_option_value(self.multiworld, self.player, "shuffle_paintings"):
            slot_data["painting_entrance_to_exit"] = self.player_logic.PAINTING_MAPPING

        return slot_data
