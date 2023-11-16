from typing import Dict, List, NamedTuple, Optional, Set

import Utils


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
    required_panels: List[RoomAndPanel]
    colors: List[str]
    check: bool
    event: bool
    internal_ids: List[str]
    exclude_reduce: bool
    achievement: bool
    non_counting: bool


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
    req_blocked: bool
    req_blocked_when_no_doors: bool


class Progression(NamedTuple):
    item_name: str
    index: int


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
PAINTING_EXIT_ROOMS: Set[str] = set()
PAINTING_EXITS: int = 0
REQUIRED_PAINTING_ROOMS: List[str] = []
REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS: List[str] = []

SPECIAL_ITEM_IDS: Dict[str, int] = {}
PANEL_LOCATION_IDS: Dict[str, Dict[str, int]] = {}
DOOR_LOCATION_IDS: Dict[str, Dict[str, int]] = {}
DOOR_ITEM_IDS: Dict[str, Dict[str, int]] = {}
DOOR_GROUP_ITEM_IDS: Dict[str, int] = {}
PROGRESSIVE_ITEM_IDS: Dict[str, int] = {}


def load_static_data():
    global PAINTING_EXITS, SPECIAL_ITEM_IDS, PANEL_LOCATION_IDS, DOOR_LOCATION_IDS, DOOR_ITEM_IDS, \
        DOOR_GROUP_ITEM_IDS, PROGRESSIVE_ITEM_IDS

    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    from . import data

    # Load in all item and location IDs. These are broken up into groups based on the type of item/location.
    with files(data).joinpath("ids.yaml").open() as file:
        config = Utils.parse_yaml(file)

        if "special_items" in config:
            for item_name, item_id in config["special_items"].items():
                SPECIAL_ITEM_IDS[item_name] = item_id

        if "panels" in config:
            for room_name in config["panels"].keys():
                PANEL_LOCATION_IDS[room_name] = {}

                for panel_name, location_id in config["panels"][room_name].items():
                    PANEL_LOCATION_IDS[room_name][panel_name] = location_id

        if "doors" in config:
            for room_name in config["doors"].keys():
                DOOR_LOCATION_IDS[room_name] = {}
                DOOR_ITEM_IDS[room_name] = {}

                for door_name, door_data in config["doors"][room_name].items():
                    if "location" in door_data:
                        DOOR_LOCATION_IDS[room_name][door_name] = door_data["location"]

                    if "item" in door_data:
                        DOOR_ITEM_IDS[room_name][door_name] = door_data["item"]

        if "door_groups" in config:
            for item_name, item_id in config["door_groups"].items():
                DOOR_GROUP_ITEM_IDS[item_name] = item_id

        if "progression" in config:
            for item_name, item_id in config["progression"].items():
                PROGRESSIVE_ITEM_IDS[item_name] = item_id

    # Process the main world file.
    with files(data).joinpath("LL1.yaml").open() as file:
        config = Utils.parse_yaml(file)

        for room_name, room_data in config.items():
            process_room(room_name, room_data)

        PAINTING_EXITS = len(PAINTING_EXIT_ROOMS)


def get_special_item_id(name: str):
    if name not in SPECIAL_ITEM_IDS:
        raise Exception(f"Item ID for special item {name} not found in ids.yaml.")

    return SPECIAL_ITEM_IDS[name]


def get_panel_location_id(room: str, name: str):
    if room not in PANEL_LOCATION_IDS or name not in PANEL_LOCATION_IDS[room]:
        raise Exception(f"Location ID for panel {room} - {name} not found in ids.yaml.")

    return PANEL_LOCATION_IDS[room][name]


def get_door_location_id(room: str, name: str):
    if room not in DOOR_LOCATION_IDS or name not in DOOR_LOCATION_IDS[room]:
        raise Exception(f"Location ID for door {room} - {name} not found in ids.yaml.")

    return DOOR_LOCATION_IDS[room][name]


def get_door_item_id(room: str, name: str):
    if room not in DOOR_ITEM_IDS or name not in DOOR_ITEM_IDS[room]:
        raise Exception(f"Item ID for door {room} - {name} not found in ids.yaml.")

    return DOOR_ITEM_IDS[room][name]


def get_door_group_item_id(name: str):
    if name not in DOOR_GROUP_ITEM_IDS:
        raise Exception(f"Item ID for door group {name} not found in ids.yaml.")

    return DOOR_GROUP_ITEM_IDS[name]


def get_progressive_item_id(name: str):
    if name not in PROGRESSIVE_ITEM_IDS:
        raise Exception(f"Item ID for progressive item {name} not found in ids.yaml.")

    return PROGRESSIVE_ITEM_IDS[name]


def process_entrance(source_room, doors, room_obj):
    global PAINTING_ENTRANCES, PAINTING_EXIT_ROOMS

    # If the value of an entrance is just True, that means that the entrance is always accessible.
    if doors is True:
        room_obj.entrances.append(RoomEntrance(source_room, None, False))
    elif isinstance(doors, dict):
        # If the value of an entrance is a dictionary, that means the entrance requires a door to be accessible, is a
        # painting-based entrance, or both.
        if "painting" in doors and "door" not in doors:
            PAINTING_EXIT_ROOMS.add(room_obj.name)
            PAINTING_ENTRANCES += 1

            room_obj.entrances.append(RoomEntrance(source_room, None, True))
        else:
            if "painting" in doors and doors["painting"]:
                PAINTING_EXIT_ROOMS.add(room_obj.name)
                PAINTING_ENTRANCES += 1

            room_obj.entrances.append(RoomEntrance(source_room, RoomAndDoor(
                doors["room"] if "room" in doors else None,
                doors["door"]
            ), doors["painting"] if "painting" in doors else False))
    else:
        # If the value of an entrance is a list, then there are multiple possible doors that can give access to the
        # entrance.
        for door in doors:
            if "painting" in door and door["painting"]:
                PAINTING_EXIT_ROOMS.add(room_obj.name)
                PAINTING_ENTRANCES += 1

            room_obj.entrances.append(RoomEntrance(source_room, RoomAndDoor(
                door["room"] if "room" in door else None,
                door["door"]
            ), door["painting"] if "painting" in door else False))


def process_panel(room_name, panel_name, panel_data):
    global PANELS, PANELS_BY_ROOM

    full_name = f"{room_name} - {panel_name}"

    # required_room can either be a single room or a list of rooms.
    if "required_room" in panel_data:
        if isinstance(panel_data["required_room"], list):
            required_rooms = panel_data["required_room"]
        else:
            required_rooms = [panel_data["required_room"]]
    else:
        required_rooms = []

    # required_door can either be a single door or a list of doors. For convenience, the room key for each door does not
    # need to be specified if the door is in this room.
    required_doors = list()
    if "required_door" in panel_data:
        if isinstance(panel_data["required_door"], dict):
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

    # required_panel can either be a single panel or a list of panels. For convenience, the room key for each panel does
    # not need to be specified if the panel is in this room.
    required_panels = list()
    if "required_panel" in panel_data:
        if isinstance(panel_data["required_panel"], dict):
            other_panel = panel_data["required_panel"]
            required_panels.append(RoomAndPanel(
                other_panel["room"] if "room" in other_panel else None,
                other_panel["panel"]
            ))
        else:
            for other_panel in panel_data["required_panel"]:
                required_panels.append(RoomAndPanel(
                    other_panel["room"] if "room" in other_panel else None,
                    other_panel["panel"]
                ))

    # colors can either be a single color or a list of colors.
    if "colors" in panel_data:
        if isinstance(panel_data["colors"], list):
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

    if "achievement" in panel_data:
        achievement = True
    else:
        achievement = False

    if "exclude_reduce" in panel_data:
        exclude_reduce = panel_data["exclude_reduce"]
    else:
        exclude_reduce = False

    if "non_counting" in panel_data:
        non_counting = panel_data["non_counting"]
    else:
        non_counting = False

    if "id" in panel_data:
        if isinstance(panel_data["id"], list):
            internal_ids = panel_data["id"]
        else:
            internal_ids = [panel_data["id"]]
    else:
        internal_ids = []

    panel_obj = Panel(required_rooms, required_doors, required_panels, colors, check, event, internal_ids,
                      exclude_reduce, achievement, non_counting)
    PANELS[full_name] = panel_obj
    PANELS_BY_ROOM[room_name][panel_name] = panel_obj


def process_door(room_name, door_name, door_data):
    global DOORS, DOORS_BY_ROOM

    # The item name associated with a door can be explicitly specified in the configuration. If it is not, it is
    # generated from the room and door name.
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

    # panels is a list of panels. Each panel can either be a simple string (the name of a panel in the current room) or
    # a dictionary specifying a panel in a different room.
    if "panels" in door_data:
        panels = list()
        for panel in door_data["panels"]:
            if isinstance(panel, dict):
                panels.append(RoomAndPanel(panel["room"], panel["panel"]))
            else:
                panels.append(RoomAndPanel(None, panel))
    else:
        skip_location = True
        panels = None

    # The location name associated with a door can be explicitly specified in the configuration. If it is not, then the
    # name is generated using a combination of all of the panels that would ordinarily open the door. This can get quite
    # messy if there are a lot of panels, especially if panels from multiple rooms are involved, so in these cases it
    # would be better to specify a name.
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

    # The id field can be a single item, or a list of door IDs, in the event that the item for this logical door should
    # open more than one actual in-game door.
    if "id" in door_data:
        if isinstance(door_data["id"], list):
            door_ids = door_data["id"]
        else:
            door_ids = [door_data["id"]]
    else:
        door_ids = []

    # The painting_id field can be a single item, or a list of painting IDs, in the event that the item for this logical
    # door should move more than one actual in-game painting.
    if "painting_id" in door_data:
        if isinstance(door_data["painting_id"], list):
            painting_ids = door_data["painting_id"]
        else:
            painting_ids = [door_data["painting_id"]]
    else:
        painting_ids = []

    door_obj = Door(door_name, item_name, location_name, panels, skip_location, skip_item, door_ids,
                    painting_ids, event, group, include_reduce, junk_item)

    DOORS[door_obj.item_name] = door_obj
    DOORS_BY_ROOM[room_name][door_name] = door_obj


def process_painting(room_name, painting_data):
    global PAINTINGS, PAINTINGS_BY_ROOM, REQUIRED_PAINTING_ROOMS, REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS

    # Read in information about this painting and store it in an object.
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
            REQUIRED_PAINTING_ROOMS.append(room_name)
    else:
        required_painting = False

    if "move" in painting_data:
        move_painting = painting_data["move"]
    else:
        move_painting = False

    if "required_when_no_doors" in painting_data:
        rwnd = painting_data["required_when_no_doors"]
        if rwnd:
            REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS.append(room_name)
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

    if "req_blocked" in painting_data:
        req_blocked = painting_data["req_blocked"]
    else:
        req_blocked = False

    if "req_blocked_when_no_doors" in painting_data:
        req_blocked_when_no_doors = painting_data["req_blocked_when_no_doors"]
    else:
        req_blocked_when_no_doors = False

    required_door = None
    if "required_door" in painting_data:
        door = painting_data["required_door"]
        required_door = RoomAndDoor(
            door["room"] if "room" in door else room_name,
            door["door"]
        )

    painting_obj = Painting(painting_id, room_name, enter_only, exit_only, orientation,
                            required_painting, rwnd, required_door, disable_painting, move_painting, req_blocked,
                            req_blocked_when_no_doors)
    PAINTINGS[painting_id] = painting_obj
    PAINTINGS_BY_ROOM[room_name].append(painting_obj)


def process_progression(room_name, progression_name, progression_doors):
    global PROGRESSIVE_ITEMS, PROGRESSION_BY_ROOM

    # Progressive items are configured as a list of doors.
    PROGRESSIVE_ITEMS.append(progression_name)

    progression_index = 1
    for door in progression_doors:
        if isinstance(door, Dict):
            door_room = door["room"]
            door_door = door["door"]
        else:
            door_room = room_name
            door_door = door

        room_progressions = PROGRESSION_BY_ROOM.setdefault(door_room, {})
        room_progressions[door_door] = Progression(progression_name, progression_index)
        progression_index += 1


def process_room(room_name, room_data):
    global ROOMS, ALL_ROOMS

    room_obj = Room(room_name, [])

    if "entrances" in room_data:
        for source_room, doors in room_data["entrances"].items():
            process_entrance(source_room, doors, room_obj)

    if "panels" in room_data:
        PANELS_BY_ROOM[room_name] = dict()

        for panel_name, panel_data in room_data["panels"].items():
            process_panel(room_name, panel_name, panel_data)

    if "doors" in room_data:
        DOORS_BY_ROOM[room_name] = dict()

        for door_name, door_data in room_data["doors"].items():
            process_door(room_name, door_name, door_data)

    if "paintings" in room_data:
        PAINTINGS_BY_ROOM[room_name] = []

        for painting_data in room_data["paintings"]:
            process_painting(room_name, painting_data)

    if "progression" in room_data:
        for progression_name, progression_doors in room_data["progression"].items():
            process_progression(room_name, progression_name, progression_doors)

    ROOMS[room_name] = room_obj
    ALL_ROOMS.append(room_obj)


# Initialize the static data at module scope.
load_static_data()
