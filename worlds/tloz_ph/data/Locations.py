from .Constants import *

# TODO: Add sram data for saveslot 2

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
    "Mercay Zora Cave Chest": {
        "region_id": "mercay zora cave",
        "item_override": "Grappling Hook",
        "stage_id": 11,
        "floor_id": 16,
        "vanilla_item": "Power Gem",
        "sram_addr": 0x000418,
        "sram_value": 1
    },
    "Mercay Zora Cave South Chest 1": {
        "region_id": "mercay zora cave south",
        "item_override": "Shovel",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x2666,
        "x_max": 0x00016200,
        "vanilla_item": "Ship Part",
        "sram_addr": 0x0003C4,
        "sram_value": 0x02
    },
    "Mercay Zora Cave South Chest 2": {
        "region_id": "mercay zora cave south",
        "item_override": "Ship Part",
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
        "item_override": "Bombs (Progressive)",
        "stage_id": 38,
        "floor_id": 0,
        "address": 0x1B55A0,
        "value": 0x4,
        "y": 0x399A,
        "vanilla_item": "Green Rupee (1)"
    },
    "Mercay Freedle Tunnel Chest": {
        "region_id": "mercay freedle tunnel chest",
        "item_override": "Boomerang",
        "stage_id": 11,
        "floor_id": 18,
        "vanilla_item": "Courage Gem",
        "sram_addr": 0x000430,
        "sram_value": 1
    },
    "Mercay Freedle Island Chest": {
        "region_id": "mercay freedle island",
        "item_override": "Bow (Progressive)",
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


    # Mountain Passage

    "Mountain Passage Chest 1": {
        "region_id": "mercay passage 1",
        "vanilla_item": "Small Key (Mountain Passage)",
        "stage_id": 0x27,
        "floor_id": 0,
        "y": 0x1333,
        "sram_addr": 0x000AE4,
        "sram_value": 8,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Chest 2": {
        "region_id": "mercay passage 2",
        "item_override": "Spirit of Power (Progressive)",
        "stage_id": 0x27,
        "floor_id": 0,
        "x_min": 0x00010900,
        "z_max": 0xFFFF6E00,
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
        "sram_addr": 0x000230,
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
    "Mercay Shop Power Gem": {
        "region_id": "shop power gem",
        "item_override": "SE Sea Chart",
        "vanilla_item": "Power Gem",
        "stage_id": 11,
        "floor_id": 0x11,
        "address": 0x1B5589,
        "value": 0x02
    },
    "Island Shop Quiver": {
        "region_id": "shop quiver",
        "vanilla_item": "Bow (Progressive)",
        "stage_id": 11,
        "floor_id": 0x11,
        "address": 0x1B5589,
        "value": 0x08
    },
    "Island Shop Bombchu Bag": {
        "region_id": "shop bombchu bag",
        "vanilla_item": "Bombchus (Progressive)",
        "stage_id": 11,
        "floor_id": 0x11,
        "address": 0x1B5589,
        "value": 0x10
    },
    "Island Shop Heart Container": {
        "region_id": "shop heart container",
        "vanilla_item": "Heart Container",
        "stage_id": 11,
        "floor_id": 0x11,
        "address": 0x1B5588,
        "value": 0x80

    # ========== TotOK ==============

    },
    "TotOK 1F SW Sea Chart Chest": {
        "region_id": "totok 1f chart chest",
        "vanilla_item": "SW Sea Chart",
        "stage_id": 37,
        "floor_id": 0,
        "y": 0x1333,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK 1F Linebeck Key": {
        "region_id": "totok",
        "vanilla_item": "Small Key (Temple of the Ocean King)",
        "stage_id": 37,
        "floor_id": 0,
        "z_min": 0xB000,
        "z_max": 0x11000,
        "x_min": -100,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK 1F Empty Chest": {
        "region_id": "totok",
        "vanilla_item": "Sand of Hours",
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
        "vanilla_item": "Courage Gem",
        "stage_id": 37,
        "floor_id": 1,
        "x_max": 0xFFFF3000,
        "x_min": 0xFFFF0000,
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
        "x_max": 0xFFFFE000,
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
        "item_override": "Big Green Rupee (100)",
        "stage_id": 37,
        "floor_id": 3,
        "y": 0x1333,
        "z_max": 0xFFFFA000,
        "z_min": 0xFFFF5000,
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
        "vanilla_item": "Force Gem",
        "stage_id": 37,
        "floor_id": 3,
        "x_max": 0xFFFF3000,
        "z_max": 0xFFFF7000,
        "y": 0,
        "delay_pickup": "TotOK B3 Small Key",
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 SW Chest": {
        "region_id": "totok b3 locked chest",
        "vanilla_item": "Force Gem",
        "stage_id": 37,
        "floor_id": 3,
        "x_max": 0xFFFFC000,
        "z_min": 0x8000,
        "y": 0,
        "delay_pickup": "TotOK B3 Small Key",
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B3 SE Chest": {
        "region_id": "totok b3",
        "vanilla_item": "Force Gem",
        "stage_id": 37,
        "floor_id": 3,
        "x_min": 0xFA00,
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
        "item_override": "Spirit of Courage (Progressive)",
        "stage_id": 37,
        "floor_id": 5,
        "x_max": 0xFFFF1000,
        "x_min": 0xFFFE0000,
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
        "item_override": "Spirit of Power (Progressive)",
        "stage_id": 37,
        "floor_id": 6,
        "x_max": 0xFFFFD000,
        "x_min": 0xFFFF6000,
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
        "item_override": "Spirit of Wisdom (Progressive)",
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
        "z_max": 0xFFFF3000,
        "z_min": 0xFFFE0000,
        'dungeon': "Temple of the Ocean King"
    },
    "TotOK B6 Courage Crest": {
        "region_id": "totok b6",
        "vanilla_item": "Courage Crest",
        "stage_id": 37,
        "floor_id": 8,
        "address": 0x1B558C,
        "value": 0x4,
        'force_vanilla': True,
        'dungeon': "Temple of the Ocean King"
    },
}


for i, name in enumerate(LOCATIONS_DATA):
    LOCATIONS_DATA[name]["id"] = i+1

