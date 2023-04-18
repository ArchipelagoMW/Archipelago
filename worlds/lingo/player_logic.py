from typing import Dict, List, Optional, NamedTuple
from BaseClasses import MultiWorld
from .Options import get_option_value
from .locations import LocationData, StaticLingoLocations
from .static_logic import RoomAndPanel, StaticLingoLogic
from .items import ItemData, StaticLingoItems


class PlayerLocation(NamedTuple):
    name: str
    code: Optional[int] = None
    panels: list[RoomAndPanel] = []


class LingoPlayerLogic:
    """
    Defines logic after a player's options have been applied
    """

    ITEM_BY_DOOR: Dict[str, Dict[str, str]]

    LOCATIONS_BY_ROOM: Dict[str, List[PlayerLocation]]
    REAL_LOCATIONS: List[str]

    EVENT_LOC_TO_ITEM: Dict[str, str]
    REAL_ITEMS: List[str]

    VICTORY_CONDITION: str

    PAINTING_MAPPING: Dict[str, str]

    def add_location(self, room: str, loc: PlayerLocation):
        self.LOCATIONS_BY_ROOM.setdefault(room, []).append(loc)

    def set_door_item(self, room: str, door: str, item: str):
        self.ITEM_BY_DOOR.setdefault(room, {})[door] = item

    def __init__(self, world: MultiWorld, player: int, static_logic: StaticLingoLogic):
        self.ITEM_BY_DOOR = {}
        self.LOCATIONS_BY_ROOM = {}
        self.REAL_LOCATIONS = []
        self.EVENT_LOC_TO_ITEM = {}
        self.REAL_ITEMS = []
        self.VICTORY_CONDITION = ""
        self.PAINTING_MAPPING = {}

        if get_option_value(world, player, "shuffle_doors") == 0:  # no door shuffle
            for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
                for door_name, door_data in room_data.items():
                    itemloc_name = f"{room_name} - {door_name} (Opened)"
                    self.add_location(room_name, PlayerLocation(itemloc_name, None, door_data.panels))
                    self.EVENT_LOC_TO_ITEM[itemloc_name] = itemloc_name
                    self.set_door_item(room_name, door_name, itemloc_name)
        elif get_option_value(world, player, "shuffle_doors") == 1:  # simple doors
            for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
                for door_name, door_data in room_data.items():
                    # This line is duplicated from StaticLingoItems
                    if door_data.skip_item is False and door_data.event is False:
                        if door_data.group is None:
                            self.set_door_item(room_name, door_name, door_data.item_name)
                        else:
                            self.set_door_item(room_name, door_name, door_data.group)
        elif get_option_value(world, player, "shuffle_doors") == 2:  # complex doors
            for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
                for door_name, door_data in room_data.items():
                    # This line is duplicated from StaticLingoItems
                    if door_data.skip_item is False and door_data.event is False:
                        self.set_door_item(room_name, door_name, door_data.item_name)

        for room_name, room_data in StaticLingoLogic.DOORS_BY_ROOM.items():
            for door_name, door_data in room_data.items():
                if door_data.event:
                    self.add_location(room_name, PlayerLocation(door_data.item_name, None, door_data.panels))
                    self.EVENT_LOC_TO_ITEM[door_data.item_name] = door_data.item_name + " (Opened)"
                    self.set_door_item(room_name, door_name, door_data.item_name + " (Opened)")

        if get_option_value(world, player, "victory_condition") == 0:
            self.VICTORY_CONDITION = "Orange Tower Seventh Floor - THE END"
            self.add_location("Orange Tower Seventh Floor", PlayerLocation("The End (Solved)"))
            self.EVENT_LOC_TO_ITEM["The End (Solved)"] = "Victory"
        elif get_option_value(world, player, "victory_condition") == 1:
            self.VICTORY_CONDITION = "Orange Tower Seventh Floor - THE MASTER"
            self.EVENT_LOC_TO_ITEM["Orange Tower Seventh Floor - Mastery Achievements"] = "Victory"

        for location_name, location_data in StaticLingoLocations.ALL_LOCATION_TABLE.items():
            if location_name != self.VICTORY_CONDITION:
                self.add_location(location_data.room, PlayerLocation(location_name, location_data.code,
                                                                     location_data.panels))
                self.REAL_LOCATIONS.append(location_name)

        for name, item in StaticLingoItems.ALL_ITEM_TABLE.items():
            if item.should_include(world, player):
                self.REAL_ITEMS.append(name)

        if get_option_value(world, player, "shuffle_doors") > 0 and get_option_value(world, player,
                                                                                     "orange_tower_access") == 2:
            for i in range(0, 6):
                self.REAL_ITEMS.append("Progressive Orange Tower")

        if get_option_value(world, player, "shuffle_paintings"):
            chosen_exits = []
            if get_option_value(world, player, "shuffle_doors") == 0:
                chosen_exits = [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                                if painting.required_when_no_doors]
            chosen_exits += [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                             if painting.exit_only and painting.required]
            exitable = [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                        if not painting.enter_only and not painting.disable and not painting.required]
            chosen_exits += world.per_slot_randoms[player].sample(exitable,
                                                                  static_logic.PAINTING_EXITS - len(chosen_exits))

            enterable = [painting_id for painting_id, painting in StaticLingoLogic.PAINTINGS.items()
                         if not painting.exit_only and not painting.disable and painting_id not in chosen_exits]
            chosen_entrances = world.per_slot_randoms[player].sample(enterable, static_logic.PAINTING_ENTRANCES)

            for warp_exit in chosen_exits:
                warp_enter = world.per_slot_randoms[player].choice(chosen_entrances)
                chosen_entrances.remove(warp_enter)
                self.PAINTING_MAPPING[warp_enter] = warp_exit

            for warp_enter in chosen_entrances:
                warp_exit = world.per_slot_randoms[player].choice(chosen_exits)
                self.PAINTING_MAPPING[warp_enter] = warp_exit
