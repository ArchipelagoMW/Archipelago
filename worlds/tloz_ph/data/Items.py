from BaseClasses import ItemClassification

ITEMS_DATA = {
    #   "No Item": {
    #   'classification': ItemClassification.filler,
    #   "",
    #    'id': 0x00,
    #    'subid': 0x00
    #    },
    "Hammer": {
        'classification': ItemClassification.progression,
        'address': 0x1BA645,
        'value': 0x01,
        'set_bit': 0x021BA6C8
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
    "Bombs": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x10,
        "progressive": 0x1BA5D2,
        "give_ammo": 10,
        "ammo_address": 0x1BA6C0
    },
    "Bombchus": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x80,
        'progressive': 0x1BA5D4,
        "give_ammo": 10,
        "ammo_address": 0x1BA6C6
    },
    "Bow": {
        'classification': ItemClassification.progression,
        'address': 0x1BA644,
        'value': 0x20,
        "progressive": 0x1BA5D0,
        "give_ammo": 20,
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
    "Big Green Rupee": {
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
    "Red Rupee": {
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
    "Green Rupee": {
        'classification': ItemClassification.filler,
        'address': 0x1BA53E,
        'value': 0,
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
    }
}

# Oops apparently not a constant lul
for i, k in enumerate(ITEMS_DATA.keys()):
    ITEMS_DATA[k]["id"] = i+1
