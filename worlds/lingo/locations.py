from typing import Dict, NamedTuple, Optional, List
from BaseClasses import Location
from .static_logic import StaticLingoLogic, RoomAndPanel, Room


class LocationData(NamedTuple):
    """
    LocationData for a location in Lingo
    """
    code: Optional[int]
    room: str
    panels: List[RoomAndPanel]
    include_reduce: bool

    def panel_ids(self):
        ids = set()
        for panel in self.panels:
            effective_room = self.room if panel.room is None else panel.room
            panel_data = StaticLingoLogic.PANELS_BY_ROOM[effective_room][panel.panel]
            ids = ids | set(panel_data.internal_ids)
        return ids


class LingoLocation(Location):
    """
    Location from the game Lingo
    """
    game: str = "Lingo"


class StaticLingoLocations:
    """
    Defines the locations that can be included in a Lingo world
    """

    base_id: int = 0

    ALL_LOCATION_TABLE: Dict[str, LocationData] = {}

    def create_location(self, name: str, event: bool, room: str, panels: List[RoomAndPanel], include_reduce: bool):
        new_id = None if event is True else self.base_id + len(self.ALL_LOCATION_TABLE)
        new_locat = LocationData(new_id, room, panels, include_reduce)
        self.ALL_LOCATION_TABLE[name] = new_locat

    def __init__(self, base_id):
        self.base_id = base_id

        for room_name, panels in StaticLingoLogic.PANELS_BY_ROOM.items():
            for panel_name, panel in panels.items():
                locat_name = f"{room_name} - {panel_name}"
                if panel.check:
                    self.create_location(locat_name, False, room_name, [RoomAndPanel(None, panel_name)],
                                         not panel.exclude_reduce)
                elif panel.event:
                    self.create_location(locat_name, True, room_name, [RoomAndPanel(None, panel_name)], True)

        for room_name, doors in StaticLingoLogic.DOORS_BY_ROOM.items():
            for door_name, door in doors.items():
                if door.skip_location or door.event or door.panels is None:
                    continue
                
                locat_name = door.location_name
                self.create_location(locat_name, False, room_name, door.panels, door.include_reduce)
