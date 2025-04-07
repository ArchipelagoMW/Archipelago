"""
Archipelago init file for The Witness
"""
import dataclasses
from logging import error, warning
from typing import Any, Dict, List, Optional, cast

from BaseClasses import CollectionState, Entrance, Location, LocationProgressType, Region, Tutorial

from Options import OptionError, PerGameCommonOptions, Toggle
from worlds.AutoWorld import WebWorld, World

from .data import static_items as static_witness_items
from .data import static_locations as static_witness_locations
from .data import static_logic as static_witness_logic
from .data.item_definition_classes import DoorItemDefinition, ItemData
from .data.utils import cast_not_none, get_audio_logs
from .hints import CompactHintData, create_all_hints, make_compact_hint_data, make_laser_hints
from .locations import WitnessPlayerLocations
from .options import TheWitnessOptions, witness_option_groups
from .player_items import WitnessItem, WitnessPlayerItems
from .player_logic import WitnessPlayerLogic
from .presets import witness_option_presets
from .regions import WitnessPlayerRegions
from .rules import set_rules


class WitnessWebWorld(WebWorld):
    theme = "jungle"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing The Witness with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["NewSoupVi", "Jarno"]
    )]

    options_presets = witness_option_presets
    option_groups = witness_option_groups


class WitnessWorld(World):
    """
    The Witness is an open-world puzzle game with dozens of locations
    to explore and over 500 puzzles. Play the popular puzzle randomizer
    by sigma144, with an added layer of progression randomization!
    """
    game = "The Witness"
    topology_present = False
    web = WitnessWebWorld()

    origin_region_name = "Entry"

    options_dataclass = TheWitnessOptions
    options: TheWitnessOptions

    item_name_to_id = {
        # ITEM_DATA doesn't have any event items in it
        name: cast_not_none(data.ap_code) for name, data in static_witness_items.ITEM_DATA.items()
    }
    location_name_to_id = static_witness_locations.ALL_LOCATIONS_TO_ID
    item_name_groups = static_witness_items.ITEM_GROUPS
    location_name_groups = static_witness_locations.AREA_LOCATION_GROUPS

    required_client_version = (0, 6, 0)

    player_logic: WitnessPlayerLogic
    player_locations: WitnessPlayerLocations
    player_items: WitnessPlayerItems
    player_regions: WitnessPlayerRegions

    log_ids_to_hints: Dict[int, CompactHintData]
    laser_ids_to_hints: Dict[int, CompactHintData]

    items_placed_early: List[str]
    own_itempool: List[WitnessItem]

    panel_hunt_required_count: int

    def _get_slot_data(self) -> Dict[str, Any]:
        return {
            "seed": self.options.puzzle_randomization_seed.value,
            "victory_location": int(self.player_logic.VICTORY_LOCATION, 16),
            "panelhex_to_id": self.player_locations.CHECK_PANELHEX_TO_ID,
            "item_id_to_door_hexes": static_witness_items.get_item_to_door_mappings(),
            "door_items_in_the_pool": self.player_items.get_door_item_ids_in_pool(),
            "doors_that_shouldnt_be_locked": [int(h, 16) for h in self.player_logic.FORBIDDEN_DOORS],
            "symbols_not_in_the_game": self.player_items.get_symbol_ids_not_in_pool(),
            "disabled_entities": [int(h, 16) for h in self.player_logic.COMPLETELY_DISABLED_ENTITIES],
            "hunt_entities": [int(h, 16) for h in self.player_logic.HUNT_ENTITIES],
            "log_ids_to_hints": self.log_ids_to_hints,
            "laser_ids_to_hints": self.laser_ids_to_hints,
            "progressive_item_lists": self.player_items.get_progressive_item_ids_in_pool(),
            "obelisk_side_id_to_EPs": static_witness_logic.OBELISK_SIDE_ID_TO_EP_HEXES,
            "precompleted_puzzles": [int(h, 16) for h in self.player_logic.EXCLUDED_ENTITIES],
            "entity_to_name": static_witness_logic.ENTITY_ID_TO_NAME,
            "panel_hunt_required_absolute": self.panel_hunt_required_count
        }

    def determine_sufficient_progression(self) -> None:
        """
        Determine whether there are enough progression items in this world to consider it "interactive".
        In the case of singleplayer, this just outputs a warning.
        In the case of multiplayer, the requirements are a bit stricter and an Exception is raised.
        """

        # A note on Obelisk Keys:
        # Obelisk Keys are never relevant in singleplayer, because the locations they lock are irrelevant to in-game
        # progress and irrelevant to all victory conditions. Thus, I consider them "fake progression" for singleplayer.
        # However, those locations could obviously contain big items needed for other players, so I consider
        # "Obelisk Keys only" valid for multiworld.

        # A note on Laser Shuffle:
        # In singleplayer, I don't mind "Ice Rod Hunt" type gameplay, so "laser shuffle only" is valid.
        # However, I do not want to allow "Ice Rod Hunt" style gameplay in multiworld, so "laser shuffle only" is
        # not considered interactive enough for multiworld.

        interacts_sufficiently_with_multiworld = (
            self.options.shuffle_symbols
            or self.options.shuffle_doors
            or self.options.obelisk_keys and self.options.shuffle_EPs
        )

        has_locally_relevant_progression = (
            self.options.shuffle_symbols
            or self.options.shuffle_doors
            or self.options.shuffle_lasers
            or self.options.shuffle_boat
            or self.options.early_caves == "add_to_pool" and self.options.victory_condition == "challenge"
        )

        if not has_locally_relevant_progression and self.multiworld.players == 1:
            warning(f"{self.player_name}'s Witness world doesn't have any progression"
                    f" items. Please turn on Symbol Shuffle, Door Shuffle or Laser Shuffle if that doesn't seem right.")
        elif not interacts_sufficiently_with_multiworld and self.multiworld.players > 1:
            raise OptionError(f"{self.player_name}'s Witness world doesn't have enough"
                              f" progression items that can be placed in other players' worlds. Please turn on Symbol"
                              f" Shuffle, Door Shuffle, or Obelisk Keys.")

    def generate_early(self) -> None:
        disabled_locations = self.options.exclude_locations.value

        self.player_logic = WitnessPlayerLogic(
            self, disabled_locations, self.options.start_inventory.value
        )

        self.player_locations: WitnessPlayerLocations = WitnessPlayerLocations(self, self.player_logic)
        self.player_items: WitnessPlayerItems = WitnessPlayerItems(
            self, self.player_logic, self.player_locations
        )
        self.player_regions: WitnessPlayerRegions = WitnessPlayerRegions(self.player_locations, self)

        self.log_ids_to_hints: Dict[int, CompactHintData] = {}
        self.laser_ids_to_hints: Dict[int, CompactHintData] = {}

        self.determine_sufficient_progression()

        for item_name, item_data in self.player_items.item_data.items():
            if item_data.local_only:
                self.options.local_items.value.add(item_name)

        if self.options.victory_condition == "panel_hunt":
            total_panels = self.options.panel_hunt_total
            required_percentage = self.options.panel_hunt_required_percentage
            self.panel_hunt_required_count = round(total_panels * required_percentage / 100)
        else:
            self.panel_hunt_required_count = 0

    def create_regions(self) -> None:
        self.player_regions.create_regions(self, self.player_logic)

        # Set rules early so extra locations can be created based on the results of exploring collection states

        set_rules(self)

        # Start creating items

        self.items_placed_early = []
        self.own_itempool = []

        # Add event items and tie them to event locations (e.g. laser activations).

        event_locations = []

        for event_location in self.player_locations.EVENT_LOCATION_TABLE:
            item_obj = self.create_item(
                self.player_logic.EVENT_ITEM_PAIRS[event_location][0]
            )
            location_obj = self.get_location(event_location)
            location_obj.place_locked_item(item_obj)
            self.own_itempool.append(item_obj)

            event_locations.append(location_obj)

        # Place other locked items

        if self.options.shuffle_dog == "puzzle_skip":
            dog_puzzle_skip = self.create_item("Puzzle Skip")
            self.get_location("Town Pet the Dog").place_locked_item(dog_puzzle_skip)

            self.own_itempool.append(dog_puzzle_skip)
            self.items_placed_early.append("Puzzle Skip")

        if self.options.early_symbol_item:
            # Pick an early item to place on the tutorial gate.
            early_items = [
                item for item in self.player_items.get_early_items() if item in self.player_items.get_mandatory_items()
            ]
            if early_items:
                random_early_item = self.random.choice(early_items)
                mode = self.options.puzzle_randomization
                if mode == "sigma_expert" or mode == "umbra_variety" or self.options.victory_condition == "panel_hunt":
                    # In Expert and Variety, only tag the item as early, rather than forcing it onto the gate.
                    # Same with panel hunt, since the Tutorial Gate Open panel is used for something else
                    self.multiworld.local_early_items[self.player][random_early_item] = 1
                else:
                    # Force the item onto the tutorial gate check and remove it from our random pool.
                    gate_item = self.create_item(random_early_item)
                    self.get_location("Tutorial Gate Open").place_locked_item(gate_item)
                    self.own_itempool.append(gate_item)
                    self.items_placed_early.append(random_early_item)

        # There are some really restrictive options in The Witness.
        # They are rarely played, but when they are, we add some extra sphere 1 locations.
        # This is done both to prevent generation failures, but also to make the early game less linear.
        # Only sweeps for events because having this behavior be random based on Tutorial Gate would be strange.

        state = CollectionState(self.multiworld)
        state.sweep_for_advancements(locations=event_locations)

        num_early_locs = sum(
            1 for loc in self.multiworld.get_reachable_locations(state, self.player)
            if loc.address and not loc.item
        )

        # Adjust the needed size for sphere 1 based on how restrictive the options are in terms of items

        needed_size = 2
        needed_size += self.options.puzzle_randomization == "sigma_expert"
        needed_size += self.options.shuffle_symbols
        needed_size += self.options.shuffle_doors > 0

        # Then, add checks in order until the required amount of sphere 1 checks is met.

        extra_checks = [
            ("Tutorial First Hallway Room", "Tutorial First Hallway Bend"),
            ("Tutorial First Hallway", "Tutorial First Hallway Straight"),
            ("Desert Outside", "Desert Surface 1"),
            ("Desert Outside", "Desert Surface 2"),
        ]

        for i in range(num_early_locs, needed_size):
            if not extra_checks:
                break

            region, loc = extra_checks.pop(0)
            self.player_locations.add_location_late(loc)
            self.get_region(region).add_locations({loc: self.location_name_to_id[loc]})

            warning(
                f"""Location "{loc}" had to be added to {self.player_name}'s world
                due to insufficient sphere 1 size."""
            )

    def create_items(self) -> None:
        # Determine pool size.
        pool_size = len(self.player_locations.CHECK_LOCATION_TABLE) - len(self.player_locations.EVENT_LOCATION_TABLE)

        # Fill mandatory items and remove precollected and/or starting items from the pool.
        item_pool = self.player_items.get_mandatory_items()

        # Remove one copy of each item that was placed early
        for already_placed in self.items_placed_early:
            pool_size -= 1

            if already_placed not in item_pool:
                continue

            if item_pool[already_placed] == 1:
                item_pool.pop(already_placed)
            else:
                item_pool[already_placed] -= 1

        for precollected_item_name in [item.name for item in self.multiworld.precollected_items[self.player]]:
            if precollected_item_name in item_pool:
                if item_pool[precollected_item_name] == 1:
                    item_pool.pop(precollected_item_name)
                else:
                    item_pool[precollected_item_name] -= 1

        for inventory_item_name in self.player_logic.STARTING_INVENTORY:
            if inventory_item_name in item_pool:
                if item_pool[inventory_item_name] == 1:
                    item_pool.pop(inventory_item_name)
                else:
                    item_pool[inventory_item_name] -= 1
            self.multiworld.push_precollected(self.create_item(inventory_item_name))

        if len(item_pool) > pool_size:
            error(f"{self.player_name}'s Witness world has too few locations ({pool_size})"
                  f" to place its necessary items ({len(item_pool)}).")
            return

        remaining_item_slots = pool_size - sum(item_pool.values())

        # Add puzzle skips.
        num_puzzle_skips = self.options.puzzle_skip_amount.value

        if num_puzzle_skips > remaining_item_slots:
            warning(f"{self.player_name}'s Witness world has insufficient locations"
                    f" to place all requested puzzle skips.")
            num_puzzle_skips = remaining_item_slots
        item_pool["Puzzle Skip"] = num_puzzle_skips
        remaining_item_slots -= num_puzzle_skips

        # Add junk items.
        if remaining_item_slots > 0:
            item_pool.update(self.player_items.get_filler_items(remaining_item_slots))

        # Generate the actual items.
        for item_name, quantity in sorted(item_pool.items()):
            new_items = [self.create_item(item_name) for _ in range(0, quantity)]

            self.own_itempool += new_items
            self.multiworld.itempool += new_items

    def fill_slot_data(self) -> Dict[str, Any]:
        already_hinted_locations = set()

        # Laser hints

        if self.options.laser_hints:
            laser_hints = make_laser_hints(self, sorted(static_witness_items.ITEM_GROUPS["Lasers"]))

            for item_name, hint in laser_hints.items():
                item_def = cast(DoorItemDefinition, static_witness_logic.ALL_ITEMS[item_name])
                self.laser_ids_to_hints[int(item_def.panel_id_hexes[0], 16)] = make_compact_hint_data(hint, self.player)
                already_hinted_locations.add(cast_not_none(hint.location))

        # Audio Log Hints

        hint_amount = self.options.hint_amount.value
        audio_logs = get_audio_logs().copy()

        if hint_amount:
            area_hints = round(self.options.area_hint_percentage / 100 * hint_amount)

            generated_hints = create_all_hints(self, hint_amount, area_hints, already_hinted_locations)

            self.random.shuffle(audio_logs)

            duplicates = min(3, len(audio_logs) // hint_amount)

            for hint in generated_hints:
                compact_hint_data = make_compact_hint_data(hint, self.player)

                for _ in range(0, duplicates):
                    audio_log = audio_logs.pop()
                    self.log_ids_to_hints[int(audio_log, 16)] = compact_hint_data

        # Client will generate joke hints for these.
        self.log_ids_to_hints.update({int(audio_log, 16): ("", -1, -1) for audio_log in audio_logs})

        # Options for the client & auto-tracker

        slot_data = self._get_slot_data()

        for option_name in (attr.name for attr in dataclasses.fields(TheWitnessOptions)
                            if attr not in dataclasses.fields(PerGameCommonOptions)):
            option = getattr(self.options, option_name)
            slot_data[option_name] = bool(option.value) if isinstance(option, Toggle) else option.value

        return slot_data

    def create_item(self, item_name: str) -> WitnessItem:
        # If the player's plando options are malformed, the item_name parameter could be a dictionary containing the
        #   name of the item, rather than the item itself. This is a workaround to prevent a crash.
        if isinstance(item_name, dict):
            item_name = next(iter(item_name))

        # Easter Egg events with arbitrary sizes
        if item_name.startswith("+") and "Easter Egg" in item_name:
            return WitnessItem.make_egg_event(item_name, self.player)

        # this conditional is purely for unit tests, which need to be able to create an item before generate_early
        item_data: ItemData
        if hasattr(self, "player_items") and self.player_items and item_name in self.player_items.item_data:
            item_data = self.player_items.item_data[item_name]
        else:
            item_data = static_witness_items.ITEM_DATA[item_name]

        return WitnessItem(item_name, item_data.classification, item_data.ap_code, player=self.player)

    def collect(self, state: "CollectionState", item: WitnessItem) -> bool:
        changed = super().collect(state, item)
        if changed and item.eggs:
            state.prog_items[self.player]["Egg"] += item.eggs
        return changed

    def remove(self, state: "CollectionState", item: WitnessItem) -> bool:
        changed = super().remove(state, item)
        if changed and item.eggs:
            state.prog_items[self.player]["Egg"] -= item.eggs
        return changed

    def get_filler_item_name(self) -> str:
        return "Speed Boost"


class WitnessLocation(Location):
    """
    Archipelago Location for The Witness
    """
    game: str = "The Witness"

    def __init__(self, player: int, name: str, address: Optional[int], parent: Region) -> None:
        super().__init__(player, name, address, parent)


def create_region(world: WitnessWorld, name: str, player_locations: WitnessPlayerLocations,
                  region_locations: Optional[List[str]] = None, exits: Optional[List[str]] = None) -> Region:
    """
    Create an Archipelago Region for The Witness
    """

    ret = Region(name, world.player, world.multiworld)
    if region_locations:
        for location in region_locations:
            loc_id = player_locations.CHECK_LOCATION_TABLE[location]

            location_obj = WitnessLocation(world.player, location, loc_id, ret)

            if location in static_witness_logic.ENTITIES_BY_NAME:
                entity_hex = static_witness_logic.ENTITIES_BY_NAME[location]["entity_hex"]

                if entity_hex in world.player_logic.EXCLUDED_ENTITIES:
                    location_obj.progress_type = LocationProgressType.EXCLUDED

            ret.locations.append(location_obj)
    if exits:
        for single_exit in exits:
            ret.exits.append(Entrance(world.player, single_exit, ret))

    return ret
