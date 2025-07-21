from BaseClasses import ItemClassification
from worlds.tloz_ph.data.Constants import *

ITEMS_DATA = {
    #   "No Item": {
    #   'classification': ItemClassification,   # classification category
    #   'address': int,                         # address in memory
    #   'value': int,                           # value to set in memory, if incremental added else bitwise or
    #   'size': int,                            # size in bytes
    #   'set_bit': list[tuple[int, int]],       # for setting additional bits on acquisition
    #   'incremental': bool                     # true for positive, False for negative
    #   'progressive': list[list[int, int]]     # address, value for each progressive stage
    #   'give_ammo': list[int]                  # how much ammo to give for each progressive stage
    #   'ammo_address: int                      # address for ammo
    #    },

    # ======= Regular Items==========

    "Sword (Progressive)": {
        'classification': ItemClassification.progression,
        'progressive': [[0x1BA644, 1], [0x1BA648, 32]],
        'set_bit': [(0x1BA644, 1)]  # Means that sending sword if sword breaks gives the base layer
    },
    "Oshus' Sword": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 1
    },
    "Phantom Sword": {
        'classification': ItemClassification.progression,
        'address': 0x1BA648,
        'value': 32
    },
    "Shield": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x02
    },
    "Boomerang": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x04,
        'set_bit': [(0x1BA6BC, 1)]
    },
    "Bombs (Progressive)": {
        'classification': ItemClassification.progression,
        "progressive": [[0x1BA644, 0x10], [0x1BA5D2, 1], [0x1BA5D2, 2]],
        "progressive_overwrite": True,
        "give_ammo": [10, 20, 30],
        "ammo_address": 0x1BA6C0
    },
    "Bombchus (Progressive)": {
        'classification': ItemClassification.progression,
        'progressive': [[0x1BA644, 0x80], [0x1BA5D4, 1], [0x1BA5D4, 2]],
        "give_ammo": [10, 20, 30],
        "ammo_address": 0x1BA6C6,
        "progressive_overwrite": True,
    },
    "Bow (Progressive)": {
        'classification': ItemClassification.progression,
        "progressive": [[0x1BA644, 0x20], [0x1BA5D0, 1], [0x1BA5D0, 2]],
        "give_ammo": [20, 30, 50],
        "ammo_address": 0x1BA6C2,
        "progressive_overwrite": True,
    },
    "Grappling Hook": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x40,
        "set_bit": [(0x1BA6C4, 1)]
    },
    "Shovel": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x08,
        "set_bit": [(0x1BA6BE, 1)]
    },
    "Hammer": {
        'classification': ItemClassification.progression,
        'address': 0x1BA645,
        'value': 0x01,
        'set_bit': [(0x1BA6C8, 1)]
    },

    # ============= Spirits and Upgrades =============

    "Spirit of Power (Progressive)": {
        'classification': ItemClassification.progression,
        'progressive': [[0x1BA646, 0x20], [0x1BA647, 0x01], [0x1BA647, 0x08]]
    },
    "Spirit of Wisdom (Progressive)": {
        'classification': ItemClassification.progression,
        'progressive': [[0x1BA646, 0x40], [0x1BA647, 0x02], [0x1BA647, 0x10]]
    },
    "Spirit of Courage (Progressive)": {
        'classification': ItemClassification.progression,
        'progressive': [[0x1BA646, 0x10], [0x1BA646, 0x80], [0x1BA647, 0x04]]
    },
    "Spirit of Courage White": {
        'classification': ItemClassification.progression,
        'address': None,
        'dummy': True  # TODO won't be dummy once address exists
    },
    "Heart Container": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'address': 0x1BA388,
        'value': 4,
        'incremental': True,
        'size': 2
    },
    "Phantom Hourglass": {
        'classification': ItemClassification.progression,
        'address': 0x1BA528,
        'value': "Sand PH",
        'incremental': True,
        'size': 4
    },
    "Sand of Hours (Boss)": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'address': 0x1BA528,
        'value': 7200,
        'incremental': True,
        'size': 4
    },
    "Sand of Hours (Small)": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'address': 0x1BA528,
        'value': 3600,
        'incremental': True,
        'size': 4
    },
    "Sand of Hours": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'address': 0x1BA528,
        'value': "Sand",
        'incremental': True,
        'size': 4
    },
    "Swordsman's Scroll": {
        'classification': ItemClassification.useful,
        'address': 0x1BA649,
        'value': 0x20,

    },
    # ============= Ship Items =============

    "Cannon": {
        'classification': ItemClassification.progression,
        'address': 0x1B5582,
        'value': 1
    },
    "Salvage Arm": {
        'classification': ItemClassification.progression,
        'address': 0x1BA649,
        'value': 0x10
    },
    "Fishing Rod": {
        'classification': ItemClassification.progression,
        'address': 0x1BA649,
        'value': 0x01,
    },
    "Big Catch Lure": {
        'classification': ItemClassification.progression,
        'address': 0x1BA649,
        'value': 0x80
    },
    "Swordfish Shadows": {
        'classification': ItemClassification.progression,
        'address': 0x1B55A7,
        'value': 0x10
    },
    "Cyclone Slate": {
        'classification': ItemClassification.progression,
        'address': 0x1BA649,
        'value': 0x40
    },
    # ========== Sea Charts ============

    "SW Sea Chart": {
        'classification': ItemClassification.progression,
        'address': 0x1BA648,
        'value': 0x02
    },
    "NW Sea Chart": {
        'classification': ItemClassification.progression,
        'address': 0x1BA648,
        'value': 0x04
    },
    "SE Sea Chart": {
        'classification': ItemClassification.progression,
        'address': 0x1BA648,
        'value': 0x08,
        'set_bit': [(0x1B557D, 0x8)]
    },
    "NE Sea Chart": {
        'classification': ItemClassification.progression,
        'address': 0x1BA648,
        'value': 0x10
    },

    # ========= Gems ==============

    "Power Gem": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA541,
        'value': 1,
        'incremental': True
    },
    "Wisdom Gem": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA542,
        'value': 1,
        'incremental': True
    },
    "Courage Gem": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA540,
        'value': 1,
        'incremental': True
    },
    "Power Gem Pack": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA541,
        'value': "pack_size",
        'incremental': True
    },
    "Wisdom Gem Pack": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA542,
        'value': "pack_size",
        'incremental': True
    },
    "Courage Gem Pack": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA540,
        'value': "pack_size",
        'incremental': True
    },

    # ========== Rupees and filler =============

    "Green Rupee (1)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 1,
        'incremental': True,
        'size': 2
    },
    "Blue Rupee (5)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 5,
        'incremental': True,
        'size': 2
    },
    "Red Rupee (20)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 20,
        'incremental': True,
        'size': 2,
    },
    "Big Green Rupee (100)": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'address': 0x1BA53E,
        'value': 100,
        'incremental': True,
        'size': 2
    },
    "Big Red Rupee (200)": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'address': 0x1BA53E,
        'value': 200,
        'incremental': True,
        'size': 2
    },
    "Gold Rupee (300)": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'address': 0x1BA53E,
        'value': 300,
        'incremental': True,
        'size': 2
    },
    "Rupoor (-10)": {
        'classification': ItemClassification.trap,
        'address': 0x1BA53E,
        'value': -10,
        'incremental': True,
        'size': 2
    },
    "Big Rupoor (-50)": {
        'classification': ItemClassification.trap,
        'address': 0x1BA53E,
        'value': -50,
        'incremental': True,
        'size': 2
    },
    "Pre-Alpha Rupee (5000)": {
        'classification': ItemClassification.progression,
        'address': 0x1BA53E,
        'value': 5000,
        'incremental': True,
        'size': 2
    },
    "Treasure": {
        'classification': ItemClassification.filler,
        'incremental': True
    },
    "Ship Part": {
        'classification': ItemClassification.filler,
        'ship_part': True
    },
    "Potion": {
        'classification': ItemClassification.filler,
        'dummy': True
    },
    "Red Potion": {
        'classification': ItemClassification.filler,
        'value': 100
    },
    "Purple Potion": {
        'classification': ItemClassification.filler,
        'value': 100
    },
    "Yellow Potion": {
        'classification': ItemClassification.filler,
        'value': 200
    },
    "Nothing!": {
        'classification': ItemClassification.filler,
        'dummy': True
    },
    "Refill: Bombs": {
        'classification': ItemClassification.filler,
        "give_ammo": [10, 20, 30],
        "address": 0x1BA6C0,
        "refill": "Bombs (Progressive)"
    },
    "Refill: Arrows": {
        'classification': ItemClassification.filler,
        "give_ammo": [20, 30, 50],
        "address": 0x1BA6C2,
        "refill": "Bow (Progressive)"
    },
    "Refill: Bombchus": {
        'classification': ItemClassification.filler,
        "give_ammo": [10, 20, 30],
        "address": 0x1BA6C6,
        "refill": "Bombchus (Progressive)"
    },

    # ========= Treasure =============

    "Treasure: Pink Coral": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5AC,
        'incremental': True
    },
    "Treasure: White Pearl Loop": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5AD,
        'incremental': True
    },
    "Treasure: Dark Pearl Loop": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5AE,
        'incremental': True
    },
    "Treasure: Zora Scale": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5AF,
        'incremental': True
    },
    "Treasure: Goron Amber": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5B0,
        'incremental': True
    },
    "Treasure: Ruto Crown": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5B1,
        'incremental': True
    },
    "Treasure: Helmaroc Plume": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5B2,
        'incremental': True
    },
    "Treasure: Regal Ring": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        'address': 0x1BA5B3,
        'incremental': True
    },

    # =============== Treasure Maps ==============

    "Courage Crest": {
        'classification': ItemClassification.progression,
        'address': 0x1B558C,
        'value': 0x04,
        'set_bit': [(0x1BA650, 1)]
    },
    "Treasure Map #1": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba650,
        "value": 0x80,
        "id": 0x42,
        "hint_on_receive": ['Ocean SW Salvage #1 Molida SW'],
    },
    "Treasure Map #2": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba650,
        "value": 0x10,
        "id": 0x43,
        "hint_on_receive": ['Ocean SW Salvage #2 Mercay NE'],
    },
    "Treasure Map #3": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x20,
        "id": 0x44,
        "hint_on_receive": ['Ocean NW Salvage #3 Gusts SW'],
    },
    "Treasure Map #4": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x80,
        "id": 0x45,
        "hint_on_receive": ['Ocean NW Salvage #4 Bannan SE'],
    },
    "Treasure Map #5": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba650,
        "value": 0x40,
        "id": 0x46,
        "hint_on_receive": ['Ocean SW Salvage #5 Molida N'],
    },
    "Treasure Map #6": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x1,
        "id": 0x47,
        "hint_on_receive": ['Ocean NW Salvage #6 Bannan W'],
    },
    "Treasure Map #7": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x8,
        "id": 0x48,
        "hint_on_receive": ['Ocean NW Salvage #7 Gusts E'],
    },
    "Treasure Map #8": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba650,
        "value": 0x8,
        "id": 0x49,
        "hint_on_receive": ['Ocean SW Salvage #8 Mercay SE'],
    },
    "Treasure Map #9": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba650,
        "value": 0x2,
        "id": 0x4a,
        "hint_on_receive": ['Ocean SW Salvage #9 Cannon W'],
    },
    "Treasure Map #10": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x10,
        "id": 0x4b,
        "hint_on_receive": ['Ocean NW Salvage #10 Gusts SE'],
    },
    "Treasure Map #11": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x2,
        "id": 0x4c,
        "hint_on_receive": ['Ocean NW Salvage #11 Gusts N'],
    },
    "Treasure Map #12": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x20,
        "id": 0x4d,
        "hint_on_receive": ['Ocean SE Salvage #12 Dee Ess N'],
    },
    "Treasure Map #13": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x4,
        "id": 0x4e,
        "hint_on_receive": ['Ocean SE Salvage #13 Harrow E'],
    },
    "Treasure Map #14": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x1,
        "id": 0x4f,
        "hint_on_receive": ['Ocean SE Salvage #14 Goron NW'],
    },
    "Treasure Map #15": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x2,
        "id": 0x50,
        "hint_on_receive": ['Ocean SE Salvage #15 Goron W'],
    },
    "Treasure Map #16": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x10,
        "id": 0x51,
        "hint_on_receive": ['Ocean SE Salvage #16 Goron NE'],
    },
    "Treasure Map #17": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x40,
        "id": 0x52,
        "hint_on_receive": ['Ocean SE Salvage #17 Frost S'],
    },
    "Treasure Map #18": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba650,
        "value": 0x4,
        "id": 0x53,
        "hint_on_receive": ['Ocean SW Salvage #18 Cannon S'],
    },
    "Treasure Map #19": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x4,
        "id": 0x54,
        "hint_on_receive": ['Ocean NW Salvage #19 Gusts NE'],
    },
    "Treasure Map #20": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba651,
        "value": 0x40,
        "id": 0x55,
        "hint_on_receive": ['Ocean NW Salvage #20 Bannan E'],
    },
    "Treasure Map #21": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba650,
        "value": 0x20,
        "id": 0x56,
        "hint_on_receive": ['Ocean SW Salvage #21 Molida NW'],
    },
    "Treasure Map #22": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x8,
        "id": 0x57,
        "hint_on_receive": ['Ocean SE Salvage #22 Harrow S'],
    },
    "Treasure Map #23": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba652,
        "value": 0x80,
        "id": 0x58,
        "hint_on_receive": ['Ocean SE Salvage #23 Frost NW'],
    },
    "Treasure Map #24": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x2,
        "id": 0x59,
        "hint_on_receive": ['Ocean NE Salvage #24 Ruins W'],
    },
    "Treasure Map #25": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x4,
        "id": 0x5a,
        "hint_on_receive": ['Ocean NE Salvage #25 Dead E'],
    },
    "Treasure Map #26": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x20,
        "id": 0x5b,
        "hint_on_receive": ['Ocean NE Salvage #26 Ruins SW'],
    },
    "Treasure Map #27": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x8,
        "id": 0x5c,
        "hint_on_receive": ['Ocean NE Salvage #27 Maze E'],
    },
    "Treasure Map #28": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x1,
        "id": 0x5d,
        "hint_on_receive": ['Ocean NE Salvage #28 Ruins NW'],
    },
    "Treasure Map #29": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x10,
        "id": 0x5e,
        "hint_on_receive": ['Ocean NE Salvage #29 Maze W'],
    },
    "Treasure Map #30": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x40,
        "id": 0x5f,
        "hint_on_receive": ['Ocean NE Salvage #30 Ruins S'],
    },
    "Treasure Map #31": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba653,
        "value": 0x80,
        "id": 0x60,
        "hint_on_receive": ['Ocean NE Salvage #31 Dead S'],
    },


    # =========== Keys ============

    "Small Key (Mountain Passage)": {
        'classification': ItemClassification.progression,
        'dungeon': 39,
        'incremental': True
    },
    "Small Key (Temple of the Ocean King)": {
        'classification': ItemClassification.progression,
        'dungeon': 37,
        'incremental': True
    },
    "Small Key (Temple of Fire)": {
        'classification': ItemClassification.progression,
        'dungeon': 0x1C,
        'incremental': True
    },
    "Small Key (Temple of Wind)": {
        'classification': ItemClassification.progression,
        'dungeon': 0x1D,
        'incremental': True
    },
    "Small Key (Temple of Courage)": {
        'classification': ItemClassification.progression,
        'dungeon': 0x1E,
        'incremental': True
    },
    "Small Key (Temple of Ice)": {
        'classification': ItemClassification.progression,
        'dungeon': 0x1F,
        'incremental': True
    },
    "Small Key (Mutoh's Temple)": {
        'classification': ItemClassification.progression,
        'dungeon': 0x21,
        'incremental': True
    },
    "Boss Key (Temple of Fire)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True
    },
    "Boss Key (Temple of Wind)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': 0x1D,
        'dummy': True
    },
    "Boss Key (Temple of Courage)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True
    },
    "Boss Key (Goron Temple)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True
    },
    "Boss Key (Temple of Ice)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True
    },
    "Boss Key (Mutoh's Temple)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True
    },
    "Square Crystal (Temple of Courage)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True,
    },
    "Triangle Crystal (Ghost Ship)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True,
    },
    "Round Crystal (Ghost Ship)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dungeon': True,
        'dummy': True,
    },
    "Round Crystal (Temple of the Ocean King)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dummy': True,
        'dungeon': 37,
    },
    "Triangle Crystal (Temple of the Ocean King)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dummy': True,
        'dungeon': 37,
    },
    "Force Gem (B3)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dummy': True,
        'dungeon': 37,
    },
    "Force Gem (B12)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dummy': True,
        'dungeon': 37,
    },
    "Triforce Crest": {
        'classification': ItemClassification.progression,
        'address': 0x1B5580,
        'value': 0x02
    },
    "Sun Key": {
        'classification': ItemClassification.progression,
        'address': 0x1BA648,
        'value': 0x40
    },
    "Ghost Key": {
        'classification': ItemClassification.progression,
        'address': 0x1BA649,
        'value': 0x08
    },
    "King's Key": {
        'classification': ItemClassification.progression,
        'address': 0x1BA649,
        'value': 0x04
    },
    "Regal Necklace": {
        'classification': ItemClassification.progression,
        'address': 0x1B5582,
        'value': 0x08
    },
    "Crimzonine": {
        'classification': ItemClassification.progression,
        "address": 0x1B558B,
        "value": 0x40
    },
    "Azurine": {
        'classification': ItemClassification.progression,
        "address": 0x1B558B,
        "value": 0x20
    },
    "Aquanine": {
        'classification': ItemClassification.progression,
        "address": 0x1B558B,
        "value": 0x80
    },
    "Rare Metal": {
        'classification': ItemClassification.progression,
        'dummy': True
    },
    "Additional Rare Metal": {
        'classification': ItemClassification.progression,
        'dummy': True
    },
    # Trade Quest and misc

    "Hero's New Clothes": {
        'classification': ItemClassification.progression,
        'address': 0x1B5590,
        'value': 0x4
    },
    "Kaleidoscope": {
        'classification': ItemClassification.progression,
        'address': 0x1B5590,
        'value': 0x8
    },
    "Guard Notebook": {
        'classification': ItemClassification.progression,
        'address': 0x1B5590,
        'value': 0x10
    },
    "Wood Heart": {
        'classification': ItemClassification.progression,
        'address': 0x1B5590,
        'value': 0x80
    },
    "Phantom Blade": {
        'classification': ItemClassification.progression,
        'address': 0x1B5592,
        'value': 0x20
    },

    # Frogs
    "Golden Frog Glyph X": {
        'classification': ItemClassification.progression,
        'address': 0x1B55A2,
        'value': 0x80
    },
    "Golden Frog Glyph Phi": {
        'classification': ItemClassification.progression,
        'address': 0x1B55A3,
        'value': 0x01
    },
    "Golden Frog Glyph N": {
        'classification': ItemClassification.progression,
        'address': 0x1B55A3,
        'value': 0x02
    },
    "Golden Frog Glyph Omega": {
        'classification': ItemClassification.useful,
        'address': 0x1B55A3,
        'value': 0x04
    },
    "Golden Frog Glyph W": {
        'classification': ItemClassification.useful,
        'address': 0x1B55A3,
        'value': 0x08
    },
    "Golden Frog Glyph Square": {
        'classification': ItemClassification.progression,
        'address': 0x1B55A3,
        'value': 0x10
    },

    # Ships
    "Ship: Bright Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 1
    },
    "Ship: Iron Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 2
    },
    "Ship: Stone Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 3
    },
    "Ship: Vintage Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 4
    },
    "Ship: Demon Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 5
    },
    "Ship: Tropical Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 6
    },
    "Ship: Dignified Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 7
    },
    "Ship: Golden Ship": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'ship': 8
    },
    # Fish
    "Fish: Skippyjack": {
        'classification': ItemClassification.filler,
        'address': 0x1BA5B4,
        'value': 1,
        'incremental': True,
        'size': 1
    },
    "Fish: Toona": {
        'classification': ItemClassification.filler,
        'address': 0x1BA5B5,
        'value': 1,
        'incremental': True,
        'size': 1
    },
    "Fish: Loovar": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA5B6,
        'value': 1,
        'incremental': True,
        'size': 1
    },
    "Fish: Rusty Swordfish": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA5B7,
        'value': 1,
        'incremental': True,
        'size': 1
    },
    "Fish: Legendary Neptoona": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA5B8,
        'value': 1,
        'incremental': True,
        'size': 1
    },
    "Fish: Stowfish": {
        'classification': ItemClassification.progression_skip_balancing,
        'address': 0x1BA5B9,
        'value': 1,
        'incremental': True,
        'size': 1
    },
    "_UT_Glitched_logic": {
        'classification': ItemClassification.progression,
        'dummy': True
    }
}


# Oops apparently not a constant lul (it will be after this)
for i, k in enumerate(ITEMS_DATA):
    ITEMS_DATA[k]["id"] = i+1

if __name__ == "__main__":
    for name, data in ITEMS_DATA.items():
        if "Treasure Map" in name:
            i = int(name[name.find("#")+1:])

            loc = LOCATION_GROUPS["Salvage Locations"][i-1]
            data["hint_on_receive"] = [loc]
            print(f"\t\"{name}\": " + "{")
            for key, value in data.items():
                if type(value) is str:
                    print(f"\t\t\"{key}\": \"{value}\",")
                elif key == "classification":
                    print(f"\t\t\"{key}\": ItemClassification.progression_skip_balancing,")
                elif type(value) is int:
                    print(f"\t\t\"{key}\": {hex(value)},")
                elif key != "id":
                    print(f"\t\t\"{key}\": {value},")
            print("\t},")

