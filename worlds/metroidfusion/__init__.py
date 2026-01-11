import json
import logging
import os
from copy import deepcopy, copy

import Utils
import settings
import typing

from typing import Dict, Any, TextIO
from BaseClasses import MultiWorld, ItemClassification, Tutorial, Item, Region, EntranceType, CollectionState
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule
from .Entrance import FusionEntrance
from .Hints import create_hints, HintedPair

from .Items import item_table, default_item_quantities, ap_name_to_mars_name, major_upgrades
from .Locations import all_locations, MetroidFusionLocation, get_location_data_by_name, build_item_message, \
    location_groups, build_shiny_item_message, ERGroups
from .Logic import create_logic_rule, create_logic_rule_for_list, LogicObject
from .Options import MetroidFusionOptions, metroid_fusion_option_groups
from .Rom import MetroidFusionProcedurePatch
from .StartingLocations import main_deck_hub, StartingLocation, sector_hub, starting_location_data, operations_deck
from .data import memory
from .data.items import events
from .data.locations import (fusion_regions, left_tubes, right_tubes, sector_elevator_tops, sector_elevator_bottoms,
                             other_elevator_tops, other_elevator_bottoms, sector_tube_id_lookups, elevator_id_lookups,
                             sector_elevators, other_elevators)
from .data.logic.VariableConnection import VariableConnection
from .data.logic.RegionMap import default_region_map, reverse_region_map
from .data.logic.regions.MainDeck import (OperationsDeck, SectorHubElevator1Top, SectorHubElevator2Top,
                                          SectorHubElevator3Top, SectorHubElevator4Top, SectorHubElevator5Top,
                                          SectorHubElevator6Top, SectorHubElevatorTop, HabitationDeckElevatorTop,
                                          OperationsDeckElevatorBottom, SectorHubElevatorBottom,
                                          OperationsDeckElevatorTop, HabitationDeckElevatorBottom)
from .data.logic.regions.Sector1 import Sector1Hub, Sector1TubeLeft, Sector1TubeRight, Sector1TourianHub, \
    Sector1TourianHubElevatorTop
from .data.logic.regions.Sector2 import Sector2Hub, Sector2TubeLeft, Sector2TubeRight
from .data.logic.regions.Sector3 import Sector3Hub, Sector3TubeLeft, Sector3TubeRight
from .data.logic.regions.Sector4 import Sector4Hub, Sector4TubeLeft, Sector4TubeRight
from .data.logic.regions.Sector5 import Sector5Hub, Sector5TubeLeft, Sector5TubeRight
from .data.logic.regions.Sector6 import (Sector6Hub, Sector6TubeLeft, Sector6TubeRight,
                                         Sector6RestrictedZoneElevatorToTourian)
from .data.major_locations import boss_locations
from .data.offworld_sprites import offworld_sprites, SpriteNames
from .data.room_names import room_names
from .Client import MetroidFusionClient


class MetroidFusionSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Metroid Fusion ROM"""
        description = "Metroid Fusion (USA) ROM File"
        copy_to = "Metroid Fusion (USA).gba"
        md5s = ["af5040fc0f579800151ee2a683e2e5b5"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True
    display_location_found_messages: bool = True


class MetroidFusionWeb(WebWorld):
    theme = "ocean"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Metroid Fusion for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rosalie"]
    )

    tutorials = [setup]

    rich_text_options_doc = True
    option_groups = metroid_fusion_option_groups


class MetroidFusionWorld(World):
    """
    Metroid Fusion, powered by MARS. The fourth Metroid game, known for its linearity, in randomized form!
    Locate the Infant Metroids to lure out the SA-X, set the self destruct, and escape the station.
    """
    settings: typing.ClassVar[MetroidFusionSettings]
    game = "Metroid Fusion"
    options_dataclass = MetroidFusionOptions
    options: MetroidFusionOptions

    topology_present = True
    base_id = 0
    web = MetroidFusionWeb()
    hint_text: list[str] | None
    hint_pairs: list[HintedPair] | None
    region_map: dict[str, str]
    spoiler_region_map: dict[str, str]
    er_map: list[tuple[str, str]] = None
    preplaced_item: str = None

    starting_region: str = None
    starting_location: str = None
    starting_location_object: StartingLocation
    starting_region: Region
    starting_major_upgrades: int = 0
    starting_energy_tanks: int = 0
    open_sector_elevators: bool = False
    navigation_room_hint_locks: bool = False

    er_group_mappings = {
        ERGroups.TUBE_LEFT: [ERGroups.TUBE_RIGHT],
        ERGroups.TUBE_RIGHT: [ERGroups.TUBE_LEFT],
        ERGroups.ELEVATOR_TOP: [ERGroups.ELEVATOR_BOTTOM],
        ERGroups.ELEVATOR_BOTTOM: [ERGroups.ELEVATOR_TOP],
    }

    item_name_to_id = {item: item_data.mars_id for item, item_data in item_table.items()}
    location_name_to_id = {location.name: location.ap_id for location in all_locations}
    location_name_groups = location_groups
    item_name_groups = {
        "MajorUpgrades": major_upgrades
    }
    version = 17
    debug = False



    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.filler_items = None
        self.hint_text = None
        self.hint_pairs = None
        self.region_map = dict()
        self.spoiler_region_map = dict()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        logging.info(f"Metroid Fusion APWorld v{cls.version} used for generation.")

    @classmethod
    def stage_write_spoiler_header(cls, _multiworld: MultiWorld, spoiler_handle: TextIO):
        spoiler_handle.write(f"\nMetroid Fusion APWorld version: v{cls.version}\n")

    def create_item(self, name: str) -> "MetroidFusionItem":
        return MetroidFusionItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> "MetroidFusionItem":
        return MetroidFusionItem(name, ItemClassification.progression, None, self.player)

    def parse_game_mode_options(self):
        if self.options.GameMode == self.options.GameMode.option_vanilla:
            if self.starting_location is None:
                self.starting_region = "Main Deck Hub"
                self.starting_location = "Docking Bay"
                self.starting_location_object = main_deck_hub
            self.starting_major_upgrades = 0
            self.starting_energy_tanks = 0
            self.open_sector_elevators = False
            self.navigation_room_hint_locks = False
        elif self.options.GameMode == self.options.GameMode.option_open_sector_hub:
            if self.starting_location is None:
                self.starting_region = "Sector Hub Elevator Bottom"
                self.starting_location = "Sector Hub"
                self.starting_location_object = sector_hub
            self.starting_major_upgrades = 1
            self.starting_energy_tanks = 1
            self.open_sector_elevators = True
            self.navigation_room_hint_locks = True
        elif self.options.GameMode == self.options.GameMode.option_custom:
            if self.starting_location is None:
                if self.options.StartingLocation == self.options.StartingLocation.option_docking_bay:
                    self.starting_region = "Main Deck Hub"
                    self.starting_location = "Docking Bay"
                    self.starting_location_object = main_deck_hub
                elif self.options.StartingLocation == self.options.StartingLocation.option_operations_deck:
                    self.starting_region = "Operations Deck"
                    self.starting_location = "Operations Deck"
                    self.starting_location_object = operations_deck
                elif self.options.StartingLocation == self.options.StartingLocation.option_sector_hub:
                    self.starting_region = "Sector Hub Elevator Bottom"
                    self.starting_location = "Sector Hub"
                    self.starting_location_object = sector_hub
                elif self.options.StartingLocation == self.options.StartingLocation.option_concourse_save_station:
                    self.starting_region = "Main Deck Hub"
                    self.starting_location = "Concourse Save Station"
                    self.starting_location_object = main_deck_hub
            self.starting_major_upgrades = self.options.StartingMajorUpgrades.value
            self.starting_energy_tanks = self.options.StartingEnergyTanks.value
            self.open_sector_elevators = bool(self.options.OpenSectorElevators.value)
            self.navigation_room_hint_locks = bool(self.options.SectorNavigationRoomHintLocks.value)

    def generate_early(self) -> None:
        self.parse_game_mode_options()
        for origin, destination in default_region_map.items():
            self.region_map[origin.name] = destination.name
        for origin, destination in reverse_region_map.items():
            self.region_map[origin.name] = destination.name

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        for region_data in fusion_regions:
            region = Region(region_data.name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        starting_region = self.get_region(self.starting_region)
        menu.connect(starting_region)

        # Define connections
        for origin_region_data in fusion_regions:
            origin_region = self.get_region(origin_region_data.name)
            for connection in origin_region_data.connections:
                connecting_region = self.get_region(connection.destination.name)
                logic_object = LogicObject(self.player, self.options)
                if self.debug:
                    print(f"{'One way connection' if connection.one_way else 'Two way connection'}: "
                          f"{origin_region.name} to {connecting_region.name}")
                logic_object.requirements, logic_object.energy_tanks = create_logic_rule_for_list(
                    connection.requirements,
                    self.options,
                    self.debug)
                connection_name = f"{origin_region.name} to {connecting_region.name}"
                entrance_type = EntranceType.ONE_WAY if connection.one_way else EntranceType.TWO_WAY
                if connection.__class__ == VariableConnection:
                    if "Tube" in connection.destination.name:
                        if "Left" in connection.destination.name:
                            group = ERGroups.TUBE_RIGHT if self.options.SectorTubeShuffle else ERGroups.STATIC
                        else:
                            group = ERGroups.TUBE_LEFT if self.options.SectorTubeShuffle else ERGroups.STATIC
                    else:
                        if self.options.ElevatorShuffle == self.options.ElevatorShuffle.option_sectors:
                            eligible_elevators = sector_elevators
                        elif self.options.ElevatorShuffle == self.options.ElevatorShuffle.option_all:
                            eligible_elevators = [*sector_elevators, *other_elevators]
                        else:
                            eligible_elevators = []
                        if origin_region_data in eligible_elevators:
                            if "Top" in connection.destination.name:
                                group = ERGroups.ELEVATOR_BOTTOM
                            else:
                                group = ERGroups.ELEVATOR_TOP
                        else:
                            group = ERGroups.STATIC
                    connection_name = origin_region.name + " Destination"
                else:
                    group = ERGroups.STATIC
                new_entrance = FusionEntrance(self.player, connection_name, origin_region, group, entrance_type)
                new_entrance.access_rule = logic_object.logic_rule
                origin_region.exits.append(new_entrance)
                new_entrance.connect(connecting_region)
                if group != ERGroups.STATIC:
                    disconnect_entrance_for_randomization(new_entrance)
                elif entrance_type == EntranceType.TWO_WAY:
                    connection_name = f"{origin_region.name} from {connecting_region.name}"
                    new_entrance = FusionEntrance(self.player, connection_name, connecting_region, group, entrance_type)
                    new_entrance.access_rule = logic_object.logic_rule
                    connecting_region.exits.append(new_entrance)
                    new_entrance.connect(origin_region)
            for location in origin_region_data.locations:
                new_location = MetroidFusionLocation(
                    self.player,
                    location.name,
                    self.location_name_to_id[location.name],
                    origin_region
                )
                origin_region.locations.append(new_location)
        for event in events:
            region = self.get_region(event[2])
            event_location = MetroidFusionLocation(self.player, event[0], None, region)
            region.locations.append(event_location)
            event_location.place_locked_item(self.create_event(event[3]))

    def connect_entrances(self) -> None:
        self.er_map = randomize_entrances(self, True, self.er_group_mappings).pairings
        for connection in self.er_map:
            source = connection[0].replace(" Destination", "")
            destination = connection[1].replace(" Destination", "")
            self.region_map[source] = destination
            self.region_map[destination] = source
            self.spoiler_region_map[source] = destination
        if self.debug:
            for source, destination in self.spoiler_region_map.items():
                print(f"{source} <-> {destination}")
            from Utils import visualize_regions
            visualize_regions(self.get_region("Menu"), f"fusiondiagram{self.player}.puml")

    def build_early_progression(self):
        starting_inventory = self.options.start_inventory.value | self.options.start_inventory_from_pool.value

        # Starting major upgrades plus start inventory
        major_upgrade_count = self.starting_major_upgrades
        major_upgrade_choices = major_upgrades.copy()
        for item in starting_inventory.keys():
            if item in major_upgrade_choices:
                major_upgrade_choices.remove(item)
        major_upgrade_count = min(major_upgrade_count, len(major_upgrade_choices))
        major_upgrades_to_add = self.random.sample(major_upgrade_choices, k=major_upgrade_count)
        for upgrade in major_upgrades_to_add:
            self.options.start_inventory_from_pool.value[upgrade] = 1
            self.push_precollected(self.create_item(upgrade))

        ponr = self.options.PointOfNoReturnsInLogic
        sphere_0_items = self.starting_location_object.get_sphere_0(ponr).copy()
        if len(sphere_0_items) > 0:
            starting_inventory = self.options.start_inventory.value | self.options.start_inventory_from_pool.value
            sphere_0_item_set = self.random.sample(sphere_0_items, k=self.starting_location_object.sphere_0_item_count)
            for sphere_0_item in sphere_0_item_set:
                if sphere_0_item not in starting_inventory.keys():
                    self.options.start_inventory_from_pool.value[sphere_0_item] = 1
                    self.push_precollected(self.create_item(sphere_0_item))
        if self.options.EarlyProgression != self.options.EarlyProgression.option_none:
            sphere_1_items = self.starting_location_object.get_sphere_1(ponr).copy()
            sphere_1_items.extend(self.starting_location_object.get_additional_items(self.options))
            self.preplaced_item = self.random.choice(sphere_1_items)
            self.multiworld.local_early_items[self.player][self.preplaced_item] = 1

        # Starting energy tanks plus start inventory
        if "Energy Tank" not in starting_inventory.keys():
            if self.options.StartingEnergyTanks > 0:
                self.options.start_inventory_from_pool.value["Energy Tank"] = self.options.StartingEnergyTanks.value
                for i in range(self.options.StartingEnergyTanks.value):
                    self.push_precollected(self.create_item("Energy Tank"))

    def build_metroid_boss_list(self):
        if self.options.InfantMetroidLocations == self.options.InfantMetroidLocations.option_bosses_encouraged:
            boss_count = self.random.randint(3, 5)
            bosses = self.random.sample(boss_locations, k=boss_count)
            chosen_bosses = []
            for boss in bosses:
                chance = self.random.randint(0, 1)
                if chance == 1:
                    chosen_bosses.append(boss)
            return chosen_bosses
        elif self.options.InfantMetroidLocations == self.options.InfantMetroidLocations.option_only_bosses:
            bosses = copy(boss_locations)
            self.random.shuffle(bosses)
            return bosses
        else:
            return []

    def create_items(self):
        itempool = []
        self.build_early_progression()

        item_quantities = deepcopy(default_item_quantities)
        infant_metroids_in_pool = self.options.InfantMetroidsInPool.value
        if self.options.InfantMetroidLocations == self.options.InfantMetroidLocations.option_only_bosses:
            infant_metroids_in_pool = min(infant_metroids_in_pool, len(boss_locations))
        item_quantities["Infant Metroid"] = infant_metroids_in_pool
        item_quantities["Power Bomb Tank"] -= infant_metroids_in_pool
        metroid_bosses = self.build_metroid_boss_list()
        energy_tanks = 0
        max_progressive_energy_tanks = 10
        for item in item_table:
            if item in item_quantities.keys():
                for i in range(item_quantities[item]):
                    itempool.append(item)
            else:
                itempool.append(item)
        for item in map(self.create_item, itempool):
            if item.name == "Energy Tank":
                energy_tanks += 1
                if energy_tanks > max_progressive_energy_tanks:
                    item.classification = ItemClassification.useful
            if item.name == "Infant Metroid" and len(metroid_bosses) > 0:
                boss_location = metroid_bosses.pop()
                self.get_location(boss_location).place_locked_item(item)
                if self.debug:
                    print(f"Placed Infant Metroid at {boss_location}")
            else:
                self.multiworld.itempool.append(item)

    def set_rules(self):
        for location in all_locations:
            ap_location = self.get_location(location.name)
            location_data = get_location_data_by_name(location.name)
            logic_object = LogicObject(self.player, self.options)
            if self.debug:
                print(f"\n{location.name} requirements:")
            logic_object.requirements, logic_object.energy_tanks = create_logic_rule_for_list(
                location_data.requirements, self.options, self.debug)
            add_rule(ap_location, logic_object.logic_rule)

        infant_metroids_required = self.options.InfantMetroidsRequired.value
        infant_metroids_in_pool = self.options.InfantMetroidsInPool.value
        if self.options.InfantMetroidLocations == self.options.InfantMetroidLocations.option_only_bosses:
            infant_metroids_in_pool = min(infant_metroids_in_pool, len(boss_locations))
        if infant_metroids_required > infant_metroids_in_pool:
            infant_metroids_required = infant_metroids_in_pool


        add_rule(
            self.get_location("Victory"),
            lambda state: state.has("Infant Metroid", self.player, infant_metroids_required)
                          and state.has("Charge Beam", self.player)
                          and state.has("Missile Data", self.player)
                          and state.has("Energy Tank", self.player, 3)
                          and (state.has("Space Jump", self.player) or state.has("Hi-Jump", self.player)))
        if self.options.CombatDifficulty < self.options.CombatDifficulty.option_expert:
            add_rule(
                self.get_location("Victory"),
                lambda state: state.has("Plasma Beam", self.player)
                              and state.has("Varia Suit", self.player)
                              and state.has("Energy Tank", self.player, 6))
        if self.options.CombatDifficulty < self.options.CombatDifficulty.option_advanced:
            add_rule(
                self.get_location("Victory"),
                lambda state: state.has("Wide Beam", self.player)
                              and state.has("Super Missile", self.player)
                              and state.has("Energy Tank", self.player, 10))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def pre_fill(self) -> None:
        pass

    def generate_basic(self):
        pass

    @staticmethod
    def create_palette_rando(seed: int):
        return {
            "Seed": seed % 2**32,
            "Randomize": {
                "Samus": {
                    "HueMin": 0,
                    "HueMax": 360
                },
                "Beams": {
                    "HueMin": 0,
                    "HueMax": 360
                },
                "Enemies": {
                    "HueMin": 0,
                    "HueMax": 360
                },
                "Tilesets": {
                    "HueMin": 0,
                    "HueMax": 360
                }
            },
            "ColorSpace": "Oklab"
        }

    def create_navigation_text(self, hint_text: list[str], required_metroids: int):
        briefing_text_addition_start = ""
        starting_inventory_strings = []
        starting_inventory_items = [item.name for item in self.multiworld.precollected_items[self.player]]
        starting_inventory_counter = {item: starting_inventory_items.count(item) for item in starting_inventory_items}
        if len(starting_inventory_counter) > 0:
            for item, quantity in starting_inventory_counter.items():
                item_string = item
                if quantity > 1:
                    item_string += f" x {quantity}"
                starting_inventory_strings.append(item_string)
        starting_inventory_strings.sort()
        if len(starting_inventory_strings) > 0:
            starting_inventory_string = ", ".join(starting_inventory_strings)
            briefing_text_addition_start = f"Your starting gear is: {starting_inventory_string}. "
        briefing_text_addition_end = ""
        if self.options.EnableHints:
            briefing_text_addition_end = (f"Uplink at [COLOR=2]Navigation Rooms[/COLOR] along the way. "
                                       f"I can scan the station for useful equipment from there.")
        navigation_text = {
            "English": {
                "ShipText": {
                    "InitialText": f"{briefing_text_addition_start}"
                                   f"Your objective is as follows: Find enough [COLOR=3]Infant Metroids[/COLOR] "
                                   f"({required_metroids}) to lure out the SA-X. "
                                   f"Then initiate the station's self-destruct sequence. "
                                   f"{briefing_text_addition_end}"
                                   f"[OBJECTIVE]Good. Move out.",
                    "ConfirmText": "Any objections, Lady?"
                }
            }
        }
        if self.options.EnableHints:
            nav_room_text = {
                    "MainDeckEast": hint_text[0],
                    "MainDeckWest": hint_text[1],
                    "OperationsDeck": hint_text[2],
                    "AuxiliaryPower": hint_text[3],
                    "RestrictedLabs": hint_text[4],
                    "Sector1Entrance": hint_text[5],
                    "Sector2Entrance": hint_text[6],
                    "Sector3Entrance": hint_text[7],
                    "Sector4Entrance": hint_text[8],
                    "Sector5Entrance": hint_text[9],
                    "Sector6Entrance": hint_text[10]
                }
        else:
            nav_room_text = {
                    "MainDeckEast": "No hint data available.",
                    "MainDeckWest": "No hint data available.",
                    "OperationsDeck": "No hint data available.",
                    "AuxiliaryPower": "No hint data available.",
                    "RestrictedLabs": "No hint data available.",
                    "Sector1Entrance": "No hint data available.",
                    "Sector2Entrance": "No hint data available.",
                    "Sector3Entrance": "No hint data available.",
                    "Sector4Entrance": "No hint data available.",
                    "Sector5Entrance": "No hint data available.",
                    "Sector6Entrance": "No hint data available."
                }
        navigation_text["English"]["NavigationTerminals"] = nav_room_text
        return navigation_text

    @staticmethod
    def build_door_dict():
        return [
        {
            "Area": 0,
            "Door": 51,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 57,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 52,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 53,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 54,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 55,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 56,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 58,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 59,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 60,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 61,
            "LockType": "Open"
        },
        {
            "Area": 0,
            "Door": 62,
            "LockType": "Open"
        }
    ]

    def build_starting_location_dict(self) -> dict[str, int]:
        return starting_location_data[self.starting_location]

    @staticmethod
    def build_credits_text() -> list[dict]:
        return [
            {
                "LineType": "White2",
                "Text": "",
                "BlankLines": 2
            },
            {
                "LineType": "Blue",
                "Text": "Archipelago Integration",
                "BlankLines": 1
            },
            {
                "LineType": "White2",
                "Text": "Rosalie",
                "BlankLines": 1
            },
            {
                "LineType": "White2",
                "Text": "CRIT MAGNET",
                "BlankLines": 1
            },
            {
                "LineType": "White2",
                "Text": "JaggerG",
                "BlankLines": 1
            },
            {
                "LineType": "White2",
                "Text": "Palm__",
                "BlankLines": 2
            },
            {
                "LineType": "White1",
                "Text": "And the AP community",
                "BlankLines": 4
            },
        ]

    def build_nav_locks_dict(self):
        if not self.navigation_room_hint_locks:
            return {
                "MainDeckWest": "OPEN",
                "MainDeckEast": "OPEN",
                "OperationsDeck": "OPEN",
                "Sector1Entrance": "OPEN",
                "Sector2Entrance": "OPEN",
                "Sector3Entrance": "OPEN",
                "Sector4Entrance": "OPEN",
                "Sector5Entrance": "OPEN",
                "Sector6Entrance": "OPEN",
                "AuxiliaryPower": "OPEN",
                "RestrictedLabs": "OPEN"
            }
        else:
            return {
                "MainDeckWest": "OPEN",
                "MainDeckEast": "OPEN",
                "OperationsDeck": "OPEN",
                "Sector1Entrance": "BLUE",
                "Sector2Entrance": "BLUE",
                "Sector3Entrance": "GREEN",
                "Sector4Entrance": "GREEN",
                "Sector5Entrance": "YELLOW",
                "Sector6Entrance": "YELLOW",
                "AuxiliaryPower": "OPEN",
                "RestrictedLabs": "OPEN"
            }

    def build_sector_connections(self):
        return {
            "LeftAreas": [
                sector_tube_id_lookups[self.region_map[Sector1TubeLeft.name]],
                sector_tube_id_lookups[self.region_map[Sector2TubeLeft.name]],
                sector_tube_id_lookups[self.region_map[Sector3TubeLeft.name]],
                sector_tube_id_lookups[self.region_map[Sector4TubeLeft.name]],
                sector_tube_id_lookups[self.region_map[Sector5TubeLeft.name]],
                sector_tube_id_lookups[self.region_map[Sector6TubeLeft.name]],
            ],
            "RightAreas": [
                sector_tube_id_lookups[self.region_map[Sector1TubeRight.name]],
                sector_tube_id_lookups[self.region_map[Sector2TubeRight.name]],
                sector_tube_id_lookups[self.region_map[Sector3TubeRight.name]],
                sector_tube_id_lookups[self.region_map[Sector4TubeRight.name]],
                sector_tube_id_lookups[self.region_map[Sector5TubeRight.name]],
                sector_tube_id_lookups[self.region_map[Sector6TubeRight.name]],
            ]
        }

    def build_elevator_connections(self):
        return {
            "ElevatorTops": {
                "OperationsDeckTop": elevator_id_lookups[self.region_map[OperationsDeckElevatorTop.name]],
                "MainHubToSector1": elevator_id_lookups[self.region_map[SectorHubElevator1Top.name]],
                "MainHubToSector2": elevator_id_lookups[self.region_map[SectorHubElevator2Top.name]],
                "MainHubToSector3": elevator_id_lookups[self.region_map[SectorHubElevator3Top.name]],
                "MainHubToSector4": elevator_id_lookups[self.region_map[SectorHubElevator4Top.name]],
                "MainHubToSector5": elevator_id_lookups[self.region_map[SectorHubElevator5Top.name]],
                "MainHubToSector6": elevator_id_lookups[self.region_map[SectorHubElevator6Top.name]],
                "MainHubTop": elevator_id_lookups[self.region_map[SectorHubElevatorTop.name]],
                "HabitationDeckTop": elevator_id_lookups[self.region_map[HabitationDeckElevatorTop.name]],
                "Sector1ToRestrictedLab": elevator_id_lookups[self.region_map[Sector1TourianHubElevatorTop.name]]
            },
            "ElevatorBottoms": {
                "OperationsDeckBottom": elevator_id_lookups[self.region_map[OperationsDeckElevatorBottom.name]],
                "MainHubBottom": elevator_id_lookups[self.region_map[SectorHubElevatorBottom.name]],
                "RestrictedLabToSector1": elevator_id_lookups[self.region_map[Sector6RestrictedZoneElevatorToTourian.name]],
                "HabitationDeckBottom": elevator_id_lookups[self.region_map[HabitationDeckElevatorBottom.name]],
                "Sector1ToMainHub": elevator_id_lookups[self.region_map[Sector1Hub.name]],
                "Sector2ToMainHub": elevator_id_lookups[self.region_map[Sector2Hub.name]],
                "Sector3ToMainHub": elevator_id_lookups[self.region_map[Sector3Hub.name]],
                "Sector4ToMainHub": elevator_id_lookups[self.region_map[Sector4Hub.name]],
                "Sector5ToMainHub": elevator_id_lookups[self.region_map[Sector5Hub.name]],
                "Sector6ToMainHub": elevator_id_lookups[self.region_map[Sector6Hub.name]]
            }
        }

    def build_minimap_edits(self):
        pass
        return {

        }

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write("\nElevator and Tube Mapping:\n")
        origins = [
            "Operations Deck Elevator Top",
            "Habitation Deck Elevator Top",
            "Sector Hub Elevator Top",
            "Sector Hub Elevator 1 Top",
            "Sector Hub Elevator 2 Top",
            "Sector Hub Elevator 3 Top",
            "Sector Hub Elevator 4 Top",
            "Sector Hub Elevator 5 Top",
            "Sector Hub Elevator 6 Top",
            "Sector 1 Tourian Hub Elevator Top",
            "Sector 1 Tube Left",
            "Sector 2 Tube Left",
            "Sector 3 Tube Left",
            "Sector 4 Tube Left",
            "Sector 5 Tube Left",
            "Sector 6 Tube Left"
        ]
        for origin in origins:
            if origin in self.spoiler_region_map.keys():
                spoiler_handle.write(f"--{origin} <-> {self.spoiler_region_map[origin]}\n")

    def build_starting_items_dict(self):
        starting_inventory = [item.name for item in self.multiworld.precollected_items[self.player]]
        energy = 99
        missiles = 0
        power_bombs = 0
        security_levels = [0]
        abilities = []
        for item in starting_inventory:
            if item == "Energy Tank":
                energy += 100
            elif item == "Missile Tank":
                missiles += self.options.MissileTankAmmo.value
            elif item == "Power Bomb Tank":
                power_bombs += self.options.PowerBombTankAmmo.value
            elif item == "Level 1 Keycard":
                security_levels.append(1)
            elif item == "Level 2 Keycard":
                security_levels.append(2)
            elif item == "Level 3 Keycard":
                security_levels.append(3)
            elif item == "Level 4 Keycard":
                security_levels.append(4)
            elif item in major_upgrades:
                if item == "Missile Data":
                    missiles += self.options.MissileDataAmmo.value
                elif item == "Power Bomb Data":
                    power_bombs += self.options.PowerBombDataAmmo.value
                abilities.append(ap_name_to_mars_name[item])
            else:
                logging.warning(f"{item} not supported as a starting item.")


        return {
            "Energy": energy,
            "Abilities": abilities,
            "SecurityLevels": security_levels,
            "DownloadedMaps": [0, 1, 2, 3, 4, 5, 6],
            "Missiles": missiles,
            "PowerBombs": power_bombs
        }

    def generate_output(self, output_directory: str):
        patch_dict = dict()
        patch_dict["SeedHash"] = str(self.multiworld.seed)[:8]
        patch_dict["Locations"] = {"MajorLocations": [], "MinorLocations": []}

        for location in self.get_locations():
            # Victory location isn't real and can't hurt you.
            if location.address is None:
                continue
            location_data = get_location_data_by_name(location.name)
            item_sprite = None
            if location.item.player == self.player:
                item_name = ap_name_to_mars_name[location.item.name]
                if item_name == "None":   # Empty items, when we implement them,
                    item_sprite = "Empty" # have a different sprite name than item name
                else:
                    item_sprite = item_name
                message = None # A None message leaves the default Fusion message.
            else:
                item_name = "None" # Remote items shouldn't give anything ingame.
                message = build_item_message(location.item.name, self.multiworld.player_name[location.item.player])
                # Check if the item is in the list of eligible offworld items we can use a Fusion sprite for.
                game = self.multiworld.worlds[location.item.player].game
                if game in offworld_sprites.keys():
                    if location.item.name in offworld_sprites[game].keys():
                        item_sprite = offworld_sprites[game][location.item.name].value
            if item_sprite is None: # If no offworld sprite, we use one based on classification
                if location.item.classification & ItemClassification.progression:
                    item_sprite = SpriteNames.Anonymous.value
                else:
                    item_sprite = SpriteNames.Empty.value
            # For fun, local visible missile and power bomb tanks have a 1/1024 chance to be shiny.
            if location.item.player == self.player and not location_data.major:
                if item_sprite == SpriteNames.MissileTank.value:
                    chance = self.random.randint(1, 1024)
                    if chance == 1:
                        item_sprite = SpriteNames.ShinyMissileTank.value
                        message = build_shiny_item_message(location.item.name)
                if item_sprite == SpriteNames.PowerBombTank.value:
                    chance = self.random.randint(1, 1024)
                    if chance == 1:
                        item_sprite = SpriteNames.ShinyPowerBombTank.value
                        message = build_shiny_item_message(location.item.name)
            json_data = location_data.to_json(item_name, item_sprite, location.item.classification)
            if message is not None:
                json_data["ItemMessages"] = message
            if location_data.major:
                patch_dict["Locations"]["MajorLocations"].append(json_data)
            else:
                patch_dict["Locations"]["MinorLocations"].append(json_data)

        infant_metroids_required = self.options.InfantMetroidsRequired.value
        if infant_metroids_required > self.options.InfantMetroidsInPool.value:
            infant_metroids_required = self.options.InfantMetroidsInPool.value

        patch_dict["RequiredMetroidCount"] = infant_metroids_required
        patch_dict["PowerBombsWithoutBombs"] = True
        patch_dict["AccessibilityPatches"] = True
        patch_dict["RevealHiddenTiles"] = bool(self.options.RevealHiddenBlocks.value)
        patch_dict["DisableDemos"] = True
        patch_dict["SkipDoorTransitions"] = bool(self.options.FastDoorTransitions.value)
        patch_dict["UnexploredMap"] = True
        patch_dict["RoomNames"] = room_names
        patch_dict["TitleText"] = [{"Text": "         Archipelago", "LineNum": 12}]
        patch_dict["CreditsText"] = self.build_credits_text()

        if self.options.PaletteRandomization:
            patch_dict["Palettes"] = self.create_palette_rando(self.multiworld.seed)
        if self.options.EnableHints:
            if self.hint_text is None:
                self.hint_text, self.hint_pairs = create_hints(self)
            patch_dict["NavigationText"] = self.create_navigation_text(
                self.hint_text,
                infant_metroids_required)
        else:
            patch_dict["NavigationText"] = self.create_navigation_text([], infant_metroids_required)
        if len(self.options.start_inventory.value) > 0 or len(self.options.start_inventory_from_pool.value) > 0:
            patch_dict["StartingItems"] = self.build_starting_items_dict()
        patch_dict["TankIncrements"] = {
            "MissileTank": self.options.MissileTankAmmo.value,
            "PowerBombTank": self.options.PowerBombTankAmmo.value,
            "EnergyTank": 100,
            "MissileData": self.options.MissileDataAmmo.value,
            "PowerBombData": self.options.PowerBombDataAmmo.value
        }

        if self.open_sector_elevators:
            patch_dict["DoorLocks"] = self.build_door_dict()

        patch_dict["StartingLocation"] = self.build_starting_location_dict()

        patch_dict["NavStationLocks"] = self.build_nav_locks_dict()

        patch_dict["GenerationVersion"] = MetroidFusionWorld.version

        patch_dict["SectorShortcuts"] = self.build_sector_connections()
        patch_dict["ElevatorConnections"] = self.build_elevator_connections()

        rom_name_text = f'MFU{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        patch_dict["RomName"] = f'MFU{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        patch_dict["OutputFile"] = f'{self.multiworld.get_out_file_name_base(self.player)}' + '.gba'

        # Our actual patch is just a set of instructions and data for MARS to use.
        patch = MetroidFusionProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("patch_file.json", json.dumps(patch_dict).encode("UTF-8"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def modify_multidata(self, multidata: dict):
        import base64
        rom_name_text = f'MFU{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        rom_name_text = rom_name_text[:20]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        if self.filler_items is None:
            self.filler_items = [item for item in item_table if
                                 item_table[item].classification == ItemClassification.filler]
        return self.random.choice(self.filler_items)

    def fill_slot_data(self) -> Dict[str, Any]:
        hint_data = {}
        if self.options.EnableHints:
            if self.hint_text is None:
                self.hint_text, self.hint_pairs = create_hints(self)
        infant_metroids_required = self.options.InfantMetroidsRequired.value
        if infant_metroids_required > self.options.InfantMetroidsInPool.value:
            infant_metroids_required = self.options.InfantMetroidsInPool.value
        if self.options.EnableHints:
            hint_data = {
                "MainDeckEast": self.get_hint(self.hint_pairs[0]),
                "MainDeckWest": self.get_hint(self.hint_pairs[1]),
                "OperationsDeck": self.get_hint(self.hint_pairs[2]),
                "AuxiliaryPower": self.get_hint(self.hint_pairs[3]),
                "RestrictedLabs": self.get_hint(self.hint_pairs[4]),
                "Sector1Entrance": self.get_hint(self.hint_pairs[5]),
                "Sector2Entrance": self.get_hint(self.hint_pairs[6]),
                "Sector3Entrance": self.get_hint(self.hint_pairs[7]),
                "Sector4Entrance": self.get_hint(self.hint_pairs[8]),
                "Sector5Entrance": self.get_hint(self.hint_pairs[9]),
                "Sector6Entrance": self.get_hint(self.hint_pairs[10])
            }
        return {
            "Hints": hint_data,
            "InfantMetroidsRequired": infant_metroids_required,
            "MissileDataAmmo": self.options.MissileDataAmmo.value,
            "MissileTankAmmo": self.options.MissileTankAmmo.value,
            "PowerBombDataAmmo": self.options.PowerBombDataAmmo.value,
            "PowerBombTankAmmo": self.options.PowerBombTankAmmo.value,
            "PONRsInLogic": self.options.PointOfNoReturnsInLogic.value,
            "ShinesparkDifficulty": self.options.ShinesparkTrickDifficulty.value,
            "WallJumpDifficulty": self.options.WallJumpTrickDifficulty.value,
            "CombatDifficulty": self.options.CombatDifficulty.value,
            "GameMode": self.options.GameMode.value,
            "StartingLocation": self.options.StartingLocation.value,
            "OpenSectorElevators": self.options.OpenSectorElevators.value,
            "SectorTubeShuffle": self.options.SectorTubeShuffle.value,
            "ElevatorShuffle": self.options.ElevatorShuffle.value,
            "DeathLink": self.options.death_link.value,
            "StartInventory": [item.name for item in self.multiworld.precollected_items[self.player]],
            "UTStartingLocation": self.starting_region,
            "UTEntrances": self.er_map
        }

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        if "UTStartingLocation" in slot_data:
            self.origin_region_name = slot_data["UTStartingLocation"]

        if "UTEntrances" in slot_data:
            # Update entrance connections for ER
            entrances = {
                entrance.name: entrance
                for region in self.get_regions()
                for entrance in region.entrances
            }
            for source_exit, target_entrance in slot_data["UTEntrances"]:
                entrances[source_exit].connected_region = entrances[target_entrance].parent_region

    @staticmethod
    def get_hint(pair: HintedPair):
        return {
            "Location": pair.location.address,
            "Player": pair.location.player
        }


class MetroidFusionItem(Item):
    game = "Metroid Fusion"

