"""
Archipelago init file for Lingo
"""
from logging import warning

from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from .datatypes import Room, RoomEntrance
from .items import ALL_ITEM_TABLE, ITEMS_BY_GROUP, TRAP_ITEMS, LingoItem
from .locations import ALL_LOCATION_TABLE, LOCATIONS_BY_GROUP
from .options import LingoOptions
from .player_logic import LingoPlayerLogic
from .regions import create_regions


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
    item_name_groups = ITEMS_BY_GROUP
    location_name_groups = LOCATIONS_BY_GROUP

    player_logic: LingoPlayerLogic

    def generate_early(self):
        if not (self.options.shuffle_doors or self.options.shuffle_colors):
            if self.multiworld.players == 1:
                warning(f"{self.multiworld.get_player_name(self.player)}'s Lingo world doesn't have any progression"
                        f" items. Please turn on Door Shuffle or Color Shuffle if that doesn't seem right.")
            else:
                raise Exception(f"{self.multiworld.get_player_name(self.player)}'s Lingo world doesn't have any"
                                f" progression items. Please turn on Door Shuffle or Color Shuffle.")

        self.player_logic = LingoPlayerLogic(self)

    def create_regions(self):
        create_regions(self, self.player_logic)

    def create_items(self):
        pool = [self.create_item(name) for name in self.player_logic.real_items]

        if self.player_logic.forced_good_item != "":
            new_item = self.create_item(self.player_logic.forced_good_item)
            location_obj = self.multiworld.get_location("Second Room - Good Luck", self.player)
            location_obj.place_locked_item(new_item)

        item_difference = len(self.player_logic.real_locations) - len(pool)
        if item_difference:
            trap_percentage = self.options.trap_percentage
            traps = int(item_difference * trap_percentage / 100.0)
            non_traps = item_difference - traps

            if non_traps:
                skip_percentage = self.options.puzzle_skip_percentage
                skips = int(non_traps * skip_percentage / 100.0)
                non_skips = non_traps - skips

                for i in range(0, non_skips):
                    pool.append(self.create_item(self.get_filler_item_name()))

                for i in range(0, skips):
                    pool.append(self.create_item("Puzzle Skip"))

            if traps:
                total_weight = sum(self.options.trap_weights.values())

                if total_weight == 0:
                    raise Exception("Sum of trap weights must be at least one.")

                trap_counts = {name: int(weight * traps / total_weight)
                               for name, weight in self.options.trap_weights.items()}
                
                trap_difference = traps - sum(trap_counts.values())
                if trap_difference > 0:
                    allowed_traps = [name for name in TRAP_ITEMS if self.options.trap_weights[name] > 0]
                    for i in range(0, trap_difference):
                        trap_counts[allowed_traps[i % len(allowed_traps)]] += 1

                for name, count in trap_counts.items():
                    for i in range(0, count):
                        pool.append(self.create_item(name))

        self.multiworld.itempool += pool

    def create_item(self, name: str) -> Item:
        item = ALL_ITEM_TABLE[name]

        classification = item.classification
        if hasattr(self, "options") and self.options.shuffle_paintings and len(item.painting_ids) > 0 \
                and not item.has_doors and all(painting_id not in self.player_logic.painting_mapping
                                               for painting_id in item.painting_ids) \
                and "pilgrim_painting2" not in item.painting_ids:
            # If this is a "door" that just moves one or more paintings, and painting shuffle is on and those paintings
            # go nowhere, then this item should not be progression. The Pilgrim Room painting is special and needs to be
            # excluded from this.
            classification = ItemClassification.filler

        return LingoItem(name, classification, item.code, self.player)

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
            slot_data["painting_entrance_to_exit"] = self.player_logic.painting_mapping

        return slot_data

    def get_filler_item_name(self) -> str:
        filler_list = [":)", "The Feeling of Being Lost", "Wanderlust", "Empty White Hallways"]
        return self.random.choice(filler_list)
