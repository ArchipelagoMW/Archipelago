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
        'address': 0x021BA645,
        'value': 0x01,
        'id': 9,
        'set_bit': 0x021BA6C8
    },
    "Boomerang": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x04,
        'id': 3,
        'set_bit': 0x021BA6BC
    },
    "Sword": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x01,
        'id': 1
    },
    "Shield": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x02,
        'id': 2
    },
    "Bombs": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x10,
        'id': 5,
        "progressive": 0x021BA5D2,
        "give_ammo": 10,
        "ammo_address": 0x1BA6C0
    },
    "Bombchus": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x80,
        'id': 8,
        'progressive': 0x021BA5D4,
        "give_ammo": 10,
        "ammo_address": 0x1BA6C6
    },
    "Bow": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x20,
        'id': 6,
        "progressive": 0x021BA5D0,
        "give_ammo": 20,
        "ammo_address": 0x1BA6C2
    },
    "Grappling Hook": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x40,
        'id': 7,
        "set_bit": 0x021BA6C4
    },
    "Shovel": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x08,
        'id': 4,
        "set_bit": 0x021BA6BE
    },
    "SW Sea Chart": {
        'classification': ItemClassification.progression,
        'address': 0x021BA648,
        'value': 0x02,
        'id': 10
    },
    "Big Green Rupee": {
        'classification': ItemClassification.filler,
        'address': 0x021BA53E,
        'value': 100,
        'id': 11,
        'incremental': True
    },
    "Ship Part": {
        'classification': ItemClassification.filler,
        'address': 0x021BA564,  # Not correct, not priority
        'value': 1,
        'id': 12,
        'incremental': True
    },
    "Red Rupee": {
        'classification': ItemClassification.filler,
        'address': 0x021BA53E,
        'value': 20,
        'id': 13,
        'incremental': True
    },
    "Power Gem": {
        'classification': ItemClassification.filler,
        'address': 0x021BA541,
        'value': 1,
        'id': 14,
        'incremental': True
    },
    "Wisdom Gem": {
        'classification': ItemClassification.filler,
        'address': 0x021BA542,
        'value': 1,
        'id': 19,
        'incremental': True
    },
    "Courage Gem": {
        'classification': ItemClassification.filler,
        'address': 0x021BA540,
        'value': 1,
        'id': 20,
        'incremental': True
    },
    "Green Rupee": {
        'classification': ItemClassification.filler,
        'address': 0x021BA53E,
        'value': 0,
        'id': 15,
        'incremental': True
    },
    "Treasure": {
        'classification': ItemClassification.filler,
        'address': 0x021BA564,  # Not correct, not priority
        'value': 0x01,
        'id': 16,
        'incremental': True
    },
    "Treasure Map #10": {
        'classification': ItemClassification.filler,
        'address': 0x021BA651,
        'value': 0x10,
        'id': 17
    },
    "Treasure Map #12": {
        'classification': ItemClassification.filler,
        'address': 0x021BA652,  # Not correct, not priority
        'value': 0x20,
        'id': 18
    }
}