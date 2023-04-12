import os
import yaml

from typing import Dict, NamedTuple, Optional, List


class RoomAndDoor(NamedTuple):
    room: Optional[str]
    door: str


class RoomAndPanel(NamedTuple):
    room: Optional[str]
    panel: str


class RoomEntrance(NamedTuple):
    room: str  # source room
    doors: Optional[List[RoomAndDoor]]


class Room(NamedTuple):
    name: str
    entrances: List[RoomEntrance]


class Door(NamedTuple):
    name: str
    item_name: str
    location_name: Optional[str]
    panels: Optional[List[RoomAndPanel]]
    skip_location: bool
    skip_item: bool


class Panel(NamedTuple):
    required_rooms: List[str]
    required_doors: List[RoomAndDoor]
    colors: List[str]
    check: bool
    event: bool


class StaticLingoLogic:
    ROOMS: Dict[str, Room] = {}
    PANELS: Dict[str, Panel] = {}
    DOORS: Dict[str, Door] = {}

    ALL_ROOMS: List[Room] = []
    DOORS_BY_ROOM: Dict[str, Dict[str, Door]] = {}
    PANELS_BY_ROOM: Dict[str, Dict[str, Panel]] = {}

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "LL1.yaml")
        with open(path, 'r') as file:
            config = yaml.load(file, Loader=yaml.Loader)

            for room_name, room_data in config.items():
                room_obj = Room(room_name, [])

                if "entrances" in room_data:
                    for source_room, doors in room_data["entrances"].items():
                        if doors is True:
                            doors_list = None
                        elif isinstance(doors, Dict):
                            doors_list = list()
                            doors_list.append(RoomAndDoor(
                                doors["room"] if "room" in doors else None,
                                doors["door"]
                            ))
                        else:
                            doors_list = list()
                            for door in doors:
                                doors_list.append(RoomAndDoor(
                                    door["room"] if "room" in door else None,
                                    door["door"]
                                ))

                        room_obj.entrances.append(RoomEntrance(source_room, doors_list))

                if "panels" in room_data:
                    self.PANELS_BY_ROOM[room_name] = dict()

                    for panel_name, panel_data in room_data["panels"].items():
                        full_name = f"{room_name} - {panel_name}"

                        if "required_room" in panel_data:
                            if isinstance(panel_data["required_room"], List):
                                required_rooms = panel_data["required_room"]
                            else:
                                required_rooms = [panel_data["required_room"]]
                        else:
                            required_rooms = []

                        required_doors = list()
                        if "required_door" in panel_data:
                            if isinstance(panel_data["required_door"], Dict):
                                door = panel_data["required_door"]
                                required_doors.append(RoomAndDoor(
                                    door["room"] if "room" in door else None,
                                    door["door"]
                                ))
                            else:
                                for door in panel_data["required_door"]:
                                    required_doors.append(RoomAndDoor(
                                        door["room"] if "room" in door else None,
                                        door["door"]
                                    ))

                        if "colors" in panel_data:
                            if isinstance(panel_data["colors"], List):
                                colors = panel_data["colors"]
                            else:
                                colors = [panel_data["colors"]]
                        else:
                            colors = []

                        if "check" in panel_data:
                            check = panel_data["check"]
                        else:
                            check = False

                        if "event" in panel_data:
                            event = panel_data["event"]
                        else:
                            event = False

                        panel_obj = Panel(required_rooms, required_doors, colors, check, event)
                        self.PANELS[full_name] = panel_obj
                        self.PANELS_BY_ROOM[room_name][panel_name] = panel_obj

                if "doors" in room_data:
                    self.DOORS_BY_ROOM[room_name] = dict()

                    for door_name, door_data in room_data["doors"].items():
                        if "item_name" in door_data:
                            item_name = door_data["item_name"]
                        else:
                            item_name = f"{room_name} - {door_name}"

                        if "skip_location" in door_data:
                            skip_location = door_data["skip_location"]
                        else:
                            skip_location = False

                        if "skip_item" in door_data:
                            skip_item = door_data["skip_item"]
                        else:
                            skip_item = False

                        if "panels" in door_data:
                            panels = list()
                            for panel in door_data["panels"]:
                                if isinstance(panel, Dict):
                                    panels.append(RoomAndPanel(panel["room"], panel["panel"]))
                                else:
                                    panels.append(RoomAndPanel(None, panel))
                        else:
                            skip_location = True
                            panels = None

                        if "location_name" in door_data:
                            location_name = door_data["location_name"]
                        elif skip_location is False:
                            panel_per_room = dict()
                            for panel in panels:
                                panel_room_name = room_name if panel.room is None else panel.room
                                panel_per_room.setdefault(panel_room_name, []).append(panel.panel)

                            room_strs = list()
                            for door_room_str, door_panels_str in panel_per_room.items():
                                room_strs.append(door_room_str + " - " + ", ".join(door_panels_str))

                            location_name = " and ".join(room_strs)
                        else:
                            location_name = None

                        door_obj = Door(door_name, item_name, location_name, panels, skip_location, skip_item)

                        self.DOORS[door_obj.item_name] = door_obj
                        self.DOORS_BY_ROOM[room_name][door_name] = door_obj

                self.ROOMS[room_name] = room_obj
                self.ALL_ROOMS.append(room_obj)
