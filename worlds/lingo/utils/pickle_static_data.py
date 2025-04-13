from typing import Dict, List, Set, Optional

import os
import sys

sys.path.append(os.path.join("worlds", "lingo"))
sys.path.append(".")
sys.path.append("..")
from datatypes import Door, DoorType, EntranceType, Painting, Panel, PanelDoor, Progression, Room, RoomAndDoor,\
    RoomAndPanel, RoomAndPanelDoor, RoomEntrance

import hashlib
import pickle
import Utils


ALL_ROOMS: List[Room] = []
DOORS_BY_ROOM: Dict[str, Dict[str, Door]] = {}
PANELS_BY_ROOM: Dict[str, Dict[str, Panel]] = {}
PANEL_DOORS_BY_ROOM: Dict[str, Dict[str, PanelDoor]] = {}
PAINTINGS: Dict[str, Painting] = {}

PROGRESSIVE_ITEMS: Set[str] = set()
PROGRESSIVE_DOORS_BY_ROOM: Dict[str, Dict[str, Progression]] = {}
PROGRESSIVE_PANELS_BY_ROOM: Dict[str, Dict[str, Progression]] = {}

PAINTING_ENTRANCES: int = 0
PAINTING_EXIT_ROOMS: Set[str] = set()
PAINTING_EXITS: int = 0
REQUIRED_PAINTING_ROOMS: List[str] = []
REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS: List[str] = []

SUNWARP_ENTRANCES: List[str] = ["", "", "", "", "", ""]
SUNWARP_EXITS: List[str] = ["", "", "", "", "", ""]

SPECIAL_ITEM_IDS: Dict[str, int] = {}
PANEL_LOCATION_IDS: Dict[str, Dict[str, int]] = {}
DOOR_LOCATION_IDS: Dict[str, Dict[str, int]] = {}
DOOR_ITEM_IDS: Dict[str, Dict[str, int]] = {}
DOOR_GROUP_ITEM_IDS: Dict[str, int] = {}
PANEL_DOOR_ITEM_IDS: Dict[str, Dict[str, int]] = {}
PANEL_GROUP_ITEM_IDS: Dict[str, int] = {}
PROGRESSIVE_ITEM_IDS: Dict[str, int] = {}

# This doesn't need to be stored in the datafile.
PANEL_DOOR_BY_PANEL_BY_ROOM: Dict[str, Dict[str, str]] = {}


def hash_file(path):
    md5 = hashlib.md5()
    
    with open(path, 'rb') as f:
        content = f.read()
        content = content.replace(b'\r\n', b'\n')
        md5.update(content)
    
    return md5.hexdigest()


def load_static_data(ll1_path, ids_path):
    global PAINTING_EXITS

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

        if "panel_doors" in config:
            for room_name, panel_doors in config["panel_doors"].items():
                PANEL_DOOR_ITEM_IDS[room_name] = {}

                for panel_door, item_id in panel_doors.items():
                    PANEL_DOOR_ITEM_IDS[room_name][panel_door] = item_id

        if "panel_groups" in config:
            for item_name, item_id in config["panel_groups"].items():
                PANEL_GROUP_ITEM_IDS[item_name] = item_id

        if "progression" in config:
            for item_name, item_id in config["progression"].items():
                PROGRESSIVE_ITEM_IDS[item_name] = item_id

    # Process the main world file.
    with open(ll1_path, "r") as file:
        config = Utils.parse_yaml(file)

        # We have to process all panel doors first so that panels can see what panel doors they're in even if they're
        # defined earlier in the file than the panel door.
        for room_name, room_data in config.items():
            if "panel_doors" in room_data:
                PANEL_DOORS_BY_ROOM[room_name] = dict()

                for panel_door_name, panel_door_data in room_data["panel_doors"].items():
                    process_panel_door(room_name, panel_door_name, panel_door_data)

        # Process the rest of the room.
        for room_name, room_data in config.items():
            process_room(room_name, room_data)

        PAINTING_EXITS = len(PAINTING_EXIT_ROOMS)


def process_single_entrance(source_room: str, room_name: str, door_obj) -> RoomEntrance:
    global PAINTING_ENTRANCES

    entrance_type = EntranceType.NORMAL
    if "painting" in door_obj and door_obj["painting"]:
        entrance_type = EntranceType.PAINTING
    elif "sunwarp" in door_obj and door_obj["sunwarp"]:
        entrance_type = EntranceType.SUNWARP
    elif "warp" in door_obj and door_obj["warp"]:
        entrance_type = EntranceType.WARP
    elif source_room == "Crossroads" and room_name == "Roof":
        entrance_type = EntranceType.CROSSROADS_ROOF_ACCESS

    if "painting" in door_obj and door_obj["painting"]:
        PAINTING_EXIT_ROOMS.add(room_name)
        PAINTING_ENTRANCES += 1

    if "door" in door_obj:
        return RoomEntrance(source_room, RoomAndDoor(
            door_obj["room"] if "room" in door_obj else None,
            door_obj["door"]
        ), entrance_type)
    else:
        return RoomEntrance(source_room, None, entrance_type)


def process_entrance(source_room, doors, room_obj):
    # If the value of an entrance is just True, that means that the entrance is always accessible.
    if doors is True:
        room_obj.entrances.append(RoomEntrance(source_room, None, EntranceType.NORMAL))
    elif isinstance(doors, dict):
        # If the value of an entrance is a dictionary, that means the entrance requires a door to be accessible, is a
        # painting-based entrance, or both.
        room_obj.entrances.append(process_single_entrance(source_room, room_obj.name, doors))
    else:
        # If the value of an entrance is a list, then there are multiple possible doors that can give access to the
        # entrance. If there are multiple connections with the same door (or lack of door) that differ only by entrance
        # type, coalesce them into one entrance.
        entrances: Dict[Optional[RoomAndDoor], EntranceType] = {}
        for door in doors:
            entrance = process_single_entrance(source_room, room_obj.name, door)
            entrances[entrance.door] = entrances.get(entrance.door, EntranceType(0)) | entrance.type

        for door, entrance_type in entrances.items():
            room_obj.entrances.append(RoomEntrance(source_room, door, entrance_type))


def process_panel_door(room_name, panel_door_name, panel_door_data):
    panels: List[RoomAndPanel] = list()
    for panel in panel_door_data["panels"]:
        if isinstance(panel, dict):
            panels.append(RoomAndPanel(panel["room"], panel["panel"]))
        else:
            panels.append(RoomAndPanel(room_name, panel))

    for panel in panels:
        PANEL_DOOR_BY_PANEL_BY_ROOM.setdefault(panel.room, {})[panel.panel] = RoomAndPanelDoor(room_name,
                                                                                               panel_door_name)

    if "item_name" in panel_door_data:
        item_name = panel_door_data["item_name"]
    else:
        panel_per_room = dict()
        for panel in panels:
            panel_room_name = room_name if panel.room is None else panel.room
            panel_per_room.setdefault(panel_room_name, []).append(panel.panel)

        room_strs = list()
        for door_room_str, door_panels_str in panel_per_room.items():
            room_strs.append(door_room_str + " - " + ", ".join(door_panels_str))

        if len(panels) == 1:
            item_name = f"{room_strs[0]} (Panel)"
        else:
            item_name = " and ".join(room_strs) + " (Panels)"

    if "panel_group" in panel_door_data:
        panel_group = panel_door_data["panel_group"]
    else:
        panel_group = None

    panel_door_obj = PanelDoor(item_name, panel_group)
    PANEL_DOORS_BY_ROOM[room_name][panel_door_name] = panel_door_obj


def process_panel(room_name, panel_name, panel_data):
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

    if room_name in PANEL_DOOR_BY_PANEL_BY_ROOM and panel_name in PANEL_DOOR_BY_PANEL_BY_ROOM[room_name]:
        panel_door = PANEL_DOOR_BY_PANEL_BY_ROOM[room_name][panel_name]
    else:
        panel_door = None

    if "location_name" in panel_data:
        location_name = panel_data["location_name"]
    else:
        location_name = None

    panel_obj = Panel(required_rooms, required_doors, required_panels, colors, check, event, exclude_reduce,
                      achievement, non_counting, panel_door, location_name)
    PANELS_BY_ROOM[room_name][panel_name] = panel_obj


def process_door(room_name, door_name, door_data):
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
        panels = []

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

    door_type = DoorType.NORMAL
    if room_name == "Sunwarps":
        door_type = DoorType.SUNWARP
    elif room_name == "Pilgrim Antechamber" and door_name == "Sun Painting":
        door_type = DoorType.SUN_PAINTING

    door_obj = Door(door_name, item_name, location_name, panels, skip_location, skip_item, has_doors,
                    painting_ids, event, door_group, include_reduce, door_type, item_group)

    DOORS_BY_ROOM[room_name][door_name] = door_obj


def process_painting(room_name, painting_data):
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


def process_sunwarp(room_name, sunwarp_data):
    if sunwarp_data["direction"] == "enter":
        SUNWARP_ENTRANCES[sunwarp_data["dots"] - 1] = room_name
    else:
        SUNWARP_EXITS[sunwarp_data["dots"] - 1] = room_name


def process_progressive_door(room_name, progression_name, progression_doors):
    # Progressive items are configured as a list of doors.
    PROGRESSIVE_ITEMS.add(progression_name)

    progression_index = 1
    for door in progression_doors:
        if isinstance(door, Dict):
            door_room = door["room"]
            door_door = door["door"]
        else:
            door_room = room_name
            door_door = door

        room_progressions = PROGRESSIVE_DOORS_BY_ROOM.setdefault(door_room, {})
        room_progressions[door_door] = Progression(progression_name, progression_index)
        progression_index += 1


def process_progressive_panel(room_name, progression_name, progression_panel_doors):
    # Progressive items are configured as a list of panel doors.
    PROGRESSIVE_ITEMS.add(progression_name)

    progression_index = 1
    for panel_door in progression_panel_doors:
        if isinstance(panel_door, Dict):
            panel_door_room = panel_door["room"]
            panel_door_door = panel_door["panel_door"]
        else:
            panel_door_room = room_name
            panel_door_door = panel_door

        room_progressions = PROGRESSIVE_PANELS_BY_ROOM.setdefault(panel_door_room, {})
        room_progressions[panel_door_door] = Progression(progression_name, progression_index)
        progression_index += 1


def process_room(room_name, room_data):
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

    if "sunwarps" in room_data:
        for sunwarp_data in room_data["sunwarps"]:
            process_sunwarp(room_name, sunwarp_data)

    if "progression" in room_data:
        for progression_name, pdata in room_data["progression"].items():
            if "doors" in pdata:
                process_progressive_door(room_name, progression_name, pdata["doors"])
            if "panel_doors" in pdata:
                process_progressive_panel(room_name, progression_name, pdata["panel_doors"])

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
        "PANEL_DOORS_BY_ROOM": PANEL_DOORS_BY_ROOM,
        "PROGRESSIVE_ITEMS": PROGRESSIVE_ITEMS,
        "PROGRESSIVE_DOORS_BY_ROOM": PROGRESSIVE_DOORS_BY_ROOM,
        "PROGRESSIVE_PANELS_BY_ROOM": PROGRESSIVE_PANELS_BY_ROOM,
        "PAINTING_ENTRANCES": PAINTING_ENTRANCES,
        "PAINTING_EXIT_ROOMS": PAINTING_EXIT_ROOMS,
        "PAINTING_EXITS": PAINTING_EXITS,
        "REQUIRED_PAINTING_ROOMS": REQUIRED_PAINTING_ROOMS,
        "REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS": REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS,
        "SUNWARP_ENTRANCES": SUNWARP_ENTRANCES,
        "SUNWARP_EXITS": SUNWARP_EXITS,
        "SPECIAL_ITEM_IDS": SPECIAL_ITEM_IDS,
        "PANEL_LOCATION_IDS": PANEL_LOCATION_IDS,
        "DOOR_LOCATION_IDS": DOOR_LOCATION_IDS,
        "DOOR_ITEM_IDS": DOOR_ITEM_IDS,
        "DOOR_GROUP_ITEM_IDS": DOOR_GROUP_ITEM_IDS,
        "PANEL_DOOR_ITEM_IDS": PANEL_DOOR_ITEM_IDS,
        "PANEL_GROUP_ITEM_IDS": PANEL_GROUP_ITEM_IDS,
        "PROGRESSIVE_ITEM_IDS": PROGRESSIVE_ITEM_IDS,
    }
    
    with open(output_path, "wb") as file:
        pickle.dump(pickdata, file)
