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
        'id': 9
    },
    "Boomerang": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x04,
        'id' : 3
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
        'id': 5
    },
    "Bombchus": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x80,
        'id': 8
    },
    "Bow": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x20,
        'id': 6
    },
    "Grappling Hook": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x40,
        'id': 7
    },
    "Shovel": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,
        'value': 0x08,
        'id': 4
    },
    "SW Sea Chart": {
        'classification': ItemClassification.progression,
        'address': 0x021BA644,  # Not correct, not priority
        'value': 0x08,
        'id': 10
    },
    "Big Green Rupee": {
        'classification': ItemClassification.filler,
        'address': 0x021BA644,  # Not correct, not priority
        'value': 0x08,
        'id': 10
    },
    "Ship Part": {
        'classification': ItemClassification.filler,
        'address': 0x021BA644,  # Not correct, not priority
        'value': 0x08,
        'id': 10
    },
    "Red Rupee": {
        'classification': ItemClassification.filler,
        'address': 0x021BA644,  # Not correct, not priority
        'value': 0x08,
        'id': 10
    },
    "Power Gem": {
        'classification': ItemClassification.filler,
        'address': 0x021BA644,  # Not correct, not priority
        'value': 0x08,
        'id': 10
    }
}