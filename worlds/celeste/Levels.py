from __future__ import annotations
from copy import deepcopy
from enum import IntEnum
from typing import Callable, Dict, List

from BaseClasses import CollectionState


class LocationType(IntEnum):
    Strawberry = 0
    Golden_Strawberry = 1
    Cassette = 2
    Crystal_Heart = 3
    Checkpoint = 4
    Level_Clear = 5
    Room_Enter = 6

class DoorDirection(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


class Door:
    name: str
    room_name: str
    room: Room
    dir: DoorDirection
    blocked: bool
    closes_behind: bool
    region: PreRegion

    def __init__(self, name: str, room_name: str, dir: DoorDirection, blocked: bool, closes_behind: bool):
        self.name = name
        self.room_name = room_name
        self.dir = dir
        self.blocked = blocked
        self.closes_behind = closes_behind
        # Find PreRegion later using our name once we know it exists


class PreRegion:
    name: str
    room_name: str
    room: Room
    connections: List[RegionConnection]
    locations: List[LevelLocation]

    def __init__(self, name: str, room_name: str, connections: List[RegionConnection], locations: List[LevelLocation]):
        self.name = name
        self.room_name = room_name
        self.connections = deepcopy(connections)
        self.locations = deepcopy(locations)

        for loc in self.locations:
            loc.region = self


class RegionConnection:
    source_name: str
    source: PreRegion
    destination_name: str
    destination: PreRegion
    rule: Callable[[CollectionState], bool] = staticmethod(lambda state: True)

    # TODO: Assign the actual regions here after the structure is build

    def __init__(self, source_name: str, destination_name: str, possible_access: List[List[str]] = []):
        self.source_name = source_name
        self.destination_name = destination_name
        if (len(possible_access)):
            self.rule = lambda state: any(all(state.has(item) for item in sublist) for sublist in possible_access)


class LevelLocation:
    name: str
    display_name: str
    region_name: str
    region: PreRegion
    loc_type: LocationType
    rule: Callable[[CollectionState], bool] = staticmethod(lambda state: True)

    def __init__(self, name: str, display_name: str, region_name: str, loc_type: LocationType, possible_access: List[List[str]] = []):
        self.name = name
        self.display_name = display_name
        self.region_name = region_name
        self.loc_type = loc_type
        if (len(possible_access)):
            self.rule = lambda state: any(all(state.has(item) for item in sublist) for sublist in possible_access)

class Room:
    level_name: str
    name: str
    display_name: str
    regions: List[PreRegion]
    doors: List[Door]
    checkpoint: str

    def __init__(self, level_name: str, name: str, display_name: str, regions: List[PreRegion], doors: List[Door], checkpoint: str = None):
        self.level_name = level_name
        self.name = name
        self.display_name = display_name
        self.regions = deepcopy(regions)
        self.doors = deepcopy(doors)
        self.checkpoint = checkpoint

        from .data.TestLevelData import all_regions

        for reg in self.regions:
            reg.room = self

            for reg_con in reg.connections:
                reg_con.source = reg
                reg_con.destination = all_regions[reg_con.destination_name]

        for door in self.doors:
            door.room = self


class RoomConnection:
    level_name: str
    source: Door
    dest: Door
    two_way: bool

    def __init__(self, level_name: str, source: Door, dest: Door):
        self.level_name = level_name
        self.source = source
        self.dest = dest
        self.two_way = not self.dest.closes_behind


class Level:
    name: str
    display_name: str
    rooms: List[Room]
    room_connections: List[RoomConnection]

    def __init__(self, name: str, display_name: str, rooms: List[Room], room_connections: List[RoomConnection]):
        self.name = name
        self.display_name = display_name
        self.rooms = deepcopy(rooms)
        self.room_connections = deepcopy(room_connections)


def load_logic_data():
    from .data.TestLevelData import all_levels

    for _, level in all_levels.items():
        print(level.display_name)

        for room in level.rooms:
            print(" " + room.display_name)

            for region in room.regions:
                print("  " + region.name)

                for location in region.locations:
                    print("   " + location.display_name)


    return all_levels
