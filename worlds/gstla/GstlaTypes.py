from typing import List, Dict, Optional, TYPE_CHECKING
from BaseClasses import Region, EntranceType, MultiWorld, Entrance
from enum import IntEnum

class RegionData:
    name: str
    locations: List[str]
    exits: List[str]
    gs_name: str
    gs_id: int

    def __init__(self, _name: str, _locations: List[str] = None, _exits: List[str] = None, _gs_name: str = None, _gs_id: int = None):
        if _locations is None:
            _locations = []

        if _exits is None:
            _exits = []

        if _gs_name is None:
            _gs_name = _name

        self.name = _name
        self.locations = _locations
        self.exits = _exits
        self.gs_name = _gs_name
        self.gs_id = _gs_id


class ERTestGroups(IntEnum):
    #Overworld
    WALK = 1
    SHIP = 2

    #Dungeon/Village
    SCREEN_EDGE = 3
    DOOR = 4
    RISE = 5
    FALL = 6
    LADDER = 7
    TELEPORT = 8
    CYCLONE = 9


directionally_matched_group_lookup = {
    ERTestGroups.WALK: [ERTestGroups.WALK],
    ERTestGroups.SHIP: [ERTestGroups.SHIP],
    ERTestGroups.SCREEN_EDGE: [ERTestGroups.SCREEN_EDGE, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.DOOR: [ERTestGroups.SCREEN_EDGE, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.RISE: [ERTestGroups.SCREEN_EDGE, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.FALL: [ERTestGroups.SCREEN_EDGE, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.LADDER: [ERTestGroups.SCREEN_EDGE, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.TELEPORT: [ERTestGroups.SCREEN_EDGE, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE],
    ERTestGroups.CYCLONE: [ERTestGroups.SCREEN_EDGE, ERTestGroups.DOOR, ERTestGroups.RISE, ERTestGroups.FALL,ERTestGroups.LADDER,ERTestGroups.TELEPORT,ERTestGroups.CYCLONE]
}

class EntranceData:
    source_entrance: str
    target: str
    gs_id: int
    rando_group: int
    rando_type: EntranceType

    def __init__(self, _source_entrance: str, _target: str, _gs_id: int = None, _ap_rando_group: int = 0, _ap_rando_type: EntranceType = EntranceType.TWO_WAY ):
        self.source_entrance = _source_entrance
        self.target = _target
        self.gs_id = _gs_id
        self.rando_group = _ap_rando_group
        self.rando_type = _ap_rando_type