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
        'classification': ItemClassification.filler,
        'address': 0x1BA650,
        'value': 0x80
    },
    "Treasure Map #2": {
        'classification': ItemClassification.filler,
        'address': 0x1BA650,
        'value': 0x10
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
    "Treasure Map #5": {
        'classification': ItemClassification.filler,
        'address': 0x1BA650,
        'value': 0x40
    },
    "Treasure Map #6": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x1
    },
    "Treasure Map #7": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x8
    },
    "Treasure Map #8": {
        'classification': ItemClassification.filler,
        'address': 0x1BA650,
        'value': 0x8
    },
    "Treasure Map #9": {
        'classification': ItemClassification.filler,
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
    "Treasure Map #13": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x04
    },
    "Treasure Map #14": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x1
    },
    "Treasure Map #15": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x2
    },
    "Treasure Map #16": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x10
    },
    "Treasure Map #17": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x40
    },
    "Treasure Map #18": {
        'classification': ItemClassification.filler,
        'address': 0x1BA650,
        'value': 0x4
    },
    "Treasure Map #19": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x4
    },
    "Treasure Map #20": {
        'classification': ItemClassification.filler,
        'address': 0x1BA651,
        'value': 0x40
    },
    "Treasure Map #21": {
        'classification': ItemClassification.filler,
        'address': 0x1BA650,
        'value': 0x20
    },
    "Treasure Map #22": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 0x08
    },
    "Treasure Map #23": {
        'classification': ItemClassification.filler,
        'address': 0x1BA652,
        'value': 128,
    },
    "Treasure Map #24": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
        'value': 0x2,
    },
    "Treasure Map #25": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
        'value': 0x04,
    },
    "Treasure Map #26": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
        'value': 0x20,
    },
    "Treasure Map #27": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
        'value': 0x8,
    },
    "Treasure Map #28": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
        'value': 1,
    },
    "Treasure Map #29": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
        'value': 0x10,
    },
    "Treasure Map #30": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
        'value': 64,
    },
    "Treasure Map #31": {
        'classification': ItemClassification.filler,
        'address': 0x1BA653,
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
    for item in ITEMS_DATA:
        print(f"\t\"{item}\",")

