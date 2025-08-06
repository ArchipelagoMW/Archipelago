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

    # ======= Regular Items========== TODO check addresses and update

    "Sword (Progressive)": {
        'classification': ItemClassification.progression,
        'progressive': [[0x265322, 0x02], [0x265322, 0x04]],
        #'set_bit': [(0x1BA644, 1)]  # Means that sending sword if sword breaks gives the base layer
    },
    "Shield": {
        'classification': ItemClassification.useful,
        'address': 0x265322,
        'value': 0x01
    },
    "Whirlwind": {
        'classification': ItemClassification.progression,
        'address': 0x265320,
        'value': 0x01,
    },
    "Bombs (Progressive)": {
        'classification': ItemClassification.progression,
        "progressive": [[0x265320, 0x10]], #[0x1BA5D2, 1], [0x1BA5D2, 2]],
        #"progressive_overwrite": True,
        #"give_ammo": [10, 20, 30],
        #"ammo_address": 0x1BA6C0
    },
    "Bow (Progressive)": {
        'classification': ItemClassification.progression,
        "progressive": [[0x265320, 0x08]], #[0x1BA5D0, 1], []],
        #"give_ammo": [20, 30, 50],
        #"ammo_address": 0x1BA6C2,
        #"progressive_overwrite": True,
    },
    "Whip": {
        'classification': ItemClassification.progression,
        'address': 0x265320,
        'value': 0x04,
    },
    "Boomerang": {
        'classification': ItemClassification.progression,
        'address': 0x265320,
        'value': 0x02,
    },
    "Sand Wand": {
        'classification': ItemClassification.progression,
        'address': 0x265320,
        'value': 0x20,
    },
    "Spirit Flute": {
        'classification': ItemClassification.progression,
        'address': 0x265322,
        'value': 0x0080,
    },

    # ======= Misc Items==========

    "Recruit Uniform": {
        'classification': ItemClassification.progression,
        #'address': 0x1BA645,
        #'value': 0x01,
        #'set_bit': [(0x1BA6C8, 1)]
    },
    "Engineer's Clothes": {
        'classification': ItemClassification.filler,
        #'address': 0x1BA645,
        #'value': 0x01,
        #'set_bit': [(0x1BA6C8, 1)]
    },
    "Compass of Light": {
        'classification': ItemClassification.progression,
        'address': 0x265739,
        'value': 0x20,
    },
    "Royal Engineer's Certificate": {
        'classification': ItemClassification,
        'address': 0x265717,
        'value': 0x01,
    },
    "Rabbit Net": {
        'classification': ItemClassification.progression,
        #'address': ,
        #'value': ,
    },
    "Tears of Light": {
        'classification': ItemClassification.progression,
        #'address': ,
        #'value': ,
    },
    "Stamp Book": {
        'classification': ItemClassification.progression,
        'address': 0x265739,
        'value': 0x02,
    },

    # ======= Songs ==========

    "Song of Awakening": {
        'classification': ItemClassification.progression,
        'address': 0x268FB0,
        'value': 0x01,
    },
    "Song of Healing": {
        'classification': ItemClassification.progression,
        'address': 0x268FB0,
        'value': 0x02,
    },
    "Song of Birds": {
        'classification': ItemClassification.progression,
        'address': 0x268FB0,
        'value': 0x04,
    },
    "Song of Light": {
        'classification': ItemClassification.progression,
        'address': 0x268FB0,
        'value': 0x08,
    },
    "Song of Discovery": {
        'classification': ItemClassification.progression,
        'address': 0x268FB0,
        'value': 0x10,
    },

    # ============= Spirits and Upgrades =============


    "Heart Container": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        #'address': 0x1BA388,
        'value': 4,
        'incremental': True,
        'size': 2
    },
        "Sword Beam Swordsman's Scroll": {
        'classification': ItemClassification.useful,
        'address': 0x265322,
        'value': 0x0010,
    },
    "Great Spin Swordsman's Scroll": {
        'classification': ItemClassification.useful,
        'address': 0x265322,
        'value': 0x0020,
    },

    # ============= Train Items =============

    "Cannon": {
        'classification': ItemClassification.progression,
        #'address': 0x265716, TODO check this
        #'value': 0x40
    },

    # ========== Rail Maps ============

    "Forest Realm Rail Map": {
        'classification': ItemClassification.progression,
        'address': 0x265715,
        'value': 0x80,
        'set_bit': [(0x265716, 0)]
    },
    "Snow Realm Rail Map": {
        'classification': ItemClassification.progression,
        'address': 0x265716,
        'value': 0x01,
        'set_bit': [(0x265715, 0x80)]
    },
    "Ocean Realm Rail Map": {
        'classification': ItemClassification.progression,
        'address': 0x265716,
        'value': 0x02,
        'set_bit': [(0x265715, 0x80)]
    },
    "Fire Realm Rail Map": {
        'classification': ItemClassification.progression,
        'address': 0x265716,
        'value': 0x04,
        'set_bit': [(0x265715, 0x80)]
    },

    # ========= Force Gems ==============

    # Warp gates require cannon
    "Force Gem 1": {
        'classification': ItemClassification.progression,
        #'address': 0x265716,
        #'value': 0x40
    },

    # ========== Rupees and filler =============

    "Green Rupee (1)": {
        'classification': ItemClassification.filler,
        'address': 0x265328,
        'value': 1,
        'incremental': True,
        'size': 2
    },
    "Blue Rupee (5)": {
        'classification': ItemClassification.filler,
        'address': 0x265328,
        'value': 5,
        'incremental': True,
        'size': 2
    },
    "Red Rupee (20)": {
        'classification': ItemClassification.filler,
        'address': 0x265328,
        'value': 20,
        'incremental': True,
        'size': 2
    },
    "Big Green Rupee (100)": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'address': 0x265328,
        'value': 100,
        'incremental': True,
        'size': 2
    },
    "Big Red Rupee (200)": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'address': 0x265328,
        'value': 200,
        'incremental': True,
        'size': 2
    },
    "Gold Rupee (300)": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'address': 0x265328,
        'value': 300,
        'incremental': True,
        'size': 2
    },
    "Rupoor (-10)": {
        'classification': ItemClassification.trap,
        'address': 0x265328,
        'value': -10,
        'incremental': True,
        'size': 2
    },
    "Big Rupoor (-50)": {
        'classification': ItemClassification.trap,
        'address': 0x265328,
        'value': -50,
        'incremental': True,
        'size': 2
    },
    "Pre-Alpha Rupee (5000)": {
        'classification': ItemClassification.progression,
        'address': 0x265328,
        'value': 5000,
        'incremental': True,
        'size': 2
    },
    "Treasure": {
        'classification': ItemClassification.filler,
        'incremental': True
    },
    "Train Part": {
        'classification': ItemClassification.filler,
        'train_part': True
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
        #"address": 0x1BA6C0,
        "refill": "Bombs (Progressive)"
    },
    "Refill: Arrows": {
        'classification': ItemClassification.filler,
        "give_ammo": [20, 30, 50],
        #"address": 0x1BA6C2,
        "refill": "Bow (Progressive)"
    },

    # ========= Treasure =============

    "Treasure: Pink Coral": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5AC,
        'incremental': True
    },
    "Treasure: White Pearl Loop": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5AD,
        'incremental': True
    },
    "Treasure: Dark Pearl Loop": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5AE,
        'incremental': True
    },
    "Treasure: Zora Scale": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5AF,
        'incremental': True
    },
    "Treasure: Goron Amber": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5B0,
        'incremental': True
    },
    "Treasure: Ruto Crown": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5B1,
        'incremental': True
    },
    "Treasure: Helmaroc Plume": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5B2,
        'incremental': True
    },
    "Treasure: Regal Ring": {
        'classification': ItemClassification.progression_skip_balancing,
        'backup_filler': True,
        'treasure': True,
        #'address': 0x1BA5B3,
        'incremental': True
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

    # Trade Quest and misc

    # Warp Gates
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

    # Trains
    "Train: Bright Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 1
    },
    "Train: Iron Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 2
    },
    "Train: Stone Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 3
    },
    "Train: Vintage Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 4
    },
    "Train: Demon Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 5
    },
    "Train: Tropical Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 6
    },
    "Train: Dignified Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 7
    },
    "Train: Golden Train": {
        'classification': ItemClassification.useful,
        'backup_filler': True,
        'train': 8
    },
}


# Oops apparently not a constant lul (it will be after this)
for i, k in enumerate(ITEMS_DATA.keys()):
    ITEMS_DATA[k]["id"] = i+1

