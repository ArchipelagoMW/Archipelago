from worlds.AutoWorld import WebWorld, World

import logging

from .Options import GSTLAOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items
from .Locations import GSTLALocation, all_locations, location_name_to_id
from .Regions import create_regions
from .Names.ItemName import ItemName
from .Names.LocationName import LocationName
from .Names.RegionName import RegionName


class GSTLAWeb(WebWorld):
    theme = "jungle"


class GSTLAWorld(World):
    game = "Golden Sun The Lost Age"
    option_definitions = GSTLAOptions
    data_version = 1

    item_name_to_id = {item.itemName: item.id for item in all_items }
    location_name_to_id = location_name_to_id
    web = GSTLAWeb()


    def generate_early(self) -> None:
        pass


    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)


    def create_items(self) -> None:
        for item in all_items:
            for _ in range(item.quantity):
                self.multiworld.itempool.append(self.create_item(item.itemName))


    def set_rules(self) -> None:
        self.multiworld.get_location(LocationName.Dehkan_Plateau_Nut, self.player).access_rule = \
          lambda state: state.has(ItemName.Lash_Pebble, self.player)

        self.multiworld.get_location(LocationName.DoomDragonDefeated, self.player).access_rule = \
            lambda state: state.has(ItemName.Cyclone_Chip, self.player)

        self.multiworld.get_location(LocationName.DoomDragonDefeated, self.player) \
            .place_locked_item(self.create_event(ItemName.Victory))
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)


    def generate_output(self, output_directory: str):
        pass


    def create_item(self, name: str) -> "Item":
        item = item_table[name]
        return GSTLAItem(item.itemName, item.progression, item.id, self.player)


    def create_event(self, event: str):
        return GSTLAItem(event, ItemClassification.progression, None, self.player)