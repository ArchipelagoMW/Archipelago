"""
Archipelago init file for The Witness
"""
from typing import Dict, Optional

from BaseClasses import Region, Location, MultiWorld, Item, Entrance, Tutorial
from .hints import get_always_hint_locations, get_always_hint_items, get_priority_hint_locations, \
    get_priority_hint_items, make_hints, generate_joke_hints
from worlds.AutoWorld import World, WebWorld
from .player_logic import WitnessPlayerLogic
from .static_logic import StaticWitnessLogic
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .items import WitnessItem, StaticWitnessItems, WitnessPlayerItems, ItemData
from .rules import set_rules
from .regions import WitnessRegions
from .Options import is_option_enabled, the_witness_options, get_option_value
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
    data_version = 13

    StaticWitnessLogic()
    StaticWitnessLocations()
    StaticWitnessItems()
    web = WitnessWebWorld()
    option_definitions = the_witness_options

    item_name_to_id = {
        name: data.ap_code for name, data in StaticWitnessItems.item_data.items()
    }
    location_name_to_id = StaticWitnessLocations.ALL_LOCATIONS_TO_ID
    item_name_groups = StaticWitnessItems.item_groups

    required_client_version = (0, 3, 9)

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        self.player_logic = None
        self.locat = None
        self.items = None
        self.regio = None

        self.log_ids_to_hints = None

    def _get_slot_data(self):
        return {
            'seed': self.random.randrange(0, 1000000),
            'victory_location': int(self.player_logic.VICTORY_LOCATION, 16),
            'panelhex_to_id': self.locat.CHECK_PANELHEX_TO_ID,
            'item_id_to_door_hexes': StaticWitnessItems.get_item_to_door_mappings(),
            'door_hexes_in_the_pool': self.items.get_door_ids_in_pool(),
            'symbols_not_in_the_game': self.items.get_symbol_ids_not_in_pool(),
            'disabled_panels': list(self.player_logic.COMPLETELY_DISABLED_CHECKS),
            'log_ids_to_hints': self.log_ids_to_hints,
            'progressive_item_lists': self.items.get_progressive_item_ids_in_pool(),
            'obelisk_side_id_to_EPs': StaticWitnessLogic.OBELISK_SIDE_ID_TO_EP_HEXES,
            'precompleted_puzzles': [int(h, 16) for h in
                                     self.player_logic.EXCLUDED_LOCATIONS | self.player_logic.PRECOMPLETED_LOCATIONS],
            'entity_to_name': StaticWitnessLogic.ENTITY_ID_TO_NAME,
        }

    def generate_early(self):
        disabled_locations = self.multiworld.exclude_locations[self.player].value

        self.player_logic = WitnessPlayerLogic(
            self.multiworld, self.player, disabled_locations, self.multiworld.start_inventory[self.player].value
        )

        self.locat: WitnessPlayerLocations = WitnessPlayerLocations(self.multiworld, self.player, self.player_logic)
        self.items: WitnessPlayerItems = WitnessPlayerItems(self.multiworld, self.player, self.player_logic, self.locat)
        self.regio: WitnessRegions = WitnessRegions(self.locat)

        self.log_ids_to_hints = dict()

        if not (is_option_enabled(self.multiworld, self.player, "shuffle_symbols")
                or get_option_value(self.multiworld, self.player, "shuffle_doors")
                or is_option_enabled(self.multiworld, self.player, "shuffle_lasers")):
            if self.multiworld.players == 1:
                warning("This Witness world doesn't have any progression items. Please turn on Symbol Shuffle, Door"
                        " Shuffle or Laser Shuffle if that doesn't seem right.")
            else:
                raise Exception("This Witness world doesn't have any progression items. Please turn on Symbol Shuffle,"
                                " Door Shuffle or Laser Shuffle.")

    def create_regions(self):
        self.regio.create_regions(self.multiworld, self.player, self.player_logic)

    def create_items(self):

        # Determine pool size. Note that the dog location is included in the location list, so this needs to be -1.
        pool_size: int = len(self.locat.CHECK_LOCATION_TABLE) - len(self.locat.EVENT_LOCATION_TABLE) - 1

        # Fill mandatory items and remove precollected and/or starting items from the pool.
        item_pool: Dict[str, int] = self.items.get_mandatory_items()

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
            error_string = "The Witness world has too few locations ({num_loc}) to place its necessary items " \
                           "({num_item})."
            error(error_string.format(num_loc=pool_size, num_item=len(item_pool)))
            return

        remaining_item_slots = pool_size - sum(item_pool.values())

        # Add puzzle skips.
        num_puzzle_skips = get_option_value(self.multiworld, self.player, "puzzle_skip_amount")
        if num_puzzle_skips > remaining_item_slots:
            warning(f"The Witness world has insufficient locations to place all requested puzzle skips.")
            num_puzzle_skips = remaining_item_slots
        item_pool["Puzzle Skip"] = num_puzzle_skips
        remaining_item_slots -= num_puzzle_skips

        # Add junk items.
        if remaining_item_slots > 0:
            item_pool.update(self.items.get_filler_items(remaining_item_slots))

        # Add event items and tie them to event locations (e.g. laser activations).
        for event_location in self.locat.EVENT_LOCATION_TABLE:
            item_obj = self.create_item(
                self.player_logic.EVENT_ITEM_PAIRS[event_location]
            )
            location_obj = self.multiworld.get_location(event_location, self.player)
            location_obj.place_locked_item(item_obj)

        # BAD DOG GET BACK HERE WITH THAT PUZZLE SKIP YOU'RE POLLUTING THE ITEM POOL
        self.multiworld.get_location("Town Pet the Dog", self.player)\
            .place_locked_item(self.create_item("Puzzle Skip"))

        # Pick an early item to place on the tutorial gate.
        early_items = [item for item in self.items.get_early_items() if item in item_pool]
        if early_items:
            random_early_item = self.multiworld.random.choice(early_items)
            if get_option_value(self.multiworld, self.player, "puzzle_randomization") == 1:
                # In Expert, only tag the item as early, rather than forcing it onto the gate.
                self.multiworld.local_early_items[self.player][random_early_item] = 1
            else:
                # Force the item onto the tutorial gate check and remove it from our random pool.
                self.multiworld.get_location("Tutorial Gate Open", self.player)\
                    .place_locked_item(self.create_item(random_early_item))
                if item_pool[random_early_item] == 1:
                    item_pool.pop(random_early_item)
                else:
                    item_pool[random_early_item] -= 1

        # Generate the actual items.
        for item_name, quantity in sorted(item_pool.items()):
            self.multiworld.itempool += [self.create_item(item_name) for _ in range(0, quantity)]
            if self.items.item_data[item_name].local_only:
                self.multiworld.local_items[self.player].value.add(item_name)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.player_logic, self.locat)

    def fill_slot_data(self) -> dict:
        hint_amount = get_option_value(self.multiworld, self.player, "hint_amount")

        credits_hint = (
            "This Randomizer is brought to you by",
            "NewSoupVi, Jarno, blastron,",
            "jbzdarkid, sigma144, IHNN, oddGarrett, Exempt-Medic.", -1
        )

        audio_logs = get_audio_logs().copy()

        if hint_amount != 0:
            generated_hints = make_hints(self.multiworld, self.player, hint_amount)

            self.multiworld.per_slot_randoms[self.player].shuffle(audio_logs)

            duplicates = min(3, len(audio_logs) // hint_amount)

            for _ in range(0, hint_amount):
                hint = generated_hints.pop(0)

                for _ in range(0, duplicates):
                    audio_log = audio_logs.pop()
                    self.log_ids_to_hints[int(audio_log, 16)] = hint

        if audio_logs:
            audio_log = audio_logs.pop()
            self.log_ids_to_hints[int(audio_log, 16)] = credits_hint

        joke_hints = generate_joke_hints(self.multiworld, self.player, len(audio_logs))

        while audio_logs:
            audio_log = audio_logs.pop()
            self.log_ids_to_hints[int(audio_log, 16)] = joke_hints.pop()

        # generate hints done

        slot_data = self._get_slot_data()

        for option_name in the_witness_options:
            slot_data[option_name] = get_option_value(
                self.multiworld, self.player, option_name
            )

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
    check_hex: int = -1

    def __init__(self, player: int, name: str, address: Optional[int], parent, ch_hex: int = -1):
        super().__init__(player, name, address, parent)
        self.check_hex = ch_hex


def create_region(world: MultiWorld, player: int, name: str,
                  locat: WitnessPlayerLocations, region_locations=None, exits=None):
    """
    Create an Archipelago Region for The Witness
    """

    ret = Region(name, player, world)
    if region_locations:
        for location in region_locations:
            loc_id = locat.CHECK_LOCATION_TABLE[location]

            check_hex = -1
            if location in StaticWitnessLogic.CHECKS_BY_NAME:
                check_hex = int(
                    StaticWitnessLogic.CHECKS_BY_NAME[location]["checkHex"], 0
                )
            location = WitnessLocation(
                player, location, loc_id, ret, check_hex
            )

            ret.locations.append(location)
    if exits:
        for single_exit in exits:
            ret.exits.append(Entrance(player, single_exit, ret))

    return ret
