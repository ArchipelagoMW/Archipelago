from .Entrances import ENTRANCES
from .Constants import LOCATION_GROUPS

def create_scene_id(entrance):
    e_stage, e_room, e_entrance = entrance
    return e_stage * 0x100 + e_room

DYNAMIC_ENTRANCES = {
    # Dungeon Shortcuts
    "Shortcut to TotOK": {
        "entrance": "Mercay SE Tuzi's House",
        "destination": "TotOK Lobby Exit",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["TotOK Phantom Hourglass",
                          "TotOK 1F Linebeck Key"],
    },
    "Shortcut to Temple of Fire": {
        "entrance": "Ember Port House",
        "destination": "ToF Exit",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Temple of Fire 1F Keese Chest",
                              "Temple of Fire 1F Maze Chest"],
    },
    "Shortcut to Temple of Wind": {
        "entrance": "Ocean NW Gust",
        "destination": "ToW Exit",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "has_locations": LOCATION_GROUPS["Isle of Gust"],
    },
    "Shortcut to Temple of Wind no digging": {
        "entrance": "Ocean NW Gust",
        "destination": "ToW Exit",
        "has_slot_data": [("dungeon_shortcuts", 1), ("randomize_digs", 0)],
        "has_locations": [
            "Isle of Gust Hideout Chest",
            "Isle of Gust Miblin Cave North Chest",
            "Isle of Gust Miblin Cave South Chest",
            "Isle of Gust West Cliff Chest",
            "Isle of Gust Sandworm Chest",
        ],
    },
    "Shortcut to Temple of Courage": {
        "entrance": "Molida Port House",
        "destination": "ToC Exit",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Temple of Courage 1F Bomb Alcove Chest",
                          "Temple of Courage 1F Raised Platform Chest"],
    },
    "Shortcut to Goron Temple": {
        "entrance": "Goron SW Port House",
        "destination": "GT Exit",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Goron Temple 1F Switch Chest",
                              "Goron Temple 1F Bow Chest",
                              "Goron Temple B1 Bombchu Bag Chest"],
    },
    "Shortcut to Temple of Ice": {
        "entrance": "Frost SW Smart House",
        "destination": "ToI Exit",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Temple of Ice 3F Corner Chest",
                              "Temple of Ice B1 Entrance Chest"],
    },
    "Shortcut to Mutoh's Temple": {
        "entrance": "Ruins SW Port Cave",
        "destination": "MT Exit",
        "has_slot_data": [("dungeon_shortcuts", 1)],
        "any_has_locations": ["Mutoh's Temple 2F Like-Like Maze Chest",
                              "Mutoh's Temple 3F Hammer Chest",
                              "Mutoh's Temple B2 Spike Roller Chest",
                              "Mutoh's Temple B2 Ledge Chest",
                              "Mutoh's Temple B1 Lower Water Chest",
                              "Mutoh's Temple B1 Push Boulder Chest",
                              "Mutoh's Temple B1 Boss Key Chest"],
    },
    # Ending blue warps take you inside dungeon, to save ER hassles
    "Blaaz warp": {
        "entrance": "ToF Blaaz Warp",
        "destination": "ToF Exit",
        "has_slot_data": [("shuffle_dungeon_entrances", 1), ("shuffle_bosses", 0)],
    },
    "Blaaz warp Boss Shuffle": {
        "entrance": "ToF Blaaz Warp",
        "destination": "_connected_dungeon_entrance",
        "has_slot_data": [("shuffle_bosses", [1, 2])],
    },
    "Cyclok warp": {
        "entrance": "ToW Cyclok Warp",
        "destination": "ToW Exit",
        "has_slot_data": [("shuffle_dungeon_entrances", 1), ("shuffle_bosses", 0)],
    },
    "Cyclok warp Boss Shuffle": {
        "entrance": "ToW Cyclok Warp",
        "destination": "_connected_dungeon_entrance",
        "has_slot_data": [("shuffle_bosses", [1, 2])],
    },
    "Crayk warp": {
        "entrance": "ToC Crayk Warp",
        "destination": "ToC Exit",
        "has_slot_data": [("shuffle_dungeon_entrances", 1), ("shuffle_bosses", 0)],
    },
    "Crayk warp Boss Shuffle": {
        "entrance": "ToC Crayk Warp",
        "destination": "_connected_dungeon_entrance",
        "has_slot_data": [("shuffle_bosses", [1, 2])],
    },
    "Dongo warp": {
        "entrance": "GT Dongo Warp",
        "destination": "GT Exit",
        "has_slot_data": [("shuffle_dungeon_entrances", 1), ("shuffle_bosses", 0)],
    },
    "Dongo warp Boss Shuffle": {
        "entrance": "GT Dongo Warp",
        "destination": "_connected_dungeon_entrance",
        "has_slot_data": [("shuffle_bosses", [1, 2])],
    },
    "Gleeok warp": {
        "entrance": "ToI Gleeok Warp",
        "destination": "ToI Exit",
        "has_slot_data": [("shuffle_dungeon_entrances", 1), ("shuffle_bosses", 0)],
    },
    "Gleeok warp Boss Shuffle": {
        "entrance": "ToI Gleeok Warp",
        "destination": "_connected_dungeon_entrance",
        "has_slot_data": [("shuffle_bosses", [1, 2])],
    },
    "Eox warp": {
        "entrance": "MT Eox Warp",
        "destination": "MT Exit",
        "has_slot_data": [("shuffle_dungeon_entrances", 1), ("shuffle_bosses", 0)],
    },
    "Eox warp Boss Shuffle": {
        "entrance": "MT Eox Warp",
        "destination": "_connected_dungeon_entrance",
        "has_slot_data": [("shuffle_bosses", [1, 2])],
    },
    "GS warp": {
        "entrance": "Finish Ghost Ship",
        "destination": "Ghost Ship B1 Ascend",
        "has_slot_data": [("shuffle_dungeon_entrances", [1, 2])],
    },
    "Cubus warp Boss Shuffle": {
        "entrance": "Cubus Sisters Blue Warp",
        "destination": "_connected_dungeon_entrance",
        "has_slot_data": [("shuffle_bosses", [1, 2])],
    },
    # Other shortcuts
    "Brant's Maze Shortcut": {
        "entrance": "Brant's Maze 1",
        "destination": "Brant's Maze Exit", # TODO: add to dungeon shortcuts
    },
    # TotOK shortcuts
    "TotOK b10 shortcut warp": {
        "entrance": "TotOK Lobby Yellow Warp",
        "destination": "TotOK B10 Cave",
        "has_locations": ["TotOK B9.5 SE Sea Chart Chest"],
        "has_slot_data": [("totok_checkpoints", 1)]
    },
    "TotOK b9.5 warp up": {
        "entrance": "TotOK B9.5 Blue Warp",
        "destination": "TotOK B6.5 Yellow Warp",
        "has_slot_data": [("totok_checkpoints", 1)]
    },
    "TotOK midway warp up": {
        "entrance": "TotOK B6.5 Yellow Warp",
        "destination": "TotOK B3.5 Blue Warp",
        "has_slot_data": [("totok_checkpoints", 1)]
    },
    "TotOK b3 shortcut warp": {
        "entrance": "TotOK Lobby Yellow Warp",
        "destination": "TotOK B3.5 Blue Warp",
        "has_locations": ["TotOK B3 NW Sea Chart Chest"],
        "has_slot_data": [("totok_checkpoints", 1)],
        "check_bits": [(0x1BA661, 0x40, "not")]
    },
    "TotOK cc room backup": {
        "entrance": "TotOK CC Room Warp",
        "destination": "TotOK B6 Red Door Hourglass",
    },
    "TotOK B3 warp up hint": {
        "entrance": "TotOK B3.5 Blue Warp",
        "destination": "TotOK Lobby Yellow Warp",
        "has_slot_data": [("totok_checkpoints", 1)],
    },
}

DYNAMIC_ENTRANCES_BY_SCENE = {}
for name, data in DYNAMIC_ENTRANCES.items():
    data["name"] = name
    entrance_data = ENTRANCES[data["entrance"]]
    if data["destination"] == "_connected_dungeon_entrance":
        destination_data = None
    else:
        destination_data = ENTRANCES[data["destination"]]

    entrance_scene = entrance_data.scene

    # Save er_in_scene values in data
    data["detect_data"] = entrance_data
    data["exit_data"] = destination_data
    DYNAMIC_ENTRANCES_BY_SCENE.setdefault(entrance_scene, {})
    DYNAMIC_ENTRANCES_BY_SCENE[entrance_scene][name] = data
