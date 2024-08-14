from typing import Mapping, Any

from Options import OptionError
from .items import item_descriptions, item_table, ShapezItem, \
    buildings_routing, buildings_processing, buildings_other, \
    buildings_top_row, buildings_wires, gameplay_unlocks, upgrades, \
    big_upgrades, filler
from .locations import ShapezLocation, addlevels, all_locations, addupgrades, addachievements, location_description, \
    addshapesanity
from .presets import options_presets
from .options import ShapezOptions
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Item, Tutorial, LocationProgressType, ItemClassification
from .regions import create_shapez_regions


class ShapezWeb(WebWorld):
    options_presets = options_presets
    rich_text_options_doc = True
    theme = "stone"
    bug_report_page = "https://github.com/BlastSlimey/ShapezArchipelago/issues"
    game_info_languages = ['en', 'de']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing shapez with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    setup_de = Tutorial(
        "Multiworld-Setup-Anleitung",
        "Eine Anleitung zum Spielen von shapez in Archipelago",
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["BlastSlimey"]
    )
    tutorials = [setup_en, setup_de]
    item_descriptions = item_descriptions
    location_descriptions = location_description


class ShapezWorld(World):
    game = "shapez"
    options_dataclass = ShapezOptions
    options: ShapezOptions
    topology_present = True
    web = ShapezWeb()

    base_id = 20010707
    location_count: int = 0
    level_logic: list[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    upgrade_logic: list[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    maxlevel: int = 25
    finaltier: int = 8
    included_locations: dict[str, tuple[str, LocationProgressType]] = dict()
    client_seed: int = 123

    item_name_to_id = {name: id for
                       id, name in enumerate(item_table.keys(), base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(all_locations, base_id)}

    def generate_early(self):
        # "MAM" goal is supposed to be longer than vanilla, but to not have more options than necessary,
        # both goal amounts for "MAM" and "Even fasterer" are set in a single option.
        if self.options.goal.value == 1 and self.options.goal_amount.value < 27:
            raise OptionError("When setting goal to 1 ('mam'), goal_amount must be at least 27")

        # Determines maxlevel and finaltier, which are needed for location and item generation
        if self.options.goal.value == 0:
            self.maxlevel = 25
            self.finaltier = 8
        elif self.options.goal.value == 1:
            self.maxlevel = self.options.goal_amount.value - 1
            self.finaltier = 8
        elif self.options.goal.value == 2:
            self.maxlevel = 26
            self.finaltier = self.options.goal_amount.value
        else:
            self.maxlevel = 26
            self.finaltier = 8

        # Setting the seed for the game before any other randomization call is done
        self.client_seed = self.random.randint(0, 2**32)

        # Determines the order of buildings for levels und upgrades logic
        if self.options.randomize_level_requirements.value:
            if self.options.randomize_level_logic.value in [1, 3]:
                vanilla_list = ["Cutter", "Painter", "Stacker"]
                while len(vanilla_list) > 0:
                    index = self.random.randint(0, len(vanilla_list)-1)
                    next_building = vanilla_list.pop(index)
                    if next_building == "Cutter":
                        vanilla_list.append("Rotator")
                    if next_building == "Painter":
                        vanilla_list.append("Color Mixer")
                    self.level_logic.append(next_building)
            else:
                self.level_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
        else:
            self.level_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

        if self.options.randomize_upgrade_requirements.value:
            if self.options.randomize_upgrade_logic.value == 2:
                self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
            else:
                vanilla_list = ["Cutter", "Painter", "Stacker"]
                while len(vanilla_list) > 0:
                    index = self.random.randint(0, len(vanilla_list)-1)
                    next_building = vanilla_list.pop(index)
                    if next_building == "Cutter":
                        vanilla_list.append("Rotator")
                    if next_building == "Painter":
                        vanilla_list.append("Color Mixer")
                    self.upgrade_logic.append(next_building)
        else:
            self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

    def create_item(self, name: str) -> Item:
        return ShapezItem(name, item_table[name], self.item_name_to_id[name], self.player)

    def create_regions(self) -> None:
        # Create Menu region like in docs
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Create list of all included locations based on player options
        self.included_locations = {**addlevels(self.maxlevel, self.options.randomize_level_logic.value),
                                   **addupgrades(self.finaltier, self.options.randomize_upgrade_logic.value),
                                   # **addachievements
                                   **addshapesanity(self.options.shapesanity_amount.value, self.random, True)}
#                                                    bool(self.options.additional_locations.value > 0))}
        self.location_count = len(self.included_locations)

        # Create regions and entrances based on included locations and player options
        self.multiworld.regions.extend(create_shapez_regions(self.player, self.multiworld, self.included_locations,
                                                             self.location_name_to_id,
                                                             self.level_logic, self.upgrade_logic))

        goal_location = ShapezLocation(self.player, "Goal", None, None, None)
        goal_location.place_locked_item(ShapezItem("Goal", ItemClassification.progression, None, self.player))

        # Connect Menu to rest of regions
        menu_region.connect(self.multiworld.get_region("Main", self.player))

    def create_items(self) -> None:
        # Include guaranteed items (game mechanic unlocks and 7x4 big upgrades)
        included_items: list[Item] = ([self.create_item(name) for name in buildings_processing.keys()]
                                      + [self.create_item(name) for name in buildings_routing.keys()]
                                      + [self.create_item(name) for name in buildings_other.keys()]
                                      + [self.create_item(name) for name in buildings_top_row.keys()]
                                      + [self.create_item(name) for name in buildings_wires.keys()]
                                      + [self.create_item(name) for name in gameplay_unlocks.keys()]
                                      + [self.create_item(name) for name in big_upgrades for _ in range(7)])

        # Get value from traps probability option and convert to float
        traps_probability = self.options.traps_percentage.value/100
        # Fill remaining locations with fillers
        for x in range(self.location_count - len(included_items)):
            if self.random.random() < traps_probability:
                # Fill with trap (only 1 kind of traps atm)
                included_items.append(self.create_item("Inventory Draining Trap"))
            else:
                # Fil with random filler item
                included_items.append(self.create_item(filler(self.random.random())))

        # Add correct number of items to itempool
        self.multiworld.itempool += included_items

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Buildings logic; all buildings as individual parameters
        level_logic_data = {f"Level building {x+1}": self.level_logic[x] for x in range(5)}
        upgrade_logic_data = {f"Upgrade building {x+1}": self.upgrade_logic[x] for x in range(5)}

        # Options that are relevant to the mod
        option_data = {
            "goal": self.options.goal.value,
            "maxlevel": self.maxlevel,
            "finaltier": self.finaltier,
            "required_shapes_multiplier": self.options.required_shapes_multiplier.value,
            "randomize_level_requirements": bool(self.options.randomize_level_requirements.value),
            "randomize_upgrade_requirements": bool(self.options.randomize_upgrade_requirements.value),
            "randomize_level_logic": self.options.randomize_level_logic.value,
            "randomize_upgrade_logic": self.options.randomize_upgrade_logic.value,
            "same_late_upgrade_requirements": bool(self.options.same_late_upgrade_requirements.value)
        }

        return {**level_logic_data, **upgrade_logic_data, **option_data, "seed": self.client_seed}

