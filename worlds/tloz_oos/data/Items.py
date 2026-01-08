from BaseClasses import ItemClassification

ITEMS_DATA = {
    #   "No Item": {
    #   'classification': ItemClassification.filler,
    #   "",
    #    'id': 0x00,
    #    'subid': 0x00
    #    },
    "Progressive Shield": {
        "classification": ItemClassification.progression,
        "id": 0x01
    },
    "Bombs (10)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x03
    },
    "Bombs (20)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x03,
        "subid": 0x03  # Just to make sure we're not erasing anything important, this goes over a 30 bombs drop
    },
    "Cane of Somaria": {
        'classification': ItemClassification.progression,
        'id': 0x04
    },
    "Progressive Sword": {
        "classification": ItemClassification.progression,
        "id": 0x05
    },
    "Progressive Boomerang": {
        "classification": ItemClassification.progression,
        "id": 0x06
    },
    "Rod of Seasons (Spring)": {
        "classification": ItemClassification.progression,
        "id": 0x07,
        "subid": 0x02
    },
    "Rod of Seasons (Summer)": {
        "classification": ItemClassification.progression,
        "id": 0x07,
        "subid": 0x03
    },
    "Rod of Seasons (Autumn)": {
        "classification": ItemClassification.progression,
        "id": 0x07,
        "subid": 0x04
    },
    "Rod of Seasons (Winter)": {
        "classification": ItemClassification.progression,
        "id": 0x07,
        "subid": 0x05
    },
    "Magnetic Gloves": {
        "classification": ItemClassification.progression,
        "id": 0x08
    },
    "Switch Hook": {
        'classification': ItemClassification.progression,
        'id': 0x0a
    },
    "Biggoron's Sword": {
        "classification": ItemClassification.progression,
        "id": 0x0c
    },
    "Bombchus (10)": {
        'classification': ItemClassification.progression,
        'id': 0x0d
    },
    "Bombchus (20)": {
        'classification': ItemClassification.progression,
        'id': 0x0d,
        "subid": 0x01
    },
    "Ricky's Flute": {
        "classification": ItemClassification.progression,
        "id": 0x0e,
        "subid": 0x00
    },
    "Dimitri's Flute": {
        "classification": ItemClassification.progression,
        "id": 0x0e,
        "subid": 0x01
    },
    "Moosh's Flute": {
        "classification": ItemClassification.progression,
        "id": 0x0e,
        "subid": 0x02
    },
    "Seed Shooter": {
        'classification': ItemClassification.progression,
        'id': 0x0f
    },
    # "Progressive Harp": {
    #     'classification': ItemClassification.progression,
    #     'id': 0x11
    # },
    "Progressive Slingshot": {
        "classification": ItemClassification.progression,
        "id": 0x13
    },
    "Shovel": {
        "classification": ItemClassification.progression,
        "id": 0x15
    },
    "Power Bracelet": {
        "classification": ItemClassification.progression,
        "id": 0x16
    },
    "Progressive Feather": {
        "classification": ItemClassification.progression,
        "id": 0x17
    },
    "Seed Satchel": {
        "classification": ItemClassification.progression,
        "id": 0x19
    },
    "Fool's Ore": {
        "classification": ItemClassification.progression,
        "id": 0x1e
    },
    "Ember Seeds": {
        "classification": ItemClassification.progression,
        "id": 0x20
    },
    "Scent Seeds": {
        "classification": ItemClassification.progression,
        "id": 0x21
    },
    "Pegasus Seeds": {
        "classification": ItemClassification.progression,
        "id": 0x22
    },
    "Gale Seeds": {
        "classification": ItemClassification.progression,
        "id": 0x23
    },
    "Mystery Seeds": {
        "classification": ItemClassification.progression,
        "id": 0x24
    },
    "Rupees (1)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x00
    },
    "Rupees (5)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x01
    },
    "Rupees (10)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x02
    },
    "Rupees (20)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x03
    },
    "Rupees (30)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x04
    },
    "Rupees (50)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x05
    },
    "Rupees (100)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x06
    },
    "Rupees (200)": {
        "classification": ItemClassification.filler,
        "id": 0x28,
        "subid": 0x08
    },
    "Ore Chunks (10)": {
        "classification": ItemClassification.filler,
        "id": 0x37,
        "subid": 0x02
    },
    "Ore Chunks (25)": {
        "classification": ItemClassification.filler,
        "id": 0x37,
        "subid": 0x01
    },
    "Ore Chunks (50)": {
        "classification": ItemClassification.filler,
        "id": 0x37,
        "subid": 0x00
    },
    "Heart Container": {
        "classification": ItemClassification.useful,
        "id": 0x2a
    },
    "Piece of Heart": {
        "classification": ItemClassification.filler,
        "id": 0x2b,
        "subid": 0x01
    },
    "Rare Peach Stone": {
        "classification": ItemClassification.filler,
        "id": 0x2b,
        "subid": 0x02
    },
    "Flippers": {
        "classification": ItemClassification.progression,
        "id": 0x2e
    },
    "Potion": {
        "classification": ItemClassification.filler,
        "id": 0x2f
    },

    "Small Key (Hero's Cave)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x00
    },
    "Small Key (Gnarled Root Dungeon)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x01
    },
    "Small Key (Snake's Remains)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x02
    },
    "Small Key (Poison Moth's Lair)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x03
    },
    "Small Key (Dancing Dragon Dungeon)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x04
    },
    "Small Key (Unicorn's Cave)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x05
    },
    "Small Key (Ancient Ruins)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x06
    },
    "Small Key (Explorer's Crypt)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x07
    },
    "Small Key (Sword & Shield Dungeon)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x08
    },
    "Master Key (Hero's Cave)": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x80
    },
    "Master Key (Gnarled Root Dungeon)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x81
    },
    "Master Key (Snake's Remains)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x82
    },
    "Master Key (Poison Moth's Lair)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x83
    },
    "Master Key (Dancing Dragon Dungeon)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x84
    },
    "Master Key (Unicorn's Cave)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x85
    },
    "Master Key (Ancient Ruins)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x86
    },
    "Master Key (Explorer's Crypt)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x87
    },
    "Master Key (Sword & Shield Dungeon)": {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x88
    },
    "Boss Key (Gnarled Root Dungeon)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x00
    },
    "Boss Key (Snake's Remains)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x01
    },
    "Boss Key (Poison Moth's Lair)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x02
    },
    "Boss Key (Dancing Dragon Dungeon)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x03
    },
    "Boss Key (Unicorn's Cave)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x04
    },
    "Boss Key (Ancient Ruins)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x05
    },
    "Boss Key (Explorer's Crypt)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x06
    },
    "Boss Key (Sword & Shield Dungeon)": {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x07
    },
    "Compass (Hero's Cave)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x00
    },
    "Compass (Gnarled Root Dungeon)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x01
    },
    "Compass (Snake's Remains)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x02
    },
    "Compass (Poison Moth's Lair)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x03
    },
    "Compass (Dancing Dragon Dungeon)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x04
    },
    "Compass (Unicorn's Cave)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x05
    },
    "Compass (Ancient Ruins)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x06
    },
    "Compass (Explorer's Crypt)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x07
    },
    "Compass (Sword & Shield Dungeon)": {
        "classification": ItemClassification.useful,
        "id": 0x32,
        "subid": 0x08
    },
    "Dungeon Map (Hero's Cave)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x00
    },
    "Dungeon Map (Gnarled Root Dungeon)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x01
    },
    "Dungeon Map (Snake's Remains)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x02
    },
    "Dungeon Map (Poison Moth's Lair)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x03
    },
    "Dungeon Map (Dancing Dragon Dungeon)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x04
    },
    "Dungeon Map (Unicorn's Cave)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x05
    },
    "Dungeon Map (Ancient Ruins)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x06
    },
    "Dungeon Map (Explorer's Crypt)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x07
    },
    "Dungeon Map (Sword & Shield Dungeon)": {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x08
    },

    "Gasha Seed": {
        "classification": ItemClassification.filler,
        "id": 0x34,
        "subid": 0x01
    },

    "Cuccodex": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x55
    },
    "Lon Lon Egg": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x56
    },
    "Ghastly Doll": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x57
    },
    "Iron Pot": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x35
    },
    "Lava Soup": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x38
    },
    "Goron Vase": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x39
    },
    "Fish": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x3a
    },
    "Megaphone": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x3b
    },
    "Mushroom": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x3c
    },
    "Wooden Bird": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x3d
    },
    "Engine Grease": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x3e
    },
    "Phonograph": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x3f
    },

    "Gnarled Key": {
        "classification": ItemClassification.progression,
        "id": 0x42
    },
    "Floodgate Key": {
        "classification": ItemClassification.progression,
        "id": 0x43
    },
    "Dragon Key": {
        "classification": ItemClassification.progression,
        "id": 0x44
    },
    "Star Ore": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x45
    },
    "Ribbon": {
        "classification": ItemClassification.progression,
        "id": 0x46
    },
    "Spring Banana": {
        "classification": ItemClassification.progression,
        "id": 0x47
    },
    #   "ricky's gloves": {
    #       'classification': ItemClassification.progression,
    #       'pretty_name': "Ricky's Gloves",
    #       'id': 0x48
    #   },
    "Rusty Bell": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x4a
    },
    "Pirate's Bell": {
        "classification": ItemClassification.progression,
        "id": 0x25
    },
    "Treasure Map": {
        "classification": ItemClassification.useful,
        "id": 0x4b
    },
    "Round Jewel": {
        "classification": ItemClassification.progression,
        "id": 0x4c
    },
    "Pyramid Jewel": {
        "classification": ItemClassification.progression,
        "id": 0x4d
    },
    "Square Jewel": {
        "classification": ItemClassification.progression,
        "id": 0x4e
    },
    "X-Shaped Jewel": {
        "classification": ItemClassification.progression,
        "id": 0x4f
    },
    "Red Ore": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x50
    },
    "Blue Ore": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x51
    },
    "Hard Ore": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x52
    },
    "Member's Card": {
        "classification": ItemClassification.progression,
        "id": 0x53
    },
    "Master's Plaque": {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x54
    },
    #   "Bomb Upgrade": {
    #   'classification': ItemClassification.progression,
    #   "",
    #        'id': 0x61
    #    },
    #   "Satchel Upgrade": {
    #   'classification': ItemClassification.progression,
    #   "",
    #        'id': 0x62)

    "Friendship Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x04,
        "ring": "useless"
    },
    "Power Ring L-1": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x05,
        "ring": "good"
    },
    "Power Ring L-2": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x06,
        "ring": "good"
    },
    "Power Ring L-3": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x07,
        "ring": "good"
    },
    "Armor Ring L-1": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x08,
        "ring": "good"
    },
    "Armor Ring L-2": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x09,
        "ring": "good"
    },
    "Armor Ring L-3": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x0a,
        "ring": "good"
    },
    "Red Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x0b,
        "ring": "good"
    },
    "Blue Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x0c,
        "ring": "good"
    },
    "Green Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x0d,
        "ring": "good"
    },
    "Cursed Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x0e,
        "ring": "useless"
    },
    "Expert's Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x0f,
        "ring": "good"
    },
    "Blast Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x10,
        "ring": "good"
    },
    "Rang Ring L-1": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x11,
        "ring": "good"
    },
    "GBA Time Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x12,
        "ring": "useless"
    },
    "Maple's Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x13,
        "ring": "good"
    },
    "Steadfast Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x14,
        "ring": "good"
    },
    "Pegasus Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x15,
        "ring": "good"
    },
    "Toss Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x16,
        "ring": "good"
    },
    "Heart Ring L-1": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x17,
        "ring": "good"
    },
    "Heart Ring L-2": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x18,
        "ring": "good"
    },
    "Swimmer's Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x19,
        "ring": "good"
    },
    "Charge Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x1a,
        "ring": "good"
    },
    "Light Ring L-1": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x1b,
        "ring": "good"
    },
    "Light Ring L-2": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x1c,
        "ring": "good"
    },
    "Bomber's Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x1d,
        "ring": "good"
    },
    "Green Luck Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x1e,
        "ring": "good"
    },
    "Blue Luck Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x1f,
        "ring": "good"
    },
    "Gold Luck Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x20,
        "ring": "good"
    },
    "Red Luck Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x21,
        "ring": "good"
    },
    "Green Holy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x22,
        "ring": "good"
    },
    "Blue Holy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x23,
        "ring": "good"
    },
    "Red Holy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x24,
        "ring": "good"
    },
    "Snowshoe Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x25,
        "ring": "good"
    },
    "Roc's Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x26,
        "ring": "good"
    },
    "Quicksand Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x27,
        "ring": "good"
    },
    "Red Joy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x28,
        "ring": "good"
    },
    "Blue Joy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x29,
        "ring": "good"
    },
    "Gold Joy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x2a,
        "ring": "good"
    },
    "Green Joy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x2b,
        "ring": "good"
    },
    "Discovery Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x2c,
        "ring": "good"
    },
    "Rang Ring L-2": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x2d,
        "ring": "good"
    },
    "Octo Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x2e,
        "ring": "useless"
    },
    "Moblin Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x2f,
        "ring": "useless"
    },
    "Like Like Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x30,
        "ring": "useless"
    },
    "Subrosian Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x31,
        "ring": "useless"
    },
    "First Gen Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x32,
        "ring": "useless"
    },
    "Spin Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x33,
        "ring": "good"
    },
    "Bombproof Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x34,
        "ring": "good"
    },
    "Energy Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x35,
        "ring": "good"
    },
    "Dbl. Edge Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x36,
        "ring": "good"
    },
    "GBA Nature Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x37,
        "ring": "useless"
    },
    "Slayer's Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x38,
        "ring": "useless"
    },
    "Rupee Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x39,
        "ring": "useless"
    },
    "Victory Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x3a,
        "ring": "useless"
    },
    "Sign Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x3b,
        "ring": "useless"
    },
    "100th Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x3c,
        "ring": "useless"
    },
    "Whisp Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x3d,
        "ring": "good"
    },
    "Gasha Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x3e,
        "ring": "good"
    },
    "Peace Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x3f,
        "ring": "good"
    },
    "Zora Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x40,
        "ring": "good"
    },
    "Fist Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x41,
        "ring": "good"
    },
    "Whimsical Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x42,
        "ring": "good"
    },
    "Protection Ring": {
        "classification": ItemClassification.filler,
        "id": 0x2d,
        "subid": 0x43,
        "ring": "good"
    },

    "Bomb Flower": {
        "classification": ItemClassification.progression,
        "id": 0x49
    },
    "Fertile Soil": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x00
    },
    "Gift of Time": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x01
    },
    "Bright Sun": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x02
    },
    "Soothing Rain": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x03
    },
    "Nurturing Warmth": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x04
    },
    "Blowing Wind": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x05
    },
    "Seed of Life": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x06
    },
    "Changing Seasons": {
        "classification": ItemClassification.progression,
        "id": 0x40,
        "subid": 0x07
    },
    "Maku Seed": {  # Mostly for debug
        "classification": ItemClassification.progression_skip_balancing,
        "id": 0x36
    },
}
