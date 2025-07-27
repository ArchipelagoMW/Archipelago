import time

from worlds.tloz_ph.data.Constants import *

# TODO: Add sram data for saveslot 2
# TODO: Add the rest of sram data in bulk

LOCATIONS_DATA = {
    "Mercay Sword Chest": {
        "region_id": "mercay island",
        "item_override": "Sword (Progressive)",
        "vanilla_item": "Oshus' Sword",
        "stage_id": 11,
        "floor_id": 19,
        "sram_addr": 0x00043C,
        "sram_value": 0x1
    },
    "Mercay Clear Rocks": {
        "region_id": "mercay island",
        "vanilla_item": "Green Rupee (1)",
        "stage_id": 11,
        "floor_id": 0,
        "y": 0,
        "x_max": -170000,
        "sram_addr": 0x0020CA,
        "sram_value": 0x40
    },
    "Mercay Oshus Dig": {
        "region_id": "mercay dig spot",
        "stage_id": 11,
        "floor_id": 0,
        "y": 0x1333,
        "vanilla_item": "Treasure Map #10 (Gusts SE)",
    },
    "Mercay Cuccoo Chest": {
        "region_id": "mercay island",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x1333,
        "vanilla_item": "Treasure",
        "sram_addr": 0x0003C4,
        "sram_value": 0x08
    },
    "Mercay North Bonk Tree": {
        "region_id": "mercay island",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x2666,
        "sram_addr": 0x0017AC,
        "sram_value": 1,
        "vanilla_item": "Big Green Rupee (100)"
    },
    "Mercay Geozard Cave Chest": {
        "region_id": "mercay zora cave",
        "stage_id": 11,
        "floor_id": 16,
        "vanilla_item": "Power Gem",
        "sram_addr": 0x000418,
        "sram_value": 1
    },
    "Mercay Geozard Cave South Chest West": {
        "region_id": "mercay zora cave south",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x2666,
        "x_max": 0x00016200,
        "vanilla_item": "Ship Part",
        "sram_addr": 0x0003C4,
        "sram_value": 0x02
    },
    "Mercay Geozard Cave South Chest East": {
        "region_id": "mercay zora cave south",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x2666,
        "x_min": 0x00016200,
        "vanilla_item": "Big Green Rupee (100)",
        "sram_addr": 0x0003C4,
        "sram_value": 0x04
    },
    "TotOK Phantom Hourglass": {
        "region_id": "totok",
        "stage_id": 38,
        "floor_id": 0,
        "address": 0x1B55A0,
        "value": 0x4,
        "y": 0x399A,
        "vanilla_item": "Nothing!",
        # "item_override": "Phantom Hourglass",
    },
    "Mercay Freedle Tunnel Chest": {
        "region_id": "mercay freedle tunnel chest",
        "stage_id": 11,
        "floor_id": 18,
        "vanilla_item": "Courage Gem",
        "sram_addr": 0x000430,
        "sram_value": 1
    },
    "Mercay Freedle Island Chest": {
        "region_id": "mercay freedle island",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x4CCD,
        "x_min": 0x00025000,
        "vanilla_item": "Wisdom Gem",
        "sram_addr": 0x0003AC,
        "sram_value": 64
    },
    "Mercay Freedle Gift Item": {
        "region_id": "mercay freedle gift",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x4CCD,
        "x_max": 0x00025000,
        "vanilla_item": "Treasure Map #12 (Dee Ess N)",
        # "sram_addr": 0x000EB0,  something's bugging with this
        # "sram_value": 0x08
    },
    "Mercay Chartreuse Guy Item": {
        "region_id": "mercay yellow guy",
        "stage_id": 11,
        "floor_id": 3,
        "address": 0x1BA650,
        "value": 2,
        "vanilla_item": "Treasure Map #9 (Cannon W)",
    },
    "Mercay Shipyard Chest": {
        "region_id": "post tof",
        "stage_id": 11,
        "floor_id": 13,
        "vanilla_item": "Ship Part",
        'post_dungeon': "Temple of Fire"
    },
    "Mercay Oshus Spirit Gem": {
        "region_id": "mercay oshus gem",
        "stage_id": 11,
        "floor_id": 10,
        "vanilla_item": "Power Gem",
        "address": 0x1B55A5,
        "value": 0x2,
        "delay_reset": True
    },
    "Mercay Oshus Phantom Sword": {
        "region_id": "mercay oshus phantom blade",
        "stage_id": 11,
        "floor_id": 10,
        "item_override": "Sword (Progressive)",
        "vanilla_item": "Phantom Sword",
        "address": 0x1BA648,
        "value": 0x20
    },


    # Mountain Passage

    "Mountain Passage Chest 1": {
        "region_id": "mercay passage 1",
        "vanilla_item": "Small Key (Mountain Passage)",
        "stage_id": 0x27,
        "floor_id": 0,
        "x_min": 25000,
        "z_min": 25000,
        "sram_addr": 0x000AE4,
        "sram_value": 8,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Chest 2": {
        "region_id": "mercay passage 2",
        "stage_id": 0x27,
        "floor_id": 0,
        "x_min": 0x10900,
        "z_max": -30000,
        "vanilla_item": "Red Rupee (20)",
        "sram_addr": 0x000AE4,
        "sram_value": 2,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Key Drop": {
        "region_id": "mercay passage 2",
        "vanilla_item": "Small Key (Mountain Passage)",
        "stage_id": 0x27,
        "floor_id": 0,
        "z_max": 70000,
        "sram_addr": 0x230,
        "sram_value": 2,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Rat Key": {
        "region_id": "mercay passage rat",
        "vanilla_item": "Small Key (Mountain Passage)",
        "stage_id": 0x27,
        "floor_id": 1,
        "sram_addr": 0x000230,
        "sram_value": 32,
        "dungeon": "Mountain Passage"
    },

    # Shops
    "Island Shop Power Gem": {
        "region_id": "shop power gem",
        "vanilla_item": "Power Gem",
        "stage_id": 11,
        "floor_id": 0x11,
        "additional_rooms": [0xC0E, 0x1014],
        "address": 0x1B5589,
        "value": 0x02,
        "island_shop": True,
        "delay_reset": True
    },
    "Island Shop Quiver": {
        "region_id": "shop quiver",
        "vanilla_item": "Bow (Progressive)",
        "stage_id": 11,
        "floor_id": 0x11,
        "additional_rooms": [0xC0E, 0x1014],
        "address": 0x1B5589,
        "value": 0x08,
        "island_shop": True,
        "delay_reset": True
    },
    "Island Shop Bombchu Bag": {
        "region_id": "shop bombchu bag",
        "vanilla_item": "Bombchus (Progressive)",
        "stage_id": 11,
        "floor_id": 0x11,
        "additional_rooms": [0xC0E, 0x1014],
        "address": 0x1B5589,
        "value": 0x10,
        "island_shop": True,
        "delay_reset": True
    },
    "Island Shop Heart Container": {
        "region_id": "shop heart container",
        "vanilla_item": "Heart Container",
        "stage_id": 11,
        "floor_id": 0x11,
        "additional_rooms": [0xC0E, 0x1014],
        "address": 0x1B5588,
        "value": 0x80,
        "island_shop": True
    },
    "Beedle Shop Bomb Bag": {
        "region_id": "beedle bomb bag",
        "vanilla_item": "Bombs (Progressive)",
        "stage_id": 5,
        "floor_id": 0,
        "address": 0x1B5589,
        "value": 0x04,
        "delay_reset": True
    },
    "Beedle Shop Wisdom Gem": {
        "region_id": "beedle gem",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 5,
        "floor_id": 0,
        "address": 0x1B5589,
        "value": 0x20,
        "delay_reset": True
    },
    "Masked Beedle Heart Container": {
        "region_id": "masked ship hc",
        "vanilla_item": "Heart Container",
        "stage_id": 5,
        "floor_id": 0,
        "address": 0x1B5589,
        "value": 0x01,
        "conditional": True,
        "delay_reset": True
    },
    "Masked Beedle Courage Gem": {
        "region_id": "masked ship gem",
        "vanilla_item": "Courage Gem",
        "stage_id": 5,
        "floor_id": 0,
        "address": 0x1B558A,
        "value": 0x02,
        "conditional": True,
        "delay_reset": True
    },

    # ========== TotOK ==============

    "TotOK 1F SW Sea Chart Chest": {
        "region_id": "totok 1f chart",
        "vanilla_item": "SW Sea Chart",
        "stage_id": 37,
        "floor_id": 0,
        "y": 0x1333,
        'dungeon': "Temple of the Ocean King",
        'set_bit': [(0x1B557D, 2)]
    },
    "TotOK 1F Linebeck Key": {
        "region_id": "totok 1f",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 0,
        "z_min": 0xB000,
        "z_max": 0x11000,
        "x_min": -100,
        'set_bit': [(0x1B557D, 2)],
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK 1F Empty Chest": {
        "region_id": "totok 1f chest",
        "vanilla_item": "Nothing!",
        "stage_id": 37,
        "floor_id": 0,
        "x_min": 0x4000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B1 Small Key": {
        "region_id": "totok b1 key",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 1,
        "y": 0x1333,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B1 Shoot Eye Chest": {
        "region_id": "totok b1 bow",
        "vanilla_item": "Courage Gem",
        "stage_id": 37,
        "floor_id": 1,
        "x_min": 0xB000,
        "x_max": 0x10000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B1 Phantom Chest": {
        "region_id": "totok b1 phantom",
        "vanilla_item": "Treasure",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 1,
        "x_max": -50000,
        "x_min": -70000,
        "y": 0,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B2 Bombchu Chest": {
        "region_id": "totok b2 chu",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 37,
        "floor_id": 2,
        "x_min": 0xD800,
        "x_max": 0x10000,
        "require_item": ["Bombchus (Progressive)", "Hammer"],
        "delay_pickup": "TotOK B2 Small Key",
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B2 Phantom Chest": {
        "region_id": "totok b2 phantom",
        "vanilla_item": "Treasure",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 2,
        "z_min": 0x7000,
        "z_max": 0xF000,
        "delay_pickup": "TotOK B2 Small Key",
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B2 Small Key": {
        "region_id": "totok b2 key",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 2,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 Bow Chest": {
        "region_id": "totok b3 bow",
        "vanilla_item": "Power Gem",
        "stage_id": 37,
        "floor_id": 3,
        "y": 0x1333,
        "z_max": -22000,
        "z_min": -40000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 Phantom Chest": {
        "region_id": "totok b3 phantom",
        "vanilla_item": "Treasure",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 3,
        "y": 0x1333,
        "z_min": 0x5000,
        "z_max": 0xD000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 NW Chest": {
        "region_id": "totok b3 nw",
        "vanilla_item": "Force Gem (B3)",
        "stage_id": 37,
        "floor_id": 3,
        "x_max": -50000,
        "z_max": -35000,
        "y": 0,
        "delay_pickup": "TotOK B3 Small Key",
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 SW Chest": {
        "region_id": "totok b3 sw",
        "vanilla_item": "Force Gem (B3)",
        "stage_id": 37,
        "floor_id": 3,
        "x_max": -11000,
        "x_min": -38500,
        "z_min": 0x8000,
        "y": 0,
        "delay_pickup": "TotOK B3 Small Key",
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 SE Chest": {
        "region_id": "totok b3 se",
        "vanilla_item": "Force Gem (B3)",
        "stage_id": 37,
        "floor_id": 3,
        "x_min": 0xE000,
        "z_min": 0xB000,
        "y": 0,
        "delay_pickup": "TotOK B3 Small Key",
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 Small Key": {
        "region_id": "totok b3 key",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 3,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 NW Sea Chart Chest": {
        "region_id": "totok b35",
        "vanilla_item": "NW Sea Chart",
        "stage_id": 37,
        "floor_id": 4,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B4 Phantom Eye Chest": {
        "region_id": "totok b4 eyes",
        "vanilla_item": "Power Gem",
        "stage_id": 37,
        "floor_id": 5,
        "x_min": 0xF000,
        "x_max": 0x16000,
        "delay_pickup": "TotOK B4 Small Key",
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B4 Phantom Chest": {
        "region_id": "totok b4 phantom",
        "vanilla_item": "Treasure",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 5,
        "x_max": -60000,
        'dungeon': "Temple of the Ocean King",
        "delay_pickup": "TotOK B4 Small Key",
    },
    "TotOK B4 Small Key": {
        "region_id": "totok b4 key",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 5,
        'dungeon': "Temple of the Ocean King",
        "delay_pickup": "TotOK B4 Small Key",
    },
    "TotOK B5 Alt Path Chest": {
        "region_id": "totok b5 alt chest",
        "vanilla_item": "Treasure Map #23 (Frost NW)",
        "stage_id": 37,
        "floor_id": 6,
        "x_max": -15000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B5 Chest": {
        "region_id": "totok b5 chest",
        "vanilla_item": "Red Potion",
        "stage_id": 37,
        "floor_id": 6,
        "x_min": 0x6000,
        "x_max": 0xC000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B6 Phantom Chest": {
        "region_id": "totok b6 phantom",
        "vanilla_item": "Treasure",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 7,
        "z_min": 0xA000,
        "z_max": 0xF000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B6 Bow Chest": {
        "region_id": "totok b6 bow",
        "vanilla_item": "Treasure Map #11 (Gusts N)",
        "stage_id": 37,
        "floor_id": 7,
        "z_max": -40000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B6 Courage Crest": {
        "region_id": "totok b6 crest",
        "vanilla_item": "Nothing!",
        "item_override": "Courage Crest",
        "stage_id": 37,
        "floor_id": 8,
        "address": 0x1B558C,
        "value": 0x4,
        'dungeon': "Temple of the Ocean King"
    },

    # =============== TotOK Part 2 ===================

    "TotOK B7 North Chest": {
        "region_id": "totok b7 crystal",
        "vanilla_item": "Round Crystal (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 0xA,
        "x_min": -5000,
        "x_max": 15000,
        "z_max": -50000,
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B7 Peg Chest": {
        "region_id": "totok b7 switch",
        "vanilla_item": "Power Gem",
        "stage_id": 37,
        "floor_id": 0xA,
        "x_min": 50000,
        "x_max": 75000,
        "z_max": 11000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B7 Phantom Chest": {
        "region_id": "totok b7 phantom",
        "vanilla_item": "Ship Part",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 0xA,
        "x_max": -60000,
        "z_max": -50000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B8 2 Crystals Chest": {
        "region_id": "totok b8 2c chest",
        "vanilla_item": "Courage Gem",
        "stage_id": 37,
        "floor_id": 0xB,
        "x_max": -10000,
        "z_max": -30000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B8 Phantom Chest": {
        "region_id": "totok b8 phantom",
        "vanilla_item": "Ship Part",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 0xB,
        "x_max": 50000,
        "z_max": 10000,
        "x_min": 25000,
        "z_min": -10000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B9 NW Chest": {
        "region_id": "totok b9 corner chest",
        "vanilla_item": "Triangle Crystal (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 0xC,
        "x_min": -45000,
        "z_max": -30000,
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B9 Wizzrobe Chest": {
        "region_id": "totok b9 ghosts",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 37,
        "floor_id": 0xC,
        "x_min": -30000,
        "z_min": -9000,
        "x_max": -3000,
        "z_max": 20000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B9 Phantom Chest": {
        "region_id": "totok b9 phantom",
        "vanilla_item": "Ship Part",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 0xC,
        "x_max": -60000,
        "z_min": 45000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B9.5 SE Sea Chart Chest": {
        "region_id": "totok b10",
        "vanilla_item": "SE Sea Chart",
        "stage_id": 37,
        "floor_id": 0xD,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B10 Hammer Switch Chest": {
        "region_id": "totok b10 hammer",
        "vanilla_item": "Treasure Map #30 (Ruins S)",
        "stage_id": 37,
        "floor_id": 0xE,
        "x_min": 15000,
        "z_min": -15000,
        "x_max": 40000,
        "z_max": 10000,
        "y": 0,
        "delay_pickup": "TotOK B10 Small Key",
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B10 Phantom Chest": {
        "region_id": "totok b10 phantom",
        "vanilla_item": "Big Green Rupee (100)",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 0xE,
        "x_min": -40000,
        "z_min": -10000,
        "x_max": -20000,
        "z_max": 10000,
        "y": 0,
        "delay_pickup": "TotOK B10 Small Key",
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B10 Phantom Eye Chest": {
        "region_id": "totok b10 eye",
        "vanilla_item": "Red Potion",
        "stage_id": 37,
        "floor_id": 0xE,
        "y": 0x1333,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B10 Small Key": {
        "region_id": "totok b10 key",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 0xE,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B11 Phantom Eye Chest": {
        "region_id": "totok b11 eyes",
        "vanilla_item": "Treasure",
        "stage_id": 37,
        "floor_id": 0x0F,
        "x_min": 50000,
        "z_max": -45000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B11 Phantom Chest": {
        "region_id": "totok b11 phantom",
        "vanilla_item": "Big Red Rupee (200)",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 0x0F,
        "x_max": -50000,
        "z_min": 40000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 NW Chest": {
        "region_id": "totok b12 nw",
        "vanilla_item": "Force Gem (B12)",
        "stage_id": 37,
        "floor_id": 0x10,
        "x_min": 35000,
        "z_max": -50000,
        "force_vanilla": True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 NE Chest": {
        "region_id": "totok b12 ne",
        "vanilla_item": "Force Gem (B12)",
        "stage_id": 37,
        "floor_id": 0x10,
        "x_max": -35000,
        "z_max": -50000,
        "force_vanilla": True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 Hammer Chest": {
        "region_id": "totok b12 hammer",
        "vanilla_item": "Treasure Map #31 (Dead S)",
        "stage_id": 37,
        "floor_id": 0x10,
        "x_min": 65000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 Kill Everything Chest": {
        "region_id": "totok b12 ghost",
        "vanilla_item": "Ship Part",
        "item_override": "NE Sea Chart",  # Lets the B13 chest be a dungeon reward
        "stage_id": 37,
        "floor_id": 0x10,
        "x_max": -65000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 Phantom Chest": {
        "region_id": "totok b12 phantom",
        "vanilla_item": "Gold Rupee (300)",
        "farmable": True,
        "stage_id": 37,
        "floor_id": 0x10,
        "x_min": -10000,
        "z_min": 0,
        "x_max": 10000,
        "z_max": 25000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B13 NE Sea Chart Chest": {
        "region_id": "totok b13 chest",
        "vanilla_item": "NE Sea Chart",
        "item_override": "Rare Metal",
        "stage_id": 37,
        "floor_id": 0x11,
        "y": 0,
        'dungeon': "Temple of the Ocean King"
    },

    # SW Ocean
    "Ocean SW Salvage Courage Crest": {
        "region_id": "sw ocean crest salvage",
        "vanilla_item": "Sun Key",
        "stage_id": 0,
        "floor_id": 0,
        "address": 0x1B557E,
        "value": 0x40
    },
    "Ocean SW Golden Frog X": {
        "region_id": "sw ocean frog x",
        "vanilla_item": "Golden Frog Glyph X",
        "stage_id": 0,
        "floor_id": 0,
        "x_min": 125000,
        "conditional": True
    },
    "Ocean SW Golden Frog Phi": {
        "region_id": "sw ocean frog phi",
        "vanilla_item": "Golden Frog Glyph Phi",
        "stage_id": 0,
        "floor_id": 0,
        "x_max": -120000,
        "conditional": True
    },
    "Ocean SW Nyave Treasure": {
        "region_id": "sw ocean nyave",
        "vanilla_item": "Treasure",
        "stage_id": 0xA,
        "floor_id": 0,
        "address": 0x1B5592,
        "value": 0x1,
        "delay_reset": True
    },

    # Cannon Island
    "Cannon Island Bee Chest": {
        "region_id": "cannon island",
        "vanilla_item": "Treasure Map #1 (Molida SW)",
        "stage_id": 0x13,
        "floor_id": 0,
        "x_max": -30000,
        "z_max": -15000,
        "x_min": -50000,
        "y": 0x1333,
    },
    "Cannon Island Bee Dig": {
        "region_id": "cannon island dig",
        "vanilla_item": "Big Red Rupee (200)",
        "stage_id": 0x13,
        "floor_id": 0,
        "x_max": -50000,
        "y": 0x1333,
        "conditional": True
    },
    "Cannon Island Cave Chest": {
        "region_id": "cannon island",
        "vanilla_item": "Power Gem",
        "stage_id": 0x28,
        "floor_id": 0,
    },
    "Cannon Island Cliff Chest": {
        "region_id": "cannon island",
        "vanilla_item": "Red Rupee (20)",
        "stage_id": 0x13,
        "floor_id": 0,
        "y": 0x2666
    },
    "Cannon Island SE Dig": {
        "region_id": "cannon island dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x13,
        "floor_id": 0,
        "y": 0x1333,
        "x_max": 27000,
        "z_min": 37000,
        "conditional": True
    },
    "Cannon Island Bonk Tree": {
        "region_id": "cannon island",
        "vanilla_item": "Big Red Rupee (200)",
        "stage_id": 0x13,
        "floor_id": 0,
        "y": 0x1333,
        "x_min": 27000,
        "z_min": 12300,
        "z_max": 37000,
        "sram_addr": 0x0006DC,
        "sram_value": 0x1
    },
    "Cannon Island East Dig": {
        "region_id": "cannon island dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x13,
        "floor_id": 0,
        "y": 0x1333,
        "x_min": 0,
        "z_max": 12300,
        "sram_addr": 0x000190,
        "sram_value": 2,
        "conditional": True
    },
    "Cannon Island Cannon": {
        "region_id": "cannon island",
        "vanilla_item": "Nothing!",
        "item_override": "Cannon",  # Overriden so that you can buy the cannon and sa on the same visit
        "stage_id": 0x13,
        "floor_id": 11,
        "address": 0x1BA649,
        "value": 0x2
    },
    "Cannon Island Salvage Arm": {
        "region_id": "cannon island salvage arm",
        "vanilla_item": "Salvage Arm",
        "stage_id": 0x13,
        "floor_id": 11,
        "address": 0x1B558D,
        "value": 0x10,
    },

    # Isle of Ember

    "Isle of Ember Astrid's Basement Dig": {
        "region_id": "ember island dig",
        "vanilla_item": "Treasure Map #3 (Gusts SW)",
        "stage_id": 0xD,
        "floor_id": 20
    },
    "Isle of Ember Grapple Chest": {
        "region_id": "ember island grapple",
        "vanilla_item": "Courage Gem",
        "stage_id": 0xD,
        "floor_id": 0,
        "z_max": -70000,
        "y": 0
    },
    "Isle of Ember Summit Dig": {
        "region_id": "ember island dig",
        "vanilla_item": "Treasure Map #4 (Bannan SE)",
        "stage_id": 0xD,
        "floor_id": 1,
        "y": 0x2666,
    },
    "Isle of Ember Summit Chest": {
        "region_id": "ember island",
        "vanilla_item": "Red Rupee (20)",
        "stage_id": 0xD,
        "floor_id": 0,
        "y": 0x399A,
    },
    "Isle of Ember Astrid after Fire Temple": {
        "region_id": "post tof",
        "item_override": "Power Gem",  # Overidden cause Astrid reads too many flags
        "vanilla_item": "Nothing!",
        "stage_id": 0xD,
        "floor_id": 10,
        "address": 0x1B557F,
        "value": 0x20,
        'post_dungeon': "Temple of Fire"
    },
    # Temple of Fire
    "Temple of Fire 1F Keese Chest": {
        "region_id": "tof 1f keese",
        "vanilla_item": "Small Key (Temple of Fire)",
        "stage_id": 0x1C,
        "floor_id": 0,
        "z_min": 0x9000,
        "z_max": 0xF000,
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire 1F Maze Chest": {
        "region_id": "tof 1f maze",
        "vanilla_item": "Red Rupee (20)",
        "stage_id": 0x1C,
        "floor_id": 0,
        "x_min": 40000,
        "z_max": -40000,
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire 2F Boomerang Chest": {
        "region_id": "tof 2f",
        "vanilla_item": "Boomerang",
        "stage_id": 0x1C,
        "floor_id": 1,
        "z_max": 10000,
        "x_min": 10000,
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire 2F Fire Keese Chest": {
        "region_id": "tof 2f south",
        "vanilla_item": "Red Rupee (20)",
        "item_override": "Spirit of Power (Progressive)",  # Allows ToF to have dungeon reward
        "stage_id": 0x1C,
        "floor_id": 1,
        "z_min": 0x4000,
        "z_max": 0x7000,
        "x_min": -7000,
        "x_max": 0x1000,
        "delay_pickup": "Temple of Fire 2F Rat Key",
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire 2F Rat Key": {
        "region_id": "tof 2f south",
        "vanilla_item": "Small Key (Temple of Fire)",
        "stage_id": 0x1C,
        "floor_id": 1,
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire 3F Key Drop": {
        "region_id": "tof 3f key drop",
        "vanilla_item": "Small Key (Temple of Fire)",
        "stage_id": 0x1C,
        "floor_id": 2,
        "y": 0,
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire 3F Boss Key Chest": {
        "region_id": "tof 3f boss key",
        "vanilla_item": "Boss Key (Temple of Fire)",
        "stage_id": 0x1C,
        "floor_id": 2,
        "y": 0x1333,
        "force_vanilla": True,
        "dungeon": "Temple of Fire",
    },
    "Temple of Fire Blaaz Heart Container": {
        "region_id": "tof blaaz",
        "vanilla_item": "Heart Container",
        "stage_id": 0x2B,
        "floor_id": 0,
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire Blaaz Dungeon Reward": {
        "region_id": "tof blaaz",
        "vanilla_item": "Spirit of Power (Progressive)",
        "item_override": "Rare Metal",
        "stage_id": 0x2B,
        "floor_id": 0,
        "address": 0x1B557F,
        "value": 0x20,
        "dungeon": "Temple of Fire",
        "boss_reward_location": True,
        "delay_reset": True
    },

    # ============ Molida Island ==============

    "Molida Island 2nd House Chest": {
        "region_id": "molida island",
        "vanilla_item": "Treasure",
        "stage_id": 0xC,
        "floor_id": 0xD,
    },

    "Molida Island Romanos Tree Dig": {
        "region_id": "molida dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0xC,
        "floor_id": 0,
        "z_max": 58000,
        "z_min": 25000,
        "x_min": 40000,
        "y": 0,
        "conditional": True
    },
    "Molida Cave Wayfarer Hideaway Chest": {
        "region_id": "molida dig",
        "vanilla_item": "Treasure Map #2 (Mercay NE)",
        "stage_id": 0xC,
        "floor_id": 10,
        "y": 0,
        "x_max": -25000,
    },
    "Molida Cave Grapple Chest": {
        "region_id": "molida grapple",
        "vanilla_item": "Power Gem",
        "stage_id": 0xC,
        "floor_id": 10,
        "y": 0x1333,
        "x_min": 40000
    },
    "Molida Cave Geozard Dig": {
        "region_id": "molida dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0xC,
        "floor_id": 10,
        "y": 0,
        "x_min": 15000,
        "conditional": True
    },
    "Molida Cave Shovel Chest": {
        "region_id": "molida cave back",
        "vanilla_item": "Shovel",
        "stage_id": 0xC,
        "floor_id": 15,
        "z_max": 41000,
        "sram_addr": 0x49C,
        "sram_value": 0x1
    },
    "Molida Cave Shovel Room Dig": {
        "region_id": "molida cave back dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0xC,
        "floor_id": 15,
        "sram_addr": 0x158,
        "sram_value": 0x100,
        "conditional": True
    },
    "Molida Island Cliff Chest": {
        "region_id": "molida cave back",
        "vanilla_item": "Treasure",
        "stage_id": 0xC,
        "floor_id": 1,
        "y": 0x1333,
        "x_max": -18000,
        "z_min": -30000
    },
    "Molida Island Cuccoo Grapple Tree Dig": {
        "region_id": "molida cuccoo dig",
        "vanilla_item": "Treasure Map #20 (Bannan E)",
        "stage_id": 0xC,
        "floor_id": 0,
        "y": 0x1333,
        "x_min": 90000
    },
    "Molida Island Cuccoo Grapple Small Island Dig": {
        "region_id": "molida cuccoo dig",
        "vanilla_item": "Big Red Rupee (200)",
        "stage_id": 0xC,
        "floor_id": 0,
        "z_min": 58000,
        "y": 0,
        "x_min": 40000,
        "conditional": True
    },
    "Molida Island North Dig Chest": {
        "region_id": "molida north",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0xC,
        "floor_id": 10,
        "y": 0x2666,
        "z_max": -65000
    },
    "Molida Island North Grapple Chest": {
        "region_id": "molida north grapple",
        "vanilla_item": "Courage Gem",
        "stage_id": 0xC,
        "floor_id": 1,
        "y": 0x2666,
        "x_max": 0
    },
    "Molida Archery 1700": {
        "region_id": "molida archery",
        "vanilla_item": "Bow (Progressive)",
        "stage_id": 0xC,
        "floor_id": 11,
        "address": 0x1B55A2,
        "value": 0x8,
        'post_dungeon': "Temple of Courage",
        "delay_reset": True,
        "conditional": True
    },
    "Molida Archery 2000": {
        "region_id": "molida archery",
        "vanilla_item": "Heart Container",
        "stage_id": 0xC,
        "floor_id": 1,
        "address": 0x1B55A6,
        "value": 0x10,
        'post_dungeon': "Temple of Courage",
        "delay_reset": True,
        "conditional": True
    },

    # ============= Temple of Courage ===========

    "Temple of Courage 1F Bomb Alcove Chest": {
        "region_id": "toc bomb alcove",
        "vanilla_item": "Treasure",
        "stage_id": 0x1E,
        "floor_id": 0,
        "z_max": -55000,
        "x_max": 35000,
        "x_min": 20000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 1F Raised Platform Chest": {
        "region_id": "toc",
        "vanilla_item": "Small Key (Temple of Courage)",
        "stage_id": 0x1E,
        "floor_id": 0,
        "y": 0x1333,
        "x_min": 15000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 1F Map Room Chest East": {
        "region_id": "toc map room",
        "vanilla_item": "Power Gem",
        "stage_id": 0x1E,
        "floor_id": 0,
        "z_max": -50000,
        "x_min": -73000,
        "x_max": -55000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 1F Map Room Chest West": {
        "region_id": "toc map room",
        "vanilla_item": "Ship Part",
        "stage_id": 0x1E,
        "floor_id": 0,
        "z_max": -50000,
        "x_max": -73000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 1F Pols Voice Key": {
        "region_id": "toc 1f west",
        "vanilla_item": "Small Key (Temple of Courage)",
        "stage_id": 0x1E,
        "floor_id": 0,
        "y": 0x1333,
        "x_max": 0,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 2F Beamos Maze Chest": {
        "region_id": "toc 2f beamos",
        "vanilla_item": "Square Crystal (Temple of Courage)",
        "stage_id": 0x1E,
        "floor_id": 2,
        "z_max": -30000,
        "x_max": -50000,
        "force_vanilla": True,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage B1 Maze Chest": {
        "region_id": "toc b1 maze",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x1E,
        "floor_id": 1,
        "x_min": -30000,
        "x_max": 0,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage B1 Bow Chest": {
        "region_id": "toc b1 maze",
        "vanilla_item": "Bow (Progressive)",
        "stage_id": 0x1E,
        "floor_id": 1,
        "x_max": -80000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 2F Moving Platform Chest": {
        "region_id": "toc 2f platforms",
        "vanilla_item": "Power Gem",
        "stage_id": 0x1E,
        "floor_id": 2,
        "x_max": -5000,
        "x_min": -20000,
        "z_max": 50000,
        "z_min": 30000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 2F Spike Corridor Chest": {
        "region_id": "toc 2f spike corridor",
        "vanilla_item": "Treasure",
        "item_override": "Spirit of Courage (Progressive)",  # Overidden for dung reward
        "stage_id": 0x1E,
        "floor_id": 2,
        "x_min": 85000,
        "z_min": 30000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage B1 Torch Room Secret Chest": {
        "region_id": "toc torches chest",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0x1E,
        "floor_id": 1,
        "x_min": 70000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 1F Pols Voice Key 2": {
        "region_id": "toc pols 2",
        "vanilla_item": "Small Key (Temple of Courage)",
        "stage_id": 0x1E,
        "floor_id": 0,
        "x_min": 70000,
        "z_max": -30000,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 2F Boss Key Chest": {
        "region_id": "toc bk chest",
        "vanilla_item": "Boss Key (Temple of Courage)",
        "stage_id": 0x1E,
        "floor_id": 2,
        "x_min": 70000,
        "z_max": -30000,
        "force_vanilla": True,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage 3F Before Boss Chest": {
        "region_id": "toc before boss chest",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x1E,
        "floor_id": 3,
        "dungeon": "Temple of Courage"
    },
    "Temple of Courage Crayk Dungeon Reward": {
        "region_id": "toc crayk",
        "vanilla_item": "Spirit of Courage (White)",
        "item_override": "Rare Metal",
        "stage_id": 0x2C,
        "floor_id": 0,
        "address": 0x1B557F,
        "value": 0x80,
        "dungeon": "Temple of Courage",
        "boss_reward_location": True,
        "delay_reset": True
    },
    "Temple of Courage Crayk Sand of Hours": {
        "region_id": "toc crayk",
        "vanilla_item": "Sand of Hours (Boss)",
        "stage_id": 0x2C,
        "floor_id": 0,
        "address": 0x1B557F,
        "value": 0x80,
        "dungeon": "Temple of Courage",
        "delay_reset": True
    },
    "Temple of Courage Heart Container": {
        "region_id": "toc crayk",
        "vanilla_item": "Heart Container",
        "stage_id": 0x2C,
        "floor_id": 0,
        "dungeon": "Temple of Courage"
    },

    # ========== Spirit Island =============

    "Spirit Island Outside Chest": {
        "region_id": "spirit island",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x17,
        "floor_id": 0,
        "y": 0,
        "x_min": -8000
    },
    "Spirit Island Gauntlet Chest": {
        "region_id": "spirit island gauntlet",
        "vanilla_item": "Power Gem",
        "stage_id": 0x17,
        "floor_id": 0,
        "y": 0x2666,
    },
    "Spirit Island Power Upgrade Level 1": {
        "region_id": "spirit power 1",
        "vanilla_item": "Spirit of Power (Progressive)",
        "stage_id": 0x17,
        "floor_id": 1,
        "address": 0x1BA647,
        "value": 0x01
    },
    "Spirit Island Power Upgrade Level 2": {
        "region_id": "spirit power 2",
        "vanilla_item": "Spirit of Power (Progressive)",
        "stage_id": 0x17,
        "floor_id": 1,
        "address": 0x1BA647,
        "value": 0x08
    },
    "Spirit Island Wisdom Upgrade Level 1": {
        "region_id": "spirit wisdom 1",
        "vanilla_item": "Spirit of Wisdom (Progressive)",
        "stage_id": 0x17,
        "floor_id": 1,
        "address": 0x1BA647,
        "value": 0x02
    },
    "Spirit Island Wisdom Upgrade Level 2": {
        "region_id": "spirit wisdom 2",
        "vanilla_item": "Spirit of Wisdom (Progressive)",
        "stage_id": 0x17,
        "floor_id": 1,
        "address": 0x1BA647,
        "value": 0x10
    },
    "Spirit Island Courage Upgrade Level 1": {
        "region_id": "spirit courage 1",
        "vanilla_item": "Spirit of Courage (Progressive)",
        "stage_id": 0x17,
        "floor_id": 1,
        "address": 0x1BA646,
        "value": 0x80
    },
    "Spirit Island Courage Upgrade Level 2": {
        "region_id": "spirit courage 2",
        "vanilla_item": "Spirit of Courage (Progressive)",
        "stage_id": 0x17,
        "floor_id": 1,
        "address": 0x1BA647,
        "value": 0x04
    },
    # ======= NW Ocean ============

    "Ocean NW Golden Frog N": {
        "region_id": "nw ocean frog n",
        "vanilla_item": "Golden Frog Glyph N",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True
    },
    "Ocean NW Prince of Red Lion Combat Reward": {
        "region_id": "porl item",
        "vanilla_item": "Heart Container",
        "stage_id": 7,
        "floor_id": 0,
        "address": 0x1B55A4,
        "value": 0x40,
        "delay_reset": True,
        "conditional": True
    },
    # ============ Isle of Gust ============
    "Isle of Gust Hideout Chest": {
        "region_id": "gust",
        "vanilla_item": "Courage Gem",
        "stage_id": 0xE,
        "floor_id": 0xA,
    },
    "Isle of Gust Miblin Cave North Chest": {
        "region_id": "gust combat",
        "vanilla_item": "Treasure Map #7 (Gusts E)",
        "stage_id": 0xE,
        "floor_id": 0xB,
        "z_max": -22000
    },
    "Isle of Gust Miblin Cave South Chest": {
        "region_id": "gust",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0xE,
        "floor_id": 0xB,
        "z_min": -22000
    },
    "Isle of Gust East Cliff Dig": {
        "region_id": "gust dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0xE,
        "floor_id": 0x0,
        "y": 0x4CCD,
        "conditional": True
    },
    "Isle of Gust West Cliff Chest": {
        "region_id": "gust dig",
        "vanilla_item": "Power Gem",
        "stage_id": 0xE,
        "floor_id": 0x0,
        "y": 0x2666
    },
    "Isle of Gust NW Dig": {
        "region_id": "gust dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0xE,
        "floor_id": 0x1,
        "y": 0x2666,
        "x_max": -85000,
        "conditional": True
    },
    "Isle of Gust Sandworm Chest": {
        "region_id": "gust dig",
        "vanilla_item": "Treasure Map #8 (Mercay SE)",
        "stage_id": 0xE,
        "floor_id": 0x1,
        "y": 0x2666,
        "z_min": -30000
    },

    # ============ Temple of Wind ============

    "Temple of Wind B1 SE Corner Chest": {
        "region_id": "tow b1",
        "vanilla_item": "Treasure",
        "item_override": "Spirit of Wisdom (Progressive)",  # Overridden for dung reward
        "stage_id": 0x1D,
        "floor_id": 0x1,
        "x_min": 80000,
        "dungeon": "Temple of Wind",
    },
    "Temple of Wind B1 Ledge Chest": {
        "region_id": "tow b1",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x1D,
        "floor_id": 0x1,
        "y": 0x1333,
        "dungeon": "Temple of Wind",
    },
    "Temple of Wind B2 Chest": {
        "region_id": "tow b2",
        "vanilla_item": "Power Gem",
        "stage_id": 0x1D,
        "floor_id": 0x2,
        "x_max": -65000,
        "dungeon": "Temple of Wind",
    },
    "Temple of Wind B2 Bombable Wall Item": {
        "region_id": "tow b2 bombs",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x1D,
        "floor_id": 0x3,
        "dungeon": "Temple of Wind",
    },
    "Temple of Wind B1 Key Drop": {
        "region_id": "tow b2 dig",
        "vanilla_item": "Small Key (Temple of Wind)",
        "stage_id": 0x1D,
        "floor_id": 0x1,
        "y": 0x0,
        "dungeon": "Temple of Wind",
    },
    "Temple of Wind B2 Bomb Bag Chest": {
        "region_id": "tow b2 key",
        "vanilla_item": "Bombs (Progressive)",
        "stage_id": 0x1D,
        "floor_id": 0x2,
        "y": 0x1333,
        "dungeon": "Temple of Wind",
    },
    "Temple of Wind 1F Boss Key Chest": {
        "region_id": "tow bk chest",
        "vanilla_item": "Boss Key (Temple of Wind)",
        "stage_id": 0x1D,
        "floor_id": 0x0,
        "y": 0x1333,
        "force_vanilla": True,
        "dungeon": "Temple of Wind",
    },
    "Temple of Wind Cyclok Sand of Hours": {
        "region_id": "tow cyclok",
        "vanilla_item": "Sand of Hours (Boss)",
        "stage_id": 0x2A,
        "floor_id": 0x0,
        "address": 0x1B557F,
        "value": 0x40,
        "dungeon": "Temple of Wind",
        "delay_reset": True
    },
    "Temple of Wind Cyclok Dungeon Reward": {
        "region_id": "tow cyclok",
        "vanilla_item": "Spirit of Wisdom (Progressive)",
        "item_override": "Rare Metal",
        "stage_id": 0x2A,
        "floor_id": 0x0,
        "address": 0x1B557F,
        "value": 0x40,
        "boss_reward_location": True,
        "dungeon": "Temple of Wind",
        "delay_reset": True
    },
    "Temple of Wind Cyclok Heart Container": {
        "region_id": "tow cyclok",
        "vanilla_item": "Heart Container",
        "stage_id": 0x2A,
        "floor_id": 0x0,
        "dungeon": "Temple of Wind",
    },

    # ============ Bannan Island ============

    "Bannan Island Entrance Grapple Chest": {
        "region_id": "bannan grapple",
        "vanilla_item": "Power Gem",
        "stage_id": 0x14,
        "floor_id": 0,
        "z_min": 20000
    },
    "Bannan Island Wayfarers Dig": {
        "region_id": "bannan dig",
        "vanilla_item": "Treasure Map #21 (Molida NW)",
        "stage_id": 0x14,
        "floor_id": 0,
        "z_max": -30000,
        "x_max": 10000
    },
    "Bannan Island Wayfarer Gift": {
        "region_id": "bannan",
        "vanilla_item": "Fishing Rod",
        "item_override": "Nothing!",
        "stage_id": 0x14,
        "floor_id": 1,
        "address": 0x1B5581,
        "value": 8,
        "delay_reset": True
    },
    "Bannan Island Wayfarer Give Loovar": {
        "region_id": "bannan loovar",
        "vanilla_item": "Big Catch Lure",
        "stage_id": 0x14,
        "floor_id": 1,
        "address": 0x1B55A4,
        "value": 1,
        "delay_reset": True,
        "conditional": True,
    },
    "Bannan Island Wayfarer Give Rusty Swordfish": {
        "region_id": "bannan rsf",
        "vanilla_item": "Ship Part",
        "item_override": "Swordfish Shadows",
        "stage_id": 0x14,
        "floor_id": 1,
        "address": 0x1B55A3,
        "value": 0x80,
        "delay_reset": True,
        "conditional": True,
    },
    "Bannan Island Wayfarer Give Legendary Neptoona": {
        "region_id": "bannan neptoona",
        "vanilla_item": "Heart Container",
        "stage_id": 0x14,
        "floor_id": 1,
        "address": 0x1B55A3,
        "value": 0x40,
        "delay_reset": True,
        "conditional": True,
    },
    "Bannan Island Wayfarer Give Stowfish": {
        "region_id": "bannan stowfish",
        "vanilla_item": "Ship Part",
        "item_override": "Fishing Rod",
        "stage_id": 0x14,
        "floor_id": 1,
        "address": 0x1B55A9,
        "value": 0x4,
        "delay_reset": True,
        "conditional": True,
    },
    "Bannan Island East Grapple Chest East": {
        "region_id": "bannan east grapple",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x14,
        "floor_id": 0,
        "x_min": 60000,
        "z_max": -25000,
        "sram_addr": 0x198,
        "sram_value": 4,
        "delay_pickup": ["Bannan Island East Grapple Dig", "Bannan Island East Grapple Chest West"]
    },
    "Bannan Island East Grapple Chest West": {
        "region_id": "bannan east grapple",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x14,
        "floor_id": 0,
        "x_min": 60000,
        "x_max": 100000,
        "z_max": -25000,
        "sram_addr": 0x198,
        "sram_value": 2,
        "delay_pickup": ["Bannan Island East Grapple Dig", "Bannan Island East Grapple Chest East"]
    },
    "Bannan Island East Grapple Dig": {
        "region_id": "bannan east grapple dig",
        "vanilla_item": "Treasure Map #22 (Harrow S)",
        "stage_id": 0x14,
        "floor_id": 0,
        "x_min": 60000,
        "x_max": 100000,
        "z_max": -25000,
        # "sram_addr": 0x22B0,
        # "sram_value": 8
    },
    "Bannan Island Cannon Game": {
        "region_id": "bannan cannon game",
        "vanilla_item": "Bombs (Progressive)",
        "stage_id": 0x14,
        "floor_id": 0,
        "address": 0x1B55AA,
        "value": 0x40,
        "delay_reset": True,
        "conditional": True
    },
    "Bannan Island Wayfarer Trade Quest Chest": {
        "region_id": "bannan scroll",
        "vanilla_item": "Swordsman's Scroll",
        "stage_id": 0x14,
        "floor_id": 1,
        "address": 0x1B5592,
        "value": 0x10
    },

    # ========== Uncharted Island =============

    "Uncharted Island Eye Dig": {
        "region_id": "uncharted dig",
        "vanilla_item": "Treasure Map #6 (Bannan W)",
        "stage_id": 0x1A,
        "floor_id": 0,
        "x_min": -75000
    },
    "Uncharted Island Grapple Chest": {
        "region_id": "uncharted grapple",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x1A,
        "floor_id": 0xA,
    },
    "Uncharted Island Cyclone Slate": {
        "region_id": "uncharted cave",
        "vanilla_item": "Cyclone Slate",
        "stage_id": 0x1A,
        "floor_id": 0xB,
        "address": 0x1B55A2,
        "value": 0x40,
    },

    # ============= Zauz's Island =============

    "Zauz's Island Cuccoo Chest": {
        "region_id": "zauz",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0x16,
        "floor_id": 0,
        "y": 0x1333
    },
    "Zauz's Island Secret Dig": {
        "region_id": "zauz dig",
        "vanilla_item": "Treasure Map #5 (Molida N)",
        "stage_id": 0x16,
        "floor_id": 0,
        "y": 0x0
    },
    "Zauz's Island Triforce Crest": {
        "region_id": "zauz crest",
        "vanilla_item": "Nothing!",
        "item_override": "Triforce Crest",
        "stage_id": 0x16,
        "floor_id": 0xA,
        "address": 0x1B55AB,
        "conditional": True,
        "value": 0x10,
        "post_dungeon": "Ghost Ship"
    },
    "Zauz's Island Phantom Blade": {
        "region_id": "zauz blade",
        "vanilla_item": "Phantom Blade",
        "stage_id": 0x16,
        "floor_id": 0xA,
        "address": 0x1B5592,
        "value": 0x20,
    },


    # ========= Ghost SHip ==============

    "Ghost Ship B1 Entrance Chest": {
        "region_id": "ghost ship",
        "stage_id": 0x29,
        "floor_id": 0,
        "vanilla_item": "Treasure",
        "x_min": 5000,
        "z_min": 5000,
        "dungeon": "Ghost Ship",
    },
    "Ghost Ship B1 Second Sister Chest": {
        "region_id": "ghost ship barrel",
        "stage_id": 0x29,
        "floor_id": 0,
        "vanilla_item": "Triangle Crystal (Ghost Ship)",
        "x_min": 60000,
        "z_max": -5000,
        "force_vanilla": True,
        "dungeon": "Ghost Ship",
    },
    "Ghost Ship B2 Third Sister Right Chest": {
        "region_id": "ghost ship b2",
        "stage_id": 0x29,
        "floor_id": 1,
        "vanilla_item": "Red Potion",
        "x_min": -50000,
        "x_max": -30000,
        "dungeon": "Ghost Ship",
        "sram_addr": 0xB14,
        "sram_value": 4,
        "delay_pickup": "Ghost Ship B2 Third Sister Left Chest"
    },
    "Ghost Ship B2 Third Sister Left Chest": {
        "region_id": "ghost ship b2",
        "stage_id": 0x29,
        "floor_id": 1,
        "vanilla_item": "Rupoor (-10)",
        "x_max": -30000,
        "dungeon": "Ghost Ship",
        "sram_addr": 0xB14,
        "sram_value": 1
    },
    "Ghost Ship B2 Spike Chest": {
        "region_id": "ghost ship b2",
        "stage_id": 0x29,
        "floor_id": 1,
        "vanilla_item": "Round Crystal (Ghost Ship)",
        "z_min": -8000,
        "force_vanilla": True,
        "dungeon": "Ghost Ship",
    },
    "Ghost Ship B3 Chest": {
        "region_id": "ghost ship b3",
        "stage_id": 0x29,
        "floor_id": 2,
        "vanilla_item": "Red Potion",
        "dungeon": "Ghost Ship",
    },
    "Ghost Ship Cubus Sisters Ghost Key": {
        "region_id": "ghost ship cubus",
        "stage_id": 0x30,
        "floor_id": 0,
        "vanilla_item": "Ghost Key",
        "dungeon": "Ghost Ship",
    },
    "Ghost Ship Cubus Sisters Heart Container": {
        "region_id": "ghost ship cubus",
        "stage_id": 0x30,
        "floor_id": 0,
        "address": 0x1B55AB,
        "value": 8,
        "vanilla_item": "Heart Container",
        "dungeon": "Ghost Ship",
    },
    "Ghost Ship Rescue Tetra": {
        "region_id": "ghost ship tetra",
        "stage_id": 0x4,
        "floor_id": 0,
        "address": 0x1B559B,
        "value": 0x2,
        "vanilla_item": "Nothing!",
        "item_override": "Rare Metal",
        "dungeon": "Ghost Ship",
    },

    # ============= SE Ocean ==============

    "Ocean SE Golden Frog Omega": {
        "region_id": "se ocean frogs",
        "vanilla_item": "Golden Frog Glyph Omega",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "z_min": 250000
    },
    "Ocean SE Golden Frog W": {
        "region_id": "se ocean frogs",
        "vanilla_item": "Golden Frog Glyph W",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "z_max": 250000
    },
    "Ocean Pirate Ambush Item": {
        "region_id": "pirate ambush",
        "vanilla_item": "Courage Gem",
        "stage_id": 4,
        "floor_id": 0,
        "address": 0x1B5595,
        "value": 0x80,
        'post_dungeon': "Ghost Ship"
    },

    # ============= Goron Island ==============

    "Goron Island Yellow Chu Item": {
        "region_id": "goron chus",
        "stage_id": 0x10,
        "floor_id": 0x2,
        "vanilla_item": "Treasure Map #16 (Goron NE)",
        "address": 0x1BA652,
        "value": 0x10
    },
    "Goron Island Grapple Chest": {
        "region_id": "goron grapple",
        "stage_id": 0x10,
        "floor_id": 0x2,
        "vanilla_item": "Courage Gem",
        "z_min": 75000,
        "x_max": -90000
    },
    "Goron Island Goron Quiz": {
        "region_id": "goron quiz",
        "stage_id": 0x10,
        "floor_id": 0xA,
        "vanilla_item": "Wisdom Gem",
        "address": 0x1B558B,
        "value": 0x10
    },
    "Goron Island North Bombchu Switch Chest": {
        "region_id": "goron north bombchu",
        "stage_id": 0x10,
        "floor_id": 0x1,
        "vanilla_item": "Treasure Map #18 (Cannon S)",
        "x_min": 110000,
        "z_max": -110000
    },
    "Goron Island North Dead End Chest": {
        "region_id": "goron north",
        "stage_id": 0x10,
        "floor_id": 0x0,
        "vanilla_item": "Big Green Rupee (100)",
        "x_max": 50000
    },
    "Goron Island North Spike Chest": {
        "region_id": "goron outside temple",
        "stage_id": 0x10,
        "floor_id": 0x1,
        "vanilla_item": "Power Gem",
        "x_max": 0x35000,
    },
    "Goron Island Chief Post Dungeon Item": {
        "region_id": "goron chief 2",
        "stage_id": 0x10,
        "floor_id": 0xA,
        "vanilla_item": "Big Red Rupee (200)",
        "address": 0x1B5593,
        "value": 0x2,
        'post_dungeon': "Goron Temple"
    },

    # ============= Goron Temple ==============

    "Goron Temple 1F Switch Chest": {
        "region_id": "gt",
        "stage_id": 0x20,
        "floor_id": 0x0,
        "vanilla_item": "Treasure Map #17 (Frost S)",
        "y": 0x2666,
        "dungeon": "Goron Temple",
    },
    "Goron Temple 1F Bow Chest": {
        "region_id": "gt bow",
        "stage_id": 0x20,
        "floor_id": 0x0,
        "vanilla_item": "Red Rupee (20)",
        "y": 0x1333,
        "dungeon": "Goron Temple",
    },
    "Goron Temple B1 Bombchu Bag Chest": {
        "region_id": "gt b1",
        "stage_id": 0x20,
        "floor_id": 0x1,
        "vanilla_item": "Bombchus (Progressive)",
        "y": 0x1333,
        "dungeon": "Goron Temple",
    },
    "Goron Temple B1 Kill Eyeslugs Chest": {
        "region_id": "gt b1",
        "stage_id": 0x20,
        "floor_id": 0x1,
        "vanilla_item": "Treasure",
        "y": 0,
        "z_min": 30000,
        "dungeon": "Goron Temple",
    },
    "Goron Temple B3 Kill Miblins Chest": {
        "region_id": "gt b3",
        "stage_id": 0x20,
        "floor_id": 0x3,
        "vanilla_item": "Red Rupee (20)",
        "x_max": -20000,
        "dungeon": "Goron Temple",
    },
    "Goron Temple B2 Kill Eyeslugs Chest": {
        "region_id": "gt bk chest",
        "stage_id": 0x20,
        "floor_id": 0x2,
        "vanilla_item": "Treasure",
        "y": 0,
        "dungeon": "Goron Temple",
    },
    "Goron Temple B2 Boss Key Chest": {
        "region_id": "gt bk chest",
        "stage_id": 0x20,
        "floor_id": 0x2,
        "vanilla_item": "Boss Key (Goron Temple)",
        "y": 0x1333,
        "force_vanilla": True,
        "dungeon": "Goron Temple",
    },
    "Goron Temple Dongorongo Sand of Hours": {
        "region_id": "gt dongo",
        "stage_id": 0x2E,
        "floor_id": 0x0,
        "vanilla_item": "Sand of Hours (Boss)",
        "address": 0x1B559B,
        "value": 0x4,
        "dungeon": "Goron Temple",
        "delay_reset": True
    },
    "Goron Temple Dongorongo Heart Container": {
        "region_id": "gt dongo",
        "stage_id": 0x2E,
        "floor_id": 0x0,
        "vanilla_item": "Heart Container",
        "dungeon": "Goron Temple",
    },
    "Goron Temple Dongorongo Dungeon Reward": {
        "region_id": "gt dongo",
        "stage_id": 0x20,
        "floor_id": 0x0A,
        "vanilla_item": "Crimzonine",
        "item_override": "Rare Metal",
        "boss_reward_location": True,
        "dungeon": "Goron Temple",
    },

    # ============= Harrow Island ==============
    "Harrow Island Dig 1": {
        "region_id": "harrow dig",
        "stage_id": 0x18,
        "floor_id": 0x0,
        "item_override": "Treasure Map #14 (Goron NW)",  # Allows you to keep digging
        "vanilla_item": "Nothing!",
        "address": 0x1BA652,
        "value": 0x1,
        "conditional": True
    },
    "Harrow Island Dig 2": {
        "region_id": "harrow dig",
        "stage_id": 0x18,
        "floor_id": 0x0,
        "item_override": "Treasure Map #15 (Goron W)",
        "vanilla_item": "Nothing!",
        "address": 0x1BA652,
        "value": 0x2,
        "conditional": True
    },
    "Harrow Island Dig 3": {
        "region_id": "harrow dig 2",
        "stage_id": 0x18,
        "floor_id": 0x0,
        "item_override": "Treasure Map #24 (Ruins W)",
        "vanilla_item": "Nothing!",
        "address": 0x1BA653,
        "value": 2,
        "conditional": True
    },
    "Harrow Island Dig 4": {
        "region_id": "harrow dig 2",
        "stage_id": 0x18,
        "floor_id": 0x0,
        "item_override": "Treasure Map #25 (Dead E)",
        "vanilla_item": "Nothing!",
        "address": 0x1BA653,
        "value": 4,
        "conditional": True
    },


    # ============= Dee Ess Island ==============

    "Dee Ess Menu Button Dig": {
        "region_id": "ds dig",
        "stage_id": 0x1B,
        "floor_id": 0x0,
        "vanilla_item": "Courage Gem",
        "y": 0,
        "x_max": -25000,
        "z_min": 45000
    },
    "Dee Ess Blow in Microphone Chest": {
        "region_id": "ds",
        "stage_id": 0x1B,
        "floor_id": 0x0,
        "vanilla_item": "Gold Rupee (300)",
        "y": 0,
        "x_max": -15000,
        "z_min": 10000,
        "z_max": 30000,
    },
    "Dee Ess Left Speakers Dig SSW": {
        "region_id": "ds dig",
        "stage_id": 0x1B,
        "floor_id": 0x0,
        "vanilla_item": "Big Green Rupee (100)",
        "y": 0x2666,
        "x_min": -67500,
        "x_max": -50000,
        "conditional": True
    },
    "Dee Ess Right Speakers Dig SE": {
        "region_id": "ds dig",
        "stage_id": 0x1B,
        "floor_id": 0x0,
        "vanilla_item": "Big Green Rupee (100)",
        "y": 0x2666,
        "x_min": 45000,
        "conditional": True
    },
    "Dee Ess Left Speakers Dig West ": {
        "region_id": "ds dig",
        "stage_id": 0x1B,
        "floor_id": 0x0,
        "vanilla_item": "Big Green Rupee (100)",
        "y": 0x2666,
        "x_max": -67500,
        "conditional": True
    },
    "Dee Ess Win Goron Game": {
        "region_id": "ds race",
        "stage_id": 0x1B,
        "floor_id": 0x0,
        "vanilla_item": "Bombchus (Progressive)",
        "address": 0x1B559F,
        "value": 0x20,
        'post_dungeon': "Goron Temple",
        'delay_reset': True,
        "conditional": True
    },
    "Dee Ess Eye Brute Chest": {
        "region_id": "ds combat",
        "stage_id": 0x1B,
        "floor_id": 0x0,
        "vanilla_item": "Courage Gem",
        "y": 0,
        "z_max": -20000
    },

    # ============= Isle of Frost ==============

    "Isle of Frost Nobodo Grapple Chest": {
        "region_id": "iof grapple",
        "stage_id": 0xF,
        "floor_id": 0x0,
        "vanilla_item": "Wisdom Gem",
        "y": 0x1333
    },
    "Isle of Frost Chief House Dig": {
        "region_id": "iof dig",
        "stage_id": 0xF,
        "floor_id": 0x0,
        "vanilla_item": "Big Green Rupee (100)",
        "y": 0x2666
    },
    "Isle of Frost Estate Sign Dig": {
        "region_id": "iof dig",
        "stage_id": 0xF,
        "floor_id": 0x2,
        "vanilla_item": "Big Red Rupee (200)",
        "z_min": -20000,
        "conditional": True
    },
    "Isle of Frost Fofo Dig (SE)": {
        "region_id": "iof dig",
        "stage_id": 0xF,
        "floor_id": 0x2,
        "vanilla_item": "Big Green Rupee (100)",
        "z_min": -60000,
        "z_max": -30000,
        "x_min": -115000,
        "x_max": -85000,
        "conditional": True
    },
    "Isle of Frost Dobo Dig (SW)": {
        "region_id": "iof dig",
        "stage_id": 0xF,
        "floor_id": 0x2,
        "vanilla_item": "Big Green Rupee (100)",
        "z_min": -60000,
        "z_max": -30000,
        "x_min": -175000,
        "x_max": -145000,
        "conditional": True
    },
    "Isle of Frost Estate SW Island Dig": {
        "region_id": "iof dig",
        "stage_id": 0xF,
        "floor_id": 0x2,
        "vanilla_item": "Treasure Map #19 (Gusts NE)",
        "x_max": -185000
    },
    "Isle of Frost Estate SE Island Dig": {
        "region_id": "iof grapple dig",
        "stage_id": 0xF,
        "floor_id": 0x2,
        "vanilla_item": "Gold Rupee (300)",
        "x_min": -60000,
        "conditional": True
    },
    "Isle of Frost Ice Field South Ledge West Chest": {
        "region_id": "iof grapple",
        "stage_id": 0xF,
        "floor_id": 0x3,
        "vanilla_item": "Big Red Rupee (200)",
        "x_max": 150000,
        "y": 0x399A,
        "sram_addr": 0x544,
        "sram_value": 2,

    },
    "Isle of Frost Ice Field South Ledge East Chest": {
        "region_id": "iof grapple",
        "stage_id": 0xF,
        "floor_id": 0x3,
        "vanilla_item": "Red Rupee (20)",
        "x_min": 150000,
        "y": 0x399A,
        "sram_addr": 0x544,
        "sram_value": 4,
    },
    "Isle of Frost Ice Field SE Ledge Chest": {
        "region_id": "iof grapple",
        "stage_id": 0xF,
        "floor_id": 0x3,
        "vanilla_item": "Big Green Rupee (100)",
        "y": 0x4CCD
    },
    "Isle of Frost Ice Field East Ledge Chest": {
        "region_id": "iof grapple",
        "stage_id": 0xF,
        "floor_id": 0x3,
        "vanilla_item": "Power Gem",
        "y": 0x2666
    },

    # ============= Ice Temple ==============

    "Temple of Ice 3F Corner Chest": {
        "region_id": "toi 3f",
        "stage_id": 0x1F,
        "floor_id": 0x1,
        "vanilla_item": "Red Potion",
        "z_max": -30000,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice 3F Switch State Chest": {
        "region_id": "toi 3f switch",
        "stage_id": 0x1F,
        "floor_id": 0x1,
        "vanilla_item": "Wisdom Gem",
        "y": 0x1333,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice 3F Key Drop": {
        "region_id": "toi 3f boomerang",
        "stage_id": 0x1F,
        "floor_id": 0x1,
        "vanilla_item": "Small Key (Temple of Ice)",
        "y": 0x2666,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice 2F Grappling Hook Chest": {
        "region_id": "toi 2f miniboss",
        "stage_id": 0x1F,
        "floor_id": 0x3,
        "vanilla_item": "Grappling Hook",
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice B1 Entrance Chest": {
        "region_id": "toi b1",
        "stage_id": 0x1F,
        "floor_id": 0x2,
        "x_max": -30000,
        "vanilla_item": "Yellow Potion",
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice B1 SE Chest": {
        "region_id": "toi b1 2",
        "stage_id": 0x1F,
        "floor_id": 0x2,
        "vanilla_item": "Small Key (Temple of Ice)",
        "x_min": 70000,
        "z_min": 45000,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice B1 Locked Room Chest": {
        "region_id": "toi b1 key",
        "stage_id": 0x1F,
        "floor_id": 0x2,
        "vanilla_item": "Wisdom Gem",
        "z_max": -20000,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice B2 Bow Bounce Chest": {
        "region_id": "toi b2",
        "stage_id": 0x1F,
        "floor_id": 0x5,
        "vanilla_item": "Small Key (Temple of Ice)",
        "z_max": -50000,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice B2 Fight Chest": {
        "region_id": "toi b2 key",
        "stage_id": 0x1F,
        "floor_id": 0x5,
        "vanilla_item": "Purple Potion",
        "x_min": 30000,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice B2 Boss Key Chest": {
        "region_id": "toi bk chest",
        "stage_id": 0x1F,
        "floor_id": 0x5,
        "vanilla_item": "Boss Key (Temple of Ice)",
        "force_vanilla": True,
        "y": 0x1333,
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice Gleeok Sand of Hours": {
        "region_id": "toi gleeok",
        "stage_id": 0x2D,
        "floor_id": 0x0,
        "vanilla_item": "Sand of Hours (Boss)",
        "address": 0x1B559B,
        "value": 0x8,
        "dungeon": "Temple of Ice",
        "delay_reset": True
    },
    "Temple of Ice Gleeok Heart Container": {
        "region_id": "toi gleeok",
        "stage_id": 0x2D,
        "floor_id": 0x0,
        "vanilla_item": "Heart Container",
        "dungeon": "Temple of Ice",
    },
    "Temple of Ice Dungeon Reward": {
        "region_id": "toi gleeok",
        "stage_id": 0x1F,
        "floor_id": 0x6,
        "vanilla_item": "Azurine",
        "item_override": "Rare Metal",
        "boss_reward_location": True,
        "dungeon": "Temple of Ice",
    },

    # ============= NE Ocean ==============
    "Ocean NE Golden Frog Square": {
        "region_id": "ne ocean frog",
        "vanilla_item": "Golden Frog Glyph Square",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
    },

    # ============= Isle of the Dead ==============
    "Isle of the Dead Rupoor Cave 1": {
        "region_id": "iotd rupoor",
        "vanilla_item": "Ship Part",
        "stage_id": 0x15,
        "floor_id": 2,
        "z_max": -55000,
        "x_max": 2000,
        "sram_addr": 0x73C,
        "sram_value": 4,
        "delay_pickup": ["Isle of the Dead Rupoor Cave 3", "Isle of the Dead Rupoor Cave 2"]
    },
    "Isle of the Dead Rupoor Cave 4": {
        "region_id": "iotd rupoor",
        "vanilla_item": "Ship Part",
        "stage_id": 0x15,
        "floor_id": 2,
        "z_max": -55000,
        "x_min": -4000,
        "sram_addr": 0x73C,
        "sram_value": 1,
        "delay_pickup": ["Isle of the Dead Rupoor Cave 3", "Isle of the Dead Rupoor Cave 2"]
    },
    "Isle of the Dead Rupoor Cave 2": {
        "region_id": "iotd rupoor",
        "vanilla_item": "Treasure Map #28 (Ruins NW)",
        "stage_id": 0x15,
        "floor_id": 2,
        "z_max": -55000,
        "x_max": 8000,
        "sram_addr": 0x73C,
        "sram_value": 2,
        "delay_pickup": "Isle of the Dead Rupoor Cave 3"
    },
    "Isle of the Dead Rupoor Cave 3": {
        "region_id": "iotd rupoor",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x15,
        "floor_id": 2,
        "z_max": -55000,
        "x_min": 2000,
        "sram_addr": 0x73C,
        "sram_value": 1,
        "delay_pickup": "Isle of the Dead Rupoor Cave 2"
    },
    "Isle of the Dead Face Cave Chest": {
        "region_id": "iotd cave",
        "vanilla_item": "Power Gem",
        "stage_id": 0x15,
        "floor_id": 4,
    },
    "Isle of the Dead Face Chest": {
        "region_id": "iotd dig",
        "vanilla_item": "Treasure Map #29 (Maze W)",
        "stage_id": 0x15,
        "floor_id": 0,
        "y": 0x4CCD
    },
    "Isle of the Dead Regal Necklace Chest": {
        "region_id": "iotd",
        "vanilla_item": "Regal Necklace",
        "stage_id": 0x15,
        "floor_id": 0,
        "y": 0x2666
    },


    # ============= Isle of Ruins ==============

    "Isle of Ruins Like-Like Dig": {
        "region_id": "ruins dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x11,
        "floor_id": 1,
        "additional_rooms": [0x1201],
        "y": 0x1333,
        "x_max": -200000,
        "z_max": -40000,
        "conditional": True
    },
    "Isle of Ruins Bonk Tree": {
        "region_id": "ruins",
        "vanilla_item": "Big Red Rupee (200)",
        "stage_id": 0x11,
        "floor_id": 1,
        "additional_rooms": [0x1201],
        "y": 0x4CCD,
    },
    "Isle of Ruins Doylan's Item": {
        "region_id": "ruins",
        "vanilla_item": "King's Key",
        "stage_id": 0x22,
        "floor_id": 1,
        "address": 0x1B5585,
        "value": 0x4
    },
    "Isle of Ruins Lower Water Cave Chest": {
        "region_id": "ruins water",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0x12,
        "floor_id": 0xB,
    },
    "Isle of Ruins Maze Chest": {
        "region_id": "ruins water",
        "vanilla_item": "Power Gem",
        "stage_id": 0x12,
        "floor_id": 1,
        "y": 0x0
    },
    "Isle of Ruins Dodge Boulders Chest": {
        "region_id": "ruins water",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x12,
        "floor_id": 2,
        "y": 0x0,
        "additional_rooms": [0x1102],
        "x_min": 55000,
        "x_max": 75000,
        "z_max": -75000
    },
    "Isle of Ruins Push Boulder Chest": {
        "region_id": "ruins water",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0x12,
        "floor_id": 2,
        "additional_rooms": [0x1102],
        "y": 0x0,
        "z_min": -30000
    },
    "Isle of Ruins Outside Doylan's Temple Chest": {
        "region_id": "ruins water",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x12,
        "floor_id": 2,
        "additional_rooms": [0x1102],
        "y": 0x0,
        "x_min": 170000,
        "z_max": -75000
    },
    "Isle of Ruins Outside Mutoh's Temple Chest": {
        "region_id": "ruins water",
        "vanilla_item": "Big Red Rupee (200)",
        "stage_id": 0x11,
        "floor_id": 2,
        "additional_rooms": [0x1202],
        "y": 0x0,
        "x_min": 80000,
        "x_max": 105000,
        "z_max": -150000
    },

    # ============= Mutoh's Temple ==============

    "Mutoh's Temple 2F Like-Like Maze Chest": {
        "region_id": "mutoh",
        "vanilla_item": "Treasure",
        "stage_id": 0x21,
        "floor_id": 1,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple 3F Hammer Chest": {
        "region_id": "mutoh",
        "vanilla_item": "Hammer",
        "stage_id": 0x21,
        "floor_id": 2,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple B2 Spike Roller Chest": {
        "region_id": "mutoh hammer",
        "vanilla_item": "Courage Gem",
        "stage_id": 0x21,
        "floor_id": 4,
        "y": 0,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple B2 Ledge Chest": {
        "region_id": "mutoh hammer",
        "vanilla_item": "Small Key (Mutoh's Temple)",
        "stage_id": 0x21,
        "floor_id": 4,
        "y": 0x1333,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple B1 Lower Water Chest": {
        "region_id": "mutoh water",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x21,
        "floor_id": 3,
        "y": 0x1333,
        "z_min": -25000,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple B1 Push Boulder Chest": {
        "region_id": "mutoh water",
        "vanilla_item": "Small Key (Mutoh's Temple)",
        "stage_id": 0x21,
        "floor_id": 3,
        "y": 0x1333,
        "z_max": -25000,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple B1 Boss Key Chest": {
        "region_id": "mutoh bk chest",
        "vanilla_item": "Boss Key (Mutoh's Temple)",
        "stage_id": 0x21,
        "floor_id": 3,
        "y": 0x4CCD,
        "force_vanilla": True,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple Eox Sand of Hours": {
        "region_id": "mutoh eox",
        "vanilla_item": "Sand of Hours (Boss)",
        "stage_id": 0x2F,
        "floor_id": 0,
        "address": 0x1B559B,
        "value": 0x10,
        "dungeon": "Mutoh's Temple",
        "delay_reset": True
    },
    "Mutoh's Temple Heart Container Chest": {
        "region_id": "mutoh eox",
        "vanilla_item": "Heart Container",
        "stage_id": 0x2F,
        "floor_id": 0,
        "dungeon": "Mutoh's Temple",
    },
    "Mutoh's Temple Dungeon Reward": {
        "region_id": "mutoh eox",
        "vanilla_item": "Aquanine",
        "item_override": "Rare Metal",
        "stage_id": 0x21,
        "floor_id": 6,
        "boss_reward_location": True,
        "dungeon": "Mutoh's Temple",
    },

    # ============= Maze Island ==============

    "Maze Island Maze Chest": {
        "region_id": "maze east",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0x19,
        "floor_id": 0,
        "y": 0,
        "x_min": 40000,
        "z_max": 24000,
        "z_min": -26000
    },
    "Maze Island SE Dig": {
        "region_id": "maze dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x19,
        "floor_id": 0,
        "y": 0,
        "x_min": 80000,
        "z_min": 70000,
        "conditional": True,
        "sram_addr": 0x1c1,
        "sram_value": 0x08
    },
    "Maze Island NE Dig": {
        "region_id": "maze dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x19,
        "floor_id": 0,
        "y": 0,
        "x_min": 40000,
        "z_max": -60000,
        "conditional": True,
        "sram_addr": 0x1c1,
        "sram_value": 0x10
    },
    "Maze Island NW Dig": {
        "region_id": "maze dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x19,
        "floor_id": 0,
        "y": 0,
        "x_max": -15000,
        "z_max": -60000,
        "conditional": True,
        "sram_addr": 0x1c1,
        "sram_value": 0x80
    },
    "Maze Island Beginner": {
        "region_id": "maze",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 0x19,
        "floor_id": 0,
        "address": 0x1B558E,
        "value": 1,
        "conditional": True
    },
    "Maze Island Normal": {
        "region_id": "maze normal",
        "vanilla_item": "Treasure Map #27 (Maze E)",
        "stage_id": 0x19,
        "floor_id": 0,
        "address": 0x1B5598,
        "value": 0x40,
        "conditional": True
    },
    "Maze Island Expert": {
        "region_id": "maze expert",
        "vanilla_item": "Heart Container",
        "stage_id": 0x19,
        "floor_id": 0,
        "address": 0x1B5598,
        "value": 0x80,
        "conditional": True
    },
    "Maze Island Bonus Reward": {
        "region_id": "maze expert",
        "vanilla_item": "Gold Rupee (300)",
        "stage_id": 0x19,
        "floor_id": 0,
        "x_max": -50000,
        "z_min": 50000,
        "conditional": True
    },

    # Goals

    "GOAL: Beat Bellumbeck": {
        "region_id": "goal",
        "vanilla_item": "Nothing!",
        "stage_id": 0x36,
        "floor_id": 0,
        "conditional": True
    },
    "GOAL: Triforce Door": {
        "region_id": "goal",
        "vanilla_item": "Nothing!",
        "stage_id": 0x25,
        "floor_id": 9,
        "conditional": True
    },

    # Trade Quest

    "Ocean NE Man Of Smiles Item 1": {
        "region_id": "ne ocean combat",
        "vanilla_item": "Hero's New Clothes",
        "stage_id": 0x6,
        "floor_id": 0,
        "address": 0x1B558F,
        "value": 0x20
    },
    "Ocean NE Man Of Smiles Item 2": {
        "region_id": "ne ocean combat",
        "vanilla_item": "Treasure Map #26 (Ruins SW)",
        "stage_id": 0x6,
        "floor_id": 0,
        "address": 0x1B558F,
        "value": 0x20
    },
    "Ocean NW Prince of Red Lions Trade Quest Item": {
        "region_id": "porl trade",
        "vanilla_item": "Kaleidoscope",
        "stage_id": 0x7,
        "floor_id": 0,
        "address": 0x1B5590,
        "value": 0x8
    },
    "Ocean SW Nyave Trade Quest Item": {
        "region_id": "sw ocean nyave trade",
        "vanilla_item": "Wood Heart",
        "stage_id": 0xA,
        "floor_id": 0,
        "address": 0x1B5590,
        "value": 0x80
    },
    "Ocean SE Hoiger Howgendoogen Trade Quest Item": {
        "region_id": "se ocean trade",
        "vanilla_item": "Guard Notebook",
        "stage_id": 0x9,
        "floor_id": 0,
        "address": 0x1B5590,
        "value": 0x10
    },

    # ==== Fishing ===
    "Fishing Catch Skippyjack": {
        "region_id": "fishing",
        "vanilla_item": "Fish: Skippyjack",
        "stage_id": 0x2,
        "floor_id": 0,
        "address": 0x1BA5B4,
        "value": 1,
        "conditional": True,
    },
    "Fishing Catch Toona": {
        "region_id": "fishing",
        "vanilla_item": "Fish: Toona",
        "stage_id": 0x2,
        "floor_id": 0,
        "address": 0x1BA5B5,
        "value": 1,
        "conditional": True,
    },
    "Fishing Catch Loovar": {
        "region_id": "fishing",
        "vanilla_item": "Fish: Loovar",
        "stage_id": 0x2,
        "floor_id": 0,
        "address": 0x1BA5B6,
        "value": 1,
        "conditional": True,
    },
    "Fishing Catch Rusty Swordfish": {
        "region_id": "fishing rsf",
        "vanilla_item": "Fish: Rusty Swordfish",
        "stage_id": 0x2,
        "floor_id": 0,
        "address": 0x1BA5B7,
        "value": 1,
        "conditional": True,
    },
    "Fishing Catch Legendary Neptoona": {
        "region_id": "fishing shadows",
        "vanilla_item": "Fish: Legendary Neptoona",
        "stage_id": 0x2,
        "floor_id": 0,
        "address": 0x1BA5B8,
        "value": 0x1,
        "conditional": True,
    },
    "Fishing Catch Stowfish": {
        "region_id": "fishing stowfish",
        "vanilla_item": "Fish: Stowfish",
        "stage_id": 0x2,
        "floor_id": 0,
        "address": 0x1BA5B9,
        "value": 0x1,
        "conditional": True,
    },

    # Salvage
    "Ocean SW Salvage #1 Molida SW": {
        "region_id": "salvage 1",
        "stage_id": 0,
        "floor_id": 0,
        "conditional": True,
        "address": 1812052,
        "value": 128,
        "id": 290,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #1 (Molida SW)",
    },
    "Ocean SW Salvage #2 Mercay NE": {
        "region_id": "salvage 2",
        "stage_id": 0,
        "floor_id": 0,
        "conditional": True,
        "address": 1812052,
        "value": 16,
        "id": 291,
        "vanilla_item": "Sand of Hours (Small)",
        "item_override": "Treasure Map #2 (Mercay NE)",
    },
    "Ocean NW Salvage #3 Gusts SW": {
        "region_id": "salvage 3",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 32,
        "id": 292,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #3 (Gusts SW)",
    },
    "Ocean NW Salvage #4 Bannan SE": {
        "region_id": "salvage 4",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 128,
        "id": 293,
        "vanilla_item": "Sand of Hours (Small)",
        "item_override": "Treasure Map #4 (Bannan SE)",
    },
    "Ocean SW Salvage #5 Molida N": {
        "region_id": "salvage 5",
        "stage_id": 0,
        "floor_id": 0,
        "conditional": True,
        "address": 1812052,
        "value": 64,
        "id": 294,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #5 (Molida N)",
    },
    "Ocean NW Salvage #6 Bannan W": {
        "region_id": "salvage 6",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 1,
        "id": 295,
        "vanilla_item": "Treasure",
        "item_override": "Treasure Map #6 (Bannan W)",
    },
    "Ocean NW Salvage #7 Gusts E": {
        "region_id": "salvage 7",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 8,
        "id": 296,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #7 (Gusts E)",
    },
    "Ocean SW Salvage #8 Mercay SE": {
        "region_id": "salvage 8",
        "stage_id": 0,
        "floor_id": 0,
        "conditional": True,
        "address": 1812052,
        "value": 8,
        "id": 297,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #8 (Mercay SE)",
    },
    "Ocean SW Salvage #9 Cannon W": {
        "region_id": "salvage 9",
        "stage_id": 0,
        "floor_id": 0,
        "conditional": True,
        "address": 1812052,
        "value": 2,
        "id": 298,
        "vanilla_item": "Sand of Hours (Small)",
        "item_override": "Treasure Map #9 (Cannon W)",
    },
    "Ocean NW Salvage #10 Gusts SE": {
        "region_id": "salvage 10",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 16,
        "id": 299,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #10 (Gusts SE)",
    },
    "Ocean NW Salvage #11 Gusts N": {
        "region_id": "salvage 11",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 2,
        "id": 300,
        "vanilla_item": "Sand of Hours (Small)",
        "item_override": "Treasure Map #11 (Gusts N)",
    },
    "Ocean SE Salvage #12 Dee Ess N": {
        "region_id": "salvage 12",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 32,
        "id": 301,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #12 (Dee Ess N)",
    },
    "Ocean SE Salvage #13 Harrow E": {
        "region_id": "salvage 13",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 4,
        "id": 302,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #13 (Harrow E)",
    },
    "Ocean SE Salvage #14 Goron NW": {
        "region_id": "salvage 14",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 1,
        "id": 303,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #14 (Goron NW)",
    },
    "Ocean SE Salvage #15 Goron W": {
        "region_id": "salvage 15",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 2,
        "id": 304,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #15 (Goron W)",
    },
    "Ocean SE Salvage #16 Goron NE": {
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #16 (Goron NE)",
        "region_id": "salvage 16",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 16,
        "id": 305,
    },
    "Ocean SE Salvage #17 Frost S": {
        "region_id": "salvage 17",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 64,
        "id": 306,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #17 (Frost S)",
    },
    "Ocean SW Salvage #18 Cannon S": {
        "region_id": "salvage 18",
        "stage_id": 0,
        "floor_id": 0,
        "conditional": True,
        "address": 1812052,
        "value": 4,
        "id": 307,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #18 (Cannon S)",
    },
    "Ocean NW Salvage #19 Gusts NE": {
        "region_id": "salvage 19",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 4,
        "id": 308,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #19 (Gusts NE)",
    },
    "Ocean NW Salvage #20 Bannan E": {
        "region_id": "salvage 20",
        "stage_id": 0,
        "floor_id": 1,
        "conditional": True,
        "address": 1812053,
        "value": 64,
        "id": 309,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #20 (Bannan E)",
    },
    "Ocean SW Salvage #21 Molida NW": {
        "region_id": "salvage 21",
        "stage_id": 0,
        "floor_id": 0,
        "conditional": True,
        "address": 1812052,
        "value": 32,
        "id": 310,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #21 (Molida NW)",
    },
    "Ocean SE Salvage #22 Harrow S": {
        "region_id": "salvage 22",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 8,
        "id": 311,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #22 (Harrow S)",
    },
    "Ocean SE Salvage #23 Frost NW": {
        "region_id": "salvage 23",
        "stage_id": 0,
        "floor_id": 2,
        "conditional": True,
        "address": 1812054,
        "value": 128,
        "id": 312,
        "vanilla_item": "Sand of Hours (Small)",
        "item_override": "Treasure Map #23 (Frost NW)",
    },
    "Ocean NE Salvage #24 Ruins W": {
        "region_id": "salvage 24",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 2,
        "id": 313,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #24 (Ruins W)",
    },
    "Ocean NE Salvage #25 Dead E": {
        "region_id": "salvage 25",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 4,
        "id": 314,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #25 (Dead E)",
    },
    "Ocean NE Salvage #26 Ruins SW": {
        "region_id": "salvage 26",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 32,
        "id": 315,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #26 (Ruins SW)",
    },
    "Ocean NE Salvage #27 Maze E": {
        "region_id": "salvage 27",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 8,
        "id": 316,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #27 (Maze E)",
    },
    "Ocean NE Salvage #28 Ruins NW": {
        "region_id": "salvage 28",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 1,
        "id": 317,
        "vanilla_item": "Treasure",
        "item_override": "Treasure Map #28 (Ruins NW)",
    },
    "Ocean NE Salvage #29 Maze W": {
        "region_id": "salvage 29",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 16,
        "id": 318,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #29 (Maze W)",
    },
    "Ocean NE Salvage #30 Ruins S": {
        "region_id": "salvage 30",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 64,
        "id": 319,
        "vanilla_item": "Ship Part",
        "item_override": "Treasure Map #30 (Ruins S)",
    },
    "Ocean NE Salvage #31 Dead S": {
        "region_id": "salvage 31",
        "stage_id": 0,
        "floor_id": 3,
        "conditional": True,
        "address": 1812055,
        "value": 128,
        "id": 320,
        "vanilla_item": "Gold Rupee (300)",
        "item_override": "Treasure Map #31 (Dead S)",
    },

    # Letter Locations
    "Bannan Island Give Letter to Joanne": {
        "region_id": "bannan letter",
        "stage_id": 0x14,
        "floor_id": 0x1,
        "vanilla_item": "Wisdom Gem",
        "item_override": "Jolene's Letter",
        "address": 0x1B558F,
        "value": 0x2
    },
    # Beedle Cards
    "Beedle Membership Bronze": {
        "region_id": "beedle bronze",
        "stage_id": 0x5,
        "floor_id": 0,
        "vanilla_item": "Nothing!",
        "address": 0x1B5588,
        "value": 0x40,
        "conditional": True
    },
    "Beedle Membership Silver": {
        "region_id": "beedle silver",
        "stage_id": 0x5,
        "floor_id": 0,
        "vanilla_item": "Nothing!",
        "address": 0x1B558E,
        "value": 0x20,
        "conditional": True
    },
    "Beedle Membership Gold": {
        "region_id": "beedle gold",
        "stage_id": 0x5,
        "floor_id": 0,
        "vanilla_item": "Nothing!",
        "address": 0x1B558E,
        "value": 0x40,
        "conditional": True
    },
    "Beedle Membership Platinum": {
        "region_id": "beedle plat",
        "stage_id": 0x5,
        "floor_id": 0,
        "vanilla_item": "Nothing!",
        "address": 0x1B558E,
        "value": 0x80,
        "conditional": True
    },
    "Beedle Membership VIP": {
        "region_id": "beedle vip",
        "stage_id": 0x5,
        "floor_id": 0,
        "vanilla_item": "Nothing!",
        "address": 0x1B558F,
        "value": 0x1,
        "conditional": True
    },
    "Ocean NE Man of Smiles Prize Postcard": {
        "region_id": "ne ocean combat",
        "vanilla_item": "Prize Postcard",
        "stage_id": 0x6,
        "floor_id": 0,
        "address": 0x1B558F,
        "value": 0x08
    }



    # ==== New checks at bottom to preserve id ordering
}

for i, name in enumerate(LOCATIONS_DATA):
    LOCATIONS_DATA[name]["id"] = i+1

if __name__ == "__main__":
    """    islands = {}
        island_groups = {}
        for location, data in LOCATIONS_DATA.items():
            islands.setdefault(data["stage_id"], [])
            islands[data["stage_id"]].append(location)
    
        for i, data in islands.items():
            island_groups[STAGES[i]] = data
            print(f"\t\"{STAGES[i]}\": [")
            for loc in data:
                print(f"\t\t\"{loc}\",")
            print(f"\t],")
    """
    for name, data in LOCATIONS_DATA.items():
        if "Salvage" in name and "#" in name:

            print(f"\t\t\"{name}\",")

            """ident = name[name.find("#")+1:name.find(" ", name.find("#"))]
            data["vanilla_item"] = ""
            data["item_override"] = f"Treasure Map #{ident}"

            print(f"\t\"{name}\": " + "{")
            for key, value in data.items():
                if type(value) is str:
                    print(f"\t\t\"{key}\": \"{value}\",")
                else:
                    print(f"\t\t\"{key}\": {value},")
            print("\t},")"""


