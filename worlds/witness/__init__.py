"""
Archipelago init file for The Witness
"""

from typing import NamedTuple, Union
import typing
import logging
import random

from BaseClasses import (
    Region, RegionType, Location, MultiWorld, Item, Entrance
)

from ..AutoWorld import World
from .items import WitnessItem, ITEM_TABLE, junk_weights, EVENT_ITEM_TABLE
from .locations import (
    CHECK_LOCATION_TABLE, EVENT_LOCATION_TABLE,
    ALL_LOCATIONS_TO_ID, CHECK_PANELHEX_TO_ID
)
from .rules import set_rules
from .regions import create_regions
from .full_logic import ParsedWitnessLogic
from .Options import is_option_enabled, the_witness_options


class WitnessWorld(World):
    """
    Archipelago World class for The Witness
    """
    game = "The Witness"
    topology_present = False
    item_name_to_id = {name: data.code for name, data in ITEM_TABLE.items()}
    location_name_to_id = ALL_LOCATIONS_TO_ID
    hidden = False
    options = the_witness_options
    logic = ParsedWitnessLogic()

    def _get_slot_data(self):
        return {
            'seed': self.world.random.randint(0, 1000000),
            'panelhex_to_id': CHECK_PANELHEX_TO_ID
        }

    def generate_basic(self):
        # Link regions

        # Generate item pool
        pool = []
        for item in ITEM_TABLE:
            witness_item = self.create_item(item)
            if not item == "Victory" and item not in EVENT_ITEM_TABLE:
                pool.append(witness_item)

        junk_pool = junk_weights.copy()
        junk_pool = self.world.random.choices(
            list(junk_pool.keys()), weights=list(junk_pool.values()),
            k=len(CHECK_LOCATION_TABLE)-len(pool)-len(EVENT_LOCATION_TABLE) - 1
        )

        pool += [self.create_item(junk) for junk in junk_pool]

        victory_location = "Inside Mountain Final Room Elevator Start"
        victory_ap_loc = self.world.get_location(victory_location, self.player)
        victory_ap_loc.place_locked_item(self.create_item("Victory"))

        for event_location in EVENT_LOCATION_TABLE:
            item_obj = self.create_item(
                self.logic.EVENT_ITEM_PAIRS[event_location]
            )
            location_obj = self.world.get_location(event_location, self.player)
            location_obj.place_locked_item(item_obj)

        self.world.itempool += pool

    def create_regions(self):
        create_regions(self.world, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()

        for option_name in the_witness_options:
            slot_data[option_name] = is_option_enabled(
                self.world, self.player, option_name
            )

        slot_data["hard_mode"] = False

        return slot_data

    def create_item(self, name: str) -> Item:
        item = ITEM_TABLE[name]
        return WitnessItem(
            name, item.progression, item.code, player=self.player
        )


class WitnessLocation(Location):
    """
    Archipelago Location for The Witness
    """
    game: str = "The Witness"
    check_hex: int = -1

    def __init__(self, player: int, name: str, address: typing.Optional[int],
                 parent, ch_hex: int = -1):

        super().__init__(player, name, address, parent)
        self.check_hex = ch_hex


def create_region(world: MultiWorld, player: int, name: str, 
                  logic: ParsedWitnessLogic, locations=None, exits=None):
    """
    Create an Archipelago Region for The Witness
    """

    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            print(location)
            
            loc_id = CHECK_LOCATION_TABLE[location]

            check_hex = -1
            if location in logic.CHECKS_BY_NAME:
                check_hex = int(
                    logic.CHECKS_BY_NAME[location]["checkHex"], 0
                )
            location = WitnessLocation(
                player, location, loc_id, ret, check_hex
            )

            ret.locations.append(location)
    if exits:
        for single_exit in exits:
            ret.exits.append(Entrance(player, single_exit, ret))

    return ret