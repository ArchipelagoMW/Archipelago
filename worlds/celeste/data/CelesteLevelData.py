from typing import Dict, List
from ..Levels import Level, Room, PreRegion, LevelLocation, RegionConnection, RoomConnection, Door, DoorDirection, LocationType

all_doors: Dict[str, Door] = {
    "0a_-1_east": Door("0a_-1_east", "0a_-1", DoorDirection.right, False, False),

    "0a_0_west": Door("0a_0_west", "0a_0", DoorDirection.left, False, False),
    "0a_0_east": Door("0a_0_east", "0a_0", DoorDirection.right, False, False),
    "0a_0_north": Door("0a_0_north", "0a_0", DoorDirection.up, False, False),

    "0a_0b_south": Door("0a_0b_south", "0a_0b", DoorDirection.down, False, False),

    "0a_1_west": Door("0a_1_west", "0a_1", DoorDirection.left, False, False),
    "0a_1_east": Door("0a_1_east", "0a_1", DoorDirection.right, False, False),

    "0a_2_west": Door("0a_2_west", "0a_2", DoorDirection.left, False, False),
    "0a_2_east": Door("0a_2_east", "0a_2", DoorDirection.right, False, False),

    "0a_3_west": Door("0a_3_west", "0a_3", DoorDirection.left, False, False),

}

all_region_connections: Dict[str, RegionConnection] = {
    "0a_-1_main---0a_-1_east": RegionConnection("0a_-1_main", "0a_-1_east", []),
    "0a_-1_east---0a_-1_main": RegionConnection("0a_-1_east", "0a_-1_main", []),

    "0a_0_west---0a_0_main": RegionConnection("0a_0_west", "0a_0_main", []),
    "0a_0_main---0a_0_west": RegionConnection("0a_0_main", "0a_0_west", []),
    "0a_0_main---0a_0_east": RegionConnection("0a_0_main", "0a_0_east", []),
    "0a_0_main---0a_0_north": RegionConnection("0a_0_main", "0a_0_north", []),
    "0a_0_north---0a_0_main": RegionConnection("0a_0_north", "0a_0_main", []),
    "0a_0_east---0a_0_main": RegionConnection("0a_0_east", "0a_0_main", []),


    "0a_1_west---0a_1_main": RegionConnection("0a_1_west", "0a_1_main", []),
    "0a_1_main---0a_1_west": RegionConnection("0a_1_main", "0a_1_west", []),
    "0a_1_main---0a_1_east": RegionConnection("0a_1_main", "0a_1_east", []),
    "0a_1_east---0a_1_main": RegionConnection("0a_1_east", "0a_1_main", []),

    "0a_2_west---0a_2_main": RegionConnection("0a_2_west", "0a_2_main", []),
    "0a_2_main---0a_2_west": RegionConnection("0a_2_main", "0a_2_west", []),
    "0a_2_main---0a_2_east": RegionConnection("0a_2_main", "0a_2_east", []),
    "0a_2_east---0a_2_main": RegionConnection("0a_2_east", "0a_2_main", []),

    "0a_3_west---0a_3_main": RegionConnection("0a_3_west", "0a_3_main", []),
    "0a_3_main---0a_3_west": RegionConnection("0a_3_main", "0a_3_west", []),
    "0a_3_main---0a_3_east": RegionConnection("0a_3_main", "0a_3_east", []),
    "0a_3_east---0a_3_main": RegionConnection("0a_3_east", "0a_3_main", []),

}

all_locations: Dict[str, LevelLocation] = {
    "0a_3_clear": LevelLocation("0a_3_clear", "Prologue - Level Clear", "0a_3_east", LocationType.level_clear, []),

}

all_regions: Dict[str, PreRegion] = {
    "0a_-1_main": PreRegion("0a_-1_main", "0a_-1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_-1_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_-1_main"]),
    "0a_-1_east": PreRegion("0a_-1_east", "0a_-1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_-1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_-1_east"]),

    "0a_0_west": PreRegion("0a_0_west", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_west"]),
    "0a_0_main": PreRegion("0a_0_main", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_main"]),
    "0a_0_north": PreRegion("0a_0_north", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_north"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_north"]),
    "0a_0_east": PreRegion("0a_0_east", "0a_0", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0_east"]),

    "0a_0b_south": PreRegion("0a_0b_south", "0a_0b", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_0b_south"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_0b_south"]),

    "0a_1_west": PreRegion("0a_1_west", "0a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_1_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_1_west"]),
    "0a_1_main": PreRegion("0a_1_main", "0a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_1_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_1_main"]),
    "0a_1_east": PreRegion("0a_1_east", "0a_1", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_1_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_1_east"]),

    "0a_2_west": PreRegion("0a_2_west", "0a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_2_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_2_west"]),
    "0a_2_main": PreRegion("0a_2_main", "0a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_2_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_2_main"]),
    "0a_2_east": PreRegion("0a_2_east", "0a_2", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_2_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_2_east"]),

    "0a_3_west": PreRegion("0a_3_west", "0a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_3_west"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_3_west"]),
    "0a_3_main": PreRegion("0a_3_main", "0a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_3_main"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_3_main"]),
    "0a_3_east": PreRegion("0a_3_east", "0a_3", [reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == "0a_3_east"], [loc for _, loc in all_locations.items() if loc.region_name == "0a_3_east"]),

}

all_room_connections: Dict[str, RoomConnection] = {
    "0a_-1---0a_0": RoomConnection("0a", all_doors["0a_-1_east"], all_doors["0a_0_west"]),
    "0a_0---0a_0b": RoomConnection("0a", all_doors["0a_0_north"], all_doors["0a_0b_south"]),
    "0a_0---0a_1": RoomConnection("0a", all_doors["0a_0_east"], all_doors["0a_1_west"]),
    "0a_1---0a_2": RoomConnection("0a", all_doors["0a_1_east"], all_doors["0a_2_west"]),
    "0a_2---0a_3": RoomConnection("0a", all_doors["0a_2_east"], all_doors["0a_3_west"]),

}

all_rooms: Dict[str, Room] = {
    "0a_-1": Room("0a", "0a_-1", "Prologue - Room -1", [reg for _, reg in all_regions.items() if reg.room_name == "0a_-1"], [door for _, door in all_doors.items() if door.room_name == "0a_-1"]),
    "0a_0": Room("0a", "0a_0", "Prologue - Room 0", [reg for _, reg in all_regions.items() if reg.room_name == "0a_0"], [door for _, door in all_doors.items() if door.room_name == "0a_0"], "Start", "0a_0_west"),
    "0a_0b": Room("0a", "0a_0b", "Prologue - Room 0b", [reg for _, reg in all_regions.items() if reg.room_name == "0a_0b"], [door for _, door in all_doors.items() if door.room_name == "0a_0b"]),
    "0a_1": Room("0a", "0a_1", "Prologue - Room 1", [reg for _, reg in all_regions.items() if reg.room_name == "0a_1"], [door for _, door in all_doors.items() if door.room_name == "0a_1"]),
    "0a_2": Room("0a", "0a_2", "Prologue - Room 2", [reg for _, reg in all_regions.items() if reg.room_name == "0a_2"], [door for _, door in all_doors.items() if door.room_name == "0a_2"]),
    "0a_3": Room("0a", "0a_3", "Prologue - Room 3", [reg for _, reg in all_regions.items() if reg.room_name == "0a_3"], [door for _, door in all_doors.items() if door.room_name == "0a_3"]),

}

all_levels: Dict[str, Level] = {
    "0a": Level("0a", "Prologue", [room for _, room in all_rooms.items() if room.level_name == "0a"], [room_con for _, room_con in all_room_connections.items() if room_con.level_name == "0a"]),

}

