VERSION = "0.3.0"
ROM_HASH = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"

#TODO all change
STARTING_FLAGS = [
    # Starting flags (these are in the same memory block so can be simplified, but it's called once and this is
    # easier to bugfix)

    [0x26572F, 0x02], #initial train cutscene skip

]

STAGE_FLAGS = {
    # 11: [0xC4,  # Mercay
    #      0xDC,
    #      0x06,
    #      0x00],
    # 39: [0x40,  # Mountain Passage
    #      0x00,
    #      0x00,
    #      0x00],
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
    0x2F: "Aboda Village"
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
    ],
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
    "Ammo Refills": [
        "Refill: Bombs",
        "Refill: Arrows",
        "Refill: Bombchus"
    ]
}

LOCATION_GROUPS = {
    "Mountain Passage": [
        "Mountain Passage Chest 1",
        "Mountain Passage Chest 2",
        "Mountain Passage Key Drop",
        "Mountain Passage Rat Key",
    ],
    "Temple of the Ocean King": [],
    "Temple of Fire": [],
    "Temple of Wind": [],
    "Temple of Courage": [],
    "Goron Temple": [],
    "Temple of Ice": [],
    "Mutoh's Temple": [],
    "Ghost Ship": []
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

DUNGEON_TO_BOSS_ITEM_LOCATION = {
    "Temple of the Ocean King": "TotOK B13 NE Sea Chart Chest",
    "Temple of Fire": "Temple of Fire Blaaz Dungeon Reward",
    "Temple of Wind": "Temple of Wind Cyclok Dungeon Reward",
    "Temple of Courage": "Temple of Courage Crayk Dungeon Reward",
    "Goron Temple": "Goron Temple Dongorongo Dungeon Reward",
    "Temple of Ice": "Temple of Ice Dungeon Reward",
    "Mutoh's Temple": "Mutoh's Temple Dungeon Reward",
    "Ghost Ship": "_gs",
}

GHOST_SHIP_BOSS_ITEM_LOCATION = [
    "Ghost Ship Rescue Tetra",
    "Ghost Ship Cubus Sisters Ghost Key"
]

FROG_LOCATION_NAMES = [
    "Ocean SW Golden Frog X",
    "Ocean SW Golden Frog Phi",
    "Ocean NW Golden Frog N",
    "Ocean SE Golden Frog Omega",
    "Ocean SE Golden Frog W",
    "Ocean NE Golden Frog Square"
]

FROG_NAMES = [
    "Golden Frog Glyph X",
    "Golden Frog Glyph Phi",
    "Golden Frog Glyph N",
    "Golden Frog Glyph Omega",
    "Golden Frog Glyph W",
    "Golden Frog Glyph Square"
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
    },
    37: {
        "name": "Temple of the Ocean King",
        "address": 0x1BA64E,
        "filter": 0xE0,
        "value": 0x20,
        "size": 3,
        'entrances': {
            0x2600: {
                "max_z": 0x11800,
                "min_z": 0x0
            }
        }
    },
    372: {
        "name": "Temple of the Ocean King",
        "address": 0x1BA64F,
        "filter": 0xC0,
        "value": 0x40,
        "size": 2,
        'entrances': {
            0x2600: {
                "max_z": 0x11800,
                "min_z": 0x0}
        }
    },
    0x1C: {
        "name": "Temple of Fire",
        "address": 0x1BA64E,
        "value": 1,
        "size": 2,
        "filter": 0x03,
        "entrances": {
            0xD01: {
                "max_z": 0x10800,
                "min_z": 0x8000},
            0x2B00: {
                "min_z": 0x800,
                "max_z": 0xF000}
        }
    },
    0x1E: {
        "name": "Temple of Courage",
        "address": 0x1BA64F,
        "value": 0x10,
        "size": 2,
        "filter": 0x30,
    },
    0x1D: {
        "name": "Temple of Wind",
        "address": 0x1BA64E,
        "value": 0x10,
        "size": 1,
        "filter": 0x10
    },
    0x1F: {
        "name": "Temple of Ice",
        "address": 0x1BA64F,
        "value": 0x1,
        "size": 2,
        "filter": 0x03
    },
    0x21: {
        "name": "Mutoh's Temple",
        "address": 0x1BA64F,
        "value": 0x4,
        "size": 2,
        "filter": 0x0C
    },
}

HINTS_ON_SCENE = {
    0xB11: {  # Mercay Shop
        "island_shop": True
    },
    0xC0E: {  # Molida Shop
        "island_shop": True
    },
    0x1014: {  # Goron Shop
        "island_shop": True
    },
    0x130B: {  # Eddo Cannon Island
        "unique": ["Cannon Island Cannon", "Cannon Island Salvage Arm"]
    },
    0x500: {  # Beedle Shop
        "unique": ["Beedle Shop Wisdom Gem"],
        "beedle": True  # TODO: make this modular, instead of hard coding item requirements
    },
    0xb0A: {  # Oshus Dungeon hints
        "dungeon_hints": 1
    },
    0x2600: {  # TotOK Dungeon hints
        "dungeon_hints": 2
    },
    0x1701: {
        "spirit_island_hints": True
    },
}

HINTS_ON_TRIGGER = {
    "Masked Beedle": ["Masked Beedle Courage Gem", "Masked Beedle Heart Container"]
}

# Train sets
SHIPS = [
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

# Decode classification for humans
CLASSIFICATION = {
    1: "Progression",
    2: "Useful",
    4: "Trap",
    9: "Prog Skip Balancing",
    0: "Filler"
                  }

#TREASURE_READ_LIST = {i: (0x1BA5AC + i * 4, 4, "Main RAM") for i in range(8)}
