from BaseClasses import ItemClassification
from ..patching.Constants import DEFINES

BASE_ITEM_ID = 27022002000

ITEMS_DATA = {
    #   "No Item": {
    #   'classification': ItemClassification.filler,
    #   "",
    #    'id': 0x00,
    #    'subid': 0x00
    #    },
    "Progressive Shield": {
        'classification': ItemClassification.progression,
        'id': 0x01
    },
    "Bombs (10)": {
        'classification': ItemClassification.progression,
        'id': 0x03
    },
    "Progressive Sword": {
        'classification': ItemClassification.progression,
        'id': 0x05
    },
    "Boomerang": {
        'classification': ItemClassification.progression,
        'id': 0x06
    },
    "Progressive Harp": {
        'classification': ItemClassification.progression,
        'id': 0x25,
        'subid': 0x00                                                                                                           
    },
    "Progressive Hook": {
        'classification': ItemClassification.progression,
        'id': 0x0a
    },
    "Cane of Somaria": {
        'classification': ItemClassification.progression,
        'id': 0x04
    },
    "Biggoron's Sword": {
        'classification': ItemClassification.progression,
        'id': 0x0c
    },
    #   "Bombchus (10)": {
    #       'classification': ItemClassification.progression,
    #       'id': 0x0d
    #   },
    "Ricky's Flute": {
        'classification': ItemClassification.progression,
        'id': 0x0e,
        'subid': 0x00
    },
    "Dimitri's Flute": {
        'classification': ItemClassification.progression,
        'id': 0x0e,
        'subid': 0x01
    },
    "Moosh's Flute": {
        'classification': ItemClassification.progression,
        'id': 0x0e,
        'subid': 0x02
    },
    "Seed Shooter": {
        'classification': ItemClassification.progression,
        'id': 0x0f
    },
    "Shovel": {
        'classification': ItemClassification.progression,
        'id': 0x15
    },
    "Progressive Bracelet": {
        'classification': ItemClassification.progression,
        'id': 0x16
    },
    "Feather": {
        'classification': ItemClassification.progression,
        'id': 0x17
    },
    "Seed Satchel": {
        'classification': ItemClassification.progression,
        'id': 0x19
    },
    "Ember Seeds": {
        'classification': ItemClassification.progression,
        'id': 0x20
    },
    "Scent Seeds": {
        'classification': ItemClassification.progression,
        'id': 0x21
    },
    "Pegasus Seeds": {
        'classification': ItemClassification.progression,
        'id': 0x22
    },
    "Gale Seeds": {
        'classification': ItemClassification.useful,
        'id': 0x23
    },
    "Mystery Seeds": {
        'classification': ItemClassification.progression,
        'id': 0x24
    },
    "Rupees (1)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x00
    },
    "Rupees (5)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x01
    },
    "Rupees (10)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x02
    },
    "Rupees (20)": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x28,
        'subid': 0x03
    },
    "Rupees (30)": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x28,
        'subid': 0x04
    },
    "Rupees (50)": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x28,
        'subid': 0x05
    },
    "Rupees (100)": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x28,
        'subid': 0x06
    },
    "Rupees (200)": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x28,
        'subid': 0x08
    },
    "Heart Container": {
        'classification': ItemClassification.useful,
        'id': 0x2a
    },
    "Piece of Heart": {
        'classification': ItemClassification.useful,
        'id': 0x2b,
        'subid': 0x01
    },
    "Progressive Flippers": {
        'classification': ItemClassification.progression,
        'id': 0x2e
    },
    "Potion": {
        'classification': ItemClassification.useful,
        'id': 0x2f
    },
    "King Zora's Potion": {
        'classification': ItemClassification.progression,
        'id': 0x37
    },

    "Small Key (Maku Path)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x00
    },
    "Small Key (Spirit's Grave)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x01
    },
    "Small Key (Wing Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x02
    },
    "Small Key (Moonlit Grotto)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x03
    },
    "Small Key (Skull Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x04
    },
    "Small Key (Crown Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x05
    },
    "Small Key (Mermaid's Cave Past)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x0C
    },
    "Small Key (Mermaid's Cave Present)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x06
    },
    "Small Key (Jabu-Jabu's Belly)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x07
    },
    "Small Key (Ancient Tomb)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x08
    },
    "Master Key (Maku Path)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x00
    },
    "Master Key (Spirit's Grave)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x01
    },
    "Master Key (Wing Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x02
    },
    "Master Key (Moonlit Grotto)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x03
    },
    "Master Key (Skull Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x04
    },
    "Master Key (Crown Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x05
    },
    "Master Key (Mermaid's Cave Past)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x0C
    },
    "Master Key (Mermaid's Cave Present)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x06
    },
    "Master Key (Jabu-Jabu's Belly)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x07
    },
    "Master Key (Ancient Tomb)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x08
    },
    "Boss Key (Spirit's Grave)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x01
    },
    "Boss Key (Wing Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x02
    },
    "Boss Key (Moonlit Grotto)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x03
    },
    "Boss Key (Skull Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x04
    },
    "Boss Key (Crown Dungeon)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x05
    },
    "Boss Key (Mermaid's Cave)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x06
    },
    "Boss Key (Jabu-Jabu's Belly)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x07
    },
    "Boss Key (Ancient Tomb)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x08
    },
    "Compass (Spirit's Grave)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x01
    },
    "Compass (Wing Dungeon)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x02
    },
    "Compass (Moonlit Grotto)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x03
    },
    "Compass (Skull Dungeon)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x04
    },
    "Compass (Crown Dungeon)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x05
    },
    "Compass (Mermaid's Cave Past)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x0C
    },
    "Compass (Mermaid's Cave Present)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x06
    },
    "Compass (Jabu-Jabu's Belly)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x07
    },
    "Compass (Ancient Tomb)": {
        'classification': ItemClassification.useful,
        'id': 0x32,
        'subid': 0x08
    },
    "Dungeon Map (Spirit's Grave)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x01
    },
    "Dungeon Map (Wing Dungeon)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x02
    },
    "Dungeon Map (Moonlit Grotto)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x03
    },
    "Dungeon Map (Skull Dungeon)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x04
    },
    "Dungeon Map (Crown Dungeon)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x05
    },
    "Dungeon Map (Mermaid's Cave Past)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x0C
    },
    "Dungeon Map (Mermaid's Cave Present)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x06
    },
    "Dungeon Map (Jabu-Jabu's Belly)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x07
    },
    "Dungeon Map (Ancient Tomb)": {
        'classification': ItemClassification.useful,
        'id': 0x33,
        'subid': 0x08
    },

    "Gasha Seed": {
        'classification': ItemClassification.filler,
        'id': 0x34,
        'subid': 0x01
    },
    
    #     "Maku Seed": {
    #           'classification': ItemClassification.progression,
    #         'id': 0x36
    #     },

    "Poe Clock": {
        'classification': ItemClassification.progression,
        'id': 0x3d
    },
    "Stationary": {
        'classification': ItemClassification.progression,
        'id': 0x3e
    },
    "Stink Bag": {
        'classification': ItemClassification.progression,
        'id': 0x3f
    },
    "Tasty Meat": {
        'classification': ItemClassification.progression,
        'id': 0x47
    },
    "Doggie Mask": {
        'classification': ItemClassification.progression,
        'id': 0x56
    },
    "Dumbbell": {
        'classification': ItemClassification.progression,
        'id': 0x57
    },
    "Cheesy Mustache": {
        'classification': ItemClassification.progression,
        'id': 0x5f
    },
    "Funny Joke": {
        'classification': ItemClassification.progression,
        'id': 0x3c
    },
    "Touching Book": {
        'classification': ItemClassification.progression,
        'id': 0x35
    },
    "Magic Oar": {
        'classification': ItemClassification.progression,
        'id': 0x38
    },
    "Sea Ukulele": {
        'classification': ItemClassification.progression,
        'id': 0x39
    },
    "Broken Sword": {
         'classification': ItemClassification.progression,
         'id': 0x3a
    },

    "Bomb Flower": {
        'classification': ItemClassification.progression,
        'id': 0x49
    },
    "Book of Seals": {
        'classification': ItemClassification.progression,
        'id': 0x55
    },
    "Brother Emblem": {
        'classification': ItemClassification.progression,
        'id': 0x5b
    },
    "Cheval Rope": {
        'classification': ItemClassification.progression,
        'id': 0x52
    },
    "Crown Key": {
        'classification': ItemClassification.progression,
        'id': 0x43
    },
    "Fairy Powder": {
        'classification': ItemClassification.progression,
        'id': 0x51
    },
    "Goron Vase": {
        'classification': ItemClassification.progression,
        'id': 0x5c
    },
    "Goronade": {
        'classification': ItemClassification.progression,
        'id': 0x5d
    },
    "Graveyard Key": {
        'classification': ItemClassification.progression,
        'id': 0x42,
    },
    "Island Chart": {
        'classification': ItemClassification.progression,
        'id': 0x54
    },
    "Lava Juice": {
        'classification': ItemClassification.progression,
        'id': 0x5a
    },
    "Letter of Introduction": {
        'classification': ItemClassification.progression,
        'id': 0x59
    },
    "Library Key": {
        'classification': ItemClassification.progression,
        'id': 0x46
    },
    "Mermaid Key": {
        'classification': ItemClassification.progression,
        'id': 0x44
    },
    "Old Mermaid Key": {
        'classification': ItemClassification.progression,
        'id': 0x45
    },
    "Ricky's Gloves": {
        'classification': ItemClassification.progression,
        'id': 0x48
    },
    "Rock Brisket": {
        'classification': ItemClassification.progression,
        'id': 0x5e
    },
    "Scent Seedling": {
        'classification': ItemClassification.progression,
        'id': 0x4d
    },
    "Slate": {
        'classification': ItemClassification.progression,
        'id': 0x4b
    },
    "Tokay Eyeball": {
        'classification': ItemClassification.progression,
        'id': 0x4f
    },
    "Cracked Tuni Nut": {
        'classification': ItemClassification.progression,
        'id': 0x4c,
        'subid': 0x00
    },
    "Tuni Nut": {
        'classification': ItemClassification.progression,
        'id': 0x3b,
        'subid': 0x00
    },
    "Zora Scale": {
        'classification': ItemClassification.progression,
        'id': 0x4e
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
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x04,
        'ring': 'useless'
    },
    "Power Ring L-1": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x05,
        'ring': 'good'
    },
    "Power Ring L-2": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x06,
        'ring': 'good'
    },
    "Power Ring L-3": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x07,
        'ring': 'good'
    },
    "Armor Ring L-1": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x08,
        'ring': 'good'
    },
    "Armor Ring L-2": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x09,
        'ring': 'good'
    },
    "Armor Ring L-3": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x0a,
        'ring': 'good'
    },
    "Red Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x0b,
        'ring': 'good'
    },
    "Blue Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x0c,
        'ring': 'good'
    },
    "Green Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x0d,
        'ring': 'good'
    },
    "Cursed Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x0e,
        'ring': 'useless'
    },
    "Expert's Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x0f,
        'ring': 'good'
    },
    "Blast Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x10,
        'ring': 'good'
    },
    "Rang Ring L-1": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x11,
        'ring': 'good'
    },
    "GBA Time Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x12,
        'ring': 'useless'
    },
    "Maple's Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x13,
        'ring': 'good'
    },
    "Steadfast Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x14,
        'ring': 'good'
    },
    "Pegasus Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x15,
        'ring': 'good'
    },
    "Toss Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x16,
        'ring': 'good'
    },
    "Heart Ring L-1": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x17,
        'ring': 'good'
    },
    "Heart Ring L-2": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x18,
        'ring': 'good'
    },
    "Swimmer's Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x19,
        'ring': 'good'
    },
    "Charge Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x1a,
        'ring': 'good'
    },
    "Light Ring L-1": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x1b,
        'ring': 'good'
    },
    "Light Ring L-2": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x1c,
        'ring': 'good'
    },
    "Bomber's Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x1d,
        'ring': 'good'
    },
    "Green Luck Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x1e,
        'ring': 'good'
    },
    "Blue Luck Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x1f,
        'ring': 'good'
    },
    "Gold Luck Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x20,
        'ring': 'good'
    },
    "Red Luck Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x21,
        'ring': 'good'
    },
    "Green Holy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x22,
        'ring': 'good'
    },
    "Blue Holy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x23,
        'ring': 'good'
    },
    "Red Holy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x24,
        'ring': 'good'
    },
    "Snowshoe Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x25,
        'ring': 'good'
    },
    "Roc's Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x26,
        'ring': 'good'
    },
    "Quicksand Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x27,
        'ring': 'good'
    },
    "Red Joy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x28,
        'ring': 'good'
    },
    "Blue Joy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x29,
        'ring': 'good'
    },
    "Gold Joy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x2a,
        'ring': 'good'
    },
    "Green Joy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x2b,
        'ring': 'good'
    },
    "Discovery Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x2c,
        'ring': 'good'
    },
    "Rang Ring L-2": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x2d,
        'ring': 'good'
    },
    "Octo Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x2e,
        'ring': 'useless'
    },
    "Moblin Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x2f,
        'ring': 'useless'
    },
    "Like Like Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x30,
        'ring': 'useless'
    },
    "Subrosian Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x31,
        'ring': 'useless'
    },
    "First Gen Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x32,
        'ring': 'useless'
    },
    "Spin Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x33,
        'ring': 'good'
    },
    "Bombproof Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x34,
        'ring': 'good'
    },
    "Energy Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x35,
        'ring': 'good'
    },
    "Dbl. Edge Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x36,
        'ring': 'good'
    },
    "GBA Nature Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x37,
        'ring': 'useless'
    },
    "Slayer's Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x38,
        'ring': 'useless'
    },
    "Rupee Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x39,
        'ring': 'useless'
    },
    "Victory Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x3a,
        'ring': 'useless'
    },
    "Sign Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x3b,
        'ring': 'useless'
    },
    "100th Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x3c,
        'ring': 'useless'
    },
    "Whisp Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x3d,
        'ring': 'good'
    },
    "Gasha Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x3e,
        'ring': 'good'
    },
    "Peace Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x3f,
        'ring': 'good'
    },
    "Zora Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x40,
        'ring': 'good'
    },
    "Fist Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x41,
        'ring': 'good'
    },
    "Whimsical Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x42,
        'ring': 'good'
    },
    "Protection Ring": {
        'classification': ItemClassification.filler,
        'id': 0x2d,
        'subid': 0x43,
        'ring': 'good'
    },

    "Eternal Spirit": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x00
    },
    "Ancient Wood": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x01
    },
    "Echoing Howl": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x02
    },
    "Burning Flame": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x03
    },
    "Sacred Soil": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x04
    },
    "Lonely Peak": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x05
    },
    "Rolling Sea": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x06
    },
    "Falling Star": {
        'classification': ItemClassification.progression,
        'id': 0x40,
        'subid': 0x07
    },
}
