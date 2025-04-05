from __future__ import annotations
from copy import deepcopy
from enum import IntEnum

from BaseClasses import CollectionState


class LocationType(IntEnum):
    strawberry = 0
    golden_strawberry = 1
    cassette = 2
    crystal_heart = 3
    checkpoint = 4
    level_clear = 5
    key = 6
    binoculars = 7
    room_enter = 8
    clutter = 9

class DoorDirection(IntEnum):
    up = 0
    right = 1
    down = 2
    left = 3
    special = 4


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
    connections: list[RegionConnection]
    locations: list[LevelLocation]

    def __init__(self, name: str, room_name: str, connections: list[RegionConnection], locations: list[LevelLocation]):
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
    possible_access: list[list[str]]

    # TODO: Assign the actual regions here after the structure is built

    def __init__(self, source_name: str, destination_name: str, possible_access: list[list[str]] = []):
        self.source_name = source_name
        self.destination_name = destination_name
        self.possible_access = deepcopy(possible_access)


class LevelLocation:
    name: str
    display_name: str
    region_name: str
    region: PreRegion
    loc_type: LocationType
    possible_access: list[list[str]]

    def __init__(self, name: str, display_name: str, region_name: str, loc_type: LocationType, possible_access: list[list[str]] = []):
        self.name = name
        self.display_name = display_name
        self.region_name = region_name
        self.loc_type = loc_type
        self.possible_access = deepcopy(possible_access)

class Room:
    level_name: str
    name: str
    display_name: str
    regions: list[PreRegion]
    doors: list[Door]
    checkpoint: str
    checkpoint_region: str

    def __init__(self, level_name: str, name: str, display_name: str, regions: list[PreRegion], doors: list[Door], checkpoint: str = None, checkpoint_region: str = None):
        self.level_name = level_name
        self.name = name
        self.display_name = display_name
        self.regions = deepcopy(regions)
        self.doors = deepcopy(doors)
        self.checkpoint = checkpoint
        self.checkpoint_region = checkpoint_region

        from .data.CelesteLevelData import all_regions

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

        if (self.source.dir == DoorDirection.left and self.dest.dir != DoorDirection.right or
            self.source.dir == DoorDirection.right and self.dest.dir != DoorDirection.left or
            self.source.dir == DoorDirection.up and self.dest.dir != DoorDirection.down or
            self.source.dir == DoorDirection.down and self.dest.dir != DoorDirection.up):
            raise Exception(f"Door {source.name} ({self.source.dir}) and Door {dest.name} ({self.dest.dir}) have mismatched directions.")


class Level:
    name: str
    display_name: str
    rooms: list[Room]
    room_connections: list[RoomConnection]

    def __init__(self, name: str, display_name: str, rooms: list[Room], room_connections: list[RoomConnection]):
        self.name = name
        self.display_name = display_name
        self.rooms = deepcopy(rooms)
        self.room_connections = deepcopy(room_connections)


def load_logic_data() -> dict[str, Level]:
    from .data.CelesteLevelData import all_levels

    #for _, level in all_levels.items():
    #    print(level.display_name)
    #
    #    for room in level.rooms:
    #        print(" " + room.display_name)
    #
    #        for region in room.regions:
    #            print("  " + region.name)
    #
    #            for location in region.locations:
    #                print("   " + location.display_name)

    return all_levels
