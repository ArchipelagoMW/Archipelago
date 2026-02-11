from BaseClasses import ItemClassification
from ..Subclasses import PHItem
from .Addresses import *

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
        "progressive": [(PHAddr.inventory_1, 0x1), (PHAddr.inventory_5, 0x20)],
        "set_bit": [(PHAddr.inventory_1, 0x1), (PHAddr.sword_count, 1)],
        "id": 1,
    },
    "Oshus' Sword": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x1,
        "ammo_address": PHAddr.sword_count,  # used to remove sword model
        "set_bit": [(PHAddr.sword_count, 1)],
        "id": 2,
    },
    "Phantom Sword": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x20,
        "id": 3,
    },
    "Shield": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x2,
        "id": 4,
    },
    "Boomerang": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x4,
        "set_bit": [(PHAddr.boomerang_bit, 0x1)],
        "id": 5,
        "inventory_id": 2,
    },
    "Bombs (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.inventory_1, 0x10), (PHAddr.bomb_upgrades, 0x1), (PHAddr.bomb_upgrades, 0x2)],
        "give_ammo": [0xa, 0x14, 0x1e],
        "ammo_address": PHAddr.bomb_count,
        "set_bit": [(PHAddr.inventory_1, 0x10)],
        "id": 6,
        "inventory_id": 4,
        "tags": ["progressive_overwrite"],
    },
    "Bombchus (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.inventory_1, 0x80), (PHAddr.chu_upgrades, 0x1), (PHAddr.chu_upgrades, 0x2)],
        "give_ammo": [0xa, 0x14, 0x1e],
        "ammo_address": PHAddr.chu_count,
        "tags": ["progressive_overwrite"],
        "set_bit": [(PHAddr.inventory_1, 0x80)],
        "id": 7,
        "inventory_id": 7,
    },
    "Bow (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.inventory_1, 0x20), (PHAddr.quiver_upgrades, 0x1), (PHAddr.quiver_upgrades, 0x2)],
        "give_ammo": [0x14, 0x1e, 0x32],
        "ammo_address": PHAddr.arrow_count,
        "tags": ["progressive_overwrite"],
        "set_bit": [(PHAddr.inventory_1, 0x20)],
        "id": 8,
        "inventory_id": 5,
    },
    "Grappling Hook": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x40,
        "set_bit": [(PHAddr.grapple_bit, 0x1)],
        "id": 9,
        "inventory_id": 6,
    },
    "Shovel": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x8,
        "set_bit": [(PHAddr.shovel_bit, 0x1)],
        "id": 10,
        "inventory_id": 3,
    },
    "Hammer": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_2,
        "value": 0x1,
        "set_bit": [(PHAddr.hammer_bit, 0x1)],
        "id": 11,
        "inventory_id": 8,
    },

    # Spirits
    "Spirit of Power (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.fairies_0, 0x20), (PHAddr.fairies_1, 0x1), (PHAddr.fairies_1, 0x8)],
        "id": 12,
    },
    "Spirit of Wisdom (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.fairies_0, 0x40), (PHAddr.fairies_1, 0x2), (PHAddr.fairies_1, 0x10)],
        "id": 13,
    },
    "Spirit of Courage (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.fairies_0, 0x10), (PHAddr.fairies_0, 0x80), (PHAddr.fairies_1, 0x4)],
        "id": 14,
    },
    "Spirit of Courage (White)": {  # Used to remove spirit from Temple of Courage
        "classification": ItemClassification.progression,
        "address": PHAddr.fairies_1,
        "value": 0x20,
        "id": 15,
    },

    # Upgrades
    "Heart Container": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.heart_containers,
        "value": 0x4,
        "tags": ["monotone_incremental"],
        "base_count": 12,
        "size": 2,
        "id": 16,
    },
    "Phantom Hourglass": {
        "classification": ItemClassification.progression,
        "address": PHAddr.phantom_hourglass_max,
        "value": "Sand PH",
        "tags": ["monotone_incremental"],
        "size": 4,
        "id": 17,
    },
    "Sand of Hours (Boss)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.phantom_hourglass_max,
        "value": 0x1c20,
        "tags": ["incremental", "backup_filler"],
        "size": 4,
        "id": 18,
    },
    "Sand of Hours (Small)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.phantom_hourglass_max,
        "value": 0xe10,
        "tags": ["incremental", "backup_filler"],
        "size": 4,
        "id": 19,
    },
    "Sand of Hours": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.phantom_hourglass_max,
        "value": "Sand",
        "tags": ["monotone_incremental"],
        "size": 4,
        "id": 20,
    },
    "Swordsman's Scroll": {
        "classification": ItemClassification.useful,
        "address": PHAddr.inventory_6,
        "value": 0x20,
        "id": 21,
    },

    # Ship Items
    "Cannon": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_cannon,
        "value": 0x1,
        "id": 22,
    },
    "Salvage Arm": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x10,
        "id": 23,
    },
    "Fishing Rod": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x1,
        "id": 24,
    },
    "Big Catch Lure": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x80,
        "id": 25,
    },
    "Swordfish Shadows": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_43,
        "value": 0x10,
        "id": 26,
    },
    "Cyclone Slate": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x40,
        "id": 27,
    },

    # Sea Charts
    "SW Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x2,
        "id": 28,
        "disconnect_entrances": [
            "Ocean SW Mercay",
            "Ocean SW Cannon",
            "Ocean SW Ember",
            "Ocean SW Molida",
            "Ocean SW Spirit",
        ],
    },
    "NW Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x4,
        "id": 29,
        "disconnect_entrances": [
            "Ocean NW Gust",
            "Ocean NW Bannan",
            "Ocean NW Zauz",
            "Ocean NW Uncharted",
            "Ocean NW Board Ghost Ship",
        ]
    },
    "SE Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x8,
        "set_bit": [(PHAddr.adv_flags_1, 0x8)],
        "id": 30,
        "disconnect_entrances": [
            "Ocean SE Goron",
            "Ocean SE Harrow",
            "Ocean SE Dee Ess",
            "Ocean SE Frost",
        ],
    },
    "NE Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x10,
        "id": 31,
        "disconnect_entrances": [
            "Ocean NE IotD",
            "Ocean NE Ruins",
            "Ocean NE Maze",
        ],
    },
    # Spirit gems
    "Power Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.power_gem_count,
        "value": 0x1,
        "tags": ["monotone_incremental"],
        "id": 32,
    },
    "Wisdom Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.wisdom_gem_count,
        "value": 0x1,
        "tags": ["monotone_incremental"],
        "id": 33,
    },
    "Courage Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.courage_gem_count,
        "value": 0x1,
        "tags": ["monotone_incremental"],
        "id": 34,
    },
    "Power Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.power_gem_count,
        "value": "pack_size",
        "tags": ["monotone_incremental"],
        "id": 35,
    },
    "Wisdom Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.wisdom_gem_count,
        "value": "pack_size",
        "tags": ["monotone_incremental"],
        "id": 36,
    },
    "Courage Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.courage_gem_count,
        "value": "pack_size",
        "tags": ["monotone_incremental"],
        "id": 37,
    },

    # Rupees and filler
    "Green Rupee (1)": {
        "classification": ItemClassification.filler,
        "address": PHAddr.rupee_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 2,
        "id": 38,
    },
    "Blue Rupee (5)": {
        "classification": ItemClassification.filler,
        "address": PHAddr.rupee_count,
        "value": 0x5,
        "tags": ["incremental"],
        "size": 2,
        "id": 39,
    },
    "Red Rupee (20)": {
        "classification": ItemClassification.filler,
        "address": PHAddr.rupee_count,
        "value": 0x14,
        "tags": ["incremental"],
        "size": 2,
        "id": 40,
    },
    "Big Green Rupee (100)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.rupee_count,
        "value": 0x64,
        "tags": ["incremental", "backup_filler"],
        "size": 2,
        "id": 41,
    },
    "Big Red Rupee (200)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.rupee_count,
        "value": 0xc8,
        "tags": ["incremental", "backup_filler"],
        "size": 2,
        "id": 42,
    },
    "Gold Rupee (300)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.rupee_count,
        "value": 0x12c,
        "tags": ["incremental", "backup_filler"],
        "size": 2,
        "id": 43
    },
    "Rupoor (-10)": {
        "classification": ItemClassification.trap,
        "address": PHAddr.rupee_count,
        "value": -0xa,
        "tags": ["incremental"],
        "size": 2,
        "id": 44,
    },
    "Big Rupoor (-50)": {
        "classification": ItemClassification.trap,
        "address": PHAddr.rupee_count,
        "value": -0x32,
        "tags": ["incremental"],
        "size": 2,
        "id": 45,
    },
    "Pre-Alpha Rupee (5000)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.rupee_count,
        "value": 0x1388,
        "tags": ["incremental"],
        "size": 2,
        "id": 46,
    },
    "Treasure": {
        "classification": ItemClassification.filler,
        "tags": ["incremental"],
        "id": 47,
    },
    "Ship Part": {
        "classification": ItemClassification.filler,
        "tags": ["ship_part"],
        "id": 48,
    },
    "Potion": {
        "classification": ItemClassification.filler,
        "id": 49,
    },
    "Red Potion": {
        "classification": ItemClassification.filler,
        "value": 1,
        "id": 50,
        "overflow_item": "Big Green Rupee (100)"
    },
    "Purple Potion": {
        "classification": ItemClassification.filler,
        "value": 2,
        "id": 51,
        "overflow_item": "Big Green Rupee (100)"
    },
    "Yellow Potion": {
        "classification": ItemClassification.filler,
        "value": 3,
        "id": 52,
        "overflow_item": "Big Red Rupee (200)"
    },
    "Nothing!": {
        "classification": ItemClassification.filler,
        "dummy": True,
        "id": 53,
    },
    "Refill: Bombs": {
        "classification": ItemClassification.filler,
        "give_ammo": [0xa, 0x14, 0x1e],
        "address": PHAddr.bomb_count,
        "refill": "Bombs (Progressive)",
        "id": 54,
    },
    "Refill: Arrows": {
        "classification": ItemClassification.filler,
        "give_ammo": [0x14, 0x1e, 0x32],
        "address": PHAddr.arrow_count,
        "refill": "Bow (Progressive)",
        "id": 55,
    },
    "Refill: Bombchus": {
        "classification": ItemClassification.filler,
        "give_ammo": [0xa, 0x14, 0x1e],
        "address": PHAddr.chu_count,
        "refill": "Bombchus (Progressive)",
        "id": 56,
    },
    "Salvage Repair Kit": {
        "classification": ItemClassification.filler,
        "address": PHAddr.custom_storage,
        "value": 0x20,
        "tags": ["incremental"],
        "id": 57,
        "max": 0xFF
    },
    "Refill: Health": {
        "classification": ItemClassification.filler,
        "value": "full_heal",
        "id": 193,
    },

    # Treasure
    "Treasure: Pink Coral": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.pink_coral_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 58,
    },
    "Treasure: White Pearl Loop": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.wpl_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 59,
    },
    "Treasure: Dark Pearl Loop": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.dpl_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 60,
    },
    "Treasure: Zora Scale": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.zora_scale_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 61,
    },
    "Treasure: Goron Amber": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.goron_amber_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 62,
    },
    "Treasure: Ruto Crown": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.ruto_crown_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 63,
    },
    "Treasure: Helmaroc Plume": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.roc_feather_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 64,
    },
    "Treasure: Regal Ring": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.regal_ring_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 65,
    },

    # Salvage
    "Courage Crest": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_16,
        "value": 0x4,
        "set_bit": [(PHAddr.treasure_maps_0, 0x1)],
        "id": 66,
    },
    "Treasure Map #1 (Molida SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x80,
        "id": 67,
        "hint_on_receive": ["Ocean SW Salvage #1 Molida SW"],
    },
    "Treasure Map #2 (Mercay NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x10,
        "id": 68,
        "hint_on_receive": ["Ocean SW Salvage #2 Mercay NE"],
    },
    "Treasure Map #3 (Gusts SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x20,
        "id": 69,
        "hint_on_receive": ["Ocean NW Salvage #3 Gusts SW"],
    },
    "Treasure Map #4 (Bannan SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x80,
        "id": 70,
        "hint_on_receive": ["Ocean NW Salvage #4 Bannan SE"],
    },
    "Treasure Map #5 (Molida N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x40,
        "id": 71,
        "hint_on_receive": ["Ocean SW Salvage #5 Molida N"],
    },
    "Treasure Map #6 (Bannan W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x1,
        "id": 72,
        "hint_on_receive": ["Ocean NW Salvage #6 Bannan W"],
    },
    "Treasure Map #7 (Gusts E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x8,
        "id": 73,
        "hint_on_receive": ["Ocean NW Salvage #7 Gusts E"],
    },
    "Treasure Map #8 (Mercay SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x8,
        "id": 74,
        "hint_on_receive": ["Ocean SW Salvage #8 Mercay SE"],
    },
    "Treasure Map #9 (Cannon W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x2,
        "id": 75,
        "hint_on_receive": ["Ocean SW Salvage #9 Cannon W"],
    },
    "Treasure Map #10 (Gusts SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x10,
        "id": 76,
        "hint_on_receive": ["Ocean NW Salvage #10 Gusts SE"],
    },
    "Treasure Map #11 (Gusts N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x2,
        "id": 77,
        "hint_on_receive": ["Ocean NW Salvage #11 Gusts N"],
    },
    "Treasure Map #12 (Dee Ess N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x20,
        "id": 78,
        "hint_on_receive": ["Ocean SE Salvage #12 Dee Ess N"],
    },
    "Treasure Map #13 (Harrow E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x4,
        "id": 79,
        "hint_on_receive": ["Ocean SE Salvage #13 Harrow E"],
    },
    "Treasure Map #14 (Goron NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x1,
        "id": 80,
        "hint_on_receive": ["Ocean SE Salvage #14 Goron NW"],
    },
    "Treasure Map #15 (Goron W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x2,
        "id": 81,
        "hint_on_receive": ["Ocean SE Salvage #15 Goron W"],
    },
    "Treasure Map #16 (Goron NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x10,
        "id": 82,
        "hint_on_receive": ["Ocean SE Salvage #16 Goron NE"],
    },
    "Treasure Map #17 (Frost S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x40,
        "id": 83,
        "hint_on_receive": ["Ocean SE Salvage #17 Frost S"],
    },
    "Treasure Map #18 (Cannon S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x4,
        "id": 84,
        "hint_on_receive": ["Ocean SW Salvage #18 Cannon S"],
    },
    "Treasure Map #19 (Gusts NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x4,
        "id": 85,
        "hint_on_receive": ["Ocean NW Salvage #19 Gusts NE"],
    },
    "Treasure Map #20 (Bannan E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x40,
        "id": 86,
        "hint_on_receive": ["Ocean NW Salvage #20 Bannan E"],
    },
    "Treasure Map #21 (Molida NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x20,
        "id": 87,
        "hint_on_receive": ["Ocean SW Salvage #21 Molida NW"],
    },
    "Treasure Map #22 (Harrow S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x8,
        "id": 88,
        "hint_on_receive": ["Ocean SE Salvage #22 Harrow S"],
    },
    "Treasure Map #23 (Frost NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x80,
        "id": 89,
        "hint_on_receive": ["Ocean SE Salvage #23 Frost NW"],
    },
    "Treasure Map #24 (Ruins W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x20,
        "id": 90,
        "hint_on_receive": ["Ocean NE Salvage #24 Ruins W"],
    },
    "Treasure Map #25 (Dead E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x4,
        "id": 91,
        "hint_on_receive": ["Ocean NE Salvage #25 Dead E"],
    },
    "Treasure Map #26 (Ruins SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x2,
        "id": 92,
        "hint_on_receive": ["Ocean NE Salvage #26 Ruins SW"],
    },
    "Treasure Map #27 (Maze E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x8,
        "id": 93,
        "hint_on_receive": ["Ocean NE Salvage #27 Maze E"],
    },
    "Treasure Map #28 (Ruins NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x1,
        "id": 94,
        "hint_on_receive": ["Ocean NE Salvage #28 Ruins NW"],
    },
    "Treasure Map #29 (Maze W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x10,
        "id": 95,
        "hint_on_receive": ["Ocean NE Salvage #29 Maze W"],
    },
    "Treasure Map #30 (Ruins S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x40,
        "id": 96,
        "hint_on_receive": ["Ocean NE Salvage #30 Ruins S"],
    },
    "Treasure Map #31 (Dead S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x80,
        "id": 97,
        "hint_on_receive": ["Ocean NE Salvage #31 Dead S"],
    },

    # Keys
    "Small Key (Mountain Passage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x27,
        "tags": ["incremental"],
        "id": 98,
    },
    "Small Key (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x25,
        "tags": ["incremental", "always_process"],
        "id": 99,
    },
    "Small Key (Temple of Fire)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1c,
        "tags": ["incremental"],
        "id": 100,
    },
    "Small Key (Temple of Wind)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1d,
        "tags": ["incremental"],
        "id": 101,
    },
    "Small Key (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1e,
        "tags": ["incremental"],
        "id": 102,
    },
    "Small Key (Temple of Ice)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1f,
        "tags": ["incremental"],
        "id": 103,
    },
    "Small Key (Mutoh's Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x21,
        "tags": ["incremental"],
        "id": 104,
    },
    "Boss Key (Temple of Fire)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1c,
        "id": 105,
        "tags": ["always_process"]
    },
    "Boss Key (Temple of Wind)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1d,
        "id": 106,
        "tags": ["always_process"],
    },
    "Boss Key (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1e,
        "id": 107,
        "tags": ["always_process"],
    },
    "Boss Key (Goron Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x20,
        "id": 108,
        "tags": ["always_process"],
    },
    "Boss Key (Temple of Ice)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1f,
        "id": 109,
        "tags": ["always_process"],
    },
    "Boss Key (Mutoh's Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x21,
        "id": 110,
        "tags": ["always_process"],
    },
    "Square Crystal (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1e,
        "tags": ["always_process"],
        "id": 111,
        "set_bit_in_room": {0x1E00: [(PHAddr.toc_crystal_state, 0x10),
                                     ("stage_flag", 0x80)]}
    },
    "Square Pedestal North (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x1e,
        "id": 194,
        "set_bit_in_room": {0x1E00: [(PHAddr.toc_crystal_state, 0x10)]}
    },
    "Square Pedestal South (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x1e,
        "id": 195,
        "set_bit_in_room": {0x1E00: [("stage_flag", 0x80)]}
    },
    "Triangle Crystal (Ghost Ship)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x29,
        "id": 112,
        "set_bit_in_room": {0x2900: [("stage_flag", [0, 8])]}
    },
    "Round Crystal (Ghost Ship)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x29,
        "id": 113,
        "set_bit_in_room": {0x2900: [("stage_flag", [0, 0, 0, 2])]}
    },
    "Round Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 114,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x2)],  # format: dict[room, list[tuple[addr, value, *dict(extra data)]]]
                            0x250C: [(PHAddr.totok_b9_state, 0x4)]}
    },
    "Round Pedestal B8 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 196,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x2)]}
    },
    "Round Pedestal B9 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 197,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x4)]}
    },
    "Round Crystals": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 204,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x2)],
                            0x250C: [(PHAddr.totok_b9_state, 0x4)],
                            0x2900: [("stage_flag", [0, 0, 0, 2])]}
    },
    "Triangle Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 115,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x4)],
                            0x250C: [(PHAddr.totok_b9_state, 0x8)]}
    },
    "Triangle Pedestal B8 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 198,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x4)]}
    },
    "Triangle Pedestal B9 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 199,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x8)]}
    },
    "Triangle Crystals": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": True,
        "id": 203,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x4)],
                            0x250C: [(PHAddr.totok_b9_state, 0x8)],
                            0x2900: [("stage_flag", [0, 8])]}
    },
    "Square Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 116,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x22)]}
    },
    "Square Pedestal West (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 200,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x20)]}
    },
    "Square Pedestal Center (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 201,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x2)]}
    },
    "Square Crystals": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "tags": ["always_process"],
        "id": 202,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x22)],
                            0x1E00: [(PHAddr.toc_crystal_state, 0x10),
                                     ("stage_flag", 0x80)]}
    },
    "Force Gem (B3)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 117,
        "set_bit_in_room": {0x2503: [(PHAddr.totok_b3_state, 0xFE, {"count": 3}),
                                     (PHAddr.totok_b3_state_1, 0xF, {"count": 3})]}
    },
    "Force Gem (B12)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 118,
        "set_bit_in_room": {0x2510: [(PHAddr.totok_b12_state, 0xFE, {"count": 3}),
                                     (PHAddr.totok_b12_state_1, 0xF, {"count": 3}),
                                     (PHAddr.totok_b12_state, 0xC, {"count": 2}),
                                     (PHAddr.totok_b12_state, 0x4, {"count": 1})]}
    },
    "Force Gems": {
        "classification": ItemClassification.progression,
        "id": 205,
        "tags": ["always_process"],
        "set_bit_in_room": {0x2503: [(PHAddr.totok_b3_state, 0xFE),
                                     (PHAddr.totok_b3_state_1, 0xF)],
                            0x2510: [(PHAddr.totok_b12_state, 0xFE),
                                     (PHAddr.totok_b12_state_1, 0xF)]}
    },
    "Triforce Crest": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_4,
        "value": 0x2,
        "id": 119,
    },
    "Sun Key": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x40,
        "id": 120,
    },
    "Ghost Key": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x8,
        "id": 121,
    },
    "King's Key": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x4,
        "id": 122,
    },
    "Regal Necklace": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_6,
        "value": 0x8,
        "id": 123,
    },

    # Metals
    "Crimzonine": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_metals,
        "value": 0x40,
        "id": 124,
    },
    "Azurine": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_metals,
        "value": 0x20,
        "id": 125,
    },
    "Aquanine": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_metals,
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
        "address": PHAddr.flags_trade_quest,
        "value": 0x4,
        "id": 157,
    },
    "Kaleidoscope": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x8,
        "id": 158,
    },
    "Guard Notebook": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x10,
        "id": 159,
    },
    "Wood Heart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x80,
        "id": 160,
    },
    "Phantom Blade": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_22,
        "value": 0x20,
        "id": 161,
    },

    # Letters and cards
    "Freebie Card": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.adv_flags_14,
        "value": 0x40,
        "id": 162,
        "tags": ["backup_filler"]
    },
    "Member's Card (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.adv_flags_12, 0x40), (PHAddr.adv_flags_18, 0x20), (PHAddr.adv_flags_18, 0x40), (PHAddr.adv_flags_18, 0x80), (PHAddr.adv_flags_19, 0x1)],
        "id": 163,
    },
    "Complimentary Card": {
        "classification": ItemClassification.filler,
        "address": PHAddr.adv_flags_14,
        "value": 0x20,
        "id": 164,
    },
    "Compliment Card": {
        "classification": ItemClassification.filler,
        "address": PHAddr.adv_flags_14,
        "value": 0x80,
        "id": 190,
    },
    "Jolene's Letter": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x20,
        "id": 165,
    },
    "Prize Postcard": {
        "classification": ItemClassification.filler,
        "address": PHAddr.adv_flags_19,
        "value": 0x8,
        "id": 166,
    },
    "Beedle Points (10)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.beedle_points,
        "tags": ["incremental"],
        "value": 10,
        "id": 167,
    },
    "Beedle Points (20)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.beedle_points,
        "value": 20,
        "tags": ["incremental"],
        "id": 191,
    },
    "Beedle Points (50)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.beedle_points,
        "value": 50,
        "tags": ["incremental"],
        "id": 192,
    },

    # Frogs
    "Golden Frog Glyph X": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_38,
        "value": 0x80,
        "id": 168,
    },
    "Golden Frog Glyph Phi": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x1,
        "id": 169,
    },
    "Golden Frog Glyph N": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x2,
        "id": 170,
    },
    "Golden Frog Glyph Omega": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x4,
        "id": 171,
    },
    "Golden Frog Glyph W": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x8,
        "id": 172,
    },
    "Golden Frog Glyph Square": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
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
        "tags": ["backup_filler"],
        "ship": 0x1,
        "id": 175,
    },
    "Ship: Iron Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x2,
        "id": 176,
    },
    "Ship: Stone Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x3,
        "id": 177,
    },
    "Ship: Vintage Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x4,
        "id": 178,
    },
    "Ship: Demon Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x5,
        "id": 179,
    },
    "Ship: Tropical Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x6,
        "id": 180,
    },
    "Ship: Dignified Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x7,
        "id": 181,
    },
    "Ship: Golden Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x8,
        "id": 182,
    },

    # Fish
    "Fish: Skippyjack": {
        "classification": ItemClassification.filler,
        "address": PHAddr.skippyjack_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 183,
    },
    "Fish: Toona": {
        "classification": ItemClassification.filler,
        "address": PHAddr.toona_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 184,
    },
    "Fish: Loovar": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.loovar_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 185,
    },
    "Fish: Rusty Swordfish": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.rsf_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 186,
    },
    "Fish: Legendary Neptoona": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.neptoona_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 187,
    },
    "Fish: Stowfish": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.stowfish_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 188,
    },
    "_UT_Glitched_Logic": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 189,
    },
    "Map Warp: Mercay": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 206,
        "tags": ["backup_filler"],
    },
    "Map Warp: Cannon": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 207,
        "tags": ["backup_filler"],
    },
    "Map Warp: Ember": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 208,
        "tags": ["backup_filler"],
    },
    "Map Warp: Molida": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 209,
        "tags": ["backup_filler"],
    },
    "Map Warp: Spirit": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 210,
        "tags": ["backup_filler"],
    },
    "Map Warp: Gust": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 211,
        "tags": ["backup_filler"],
    },
    "Map Warp: Bannan": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 212,
        "tags": ["backup_filler"],
    },
    "Map Warp: Uncharted": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 213,
        "tags": ["backup_filler"],
    },
    "Map Warp: Zauz": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 214,
        "tags": ["backup_filler"],
    },
    "Map Warp: Goron": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 215,
        "tags": ["backup_filler"],
    },
    "Map Warp: Frost": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 216,
        "tags": ["backup_filler"],
    },
    "Map Warp: Harrow": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 217,
        "tags": ["backup_filler"],
    },
    "Map Warp: Dee Ess": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 218,
        "tags": ["backup_filler"],
    },
    "Map Warp: Isle of the Dead": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 219,
        "tags": ["backup_filler"],
    },
    "Map Warp: Ruins": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 220,
        "tags": ["backup_filler"],
    },
    "Map Warp: Maze": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 221,
        "tags": ["backup_filler"],
    },
}
ITEMS: dict[str, "PHItem"] = dict()
item_id_to_name_dict: dict[int, str] = dict()

id_check = []
for name, data in ITEMS_DATA.items():
    if data["id"] in id_check:
        raise f"Duplicate ID Detected: {data['id']}"
    id_check.append(data["id"])
    item_id_to_name_dict[data["id"]] = name
    ITEMS[name] = PHItem(name, data, ITEMS)

# IDs are now fixed!!!
"""for i, k in enumerate(ITEMS_DATA):
    ITEMS_DATA[k]["id"] = i+1"""

# bulk data editing / export
if __name__ == "__main__":
    attributes = set()
    for name, data in ITEMS_DATA.items():
        for attribute in data:
            attributes.add(attribute)
    for attribute in attributes:
        print(f"self.{attribute}: ")
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
