from BaseClasses import ItemClassification

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
        'progressive': [[0x1BA644, 1], [0x1BA648, 32]]
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
        "give_ammo": [10, 20, 30],
        "ammo_address": 0x1BA6C0
    },
    "Bombchus (Progressive)": {
        'classification': ItemClassification.progression,
        'progressive': [[0x1BA644, 0x80], [0x1BA5D4, 1], [0x1BA5D4, 2]],
        "give_ammo": [10, 20, 30],
        "ammo_address": 0x1BA6C6
    },
    "Bow (Progressive)": {
        'classification': ItemClassification.progression,
        "progressive": [[0x1BA644, 0x20], [0x1BA5D0, 1], [0x1BA5D0, 2]],
        "give_ammo": [20, 30, 50],
        "ammo_address": 0x1BA6C2
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
    "Heart Container": {
        'classification': ItemClassification.useful,
        'address': 0x1BA388,
        'value': 4,
        'incremental': True,
        'size': 2
    },
    "Sand of Hours": {
        'classification': ItemClassification.useful,
        'address': 0x1BA528,
        'value': "Sand",
        'incremental': True,
        'size': 4
    },
    "Swordsman's Scroll": {
        'classification': ItemClassification.progression,
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
        'value': 0x01
    },
    "Big Catch Lure": {
        'classification': ItemClassification.progression,
        'address': 0x1BA649,
        'value': 0x80
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
        'classification': ItemClassification.filler,
        'address': 0x1BA541,
        'value': 1,
        'incremental': True
    },
    "Wisdom Gem": {
        'classification': ItemClassification.filler,
        'address': 0x1BA542,
        'value': 1,
        'incremental': True
    },
    "Courage Gem": {
        'classification': ItemClassification.filler,
        'address': 0x1BA540,
        'value': 1,
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
        'size': 2
    },
    "Big Green Rupee (100)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 100,
        'incremental': True,
        'size': 2
    },
    "Big Red Rupee (200)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 200,
        'incremental': True,
        'size': 2
    },
    "Gold Rupee (300)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 300,
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
        'address': 0x1BA564,  # Not correct, not priority
        'value': 0x01,
        'incremental': True
    },
    "Ship Part": {
        'classification': ItemClassification.filler,
        'address': 0x1BA564,  # Not correct, not priority
        'value': 1,
        'incremental': True
    },
    "Potion": {
        'classification': ItemClassification.filler,
        'dummy': True
    },
    "Nothing!": {
        'classification': ItemClassification.filler,
        'dummy': True
    },

    # =============== Treasure Maps ==============

    "Courage Crest": {
        'classification': ItemClassification.progression,
        'address': 0x1B558C,
        'value': 0x04,
        'set_bit': [(0x1BA650, 1)]
    },
    "Treasure Map #1": {
        'classification': ItemClassification.filler,
        'address': 0x1BA650,
        'value': 0x80
    },
    "Treasure Map #3": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x20
    },
    "Treasure Map #4": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x80
    },
    "Treasure Map #9": {
        'classification': ItemClassification.progression,
        'address': 0x1BA650,
        'value': 0x02
    },
    "Treasure Map #10": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x10
    },
    "Treasure Map #11": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x2,
    },
    "Treasure Map #12": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x20
    },
    "Treasure Map #23": {
        'classification': ItemClassification.filler,
        'address': 0x1BA612,
        'value': 128,
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
    "Boss Key (Temple of Fire)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dummy': True
    },
    "Force Gem (B3)": {
        'classification': ItemClassification.progression,
        'force_vanilla': True,
        'dummy': True
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
}

# Oops apparently not a constant lul (it will be after this)
for i, k in enumerate(ITEMS_DATA.keys()):
    ITEMS_DATA[k]["id"] = i+1
