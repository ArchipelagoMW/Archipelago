"""
"Dynamic Flag Name": {
    "on_scenes": list[int],
    "has_items": list[tuple[str, int]],         item_name, count (0 for none)
    "has_locations": list[str],
    "not_has_locations": list[str],
    "set_if_true": list[tuple[int, int]],       adress, value
    "unset_if_true": list[tuple[int, int]],     adress, value
    "has_slot_data": list[list[str, any]]       slot_data, ==value
}
"""
DYNAMIC_FLAGS = {
    "Astrid's Basement Treasure Map": {
        "on_scenes": [0xD14],
        "not_has_locations": ["Isle of Ember Astrid's Basement Dig"],
        "unset_if_true": [(0x1BA651, 0x20)]
    },
    "RESET Astrid's Basement Treasure Map": {
        "on_scenes": [0xD0A],
        "has_items": [("Treasure Map #3", 1)],
        "set_if_true": [(0x1BA651, 0x20)]
    },
    "Ember summit treasure map": {
        "on_scenes": [0xD01],
        "not_has_locations": ["Isle of Ember Summit Dig"],
        "unset_if_true": [(0x1BA651, 0x80)]
    },
    "RESET Ember summit treasure map": {
        "on_scenes": [0xD00, 0x1C0],
        "has_items": [("Treasure Map #4", 1)],
        "set_if_true": [(0x1BA651, 0x80)]
    },
    "Mercay yellow guy treasure map": {
        "on_scenes": [0xB03],
        "not_has_locations": ["Mercay Chartreuse Guy Item"],
        "unset_if_true": [(0x1BA650, 0x02)]
    },
    "RESET Mercay yellow guy treasure map": {
        "on_scenes": [0x000, 0xB00, 0xB02, 0xB0C, 0xB0D, 0xB0E, 0xB0F, 0xB11, 0x2701],
        "has_items": [("Treasure Map #9", 1)],
        "set_if_true": [(0x1BA650, 0x02)]
    },
    "Mercay freedle gift treasure map": {
        "on_scenes": [0xB02],
        "not_has_locations": ["Mercay Freedle Gift Item"],
        "unset_if_true": [(0x1BA652, 0x20)]
    },
    "RESET Mercay freedle gift treasure map": {
        "on_scenes": [0xB01, 0xB03, 0xB12],
        "has_items": [("Treasure Map #12", 1)],
        "set_if_true": [(0x1BA652, 0x20)]
    },
    "Mercay oshus dig treasure map": {
        "on_scenes": [0xB00],
        "not_has_locations": ["Mercay Oshus Dig"],
        "unset_if_true": [(0x1BA651, 0x10)]
    },
    "RESET Mercay oshus dig treasure map": {
        "on_scenes": [0xB01, 0xB03, 0xB13, 0xB01, 0xB0A, 0xB0B],
        "has_items": [("Treasure Map #10", 1)],
        "set_if_true": [(0x1BA651, 0x10)]
    },
    "Molida Cuccoo dig map": {
        "on_scenes": [0xC00],
        "not_has_locations": ["Molida Island Cuccoo Dig"],
        "unset_if_true": [(0x1BA651, 0x40)]
    },
    "RESET Molida Cuccoo dig map": {
        "on_scenes": [0x000, 0xC01, 0xC0A, 0xC0B, 0xC0C,  0xC0D, 0xC0E,],
        "has_items": [("Treasure Map #20", 1)],
        "set_if_true": [(0x1BA651, 0x40)]
    },
    "TotoK Don't open key door": {
        "on_scenes": [0x2500],
        "not_has_locations": ["TotOK 1F SW Sea Chart Chest"],
        "unset_if_true": [(0x1B557D, 0x02)]
    },
    "TotoK remove linebeck": {
        "on_scenes": [0x2500],
        "has_locations": ["TotOK 1F SW Sea Chart Chest"],
        "set_if_true": [(0x1B557D, 0x02)]
    },
    "Enter Cannon: Not Bought Cannon": {
        "on_scenes": [0x130B],
        "not_has_locations": ["Cannon Island Cannon"],
        "unset_if_true": [(0x1B5582, 0x1)]
    },
    "Enter Cannon: Not Bought Salvage": {
        "on_scenes": [0x130B],
        "not_has_locations": ["Cannon Island Salvage Arm"],
        "has_locations": ["Cannon Island Cannon"],
        "set_if_true": [(0x1B5582, 0x1)],
        "unset_if_true": [(0x1BA649, 0x10)],
    },
    "Exit Cannon: Have Cannon": {
        "on_scenes": [0x1300, 0x130A],
        "has_items": [("Cannon", 1)],
        "set_if_true": [(0x1B5582, 0x1)]
    },
    "Exit Cannon: Have Salvage": {
        "on_scenes": [0x1300, 0x130A],
        "has_items": [("Salvage Arm", 1)],
        "set_if_true": [(0x1BA649, 0x10)]
    },
    "Exit Cannon: Not Have Cannon": {
        "on_scenes": [0x1300, 0x130A],
        "has_items": [("Cannon", 0)],
        "unset_if_true": [(0x1B5582, 0x1)]
    },
    "Exit Cannon: Not Have Salvage": {
        "on_scenes": [0x1300, 0x130A],
        "has_items": [("Salvage Arm", 0)],
        "unset_if_true": [(0x1BA649, 0x10)]
    },
    "Mercay skip blow on map for Linebeck": {
        "on_scenes": [0xB03],
        "unset_if_true": [(0x1B557D, 0x02)]
    },
    "Cannon Open Door": {
        "on_scenes": [0x130B],
        "set_if_true": [(0x1B5582, 0x2)]
    },
    "Spirit of Power 1": {
        "on_scenes": [0x1701],
        "not_has_locations": ["Spirit Island Power Upgrade Level 1"],
        "unset_if_true": [(0x1BA647, 0x9)]
    },
    "Spirit of Wisdom 1": {
        "on_scenes": [0x1701],
        "not_has_locations": ["Spirit Island Wisdom Upgrade Level 1"],
        "unset_if_true": [(0x1BA647, 0x12)]
    },
    "Spirit of Courage 1": {
        "on_scenes": [0x1701],
        "not_has_locations": ["Spirit Island Courage Upgrade Level 1"],
        "unset_if_true": [(0x1BA646, 0x80), (0x1BA647, 0x04)]
    },
    "Spirit of Power 2": {
        "on_scenes": [0x1701],
        "has_locations": ["Spirit Island Power Upgrade Level 1"],
        "not_has_locations": ["Spirit Island Power Upgrade Level 2"],
        "unset_if_true": [(0x1BA647, 0x8)],
        "set_if_true": [(0x1BA647, 0x1)],
    },
    "Spirit of Wisdom 2": {
        "on_scenes": [0x1701],
        "has_locations": ["Spirit Island Wisdom Upgrade Level 1"],
        "not_has_locations": ["Spirit Island Wisdom Upgrade Level 2"],
        "unset_if_true": [(0x1BA647, 0x10)],
        "set_if_true": [(0x1BA647, 0x2)],
    },
    "Spirit of Courage 2": {
        "on_scenes": [0x1701],
        "has_locations": ["Spirit Island Courage Upgrade Level 1"],
        "not_has_locations": ["Spirit Island Courage Upgrade Level 2"],
        "unset_if_true": [(0x1BA647, 0x4)],
        "set_if_true": [(0x1BA646, 0x80)],
    },
    "RESET Spirit of power 1": {
        "on_scenes": [0x1700],
        "has_items": [("Spirit of Power (Progressive)", 2)],
        "set_if_true": [(0x1BA647, 0x1)]
    },
    "RESET Spirit of power 2": {
        "on_scenes": [0x1700],
        "has_items": [("Spirit of Power (Progressive)", 3)],
        "set_if_true": [(0x1BA647, 0x9)]
    },
    "RESET Spirit of Wisdom 1": {
        "on_scenes": [0x1700],
        "has_items": [("Spirit of Wisdom (Progressive)", 2)],
        "set_if_true": [(0x1BA647, 0x02)]
    },
    "RESET Spirit of Wisdom 2": {
        "on_scenes": [0x1700],
        "has_items": [("Spirit of Wisdom (Progressive)", 3)],
        "set_if_true": [(0x1BA647, 0x10)]
    },
    "RESET Spirit of Courage 1": {
        "on_scenes": [0x1700],
        "has_items": [("Spirit of Courage (Progressive)", 2)],
        "set_if_true": [(0x1BA646, 0x80)]
    },
    "RESET Spirit of Courage 2": {
        "on_scenes": [0x1700],
        "has_items": [("Spirit of Courage (Progressive)", 3)],
        "set_if_true": [(0x1BA646, 0x80), (0x1BA647, 0x04)]
    },
    "Spirit of Wisdom boss flag": {
        "on_scenes": [0x1701],
        "has_items": [("Spirit of Wisdom (Progressive)", 1)],
        "set_if_true": [(0x1B557F, 0x40)]
    },
    "Spirit of Courage boss flag": {
        "on_scenes": [0x1701],
        "has_items": [("Spirit of Courage (Progressive)", 1)],
        "set_if_true": [(0x1B557F, 0xC0)]
    },
    "RESET Spirit of Wisdom boss flag": {
        "on_scenes": [0x1700],
        "not_has_locations": ["Temple of Courage Crayk Spirit of Courage"],  # TODO add Cyklok when location exists
        "unset_if_true": [(0x1B557F, 0x40)]
    },
    "RESET Spirit of Courage boss flag": {
        "on_scenes": [0x1700],
        "not_has_locations": ["Temple of Courage Crayk Spirit of Courage"],
        "unset_if_true": [(0x1B557F, 0x80)]
    },
    "Courage Creset room not salvaged it": {
        "on_scenes": [0x2508],
        "has_locations": ["Ocean SW Salvage Courage Crest"],
        "unset_if_true": [(0x1B557E, 0x40)]
    },
    "RESET Courage Creset room not salvaged it": {
        "on_scenes": [0x2600, 0x2507],
        "has_locations": ["Ocean SW Salvage Courage Crest"],
        "set_if_true": [(0x1B557E, 0x40)]
    },
    "Courage Crest room remove crest": {
        "on_scenes": [0x2508],
        "unset_if_true": [(0x1B558C, 0x04)],
        "not_has_locations": ["TotOK B6 Courage Crest"]
    },
    "RESET Courage Crest room remove crest": {
        "on_scenes": [0x2600, 0x2507],
        "has_items": [("Courage Crest", 1)],
        "set_if_true": [(0x1B558C, 0x04)]
    },
    # Endgame
    "Spawn Phantoms in Totok B13": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "has_slot_data": [["bellum_access", 1], ["bellum_access", 2], ["bellum_access", 3]],
        "set_if_true": [(0x1B5592, 0x40)]
    },
    "Spawn Phantoms in Totok B13 door option": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "goal_requirement": True,
        "has_slot_data": [["bellum_access", 0]],
        "set_if_true": [(0x1B5592, 0x40)]
    },
    "RESET Spawn Phantoms in Totok B13": {
        "on_scenes": [0x2600],
        "unset_if_true": [(0x1B5592, 0x40)]
    },
    "Block Bellum Staircase": {
        "on_scenes": [0x2600],
        "set_if_true": [(0x1B5595, 0x2)]
    },
    "RESET Block Bellum Staircase": {
        "on_scenes": [0xB01],
        "unset_if_true": [(0x1B5595, 0x2)]
    },
    "Unblock bellum staircase": {
        "on_scenes": [0x2512],
        "goal_requirement": True,
        "unset_if_true": [(0x1B5595, 0x2)]
    },
    "Spawn bellum warp": {
        "on_scenes": [0x2600],
        "goal_requirement": True,
        "set_if_true": [(0x1B5599, 0x4)],
        "has_slot_data": [["bellum_access", 2]],
    },
    "Spawn phantom wreckage": {
        "on_scenes": [0x0],
        "goal_requirement": True,
        "has_items": [("Sword (Progressive)", 2), ("Spirit of Courage (Progressive)", 1)],
        "set_if_true": [(0x1B559B, 0x1)],
        "has_slot_data": [["bellum_access", 3]],
    },
    "Not Triforce Crest Rando": {
        "on_scenes": [0x2507],
        "set_if_true": [(0x1B5580, 0x2)],
        "has_slot_data": [["randomize_triforce_crest", 0]],
    },
    # boat requires sea chart
    "Despawn linebeck 2": {
        "on_scenes": [0xB03],
        "unset_if_true": [(0x1B5580, 0x4)],
    },
    "RESET despawn linebeck 2": {
        "on_scenes": [0xB02],
        "set_if_true": [(0x1B5580, 0x4)],
    },
    "Despawn Linebeck setting": {
        "on_scenes": [0xB03],
        "has_slot_data": [["boat_requires_sea_chart", 1]],
        "has_items": [("SW Sea Chart", 0)],
        "unset_if_true": [(0x1B557E, 0x8)]
    },
    "Spawn Linebeck setting": {
        "on_scenes": [0xB03],
        "has_slot_data": [["boat_requires_sea_chart", 1]],
        "has_items": [("SW Sea Chart", 1)],
        "set_if_true": [(0x1B557E, 0x8)]
    },
    "RESET Despawn Linebeck setting": {
        "on_scenes": [0xB02],
        "set_if_true": [(0x1B557E, 0x8)]
    }
}

