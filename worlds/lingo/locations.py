from typing import Dict, NamedTuple, List
from types import MappingProxyType
from BaseClasses import Location
from .static_logic import StaticLingoLogic, RoomAndPanel
from enum import Flag, auto


class LocationClassification(Flag):
    normal = auto()
    reduced = auto()
    insanity = auto()


class LocationData(NamedTuple):
    """
    LocationData for a location in Lingo
    """
    code: int
    room: str
    panels: List[RoomAndPanel]
    classification: LocationClassification

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

    ALL_LOCATION_TABLE: MappingProxyType[str, LocationData]

    def __init__(self, static_logic: StaticLingoLogic):
        temp_location_table: Dict[str, LocationData] = {}

        for room_name, panels in static_logic.PANELS_BY_ROOM.items():
            for panel_name, panel in panels.items():
                locat_name = f"{room_name} - {panel_name}"

                classification = LocationClassification.insanity
                if panel.check:
                    classification |= LocationClassification.normal

                    if not panel.exclude_reduce:
                        classification |= LocationClassification.reduced

                temp_location_table[locat_name] =\
                    LocationData(static_logic.get_panel_location_id(room_name, panel_name), room_name,
                                 [RoomAndPanel(None, panel_name)], classification)

        for room_name, doors in static_logic.DOORS_BY_ROOM.items():
            for door_name, door in doors.items():
                if door.skip_location or door.event or door.panels is None:
                    continue
                
                locat_name = door.location_name
                classification = LocationClassification.normal
                if door.include_reduce:
                    classification |= LocationClassification.reduced

                if locat_name in temp_location_table:
                    new_id = temp_location_table[locat_name].code
                    classification |= temp_location_table[locat_name].classification
                else:
                    new_id = static_logic.get_door_location_id(room_name, door_name)

                temp_location_table[locat_name] = LocationData(new_id, room_name, door.panels, classification)

        self.ALL_LOCATION_TABLE = MappingProxyType(temp_location_table)
