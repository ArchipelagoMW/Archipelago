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
from .player_logic import LingoPlayerLogic


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
            'seed': self.multiworld.per_slot_randoms[self.player].randint(0, 1000000),
        }

    def generate_early(self):
        self.player_logic = LingoPlayerLogic(self.multiworld, self.player, self.static_logic)
        self.topology_present = get_option_value(self.multiworld, self.player, "shuffle_paintings")

    def create_region(self, room: Room):
        new_region = Region(room.name, self.player, self.multiworld)

        if room.name in self.player_logic.LOCATIONS_BY_ROOM.keys():
            for location in self.player_logic.LOCATIONS_BY_ROOM[room.name]:
                new_loc = LingoLocation(self.player, location.name, location.code, new_region)
                new_region.locations.append(new_loc)

        self.multiworld.regions += [
            new_region
        ]

    def connect(self, target: Room, entrance: RoomEntrance):
        target_region = self.multiworld.get_region(target.name, self.player)
        source_region = self.multiworld.get_region(entrance.room, self.player)
        connection = Entrance(self.player, f"{entrance.room} to {target.name}", source_region)
        connection.access_rule = lambda state: state.lingo_can_use_entrance(
            target.name, entrance.door, self.multiworld, self.player, self.player_logic)

        source_region.exits.append(connection)
        connection.connect(target_region)

    def handle_pilgrim_room(self):
        target_region = self.multiworld.get_region("Pilgrim Antechamber", self.player)
        source_region = self.multiworld.get_region("Outside The Agreeable", self.player)
        connection = Entrance(self.player, f"Pilgrimage", source_region)
        connection.access_rule = lambda state: state.lingo_can_use_pilgrimage(
            self.player, self.player_logic)

        source_region.exits.append(connection)
        connection.connect(target_region)

    def connect_painting(self, warp_enter: str, warp_exit: str):
        source_painting = StaticLingoLogic.PAINTINGS[warp_enter]
        target_painting = StaticLingoLogic.PAINTINGS[warp_exit]

        target_region = self.multiworld.get_region(target_painting.room, self.player)
        source_region = self.multiworld.get_region(source_painting.room, self.player)
        connection = Entrance(self.player, f"{source_painting.room} to {target_painting.room} (Painting)",
                              source_region)
        connection.access_rule = lambda state: state.lingo_can_use_entrance(
            target_painting.room, source_painting.required_door, self.multiworld, self.player, self.player_logic)

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
                if entrance.painting and get_option_value(self.multiworld, self.player, "shuffle_paintings"):
                    # Don't use the vanilla painting connections if we are shuffling paintings.
                    continue

                self.connect(room, entrance)

        self.handle_pilgrim_room()

        if get_option_value(self.multiworld, self.player, "shuffle_paintings"):
            for warp_enter, warp_exit in self.player_logic.PAINTING_MAPPING.items():
                self.connect_painting(warp_enter, warp_exit)

    def create_items(self):
        pool = []

        for name in self.player_logic.REAL_ITEMS:
            new_item = self.create_item(name)
            pool.append(new_item)

        for location, item in self.player_logic.EVENT_LOC_TO_ITEM.items():
            event_item = LingoItem(item, ItemClassification.progression, None, player=self.player)
            location_obj = self.multiworld.get_location(location, self.player)
            location_obj.place_locked_item(event_item)

        while len(pool) < len(self.player_logic.REAL_LOCATIONS):
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
        set_rules(self.multiworld, self.player, self.player_logic)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        slot_data = self._get_slot_data()

        for option_name in lingo_options:
            slot_data[option_name] = get_option_value(self.multiworld, self.player, option_name)

        if get_option_value(self.multiworld, self.player, "shuffle_paintings"):
            slot_data["painting_entrance_to_exit"] = self.player_logic.PAINTING_MAPPING
            slot_data["paintings"] = {
                painting.id: {"orientation": painting.orientation, "move": painting.move}
                for painting in self.static_logic.PAINTINGS.values()
            }

        return slot_data
