from typing import Dict, List, Set

import pickle

from .datatypes import Door, Painting, Panel, Progression, Room

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

HASHES: Dict[str, str] = {}


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


def load_static_data_from_file():
    global HASHES, PAINTINGS, ALL_ROOMS, DOORS_BY_ROOM, PANELS_BY_ROOM, PROGRESSIVE_ITEMS, PROGRESSION_BY_ROOM, PAINTING_ENTRANCES, PAINTING_EXIT_ROOMS, PAINTING_EXITS, REQUIRED_PAINTING_ROOMS, REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS, SPECIAL_ITEM_IDS, PANEL_LOCATION_IDS, DOOR_LOCATION_IDS, DOOR_ITEM_IDS, DOOR_GROUP_ITEM_IDS, PROGRESSIVE_ITEM_IDS
    
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files

    from . import data
    
    if not files(data).joinpath("generated.dat").exists():
        return

    with files(data).joinpath("generated.dat").open("rb") as file:
        class RenameUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                renamed_module = module
                if module == "datatypes":
                    renamed_module = "worlds.lingo.datatypes"

                return super(RenameUnpickler, self).find_class(renamed_module, name)

        pickdata = RenameUnpickler(file).load()
        
        HASHES = pickdata["HASHES"]
        PAINTINGS = pickdata["PAINTINGS"]
        ALL_ROOMS = pickdata["ALL_ROOMS"]
        DOORS_BY_ROOM = pickdata["DOORS_BY_ROOM"]
        PANELS_BY_ROOM = pickdata["PANELS_BY_ROOM"]
        PROGRESSIVE_ITEMS = pickdata["PROGRESSIVE_ITEMS"]
        PROGRESSION_BY_ROOM = pickdata["PROGRESSION_BY_ROOM"]
        PAINTING_ENTRANCES = pickdata["PAINTING_ENTRANCES"]
        PAINTING_EXIT_ROOMS = pickdata["PAINTING_EXIT_ROOMS"]
        PAINTING_EXITS = pickdata["PAINTING_EXITS"]
        REQUIRED_PAINTING_ROOMS = pickdata["REQUIRED_PAINTING_ROOMS"]
        REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS = pickdata["REQUIRED_PAINTING_WHEN_NO_DOORS_ROOMS"]
        SPECIAL_ITEM_IDS = pickdata["SPECIAL_ITEM_IDS"]
        PANEL_LOCATION_IDS = pickdata["PANEL_LOCATION_IDS"]
        DOOR_LOCATION_IDS = pickdata["DOOR_LOCATION_IDS"]
        DOOR_ITEM_IDS = pickdata["DOOR_ITEM_IDS"]
        DOOR_GROUP_ITEM_IDS = pickdata["DOOR_GROUP_ITEM_IDS"]
        PROGRESSIVE_ITEM_IDS = pickdata["PROGRESSIVE_ITEM_IDS"]


# Initialize the static data at module scope.
load_static_data_from_file()
