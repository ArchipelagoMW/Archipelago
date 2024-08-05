from typing import Mapping, Any

import settings
import typing
from .items import item_descriptions, item_table, ShapezItem, \
    buildings_routing, buildings_processing, buildings_other, \
    buildings_top_row, buildings_wires, gameplay_unlocks, upgrades, \
    big_upgrades, fillers  # data used below to add items to the World
from .locations import ShapezLocation, addlevels, all_locations, addupgrades, addachievements
from .presets import options_presets
from .options import ShapezOptions
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Item, ItemClassification, Tutorial, LocationProgressType
from .regions import create_shapez_regions


class ShapezSettings(settings.Group):
    game = "Shapez"


class ShapezWeb(WebWorld):
    options_presets = options_presets
    rich_text_options_doc = True
    theme = "stone"
    bug_report_page = "https://github.com/BlastSlimey/ShapezArchipelago/issues"
    game_info_languages = ['en', 'de']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Shapez with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    setup_de = Tutorial(
        "Multiworld-Setup-Anleitung",
        "Eine Anleitung zum Spielen von Shapez in Archipelago",
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["BlastSlimey"]
    )
    tutorials = [setup_en, setup_de]
    item_descriptions = item_descriptions


class ShapezWorld(World):
    """Insert description of the world/game here."""
    game = "Shapez"  # name of the game/world
    options_dataclass = ShapezOptions  # options the player can set
    options: ShapezOptions  # typing hints for option results
    settings: typing.ClassVar[ShapezSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # TODO TestBase, Docs

    base_id = 20010707
    location_count: int = 0
    level_logic: list[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    upgrade_logic: list[str] = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
    maxlevel: int = 25
    finaltier: int = 8
    included_locations: dict[str, tuple[str, LocationProgressType]] = dict()
    # victory_loc = MyGameLocation(self.player, "Victory", None)
    # victory_loc.place_locked_item(MyGameItem("Victory", ItemClassification.progression, None, self.player))

    item_name_to_id = {name: id for
                       id, name in enumerate(item_table.keys(), base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(all_locations, base_id)}

    def generate_early(self):
        # Load necessary options atm
        goal = self.options.goal
        goal_amount = self.options.goal_amount
        randomize_level_requirements = self.options.randomize_level_requirements
        randomize_upgrade_requirements = self.options.randomize_upgrade_requirements
        randomize_level_logic = self.options.randomize_level_logic
        randomize_upgrade_logic = self.options.randomize_upgrade_logic

        # Determines maxlevel and finaltier, which are needed for location and item generation
        if goal == 0:
            self.maxlevel = 25
            self.finaltier = 8
        elif goal == 1:
            self.maxlevel = goal_amount.value - 1
            self.finaltier = 8
        elif goal == 2:
            self.maxlevel = 26
            self.finaltier = goal_amount.value
        else:
            self.maxlevel = 26
            self.finaltier = 8

        # Determines the order of buildings for logic
        if randomize_level_requirements:
            if randomize_level_logic in [1, 3]:
                vanilla_list = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
                for i in range(4, -1, -1):
                    next_building = self.random.randint(0, i)
                    self.level_logic.append(vanilla_list.pop(next_building))
            else:
                self.level_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
        else:
            self.level_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

        if randomize_upgrade_requirements:
            if randomize_upgrade_logic == 2:
                self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
            else:
                vanilla_list = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]
                for i in range(4, -1, -1):
                    next_building = self.random.randint(0, i)
                    self.upgrade_logic.append(vanilla_list.pop(next_building))
        else:
            self.upgrade_logic = ["Cutter", "Rotator", "Painter", "Color Mixer", "Stacker"]

    def create_item(self, name: str) -> Item:
        return ShapezItem(name, item_table[name], self.item_name_to_id[name], self.player)

    def create_event_item(self, event: str) -> Item:
        return ShapezItem(event, ItemClassification.progression, None, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        self.included_locations = {**addlevels(self.maxlevel, self.options.randomize_level_logic.value),
                                   **addupgrades(self.finaltier, self.options.randomize_upgrade_logic.value),
                                   **addachievements(bool(self.options.include_achievements.value),
                                                     bool(self.options.exclude_softlock_achievements.value),
                                                     bool(self.options.exclude_long_playtime_achievements.value),
                                                     bool(self.options.exclude_progression_softlock_long_playtime.value),
                                                     self.maxlevel, self.options.randomize_level_logic.value,
                                                     self.finaltier, self.options.randomize_upgrade_logic.value,
                                                     self.options.goal.value)}
        menu_region.connect(self.multiworld.get_region("Main", self.player))
        self.location_count = len(self.included_locations)
        self.multiworld.regions.extend(create_shapez_regions(self))

    def create_items(self) -> None:
        # Include guaranteed items (game mechanic unlocks and 7x4 big upgrades)
        included_items: list[Item] = ([self.create_item(name) for name in buildings_routing.keys()]
                                      + [self.create_item(name) for name in buildings_processing.keys()]
                                      + [self.create_item(name) for name in buildings_other.keys()]
                                      + [self.create_item(name) for name in buildings_top_row.keys()]
                                      + [self.create_item(name) for name in buildings_wires.keys()]
                                      + [self.create_item(name) for name in gameplay_unlocks.keys()]
                                      + [self.create_item(name) for name in big_upgrades for _ in range(7)])

        # Get value from traps probability option and convert into float
        traps_probability = self.options.traps_percentage.value/100
        # Fill remaining locations with fillers
        for x in range(self.location_count - len(included_items)):
            # Fill with trap (only 1 kind of traps atm)
            if self.multiworld.random.random() < traps_probability:
                included_items.append(self.create_item("Inventory Draining Trap"))
            else:
                # Fil with random filler item (all equal chance)
                included_items.append(self.create_item(fillers[self.multiworld.random.randint(0, len(fillers)-1)]))

        self.multiworld.itempool += included_items

    def fill_slot_data(self) -> Mapping[str, Any]:
        level_logic_data = {f"Level building {x+1}": self.level_logic[x] for x in range(5)}
        upgrade_logic_data = {f"Upgrade building {x+1}": self.upgrade_logic[x] for x in range(5)}
        option_data = {
            "goal": self.options.goal.value,
            "goal_amount": self.options.goal_amount.value,
            "required_shapes_multiplier": self.options.required_shapes_multiplier.value,
            "randomize_level_requirements": bool(self.options.randomize_level_requirements.value),
            "randomize_upgrade_requirements": bool(self.options.randomize_upgrade_requirements.value),
            "randomize_level_logic": self.options.randomize_level_logic.value,
            "randomize_upgrade_logic": self.options.randomize_upgrade_logic.value,
            "same_late_upgrade_requirements": self.options.same_late_upgrade_requirements.value,
            "include_achievements": self.options.include_achievements.value,
            "exclude_softlock_achievements": self.options.exclude_softlock_achievements.value,
            "exclude_long_playtime_achievements": self.options.exclude_long_playtime_achievements.value
        }
        # Client also needs the seed, do I need to send it per slot data?
        return {**level_logic_data, **upgrade_logic_data, **option_data}
