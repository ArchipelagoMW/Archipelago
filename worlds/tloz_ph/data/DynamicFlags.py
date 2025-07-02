"""
"Dynamic Flag Name": {
    "on_scenes": list[int],
    "not_last_scenes": list[int]
    "has_items": list[tuple[str, int]],         item_name, min count (0 for not have item)
    "has_locations": list[str],
    "not_has_locations": list[str],
    "any_not_has_locations": list[str],
    "set_if_true": list[tuple[int, int]],       address, value
    "unset_if_true": list[tuple[int, int]],     address, value
    "has_slot_data": list[list[str, any]]       slot_data, ==value
    "goal_requirement": bool                    checks dungeon requirement if true
}
"""
DYNAMIC_FLAGS = {
    # Treasure Maps
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
    "Zauz Map": {
        "on_scenes": [0x1600],
        "not_has_locations": ["Zauz's Island Secret Dig"],
        "unset_if_true": [(0x1BA650, 0x40)]
    },
    "RESET Zauz Map": {
        "on_scenes": [0x1],
        "has_items": [("Treasure Map #5", 1)],
        "set_if_true": [(0x1BA650, 0x40)]
    },
    "Uncharted Island Map": {
        "on_scenes": [0x1A00],
        "not_has_locations": ["Uncharted Island Eye Dig"],
        "unset_if_true": [(0x1BA651, 0x1)]
    },
    "RESET Uncharted Island Map": {
        "on_scenes": [0x1],
        "has_items": [("Treasure Map #6", 1)],
        "set_if_true": [(0x1BA651, 0x1)]
    },
    "Frost Island Map": {
        "on_scenes": [0xF02],
        "not_has_locations": ["Isle of Frost Estate SW Island Dig"],
        "unset_if_true": [(0x1BA651, 0x4)]
    },
    "RESET Frost Island Map": {
        "on_scenes": [0xF00],
        "has_items": [("Treasure Map #19", 1)],
        "set_if_true": [(0x1BA651, 0x4)]
    },
    "Bannan Wayfarer Map": {
        "on_scenes": [0x1400],
        "not_has_locations": ["Bannan Island Wayfarers Dig"],
        "unset_if_true": [(0x1BA650, 0x20)]
    },
    "RESET Bannan Wayfarer Map": {
        "on_scenes": [0x1],
        "has_items": [("Treasure Map #21", 1)],
        "set_if_true": [(0x1BA650, 0x20)]
    },
    "Bannan Island Map": {
        "on_scenes": [0x1400],
        "not_has_locations": ["Bannan Island East Grapple Dig"],
        "unset_if_true": [(0x1BA652, 0x8)]
    },
    "RESET Bannan Island Map": {
        "on_scenes": [0x1],
        "has_items": [("Treasure Map #22", 1)],
        "set_if_true": [(0x1BA652, 0x8)]
    },
    # TotoK 1F
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

    # Cannon Island
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
        "unset_if_true": [(0x1B557D, 0x1d2)]
    },
    "Cannon Open Door": {
        "on_scenes": [0x130B],
        "set_if_true": [(0x1B5582, 0x2)]
    },

    # Spirit Island
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
        "not_has_locations": ["Temple of Wind Cyclok Dungeon Reward"],
        "unset_if_true": [(0x1B557F, 0x40)]
    },
    "RESET Spirit of Courage boss flag": {
        "on_scenes": [0x1700],
        "not_has_locations": ["Temple of Courage Crayk Dungeon Reward"],
        "unset_if_true": [(0x1B557F, 0x80)]
    },
    # Courage Crest Room
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
    "Courage Crest room remove crest if not got it": {
        "on_scenes": [0x2600, 0x2507],
        "has_items": [("Courage Crest", 0)],
        "unset_if_true": [(0x1B558C, 0x04)]
    },

    # Endgame
    "Spawn Phantoms in Totok B13": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "has_slot_data": [["bellum_access", 1]],
        "set_if_true": [(0x1B5592, 0x40)]
    },
    "Spawn Phantoms in Totok B13 2": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "has_slot_data": [["bellum_access", 2]],
        "set_if_true": [(0x1B5592, 0x40)]
    },
    "Spawn Phantoms in Totok B13 3": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "has_slot_data": [["bellum_access", 3]],
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
    },

    # Fog
    "No fog add fog if spirits": {
        "on_scenes": [0x01],
        "not_last_scenes": [0x2903],
        "has_items": [("Spirit of Power (Progressive)", 1),
                      ("Spirit of Wisdom (Progressive)", 1),
                      ("Spirit of Courage (Progressive)", 1)],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "has_slot_data": [("fog_settings", 0)],
        "unset_if_true": [(0x1B5582, 0x80)],
        "set_if_true": [(0x1B55AB, 0x10)]
    },
    "Remove fog on ghost ship if no fog": {
        "on_scenes": [0x2903],
        "has_slot_data": [("fog_settings", 0)],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B5582, 0x80), (0x1B55AB, 0x10)],
    },
    "Spawn Spirits in fog": {
        "on_scenes": [0x1],
        "not_last_scenes": [0x2903],
        "has_items": [("Spirit of Power (Progressive)", 1),
                      ("Spirit of Wisdom (Progressive)", 1),
                      ("Spirit of Courage (Progressive)", 1)],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B557E, 0x10)],
    },
    "Remove spirit flag on GS": {
        "on_scenes": [0x2903],
        "unset_if_true": [(0x1B557E, 0x10)]
    },
    "Remove fog on GS if saved tetra": {
        "on_scenes": [0x2903],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B5582, 0x80), (0x1B55AB, 0x10)]
    },
    "Respawn ghost ship": {
        "on_scenes": [0x1],
        "not_last_scenes": [0x2903, 0x400],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "any_not_has_locations": ["Ghost Ship B1 Entrance Chest",
                                  "Ghost Ship B1 Second Sister Chest",
                                  "Ghost Ship B2 Third Sister Left Chest",
                                  "Ghost Ship B2 Third Sister Right Chest",
                                  "Ghost Ship B2 Spike Chest",
                                  "Ghost Ship B3 Chest",
                                  "Ghost Ship Cubus Sisters Ghost Key",
                                  "Ghost Ship Cubus Sisters Heart Container"],
        "set_if_true": [(0x1B557E, 0x10), (0x1B55AB, 0x10)],
        "unset_if_true": [(0x1B5582, 0x80)]
    },
    "RESET Respawn ghost ship": {
        "on_scenes": [0x1],
        "has_locations": ["Ghost Ship B1 Entrance Chest",
                          "Ghost Ship B1 Second Sister Chest",
                          "Ghost Ship B2 Third Sister Left Chest",
                          "Ghost Ship B2 Third Sister Right Chest",
                          "Ghost Ship B2 Spike Chest",
                          "Ghost Ship B3 Chest",
                          "Ghost Ship Cubus Sisters Ghost Key",
                          "Ghost Ship Cubus Sisters Heart Container",
                          "Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B5582, 0x80), (0x1B557E, 0x10), (0x1B55AB, 0x10)]
    },
    "Yellow Guy moves after ghost ship": {
        "on_scenes": [0xB03],
        "unset_if_true": [(0x1B5582, 0x80)]
    },
    "RESET yellow guy fog to settings": {
        "on_scenes": [0x0],
        "has_slot_data": [("fog_settings", 0)],
        "set_if_true": [(0x1B5582, 0x80)]
    },
    "RESET yellow guy beat gs": {
        "on_scenes": [0x0],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "unset_if_true": [(0x1B5582, 0x80)]
    },
    "Spawn swift phantoms, despawn oshus on Molida": {
        "on_scenes": [0x2600, 0xC00],
        "set_if_true": [(0x1B557E, 0x10)]
    },
    "Remove Spirit flag": {
        "on_scenes": [0x0],
        "has_slot_data": [["fog_settings", 0]],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "unset_if_true": [(0x1B557E, 0x10)]
    },
    "Remove Spirit flag 2": {
        "on_scenes": [0x0],
        "has_slot_data": [["fog_settings", 1]],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "unset_if_true": [(0x1B557E, 0x10)]
    },

    # Goron Chief
    "Beat goron temple goron chief": {
        "on_scenes": [0x100A],
        "not_has_locations": ["Goron Island Chief Post Dungeon Item"],
        "unset_if_true": [(0x1B5593, 0x2)]
    },
    "Beat goron temple goron chief metal": {
        "on_scenes": [0x100A],
        "not_has_locations": ["Goron Island Chief Post Dungeon Item"],
        "has_locations": ["Goron Temple Dongorongo Dungeon Reward", "Goron Island Goron Quiz"],
        "set_if_true": [(0x1B558B, 0x40)]
    },
    "RESET Beat goron temple goron chief metal": {
        "on_scenes": [0x1003],
        "not_has_items": [("Crimzonine", 1)],
        "unset_if_true": [(0x1B558B, 0x40)]
    },
    "RESET Beat goron temple goron chief": {
        "on_scenes": [0x1003],
        "set_if_true": [(0x1B5593, 0x2)]
    },
    "Play goron game on dee ess after temple": {
        "on_scenes": [0x1B00],
        "has_locations": ["Goron Temple Dongorongo Dungeon Reward"],
        "set_if_true": [(0x1B5597, 0x20)]
    },

    # Harrow Island
    "Harrow island Map 1": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 1"],
        "unset_if_true": [(0x1BA652, 0x1)]
    },
    "Harrow island Map 1 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 1"],
        "set_if_true": [(0x1BA652, 0x1)]
    },
    "Harrow island Map 2": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 2"],
        "unset_if_true": [(0x1BA652, 0x2)]
    },
    "Harrow island Map 2 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 2"],
        "set_if_true": [(0x1BA652, 0x2)]
    },
    "Harrow island Map 3": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 3"],
        "unset_if_true": [(0x1BA653, 2)]
    },
    "Harrow island Map 3 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 3"],
        "set_if_true": [(0x1BA653, 2)]
    },
    "Harrow island Map 4": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 4"],
        "unset_if_true": [(0x1BA653, 4)]
    },
    "Harrow island Map 4 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 4"],
        "set_if_true": [(0x1BA653, 4)]
    },
    "RESET Harrow island Map 1": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #14", 1)],
        "set_if_true": [(0x1BA652, 0x1)]
    },
    "RESET Harrow island Map 1 got": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #14", 0)],
        "unset_if_true": [(0x1BA652, 0x1)]
    },
    "RESET Harrow island Map 2": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #15", 1)],
        "set_if_true": [(0x1BA652, 0x2)]
    },
    "RESET Harrow island Map 2 got": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #15", 0)],
        "unset_if_true": [(0x1BA652, 0x2)]
    },
    "RESET Harrow island Map 3": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #24", 1)],
        "set_if_true": [(0x1BA653, 2)]
    },
    "RESET Harrow island Map 3 got": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #24", 0)],
        "unset_if_true": [(0x1BA653, 2)]
    },
    "RESET Harrow island Map 4": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #25", 1)],
        "set_if_true": [(0x1BA653, 0x4)]
    },
    "RESET Harrow island Map 4 got": {
        "on_scenes": [0x2],
        "has_items": [("Treasure Map #25", 0)],
        "unset_if_true": [(0x1BA653, 0x4)]
    },
    "Harrow have NE sea chart": {
        "on_scenes": [0x1800],
        "has_items": [("NE Sea Chart", 1)],
        "set_if_true": [(0x1B557D, 0x10)]
    },
    "Harrow not have NE sea chart": {
        "on_scenes": [0x1800],
        "has_items": [("NE Sea Chart", 0)],
        "unset_if_true": [(0x1B557D, 0x10)]
    },
    "SE spawn pirate ship": {
        "on_scenes": [0x2, 0x3],
        "not_has_locations": ["Ocean Pirate Ambush Item"],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B5582, 0x80), (0x1B55AB, 0x10)]
    },
    "SE despawn pirate ship": {
        "on_scenes": [0x2, 0x3],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "unset_if_true": [(0x1B5582, 0x80), (0x1B55AB, 0x10)]
    },

    # Zauz
    "Zauz remove phantom blade": {
        "on_scenes": [0x160A],
        "not_has_locations": ["Zauz's Island Phantom Blade"],
        "unset_if_true": [(0x1B5592, 0x20)]
    },
    "RESET Zauz remove phantom blade": {
        "on_scenes": [0x1600],
        "has_items": [("Phantom Blade", 1)],
        "set_if_true": [(0x1B5592, 0x20)]
    },
    "Zauz remove triforce crest": {
        "on_scenes": [0x160A],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "unset_if_true": [(0x1B55AB, 0x10), (0x1B5580, 2), (0x1B5582, 0x80)]
    },
    "Zauz add triforce crest": {
        "on_scenes": [0x160A],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B55AB, 0x10), (0x1B5580, 2), (0x1B5582, 0x80)]
    },
    "RESET Zauz remove triforce crest": {
        "on_scenes": [0x1600],
        "has_items": [("Triforce Crest", 1)],
        "set_if_true": [(0x1B5580, 2)]
    },
    "RESET add triforce crest": {
        "on_scenes": [0x1600],
        "has_items": [("Triforce Crest", 0)],
        "unset_if_true": [(0x1B5580, 2)]
    },
    "RESET Zauz remove triforce crest fog": {
        "on_scenes": [0x1600],
        "has_slot_data": [("fog_settings", 0)],
        "set_if_true": [(0x1B55AB, 0x10), (0x1B5582, 0x80)]
    },
    # Jolene
    "Remove Jolene": {
        "on_scenes": [0x0],
        "unset_if_true": [(0x1B557F, 0x80)]
    },
    "RESET Remove Jolene": {
        "on_scenes": [0xC00],
        "has_locations": ["Temple of Courage Crayk Dungeon Reward"],
        "set_if_true": [(0x1B557F, 0x80)]
    },
    # Dungeons and metals
    "Goron temple metals": {
        "on_scenes": [0x2000],
        "unset_if_true": [(0x1B558B, 0x40)]
    },
    "RESET Goron temple metals": {
        "on_scenes": [0x1000],
        "has_items": [("Crimzonine", 1)],
        "set_if_true": [(0x1B558B, 0x40)]
    },
    "Tce temple metals": {
        "on_scenes": [0x1F00],
        "unset_if_true": [(0x1B558B, 0x20)]
    },
    "RESET Ice temple metals": {
        "on_scenes": [0xF01],
        "has_items": [("Azurine", 1)],
        "set_if_true": [(0x1B558B, 0x20)]
    },
    "Mutoh temple metals": {
        "on_scenes": [0x2106, 0x2100],
        "unset_if_true": [(0x1B558B, 0x80)]
    },
    "RESET Mutoh temple metals": {
        "on_scenes": [0x1202],
        "has_items": [("Aquanine", 1)],
        "set_if_true": [(0x1B558B, 0x80)]
    },
    # Oshus Items
    "Block phantom sword crafting": {
        "on_scenes": [0xB0A],
        "has_items": [("Phantom Blade", 0)],
        "not_has_locations": ["Mercay Oshus Phantom Sword"],
        "unset_if_true": [(0x1B5592, 0x20), (0x1BA648, 0x20)]
    },
    "RESET Block phantom sword crafting": {
        "on_scenes": [0xB00],
        "has_items": [("Sword (Progressive)", 2)],
        "set_if_true": [(0x1BA648, 0x20)]
    },
    "Block Oshus Gem": {
        "on_scenes": [0xB0A],
        "not_has_locations": ["Temple of Wind Cyclok Dungeon Reward"],
        "unset_if_true": [(0x1B55A0, 0x4), (0x1B557D, 0x2)]
    },
    "RESET Block Oshus Gem": {
        "on_scenes": [0xB00],
        "has_locations": ["TotOK Phantom Hourglass"],
        "set_if_true": [(0x1B55A0, 0x4)]
    },
    "Oshus Gem": {
        "on_scenes": [0xB0A],
        "not_has_locations": ["Mercay Oshus Item After Temple of Wind"],
        "has_locations": ["Temple of Wind Cyclok Dungeon Reward"],
        "set_if_true": [(0x1B55A0, 0x4), (0x1B557D, 0x2)]
    },
    "RESET Oshus Gem hourglass": {
        "on_scenes": [0xB00],
        "not_has_locations": ["TotOK Phantom Hourglass"],
        "unset_if_true": [(0x1B55A0, 0x4)]
    },
    "RESET Oshus Gem chart": {
        "on_scenes": [0xB00],
        "unset_if_true": [(0x1B557D, 0x2)]
    },
    # Trade Quest
    "PoRL Trade Quest": {
        "on_scenes": [0x700],
        "not_has_locations": ["Ocean NW Prince of Red Lions Trade Quest Item"],
        "unset_if_true": [(0x1B5590, 0x98), (0x1BA649, 0x20)]
    },
    "Nyave Trade Quest": {
        "on_scenes": [0xA00],
        "not_has_locations": ["Ocean NW Prince of Red Lions Trade Quest Item"],
        "unset_if_true": [(0x1B5590, 0x80), (0x1BA649, 0x20)]
    },
    "Hoiger Trade Quest": {
        "on_scenes": [0x900],
        "not_has_locations": ["Ocean NW Prince of Red Lions Trade Quest Item"],
        "unset_if_true": [(0x1B5590, 0x90), (0x1BA649, 0x20)]
    },
    "Wayfarer Trade Quest": {
        "on_scenes": [0x800],
        "not_has_locations": ["Ocean NW Prince of Red Lions Trade Quest Item"],
        "unset_if_true": [(0x1BA649, 0x20)]
    },
    "RESET Swordsmans Scroll": {
        "on_scenes": [0x0, 0x1, 0x2, 0x3],
        "has_items": [("Swordsman's Scroll", 1)],
        "set_if_true": [(0x1BA649, 0x20)]
    },
    "RESET Wood Heart": {
        "on_scenes": [0x0, 0x1, 0x2, 0x3],
        "has_items": [("Wood Heart", 1)],
        "not_has_locations": ["Bannan Island Wayfarer Trade Quest Chest"],
        "set_if_true": [(0x1B5590, 0x80)]
    },
    "RESET Guard Notebook": {
        "on_scenes": [0x0, 0x1, 0x2, 0x3],
        "has_items": [("Guard Notebook", 1)],
        "not_has_locations": ["Ocean SW Nyave Trade Quest Item"],
        "set_if_true": [(0x1B5590, 0x10)]
    },
    "RESET Kaleidoscope": {
        "on_scenes": [0x1, 0x2, 0x3],
        "has_items": [("Guard Notebook", 1)],
        "not_has_locations": ["Ocean SE Hoiger Howgendoogen Trade Quest Item"],
        "set_if_true": [(0x1B5590, 0x8)]
    },
    # Ghost Ship HC
    "Ghost Ship HC": {
        "on_scenes": [0x2903],
        "not_has_locations": ["Ghost Ship Cubus Sisters Heart Container"],
        "unset_if_true": [(0x1B55AB, 0x8)]
    },
    "RESET Ghost Ship HC": {
        "on_scenes": [0x1],
        "set_if_true": [(0x1B55AB, 0x8)]
    },
    # Vanilla frogs
    "Frogs show glyph": {
        "on_scenes": [0, 0x1],
        "set_if_true": [(0x1B55A2, 0x40)]
    },
    "RESET Frogs show glyph": {
        "on_scenes": [0x1A00],
        "not_has_locations": ["Uncharted Island Cyclone Slate"],
        "unset_if_true": [(0x1B55A2, 0x40)]
    },
    # Mountain Passage anti-softlock
    "Give Anti-softlock bombs": {
        "on_scenes": [0xB01],
        "not_last_scenes": [0xB00, 0x2600, 0xB02, 0xB10],
        "has_items": [("Bombs (Progressive)", 0)],
        "set_if_true": [(0x1BA644, 0x10), (0x1BA6C0, 1)]
    },
    "RESET Anti-softlock bombs": {
        "on_scenes": [0xB00, 0x2700],
        "has_items": [("Bombs (Progressive)", 0)],
        "unset_if_true": [(0x1BA644, 0x10)]
    },
    # Doyland
    "Doyland has lowered water": {
        "on_scenes": [0x2201],
        "check_bits": {0x1B5582: 0x4},
        "unset_if_true": [(0x1B5582, 0x4)],
        "set_if_true": [(0x1B5590, 0x02)]  # Water state memory
    },
    "Doyland memory bit": {
        "on_scenes": [0x2200],
        "not_last_scenes": [0x2201],
        "unset_if_true": [(0x1B5590, 0x02)],  # Memory of water
    },
    "RESET Doyland has lowered water": {
        "on_scenes": [0x2200],
        "not_last_scenes": [0x1102, 0x1202],
        "check_bits": {0x1B5590: 0x02},  # Memory of water level
        "set_if_true": [(0x1B5582, 0x4)],  # Water level
        "unset_if_true": [(0x1B5590, 0x02)],
    },
    "RESET Doyland memory bit": {
        "on_scenes": [0x1102, 0x1202],
        "set_if_true": [(0x1B5590, 0x02)],  # Memory of water
    },
    "Ice Field pre-dungeon": {
        "on_scenes": [0xF03],
        "not_has_locations": ["Temple of Ice Dungeon Reward"],
        "unset_bits": [(0x1B558B, 0x20)]
    },
    "Ice Field post-dungeon": {
        "on_scenes": [0xF03],
        "has_locations": ["Temple of Ice Dungeon Reward"],
        "set_bits": [(0x1B558B, 0x20)]
    },
    "RESET Ice Field pre-dungeon": {
        "on_scenes": [0xF13, 0xF01],
        "has_items": [("Azurine", 1)],
        "set_bits": [(0x1B558B, 0x20)]
    },
    "RESET Ice Field post-dungeon": {
        "on_scenes": [0xF13, 0xF01],
        "has_items": [("Azurine", 0)],
        "unset_bits": [(0x1B558B, 0x20)]
    },
}

