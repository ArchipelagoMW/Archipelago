VERSION = "0.3.0"
ROM_HASH = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"

STARTING_FLAGS = [
    [0x1B557C, 0xEF],
    [0x1B557D, 0x3C],
    [0x1B557E, 0x3E],
    [0x1B557F, 0x03],
    [0x1B5580, 0xE7],
    [0x1B5581, 0xB0],
    [0x1B5582, 0x40],
    [0x1B5583, 0xAB],
    [0x1B5584, 0xFF],
    [0x1B5585, 0xFF],
    [0x1B5586, 0x27],
    [0x1B5587, 0xFC],
    [0x1B5588, 0x3B],
    [0x1B5589, 0x00],
    [0x1B558A, 0x04],
    [0x1B558B, 0x02],
    [0x1B558C, 0xD9],
    [0x1B558D, 0x4F],
    [0x1B558E, 0x12],
    [0x1B558F, 0x04],
    [0x1B5590, 0x02],
    [0x1B5591, 0xFE],
    [0x1B5592, 0x05],
    [0x1B5593, 0xEA],
    [0x1B5594, 0x47],
    [0x1B5595, 0x00],
    [0x1B5596, 0x08],
    [0x1B5597, 0x03],
    [0x1B5598, 0x34],
    [0x1B5599, 0xE0],
    [0x1B559A, 0x10],
    [0x1B559B, 0xE0],
    [0x1B559C, 0x4E],
    [0x1B559D, 0xF9],
    [0x1B559E, 0x0F],
    [0x1B559F, 0x05],
    [0x1B55A0, 0x31],
    [0x1B55A1, 0x00],
    [0x1B55A2, 0xA0],
    [0x1B55A3, 0x1F],
    [0x1B55A4, 0x26],
    [0x1B55A5, 0xCC],
    [0x1B55A6, 0x00],
    [0x1B55A7, 0x48],
    [0x1B55A8, 0x1F],
    [0x1B55A9, 0x00],
    [0x1B55AA, 0x18],
    [0x1B55AB, 0x40],
    [0x1B55AC, 0x70],
    [0x1B55AD, 0x00],
    [0x1B55AE, 0x00],
    [0x1B55AF, 0x00],
    [0x1BA6BC, 0x01],
    [0x1BA6BE, 0x01],
    [0x1BA6C4, 0x01],
    [0x1BA6C8, 0x01],
    [0x1BA644, 0x04]
]

STAGES = {
    0: "Sea",
    1: "Cannon Game",
    2: "Fishing",
    3: "Salvage",
    4: "Linebeck's Ship",
    5: "Beedle's Ship",
    6: "Man of Smiles' Ship",
    7: "PoRL's Ship",
    8: "SS Wayfarer",
    9: "Wayaway's Ship",
    10: "Nyave's Ship",
    11: "Mercay Island",
    12: "Molida Island",
    13: "Isle of Ember",
    14: "Isle of Gust",
    15: "Isle of Frost",
    16: "Goron Island",
    17: "Isle of Ruins (High Water)",
    18: "Isle of Ruins (Low Water)",
    19: "Cannon Island",
    20: "Bannan Island",
    21: "Isle of the Dead",
    22: "Zauz's Island",
    23: "Spirit Island",
    24: "Harrow Island",
    25: "Maze Island",
    26: "Uncharted Island",
    27: "Dee Ess Island",
    28: "Temple of Fire",
    29: "Temple of Wind",
    30: "Temple of Courage",
    31: "Temple of Ice",
    32: "Goron Temple",
    33: "Mutoh's Temple",
    34: "Doylan's Temple",
    35: "Max's Temple",
    36: "Bremeur's Temple",
    37: "Temple of the Ocean King",
    38: "Temple of the Ocean King Entrance",
    39: "Mercay Mountain Passage",
    40: "Cannon Island Cave",
    41: "Ghost Ship",
    42: "Cyclok",
    43: "Blaaz",
    44: "Crayk",
    45: "Gleeok",
    46: "Dongorongo",
    47: "Eox",
    48: "Cubus Sisters",
    49: "Bellum",
    50: "Bellum's Ghost Ship",
    51: "Bellumbeck"


}

ITEM_GROUPS = {
    "Small Keys": [
        "Small Key (Mountain Passage)",
        "Small Key (Temple of the Ocean King)",
        "Small Key (Temple of Fire)",
        "Small Key (Temple of Wind)",
        "Small Key (Temple of Courage)",
        "Small Key (Temple of Ice)",
        "Small Key (Mutoh's Temple)"
    ]
}

DUNGEON_NAMES = [
    "Mountain Passage",
    "Temple of the Ocean King",
    "Temple of Fire",
    "Temple of Wind",
    "Temple of Courage",
    "Goron Temple",
    "Temple of Ice",
    "Mutoh's Temple",
    "Ghost Ship"
]

DUNGEON_KEY_DATA = {
    39: {
        "name": "Mountain Passage",
        "address": 0x1BA64E,
        "filter": 0x0C,
        "value": 4,
        "size": 2,
        'entrances': {
            0xB01: {
                "max_z": 0x12800,
                # "max_z": 0xFFFF7000
            },
            0xB03: {
                "max_z": 0xB200,
                "min_z": 0x5000
            }

        }
    }
}

SHOPS = {
    0xB11: {
        "unique": "Mercay Shop Power Gem"
    }
}
