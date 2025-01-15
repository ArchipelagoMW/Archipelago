from random import Random

import settings
import string
import typing

from BaseClasses import Item, Tutorial, ItemClassification
from Options import NumericOption
from .Items import item_table, faction_table, Wargroove2Item
from .Levels import Wargroove2Level, low_victory_checks_levels, high_victory_checks_levels, first_level, \
    final_levels, region_names, FINAL_LEVEL_1, \
    FINAL_LEVEL_2, FINAL_LEVEL_3, FINAL_LEVEL_4, LEVEL_COUNT, FINAL_LEVEL_COUNT
from .Locations import location_table
from .Presets import wargroove2_option_presets
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld
from .Options import Wargroove2Options
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="Wargroove2Client")


components.append(Component("Wargroove 2 Client", game_name="Wargroove 2", func=launch_client, component_type=Type.CLIENT))


class Wargroove2Settings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """
        Locate the Wargroove 2 root directory on your system.
        This is used by the Wargroove 2 client, so it knows where to send communication files to
        """
        description = "Wargroove 2 root directory"

    root_directory: RootDirectory = RootDirectory("C:/Program Files (x86)/Steam/steamapps/common/Wargroove 2")


class Wargroove2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Wargroove 2 for Archipelago.",
        "English",
        "wargroove2_en.md",
        "wargroove2/en",
        ["Fly Sniper"]
    )]

    options_presets = wargroove2_option_presets


class Wargroove2World(World):
    """
    Command an army, in the sequel to the hit turn based strategy game Wargroove!
    """
    options: Wargroove2Options
    options_dataclass = Wargroove2Options
    settings: typing.ClassVar[Wargroove2Settings]
    game = "Wargroove 2"
    topology_present = True
    web = Wargroove2Web()
    level_list: typing.List[Wargroove2Level] = []
    final_levels: typing.List[Wargroove2Level] = []

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: code for name, code in location_table.items() if code is not None}

    def generate_early(self) -> None:
        if self.options.level_shuffle_seed.value == 0:
            random = self.random
        else:
            random = Random(str(self.options.level_shuffle_seed))

        low_victory_checks_levels_copy = low_victory_checks_levels.copy()
        high_victory_checks_levels_copy = high_victory_checks_levels.copy()
        random.shuffle(low_victory_checks_levels_copy)
        random.shuffle(high_victory_checks_levels_copy)
        non_starting_levels = high_victory_checks_levels_copy + low_victory_checks_levels_copy[4:]
        random.shuffle(non_starting_levels)
        self.level_list = low_victory_checks_levels_copy[0:4] + non_starting_levels

        final_levels_no_ocean = [level for level in final_levels if not level.has_ocean]
        final_levels_ocean = [level for level in final_levels if level.has_ocean]
        random.shuffle(final_levels_no_ocean)
        random.shuffle(final_levels_ocean)
        non_north_levels = final_levels_ocean + final_levels_no_ocean[1:]
        random.shuffle(non_north_levels)
        self.final_levels = final_levels_no_ocean[0:1] + non_north_levels

        # Selecting a random starting faction
        if self.options.commander_choice == "random_starting_faction":
            factions = [faction for faction in faction_table.keys() if faction != "Starter"]
            starting_faction = Wargroove2Item(self.random.choice(factions) + ' Commanders', self.player)
            self.multiworld.push_precollected(starting_faction)

    def create_items(self) -> None:
        # Fill out our pool with our items from the item table
        pool = []
        precollected_item_names = {item.name for item in self.multiworld.precollected_items[self.player]}
        ignore_faction_items = self.options.commander_choice == "locked_random"
        for name, data in item_table.items():
            if data.code is not None and name not in precollected_item_names and \
                    not data.classification == ItemClassification.filler:
                if name.endswith(' Commanders') and ignore_faction_items:
                    continue
                item = Wargroove2Item(name, self.player)
                pool.append(item)

        for _ in range(5):
            pool.append(Wargroove2Item("Commander Defense Boost", self.player))
            pool.append(Wargroove2Item("Income Boost", self.player))

        # Matching number of unfilled locations with filler items
        total_locations = 0
        total_locations += self.get_total_locations_in_level(first_level)

        for level in self.level_list[0:LEVEL_COUNT]:
            total_locations += self.get_total_locations_in_level(level)
        locations_remaining = total_locations - len(pool)
        while locations_remaining > 0:
            # Filling the pool equally with the groove boost
            pool.append(Wargroove2Item("Groove Boost", self.player))
            locations_remaining -= 1

        self.multiworld.itempool += pool

        victory = Wargroove2Item("Wargroove 2 Victory", self.player)
        for i in range(0, 4):
            final_level = self.final_levels[i]
            self.get_location(final_level.victory_location).place_locked_item(victory)
        # Placing victory event at final location
        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has("Wargroove 2 Victory", self.player, self.options.final_levels.value)

    def set_rules(self) -> None:
        set_rules(self)

    def create_item(self, name: str) -> Item:
        return Wargroove2Item(name, self.player)

    def create_regions(self) -> None:
        create_regions(self)

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        slot_data = {'seed': "".join(self.random.choice(string.ascii_letters) for _ in range(16))}
        for option_name in self.options.__dict__.keys():
            option = getattr(self.options, option_name)
            if isinstance(option, NumericOption):
                slot_data[option_name] = int(option.value)
            else:
                slot_data[option_name] = str(option.value)
        for i in range(0, min(LEVEL_COUNT, len(self.level_list))):
            slot_data[f"Level File #{i}"] = self.level_list[i].file_name
            slot_data[region_names[i]] = self.level_list[i].name
            for location_name in self.level_list[i].location_rules.keys():
                slot_data[location_name] = region_names[i]
        for i in range(0, FINAL_LEVEL_COUNT):
            slot_data[f"Final Level File #{i}"] = self.final_levels[i].file_name
        slot_data[FINAL_LEVEL_1] = self.final_levels[0].name
        for location_name in self.final_levels[0].location_rules.keys():
            slot_data[location_name] = FINAL_LEVEL_1
        slot_data[FINAL_LEVEL_2] = self.final_levels[1].name
        for location_name in self.final_levels[0].location_rules.keys():
            slot_data[location_name] = FINAL_LEVEL_2
        slot_data[FINAL_LEVEL_3] = self.final_levels[2].name
        for location_name in self.final_levels[0].location_rules.keys():
            slot_data[location_name] = FINAL_LEVEL_3
        slot_data[FINAL_LEVEL_4] = self.final_levels[3].name
        for location_name in self.final_levels[0].location_rules.keys():
            slot_data[location_name] = FINAL_LEVEL_4
        return slot_data

    def get_filler_item_name(self) -> str:
        return "Groove Boost"

    def get_total_locations_in_level(self, level: Wargroove2Level) -> int:
        total_locations = 0
        for location_name in level.location_rules.keys():
            if location_name.endswith("Victory"):
                total_locations += self.options.victory_locations
            else:
                total_locations += self.options.objective_locations
        return total_locations
