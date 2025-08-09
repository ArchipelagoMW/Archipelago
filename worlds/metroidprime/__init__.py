from collections import defaultdict
import typing
from Options import NumericOption
from typing import Any, Dict, List, Optional, TextIO, Union, cast
from logging import info

from .Logic import Logic
from .data.RoomNames import RoomName
from .data.PhazonMines import PhazonMinesAreaData
from .data.PhendranaDrifts import PhendranaDriftsAreaData
from .data.MagmoorCaverns import MagmoorCavernsAreaData
from .data.ChozoRuins import ChozoRuinsAreaData
from .data.TallonOverworld import TallonOverworldAreaData
from .data.Tricks import Tricks
from .BlastShieldRando import (
    WorldBlastShieldMapping,
    apply_blast_shield_mapping,
    get_world_blast_shield_mapping,
)
from .data.RoomData import AreaData
from .data.AreaNames import MetroidPrimeArea
from .DoorRando import (
    WorldDoorColorMapping,
    get_world_door_mapping,
    remap_doors_to_power_beam_if_necessary,
)

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess  # type: ignore
import settings
from worlds.AutoWorld import World, WebWorld
from .data.Transports import (
    ELEVATOR_USEFUL_NAMES,
    DEFAULT_ELEVATOR_MAPPINGS,
    get_random_elevator_mapping,
)
from .Config import make_config
from .Regions import create_regions
from .Locations import EVERY_LOCATION_TABLE
from .ItemPool import generate_item_pool, generate_base_start_inventory
from .PrimeOptions import (
    BlastShieldRandomization,
    DoorColorRandomization,
    MetroidPrimeOptions,
    PRIME_OPTION_GROUPS,
)
from .Items import (
    MetroidPrimeEvent,
    MetroidPrimeItem,
    SuitUpgrade,
    ARTIFACT_TABLE,
    ITEM_TABLE,
)
from .data.StartRoomData import (
    StartRoomData,
    init_starting_beam,
    init_starting_loadout,
    init_starting_room_data,
)
from .Container import MetroidPrimeContainer
from BaseClasses import MultiWorld, Tutorial, ItemClassification


class MultiworldWithPassthrough(MultiWorld):
    re_gen_passthrough: Dict[str, Dict[str, Any]] = {}


def run_client(*args: Any):
    from .MetroidPrimeClient import launch

    launch_subprocess(launch, name="MetroidPrimeClient")


components.append(
    Component(
        "Metroid Prime Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apmp1"),
    )
)


class MetroidPrimeSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Metroid Prime ISO"""

        description = "Metroid Prime GC ISO file"
        copy_to = "Metroid_Prime.iso"

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
        Set it to true to have the operating system default program open the iso
        Alternatively, set it to a path to a program to open the .iso file with (like Dolplhin)
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = False


class MetroidPrimeWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Metroid Prime for Archipelago",
            "English",
            "setup_en.md",
            "setup/en",
            ["hesto2", "Electro15"],
        )
    ]
    option_groups = PRIME_OPTION_GROUPS


class MetroidPrimeWorld(World):
    """
    Metroid Prime is a first-person action-adventure game originally for the Gamecube. Play as
    the bounty hunter Samus Aran as she traverses the planet Tallon IV and uncovers the plans
    of the Space Pirates.
    """

    game = "Metroid Prime"
    web = MetroidPrimeWeb()
    required_client_version = (0, 5, 0)
    options_dataclass = MetroidPrimeOptions
    options: MetroidPrimeOptions  # type: ignore
    topology_present = True
    item_name_to_id = {name: data.code for name, data in ITEM_TABLE.items()}
    location_name_to_id = EVERY_LOCATION_TABLE
    settings: MetroidPrimeSettings  # type: ignore
    item_name_groups = {"Artifacts": set(ARTIFACT_TABLE.keys())}
    starting_room_data: StartRoomData
    prefilled_item_map: Dict[str, str] = {}  # Dict of location name to item name
    elevator_mapping: Dict[str, Dict[str, str]] = defaultdict(dict)
    door_color_mapping: Optional[WorldDoorColorMapping] = None
    blast_shield_mapping: Optional[WorldBlastShieldMapping] = None
    game_region_data: Dict[MetroidPrimeArea, AreaData]
    has_generated_bomb_doors: bool = False
    starting_room_name: Optional[str] = None
    starting_beam: Optional[str] = None
    disable_starting_room_bk_prevention: bool = (
        False  # Used in certain scenarios to enable more flexibility with starting loadouts
    )
    logic: Logic
    tricks: Tricks

    def get_filler_item_name(self) -> str:
        return SuitUpgrade.Missile_Expansion.value

    def init_tracker_data(self):
        # Universal tracker stuff, shouldn't do anything in standard gen
        tracker_multiworld = cast(MultiworldWithPassthrough, self.multiworld)
        if self.game in tracker_multiworld.re_gen_passthrough:
            info("Setting data for tracker")
            passthrough = tracker_multiworld.re_gen_passthrough[self.game]
            # Need to re initialize the game region data
            self.game_region_data = {
                MetroidPrimeArea.Tallon_Overworld: TallonOverworldAreaData(self),
                MetroidPrimeArea.Chozo_Ruins: ChozoRuinsAreaData(self),
                MetroidPrimeArea.Magmoor_Caverns: MagmoorCavernsAreaData(self),
                MetroidPrimeArea.Phendrana_Drifts: PhendranaDriftsAreaData(self),
                MetroidPrimeArea.Phazon_Mines: PhazonMinesAreaData(self),
            }

            for key, value in passthrough.items():
                option = getattr(self.options, key, None)
                if option is not None:
                    # These get interpreted as lists but the tracker expects them to be sets
                    if key in [
                        "non_local_items",
                        "local_items",
                        "local_early_items",
                        "priority_locations",
                        "exclude_locations",
                        "elevator_mapping",
                        "door_color_mapping",
                    ]:
                        option.value = set(value)
                    else:
                        option.value = value

                if key == "elevator_mapping":
                    self.elevator_mapping = value

                if key == "door_color_mapping":
                    self.door_color_mapping = WorldDoorColorMapping.from_option_value(
                        value
                    )
                if key == "blast_shield_mapping":
                    self.blast_shield_mapping = (
                        WorldBlastShieldMapping.from_option_value(value)
                    )
                if key == "starting_room_name":
                    self.starting_room_name = value
                if key == "starting_beam":
                    self.starting_beam = value

    def init_world_data(self) -> None:
        self.logic = Logic(self)
        self.tricks = Tricks(self)
        self.game_region_data = {
            MetroidPrimeArea.Tallon_Overworld: TallonOverworldAreaData(self),
            MetroidPrimeArea.Chozo_Ruins: ChozoRuinsAreaData(self),
            MetroidPrimeArea.Magmoor_Caverns: MagmoorCavernsAreaData(self),
            MetroidPrimeArea.Phendrana_Drifts: PhendranaDriftsAreaData(self),
            MetroidPrimeArea.Phazon_Mines: PhazonMinesAreaData(self),
        }

    def generate_early(self) -> None:
        self.init_world_data()
        if hasattr(self.multiworld, "re_gen_passthrough"):
            self.init_tracker_data()

        # Fix scan options, if necessary
        if self.options.shuffle_scan_visor:
            self.options.pre_scan_elevators.value = True

        # Select Start Room
        init_starting_room_data(self)

        # Randomize Door Colors
        if (
            self.options.door_color_randomization != DoorColorRandomization.option_none
            and not self.door_color_mapping
        ):
            self.door_color_mapping = get_world_door_mapping(self)

        init_starting_beam(self)

        # Reconcile starting beam with door color mapping, if applicable
        remap_doors_to_power_beam_if_necessary(self)

        # Set starting loadout
        init_starting_loadout(self)

        # Randomize Blast Shields
        if (
            self.options.blast_shield_randomization.value
            != BlastShieldRandomization.option_none
            or self.options.locked_door_count > 0
        ) and not self.blast_shield_mapping:
            self.blast_shield_mapping = get_world_blast_shield_mapping(self)

        if self.blast_shield_mapping:
            apply_blast_shield_mapping(self)

        # Randomize Elevators
        if self.options.elevator_randomization:
            if not len(self.elevator_mapping):
                self.elevator_mapping = get_random_elevator_mapping(self)
        else:
            self.elevator_mapping = DEFAULT_ELEVATOR_MAPPINGS

        # Init starting inventory
        starting_items = generate_base_start_inventory(self)
        option_filled_items = {
            *self.options.start_inventory.value.keys(),
            *self.options.start_inventory_from_pool.value.keys(),
        }

        for item in starting_items:
            if item in option_filled_items:
                continue
            self.multiworld.push_precollected(
                self.create_item(item, ItemClassification.progression)
            )
        # Select random suit colors if applicable
        if self.options.randomize_suit_colors:
            self.select_random_suit_color()

    def create_regions(self) -> None:
        boss_selection = self.options.final_bosses.value
        create_regions(self, boss_selection)

    def create_event(self, event: str):
        return MetroidPrimeEvent(
            event, ItemClassification.progression, None, self.player
        )

    def create_item(
        self, name: str, override: Optional[ItemClassification] = None
    ) -> "MetroidPrimeItem":
        item_data = ITEM_TABLE[name]

        if hasattr(self.multiworld, "generation_is_fake"):
            # All items should be progression for the Universal Tracker
            override = ItemClassification.progression
        if override:
            return MetroidPrimeItem(name, override, item_data.code, self.player)
        return MetroidPrimeItem(
            name, item_data.classification, item_data.code, self.player
        )

    def create_items(self) -> None:
        precollected_item_names = {
            item.name for item in self.multiworld.precollected_items[self.player]
        }
        new_map: Dict[str, str] = {}

        for location, item in self.prefilled_item_map.items():
            if item not in precollected_item_names:
                # Prefilled items affect what goes into the item pool.
                # If we already have collected something, we won't need to prefill it
                new_map[location] = item

        self.prefilled_item_map = new_map

        item_pool = generate_item_pool(self)
        self.multiworld.itempool += item_pool

        for location_name, item_name in self.prefilled_item_map.items():
            location = self.get_location(location_name)
            item = self.create_item(item_name, ItemClassification.progression)
            location.place_locked_item(item)

    def post_fill(self) -> None:
        if self.options.artifact_hints:
            start_hints: typing.Set[str] = self.options.start_hints.value
            for i in ARTIFACT_TABLE:
                start_hints.add(i)

    def select_random_suit_color(self) -> None:
        options: List[NumericOption] = [
            self.options.power_suit_color,
            self.options.varia_suit_color,
            self.options.gravity_suit_color,
            self.options.phazon_suit_color,
        ]

        # Select a random valid suit color index
        for option in options:
            if option.value == 0:
                option.value = self.random.randint(1, 35) * 10

    def generate_output(self, output_directory: str) -> None:
        import json

        configjson = make_config(self)
        configjsons = json.dumps(configjson)

        # DEBUG
        # with open("test_config.json", "w") as f:
        #     f.write(configjsons)

        options_dict: Dict[str, Union[int, str]] = {
            "progressive_beam_upgrades": self.options.progressive_beam_upgrades.value,
            "player_name": self.player_name,
        }

        options_json = json.dumps(options_dict)

        outfile_name = self.multiworld.get_out_file_name_base(self.player)
        apmp1 = MetroidPrimeContainer(
            configjsons,
            options_json,
            outfile_name,
            output_directory,
            player=self.player,
            player_name=self.player_name,
        )
        apmp1.write()

    def fill_slot_data(self) -> Dict[str, Any]:
        exclude_options = {
            "fusion_suit",
            "as_dict",
            "artifact_hints",
            "staggered_suit_damage",
            "start_hints",
        }

        non_cosmetic_options = [
            o
            for o in type(self.options).type_hints.keys()
            if "suit_color" not in o and o not in exclude_options
        ]
        slot_data: Dict[str, Any] = self.options.as_dict(*non_cosmetic_options)
        slot_data["elevator_mapping"] = dict(self.elevator_mapping)
        if self.door_color_mapping:
            slot_data["door_color_mapping"] = self.door_color_mapping.to_option_value()
        if self.blast_shield_mapping:
            slot_data["blast_shield_mapping"] = (
                self.blast_shield_mapping.to_option_value()
            )
        if self.starting_room_name:
            slot_data["starting_room_name"] = self.starting_room_name
        if self.starting_beam:
            slot_data["starting_beam"] = self.starting_beam

        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        info("Regenerating world for tracker")
        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO):
        player_name = self.player_name

        spoiler_handle.write(
            f"Starting Room({player_name}): {self.starting_room_name}\n"
        )

        if self.options.randomize_starting_beam:
            spoiler_handle.write(
                f"Starting Beam({player_name}): {self.starting_beam}\n"
            )

        if self.options.elevator_randomization:
            spoiler_handle.write(f"\n\nElevator Mapping({player_name}):\n")
            for area, elevator_mapping in self.elevator_mapping.items():
                spoiler_handle.write(f"{area}:\n")
                for source, target in elevator_mapping.items():
                    spoiler_handle.write(
                        f"    {ELEVATOR_USEFUL_NAMES[source]} -> {ELEVATOR_USEFUL_NAMES[target]}\n"
                    )

        if (self.options.door_color_randomization == DoorColorRandomization.option_regional):
            assert self.door_color_mapping is not None
            spoiler_handle.write(f"\n\nDoor Color Mapping({player_name}):\n")

            for area, door_color_mapping in self.door_color_mapping.items():
                spoiler_handle.write(f"{area}:\n")
                for door, color in door_color_mapping.type_mapping.items():
                    spoiler_handle.write(f"    {door} -> {color}\n")

        elif (self.options.door_color_randomization == DoorColorRandomization.option_global):
            assert self.door_color_mapping is not None
            spoiler_handle.write(f"\n\nDoor Color Mapping({player_name}):\n")
            for door, color in self.door_color_mapping[MetroidPrimeArea.Tallon_Overworld.value].type_mapping.items():
                spoiler_handle.write(f"    {door} -> {color}\n")

        if (
            self.options.blast_shield_randomization.value
            != BlastShieldRandomization.option_none
            or self.options.locked_door_count > 0
        ):
            assert self.blast_shield_mapping is not None
            spoiler_handle.write(f"\n\nBlast Shield Mapping({player_name}):\n")
            written_mappings: List[List[str]] = []

            for area, blast_shield_mapping in self.blast_shield_mapping.items():
                spoiler_handle.write(f"{area}:\n")
                if len(blast_shield_mapping.type_mapping) == 0:
                    spoiler_handle.write(f"    None\n")
                    continue
                for room, doors in blast_shield_mapping.type_mapping.items():
                    for door in doors.keys():
                        source_room = self.game_region_data[MetroidPrimeArea(area)].rooms[RoomName(room)]
                        # Use the door_data blast shield since it may have been overridden by the door on the other side
                        door_data = source_room.doors[door]

                        assert door_data.default_destination is not None
                        assert door_data.blast_shield is not None

                        destination = door_data.default_destination.value

                        # Don't double write mappings since each door is paired
                        if [destination, room] in written_mappings:
                            continue

                        spoiler_handle.write(f"    {room} <--> {destination}: {door_data.blast_shield.value}\n")
                        written_mappings.append([room, destination])
