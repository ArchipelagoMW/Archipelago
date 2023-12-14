"""
Archipelago init file for The Witness
"""
import dataclasses
from typing import Dict, Optional

from BaseClasses import Region, Location, MultiWorld, Item, Entrance, Tutorial, CollectionState
from Options import PerGameCommonOptions, Toggle
from .hints import get_always_hint_locations, get_always_hint_items, get_priority_hint_locations, \
    get_priority_hint_items, make_hints, generate_joke_hints
from worlds.AutoWorld import World, WebWorld
from .player_logic import WitnessPlayerLogic
from .static_logic import StaticWitnessLogic
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .items import WitnessItem, StaticWitnessItems, WitnessPlayerItems, ItemData
from .regions import WitnessRegions
from .rules import set_rules
from .Options import TheWitnessOptions
from .utils import get_audio_logs
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


class WitnessWorld(World):
    """
    The Witness is an open-world puzzle game with dozens of locations
    to explore and over 500 puzzles. Play the popular puzzle randomizer
    by sigma144, with an added layer of progression randomization!
    """
    game = "The Witness"
    topology_present = False
    data_version = 14

    StaticWitnessLogic()
    StaticWitnessLocations()
    StaticWitnessItems()
    web = WitnessWebWorld()

    options_dataclass = TheWitnessOptions
    options: TheWitnessOptions

    item_name_to_id = {
        name: data.ap_code for name, data in StaticWitnessItems.item_data.items()
    }
    location_name_to_id = StaticWitnessLocations.ALL_LOCATIONS_TO_ID
    item_name_groups = StaticWitnessItems.item_groups

    required_client_version = (0, 4, 4)

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        self.player_logic = None
        self.locat = None
        self.items = None
        self.regio = None

        self.log_ids_to_hints = None

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
            'progressive_item_lists': self.items.get_progressive_item_ids_in_pool(),
            'obelisk_side_id_to_EPs': StaticWitnessLogic.OBELISK_SIDE_ID_TO_EP_HEXES,
            'precompleted_puzzles': [int(h, 16) for h in self.player_logic.EXCLUDED_LOCATIONS],
            'entity_to_name': StaticWitnessLogic.ENTITY_ID_TO_NAME,
        }

    def generate_early(self):
        disabled_locations = self.multiworld.exclude_locations[self.player].value

        self.player_logic = WitnessPlayerLogic(
            self, disabled_locations, self.multiworld.start_inventory[self.player].value
        )

        self.locat: WitnessPlayerLocations = WitnessPlayerLocations(self, self.player_logic)
        self.items: WitnessPlayerItems = WitnessPlayerItems(
            self, self.player_logic, self.locat
        )
        self.regio: WitnessRegions = WitnessRegions(self.locat, self)

        self.log_ids_to_hints = dict()

        if not (self.options.shuffle_symbols or self.options.shuffle_doors or self.options.shuffle_lasers):
            if self.multiworld.players == 1:
                warning(f"{self.multiworld.get_player_name(self.player)}'s Witness world doesn't have any progression"
                        f" items. Please turn on Symbol Shuffle, Door Shuffle or Laser Shuffle if that doesn't"
                        f" seem right.")
            else:
                raise Exception(f"{self.multiworld.get_player_name(self.player)}'s Witness world doesn't have any"
                                f" progression items. Please turn on Symbol Shuffle, Door Shuffle or Laser Shuffle.")

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
            random_early_item = self.multiworld.random.choice(early_items)
            if self.options.puzzle_randomization == 1:
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
        needed_size += self.options.puzzle_randomization == 1
        needed_size += self.options.shuffle_symbols
        needed_size += self.options.shuffle_doors > 0

        # Then, add checks in order until the required amount of sphere 1 checks is met.

        extra_checks = [
            ("First Hallway Room", "First Hallway Bend"),
            ("First Hallway", "First Hallway Straight"),
            ("Desert Outside", "Desert Surface 3"),
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
                self.multiworld.local_items[self.player].value.add(item_name)

    def fill_slot_data(self) -> dict:
        hint_amount = self.options.hint_amount.value

        credits_hint = (
            "This Randomizer is brought to you by",
            "NewSoupVi, Jarno, blastron,",
            "jbzdarkid, sigma144, IHNN, oddGarrett, Exempt-Medic.", -1
        )

        audio_logs = get_audio_logs().copy()

        if hint_amount != 0:
            generated_hints = make_hints(self, hint_amount, self.own_itempool)

            self.random.shuffle(audio_logs)

            duplicates = min(3, len(audio_logs) // hint_amount)

            for _ in range(0, hint_amount):
                hint = generated_hints.pop(0)

                for _ in range(0, duplicates):
                    audio_log = audio_logs.pop()
                    self.log_ids_to_hints[int(audio_log, 16)] = hint

        if audio_logs:
            audio_log = audio_logs.pop()
            self.log_ids_to_hints[int(audio_log, 16)] = credits_hint

        joke_hints = generate_joke_hints(self, len(audio_logs))

        while audio_logs:
            audio_log = audio_logs.pop()
            self.log_ids_to_hints[int(audio_log, 16)] = joke_hints.pop()

        # generate hints done

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
