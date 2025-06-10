from .Constants import *

# TODO: Add sram data for saveslot 2

LOCATIONS_DATA = {
    "Mercay Sword Chest": {
        "region_id": "mercay island",
        "vanilla_item": "Sword",
        "stage_id": 11,
        "floor_id": 19,
        "sram_addr": 0x00043C,
        "sram_value": 0x1
    },
    "Mercay Clear Rocks": {
        "region_id": "mercay island",
        "vanilla_item": "Bombs (Progressive)",
        "stage_id": 11,
        "floor_id": 0,
        "y": 0,
        "true_item": "Green Rupee (1)",
        "sram_addr": 0x0020CA,
        "sram_value": 0x40
    },
    "Mercay Oshus Dig": {
        "region_id": "mercay dig spot",
        "vanilla_item": "Bombchus (Progressive)",
        "stage_id": 11,
        "floor_id": 0,
        "y": 0x1333,
        "true_item": "Treasure Map #10",
        "sram_addr": 0x000EB0,
        "sram_value": 1
    },
    "Mercay Cuccoo Chest": {
        "region_id": "mercay island",
        "vanilla_item": "Hammer",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x1333,
        "true_item": "Treasure",
        "sram_addr": 0x0003C4,
        "sram_value": 0x08
    },
    "Mercay North Bonk Tree": {
        "region_id": "mercay island",
        "vanilla_item": "Big Green Rupee (100)",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x2666,
        "sram_addr": 0x0017AC,
        "sram_value": 1
    },
    "Mercay Zora Cave Chest": {
        "region_id": "mercay zora cave",
        "vanilla_item": "Grappling Hook",
        "stage_id": 11,
        "floor_id": 16,
        "true_item": "Power Gem",
        "sram_addr": 0x000418,
        "sram_value": 1
    },
    "Mercay Zora Cave South Chest 1": {
        "region_id": "mercay zora cave south",
        "vanilla_item": "Shovel",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x2666,
        "x_max": 0x00016200,
        "true_item": "Ship Part",
        "sram_addr": 0x0003C4,
        "sram_value": 0x02
    },
    "Mercay Zora Cave South Chest 2": {
        "region_id": "mercay zora cave south",
        "vanilla_item": "Ship Part",
        "stage_id": 11,
        "floor_id": 3,
        "y": 0x2666,
        "x_min": 0x00016200,
        "true_item": "Big Green Rupee (100)",
        "sram_addr": 0x0003C4,
        "sram_value": 0x04
    },
    "TotOK Phantom Hourgalss": {
        "region_id": "totok",
        "vanilla_item": "SW Sea Chart",
        "stage_id": 38,
        "floor_id": 0,
        "address": 0x1B55A0,
        "value": 0x4,
        "true_item": "Green Rupee (1)"
    },
    "Mercay Freedle Tunnel Chest": {
        "region_id": "mercay freedle tunnel chest",
        "vanilla_item": "Boomerang",
        "stage_id": 11,
        "floor_id": 18,
        "true_item": "Courage Gem",
        "sram_addr": 0x000430,
        "sram_value": 1
    },
    "Mercay Freedle Island Chest": {
        "region_id": "mercay freedle island",
        "vanilla_item": "Bow (Progressive)",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x4CCD,
        "x_min": 0x00025000,
        "true_item": "Wisdom Gem",
        "sram_addr": 0x0003AC,
        "sram_value": 64
    },
    "Mercay Freedle Gift Item": {
        "region_id": "mercay freedle island",
        "vanilla_item": "Power Gem",
        "stage_id": 11,
        "floor_id": 2,
        "y": 0x4CCD,
        "x_max": 0x00025000,
        "true_item": "Treasure Map #12",
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
        "sram_addr": None,
        "sram_value": None,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Chest 2": {
        "region_id": "mercay passage 2",
        "vanilla_item": "Spirit of Power (Progressive)",
        "stage_id": 0x27,
        "floor_id": 0,
        "x_min": 0x00010900,
        "z_max": 0xFFFF6E00,
        "true_item": "Red Rupee (20)",
        "sram_addr": None,
        "sram_value": None,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Key Drop": {
        "region_id": "mercay passage 2",
        "vanilla_item": "Small Key (Mountain Passage)",
        "stage_id": 0x27,
        "floor_id": 0,
        "sram_addr": None,
        "sram_value": None,
        "dungeon": "Mountain Passage"
    },
    "Mountain Passage Rat Key": {
        "region_id": "mercay passage 2",
        "vanilla_item": "Small Key (Mountain Passage)",
        "stage_id": 0x27,
        "floor_id": 1,
        "sram_addr": None,
        "sram_value": None,
        "dungeon": "Mountain Passage"
    },
    "Mercay Shop Power Gem": {
        "region_id": "shop power gem",
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
    },
}
