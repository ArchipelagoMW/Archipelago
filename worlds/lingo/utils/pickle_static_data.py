from typing import Dict, List, Set

import os
import sys

sys.path.append(os.path.join("worlds", "lingo"))
sys.path.append(".")
sys.path.append("..")
from datatypes import Door, Painting, Panel, Progression, Room, RoomAndDoor, RoomAndPanel, RoomEntrance

import hashlib
import pickle
import sys
import Utils


ALL_ROOMS: List[Room] = []
DOORS_BY_ROOM: Dict[str, Dict[str, Door]] = {}
PANELS_BY_ROOM: Dict[str, Dict[str, Panel]] = {}
PAINTINGS: Dict[str, Painting] = {}

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


def hash_file(path):
    md5 = hashlib.md5()
    
    with open(path, 'rb') as f:
        content = f.read()
        content = content.replace(b'\r\n', b'\n')
        md5.update(content)
    
    return md5.hexdigest()


def load_static_data(ll1_path, ids_path):
    global PAINTING_EXITS, SPECIAL_ITEM_IDS, PANEL_LOCATION_IDS, DOOR_LOCATION_IDS, DOOR_ITEM_IDS, \
        DOOR_GROUP_ITEM_IDS, PROGRESSIVE_ITEM_IDS

    # Load in all item and location IDs. These are broken up into groups based on the type of item/location.
    with open(ids_path, "r") as file:
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
    with open(ll1_path, "r") as file:
        config = Utils.parse_yaml(file)

        for room_name, room_data in config.items():
            process_room(room_name, room_data)

        PAINTING_EXITS = len(PAINTING_EXIT_ROOMS)


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
    global PANELS_BY_ROOM

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

    panel_obj = Panel(required_rooms, required_doors, required_panels, colors, check, event, exclude_reduce,
                      achievement, non_counting)
    PANELS_BY_ROOM[room_name][panel_name] = panel_obj


def process_door(room_name, door_name, door_data):
    global DOORS_BY_ROOM

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

    if "door_group" in door_data:
        door_group = door_data["door_group"]
    else:
        door_group = None

    if "item_group" in door_data:
        item_group = door_data["item_group"]
    else:
        item_group = None

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
    has_doors = "id" in door_data

    # The painting_id field can be a single item, or a list of painting IDs, in the event that the item for this logical
    # door should move more than one actual in-game painting.
    if "painting_id" in door_data:
        if isinstance(door_data["painting_id"], list):
            painting_ids = door_data["painting_id"]
        else:
            painting_ids = [door_data["painting_id"]]
    else:
        painting_ids = []

    door_obj = Door(door_name, item_name, location_name, panels, skip_location, skip_item, has_doors,
                    painting_ids, event, door_group, include_reduce, junk_item, item_group)

    DOORS_BY_ROOM[room_name][door_name] = door_obj


def process_painting(room_name, painting_data):
    global PAINTINGS, REQUIRED_PAINTING_ROOMS, REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS

    # Read in information about this painting and store it in an object.
    painting_id = painting_data["id"]

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

    painting_obj = Painting(painting_id, room_name, enter_only, exit_only,
                            required_painting, rwnd, required_door, disable_painting, req_blocked,
                            req_blocked_when_no_doors)
    PAINTINGS[painting_id] = painting_obj


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
    global ALL_ROOMS

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
        for painting_data in room_data["paintings"]:
            process_painting(room_name, painting_data)

    if "progression" in room_data:
        for progression_name, progression_doors in room_data["progression"].items():
            process_progression(room_name, progression_name, progression_doors)

    ALL_ROOMS.append(room_obj)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        ll1_path = os.path.join("worlds", "lingo", "data", "LL1.yaml")
        ids_path = os.path.join("worlds", "lingo", "data", "ids.yaml")
        output_path = os.path.join("worlds", "lingo", "data", "generated.dat")
    elif len(sys.argv) != 4:
        print("")
        print("Usage: python worlds/lingo/utils/pickle_static_data.py [args]")
        print("Arguments:")
        print(" - Path to LL1.yaml")
        print(" - Path to ids.yaml")
        print(" - Path to output file")
        
        exit()
    else:
        ll1_path = sys.argv[1]
        ids_path = sys.argv[2]
        output_path = sys.argv[3]
        
    load_static_data(ll1_path, ids_path)
    
    hashes = {
        "LL1.yaml": hash_file(ll1_path),
        "ids.yaml": hash_file(ids_path),
    }
    
    pickdata = {
        "HASHES": hashes,
        "PAINTINGS": PAINTINGS,
        "ALL_ROOMS": ALL_ROOMS,
        "DOORS_BY_ROOM": DOORS_BY_ROOM,
        "PANELS_BY_ROOM": PANELS_BY_ROOM,
        "PROGRESSIVE_ITEMS": PROGRESSIVE_ITEMS,
        "PROGRESSION_BY_ROOM": PROGRESSION_BY_ROOM,
        "PAINTING_ENTRANCES": PAINTING_ENTRANCES,
        "PAINTING_EXIT_ROOMS": PAINTING_EXIT_ROOMS,
        "PAINTING_EXITS": PAINTING_EXITS,
        "REQUIRED_PAINTING_ROOMS": REQUIRED_PAINTING_ROOMS,
        "REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS": REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS,
        "SPECIAL_ITEM_IDS": SPECIAL_ITEM_IDS,
        "PANEL_LOCATION_IDS": PANEL_LOCATION_IDS,
        "DOOR_LOCATION_IDS": DOOR_LOCATION_IDS,
        "DOOR_ITEM_IDS": DOOR_ITEM_IDS,
        "DOOR_GROUP_ITEM_IDS": DOOR_GROUP_ITEM_IDS,
        "PROGRESSIVE_ITEM_IDS": PROGRESSIVE_ITEM_IDS,
    }
    
    with open(output_path, "wb") as file:
        pickle.dump(pickdata, file)
