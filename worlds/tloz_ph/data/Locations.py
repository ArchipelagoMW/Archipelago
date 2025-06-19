from .Constants import *

# TODO: Add sram data for saveslot 2
# TODO: Add the rest of sram data in bulk

LOCATIONS_DATA = {
    "Mercay Sword Chest": {
        "region_id": "mercay island",
        "vanilla_item": "Sword (Progressive)",
        "stage_id": 11,
        "floor_id": 19,
        "sram_addr": 0x00043C,
        "sram_value": 0x1
    },
    "Mercay Clear Rocks": {
        "region_id": "mercay island",
        "item_override": "Bombs (Progressive)",
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
        "item_override": "Bombchus (Progressive)",
        "stage_id": 11,
        "floor_id": 0,
        "y": 0x1333,
        "vanilla_item": "Treasure Map #10",
        "sram_addr": 0x000EB0,
        "sram_value": 1
    },
    "Mercay Cuccoo Chest": {
        "region_id": "mercay island",
        "item_override": "Hammer",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x1333,
        "vanilla_item": "Treasure",
        "sram_addr": 0x0003C4,
        "sram_value": 0x08
    },
    "Mercay North Bonk Tree": {
        "region_id": "mercay island",
        "item_override": "Pre-Alpha Rupee (5000)",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x2666,
        "sram_addr": 0x0017AC,
        "sram_value": 1,
        "vanilla_item": "Big Green Rupee (100)"
    },
    "Mercay Geozard Cave Chest": {
        "region_id": "mercay zora cave",
        "item_override": "Grappling Hook",
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
        "item_override": "Wisdom Gem",
        "sram_addr": 0x0003C4,
        "sram_value": 0x02
    },
    "Mercay Geozard Cave South Chest East": {
        "region_id": "mercay zora cave south",
        "item_override": "Wisdom Gem",
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
        "item_override": "Triforce Crest",
        "stage_id": 38,
        "floor_id": 0,
        "address": 0x1B55A0,
        "value": 0x4,
        "y": 0x399A,
        "vanilla_item": "Nothing!"
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
        "item_override": "Heart Container",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x4CCD,
        "x_max": 0x00025000,
        "vanilla_item": "Treasure Map #12",
        "sram_addr": 0x000EB0,
        "sram_value": 0x08
    },
    "Mercay Chartreuse Guy Item": {
        "region_id": "mercay yellow guy",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0,
        "x_min": 140000,
        "vanilla_item": "Treasure Map #9",
    },
    "Mercay Shipyard Chest": {
        "region_id": "post tof",
        "stage_id": 11,
        "floor_id": 13,
        "vanilla_item": "Ship Part",
        "item_override": "Wisdom Gem"
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
        "sram_addr": 0x230,
        "sram_value": 2,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Rat Key": {
        "region_id": "mercay passage 2",
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
        "item_override": "SE Sea Chart",
        "vanilla_item": "Power Gem",
        "stage_id": 11,
        "floor_id": 0x11,
        "address": 0x1B5589,
        "value": 0x02,
        "island_shop": True
    },
    "Island Shop Quiver": {
        "region_id": "shop quiver",
        "vanilla_item": "Bow (Progressive)",
        "stage_id": 11,
        "floor_id": 0x11,
        "address": 0x1B5589,
        "value": 0x08,
        "island_shop": True
    },
    "Island Shop Bombchu Bag": {
        "region_id": "shop bombchu bag",
        "vanilla_item": "Bombchus (Progressive)",
        "stage_id": 11,
        "floor_id": 0x11,
        "address": 0x1B5589,
        "value": 0x10,
        "island_shop": True
    },
    "Island Shop Heart Container": {
        "region_id": "shop heart container",
        "vanilla_item": "Heart Container",
        "stage_id": 11,
        "floor_id": 0x11,
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
        "value": 0x04
    },
    "Beedle Shop Wisdom Gem": {
        "region_id": "beedle gem",
        "vanilla_item": "Wisdom Gem",
        "stage_id": 5,
        "floor_id": 0,
        "address": 0x1B5589,
        "value": 0x20
    },
    "Masked Ship Heart Container": {
        "region_id": "masked ship",
        "vanilla_item": "Heart Container",
        "stage_id": 5,
        "floor_id": 0,
        "address": 0x1B5589,
        "value": 0x01,
        "conditional": True,
    },
    "Masked Ship Courage Gem": {
        "region_id": "masked ship",
        "vanilla_item": "Courage Gem",
        "stage_id": 5,
        "floor_id": 0,
        "address": 0x1B558A,
        "value": 0x02,
        "conditional": True
    },

    # ========== TotOK ==============

    "TotOK 1F SW Sea Chart Chest": {
        "region_id": "totok 1f chart chest",
        "vanilla_item": "SW Sea Chart",
        "stage_id": 37,
        "floor_id": 0,
        "y": 0x1333,
        'dungeon': "Temple of the Ocean King",
        'set_bit': [(0x1B557D, 2)]
    },
    "TotOK 1F Linebeck Key": {
        "region_id": "totok",
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
        "region_id": "totok",
        "vanilla_item": "Nothing!",
        "item_override": "Sand of Hours",
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
        "region_id": "totok b1 eye chest",
        "vanilla_item": "Courage Gem",
        "stage_id": 37,
        "floor_id": 1,
        "x_min": 0xB000,
        "x_max": 0x10000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B1 Phantom Chest": {
        "region_id": "totok b1 phantom chest",
        "vanilla_item": "Treasure",
        "item_override": "Power Gem",
        "stage_id": 37,
        "floor_id": 1,
        "x_max": -50000,
        "x_min": -70000,
        "y": 0,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B2 Bombchu Chest": {
        "region_id": "totok b2 bombchu chest",
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
        "region_id": "totok b2 phantom chest",
        "item_override": "Spirit of Wisdom (Progressive)",
        "vanilla_item": "Treasure",
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
        "region_id": "totok b3 bow chest",
        "vanilla_item": "Power Gem",
        "stage_id": 37,
        "floor_id": 3,
        "y": 0x1333,
        "z_max": -22000,
        "z_min": -40000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 Phantom Chest": {
        "region_id": "totok b3 phantom chest",
        "vanilla_item": "Treasure",
        "item_override": "Heart Container",
        "stage_id": 37,
        "floor_id": 3,
        "y": 0x1333,
        "z_min": 0x5000,
        "z_max": 0xD000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 NW Chest": {
        "region_id": "totok b3",
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
        "region_id": "totok b3 locked chest",
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
        "region_id": "totok b3",
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
        "region_id": "totok b3",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 3,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 NW Sea Chart Chest": {
        "region_id": "totok b3.5",
        "vanilla_item": "NW Sea Chart",
        "stage_id": 37,
        "floor_id": 4,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B4 Phantom Eye Chest": {
        "region_id": "totok b4",
        "vanilla_item": "Power Gem",
        "item_override": "Sand of Hours",
        "stage_id": 37,
        "floor_id": 5,
        "x_min": 0xF000,
        "x_max": 0x16000,
        "delay_pickup": "TotOK B4 Small Key",
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B4 Phantom Chest": {
        "region_id": "totok b4 phantom chest",
        "vanilla_item": "Treasure",
        "item_override": "Courage Gem",
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
        "region_id": "totok b5.5 chest",
        "vanilla_item": "Treasure Map #23",
        "stage_id": 37,
        "floor_id": 6,
        "x_max": -15000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B5 Chest": {
        "region_id": "totok b5 chest",
        "item_override": "Sword (Progressive)",
        "vanilla_item": "Potion",
        "stage_id": 37,
        "floor_id": 6,
        "x_min": 0x6000,
        "x_max": 0xC000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B6 Phantom Chest": {
        "region_id": "totok b6 phantom chest",
        "vanilla_item": "Treasure",
        "item_override": "Courage Gem",
        "stage_id": 37,
        "floor_id": 7,
        "z_min": 0xA000,
        "z_max": 0xF000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B6 Bow Chest": {
        "region_id": "totok b6 bow chest",
        "vanilla_item": "Treasure Map #11",
        "item_override": "Spirit of Courage (Progressive)",
        "stage_id": 37,
        "floor_id": 7,
        "z_max": -40000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B6 Courage Crest": {
        "region_id": "totok b6",
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
        "region_id": "totok b7 east",
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
        "region_id": "totok b7 peg",
        "vanilla_item": "Courage Gem",
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
        "stage_id": 37,
        "floor_id": 0xA,
        "x_max": -60000,
        "z_max": -50000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B8 2 Crystals Chest": {
        "region_id": "totok b8 2 crystals",
        "vanilla_item": "Courage Gem",
        "stage_id": 37,
        "floor_id": 0xB,
        "x_max": -10000,
        "z_max": -30000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B8 Phantom Chest": {
        "region_id": "totok b7 phantom",
        "vanilla_item": "Ship Part",
        "stage_id": 37,
        "floor_id": 0xB,
        "x_max": 50000,
        "z_max": 10000,
        "x_min": 25000,
        "z_min": -10000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B9 NW Chest": {
        "region_id": "totok b9 nw",
        "vanilla_item": "Triangle Crystal (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 0xC,
        "x_min": -45000,
        "z_max": -30000,
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B9 Ghost Chest": {
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
        "stage_id": 37,
        "floor_id": 0xC,
        "x_max": -60000,
        "z_min": 45000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B9.5 SE Sea Chart Chest": {
        "region_id": "totok b9.5",
        "vanilla_item": "SE Sea Chart",
        "stage_id": 37,
        "floor_id": 0xD,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B10 Hammer Switch Chest": {
        "region_id": "totok b10 hammer",
        "vanilla_item": "Treasure Map #30",
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
        "region_id": "totok b10 phantom eyes",
        "vanilla_item": "Potion",
        "stage_id": 37,
        "floor_id": 0xE,
        "y": 0x1333,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B10 Small Key": {
        "region_id": "totok b10",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 0xE,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B11 Phantom Eye Chest": {
        "region_id": "totok b11",
        "vanilla_item": "Treasure",
        "item_override": "Bombs (Progressive)",
        "stage_id": 37,
        "floor_id": 0x0F,
        "x_min": 50000,
        "z_max": -45000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B11 Phantom Chest": {
        "region_id": "totok b11 phantom",
        "vanilla_item": "Big Red Rupee (200)",
        "stage_id": 37,
        "floor_id": 0x0F,
        "x_max": -50000,
        "z_min": 40000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 NW Chest": {
        "region_id": "totok b12",
        "vanilla_item": "Force Gem (B12)",
        "stage_id": 37,
        "floor_id": 0x10,
        "x_min": 35000,
        "z_max": -50000,
        "force_vanilla": True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 NE Chest": {
        "region_id": "totok b12",
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
        "vanilla_item": "Treasure Map #31",
        "item_override": "Spirit of Power (Progressive)",
        "stage_id": 37,
        "floor_id": 0x10,
        "x_min": 65000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 Ghost Chest": {
        "region_id": "totok b13",
        "vanilla_item": "Ship Part",
        "item_override": "Spirit of Courage (Progressive)",
        "stage_id": 37,
        "floor_id": 0x10,
        "x_max": -65000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B12 Phantom Chest": {
        "region_id": "totok b12 phantom",
        "vanilla_item": "Gold Rupee (300)",
        "stage_id": 37,
        "floor_id": 0x10,
        "x_min": -10000,
        "z_min": 0,
        "x_max": 10000,
        "z_max": 25000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B13 NE Sea Chart Chest": {
        "region_id": "totok b13",
        "vanilla_item": "NE Sea Chart",
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
        "item_override": "Courage Gem",
        "stage_id": 0xA,
        "floor_id": 0,
        "address": 0x1B5592,
        "value": 0x1
    },

    # Cannon Island
    "Cannon Island Bee Chest": {
        "region_id": "cannon island",
        "vanilla_item": "Treasure Map #1",
        "stage_id": 0x13,
        "floor_id": 0,
        "x_max": -30000,
        "z_max": -15000,
        "y": 0x1333,
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
        "item_override": "Cyclone Slate",
        "stage_id": 0x13,
        "floor_id": 0,
        "y": 0x2666
    },
    "Cannon Island Bonk Tree": {
        "region_id": "cannon island",
        "vanilla_item": "Big Red Rupee (200)",
        "stage_id": 0x13,
        "floor_id": 0,
        "y": 0x1333,
        "x_min": 0,
        "z_min": 12300,
        "sram_addr": 0x0006DC,
        "sram_value": 0x1
    },
    "Cannon Island Dig": {
        "region_id": "cannon island dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0x13,
        "floor_id": 0,
        "y": 0x1333,
        "x_min": 0,
        "z_max": 12300,
        "sram_addr": 0x000190,
        "sram_value": 2
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
        "vanilla_item": "Treasure Map #3",
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
        "vanilla_item": "Treasure Map #4",
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
        "item_override": "Power Gem",
        "vanilla_item": "Nothing!",
        "stage_id": 0xD,
        "floor_id": 10,
        "address": 0x1B557F,
        "value": 0x20
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
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire Blaaz Heart Container": {
        "region_id": "tof blaaz",
        "vanilla_item": "Heart Container",
        "stage_id": 0x2B,
        "floor_id": 0,
        "dungeon": "Temple of Fire"
    },
    "Temple of Fire Blaaz Boss Reward": {
        "region_id": "tof blaaz",
        "vanilla_item": "Spirit of Power (Progressive)",
        "item_override": "Rare Metal",
        "stage_id": 0x2B,
        "floor_id": 0,
        "address": 0x1B557F,
        "value": 0x20,
        "dungeon": "Temple of Fire",
        "boss_reward_location": True,
    },

    # ============ Molida Island ==============

    "Molida Island 2nd House Chest": {
        "region_id": "molida island",
        "vanilla_item": "Treasure",
        "item_override": "Courage Gem",
        "stage_id": 0xC,
        "floor_id": 0xD,
    },

    "Molida Island Romanos Tree Dig": {
        "region_id": "molida dig",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 0xC,
        "floor_id": 0,
        "y": 0
    },
    "Molida Cave Wayfarer Hideaway Chest": {
        "region_id": "molida dig",
        "vanilla_item": "Treasure Map #2",
        "stage_id": 0xC,
        "floor_id": 10,
        "y": 0,
        "x_max": -25000,
        "z_min": 25000
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
        "x_min": 15000
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
        "sram_value": 0x100
    },
    "Molida Island Cliff Chest": {
        "region_id": "molida cave back",
        "vanilla_item": "Treasure",
        "item_override": "Wisdom Gem",
        "stage_id": 0xC,
        "floor_id": 1,
        "y": 0x1333,
        "x_max": -18000,
        "z_min": -30000
    },
    "Molida Island Cuccoo Dig": {
        "region_id": "molida cuccoo dig",
        "vanilla_item": "Treasure Map #20",
        "stage_id": 0xC,
        "floor_id": 0,
        "y": 0x1333,
        "x_min": 90000
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
        "value": 0x8
    },
    "Molida Archery 2000": {
        "region_id": "molida archery",
        "vanilla_item": "Heart Container",
        "stage_id": 0xC,
        "floor_id": 1,
        "address": 0x1B55A6,
        "value": 0x10
    },

    # ============= Temple of Courage ===========

    "Temple of Courage 1F Bomb Alcove Chest": {
        "region_id": "toc bomb alcove",
        "vanilla_item": "Treasure",
        "item_override": "Power Gem",
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
        "item_override": "Wisdom Gem",
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
        "item_override": "Power Gem",
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
    "Temple of Courage Crayk Spirit of Courage": {
        "region_id": "toc crayk",
        "vanilla_item": "Spirit of Courage (Progressive)",
        "item_override": "Rare Metal",
        "stage_id": 0x2C,
        "floor_id": 0,
        "address": 0x1B557F,
        "value": 0x80,
        "dungeon": "Temple of Courage",
        "boss_reward_location": True
    },
    "Temple of Courage Crayk Sand of Hours": {
        "region_id": "toc crayk",
        "vanilla_item": "Sand of Hours",
        "stage_id": 0x2C,
        "floor_id": 0,
        "address": 0x1B557F,
        "value": 0x80,
        "dungeon": "Temple of Courage"
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
        "conditional": True,
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
        "conditional": True,
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
        "conditional": True,
        "address": 0x1BA647,
        "value": 0x04
    },
}

for i, name in enumerate(LOCATIONS_DATA):
    LOCATIONS_DATA[name]["id"] = i+1

