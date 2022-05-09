"""
Archipelago init file for The Witness
"""

import typing

from BaseClasses import Region, RegionType, Location, MultiWorld, Item, Entrance
from ..AutoWorld import World, WebWorld
from .player_logic import StaticWitnessLogic, WitnessPlayerLogic
from .locations import WitnessPlayerLocations, StaticWitnessLocations
from .items import WitnessItem, StaticWitnessItems, WitnessPlayerItems
from .rules import set_rules
from .regions import WitnessRegions
from .Options import is_option_enabled, the_witness_options
from .utils import best_junk_to_add_based_on_weights


class WitnessWebWorld(WebWorld):
    theme = "jungle"


class WitnessWorld(World):
    """
    The Witness is an open-world puzzle game with dozens of locations
    to explore and over 500 puzzles. Play the popular puzzle randomizer
    by sigma144, with an added layer of progression randomization!
    """
    game = "The Witness"
    topology_present = False
    static_logic = StaticWitnessLogic()
    static_locat = StaticWitnessLocations()
    static_items = StaticWitnessItems()
    web = WitnessWebWorld()
    options = the_witness_options

    item_name_to_id = {
        name: data.code for name, data in static_items.ALL_ITEM_TABLE.items()
    }
    location_name_to_id = StaticWitnessLocations.ALL_LOCATIONS_TO_ID

    def _get_slot_data(self):
        return {
            'seed': self.world.random.randint(0, 1000000),
            'victory_location': int(self.player_logic.VICTORY_LOCATION, 16),
            'panelhex_to_id': self.locat.CHECK_PANELHEX_TO_ID
        }

    def generate_early(self):
        self.player_logic = WitnessPlayerLogic(self.world, self.player)
        self.locat = WitnessPlayerLocations(self.world, self.player, self.player_logic)
        self.items = WitnessPlayerItems(self.locat, self.world, self.player, self.player_logic)
        self.regio = WitnessRegions(self.locat)

        self.junk_items_created = {key: 0 for key in self.items.JUNK_WEIGHTS.keys()}

    def generate_basic(self):
        # Generate item pool
        pool = []
        items_by_name = dict()
        for item in self.items.ITEM_TABLE:
            witness_item = self.create_item(item)
            if item not in self.items.EVENT_ITEM_TABLE:
                pool.append(witness_item)
                items_by_name[item] = witness_item

        # Put good item on first check
        random_good_item = self.world.random.choice(self.items.GOOD_ITEMS)
        first_check = self.world.get_location(
            "Tutorial Gate Open", self.player
        )
        first_check.place_locked_item(items_by_name[random_good_item])
        pool.remove(items_by_name[random_good_item])

        # Put in junk items to fill the rest
        junk_size = len(self.locat.CHECK_LOCATION_TABLE) - len(pool) - len(self.locat.EVENT_LOCATION_TABLE) - 1

        for i in range(0, junk_size):
            pool.append(self.create_item(self.get_filler_item_name()))

        # Tie Event Items to Event Locations (e.g. Laser Activations)
        for event_location in self.locat.EVENT_LOCATION_TABLE:
            item_obj = self.create_item(
                self.player_logic.EVENT_ITEM_PAIRS[event_location]
            )
            location_obj = self.world.get_location(event_location, self.player)
            location_obj.place_locked_item(item_obj)

        self.world.itempool += pool

    def create_regions(self):
        self.regio.create_regions(self.world, self.player, self.player_logic)

    def set_rules(self):
        set_rules(self.world, self.player, self.player_logic, self.locat)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()

        slot_data["hard_mode"] = False

        for option_name in the_witness_options:
            slot_data[option_name] = is_option_enabled(
                self.world, self.player, option_name
            )

        return slot_data

    def create_item(self, name: str) -> Item:
        # this conditional is purely for unit tests, which need to be able to create an item before generate_early
        if hasattr(self, 'items'):
            item = self.items.ITEM_TABLE[name]
        else:
            item = StaticWitnessItems.ALL_ITEM_TABLE[name]

        new_item = WitnessItem(
            name, item.progression, item.code, player=self.player
        )
        new_item.trap = item.trap
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

    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
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
