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
    door: Optional[RoomAndDoor]
    painting: bool


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
    door_ids: List[str]
    painting_ids: List[str]
    event: bool
    group: Optional[str]
    include_reduce: bool
    junk_item: bool


class Panel(NamedTuple):
    required_rooms: List[str]
    required_doors: List[RoomAndDoor]
    colors: List[str]
    check: bool
    event: bool
    internal_ids: List[str]
    exclude_reduce: bool


class Painting(NamedTuple):
    id: str
    room: str
    enter_only: bool
    exit_only: bool
    orientation: str
    required: bool
    required_when_no_doors: bool
    required_door: Optional[RoomAndDoor]
    disable: bool
    move: bool


class Progression(NamedTuple):
    item_name: str
    index: int


class StaticLingoLogic:
    ROOMS: Dict[str, Room] = {}
    PANELS: Dict[str, Panel] = {}
    DOORS: Dict[str, Door] = {}
    PAINTINGS: Dict[str, Painting] = {}

    ALL_ROOMS: List[Room] = []
    DOORS_BY_ROOM: Dict[str, Dict[str, Door]] = {}
    PANELS_BY_ROOM: Dict[str, Dict[str, Panel]] = {}
    PAINTINGS_BY_ROOM: Dict[str, List[Painting]] = {}

    PROGRESSIVE_ITEMS: List[str] = []
    PROGRESSION_BY_ROOM: Dict[str, Dict[str, Progression]] = {}

    PAINTING_ENTRANCES: int = 0
    PAINTING_EXITS: int = 0
    REQUIRED_PAINTING_ROOMS: List[str] = []
    REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS: List[str] = []

    def __init__(self):
        try:
            from importlib.resources import files
        except ImportError:
            from importlib_resources import files

        with files("worlds.lingo").joinpath("LL1.yaml").open() as file:
            config = yaml.load(file, Loader=yaml.Loader)

            for room_name, room_data in config.items():
                room_obj = Room(room_name, [])

                if "entrances" in room_data:
                    is_painting_exit = False

                    for source_room, doors in room_data["entrances"].items():
                        if doors is True:
                            room_obj.entrances.append(RoomEntrance(source_room, None, False))
                        elif isinstance(doors, Dict):
                            if "painting" in doors and "door" not in doors:
                                is_painting_exit = True
                                self.PAINTING_ENTRANCES += 1

                                room_obj.entrances.append(RoomEntrance(source_room, None, True))
                            else:
                                if "painting" in doors and doors["painting"]:
                                    is_painting_exit = True
                                    self.PAINTING_ENTRANCES += 1

                                room_obj.entrances.append(RoomEntrance(source_room, RoomAndDoor(
                                    doors["room"] if "room" in doors else None,
                                    doors["door"]
                                ), doors["painting"] if "painting" in doors else False))
                        else:
                            for door in doors:
                                if "painting" in door and door["painting"]:
                                    is_painting_exit = True
                                    self.PAINTING_ENTRANCES += 1

                                room_obj.entrances.append(RoomEntrance(source_room, RoomAndDoor(
                                    door["room"] if "room" in door else None,
                                    door["door"]
                                ), door["painting"] if "painting" in door else False))

                    if is_painting_exit:
                        self.PAINTING_EXITS += 1

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

                        if "exclude_reduce" in panel_data:
                            exclude_reduce = panel_data["exclude_reduce"]
                        else:
                            exclude_reduce = False

                        if "id" in panel_data:
                            if isinstance(panel_data["id"], List):
                                internal_ids = panel_data["id"]
                            else:
                                internal_ids = [panel_data["id"]]
                        else:
                            internal_ids = []

                        panel_obj = Panel(required_rooms, required_doors, colors, check, event, internal_ids,
                                          exclude_reduce)
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

                        if "event" in door_data:
                            event = door_data["event"]
                        else:
                            event = False

                        if "include_reduce" in door_data:
                            include_reduce = door_data["include_reduce"]
                        else:
                            include_reduce = False

                        if "junk_item" in door_data:
                            junk_item = door_data["junk_item"]
                        else:
                            junk_item = False

                        if "group" in door_data:
                            group = door_data["group"]
                        else:
                            group = None

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

                        if "id" in door_data:
                            if isinstance(door_data["id"], List):
                                door_ids = door_data["id"]
                            else:
                                door_ids = [door_data["id"]]
                        else:
                            door_ids = []

                        if "painting_id" in door_data:
                            if isinstance(door_data["painting_id"], List):
                                painting_ids = door_data["painting_id"]
                            else:
                                painting_ids = [door_data["painting_id"]]
                        else:
                            painting_ids = []

                        door_obj = Door(door_name, item_name, location_name, panels, skip_location, skip_item, door_ids,
                                        painting_ids, event, group, include_reduce, junk_item)

                        self.DOORS[door_obj.item_name] = door_obj
                        self.DOORS_BY_ROOM[room_name][door_name] = door_obj

                if "paintings" in room_data:
                    self.PAINTINGS_BY_ROOM[room_name] = []

                    for painting_data in room_data["paintings"]:
                        painting_id = painting_data["id"]

                        if "orientation" in painting_data:
                            orientation = painting_data["orientation"]
                        else:
                            orientation = ""

                        if "disable" in painting_data:
                            disable_painting = painting_data["disable"]
                        else:
                            disable_painting = False

                        if "required" in painting_data:
                            required_painting = painting_data["required"]
                            if required_painting:
                                self.REQUIRED_PAINTING_ROOMS.append(room_name)
                        else:
                            required_painting = False

                        if "move" in painting_data:
                            move_painting = painting_data["move"]
                        else:
                            move_painting = False

                        if "required_when_no_doors" in painting_data:
                            rwnd = painting_data["required_when_no_doors"]
                            if rwnd:
                                self.REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS.append(room_name)
                        else:
                            rwnd = False

                        if "exit_only" in painting_data:
                            exit_only = painting_data["exit_only"]
                        else:
                            exit_only = False

                        if "enter_only" in painting_data:
                            enter_only = painting_data["enter_only"]
                        else:
                            enter_only = False

                        required_door = None
                        if "required_door" in painting_data:
                            door = painting_data["required_door"]
                            required_door = RoomAndDoor(
                                door["room"] if "room" in door else room_name,
                                door["door"]
                            )

                        painting_obj = Painting(painting_id, room_name, enter_only, exit_only, orientation,
                                                required_painting, rwnd, required_door, disable_painting, move_painting)
                        self.PAINTINGS[painting_id] = painting_obj
                        self.PAINTINGS_BY_ROOM[room_name].append(painting_obj)

                if "progression" in room_data:
                    for progression_name, progression_doors in room_data["progression"].items():
                        self.PROGRESSIVE_ITEMS.append(progression_name)

                        progression_index = 1
                        for door in progression_doors:
                            if isinstance(door, Dict):
                                door_room = door["room"]
                                door_door = door["door"]
                            else:
                                door_room = room_name
                                door_door = door

                            room_progressions = self.PROGRESSION_BY_ROOM.setdefault(door_room, {})
                            room_progressions[door_door] = Progression(progression_name, progression_index)
                            progression_index += 1

                self.ROOMS[room_name] = room_obj
                self.ALL_ROOMS.append(room_obj)
