from BaseClasses import ItemClassification
from worlds.tloz_ph.data.Constants import *


"""backwards-compatible fallback for AP v0.6.2 and prior
Code idea from @eternalcode0s minish cap implementation
"""
try:
    DEPRIORITIZED_SKIP_BALANCING_FALLBACK = ItemClassification.progression_deprioritized_skip_balancing
    DEPRIORITIZED_FALLBACK = ItemClassification.progression_deprioritized
except AttributeError as e:
    DEPRIORITIZED_SKIP_BALANCING_FALLBACK = ItemClassification.progression_skip_balancing
    DEPRIORITIZED_FALLBACK = ItemClassification.progression

ITEMS_DATA = {
    #   "Item Name": {
    #   'classification': ItemClassification,   # classification category
    #   'address': int,                         # address in memory. not used if progressive
    #   'value': int,                           # value to set in memory, if incremental added else bitwise or
    #   'incremental': bool                     # true for positive, False for negative
    #   'progressive': list[tuple[int, int]]    # address, value for each progressive stage
    #   'size': int,                            # size in bytes
    #   'set_bit': list[tuple[int, int]],       # for setting additional bits on acquisition
    #   'give_ammo': list[int]                  # how much ammo to give for each progressive stage
    #   'ammo_address': int                     # address for ammo
    #   'progressive_overwrite':                # for setting progressive stages as overwrites instead of bitwise or.
    # used for ammo upgrades cause setting the upgrade to 3 rather than 1 or 2 creates a glitched ammo upgrade
    #   'id': int                               # item id. no longer generated automatically :(
    #   'ammo_address': int                     # address for ammo
    #   'dungeon': int                          # Stage id for items tied to specific dungeons, like small keys
    #   'dummy': bool                           # ignores all item writing operations. Used for big keys and abstracts
    #   'force_vanilla': bool                   # forces item to be in it's vanilla location, probably not used?
    #   'hint_on_receive': list[str]            # locations to hint if conditions are met
    #   'ship': int                             # ship id for ships
    #   'refill': str                      # progressive item to draw data from
    #   'treasure': bool                   # treasure item tag
    #   'backup_filler': bool              # if item can safely be classified as filler when the filler pool runs out
    #    },

    # ======= Regular Items==========

    # Link items
    "Sword (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1ba644, 0x1), (0x1ba648, 0x20)],
        "set_bit": [(0x1ba644, 0x1), (0x1ba6b8, 1)],
        "id": 1,
    },
    "Oshus' Sword": {
        "classification": ItemClassification.progression,
        "address": 0x1ba644,
        "value": 0x1,
        "ammo_address": 0x1ba6b8,  # used to remove sword model
        "set_bit": [(0x1ba6b8, 1)],
        "id": 2,
    },
    "Phantom Sword": {
        "classification": ItemClassification.progression,
        "address": 0x1ba648,
        "value": 0x20,
        "id": 3,
    },
    "Shield": {
        "classification": ItemClassification.progression,
        "address": 0x1ba644,
        "value": 0x2,
        "id": 4,
    },
    "Boomerang": {
        "classification": ItemClassification.progression,
        "address": 0x1ba644,
        "value": 0x4,
        "set_bit": [(0x1ba6bc, 0x1)],
        "id": 5,
        "inventory_id": 2,
    },
    "Bombs (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1ba644, 0x10), (0x1ba5d2, 0x1), (0x1ba5d2, 0x2)],
        "progressive_overwrite": True,
        "give_ammo": [0xa, 0x14, 0x1e],
        "ammo_address": 0x1ba6c0,
        "set_bit": [(0x1ba644, 0x10)],
        "id": 6,
        "inventory_id": 4,
    },
    "Bombchus (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1ba644, 0x80), (0x1ba5d4, 0x1), (0x1ba5d4, 0x2)],
        "give_ammo": [0xa, 0x14, 0x1e],
        "ammo_address": 0x1ba6c6,
        "progressive_overwrite": True,
        "set_bit": [(0x1ba644, 0x80)],
        "id": 7,
        "inventory_id": 7,
    },
    "Bow (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1ba644, 0x20), (0x1ba5d0, 0x1), (0x1ba5d0, 0x2)],
        "give_ammo": [0x14, 0x1e, 0x32],
        "ammo_address": 0x1ba6c2,
        "progressive_overwrite": True,
        "set_bit": [(0x1ba644, 0x20)],
        "id": 8,
        "inventory_id": 5,
    },
    "Grappling Hook": {
        "classification": ItemClassification.progression,
        "address": 0x1ba644,
        "value": 0x40,
        "set_bit": [(0x1ba6c4, 0x1)],
        "id": 9,
        "inventory_id": 6,
    },
    "Shovel": {
        "classification": ItemClassification.progression,
        "address": 0x1ba644,
        "value": 0x8,
        "set_bit": [(0x1ba6be, 0x1)],
        "id": 10,
        "inventory_id": 3,
    },
    "Hammer": {
        "classification": ItemClassification.progression,
        "address": 0x1ba645,
        "value": 0x1,
        "set_bit": [(0x1ba6c8, 0x1)],
        "id": 11,
        "inventory_id": 8,
    },

    # Spirits
    "Spirit of Power (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1ba646, 0x20), (0x1ba647, 0x1), (0x1ba647, 0x8)],
        "id": 12,
    },
    "Spirit of Wisdom (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1ba646, 0x40), (0x1ba647, 0x2), (0x1ba647, 0x10)],
        "id": 13,
    },
    "Spirit of Courage (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1ba646, 0x10), (0x1ba646, 0x80), (0x1ba647, 0x4)],
        "id": 14,
    },
    "Spirit of Courage (White)": {  # Used to remove spirit from Temple of Courage
        "classification": ItemClassification.progression,
        "address": 0x1BA647,
        "value": 0x20,
        "id": 15,
    },

    # Upgrades
    "Heart Container": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba388,
        "value": 0x4,
        "incremental": True,
        "size": 2,
        "id": 16,
    },
    "Phantom Hourglass": {
        "classification": ItemClassification.progression,
        "address": 0x1ba528,
        "value": "Sand PH",
        "incremental": True,
        "size": 4,
        "id": 17,
    },
    "Sand of Hours (Boss)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "address": 0x1ba528,
        "value": 0x1c20,
        "incremental": True,
        "size": 4,
        "id": 18,
    },
    "Sand of Hours (Small)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "address": 0x1ba528,
        "value": 0xe10,
        "incremental": True,
        "size": 4,
        "id": 19,
    },
    "Sand of Hours": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba528,
        "value": "Sand",
        "incremental": True,
        "size": 4,
        "id": 20,
    },
    "Swordsman's Scroll": {
        "classification": ItemClassification.useful,
        "address": 0x1ba649,
        "value": 0x20,
        "id": 21,
    },

    # Ship Items
    "Cannon": {
        "classification": ItemClassification.progression,
        "address": 0x1b5582,
        "value": 0x1,
        "id": 22,
    },
    "Salvage Arm": {
        "classification": ItemClassification.progression,
        "address": 0x1ba649,
        "value": 0x10,
        "id": 23,
    },
    "Fishing Rod": {
        "classification": ItemClassification.progression,
        "address": 0x1ba649,
        "value": 0x1,
        "id": 24,
    },
    "Big Catch Lure": {
        "classification": ItemClassification.progression,
        "address": 0x1ba649,
        "value": 0x80,
        "id": 25,
    },
    "Swordfish Shadows": {
        "classification": ItemClassification.progression,
        "address": 0x1b55a7,
        "value": 0x10,
        "id": 26,
    },
    "Cyclone Slate": {
        "classification": ItemClassification.progression,
        "address": 0x1ba649,
        "value": 0x40,
        "id": 27,
    },

    # Sea Charts
    "SW Sea Chart": {
        "classification": ItemClassification.progression,
        "address": 0x1ba648,
        "value": 0x2,
        "id": 28,
    },
    "NW Sea Chart": {
        "classification": ItemClassification.progression,
        "address": 0x1ba648,
        "value": 0x4,
        "id": 29,
    },
    "SE Sea Chart": {
        "classification": ItemClassification.progression,
        "address": 0x1ba648,
        "value": 0x8,
        "set_bit": [(0x1b557d, 0x8)],
        "id": 30,
    },
    "NE Sea Chart": {
        "classification": ItemClassification.progression,
        "address": 0x1ba648,
        "value": 0x10,
        "id": 31,
    },

    # Spirit gems
    "Power Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": 0x1ba541,
        "value": 0x1,
        "incremental": True,
        "id": 32,
    },
    "Wisdom Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": 0x1ba542,
        "value": 0x1,
        "incremental": True,
        "id": 33,
    },
    "Courage Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": 0x1ba540,
        "value": 0x1,
        "incremental": True,
        "id": 34,
    },
    "Power Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba541,
        "value": "pack_size",
        "incremental": True,
        "id": 35,
    },
    "Wisdom Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba542,
        "value": "pack_size",
        "incremental": True,
        "id": 36,
    },
    "Courage Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba540,
        "value": "pack_size",
        "incremental": True,
        "id": 37,
    },

    # Rupees and filler
    "Green Rupee (1)": {
        "classification": ItemClassification.filler,
        "address": 0x1ba53e,
        "value": 0x1,
        "incremental": True,
        "size": 2,
        "id": 38,
    },
    "Blue Rupee (5)": {
        "classification": ItemClassification.filler,
        "address": 0x1ba53e,
        "value": 0x5,
        "incremental": True,
        "size": 2,
        "id": 39,
    },
    "Red Rupee (20)": {
        "classification": ItemClassification.filler,
        "address": 0x1ba53e,
        "value": 0x14,
        "incremental": True,
        "size": 2,
        "id": 40,
    },
    "Big Green Rupee (100)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "address": 0x1ba53e,
        "value": 0x64,
        "incremental": True,
        "size": 2,
        "id": 41,
    },
    "Big Red Rupee (200)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "address": 0x1ba53e,
        "value": 0xc8,
        "incremental": True,
        "size": 2,
        "id": 42,
    },
    "Gold Rupee (300)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "address": 0x1ba53e,
        "value": 0x12c,
        "incremental": True,
        "size": 2,
        "id": 43
    },
    "Rupoor (-10)": {
        "classification": ItemClassification.trap,
        "address": 0x1ba53e,
        "value": -0xa,
        "incremental": True,
        "size": 2,
        "id": 44,
    },
    "Big Rupoor (-50)": {
        "classification": ItemClassification.trap,
        "address": 0x1ba53e,
        "value": -0x32,
        "incremental": True,
        "size": 2,
        "id": 45,
    },
    "Pre-Alpha Rupee (5000)": {
        "classification": ItemClassification.progression,
        "address": 0x1ba53e,
        "value": 0x1388,
        "incremental": True,
        "size": 2,
        "id": 46,
    },
    "Treasure": {
        "classification": ItemClassification.filler,
        "incremental": True,
        "id": 47,
    },
    "Ship Part": {
        "classification": ItemClassification.filler,
        "ship_part": True,
        "id": 48,
    },
    "Potion": {
        "classification": ItemClassification.filler,
        "dummy": True,
        "id": 49,
    },
    "Red Potion": {
        "classification": ItemClassification.filler,
        "value": 0x64,
        "id": 50,
    },
    "Purple Potion": {
        "classification": ItemClassification.filler,
        "value": 0x64,
        "id": 51,
    },
    "Yellow Potion": {
        "classification": ItemClassification.filler,
        "value": 0xc8,
        "id": 52,
    },
    "Nothing!": {
        "classification": ItemClassification.filler,
        "dummy": True,
        "id": 53,
    },
    "Refill: Bombs": {
        "classification": ItemClassification.filler,
        "give_ammo": [0xa, 0x14, 0x1e],
        "address": 0x1ba6c0,
        "refill": "Bombs (Progressive)",
        "id": 54,
    },
    "Refill: Arrows": {
        "classification": ItemClassification.filler,
        "give_ammo": [0x14, 0x1e, 0x32],
        "address": 0x1ba6c2,
        "refill": "Bow (Progressive)",
        "id": 55,
    },
    "Refill: Bombchus": {
        "classification": ItemClassification.filler,
        "give_ammo": [0xa, 0x14, 0x1e],
        "address": 0x1ba6c6,
        "refill": "Bombchus (Progressive)",
        "id": 56,
    },
    "Salvage Repair Kit": {
        "classification": ItemClassification.filler,
        "address": 0x1ba661,
        "value": 0x1,
        "id": 57,
        "max": 0x7
    },
    "Refill: Health": {
        "classification": ItemClassification.filler,
        "value": "full_heal",
        "id": 193,
    },

    # Treasure
    "Treasure: Pink Coral": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5ac,
        "incremental": True,
        "id": 58,
    },
    "Treasure: White Pearl Loop": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5ad,
        "incremental": True,
        "id": 59,
    },
    "Treasure: Dark Pearl Loop": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5ae,
        "incremental": True,
        "id": 60,
    },
    "Treasure: Zora Scale": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5af,
        "incremental": True,
        "id": 61,
    },
    "Treasure: Goron Amber": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5b0,
        "incremental": True,
        "id": 62,
    },
    "Treasure: Ruto Crown": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5b1,
        "incremental": True,
        "id": 63,
    },
    "Treasure: Helmaroc Plume": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5b2,
        "incremental": True,
        "id": 64,
    },
    "Treasure: Regal Ring": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "backup_filler": True,
        "treasure": True,
        "address": 0x1ba5b3,
        "incremental": True,
        "id": 65,
    },

    # Salvage
    "Courage Crest": {
        "classification": ItemClassification.progression,
        "address": 0x1b558c,
        "value": 0x4,
        "set_bit": [(0x1ba650, 0x1)],
        "id": 66,
    },
    "Treasure Map #1 (Molida SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba650,
        "value": 0x80,
        "id": 67,
        "hint_on_receive": ["Ocean SW Salvage #1 Molida SW"],
    },
    "Treasure Map #2 (Mercay NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba650,
        "value": 0x10,
        "id": 68,
        "hint_on_receive": ["Ocean SW Salvage #2 Mercay NE"],
    },
    "Treasure Map #3 (Gusts SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x20,
        "id": 69,
        "hint_on_receive": ["Ocean NW Salvage #3 Gusts SW"],
    },
    "Treasure Map #4 (Bannan SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x80,
        "id": 70,
        "hint_on_receive": ["Ocean NW Salvage #4 Bannan SE"],
    },
    "Treasure Map #5 (Molida N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba650,
        "value": 0x40,
        "id": 71,
        "hint_on_receive": ["Ocean SW Salvage #5 Molida N"],
    },
    "Treasure Map #6 (Bannan W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x1,
        "id": 72,
        "hint_on_receive": ["Ocean NW Salvage #6 Bannan W"],
    },
    "Treasure Map #7 (Gusts E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x8,
        "id": 73,
        "hint_on_receive": ["Ocean NW Salvage #7 Gusts E"],
    },
    "Treasure Map #8 (Mercay SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba650,
        "value": 0x8,
        "id": 74,
        "hint_on_receive": ["Ocean SW Salvage #8 Mercay SE"],
    },
    "Treasure Map #9 (Cannon W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba650,
        "value": 0x2,
        "id": 75,
        "hint_on_receive": ["Ocean SW Salvage #9 Cannon W"],
    },
    "Treasure Map #10 (Gusts SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x10,
        "id": 76,
        "hint_on_receive": ["Ocean NW Salvage #10 Gusts SE"],
    },
    "Treasure Map #11 (Gusts N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x2,
        "id": 77,
        "hint_on_receive": ["Ocean NW Salvage #11 Gusts N"],
    },
    "Treasure Map #12 (Dee Ess N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x20,
        "id": 78,
        "hint_on_receive": ["Ocean SE Salvage #12 Dee Ess N"],
    },
    "Treasure Map #13 (Harrow E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x4,
        "id": 79,
        "hint_on_receive": ["Ocean SE Salvage #13 Harrow E"],
    },
    "Treasure Map #14 (Goron NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x1,
        "id": 80,
        "hint_on_receive": ["Ocean SE Salvage #14 Goron NW"],
    },
    "Treasure Map #15 (Goron W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x2,
        "id": 81,
        "hint_on_receive": ["Ocean SE Salvage #15 Goron W"],
    },
    "Treasure Map #16 (Goron NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x10,
        "id": 82,
        "hint_on_receive": ["Ocean SE Salvage #16 Goron NE"],
    },
    "Treasure Map #17 (Frost S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x40,
        "id": 83,
        "hint_on_receive": ["Ocean SE Salvage #17 Frost S"],
    },
    "Treasure Map #18 (Cannon S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba650,
        "value": 0x4,
        "id": 84,
        "hint_on_receive": ["Ocean SW Salvage #18 Cannon S"],
    },
    "Treasure Map #19 (Gusts NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x4,
        "id": 85,
        "hint_on_receive": ["Ocean NW Salvage #19 Gusts NE"],
    },
    "Treasure Map #20 (Bannan E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba651,
        "value": 0x40,
        "id": 86,
        "hint_on_receive": ["Ocean NW Salvage #20 Bannan E"],
    },
    "Treasure Map #21 (Molida NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba650,
        "value": 0x20,
        "id": 87,
        "hint_on_receive": ["Ocean SW Salvage #21 Molida NW"],
    },
    "Treasure Map #22 (Harrow S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x8,
        "id": 88,
        "hint_on_receive": ["Ocean SE Salvage #22 Harrow S"],
    },
    "Treasure Map #23 (Frost NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba652,
        "value": 0x80,
        "id": 89,
        "hint_on_receive": ["Ocean SE Salvage #23 Frost NW"],
    },
    "Treasure Map #24 (Ruins W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x20,
        "id": 90,
        "hint_on_receive": ["Ocean NE Salvage #24 Ruins W"],
    },
    "Treasure Map #25 (Dead E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x4,
        "id": 91,
        "hint_on_receive": ["Ocean NE Salvage #25 Dead E"],
    },
    "Treasure Map #26 (Ruins SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x2,
        "id": 92,
        "hint_on_receive": ["Ocean NE Salvage #26 Ruins SW"],
    },
    "Treasure Map #27 (Maze E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x8,
        "id": 93,
        "hint_on_receive": ["Ocean NE Salvage #27 Maze E"],
    },
    "Treasure Map #28 (Ruins NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x1,
        "id": 94,
        "hint_on_receive": ["Ocean NE Salvage #28 Ruins NW"],
    },
    "Treasure Map #29 (Maze W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x10,
        "id": 95,
        "hint_on_receive": ["Ocean NE Salvage #29 Maze W"],
    },
    "Treasure Map #30 (Ruins S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x40,
        "id": 96,
        "hint_on_receive": ["Ocean NE Salvage #30 Ruins S"],
    },
    "Treasure Map #31 (Dead S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": 0x1ba653,
        "value": 0x80,
        "id": 97,
        "hint_on_receive": ["Ocean NE Salvage #31 Dead S"],
    },

    # Keys
    "Small Key (Mountain Passage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x27,
        "incremental": True,
        "id": 98,
    },
    "Small Key (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x25,
        "incremental": True,
        "id": 99,
    },
    "Small Key (Temple of Fire)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1c,
        "incremental": True,
        "id": 100,
    },
    "Small Key (Temple of Wind)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1d,
        "incremental": True,
        "id": 101,
    },
    "Small Key (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1e,
        "incremental": True,
        "id": 102,
    },
    "Small Key (Temple of Ice)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1f,
        "incremental": True,
        "id": 103,
    },
    "Small Key (Mutoh's Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x21,
        "incremental": True,
        "id": 104,
    },
    "Boss Key (Temple of Fire)": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "id": 105,
        "always_process": True
    },
    "Boss Key (Temple of Wind)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1d,
        "id": 106,
        "always_process": True
    },
    "Boss Key (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "id": 107,
        "always_process": True
    },
    "Boss Key (Goron Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "id": 108,
        "always_process": True
    },
    "Boss Key (Temple of Ice)": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "id": 109,
        "always_process": True
    },
    "Boss Key (Mutoh's Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "id": 110,
        "always_process": True
    },
    "Square Crystal (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "always_process": True,
        "id": 111,
        "set_bit_in_room": {0x1E00: [(0x252264, 0x10),
                                     ("stage_flag", 0x80)]}
    },
    "Square Pedestal North (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": True,
        "id": 194,
        "set_bit_in_room": {0x1E00: [(0x252264, 0x10)]}
    },
    "Square Pedestal South (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": True,
        "id": 195,
        "set_bit_in_room": {0x1E00: [("stage_flag", 0x80)]}
    },
    "Triangle Crystal (Ghost Ship)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": True,
        "id": 112,
        "set_bit_in_room": {0x2900: [("stage_flag", [0, 8])]}
    },
    "Round Crystal (Ghost Ship)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": True,
        "id": 113,
        "set_bit_in_room": {0x2900: [("stage_flag", [0, 0, 0, 2])]}
    },
    "Round Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 114,
        "set_bit_in_room": {0x250B: [(0x25762C, 0x2)],  # format: dict[room, list[tuple[addr, value, *dict(extra data)]]]
                            0x250C: [(0x257694, 0x4)]}
    },
    "Round Pedestal B8 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 196,
        "set_bit_in_room": {0x250B: [(0x25762C, 0x2)]}
    },
    "Round Pedestal B9 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 197,
        "set_bit_in_room": {0x250C: [(0x257694, 0x4)]}
    },
    "Round Crystals": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 204,
        "set_bit_in_room": {0x250B: [(0x25762C, 0x2)],
                            0x250C: [(0x257694, 0x4)],
                            0x2900: [("stage_flag", [0, 0, 0, 2])]}
    },
    "Triangle Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 115,
        "set_bit_in_room": {0x250B: [(0x25762C, 0x4)],
                            0x250C: [(0x257694, 0x8)]}
    },
    "Triangle Pedestal B8 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 198,
        "set_bit_in_room": {0x250B: [(0x25762C, 0x4)]}
    },
    "Triangle Pedestal B9 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 199,
        "set_bit_in_room": {0x250C: [(0x257694, 0x8)]}
    },
    "Triangle Crystals": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 203,
        "set_bit_in_room": {0x250B: [(0x25762C, 0x4)],
                            0x250C: [(0x257694, 0x8)],
                            0x2900: [("stage_flag", [0, 8])]}
    },
    "Square Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": True,
        "id": 116,
        "set_bit_in_room": {0x250C: [(0x257694, 0x22)]}
    },
    "Square Pedestal West (Temple of the Ocean King)": {
        "classification": ItemClassification.useful,
        "always_process": True,
        "dungeon": True,
        "id": 200,
        "set_bit_in_room": {0x250C: [(0x257694, 0x20)]}
    },
    "Square Pedestal Center (Temple of the Ocean King)": {
        "classification": ItemClassification.useful,
        "always_process": True,
        "dungeon": True,
        "id": 201,
        "set_bit_in_room": {0x250C: [(0x257694, 0x2)]}
    },
    "Square Crystals": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "always_process": True,
        "id": 202,
        "set_bit_in_room": {0x250C: [(0x257694, 0x22)],
                            0x1E00: [(0x252264, 0x10),
                                     ("stage_flag", 0x80)]}
    },
    "Force Gem (B3)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 117,
        "set_bit_in_room": {0x2503: [(0x2572EC, 0xFE, {"count": 3}),
                                     (0x2572ED, 0xF, {"count": 3})]}
    },
    "Force Gem (B12)": {
        "classification": ItemClassification.progression,
        "always_process": True,
        "dungeon": 0x25,
        "id": 118,
        "set_bit_in_room": {0x2510: [(0x257834, 0xFE, {"count": 3}),
                                     (0x257835, 0xF, {"count": 3}),
                                     (0x257834, 0xC, {"count": 2}),
                                     (0x257834, 0x4, {"count": 1})]}
    },
    "Force Gems": {
        "classification": ItemClassification.progression,
        "id": 205,
        "always_process": True,
        "set_bit_in_room": {0x2503: [(0x2572EC, 0xFE),
                                     (0x2572ED, 0xF)],
                            0x2510: [(0x257834, 0xFE),
                                     (0x257835, 0xF)]}
    },
    "Triforce Crest": {
        "classification": ItemClassification.progression,
        "address": 0x1b5580,
        "value": 0x2,
        "id": 119,
    },
    "Sun Key": {
        "classification": ItemClassification.progression,
        "address": 0x1ba648,
        "value": 0x40,
        "id": 120,
    },
    "Ghost Key": {
        "classification": ItemClassification.progression,
        "address": 0x1ba649,
        "value": 0x8,
        "id": 121,
    },
    "King's Key": {
        "classification": ItemClassification.progression,
        "address": 0x1ba649,
        "value": 0x4,
        "id": 122,
    },
    "Regal Necklace": {
        "classification": ItemClassification.progression,
        "address": 0x1b5582,
        "value": 0x8,
        "id": 123,
    },

    # Metals
    "Crimzonine": {
        "classification": ItemClassification.progression,
        "address": 0x1b558b,
        "value": 0x40,
        "id": 124,
    },
    "Azurine": {
        "classification": ItemClassification.progression,
        "address": 0x1b558b,
        "value": 0x20,
        "id": 125,
    },
    "Aquanine": {
        "classification": ItemClassification.progression,
        "address": 0x1b558b,
        "value": 0x80,
        "id": 126,
    },
    "Rare Metal": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 127,
    },
    "Additional Rare Metal": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 128,
    },
    "Verdanine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 129,
    },
    "Lavendine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 130,
    },
    "Amberine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 131,
    },
    "Vermilline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 132,
    },
    "Burgundine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 133,
    },
    "Crystaline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 134,
    },
    "Carrotine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 135,
    },
    "Olivine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 136,
    },
    "Chartreusine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 137,
    },
    "Violetine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 138,
    },
    "Ceruline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 139,
    },
    "Fuchsianine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 140,
    },
    "Saffrine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 141,
    },
    "Sepianine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 142,
    },
    "Apricotine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 143,
    },
    "Scarletine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 144,
    },
    "Coraline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 145,
    },
    "Magentine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 146,
    },
    "Cyanine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 147,
    },
    "Mauvine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 148,
    },
    "Indigorine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 149,
    },
    "Junipine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 150,
    },
    "Viridine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 151,
    },
    "Limeinine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 152,
    },
    "Mintine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 153,
    },
    "Umberine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 154,
    },
    "Lilacine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 155,
    },
    "Saffronine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 156,
    },

    # Trade Quest
    "Hero's New Clothes": {
        "classification": ItemClassification.progression,
        "address": 0x1b5590,
        "value": 0x4,
        "id": 157,
    },
    "Kaleidoscope": {
        "classification": ItemClassification.progression,
        "address": 0x1b5590,
        "value": 0x8,
        "id": 158,
    },
    "Guard Notebook": {
        "classification": ItemClassification.progression,
        "address": 0x1b5590,
        "value": 0x10,
        "id": 159,
    },
    "Wood Heart": {
        "classification": ItemClassification.progression,
        "address": 0x1b5590,
        "value": 0x80,
        "id": 160,
    },
    "Phantom Blade": {
        "classification": ItemClassification.progression,
        "address": 0x1b5592,
        "value": 0x20,
        "id": 161,
    },

    # Letters and cards
    "Freebie Card": {
        "classification": ItemClassification.progression,
        "address": 0x1b558a,
        "value": 0x40,
        "id": 162,
        "backup_filler": True
    },
    "Member's Card (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(0x1B5588, 0x40), (0x1b558e, 0x20), (0x1b558e, 0x40), (0x1b558e, 0x80), (0x1b558f, 0x1)],
        "id": 163,
    },
    "Complimentary Card": {
        "classification": ItemClassification.filler,
        "address": 0x1b558a,
        "value": 0x20,
        "id": 164,
    },
    "Compliment Card": {
        "classification": ItemClassification.filler,
        "address": 0x1b558a,
        "value": 0x80,
        "id": 190,
    },
    "Jolene's Letter": {
        "classification": ItemClassification.progression,
        "address": 0x1b5590,
        "value": 0x20,
        "id": 165,
    },
    "Prize Postcard": {
        "classification": ItemClassification.filler,
        "address": 0x1b558f,
        "value": 0x8,
        "id": 166,
    },
    "Beedle Points (10)": {
        "classification": ItemClassification.progression,
        "address": 0x1B2773,
        "value": 10,
        "id": 167,
    },
    "Beedle Points (20)": {
        "classification": ItemClassification.progression,
        "address": 0x1B2773,
        "value": 20,
        "id": 191,
    },
    "Beedle Points (50)": {
        "classification": ItemClassification.progression,
        "address": 0x1B2773,
        "value": 50,
        "id": 192,
    },

    # Frogs
    "Golden Frog Glyph X": {
        "classification": ItemClassification.progression,
        "address": 0x1b55a2,
        "value": 0x80,
        "id": 168,
    },
    "Golden Frog Glyph Phi": {
        "classification": ItemClassification.progression,
        "address": 0x1b55a3,
        "value": 0x1,
        "id": 169,
    },
    "Golden Frog Glyph N": {
        "classification": ItemClassification.progression,
        "address": 0x1b55a3,
        "value": 0x2,
        "id": 170,
    },
    "Golden Frog Glyph Omega": {
        "classification": ItemClassification.useful,
        "address": 0x1b55a3,
        "value": 0x4,
        "id": 171,
    },
    "Golden Frog Glyph W": {
        "classification": ItemClassification.useful,
        "address": 0x1b55a3,
        "value": 0x8,
        "id": 172,
    },
    "Golden Frog Glyph Square": {
        "classification": ItemClassification.progression,
        "address": 0x1b55a3,
        "value": 0x10,
        "id": 173,
    },

    # Ships
    "Ship: SS Linebeck": {
        "classification": ItemClassification.filler,
        "id": 174,
    },
    "Ship: Bright Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x1,
        "id": 175,
    },
    "Ship: Iron Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x2,
        "id": 176,
    },
    "Ship: Stone Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x3,
        "id": 177,
    },
    "Ship: Vintage Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x4,
        "id": 178,
    },
    "Ship: Demon Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x5,
        "id": 179,
    },
    "Ship: Tropical Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x6,
        "id": 180,
    },
    "Ship: Dignified Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x7,
        "id": 181,
    },
    "Ship: Golden Ship": {
        "classification": ItemClassification.useful,
        "backup_filler": True,
        "ship": 0x8,
        "id": 182,
    },

    # Fish
    "Fish: Skippyjack": {
        "classification": ItemClassification.filler,
        "address": 0x1ba5b4,
        "value": 0x1,
        "incremental": True,
        "size": 1,
        "id": 183,
    },
    "Fish: Toona": {
        "classification": ItemClassification.filler,
        "address": 0x1ba5b5,
        "value": 0x1,
        "incremental": True,
        "size": 1,
        "id": 184,
    },
    "Fish: Loovar": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba5b6,
        "value": 0x1,
        "incremental": True,
        "size": 1,
        "id": 185,
    },
    "Fish: Rusty Swordfish": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba5b7,
        "value": 0x1,
        "incremental": True,
        "size": 1,
        "id": 186,
    },
    "Fish: Legendary Neptoona": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba5b8,
        "value": 0x1,
        "incremental": True,
        "size": 1,
        "id": 187,
    },
    "Fish: Stowfish": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": 0x1ba5b9,
        "value": 0x1,
        "incremental": True,
        "size": 1,
        "id": 188,
    },
    "_UT_Glitched_Logic": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 189,
    },

}

id_check = []
for data in ITEMS_DATA.values():
    if data["id"] in id_check:
        raise f"Duplicate ID Detected: {data['id']}"
    id_check.append(data["id"])

# IDs are now fixed!!!
"""for i, k in enumerate(ITEMS_DATA):
    ITEMS_DATA[k]["id"] = i+1"""

# bulk data editing / export
if __name__ == "__main__":
    for name, data in ITEMS_DATA.items():
        if name in ITEM_GROUPS["Pedestal Items"]:
            print(f"{name}: {data['id']}")
"""
    keys = set()
    for name, data in ITEMS_DATA.items():
        for key in data:
            keys.add(key)
    for i in keys:
        print(i)
    # print(f"\t\"{name}\": " + "{")
"""
"""
        for key, value in data.items():
            if type(value) is str:
                print(f"\t\t\"{key}\": \"{value}\",")
            elif key == "classification":
                print(f"\t\t\"{key}\": ItemClassification.{CLASSIFICATION[value]},")
            elif type(value) is int:
                if key in ["id", "size"]:
                    print(f"\t\t\"{key}\": {value},")
                else:
                    print(f"\t\t\"{key}\": {hex(value)},")
            elif type(value) is list:
                l_print = "["
                for i in value:
                    if type(i) is tuple or type(i) is list:
                        l_print += "("
                        for j in i:
                            if type(j) is int:
                                l_print += f"{hex(j)}, "
                            elif type(j) is str:
                                l_print += f"\"{j}\", "
                            else:
                                l_print += f"{j}, "
                        l_print = l_print[:-2]
                        l_print += "), "
                    else:
                        if type(i) is int:
                            l_print += f"{hex(i)}, "
                        elif type(i) is str:
                            l_print += f"\"{i}\", "
                        else:
                            l_print += f"{i}, "
                l_print = l_print[:-2]
                l_print += "]"
                print(f"\t\t\"{key}\": {l_print},")
            else:
                print(f"\t\t\"{key}\": {value},")
        print("\t},")
"""
