from BaseClasses import ItemClassification

ITEMS_DATA = {
    #   "No Item": {
    #   'classification': ItemClassification,   # classification category
    #   'address': int,                         # address in memory
    #   'value': int,                           # value to set in memory, if incremental added else bitwise or
    #   'size': int,                            # size in bytes
    #   'set_bit': int,                         # for setting additional bits on acquisition
    #   'incremental': bool                     # true for positive, False for negative
    #   'progressive': list[list[int, int]]     # address, value for each progressive stage
    #   'give_ammo': list[int]                  # how much ammo to give for each progressive stage
    #   'ammo_address: int                      # address for ammo
    #    },
    "Hammer": {
        'classification': ItemClassification.progression,
        'address': 0x1BA645,
        'value': 0x01,
        'set_bit': 0x1BA6C8
    },
    "Boomerang": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x04,
        'set_bit': 0x1BA6BC
    },
    "Sword": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x01
    },
    "Shield": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x02
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
        "set_bit": 0x1BA6C4
    },
    "Shovel": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x08,
        "set_bit": 0x1BA6BE
    },
    "SW Sea Chart": {
        'classification': ItemClassification.progression,
        'address': 0x1BA648,
        'value': 0x02
    },
    "Big Green Rupee (100)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 100,
        'incremental': True,
        'size': 2
    },
    "Ship Part": {
        'classification': ItemClassification.filler,
        'address': 0x1BA564,  # Not correct, not priority
        'value': 1,
        'incremental': True
    },
    "Red Rupee (20)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 20,
        'incremental': True,
        'size': 2
    },
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
    "Green Rupee (1)": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 1,
        'incremental': True,
        'size': 2
    },
    "Treasure": {
        'classification': ItemClassification.filler,
        'address': 0x1BA564,  # Not correct, not priority
        'value': 0x01,
        'incremental': True
    },
    "Treasure Map #10": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x10
    },
    "Treasure Map #12": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x20
    },
    "Small Key (Mountain Passage)": {
        'classification': ItemClassification.progression,
        'dungeon': 39,
        'incremental': True
    },
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
        'classification': ItemClassification.filler,
        'address': 0x1BA388,
        'value': 4,
        'incremental': True
    }

}

# Oops apparently not a constant lul (it will be after this)
for i, k in enumerate(ITEMS_DATA.keys()):
    ITEMS_DATA[k]["id"] = i+1
