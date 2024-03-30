"""
Archipelago init file for The Witness
"""
import dataclasses

from typing import Dict, Optional, cast
from BaseClasses import Region, Location, MultiWorld, Item, Entrance, Tutorial, CollectionState
from Options import PerGameCommonOptions, Toggle
from .presets import witness_option_presets
from worlds.AutoWorld import World, WebWorld
from .player_logic import WitnessPlayerLogic
from .static_logic import StaticWitnessLogic, ItemCategory, DoorItemDefinition
from .hints import get_always_hint_locations, get_always_hint_items, get_priority_hint_locations, \
    get_priority_hint_items, make_always_and_priority_hints, generate_joke_hints, make_area_hints, get_hintable_areas, \
    make_extra_location_hints, create_all_hints, make_laser_hints, make_compact_hint_data, CompactItemData
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .items import WitnessItem, StaticWitnessItems, WitnessPlayerItems, ItemData
from .regions import WitnessRegions
from .rules import set_rules
from .options import TheWitnessOptions
from .utils import get_audio_logs, get_laser_shuffle
from logging import warning, error


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


class WitnessWorld(World):
    """
    The Witness is an open-world puzzle game with dozens of locations
    to explore and over 500 puzzles. Play the popular puzzle randomizer
    by sigma144, with an added layer of progression randomization!
    """
    game = "The Witness"
    topology_present = False
    web = WitnessWebWorld()

    options_dataclass = TheWitnessOptions
    options: TheWitnessOptions

    item_name_to_id = {
        name: data.ap_code for name, data in StaticWitnessItems.item_data.items()
    }
    location_name_to_id = StaticWitnessLocations.ALL_LOCATIONS_TO_ID
    item_name_groups = StaticWitnessItems.item_groups
    location_name_groups = StaticWitnessLocations.AREA_LOCATION_GROUPS

    required_client_version = (0, 4, 5)

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        self.player_logic = None
        self.locat = None
        self.items = None
        self.regio = None

        self.log_ids_to_hints: Dict[int, CompactItemData] = dict()
        self.laser_ids_to_hints: Dict[int, CompactItemData] = dict()

        self.items_placed_early = []
        self.own_itempool = []

    def _get_slot_data(self):
        return {
            'seed': self.random.randrange(0, 1000000),
            'victory_location': int(self.player_logic.VICTORY_LOCATION, 16),
            'panelhex_to_id': self.locat.CHECK_PANELHEX_TO_ID,
            'item_id_to_door_hexes': StaticWitnessItems.get_item_to_door_mappings(),
            'door_hexes_in_the_pool': self.items.get_door_ids_in_pool(),
            'symbols_not_in_the_game': self.items.get_symbol_ids_not_in_pool(),
            'disabled_entities': [int(h, 16) for h in self.player_logic.COMPLETELY_DISABLED_ENTITIES],
            'log_ids_to_hints': self.log_ids_to_hints,
            'laser_ids_to_hints': self.laser_ids_to_hints,
            'progressive_item_lists': self.items.get_progressive_item_ids_in_pool(),
            'obelisk_side_id_to_EPs': StaticWitnessLogic.OBELISK_SIDE_ID_TO_EP_HEXES,
            'precompleted_puzzles': [int(h, 16) for h in self.player_logic.EXCLUDED_LOCATIONS],
            'entity_to_name': StaticWitnessLogic.ENTITY_ID_TO_NAME,
        }

    def determine_sufficient_progression(self):
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
            warning(f"{self.multiworld.get_player_name(self.player)}'s Witness world doesn't have any progression"
                    f" items. Please turn on Symbol Shuffle, Door Shuffle or Laser Shuffle if that doesn't seem right.")
        elif not interacts_sufficiently_with_multiworld and self.multiworld.players > 1:
            raise Exception(f"{self.multiworld.get_player_name(self.player)}'s Witness world doesn't have enough"
                            f" progression items that can be placed in other players' worlds. Please turn on Symbol"
                            f" Shuffle, Door Shuffle or Obelisk Keys.")

    def generate_early(self):
        disabled_locations = self.options.exclude_locations.value

        self.player_logic = WitnessPlayerLogic(
            self, disabled_locations, self.options.start_inventory.value
        )

        self.locat: WitnessPlayerLocations = WitnessPlayerLocations(self, self.player_logic)
        self.items: WitnessPlayerItems = WitnessPlayerItems(
            self, self.player_logic, self.locat
        )
        self.regio: WitnessRegions = WitnessRegions(self.locat, self)

        self.log_ids_to_hints = dict()

        self.determine_sufficient_progression()

        if self.options.shuffle_lasers == "local":
            self.options.local_items.value |= self.item_name_groups["Lasers"]

    def create_regions(self):
        self.regio.create_regions(self, self.player_logic)

        # Set rules early so extra locations can be created based on the results of exploring collection states

        set_rules(self)

        # Add event items and tie them to event locations (e.g. laser activations).

        event_locations = []

        for event_location in self.locat.EVENT_LOCATION_TABLE:
            item_obj = self.create_item(
                self.player_logic.EVENT_ITEM_PAIRS[event_location]
            )
            location_obj = self.multiworld.get_location(event_location, self.player)
            location_obj.place_locked_item(item_obj)
            self.own_itempool.append(item_obj)

            event_locations.append(location_obj)

        # Place other locked items
        dog_puzzle_skip = self.create_item("Puzzle Skip")
        self.multiworld.get_location("Town Pet the Dog", self.player).place_locked_item(dog_puzzle_skip)

        self.own_itempool.append(dog_puzzle_skip)

        self.items_placed_early.append("Puzzle Skip")

        # Pick an early item to place on the tutorial gate.
        early_items = [item for item in self.items.get_early_items() if item in self.items.get_mandatory_items()]
        if early_items:
            random_early_item = self.random.choice(early_items)
            if self.options.puzzle_randomization == "sigma_expert":
                # In Expert, only tag the item as early, rather than forcing it onto the gate.
                self.multiworld.local_early_items[self.player][random_early_item] = 1
            else:
                # Force the item onto the tutorial gate check and remove it from our random pool.
                gate_item = self.create_item(random_early_item)
                self.multiworld.get_location("Tutorial Gate Open", self.player).place_locked_item(gate_item)
                self.own_itempool.append(gate_item)
                self.items_placed_early.append(random_early_item)

        # There are some really restrictive settings in The Witness.
        # They are rarely played, but when they are, we add some extra sphere 1 locations.
        # This is done both to prevent generation failures, but also to make the early game less linear.
        # Only sweeps for events because having this behavior be random based on Tutorial Gate would be strange.

        state = CollectionState(self.multiworld)
        state.sweep_for_events(locations=event_locations)

        num_early_locs = sum(1 for loc in self.multiworld.get_reachable_locations(state, self.player) if loc.address)

        # Adjust the needed size for sphere 1 based on how restrictive the settings are in terms of items

        needed_size = 3
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
            self.locat.add_location_late(loc)
            self.multiworld.get_region(region, self.player).add_locations({loc: self.location_name_to_id[loc]})

            player = self.multiworld.get_player_name(self.player)
            
            warning(f"""Location "{loc}" had to be added to {player}'s world due to insufficient sphere 1 size.""")

    def create_items(self):
        # Determine pool size.
        pool_size: int = len(self.locat.CHECK_LOCATION_TABLE) - len(self.locat.EVENT_LOCATION_TABLE)

        # Fill mandatory items and remove precollected and/or starting items from the pool.
        item_pool: Dict[str, int] = self.items.get_mandatory_items()

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
            error(f"{self.multiworld.get_player_name(self.player)}'s Witness world has too few locations ({pool_size})"
                  f" to place its necessary items ({len(item_pool)}).")
            return

        remaining_item_slots = pool_size - sum(item_pool.values())

        # Add puzzle skips.
        num_puzzle_skips = self.options.puzzle_skip_amount

        if num_puzzle_skips > remaining_item_slots:
            warning(f"{self.multiworld.get_player_name(self.player)}'s Witness world has insufficient locations"
                    f" to place all requested puzzle skips.")
            num_puzzle_skips = remaining_item_slots
        item_pool["Puzzle Skip"] = num_puzzle_skips
        remaining_item_slots -= num_puzzle_skips

        # Add junk items.
        if remaining_item_slots > 0:
            item_pool.update(self.items.get_filler_items(remaining_item_slots))

        # Generate the actual items.
        for item_name, quantity in sorted(item_pool.items()):
            new_items = [self.create_item(item_name) for _ in range(0, quantity)]

            self.own_itempool += new_items
            self.multiworld.itempool += new_items
            if self.items.item_data[item_name].local_only:
                self.options.local_items.value.add(item_name)

    def fill_slot_data(self) -> dict:
        already_hinted_locations = set()

        # Laser hints

        if self.options.laser_hints:
            laser_hints = make_laser_hints(self, StaticWitnessItems.item_groups["Lasers"])

            for item_name, hint in laser_hints.items():
                item_def = cast(DoorItemDefinition, StaticWitnessLogic.all_items[item_name])
                self.laser_ids_to_hints[int(item_def.panel_id_hexes[0], 16)] = make_compact_hint_data(hint, self.player)
                already_hinted_locations.add(hint.location)

        # Audio Log Hints

        hint_amount = self.options.hint_amount.value

        credits_hint = (
            "This Randomizer is brought to you by\n"
            "NewSoupVi, Jarno, blastron,\n"
            "jbzdarkid, sigma144, IHNN, oddGarrett, Exempt-Medic.", -1, -1
        )

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

        if audio_logs:
            audio_log = audio_logs.pop()
            self.log_ids_to_hints[int(audio_log, 16)] = credits_hint

        joke_hints = generate_joke_hints(self, len(audio_logs))

        while audio_logs:
            audio_log = audio_logs.pop()
            self.log_ids_to_hints[int(audio_log, 16)] = joke_hints.pop()

        # Options for the client & auto-tracker

        slot_data = self._get_slot_data()

        for option_name in (attr.name for attr in dataclasses.fields(TheWitnessOptions)
                            if attr not in dataclasses.fields(PerGameCommonOptions)):
            option = getattr(self.options, option_name)
            slot_data[option_name] = bool(option.value) if isinstance(option, Toggle) else option.value

        return slot_data

    def create_item(self, item_name: str) -> Item:
        # If the player's plando options are malformed, the item_name parameter could be a dictionary containing the
        #   name of the item, rather than the item itself. This is a workaround to prevent a crash.
        if type(item_name) is dict:
            item_name = list(item_name.keys())[0]

        # this conditional is purely for unit tests, which need to be able to create an item before generate_early
        item_data: ItemData
        if hasattr(self, 'items') and self.items and item_name in self.items.item_data:
            item_data = self.items.item_data[item_name]
        else:
            item_data = StaticWitnessItems.item_data[item_name]

        return WitnessItem(item_name, item_data.classification, item_data.ap_code, player=self.player)

    def get_filler_item_name(self) -> str:
        return "Speed Boost"


class WitnessLocation(Location):
    """
    Archipelago Location for The Witness
    """
    game: str = "The Witness"
    entity_hex: int = -1

    def __init__(self, player: int, name: str, address: Optional[int], parent, ch_hex: int = -1):
        super().__init__(player, name, address, parent)
        self.entity_hex = ch_hex


def create_region(world: WitnessWorld, name: str, locat: WitnessPlayerLocations, region_locations=None, exits=None):
    """
    Create an Archipelago Region for The Witness
    """

    ret = Region(name, world.player, world.multiworld)
    if region_locations:
        for location in region_locations:
            loc_id = locat.CHECK_LOCATION_TABLE[location]

            entity_hex = -1
            if location in StaticWitnessLogic.ENTITIES_BY_NAME:
                entity_hex = int(
                    StaticWitnessLogic.ENTITIES_BY_NAME[location]["entity_hex"], 0
                )
            location = WitnessLocation(
                world.player, location, loc_id, ret, entity_hex
            )

            ret.locations.append(location)
    if exits:
        for single_exit in exits:
            ret.exits.append(Entrance(world.player, single_exit, ret))

    return ret
