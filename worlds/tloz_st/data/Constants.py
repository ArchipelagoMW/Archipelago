VERSION = "0.3.0"
ROM_HASH = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"


STARTING_FLAGS = [
    # Starting flags (these are in the same memory block so can be simplified, but it's called once and this is
    # easier to bugfix)

    [0x265714, 0x04],  # restore spirit train cutscene skip
    #[0x265715, 0x80],  # unlock rail map
    [0x265716, 0xF0],  # sword tutorial and intro stuff
    [0x265717, 0x07],  # split ToS and zelda 1st convo
    [0x265718, 0x14],  # load train to ToS
    [0x265719, 0x20],  # train quill tutorial skip
    [0x26571A, 0xFC],  # Intro stuff
    [0x26571B, 0x03],  # postman & get zelda's letter
    [0x265726, 0x03],  # zelda 1st phantom possession
    [0x265729, 0x50],  # post fleeing ToS 1F
    [0x26572C, 0x07],  # HC intro Zelda
    [0x26572F, 0x02],  # initial train cutscene skip
    [0x265738, 0x08],  # move HC guards
    [0x265751, 0x20],  # ToS safe zone tutorial
    [0x265756, 0x80],  # board with zelda
    [0x265766, 0x80],  # ToS Staircase cutscene skip
    [0x265768, 0x20],  # first spirit train journey
    [0x26575C, 0x10],  # alfonzo giving cannon
]

STAGE_FLAGS = {
     35: [0x0, 0x0A, 0x0B, 0x0C], # Aboda Village
     29: [0x00, 0x00, 0x00, 0x00], # Castle Town
     28: [0x00, 0x00, 0x00, 0x00],  # Hyrule Castle
     13: [0x00, 0x00, 0x00, 0x00],  # Tower of Spirits (Main)
    14: [0x00, 0x00, 0x00, 0x00], # Tower of Spirits (Base)
    17: [0x00, 0x00, 0x00, 0x00],  # Tower of Spirits (Stairs)

    # 37: [0xFE, 0xBE, 0xFB, 0xAF],  # TotOK
    # 0: [0x82, 0xFC, 0x66, 0xED],  # Sea
    # 13: [0xEC, 0x18, 0x17, 0x00],  # Ember
    # 28: [0x8E, 0xB9, 0x00, 0x00],  # ToF
    # 12: [0x34, 0x01, 0x00, 0x00],  # Molida
    # 14: [0x02, 0x02, 0x00, 0x00],  # Gusts
    # 29: [0x00, 0x10, 0x00, 0x00],  # ToW
    # 30: [0x0, 0x0, 0x2, 0x0],  # ToC
    # 41: [0xC2, 0x10, 0xED, 0x00],  # Ghost Ship
    # 16: [0x84, 0x13, 0x00, 0xE0],  # Goron Island
    # 32: [0x00, 0x00, 0x30, 0xF0],  # Goron Temple
    # 15: [0x00, 0x3C, 0x00, 0x40],  # Isle of Frost
    # 31: [0x00, 0x00, 0xD0, 0x00],  # Temple of Ice
    # 21: [0xB6, 0x01, 0x00, 0x00],  # Isle of the Dead
    # 17: [0x12, 0x4C, 0x43, 0x00],  # Isle of ruins
    # 18: [0x10, 0x4C, 0x43, 0x00],  # Isle of ruins
    # 36: [0x20, 0x00, 0x00, 0x00],  # Bremeur's Temple
    # 33: [0x00, 0x26, 0x00, 0x00],  # Mutoh's Temple
}

STAGES = {
    4: "Forest Realm",
    0x2F: "Aboda Village",
    0x29: "Castle Town",
    0x28: "Hyrule Castle",
    0x13: "Tower of Spirits"
}

ITEM_GROUPS = {
    # "Small Keys": [
    #     "Small Key (Mountain Passage)",
    #     "Small Key (Temple of the Ocean King)",
    #     "Small Key (Temple of Fire)",
    #     "Small Key (Temple of Wind)",
    #     "Small Key (Temple of Courage)",
    #     "Small Key (Temple of Ice)",
    #     "Small Key (Mutoh's Temple)"
    # ],
    "Treasure Items": [
        "Treasure: Pink Coral",
        "Treasure: White Pearl Loop",
        "Treasure: Dark Pearl Loop",
        "Treasure: Zora Scale",
        "Treasure: Goron Amber",
        "Treasure: Ruto Crown",
        "Treasure: Helmaroc Plume",
        "Treasure: Regal Ring"
    ],
    # "Ammo Refills": [
    #     "Refill: Bombs",
    #     "Refill: Arrows",
    #     "Refill: Bombchus"
    # ]
}

LOCATION_GROUPS = {
    "Aboda Village": ["Aboda Clear Rocks", "Aboda Bee Tree", "Aboda Stamp Station"]
    # "Mountain Passage": [
    #     "Mountain Passage Chest 1",
    #     "Mountain Passage Chest 2",
    #     "Mountain Passage Key Drop",
    #     "Mountain Passage Rat Key",
    # ],
    # "Temple of the Ocean King": [],
    # "Temple of Fire": [],
    # "Temple of Wind": [],
    # "Temple of Courage": [],
    # "Goron Temple": [],
    # "Temple of Ice": [],
    # "Mutoh's Temple": [],
    # "Ghost Ship": []
}

CUSTOM_METALS = {
    "Custom Metals": [
        "Verdanine",
        "Lavendine",
        "Amberine",
        "Vermilline",
        "Crystaline",
    ],
}

DUNGEON_NAMES = [
    "Hyrule Castle",
    "Tower of Spirits"
]

DUNGEON_TO_BOSS_ITEM_LOCATION = {
    "Tower of Spirits": "ToS Forest Rail Glyph",
}


DUNGEON_KEY_DATA = {
    # 39: {
    #     "name": "Mountain Passage",
    #     "address": 0x1BA64E,
    #     "filter": 0x0C,
    #     "value": 4,
    #     "size": 2,
    #     'entrances': {
    #         0xB01: {
    #             "max_z": 0x12800,
    #             # "max_z": 0xFFFF7000
    #         },
    #         0xB03: {
    #             "max_z": 0xB200,
    #             "min_z": 0x5000
    #         }
    #
    #     }
    # },
    # 37: {
    #     "name": "Temple of the Ocean King",
    #     "address": 0x1BA64E,
    #     "filter": 0xE0,
    #     "value": 0x20,
    #     "size": 3,
    #     'entrances': {
    #         0x2600: {
    #             "max_z": 0x11800,
    #             "min_z": 0x0
    #         }
    #     }
    # },
    # 372: {
    #     "name": "Temple of the Ocean King",
    #     "address": 0x1BA64F,
    #     "filter": 0xC0,
    #     "value": 0x40,
    #     "size": 2,
    #     'entrances': {
    #         0x2600: {
    #             "max_z": 0x11800,
    #             "min_z": 0x0}
    #     }
    # },
    # 0x1C: {
    #     "name": "Temple of Fire",
    #     "address": 0x1BA64E,
    #     "value": 1,
    #     "size": 2,
    #     "filter": 0x03,
    #     "entrances": {
    #         0xD01: {
    #             "max_z": 0x10800,
    #             "min_z": 0x8000},
    #         0x2B00: {
    #             "min_z": 0x800,
    #             "max_z": 0xF000}
    #     }
    # },
    # 0x1E: {
    #     "name": "Temple of Courage",
    #     "address": 0x1BA64F,
    #     "value": 0x10,
    #     "size": 2,
    #     "filter": 0x30,
    # },
    # 0x1D: {
    #     "name": "Temple of Wind",
    #     "address": 0x1BA64E,
    #     "value": 0x10,
    #     "size": 1,
    #     "filter": 0x10
    # },
    # 0x1F: {
    #     "name": "Temple of Ice",
    #     "address": 0x1BA64F,
    #     "value": 0x1,
    #     "size": 2,
    #     "filter": 0x03
    # },
    # 0x21: {
    #     "name": "Mutoh's Temple",
    #     "address": 0x1BA64F,
    #     "value": 0x4,
    #     "size": 2,
    #     "filter": 0x0C
    # },
}

HINTS_ON_SCENE = {
    # 0xB11: {  # Mercay Shop
    #     "island_shop": True
    # },
    # 0xC0E: {  # Molida Shop
    #     "island_shop": True
    # },
    # 0x1014: {  # Goron Shop
    #     "island_shop": True
    # },
    # 0x130B: {  # Eddo Cannon Island
    #     "unique": ["Cannon Island Cannon", "Cannon Island Salvage Arm"]
    # },
    # 0x500: {  # Beedle Shop
    #     "unique": ["Beedle Shop Wisdom Gem"],
    #     "beedle": True  # TODO: make this modular, instead of hard coding item requirements
    # },
    # 0xb0A: {  # Oshus Dungeon hints
    #     "dungeon_hints": 1
    # },
    # 0x2600: {  # TotOK Dungeon hints
    #     "dungeon_hints": 2
    # },
    # 0x1701: {
    #     "spirit_island_hints": True
    # },
}

HINTS_ON_TRIGGER = {
    #"Masked Beedle": ["Masked Beedle Courage Gem", "Masked Beedle Heart Container"]
}

# Train sets
TRAINS = [
    "S.S. Linebeck",
    "Train: Bright Train",
    "Train: Iron Train",
    "Train: Stone Train",
    "Train: Vintage Train",
    "Train: Demon Train",
    "Train: Tropical Train",
    "Train: Dignified Train",
    "Train: Golden Train",
]

# Stamp stuff
STAMPS = []

# Decode classification for humans
CLASSIFICATION = {
    1: "Progression",
    2: "Useful",
    4: "Trap",
    9: "Prog Skip Balancing",
    0: "Filler"
                  }

#TREASURE_READ_LIST = {i: (0x1BA5AC + i * 4, 4, "Main RAM") for i in range(8)}
