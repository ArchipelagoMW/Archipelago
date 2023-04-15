"""
Archipelago init file for Lingo
"""
import typing

from BaseClasses import Region, Location, MultiWorld, Item, Entrance, Tutorial, ItemClassification
from ..AutoWorld import World, WebWorld
from .static_logic import StaticLingoLogic, Room, RoomEntrance
from .items import LingoItem, StaticLingoItems
from .locations import LingoLocation, StaticLingoLocations
from .Options import lingo_options, get_option_value
from ..generic.Rules import set_rule
from .rules import LingoLogic, set_rules


class LingoWebWorld(WebWorld):
    theme = "grass"


class LingoWorld(World):
    """
    TODO: Describe Lingo
    """
    game = "Lingo"
    web = LingoWebWorld()

    base_id = 444400

    static_logic = StaticLingoLogic()
    static_items = StaticLingoItems(base_id)
    static_locat = StaticLingoLocations(base_id)
    option_definitions = lingo_options

    item_name_to_id = {
        name: data.code for name, data in static_items.ALL_ITEM_TABLE.items()
    }
    location_name_to_id = {
        name: data.code for name, data in static_locat.ALL_LOCATION_TABLE.items()
        if data.code is not None
    }

    def _get_slot_data(self):
        return {
            'door_ids_by_item_id': {
                data.code: data.door_ids for name, data in self.static_items.ALL_ITEM_TABLE.items()
                if data.code is not None and len(data.door_ids) > 0
            },
            'painting_ids_by_item_id': {
                data.code: data.painting_ids for name, data in self.static_items.ALL_ITEM_TABLE.items()
                if data.code is not None and len(data.painting_ids) > 0
            },
            'panel_ids_by_location_id': {
                data.code: data.panel_ids() for name, data in self.static_locat.ALL_LOCATION_TABLE.items()
                if data.code is not None
            },
        }

    def create_region(self, room: Room):
        new_region = Region(room.name, self.player, self.multiworld)

        for location_name, location in StaticLingoLocations.ALL_LOCATION_TABLE.items():
            if location.room == room.name:
                new_loc = LingoLocation(self.player, location_name, location.code, new_region)
                new_region.locations.append(new_loc)

        self.multiworld.regions += [
            new_region
        ]

    def connect(self, target: Room, entrance: RoomEntrance):
        target_region = self.multiworld.get_region(target.name, self.player)
        source_region = self.multiworld.get_region(entrance.room, self.player)
        connection = Entrance(self.player, f"{entrance.room} to {target.name}", source_region)
        connection.access_rule = lambda state: state.lingo_can_use_entrance(
            target.name, entrance.doors, self.multiworld, self.player)

        source_region.exits.append(connection)
        connection.connect(target_region)

    def create_regions(self):
        self.multiworld.regions += [
            Region("Menu", self.player, self.multiworld)
        ]

        for room in StaticLingoLogic.ALL_ROOMS:
            self.create_region(room)
        
        for room in StaticLingoLogic.ALL_ROOMS:
            for entrance in room.entrances:
                self.connect(room, entrance)
    
    def create_items(self):
        pool = []
        placed_events = 0

        for name, item in self.static_items.ALL_ITEM_TABLE.items():
            if item.should_include(self.multiworld, self.player):
                new_item = self.create_item(name)
                pool.append(new_item)
        
        if get_option_value(self.multiworld, self.player, "orange_tower_access") == 2:
            for i in range(0, 6):
                new_item = self.create_item("Progressive Orange Tower")
                pool.append(new_item)
        
        victory_item = LingoItem("Victory", ItemClassification.progression, None, player=self.player)
        victory_condition = get_option_value(self.multiworld, self.player, "victory_condition")
        if victory_condition == 0:  # THE END
            location_obj = self.multiworld.get_location("Orange Tower Seventh Floor - THE END", self.player)
            location_obj.place_locked_item(victory_item)
            placed_events += 1
        elif victory_condition == 1:  # THE MASTER
            location_obj = self.multiworld.get_location("Orange Tower Seventh Floor - THE MASTER", self.player)
            location_obj.place_locked_item(victory_item)
            placed_events += 1

        while (len(pool) + placed_events) < len(StaticLingoLocations.ALL_LOCATION_TABLE):
            pool.append(self.create_item("Nothing"))
        
        self.multiworld.itempool += pool
    
    def create_item(self, name: str) -> Item:
        item = StaticLingoItems.ALL_ITEM_TABLE[name]

        if item.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
        
        new_item = LingoItem(name, classification, item.code, player=self.player)
        return new_item

    def set_rules(self):
        set_rules(self.multiworld, self.player)
        
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        slot_data = self._get_slot_data()

        for option_name in lingo_options:
            slot_data[option_name] = get_option_value(self.multiworld, self.player, option_name)

        return slot_data
