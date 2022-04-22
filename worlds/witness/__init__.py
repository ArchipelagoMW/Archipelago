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
from .items import WitnessItems, WitnessItem
from .locations import WitnessLocations
from .rules import set_rules
from .regions import WitnessRegions
from .full_logic import ParsedWitnessLogic
from .Options import is_option_enabled, the_witness_options


class WitnessWorld(World):
    """
    Archipelago World class for The Witness
    """
    game = "The Witness"
    topology_present = False
    logic_shell = ParsedWitnessLogic()
    locat_shell = WitnessLocations(logic_shell)
    items_shell = WitnessItems(logic_shell)
    options = the_witness_options
    item_name_to_id = {
        name: data.code for name, data in items_shell.ITEM_TABLE.items()
    }
    location_name_to_id = locat_shell.ALL_LOCATIONS_TO_ID

    hidden = False

    def _get_slot_data(self):
        return {
            'seed': self.world.random.randint(0, 1000000),
            'victory_location': int(self.logic.VICTORY_LOCATION, 16),
            'panelhex_to_id': self.locat.CHECK_PANELHEX_TO_ID
        }

    def generate_early(self):
        self.logic = ParsedWitnessLogic()
        self.logic.adjustments(self.world, self.player)
        self.locat = WitnessLocations(self.logic)
        self.locat.define_locations(self.world, self.player)
        self.items = WitnessItems(self.logic)
        self.items.adjust_after_options(self.locat)
        self.regio = WitnessRegions(self.logic, self.locat)

    def generate_basic(self):
        # Generate item pool
        pool = []
        items_by_name = dict()
        for item in self.items.ITEM_TABLE:
            witness_item = self.create_item(item)
            if item not in self.items.EVENT_ITEM_TABLE:
                pool.append(witness_item)
                items_by_name[item] = witness_item

        good_items = [
            "Dots", "Black/White Squares", "Stars",
            "Colored Squares", "Shapers"
        ]
        random_good_item = self.world.random.choice(good_items)
        first_check = self.world.get_location(
            "Tutorial Gate Open", self.player
        )
        first_check.place_locked_item(items_by_name[random_good_item])
        pool.remove(items_by_name[random_good_item])

        junk_pool = self.items.JUNK_WEIGHTS.copy()
        junk_pool = self.world.random.choices(
            list(junk_pool.keys()), weights=list(junk_pool.values()),
            k=len(self.locat.CHECK_LOCATION_TABLE) - len(pool)
            - len(self.locat.EVENT_LOCATION_TABLE) - 1
        )

        pool += [self.create_item(junk) for junk in junk_pool]

        for event_location in self.locat.EVENT_LOCATION_TABLE:
            item_obj = self.create_item(
                self.logic.EVENT_ITEM_PAIRS[event_location]
            )
            location_obj = self.world.get_location(event_location, self.player)
            location_obj.place_locked_item(item_obj)

        self.world.itempool += pool

    def create_regions(self):
        self.regio.create_regions(self.world, self.player)

    def set_rules(self):
        set_rules(self.world, self.player, self.logic, self.locat)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()

        for option_name in the_witness_options:
            slot_data[option_name] = is_option_enabled(
                self.world, self.player, option_name
            )

        slot_data["hard_mode"] = False

        return slot_data

    def create_item(self, name: str) -> Item:
        item = self.items.ITEM_TABLE[name]
        new_item = WitnessItem(
            name, item.progression, item.code, player=self.player
        )
        new_item.trap = item.trap
        return new_item


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
                  logic: ParsedWitnessLogic, locat: WitnessLocations,
                  locations=None, exits=None):
    """
    Create an Archipelago Region for The Witness
    """

    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = locat.CHECK_LOCATION_TABLE[location]

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
