import threading
from random import Random

import settings
import string
import typing

from BaseClasses import Item, Tutorial, ItemClassification, MultiWorld
from Options import NumericOption, OptionSet
from .Items import item_table, faction_table, Wargroove2Item
from .Levels import Wargroove2Level, low_victory_checks_levels, high_victory_checks_levels, first_level, \
    final_levels, region_names, FINAL_LEVEL_1, \
    FINAL_LEVEL_2, FINAL_LEVEL_3, FINAL_LEVEL_4, LEVEL_COUNT, FINAL_LEVEL_COUNT, main_filler_levels, \
    final_filler_levels, region_names_to_distance
from .Locations import location_table, Wargroove2Location
from .Presets import wargroove2_option_presets
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld
from .Options import Wargroove2Options, wargroove2_option_groups
from worlds.LauncherComponents import Component, components, Type, launch as launch_component


def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="Wargroove2Client", args=args)


components.append(Component("Wargroove 2 Client", game_name="Wargroove 2", func=launch_client, component_type=Type.CLIENT))


class Wargroove2Settings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """
        Locate the Wargroove 2 root directory on your system.
        This is used by the Wargroove 2 client, so it knows where to send communication files to
        """
        description = "Wargroove 2 root directory"


    class SaveDirectory(settings.UserFolderPath):
        """
        Locates the Wargroove 2 save file directory on your system.
        This is used by the Wargroove 2 client, so it knows where to send mod and save files to.
        """
        description = "Appdata directory containing the Chucklefish/Wargroove2 folders."

    root_directory: RootDirectory = RootDirectory("C:/Program Files (x86)/Steam/steamapps/common/Wargroove 2")
    save_directory: SaveDirectory = SaveDirectory("%APPDATA%")


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
    option_groups = wargroove2_option_groups


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
    random_barracks_cost_values: typing.List[int] = []
    random_tower_cost_values: typing.List[int] = []
    random_hideout_cost_values: typing.List[int] = []
    random_port_cost_values: typing.List[int] = []
    ai_random_barracks_cost_values: typing.List[int] = []
    ai_random_tower_cost_values: typing.List[int] = []
    ai_random_hideout_cost_values: typing.List[int] = []
    ai_random_port_cost_values: typing.List[int] = []
    player_barracks_costs: typing.Dict[int, float] = {}
    player_tower_costs: typing.Dict[int, float] = {}
    player_hideout_costs: typing.Dict[int, float] = {}
    player_port_costs: typing.Dict[int, float] = {}
    ai_barracks_costs: typing.Dict[int, float] = {}
    ai_tower_costs: typing.Dict[int, float] = {}
    ai_hideout_costs: typing.Dict[int, float] = {}
    ai_port_costs: typing.Dict[int, float] = {}
    fill_slot_data_event: threading.Event = threading.Event()
    stage_assert_generate_called: bool = False
    filler_item_counter: int = 0

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: code for name, code in location_table.items() if code is not None}

    def generate_early(self) -> None:
        early_level_slots = 4
        main_level_slots = LEVEL_COUNT - early_level_slots
        final_level_no_ocean_slots = 1

        self.random_barracks_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]
        self.random_tower_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]
        self.random_hideout_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]
        self.random_port_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]
        self.ai_random_barracks_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]
        self.ai_random_tower_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]
        self.ai_random_hideout_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]
        self.ai_random_port_cost_values = [self.random.randrange(0, 100)
                                            for _ in range(LEVEL_COUNT + FINAL_LEVEL_COUNT)]

        if self.options.level_shuffle_seed.value == 0:
            random = self.random
        else:
            random = Random(str(self.options.level_shuffle_seed))

        low_victory_checks_levels_copy = low_victory_checks_levels.copy()
        high_victory_checks_levels_copy = high_victory_checks_levels.copy()
        final_filler_levels_copy = final_filler_levels.copy()
        low_victory_checks_levels_copy = [level for level in low_victory_checks_levels_copy
                                          if level.name in self.options.custom_early_level_playlist.value]
        high_victory_checks_levels_copy = [level for level in high_victory_checks_levels_copy
                                          if level.name in self.options.custom_main_level_playlist.value]
        while len(low_victory_checks_levels_copy) < early_level_slots:
            low_victory_checks_levels_copy.append(random.choice(main_filler_levels))
        while len(high_victory_checks_levels_copy) < main_level_slots:
            high_victory_checks_levels_copy.append(random.choice(main_filler_levels))

        random.shuffle(low_victory_checks_levels_copy)
        random.shuffle(high_victory_checks_levels_copy)
        self.level_list = low_victory_checks_levels_copy[0:early_level_slots] + high_victory_checks_levels_copy

        final_levels_no_ocean = [level for level in final_levels
                                 if not level.has_ocean and level.name in self.options.custom_final_level_playlist]
        final_levels_ocean = [level for level in final_levels if level.has_ocean
                              and level.name in self.options.custom_final_level_playlist]
        while len(final_levels_no_ocean) < final_level_no_ocean_slots:
            final_filler_level = random.choice(final_filler_levels_copy)
            final_filler_levels_copy.remove(final_filler_level)
            final_levels_no_ocean.append(final_filler_level)
        while len(final_levels_ocean) + len(final_levels_no_ocean) < FINAL_LEVEL_COUNT:
            final_filler_level = random.choice(final_filler_levels_copy)
            final_filler_levels_copy.remove(final_filler_level)
            final_levels_ocean.append(final_filler_level)

        random.shuffle(final_levels_no_ocean)
        random.shuffle(final_levels_ocean)
        non_north_levels = final_levels_ocean + final_levels_no_ocean[final_level_no_ocean_slots:]
        random.shuffle(non_north_levels)
        self.final_levels = final_levels_no_ocean[0:final_level_no_ocean_slots] + non_north_levels

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


    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        cls.stage_assert_generate_called = True


    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory):
        player_to_sphere: dict[int, typing.List[typing.Tuple[int, str]]] = {}
        sphere_number = 0
        highest_wg2_sphere = 0
        for sphere in multiworld.get_spheres():
            for location in sphere:
                if location.game == "Wargroove 2":
                    assert isinstance(location, Wargroove2Location)
                    if (location.game == "Wargroove 2" and location.name.endswith("Victory") and
                            location.name != "Humble Beginnings Rebirth: Victory"):
                        if location.player in player_to_sphere:
                            player_to_sphere[location.player].append((sphere_number, location.parent_region.name))
                        else:
                            player_to_sphere[location.player] = [(sphere_number, location.parent_region.name)]
                        highest_wg2_sphere = sphere_number
            sphere_number += 1
        for world in multiworld.get_game_worlds("Wargroove 2"):
            assert isinstance(world, Wargroove2World)
            world.player_barracks_costs = calculate_production_costs(
                                       world.options.player_barracks_early_sphere.value / 100.0,
                                       world.options.player_barracks_late_sphere.value / 100.0,
                                       world.options.player_barracks_early_distance.value / 100.0,
                                       world.options.player_barracks_late_distance.value / 100.0,
                                       world.options.player_barracks_random_low_cost.value / 100.0,
                                       world.options.player_barracks_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.random_barracks_cost_values,
                                       player_to_sphere, world)
            world.player_tower_costs = calculate_production_costs(
                                       world.options.player_tower_early_sphere.value / 100.0,
                                       world.options.player_tower_late_sphere.value / 100.0,
                                       world.options.player_tower_early_distance.value / 100.0,
                                       world.options.player_tower_late_distance.value / 100.0,
                                       world.options.player_tower_random_low_cost.value / 100.0,
                                       world.options.player_tower_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.random_tower_cost_values,
                                       player_to_sphere, world)
            world.player_hideout_costs = calculate_production_costs(
                                       world.options.player_hideout_early_sphere.value / 100.0,
                                       world.options.player_hideout_late_sphere.value / 100.0,
                                       world.options.player_hideout_early_distance.value / 100.0,
                                       world.options.player_hideout_late_distance.value / 100.0,
                                       world.options.player_hideout_random_low_cost.value / 100.0,
                                       world.options.player_hideout_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.random_hideout_cost_values,
                                       player_to_sphere, world)
            world.player_port_costs = calculate_production_costs(
                                       world.options.player_port_early_sphere.value / 100.0,
                                       world.options.player_port_late_sphere.value / 100.0,
                                       world.options.player_port_early_distance.value / 100.0,
                                       world.options.player_port_late_distance.value / 100.0,
                                       world.options.player_port_random_low_cost.value / 100.0,
                                       world.options.player_port_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.random_port_cost_values,
                                       player_to_sphere, world)
            world.ai_barracks_costs = calculate_production_costs(
                                       world.options.ai_barracks_early_sphere.value / 100.0,
                                       world.options.ai_barracks_late_sphere.value / 100.0,
                                       world.options.ai_barracks_early_distance.value / 100.0,
                                       world.options.ai_barracks_late_distance.value / 100.0,
                                       world.options.ai_barracks_random_low_cost.value / 100.0,
                                       world.options.ai_barracks_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.ai_random_barracks_cost_values,
                                       player_to_sphere, world)
            world.ai_tower_costs = calculate_production_costs(
                                       world.options.ai_tower_early_sphere.value / 100.0,
                                       world.options.ai_tower_late_sphere.value / 100.0,
                                       world.options.ai_tower_early_distance.value / 100.0,
                                       world.options.ai_tower_late_distance.value / 100.0,
                                       world.options.ai_tower_random_low_cost.value / 100.0,
                                       world.options.ai_tower_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.ai_random_tower_cost_values,
                                       player_to_sphere, world)
            world.ai_hideout_costs = calculate_production_costs(
                                       world.options.ai_hideout_early_sphere.value / 100.0,
                                       world.options.ai_hideout_late_sphere.value / 100.0,
                                       world.options.ai_hideout_early_distance.value / 100.0,
                                       world.options.ai_hideout_late_distance.value / 100.0,
                                       world.options.ai_hideout_random_low_cost.value / 100.0,
                                       world.options.ai_hideout_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.ai_random_hideout_cost_values,
                                       player_to_sphere, world)
            world.ai_port_costs = calculate_production_costs(
                                       world.options.ai_port_early_sphere.value / 100.0,
                                       world.options.ai_port_late_sphere.value / 100.0,
                                       world.options.ai_port_early_distance.value / 100.0,
                                       world.options.ai_port_late_distance.value / 100.0,
                                       world.options.ai_port_random_low_cost.value / 100.0,
                                       world.options.ai_port_random_high_cost.value / 100.0,
                                       highest_wg2_sphere, world.ai_random_port_cost_values,
                                       player_to_sphere, world)
            world.fill_slot_data_event.set()

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        if self.stage_assert_generate_called:
            self.fill_slot_data_event.wait()
        slot_data = {'seed': "".join(self.random.choice(string.ascii_letters) for _ in range(16))}
        for option_name in self.options.__dict__.keys():
            option = getattr(self.options, option_name)
            if isinstance(option, NumericOption):
                slot_data[option_name] = int(option.value)
            elif isinstance(option, OptionSet):
                option_set = list(option.value)
                option_set_length = len(option_set)
                slot_data[f"{option_name}_length"] = option_set_length
                for i in range(0, option_set_length):
                    slot_data[f"{option_name} #{i}"] = str(option_set[i])
            else:
                slot_data[option_name] = str(option.value)
        for i in range(0, min(LEVEL_COUNT, len(self.level_list))):
            slot_data[f"Level File #{i}"] = self.level_list[i].file_name
            slot_data[region_names[i]] = self.level_list[i].name
            slot_data[f"Level Barracks Cost #{i}"] = f"{self.player_barracks_costs.get(i, 100):.2f}"
            slot_data[f"Level Tower Cost #{i}"] = f"{self.player_tower_costs.get(i, 100):.2f}"
            slot_data[f"Level Hideout Cost #{i}"] = f"{self.player_hideout_costs.get(i, 100):.2f}"
            slot_data[f"Level Port Cost #{i}"] = f"{self.player_port_costs.get(i, 100):.2f}"
            slot_data[f"Level AI Barracks Cost #{i}"] = f"{self.ai_barracks_costs.get(i, 100):.2f}"
            slot_data[f"Level AI Tower Cost #{i}"] = f"{self.ai_tower_costs.get(i, 100):.2f}"
            slot_data[f"Level AI Hideout Cost #{i}"] = f"{self.ai_hideout_costs.get(i, 100):.2f}"
            slot_data[f"Level AI Port Cost #{i}"] = f"{self.ai_port_costs.get(i, 100):.2f}"
            for location_name in self.level_list[i].location_rules.keys():
                slot_data[location_name] = region_names[i]
        for i in range(0, FINAL_LEVEL_COUNT):
            slot_data[f"Final Level File #{i}"] = self.final_levels[i].file_name
            slot_data[f"Level Barracks Cost #{i + LEVEL_COUNT}"] = \
                f"{self.player_barracks_costs.get(i + LEVEL_COUNT, 100):.2f}"
            slot_data[f"Level Tower Cost #{i + LEVEL_COUNT}"] = \
                f"{self.player_tower_costs.get(i + LEVEL_COUNT, 100):.2f}"
            slot_data[f"Level Hideout Cost #{i + LEVEL_COUNT}"] = \
                f"{self.player_hideout_costs.get(i + LEVEL_COUNT, 100):.2f}"
            slot_data[f"Level Port Cost #{i + LEVEL_COUNT}"] = \
                f"{self.player_port_costs.get(i + LEVEL_COUNT, 100):.2f}"
            slot_data[f"Level AI Barracks Cost #{i + LEVEL_COUNT}"] = \
                f"{self.ai_barracks_costs.get(i + LEVEL_COUNT, 100):.2f}"
            slot_data[f"Level AI Tower Cost #{i + LEVEL_COUNT}"] = \
                f"{self.ai_tower_costs.get(i + LEVEL_COUNT, 100):.2f}"
            slot_data[f"Level AI Hideout Cost #{i + LEVEL_COUNT}"] = \
                f"{self.ai_hideout_costs.get(i + LEVEL_COUNT, 100):.2f}"
            slot_data[f"Level AI Port Cost #{i + LEVEL_COUNT}"] = \
                f"{self.ai_port_costs.get(i + LEVEL_COUNT, 100):.2f}"
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
        filler_item_name: str = "Groove Boost"
        if (self.filler_item_counter % 3) == 0:
            filler_item_name = "Income Boost"

        self.filler_item_counter += 1
        return filler_item_name

    def get_total_locations_in_level(self, level: Wargroove2Level) -> int:
        total_locations = 0
        for location_name in level.location_rules.keys():
            if location_name.endswith("Victory"):
                total_locations += self.options.victory_locations
            else:
                total_locations += self.options.objective_locations
        return total_locations

#############
# Functions #
#############

def calculate_production_costs(early_sphere: float, late_sphere: float,
                                close_distance: float, far_distance: float,
                                min_random: float, max_random: float,
                                highest_wg2_sphere: int,
                                random_values: typing.List[int],
                                player_to_sphere: dict[int, list[tuple[int, str]]], world) -> dict[int, float]:
    level_distance_to_cost: dict[int, float] = {}
    min_random_tmp = min_random
    max_random_tmp = max_random
    min_random = min(min_random_tmp, max_random_tmp)
    max_random = max(min_random_tmp, max_random_tmp)
    max_range = max(min_random, max_random, far_distance, close_distance, late_sphere, early_sphere)
    min_range = min(min_random, max_random, far_distance, close_distance, late_sphere, early_sphere)
    index = 0
    for sphere_data in player_to_sphere[world.player]:
        current_sphere = sphere_data[0]
        region_distance = region_names_to_distance[sphere_data[1]]
        sphere_value = (current_sphere / highest_wg2_sphere)
        sphere_percentage = early_sphere + sphere_value * (late_sphere - early_sphere)
        distance_value = region_distance / (LEVEL_COUNT + FINAL_LEVEL_COUNT)
        distance_percentage = close_distance + (distance_value * (far_distance - close_distance))
        random_value = random_values[index] / 100.0
        random_percentage = min_random + (random_value * (max_random - min_random))
        cost = (sphere_percentage + distance_percentage + random_percentage) / 3.0
        cost_min = (min(early_sphere, late_sphere) + min(close_distance, far_distance) + min_random) / 3.0
        cost_max = (max(early_sphere, late_sphere) + max(close_distance, far_distance) + max_random) / 3.0
        if cost_max == cost_min:
            cost_min -= 0.01
        cost = min_range + ((cost - cost_min) * (max_range - min_range) / (cost_max - cost_min))
        level_distance_to_cost[region_distance] = cost
        index += 1

    for i in range(0, LEVEL_COUNT + FINAL_LEVEL_COUNT):
        if i not in level_distance_to_cost.keys():
            level_distance_to_cost[i] = 1.0
    return level_distance_to_cost
