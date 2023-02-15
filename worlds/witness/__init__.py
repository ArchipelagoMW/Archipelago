"""
Archipelago init file for The Witness
"""
import typing

from BaseClasses import Region, Location, MultiWorld, Item, Entrance, Tutorial, ItemClassification
from .hints import get_always_hint_locations, get_always_hint_items, get_priority_hint_locations, \
    get_priority_hint_items, make_hints, generate_joke_hints
from ..AutoWorld import World, WebWorld
from .player_logic import WitnessPlayerLogic
from .static_logic import StaticWitnessLogic
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .items import WitnessItem, StaticWitnessItems, WitnessPlayerItems
from .rules import set_rules
from .regions import WitnessRegions
from .Options import is_option_enabled, the_witness_options, get_option_value
from .utils import best_junk_to_add_based_on_weights, get_audio_logs
from logging import warning


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
    data_version = 12

    static_logic = StaticWitnessLogic()
    static_locat = StaticWitnessLocations()
    static_items = StaticWitnessItems()
    web = WitnessWebWorld()
    option_definitions = the_witness_options

    item_name_to_id = {
        name: data.code for name, data in static_items.ALL_ITEM_TABLE.items()
    }
    location_name_to_id = StaticWitnessLocations.ALL_LOCATIONS_TO_ID
    item_name_groups = StaticWitnessItems.ITEM_NAME_GROUPS

    required_client_version = (0, 3, 8)

    def _get_slot_data(self):
        return {
            'seed': self.multiworld.per_slot_randoms[self.player].randint(0, 1000000),
            'victory_location': int(self.player_logic.VICTORY_LOCATION, 16),
            'panelhex_to_id': self.locat.CHECK_PANELHEX_TO_ID,
            'item_id_to_door_hexes': self.static_items.ITEM_ID_TO_DOOR_HEX_ALL,
            'door_hexes_in_the_pool': self.items.DOORS,
            'symbols_not_in_the_game': self.items.SYMBOLS_NOT_IN_THE_GAME,
            'disabled_panels': self.player_logic.COMPLETELY_DISABLED_CHECKS,
            'log_ids_to_hints': self.log_ids_to_hints,
            'progressive_item_lists': self.items.MULTI_LISTS_BY_CODE,
            'obelisk_side_id_to_EPs': self.static_logic.OBELISK_SIDE_ID_TO_EP_HEXES,
            'precompleted_puzzles': {int(h, 16) for h in self.player_logic.PRECOMPLETED_LOCATIONS},
            'ep_to_name': self.static_logic.EP_ID_TO_NAME,
        }

    def generate_early(self):
        self.items_by_name = dict()

        if not (is_option_enabled(self.multiworld, self.player, "shuffle_symbols")
                or get_option_value(self.multiworld, self.player, "shuffle_doors")
                or is_option_enabled(self.multiworld, self.player, "shuffle_lasers")):
            if self.multiworld.players == 1:
                warning("This Witness world doesn't have any progression items. Please turn on Symbol Shuffle, Door"
                        " Shuffle or Laser Shuffle if that doesn't seem right.")
            else:
                raise Exception("This Witness world doesn't have any progression items. Please turn on Symbol Shuffle,"
                                " Door Shuffle or Laser Shuffle.")

        disabled_locations = self.multiworld.exclude_locations[self.player].value

        self.player_logic = WitnessPlayerLogic(
            self.multiworld, self.player, disabled_locations, self.multiworld.start_inventory[self.player].value
        )

        self.locat = WitnessPlayerLocations(self.multiworld, self.player, self.player_logic)
        self.items = WitnessPlayerItems(self.locat, self.multiworld, self.player, self.player_logic)
        self.regio = WitnessRegions(self.locat)

    def create_regions(self):
        self.regio.create_regions(self.multiworld, self.player, self.player_logic)

    def generate_basic(self):
        self.log_ids_to_hints = dict()
        self.junk_items_created = {key: 0 for key in self.items.JUNK_WEIGHTS.keys()}

        # Generate item pool
        pool = []
        for item in self.items.ITEM_TABLE:
            for i in range(0, self.items.PROG_ITEM_AMOUNTS[item]):
                if item in self.items.PROGRESSION_TABLE:
                    witness_item = self.create_item(item)
                    pool.append(witness_item)
                    self.items_by_name[item] = witness_item

        less_junk = 0

        dog_check = self.multiworld.get_location(
            "Town Pet the Dog", self.player
        )

        dog_check.place_locked_item(self.create_item("Puzzle Skip"))

        less_junk += 1

        for precol_item in self.multiworld.precollected_items[self.player]:
            if precol_item.name in self.items_by_name:  # if item is in the pool, remove 1 instance.
                item_obj = self.items_by_name[precol_item.name]

                if item_obj in pool:
                    pool.remove(item_obj) # remove one instance of this pre-collected item if it exists

        for item in self.player_logic.STARTING_INVENTORY:
            self.multiworld.push_precollected(self.items_by_name[item])
            pool.remove(self.items_by_name[item])

        for item in self.items.EXTRA_AMOUNTS:
            for i in range(0, self.items.EXTRA_AMOUNTS[item]):
                if len(pool) < len(self.locat.CHECK_LOCATION_TABLE) - len(self.locat.EVENT_LOCATION_TABLE) - less_junk:
                    witness_item = self.create_item(item)
                    pool.append(witness_item)

        # Put in junk items to fill the rest
        junk_size = len(self.locat.CHECK_LOCATION_TABLE) - len(pool) - len(self.locat.EVENT_LOCATION_TABLE) - less_junk

        for i in range(0, junk_size):
            pool.append(self.create_item(self.get_filler_item_name()))

        # Tie Event Items to Event Locations (e.g. Laser Activations)
        for event_location in self.locat.EVENT_LOCATION_TABLE:
            item_obj = self.create_item(
                self.player_logic.EVENT_ITEM_PAIRS[event_location]
            )
            location_obj = self.multiworld.get_location(event_location, self.player)
            location_obj.place_locked_item(item_obj)

        self.multiworld.itempool += pool

    def pre_fill(self):
        # Put good item on first check if there are any of the designated "good items" in the pool
        good_items_in_the_game = []

        for symbol in self.items.GOOD_ITEMS:
            item = self.items_by_name[symbol]
            if item in self.multiworld.itempool: # Only do this if the item is still in item pool (e.g. after plando)
                good_items_in_the_game.append(symbol)

        if good_items_in_the_game:
            random_good_item = self.multiworld.random.choice(good_items_in_the_game)

            first_check = self.multiworld.get_location(
                "Tutorial Gate Open", self.player
            )
            item = self.items_by_name[random_good_item]

            first_check.place_locked_item(item)
            self.multiworld.itempool.remove(item)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.player_logic, self.locat)

    def fill_slot_data(self) -> dict:
        hint_amount = get_option_value(self.multiworld, self.player, "hint_amount")

        credits_hint = (
            "This Randomizer is brought to you by",
            "NewSoupVi, Jarno, blastron,",
            "jbzdarkid, sigma144, IHNN, oddGarrett.", -1
        )

        audio_logs = get_audio_logs().copy()

        if hint_amount != 0:
            generated_hints = make_hints(self.multiworld, self.player, hint_amount)

            self.multiworld.per_slot_randoms[self.player].shuffle(audio_logs)

            duplicates = len(audio_logs) // hint_amount

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

    def create_item(self, name: str) -> Item:
        # this conditional is purely for unit tests, which need to be able to create an item before generate_early
        if hasattr(self, 'items') and name in self.items.ITEM_TABLE:
            item = self.items.ITEM_TABLE[name]
        else:
            item = StaticWitnessItems.ALL_ITEM_TABLE[name]

        if item.trap:
            classification = ItemClassification.trap
        elif item.progression:
            classification = ItemClassification.progression
        elif item.never_exclude:
            classification = ItemClassification.useful
        else:
            classification = ItemClassification.filler

        new_item = WitnessItem(
            name, classification, item.code, player=self.player
        )
        return new_item

    def get_filler_item_name(self) -> str:  # Used by itemlinks
        item = best_junk_to_add_based_on_weights(self.items.JUNK_WEIGHTS, self.junk_items_created)

        self.junk_items_created[item] += 1

        return item


class WitnessLocation(Location):
    """
    Archipelago Location for The Witness
    """
    game: str = "The Witness"
    check_hex: int = -1

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent, ch_hex: int = -1):
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
