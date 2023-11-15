"""
Archipelago init file for Lingo
"""
from BaseClasses import Item, Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import ALL_ITEM_TABLE, LingoItem
from .locations import ALL_LOCATION_TABLE
from .options import LingoOptions
from .player_logic import LingoPlayerLogic
from .regions import create_regions
from .static_logic import Room, RoomEntrance
from .testing import LingoTestOptions


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

    options_dataclass = LingoOptions
    options: LingoOptions

    item_name_to_id = {
        name: data.code for name, data in ALL_ITEM_TABLE.items()
    }
    location_name_to_id = {
        name: data.code for name, data in ALL_LOCATION_TABLE.items()
    }

    player_logic: LingoPlayerLogic

    def generate_early(self):
        self.player_logic = LingoPlayerLogic(self)

    def create_regions(self):
        create_regions(self, self.player_logic)

    def create_items(self):
        pool = [self.create_item(name) for name in self.player_logic.REAL_ITEMS]

        if self.player_logic.FORCED_GOOD_ITEM != "":
            new_item = self.create_item(self.player_logic.FORCED_GOOD_ITEM)
            location_obj = self.multiworld.get_location("Second Room - Good Luck", self.player)
            location_obj.place_locked_item(new_item)

        item_difference = len(self.player_logic.REAL_LOCATIONS) - len(pool)
        if item_difference:
            trap_percentage = self.options.trap_percentage
            traps = int(item_difference * trap_percentage / 100.0)
            non_traps = item_difference - traps

            if non_traps:
                skip_percentage = self.options.puzzle_skip_percentage
                skips = int(non_traps * skip_percentage / 100.0)
                non_skips = non_traps - skips

                filler_list = [":)", "The Feeling of Being Lost", "Wanderlust", "Empty White Hallways"]
                for i in range(0, non_skips):
                    pool.append(self.create_item(filler_list[i % len(filler_list)]))

                for i in range(0, skips):
                    pool.append(self.create_item("Puzzle Skip"))

            if traps:
                traps_list = ["Slowness Trap", "Iceland Trap", "Atbash Trap"]

                for i in range(0, traps):
                    pool.append(self.create_item(traps_list[i % len(traps_list)]))

        self.multiworld.itempool += pool

    def create_item(self, name: str) -> Item:
        item = ALL_ITEM_TABLE[name]
        return LingoItem(name, item.classification, item.code, self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        slot_options = [
            "death_link", "victory_condition", "shuffle_colors", "shuffle_doors", "shuffle_paintings", "shuffle_panels",
            "mastery_achievements", "level_2_requirement", "location_checks", "early_color_hallways"
        ]

        slot_data = {
            "seed": self.random.randint(0, 1000000),
            **self.options.as_dict(*slot_options),
        }

        if self.options.shuffle_paintings:
            slot_data["painting_entrance_to_exit"] = self.player_logic.PAINTING_MAPPING

        return slot_data
