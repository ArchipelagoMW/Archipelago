from typing import Dict, NamedTuple, Optional
from BaseClasses import Location
from .static_logic import StaticLingoLogic, RoomAndPanel, Room


class LocationData(NamedTuple):
    """
    LocationData for a location in Lingo
    """
    code: Optional[int]
    room: str
    panels: list[RoomAndPanel]


class LingoLocation(Location):
    """
    Location from the game Lingo
    """
    game: str = "Lingo"


class StaticLingoLocations:
    """
    Defines the locations that can be included in a Lingo world
    """

    ALL_LOCATION_TABLE: Dict[str, LocationData] = {}

    def __init__(self, base_id):
        location_tab = dict()

        for room_name, panels in StaticLingoLogic.PANELS_BY_ROOM.items():
            for panel_name, panel in panels.items():
                locat_name = room_name + " - " + panel_name
                if panel.check:
                    location_tab[locat_name] = \
                        LocationData(base_id + len(location_tab), room_name, [RoomAndPanel(None, panel_name)])
                elif panel.event:
                    location_tab[locat_name] = \
                        LocationData(None, room_name, [RoomAndPanel(None, panel_name)])

        for room_name, doors in StaticLingoLogic.DOORS_BY_ROOM.items():
            for door_name, door in doors.items():
                #event_locat_name = room_name + " - " + door_name + " (Door)"
                #location_tab[event_locat_name] = LocationData(None, room_name, door.panels)

                if door.skip_location or door.panels is None:
                    continue
                
                locat_name = door.location_name
                location_tab[locat_name] = LocationData(base_id + len(location_tab), room_name, door.panels)
        
        for key, locat in location_tab.items():
            self.ALL_LOCATION_TABLE[key] = locat
