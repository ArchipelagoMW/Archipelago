from worlds.AutoWorld import WebWorld, World

import logging
from typing import List

from .Options import GSTLAOptions
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification,\
    LocationProgressType, Region, Entrance
from .Items import GSTLAItem, item_table, all_items, ItemType
from .Locations import GSTLALocation, all_locations, location_name_to_id, LocationType
from .Rules import set_access_rules, set_item_rules
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
    djinnlist = []

    item_name_to_id = {item.itemName: item.id for item in all_items }
    location_name_to_id = {location: location_name_to_id[location].id for location in location_name_to_id}
    web = GSTLAWeb()

    item_name_groups = {
        ItemType.Djinn: { "Echo", "Fog", "Breath", "Iron", "Cannon" },
        "venus_djinn": {},
        "mercury_djinn": {},
        "mars_djinn": {},
        "jupiter_djinn": {}
    }

    cyclonechip = []


    def generate_early(self) -> None:
        pass


    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)


    def create_items(self) -> None:
        for item in all_items:
            for _ in range(item.quantity):
                ap_item = self.create_item(item.itemName)
                if item.type == ItemType.Djinn:
                    self.djinnlist.append(ap_item)
                elif item.itemName == ItemName.Cyclone_Chip:
                    self.cyclonechip.append(ap_item)
                else:
                    self.multiworld.itempool.append(self.create_item(item.itemName))


    def set_rules(self) -> None:
        set_item_rules(self.multiworld, self.player)
        set_access_rules(self.multiworld, self.player)

        self.multiworld.get_location(LocationName.DoomDragonDefeated, self.player) \
            .place_locked_item(self.create_event(ItemName.Victory))

        self.multiworld.get_location(LocationName.DefeatChestBeaters, self.player) \
            .place_locked_item(self.create_event("DefeatChestbeaters"))

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has(ItemName.Victory, self.player)

    def generate_basic(self):
        pass

    def get_pre_fill_items(self) -> List["Item"]:
        return self.djinnlist

    def pre_fill(self) -> None:
        from Fill import fill_restrictive, FillError
        all_state = self.multiworld.get_all_state(use_cache=False)
        locs = []
        #Todo: replace this with a list of djinn locations and fill them up with djinn items
        locs.append( self.multiworld.get_location("Echo", self.player))
        locs.append( self.multiworld.get_location("Fog", self.player))
        locs.append( self.multiworld.get_location("Breath", self.player))
        locs.append( self.multiworld.get_location("Iron", self.player))
        locs.append( self.multiworld.get_location("Cannon", self.player))

        self.multiworld.random.shuffle(locs)
        self.multiworld.random.shuffle(self.djinnlist)

        for ap_item in self.djinnlist:
            all_state.remove(ap_item)

        all_state.remove(self.cyclonechip[0])

        fill_restrictive(self.multiworld, all_state, locs, self.djinnlist, True, True)

        fill_restrictive(self.multiworld, all_state, [self.multiworld.get_location(LocationName.Kandorean_Temple_Lash_Pebble, self.player)], self.cyclonechip, True, True)

    def generate_output(self, output_directory: str):
        pass


    def create_item(self, name: str) -> "Item":
        item = item_table[name]
        return GSTLAItem(item.itemName, item.progression, item.id, self.player)


    def create_event(self, event: str):
        return GSTLAItem(event, ItemClassification.progression, None, self.player)