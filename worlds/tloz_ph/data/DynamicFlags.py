"""
"Dynamic Flag Name": {
    "on_scenes": list[int],
    "not_last_scenes": list[int],
    "has_items": list[tuple[str, int]],         item_name, min count (0 for not have item)
    "has_locations": list[str],
    "not_has_locations": list[str],
    "any_not_has_locations": list[str],
    "set_if_true": list[tuple[int, int or str]],       address, value (if value is an item name, value becomes the
    "unset_if_true": list[tuple[int, int]],     address, value
    "has_slot_data": list[list[str, any]]       slot_data, ==value
    "goal_requirement": bool                    checks dungeon requirement if true
}
"""
DYNAMIC_FLAGS = {
    # Treasure Maps don't spawn if you have them in your inventory, remove from inventory on scenes with maps, and give
    # them back on the next scene
    "Astrid's Basement Treasure Map": {
        "on_scenes": [0xD14],
        "not_has_locations": ["Isle of Ember Astrid's Basement Dig"],
        "unset_if_true": [(0x1BA651, 0x20)],
        "reset_flags": ["RESET Astrid's Basement Treasure Map"]
    },
    "RESET Astrid's Basement Treasure Map": {
        # "on_scenes": [0xD0A],
        "has_items": [("Treasure Map #3 (Gusts SW)", 1)],
        "set_if_true": [(0x1BA651, 0x20)]
    },
    "Ember summit treasure map": {
        "on_scenes": [0xD01],
        "not_has_locations": ["Isle of Ember Summit Dig"],
        "unset_if_true": [(0x1BA651, 0x80)],
        "reset_flags": ["RESET Ember summit treasure map"]
    },
    "RESET Ember summit treasure map": {
        # "on_scenes": [0xD00, 0x1C0],
        "has_items": [("Treasure Map #4 (Bannan SE)", 1)],
        "set_if_true": [(0x1BA651, 0x80)]
    },
    "Mercay yellow guy treasure map": {
        "on_scenes": [0xB03],
        "not_has_locations": ["Mercay Ojibe (Docks Guy) Item"],
        "unset_if_true": [(0x1BA650, 0x02)],
        "reset_flags": ["RESET Mercay yellow guy treasure map"]
    },
    "RESET Mercay yellow guy treasure map": {
        # "on_scenes": [0x000, 0xB00, 0xB02, 0xB0C, 0xB0D, 0xB0E, 0xB0F, 0xB11, 0x2701],
        "has_items": [("Treasure Map #9 (Cannon W)", 1)],
        "set_if_true": [(0x1BA650, 0x02)]
    },
    "Mercay freedle gift treasure map": {
        "on_scenes": [0xB02],
        "not_has_locations": ["Mercay Freedle Gift Item"],
        "unset_if_true": [(0x1BA652, 0x20)],
        "reset_flags": ["RESET Mercay freedle gift treasure map"]
    },
    "RESET Mercay freedle gift treasure map": {
        # "on_scenes": [0xB01, 0xB03, 0xB12],
        "has_items": [("Treasure Map #12 (Dee Ess N)", 1)],
        "set_if_true": [(0x1BA652, 0x20)]
    },
    "Mercay oshus dig treasure map": {
        "on_scenes": [0xB00],
        "not_has_locations": ["Mercay Oshus Dig"],
        "unset_if_true": [(0x1BA651, 0x10)],
        "reset_flags": ["RESET Mercay oshus dig treasure map"]
    },
    "RESET Mercay oshus dig treasure map": {
        # "on_scenes": [0xB01, 0xB03, 0xB13, 0xB01, 0xB0A, 0xB0B],
        "has_items": [("Treasure Map #10 (Gusts SE)", 1)],
        "set_if_true": [(0x1BA651, 0x10)]
    },
    "Molida Cuccoo dig map": {
        "on_scenes": [0xC00],
        "not_has_locations": ["Molida Island Cuccoo Grapple Tree Dig"],
        "unset_if_true": [(0x1BA651, 0x40)],
        "reset_flags": ["RESET Molida Cuccoo dig map"]
    },
    "RESET Molida Cuccoo dig map": {
        # "on_scenes": [0x000, 0xC01, 0xC0A, 0xC0B, 0xC0C,  0xC0D, 0xC0E,],
        "has_items": [("Treasure Map #20 (Bannan E)", 1)],
        "set_if_true": [(0x1BA651, 0x40)]
    },
    "Zauz Map": {
        "on_scenes": [0x1600],
        "not_has_locations": ["Zauz's Island Secret Dig"],
        "unset_if_true": [(0x1BA650, 0x40)],
        "reset_flags": ["RESET Zauz Map"]
    },
    "RESET Zauz Map": {
        # "on_scenes": [0x1],
        "has_items": [("Treasure Map #5 (Molida N)", 1)],
        "set_if_true": [(0x1BA650, 0x40)]
    },
    "Uncharted Island Map": {
        "on_scenes": [0x1A00],
        "not_has_locations": ["Uncharted Island Eye Dig"],
        "unset_if_true": [(0x1BA651, 0x1)],
        "reset_flags": ["RESET Uncharted Island Map"]
    },
    "RESET Uncharted Island Map": {
        # "on_scenes": [0x1],
        "has_items": [("Treasure Map #6 (Bannan W)", 1)],
        "set_if_true": [(0x1BA651, 0x1)]
    },
    "Frost Island Map": {
        "on_scenes": [0xF02],
        "not_has_locations": ["Isle of Frost Estate SW Island Dig"],
        "unset_if_true": [(0x1BA651, 0x4)],
        "reset_flags": ["RESET Frost Island Map"]
    },
    "RESET Frost Island Map": {
        # "on_scenes": [0xF00],
        "has_items": [("Treasure Map #19 (Gusts NE)", 1)],
        "set_if_true": [(0x1BA651, 0x4)]
    },
    "Bannan Wayfarer Map": {
        "on_scenes": [0x1400],
        "not_has_locations": ["Bannan Island Wayfarer Dig"],
        "unset_if_true": [(0x1BA650, 0x20)],
        "reset_flags": ["RESET Bannan Wayfarer Map"]
    },
    "RESET Bannan Wayfarer Map": {
        # "on_scenes": [0x1],
        "has_items": [("Treasure Map #21 (Molida NW)", 1)],
        "set_if_true": [(0x1BA650, 0x20)]
    },
    "Bannan Island Map": {
        "on_scenes": [0x1400],
        "not_has_locations": ["Bannan Island East Grapple Dig"],
        "unset_if_true": [(0x1BA652, 0x8)],
        "reset_flags": ["RESET Bannan Island Map"]
    },
    "RESET Bannan Island Map": {
        # "on_scenes": [0x1],
        "has_items": [("Treasure Map #22 (Harrow S)", 1)],
        "set_if_true": [(0x1BA652, 0x8)]
    },
    "Rupoor cave map": {
        "on_scenes": [0x1502],
        "not_has_locations": ["Isle of the Dead Rupoor Cave 2"],
        "unset_if_true": [(0x1BA653, 0x1)],
        "reset_flags": ["RESET Rupoor cave map"]
    },
    "RESET Rupoor cave map": {
        # "on_scenes": [0x1501],
        "has_items": [("Treasure Map #28 (Ruins NW)", 1)],
        "set_if_true": [(0x1BA653, 0x1)]
    },
    "Goron Chu Map": {
        "on_scenes": [0x1002],
        "not_has_locations": ["Goron Island Yellow Chu Item"],
        "unset_if_true": [(0x1ba652, 0x10)],
        "reset_flags": ["RESET Goron Chu Map"]
    },
    "RESET Goron Chu Map": {
        "has_items": [("Treasure Map #16 (Goron NE)", 1)],
        "set_if_true": [(0x1ba652, 0x10)]
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
        "unset_if_true": [(0x1B5582, 0x1), (0x1B558D, 0x10)]
    },
    "Enter Cannon: Not Bought Salvage": {
        "on_scenes": [0x130B],
        "not_has_locations": ["Cannon Island Salvage Arm"],
        "has_locations": ["Cannon Island Cannon"],
        "set_if_true": [(0x1B5582, 0x1)],
        "unset_if_true": [(0x1BA649, 0x10), (0x1B558D, 0x10)]
    },
    "Exit Cannon": {
        "on_scenes": [0x130B],
        "reset_flags": ["Exit Cannon: Have Cannon", "Exit Cannon: Have Salvage",
                        "Exit Cannon: Not Have Cannon", "Exit Cannon: Not Have Salvage"]
    },
    "Exit Cannon: Have Cannon": {
        # "on_scenes": [0x1300, 0x130A],
        "has_items": [("Cannon", 1)],
        "set_if_true": [(0x1B5582, 0x1)]
    },
    "Exit Cannon: Have Salvage": {
        #"on_scenes": [0x1300, 0x130A],
        "has_items": [("Salvage Arm", 1)],
        "set_if_true": [(0x1BA649, 0x10), (0x1B558D, 0x10)]
    },
    "Exit Cannon: Not Have Cannon": {
        # "on_scenes": [0x1300, 0x130A],
        "has_items": [("Cannon", 0)],
        "unset_if_true": [(0x1B5582, 0x1)]
    },
    "Exit Cannon: Not Have Salvage": {
        # "on_scenes": [0x1300, 0x130A],
        "has_items": [("Salvage Arm", 0)],
        "unset_if_true": [(0x1BA649, 0x10), (0x1B558D, 0x10)]
    },
    "Cannon Open Door": {
        "on_scenes": [0x130B],
        "set_if_true": [(0x1B5582, 0x2)]
    },

    # Spirit Island
    "Spirit of Power 1": {
        "on_scenes": [0x1701],
        "not_has_locations": ["Spirit Island Power Upgrade Level 1"],
        "unset_if_true": [(0x1BA647, 0x9)],
    },
    "Spirit of Wisdom 1": {
        "on_scenes": [0x1701],
        "not_has_locations": ["Spirit Island Wisdom Upgrade Level 1"],
        "unset_if_true": [(0x1BA647, 0x12)],
    },
    "Spirit of Courage 1": {
        "on_scenes": [0x1701],
        "not_has_locations": ["Spirit Island Courage Upgrade Level 1"],
        "unset_if_true": [(0x1BA646, 0x80), (0x1BA647, 0x04)],
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
    "Always reset spirit island": {
        "on_scenes": [0x1701],
        "reset_flags": ["RESET Spirit of power 0", "RESET Spirit of power 1", "RESET Spirit of power 2",
                        "RESET Spirit of wisdom 0", "RESET Spirit of wisdom 1", "RESET Spirit of wisdom 2",
                        "RESET Spirit of courage 0", "RESET Spirit of courage 1", "RESET Spirit of courage 2",
                        "RESET Spirit of Wisdom boss flag", "RESET Spirit of Courage boss flag"]
    },
    "RESET Spirit of power 0": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Power (Progressive)", 1, "has_exact")],
        "unset_if_true": [(0x1BA647, 0x9)]
    },
    "RESET Spirit of power 1": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Power (Progressive)", 2, "has_exact")],
        "set_if_true": [(0x1BA647, 0x1)],
        "unset_if_true": [(0x1BA647, 0x8)]
    },
    "RESET Spirit of power 2": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Power (Progressive)", 3)],
        "set_if_true": [(0x1BA647, 0x9)]
    },
    "RESET Spirit of wisdom 0": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Wisdom (Progressive)", 1, "has_exact")],
        "unset_if_true": [(0x1BA647, 0x12)]
    },
    "RESET Spirit of wisdom 1": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Wisdom (Progressive)", 2, "has_exact")],
        "set_if_true": [(0x1BA647, 0x02)],
        "unset_if_true": [(0x1BA647, 0x10)]
    },
    "RESET Spirit of wisdom 2": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Wisdom (Progressive)", 3)],
        "set_if_true": [(0x1BA647, 0x12)]
    },
    "RESET Spirit of courage 0": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Courage (Progressive)", 1, "has_exact")],
        "unset_if_true": [(0x1BA646, 0x80), (0x1BA647, 0x04)]
    },
    "RESET Spirit of courage 1": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Courage (Progressive)", 2, "has_exact")],
        "set_if_true": [(0x1BA646, 0x80)],
        "unset_if_true": [(0x1BA647, 0x4)]
    },
    "RESET Spirit of courage 2": {
        # "on_scenes": [0x1700],
        "has_items": [("Spirit of Courage (Progressive)", 3)],
        "set_if_true": [(0x1BA646, 0x80), (0x1BA647, 0x04)]
    },
    "Spirit of Wisdom boss flag": {
        "on_scenes": [0x1701],
        "has_items": [("Spirit of Wisdom (Progressive)", 1)],
        "set_if_true": [(0x1B557F, 0x40)],
        "reset_flags": ["RESET Spirit of Wisdom boss flag"]
    },
    "Spirit of Courage boss flag": {
        "on_scenes": [0x1701],
        "has_items": [("Spirit of Courage (Progressive)", 1)],
        "set_if_true": [(0x1B557F, 0xC0)],
        "reset_flags": ["RESET Spirit of Wisdom boss flag", "RESET Spirit of Courage boss flag"]
    },
    "RESET Spirit of Wisdom boss flag": {
        # "on_scenes": [0x1700],
        "not_has_locations": ["Cyclok Boss Reward"],
        "unset_if_true": [(0x1B557F, 0x40)]
    },
    "RESET Spirit of Courage boss flag": {
        # "on_scenes": [0x1700],
        "not_has_locations": ["Crayk Boss Reward"],
        "unset_if_true": [(0x1B557F, 0x80)]
    },
    # Spirit Island cap spirit gems to 20 on enter
    "Power Gem cap": {
        "on_scenes": [0x1701],
        "has_items": [("Power Gem", 20)],
        "overwrite_if_true": [(0x1BA541, 0x14)],
        "reset_flags": ["RESET Power Gem cap"]
    },
    "Courage Gem cap": {
        "on_scenes": [0x1701],
        "has_items": [("Courage Gem", 20)],
        "overwrite_if_true": [(0x1BA542, 0x14)],
        "reset_flags": ["RESET Courage Gem cap"]
    },
    "Wisdom Gem cap": {
        "on_scenes": [0x1701],
        "has_items": [("Wisdom Gem", 20)],
        "overwrite_if_true": [(0x1BA540, 0x14)],
        "reset_flags": ["RESET Wisdom Gem cap"]
    },
    "Power Gem cap packs": {
        "on_scenes": [0x1701],
        "count_gems": "Power",
        "overwrite_if_true": [(0x1BA541, 0x14)],
    },
    "Courage Gem cap packs": {
        "on_scenes": [0x1701],
        "count_gems": "Courage",
        "overwrite_if_true": [(0x1BA542, 0x14)],
    },
    "Wisdom Gem cap packs": {
        "on_scenes": [0x1701],
        "count_gems": "Wisdom",
        "overwrite_if_true": [(0x1BA540, 0x14)],
    },
    "RESET Power Gem cap": {
        "overwrite_if_true": [(0x1BA541, "Power Gem")],
    },
    "RESET Courage Gem cap": {
        "overwrite_if_true": [(0x1BA542, "Courage Gem")]
    },
    "RESET Wisdom Gem cap": {
        "overwrite_if_true": [(0x1BA540, "Wisdom Gem")]
    },
    # Courage Crest Room
    "Courage Crest room not salvaged it": {
        "on_scenes": [0x2508],
        "has_locations": ["Ocean SW Salvage Courage Crest"],
        "unset_if_true": [(0x1B557E, 0x40)],
    },
    "Courage Crest room remove crest": {
        "on_scenes": [0x2508],
        "unset_if_true": [(0x1B558C, 0x04)],
        "not_has_locations": ["TotOK B6 Courage Crest"]
    },
    "Courage Crest room allow leaving": {
        "on_scenes": [0x2508],
        "has_locations": ["TotOK B6 Courage Crest"],
        "set_if_true": [(0x1B558C, 0x04)]
    },
    "Reset cc room": {
        "on_scenes": [0x2508],
        "reset_flags": ["RESET Courage Crest room not salvaged it", "RESET Courage Crest room remove crest",
                        "RESET Courage Crest room remove crest if not got it"]
    },
    "RESET Courage Crest room not salvaged it": {
        # "on_scenes": [0x2600, 0x2507],
        "has_locations": ["Ocean SW Salvage Courage Crest"],
        "set_if_true": [(0x1B557E, 0x40)]
    },
    "RESET Courage Crest room remove crest": {
        # "on_scenes": [0x2600, 0x2507],
        "has_items": [("Courage Crest", 1)],
        "set_if_true": [(0x1B558C, 0x04)]
    },
    "RESET Courage Crest room remove crest if not got it": {
        # "on_scenes": [0x2600, 0x2507],
        "has_items": [("Courage Crest", 0)],
        "unset_if_true": [(0x1B558C, 0x04)]
    },
    # Endgame
    "Spawn Phantoms in Totok B13": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "has_slot_data": [["bellum_access", 1]],
        "set_if_true": [(0x1B5592, 0x40)],
        "reset_flags": ["RESET Spawn Phantoms in Totok B13"]
    },
    "Spawn Phantoms in Totok B13 2": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "has_slot_data": [["bellum_access", 2]],
        "set_if_true": [(0x1B5592, 0x40)],
        "reset_flags": ["RESET Spawn Phantoms in Totok B13"]
    },
    "Spawn Phantoms in Totok B13 3": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "has_slot_data": [["bellum_access", 3]],
        "set_if_true": [(0x1B5592, 0x40)],
        "reset_flags": ["RESET Spawn Phantoms in Totok B13"]
    },
    "Spawn Phantoms in Totok B13 door option": {
        "on_scenes": [0x2511],
        "has_items": [("Sword (Progressive)", 2)],
        "goal_requirement": True,
        "has_slot_data": [["bellum_access", 0]],
        "set_if_true": [(0x1B5592, 0x40)],
        "reset_flags": ["RESET Spawn Phantoms in Totok B13"]
    },
    "RESET Spawn Phantoms in Totok B13": {
        # "on_scenes": [0x2600],
        "unset_if_true": [(0x1B5592, 0x40)]
    },
    "Block Bellum Staircase": {
        "on_scenes": [0x2600],
        "set_if_true": [(0x1B5595, 0x2)],
        # "reset_flags": ["RESET Block Bellum Staircase"]
    },
    "RESET Block Bellum Staircase": {
        # "on_scenes": [0xB01],
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
        "has_locations": ["TotOK Phantom Hourglass"]
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
    "Triforce Crest Rando safety": {
        "on_scenes": [0x2507],
        "set_if_true": [(0x1B5580, 0x2)],
        "has_slot_data": [["randomize_triforce_crest", 1]],
        "has_items": [("Triforce Crest", 1)]
    },

    # boat requires sea chart
    "Always Despawn Linebeck 1": {
        "on_scenes": [0xB03],
        "unset_if_true": [(0x1B557E, 0x8)]
    },
    "Always Spawn linebeck 2 setting": {
        "on_scenes": [0xB03],
        "has_slot_data": [["boat_requires_sea_chart", 0]],
        "set_if_true": [(0x1B5580, 0x4)],
    },
    "Always Spawn linebeck 2 port rando": {
        "on_scenes": [0xB03],
        "has_slot_data": [["boat_requires_sea_chart", 0], ["shuffle_island_entrances", 1]],
        "set_if_true": [(0x1B5580, 0x4)],
    },
    "Spawn Linebeck if setting": {
        "on_scenes": [0xB03],
        "has_slot_data": [["boat_requires_sea_chart", 1], ["shuffle_island_entrances", 0]],
        "has_items": [("SW Sea Chart", 1)],
        "set_if_true": [(0x1B5580, 0x4)],
    },
    "Despawn Linebeck if setting": {
        "on_scenes": [0xB03],
        "has_slot_data": [["boat_requires_sea_chart", 1], ["shuffle_island_entrances", 0]],
        "has_items": [("SW Sea Chart", 0)],
        "unset_if_true": [(0x1B5580, 0x4)],
    },
    "reset mercay": {
        "on_scenes": [0xB03],
        "reset_flags": ["RESET Despawn Linebeck setting", "RESET despawn linebeck 2",
                        "RESET yellow guy fog to settings", "RESET yellow guy beat gs"]
    },
    "RESET Despawn Linebeck setting": {
        # "on_scenes": [0xB02],
        "set_if_true": [(0x1B557E, 0x8)]
    },
    "RESET despawn linebeck 2": {
        # "on_scenes": [0xB02, 0xB00],
        "set_if_true": [(0x1B5580, 0x4)],
    },
    # Other linebeck settings
    "Mercay skip blow on map for Linebeck": {
        "on_scenes": [0xB03],
        "unset_if_true": [(0x1B557D, 0x2)]
    },
    "mercay Safety Shipyard": {
        "on_scenes": [0xB03],
        "has_locations": ["Blaaz Boss Reward"],
        "set_if_true": [(0x1B557F, 0x20)]
    },
    # Fog
    "No fog add fog if spirits": {
        "on_scenes": [0x01],
        "not_last_scenes": [0x2903],
        "not_on_entrance": [5],
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
        "not_on_entrance": [5],
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
        "on_scenes": [0x1],  # NW quadrant
        "not_last_scenes": [0x2903, 0x400],  # from ghost ship
        "not_on_entrance": [5],  # prevent respawning if coming from ghost ship
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "any_not_has_locations": ["Ghost Ship B1 Entrance Chest",
                                  "Ghost Ship B1 Second Sister Chest",
                                  "Ghost Ship B2 Third Sister Left Chest",
                                  "Ghost Ship B2 Third Sister Right Chest",
                                  "Ghost Ship B2 Spike Chest",
                                  "Ghost Ship B3 Chest",
                                  "Cubus Sisters Ghost Key",
                                  "Cubus Sisters Heart Container"],
        "has_slot_data": [("shuffle_dungeon_entrances", 0)],
        "set_if_true": [(0x1B557E, 0x10), (0x1B55AB, 0x10)],  # Spawn spirits, remove fog
        "unset_if_true": [(0x1B5582, 0x80)]  # Respawn ghost ship
    },
    "Always Respawn ghost ship with dungeon rando": {
        "on_scenes": [0x1],  # NW quadrant
        "not_on_entrance": [5],  # prevent respawning if coming from ghost ship
        "not_last_scenes": [0x2903, 0x400], # from ghost ship
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "has_slot_data": [("shuffle_dungeon_entrances", [1, 2])],
        "set_if_true": [(0x1B557E, 0x10), (0x1B55AB, 0x10)],  # Spawn spirits, remove fog
        "unset_if_true": [(0x1B5582, 0x80)],  # Respawn ghost ship
    },
    "Spawn ghost ship Open GS removed fog": {
        "on_scenes": [0x1],  # NW quadrant
        "not_on_entrance": [5],
        "has_slot_data": [("fog_settings", 2)],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B557E, 0x10)],  # Spawn spirits, remove fog
        "unset_if_true": [(0x1B5582, 0x80)],  # Respawn ghost ship
    },
    "Spawn ghost ship Open GS": {
        "on_scenes": [0x1],  # NW quadrant
        "has_slot_data": [("fog_settings", 2)],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B557E, 0x10)],  # Spawn spirits,
        "unset_if_true": [(0x1B5582, 0x80), (0x1B55AB, 0x10)],  # Respawn ghost ship, add fog
    },
    "Dungeon rando remove spirit from GS": {
        "on_scenes": [0x1],
        "on_entrance": [5],
        "unset_if_true": [(0x1B557E, 0x10)],
        "set_if_true": [(0x1B5582, 0x80), (0x1B55AB, 0x10)]
    },
    "Dungeon rando dummy spirit flag removal": {
        "on_scenes": [0x1],
        "reset_flags": ["Dungeon rando resest spirit flags"]
    },
    "Dungeon rando resest spirit flags": {
        "unset_if_true": [(0x1B557E, 0x10)],
        "set_if_true": [(0x1B5582, 0x80), (0x1B55AB, 0x10)]
    },
    "RESET Respawn ghost ship": {
        "on_scenes": [0x1],
        "has_locations": ["Ghost Ship B1 Entrance Chest",
                          "Ghost Ship B1 Second Sister Chest",
                          "Ghost Ship B2 Third Sister Left Chest",
                          "Ghost Ship B2 Third Sister Right Chest",
                          "Ghost Ship B2 Spike Chest",
                          "Ghost Ship B3 Chest",
                          "Cubus Sisters Ghost Key",
                          "Cubus Sisters Heart Container",
                          "Ghost Ship Rescue Tetra"],
        "has_slot_data": [("shuffle_dungeon_entrances", 0)],
        "set_if_true": [(0x1B5582, 0x80), (0x1B557E, 0x10), (0x1B55AB, 0x10)]
    },
    "Yellow Guy moves after ghost ship": {
        "on_scenes": [0xB03],
        "unset_if_true": [(0x1B5582, 0x80)]
    },
    "RESET yellow guy fog to settings": {
        # "on_scenes": [0x0],
        "has_slot_data": [("fog_settings", 0)],
        "set_if_true": [(0x1B5582, 0x80)]
    },
    "RESET yellow guy beat gs": {
        # "on_scenes": [0x0],
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
        "unset_if_true": [(0x1B5593, 0x2)],
        "reset_flags": ["RESET Beat goron temple goron chief"]
    },
    "Beat goron temple goron chief metal": {
        "on_scenes": [0x100A],
        "not_has_locations": ["Goron Island Chief Post Dungeon Item"],
        "has_locations": ["Dongorongo Boss Reward", "Goron Island Goron Quiz"],
        "set_if_true": [(0x1B558B, 0x40)],
        "reset_flags": ["RESET remove Crimzonine"]
    },
    "Goron Island Crimzonine": {
        "on_scenes": [0x1002, 0x1003],
        "unset_if_true": [(0x1B558B, 0x40)],
        "reset_flags": ["RESET give Crimzonine"]
    },
    "RESET remove Crimzonine": {
        # "on_scenes": [0x1003],
        "has_items": [("Crimzonine", 0)],
        "unset_if_true": [(0x1B558B, 0x40)]
    },
    "RESET give Crimzonine": {
        # "on_scenes": [0x1003],
        "has_items": [("Crimzonine", 1)],
        "set_if_true": [(0x1b558B, 0x40)]
    },
    "RESET Beat goron temple goron chief": {
        # "on_scenes": [0x1003],
        "set_if_true": [(0x1B5593, 0x2)]
    },
    "Play goron game on dee ess after temple": {
        "on_scenes": [0x1B00],
        "has_locations": ["Dongorongo Boss Reward"],
        "set_if_true": [(0x1B5597, 0x20)]
    },

    # Harrow Island
    "Harrow island Map 1": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 1"],
        "unset_if_true": [(0x1BA652, 0x1)],
        "reset_flags": ["RESET Harrow island Map 1"]
    },
    "Harrow island Map 1 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 1"],
        "set_if_true": [(0x1BA652, 0x1)],
        "reset_flags": ["RESET Harrow island Map 1 got"]
    },
    "Harrow island Map 2": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 2"],
        "unset_if_true": [(0x1BA652, 0x2)],
        "reset_flags": ["RESET Harrow island Map 2"]
    },
    "Harrow island Map 2 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 2"],
        "set_if_true": [(0x1BA652, 0x2)],
        "reset_flags": ["RESET Harrow island Map 2 got"]
    },
    "Harrow island Map 3": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 3"],
        "unset_if_true": [(0x1BA653, 2)],
        "reset_flags": ["RESET Harrow island Map 3"]
    },
    "Harrow island Map 3 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 3"],
        "set_if_true": [(0x1BA653, 2)],
        "reset_flags": ["RESET Harrow island Map 3 got"]
    },
    "Harrow island Map 4": {
        "on_scenes": [0x1800],
        "not_has_locations": ["Harrow Island Dig 4"],
        "unset_if_true": [(0x1BA653, 4)],
        "reset_flags": ["RESET Harrow island Map 4"]
    },
    "Harrow island Map 4 got": {
        "on_scenes": [0x1800],
        "has_locations": ["Harrow Island Dig 4"],
        "set_if_true": [(0x1BA653, 4)],
        "reset_flags": ["RESET Harrow island Map 4 got"]
    },
    "RESET Harrow island Map 1": {
        # "on_scenes": [0x2],
        "has_items": [("Treasure Map #14 (Goron NW)", 1)],
        "set_if_true": [(0x1BA652, 0x1)]
    },
    "RESET Harrow island Map 1 got": {
        # "on_scenes": [0x2],
        "has_items": [("Treasure Map #14 (Goron NW)", 0)],
        "unset_if_true": [(0x1BA652, 0x1)]
    },
    "RESET Harrow island Map 2": {
        #"on_scenes": [0x2],
        "has_items": [("Treasure Map #15 (Goron W)", 1)],
        "set_if_true": [(0x1BA652, 0x2)]
    },
    "RESET Harrow island Map 2 got": {
        # "on_scenes": [0x2],
        "has_items": [("Treasure Map #15 (Goron W)", 0)],
        "unset_if_true": [(0x1BA652, 0x2)]
    },
    "RESET Harrow island Map 3": {
        # "on_scenes": [0x2],
        "has_items": [("Treasure Map #24 (Ruins W)", 1)],
        "set_if_true": [(0x1BA653, 2)]
    },
    "RESET Harrow island Map 3 got": {
        # "on_scenes": [0x2],
        "has_items": [("Treasure Map #24 (Ruins W)", 0)],
        "unset_if_true": [(0x1BA653, 2)]
    },
    "RESET Harrow island Map 4": {
        # "on_scenes": [0x2],
        "has_items": [("Treasure Map #25 (Dead E)", 1)],
        "set_if_true": [(0x1BA653, 0x4)]
    },
    "RESET Harrow island Map 4 got": {
        # "on_scenes": [0x2],
        "has_items": [("Treasure Map #25 (Dead E)", 0)],
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
        "not_has_locations": ["Ocean Miniblin Pirate Ambush Item"],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B557E, 0x10), (0x1B5582, 0x80), (0x1B55AB, 0x10)]
    },
    "SE despawn pirate ship": {
        "on_scenes": [0x2, 0x3],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "unset_if_true": [(0x1B557E, 0x10), (0x1B5582, 0x80), (0x1B55AB, 0x10)]

    },

    # Zauz
    "Zauz remove phantom blade": {
        "on_scenes": [0x160A],
        "not_has_locations": ["Zauz's Island Phantom Blade"],
        "unset_if_true": [(0x1B5592, 0x20)],
        "reset_flags": ["RESET Zauz remove phantom blade"]
    },
    "RESET Zauz remove phantom blade": {
        # "on_scenes": [0x1600],
        "has_items": [("Phantom Blade", 1)],
        "set_if_true": [(0x1B5592, 0x20)]
    },
    "Zauz remove triforce crest": {
        "on_scenes": [0x160A],
        "not_has_locations": ["Ghost Ship Rescue Tetra"],
        "unset_if_true": [(0x1B55AB, 0x10), (0x1B5580, 2), (0x1B5582, 0x80)],
        "reset_flags": ["RESET Zauz remove triforce crest"]
    },
    "Zauz add triforce crest": {
        "on_scenes": [0x160A],
        "has_locations": ["Ghost Ship Rescue Tetra"],
        "set_if_true": [(0x1B55AB, 0x10), (0x1B5580, 2), (0x1B5582, 0x80)],
        "reset_flags": ["RESET add triforce crest"]
    },
    "RESET Zauz remove triforce crest": {
        # "on_scenes": [0x1600],
        "has_items": [("Triforce Crest", 1)],
        "set_if_true": [(0x1B5580, 2)]
    },
    "RESET add triforce crest": {
        # "on_scenes": [0x1600],
        "has_items": [("Triforce Crest", 0)],
        "unset_if_true": [(0x1B5580, 2)]
    },
    "RESET Zauz remove triforce crest fog": {
        "on_scenes": [0x1600],
        "has_slot_data": [("fog_settings", 0)],
        "set_if_true": [(0x1B55AB, 0x10), (0x1B5582, 0x80)]
    },
    "Zauz remove oshus flag": {
        "on_scenes": [0x160A],
        "has_locations": ["Mercay Oshus Phantom Sword"],
        "unset_if_true": [(0x1B5592, 0x40)],
        "reset_flags": ["RESET Zauz remove oshus flag"]
    },
    "RESET Zauz remove oshus flag": {
        # "on_scenes": [0x1600],
        "has_locations": ["Mercay Oshus Phantom Sword"],
        "set_if_true": [(0x1B5592, 0x40)]
    },
    # Jolene
    "Remove Jolene": {
        "on_scenes": [0x0],
        "unset_if_true": [(0x1B557F, 0x80)],
        "reset_flags": ["RESET Remove Jolene"]
    },
    "RESET Remove Jolene": {
        # "on_scenes": [0xC00],
        "has_locations": ["Crayk Boss Reward"],
        "set_if_true": [(0x1B557F, 0x80)]
    },
    "Zauz has enough metals": {
        "on_scenes": [0x160A],
        "zauz_metals": True,
        "set_if_true": [(0x1B55A0, 0x10), (0x1B558C, 1)]
    },
    "Zauz not has enough metals": {
        "on_scenes": [0x160A],
        "zauz_metals": False,
        "unset_if_true": [(0x1B55A0, 0x10), (0x1B558C, 1)]
    },
    # Dungeons and metals
    "Goron temple metals": {
        "on_scenes": [0x2000, 0x2E00, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006],
        "unset_if_true": [(0x1B558B, 0x40)],
        "reset_flags": ["RESET Goron temple metals"]
    },
    "RESET Goron temple metals": {
        # "on_scenes": [0x1000],
        "has_items": [("Crimzonine", 1)],
        "set_if_true": [(0x1B558B, 0x40)]
    },
    "Ice temple metals": {
        "on_scenes": [0x1F00, 0x1F03, 0x1F06],
        "unset_if_true": [(0x1B558B, 0x20)],
        "reset_flags": ["RESET Ice Field pre-dungeon",
                        "RESET Ice Field post-dungeon"]
    },
    "Mutoh temple metals": {
        "on_scenes": [0x2106, 0x2100],
        "unset_if_true": [(0x1B558B, 0x80)],
        "reset_flags": ["RESET Mutoh temple metals"]
    },
    "RESET Mutoh temple metals": {
        # "on_scenes": [0x1202],
        "has_items": [("Aquanine", 1)],
        "set_if_true": [(0x1B558B, 0x80)]
    },
    # Oshus Items
    "Block phantom sword crafting blade": {
        "on_scenes": [0xB0A],
        "has_items": [("Phantom Blade", 0)],
        "not_has_locations": ["Mercay Oshus Phantom Sword"],
        "unset_if_true": [(0x1B5592, 0x20), (0x1BA648, 0x20)]
    },
    "Block phantom sword crafting ph": {
        "on_scenes": [0xB0A],
        "has_items": [("Phantom Hourglass", 0)],
        "not_has_locations": ["Mercay Oshus Phantom Sword"],
        "unset_if_true": [(0x1B5592, 0x20), (0x1BA648, 0x20)]
    },
    "Reset Oshus": {
        "on_scenes": [0xB0A],
        "reset_flags": ["RESET Block phantom sword crafting",
                        "RESET Oshus have phantom sword",
                        "Oshus not have phantom sword",
                        "RESET Block Oshus Gem", "RESET Oshus Gem hourglass",
                        "RESET Oshus Gem chart",
                        "RESET Oshus Wind Temple"]
    },
    "RESET Block phantom sword crafting": {
        # "on_scenes": [0xB00],
        "has_items": [("Sword (Progressive)", 2)],
        "set_if_true": [(0x1BA648, 0x20)]
    },
    "Oshus not have phantom sword": {
        # "on_scenes": [0xB00],
        "has_items": [("Sword (Progressive)", 2, "not_has")],
        "unset_if_true": [(0x1BA648, 0x20)],
    },
    "Oshus have phantom sword": {
        "on_scenes": [0xB0A],
        "has_items": [("Sword (Progressive)", 2)],
        "not_has_locations": ["Mercay Oshus Phantom Sword"],
        "unset_if_true": [(0x1BA648, 0x20)]
    },
    "RESET Oshus have phantom sword": {
        # "on_scenes": [0xB00],
        "has_items": [("Sword (Progressive)", 2)],
        "set_if_true": [(0x1BA648, 0x20)]
    },
    "Block Oshus Gem": {
        "on_scenes": [0xB0A],
        "not_has_locations": ["Cyclok Boss Reward"],
        "unset_if_true": [(0x1B55A0, 0x4), (0x1B557D, 0x2)]
    },
    "RESET Block Oshus Gem": {
        # "on_scenes": [0xB00],
        "has_locations": ["TotOK Phantom Hourglass"],
        "set_if_true": [(0x1B55A0, 0x4)]
    },
    "Oshus Gem": {
        "on_scenes": [0xB0A],
        "not_has_locations": ["Mercay Oshus Spirit Gem"],
        "has_locations": ["Cyclok Boss Reward"],
        "set_if_true": [(0x1B55A0, 0x4), (0x1B557D, 0x2), (0x1B557F, 0x40)]
    },
    "RESET Oshus Gem hourglass": {
        # "on_scenes": [0xB00],
        "not_has_locations": ["TotOK Phantom Hourglass"],
        "unset_if_true": [(0x1B55A0, 0x4)]
    },
    "RESET Oshus Gem chart": {
        # "on_scenes": [0xB00],
        "unset_if_true": [(0x1B557D, 0x2)]
    },
    "RESET Oshus Wind Temple": {
        # "on_scenes": [0xB00],
        "not_has_locations": ["Cyclok Boss Reward"],
        "unset_if_true": [(0x1B557F, 0x40)]
    },
    "Oshus absent backup gem": {
        "on_scenes": [0xB0A],
        "has_locations": ["Cyclok Boss Reward", "Blaaz Boss Reward"],
        "set_if_true": [(0x1b55a5, 0x2)]
    },
    "Oshus absent backup sword": {
        "on_scenes": [0xB0A],
        "has_items": [("Phantom Hourglass", 1), ("Phantom Blade", 1)],
        "has_locations": ["Blaaz Boss Reward"],
        "set_if_true": [(0x1b55a5, 0x2), (0x1ba648, 0x20)]
    },
    # Trade Quest
    "PoRL Trade Quest": {
        "on_scenes": [0x700],
        "not_has_locations": ["Ocean NW Prince of Red Lions Trade Quest Item"],
        "unset_if_true": [(0x1B5590, 0x98), (0x1BA649, 0x20)],
        "reset_flags": ["RESET Swordsmans Scroll", "RESET Guard Notebook", "RESET Kaleidoscope", "RESET Wood Heart"]
    },
    "Nyave Trade Quest": {
        "on_scenes": [0xA00],
        "not_has_locations": ["Ocean SW Nyave Trade Quest Item"],
        "unset_if_true": [(0x1B5590, 0x80), (0x1BA649, 0x20)],
        "reset_flags": ["RESET Swordsmans Scroll", "RESET Wood Heart"]
    },
    "Hoiger Trade Quest": {
        "on_scenes": [0x900],
        "not_has_locations": ["Ocean SE Hoiger Howgendoogen Trade Quest Item"],
        "unset_if_true": [(0x1B5590, 0x90), (0x1BA649, 0x20)],
        "reset_flags": ["RESET Swordsmans Scroll", "RESET Guard Notebook", "RESET Wood Heart"]
    },
    "Wayfarer Trade Quest": {
        "on_scenes": [0x800],
        "not_has_locations": ["Bannan Island Wayfarer Trade Quest Chest"],
        "unset_if_true": [(0x1BA649, 0x20)],
        "reset_flags": ["RESET Swordsmans Scroll"]
    },
    "RESET Swordsmans Scroll": {
        # "on_scenes": [0x0, 0x1, 0x2, 0x3],
        "has_items": [("Swordsman's Scroll", 1)],
        "set_if_true": [(0x1BA649, 0x20)]
    },
    "RESET Wood Heart": {
        # "on_scenes": [0x0, 0x1, 0x2, 0x3],
        "has_items": [("Wood Heart", 1)],
        "not_has_locations": ["Bannan Island Wayfarer Trade Quest Chest"],
        "set_if_true": [(0x1B5590, 0x80)]
    },
    "RESET Guard Notebook": {
        # "on_scenes": [0x0, 0x1, 0x2, 0x3],
        "has_items": [("Guard Notebook", 1)],
        "not_has_locations": ["Ocean SW Nyave Trade Quest Item"],
        "set_if_true": [(0x1B5590, 0x10)]
    },
    "RESET Kaleidoscope": {
        # "on_scenes": [0x1, 0x2, 0x3],
        "has_items": [("Kaleidoscope", 1)],
        "not_has_locations": ["Ocean SE Hoiger Howgendoogen Trade Quest Item"],
        "set_if_true": [(0x1B5590, 0x8)]
    },
    # Ghost Ship HC
    "Ghost Ship HC": {
        "on_scenes": [0x3000],
        "not_has_locations": ["Cubus Sisters Heart Container"],
        "unset_if_true": [(0x1B55AB, 0x8)],
        "reset_flags": ["RESET Ghost Ship HC"]
    },
    "RESET Ghost Ship HC": {
        "set_if_true": [(0x1B55AB, 0x8)]
    },
    "Ghost ship spawn warp": {
        "on_scenes": [0x2900],
        "check_bits": [(0x1B5582, 0x10)],
        "set_if_true": [(0x1B5583, 0x40)]
    },
    # Vanilla frogs
    "Frogs show glyph": {
        "on_scenes": [0, 1, 2, 3],
        "has_slot_data": [("randomize_frogs", 0)],
        "set_if_true": [(0x1B55A2, 0x40)]
    },
    "Uncharted unset frog flag": {
        "on_scenes": [0x1a00],
        "unset_if_true": [(0x1B55A2, 0x40)]
    },
    # Doyland
    "Doyland lower water": {
        "on_scenes": [0x2201],
        "not_has_locations": ["Isle of Ruins Doylan's Item"],
        "unset_if_true": [(0x1B5582, 0x4), (0x1B55A9, 0x30)],
        "reset_flags": ["RESET Doyland lowered water"]
    },
    "RESET Doyland lowered water": {
        "has_lowered_water": True,
        "set_if_true": [(0x1B5582, 0x4)],  # Water level
    },
    "Ice Field pre-dungeon": {
        "on_scenes": [0xF03],
        "not_has_locations": ["Gleeok Boss Reward"],
        "unset_if_true": [(0x1B558B, 0x20)],
        "reset_flags": ["RESET Ice Field pre-dungeon"]
    },
    "Frost Arena Always remove Azurine": {
        "on_scenes": [0xF01],
        "unset_if_true": [(0x1B558B, 0x20)],
        "reset_flags": ["RESET Ice Field pre-dungeon", "RESET Ice Field post-dungeon"]
    },
    "Frost Port Azurine for Peg lol": {
        "on_scenes": [0xF00],
        "not_has_locations": ["Isle of Frost Stand on Peg Gift"],
        "unset_if_true": [(0x1B558B, 0x20)],
        "reset_flags": ["RESET Ice Field pre-dungeon", "RESET Ice Field post-dungeon"]
    },
    "Ice Field post-dungeon": {
        "on_scenes": [0xF03],
        "has_locations": ["Gleeok Boss Reward"],
        "set_if_true": [(0x1B558B, 0x20)],
        "reset_flags": ["RESET Ice Field post-dungeon"]
    },
    "RESET Ice Field pre-dungeon": {
        # "on_scenes": [0xF13, 0x1F00],
        "has_items": [("Azurine", 1)],
        "set_if_true": [(0x1B558B, 0x20)]
    },
    "RESET Ice Field post-dungeon": {
        # "on_scenes": [0xF13, 0x1F00],
        "has_items": [("Azurine", 0)],
        "unset_if_true": [(0x1B558B, 0x20)]
    },
    # Wayfarer fishing checks
    "RESET Swordfish Shadow": {
        "on_scenes": [0x1400],
        "has_items": [("Swordfish Shadows", 0)],
        "unset_if_true": [(0x1B55A7, 0x10)]
    },
    "Fishing remove Fish": {
        "on_scenes": [0x200],
        "unset_if_true": [(0x1BA5B4, 0xFF), (0x1BA5B5, 0xFF),
                          (0x1BA5B6, 0xFF), (0x1BA5B7, 0xFF),
                          (0x1BA5B8, 0xFF), (0x1BA5B9, 0xFF)],
        "reset_flags": ["RESET Fishing remove Stowfish", "RESET Fishing skippy",
                        "RESET Fishing toona", "RESET Fishing loovar",
                        "RESET Fishing rsf", "RESET Fishing neptoona"]
    },

    "RESET Fishing remove Stowfish": {
        # "on_scenes": [0, 1, 2, 3],
        "last_scenes": [0x200],
        "has_items": [("Fish: Stowfish", 1)],
        "set_if_true": [(0x1BA5B9, "Fish: Stowfish")]
    },
    "RESET Fishing skippy": {
        # "on_scenes": [0, 1, 2, 3],
        "last_scenes": [0x200],
        "has_items": [("Fish: Skippyjack", 1)],
        "set_if_true": [(0x1BA5B4, "Fish: Skippyjack")]
    },
    "RESET Fishing toona": {
        # "on_scenes": [0, 1, 2, 3],
        "last_scenes": [0x200],
        "has_items": [("Fish: Toona", 1)],
        "set_if_true": [(0x1BA5B5, "Fish: Toona")]
    },
    "RESET Fishing loovar": {
        # "on_scenes": [0, 1, 2, 3],
        "last_scenes": [0x200],
        "has_items": [("Fish: Loovar", 1)],
        "set_if_true": [(0x1BA5B6, "Fish: Loovar")]
    },
    "RESET Fishing rsf": {
        # "on_scenes": [0, 1, 2, 3],
        "last_scenes": [0x200],
        "has_items": [("Fish: Rusty Swordfish", 1)],
        "set_if_true": [(0x1BA5B7, "Fish: Rusty Swordfish")]
    },
    "RESET Fishing neptoona": {
        # "on_scenes": [0, 1, 2, 3],
        "last_scenes": [0x200],
        "has_items": [("Fish: Legendary Neptoona", 1)],
        "set_if_true": [(0x1BA5B8, 0x1)]
    },
    "Safety give sword cause silly": {
        "on_scenes": [0, 1, 2, 3, 0xB03],
        "has_items": [("Sword (Progressive)", 1)],
        "set_if_true": [(0x1BA644, 1)]
    },
    # Salvage
    "Salvage has no hitbox until you get cannon...": {
        "on_scenes": [0x300, 0xB0D],
        "set_if_true": [(0x1B5582, 1), (0x1B558D, 0x10)],
        "reset_flags": ["RESET Salvage has no hitbox until you get cannon...", "RESET Salvage salvage"]
    },
    "RESET Salvage has no hitbox until you get cannon...": {
        # "on_scenes": [0, 1, 2, 3, 0xB03],
        "unset_if_true": [(0x1B5582, 1)],
        "has_items": [("Cannon", 0)]
    },
    "RESET Salvage salvage": {
        # "on_scenes": [0xD00],
        "unset_if_true": [(0x1B558D, 0x10)],
        "not_has_locations": ["Cannon Island Salvage Arm"]
    },
    # Man of smiles prize postcard
    "Man of smiles prize postcard removal": {
        "on_scenes": [0x600],
        "unset_if_true": [(0x1B558F, 0x08)],
        "not_has_locations": ["Ocean NE Man of Smiles Prize Postcard"]
    },
    # Heal on bellumbeck
    "Full heal on bellumbeck": {
        "on_scenes": [0x3300],
        "full_heal": True
    },
    # Skippyjack protection
    "Remove big catch lure if no skippyjack": {
        "on_scenes": [0, 1, 2, 3],
        "not_has_locations": ["Fishing Catch Skippyjack"],
        "unset_if_true": [(0x1ba649, 0x80)],
        "reset_flags": ["RESET Remove big catch lure if no skippyjack"]
    },
    "RESET Remove big catch lure if no skippyjack": {
        # "on_scenes": [0, 1, 2, 3],
        "has_locations": ["Fishing Catch Skippyjack"],
        "has_items": [("Big Catch Lure", 1)],
        "set_if_true": [(0x1ba649, 0x80)]
    },
    # Beedle Point Thresholds
    "Beedle points bronze": {
        "on_scenes": [0x500],
        "beedle_points": 1,
        "set_if_true": [(0x1B5588, 0x40)]
    },
    "Beedle points silver": {
        "on_scenes": [0x500],
        "beedle_points": 20,
        "set_if_true": [(0x1b558e, 0x20)]
    },
    "Beedle points gold": {
        "on_scenes": [0x500],
        "beedle_points": 50,
        "set_if_true": [(0x1b558e, 0x40)]
    },
    "Beedle points plat": {
        "on_scenes": [0x500],
        "beedle_points": 100,
        "set_if_true": [(0x1b558e, 0x80)]
    },
    "Beedle points vip": {
        "on_scenes": [0x500],
        "beedle_points": 200,
        "set_if_true": [(0x1b558f, 0x1)]
    },
    # Ember Stuff
    "Ember remove double linebeck": {
        "on_scenes": [0xD00],
        "set_if_true": [(0x1B557F, 0x20)],
        "reset_flags": ["RESET Ember double linebeck"],
    },
    "RESET Ember double linebeck": {
        "not_has_locations": ["Blaaz Boss Reward"],
        "unset_if_true": [(0x1B557F, 0x20)],
    },
    "Astrid after fire temple": {
        "on_scenes": [0xD0A],
        "has_locations": ["Blaaz Boss Reward"],
        "set_if_true": [(0x1B557F, 0x20)]
    },
    "Astrid before fire temple": {
        "on_scenes": [0xD0A],
        "not_has_locations": ["Blaaz Boss Reward"],
        "unset_if_true": [(0x1B557F, 0x20)]
    },
    "Ember respawn blaaz": {
        "on_scenes": [0x2B00],
        "not_has_locations": ["Blaaz Boss Reward"],
        "unset_if_true": [(0x1B557F, 0x20)],
    },
    "Molida respawn crayk": {
        "on_scenes": [0x2C00],
        "not_has_locations": ["Crayk Boss Reward"],
        "unset_if_true": [(0x1B557F, 0x80)],
    },
    # Regal necklace backup removal
    "Regal necklace backup removal dummy": {
        "on_scenes": [0x1500],
        "reset_flags": ["Regal necklace backup removal"]
    },
    "Regal necklace backup removal": {
        "has_items": [("Regal Necklace", 0)],
        "unset_if_true": [(0x1b5582, 0x8)]
    },
    # TotOK shortcuts
    "Spawn yellow warp early": {
        "has_slot_data": [("totok_checkpoints", 1)],
        "has_locations": ["TotOK B3 NW Sea Chart Chest"],
        "on_scenes": [0x2600],
        "set_if_true": [(0x1B55AA, 0x20)]
    },
    "TotOK Elevator down": {
        "on_scenes": [0x250D],
        "last_scenes": [0x250C],
        "set_if_true": [(0x20C5F0, 0x10)]
    },
    "TotOK Elevator up": {
        "on_scenes": [0x250D],
        "last_scenes": [0x250E],
        "unset_if_true": [(0x20C5F0, 0x10)]
    },
}

