from enum import Flag, auto
from typing import Dict, List, NamedTuple

from BaseClasses import Location
from .static_logic import DOORS_BY_ROOM, PANELS_BY_ROOM, RoomAndPanel, get_door_location_id, get_panel_location_id


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
            panel_data = PANELS_BY_ROOM[effective_room][panel.panel]
            ids = ids | set(panel_data.internal_ids)
        return ids


class LingoLocation(Location):
    """
    Location from the game Lingo
    """
    game: str = "Lingo"


ALL_LOCATION_TABLE: Dict[str, LocationData] = {}


def load_location_data():
    global ALL_LOCATION_TABLE

    for room_name, panels in PANELS_BY_ROOM.items():
        for panel_name, panel in panels.items():
            location_name = f"{room_name} - {panel_name}"

            classification = LocationClassification.insanity
            if panel.check:
                classification |= LocationClassification.normal

                if not panel.exclude_reduce:
                    classification |= LocationClassification.reduced

            ALL_LOCATION_TABLE[location_name] = \
                LocationData(get_panel_location_id(room_name, panel_name), room_name,
                             [RoomAndPanel(None, panel_name)], classification)

    for room_name, doors in DOORS_BY_ROOM.items():
        for door_name, door in doors.items():
            if door.skip_location or door.event or door.panels is None:
                continue

            location_name = door.location_name
            classification = LocationClassification.normal
            if door.include_reduce:
                classification |= LocationClassification.reduced

            if location_name in ALL_LOCATION_TABLE:
                new_id = ALL_LOCATION_TABLE[location_name].code
                classification |= ALL_LOCATION_TABLE[location_name].classification
            else:
                new_id = get_door_location_id(room_name, door_name)

            ALL_LOCATION_TABLE[location_name] = LocationData(new_id, room_name, door.panels, classification)


# Initialize location data on the module scope.
load_location_data()
