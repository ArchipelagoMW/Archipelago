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
    # "RESET Bannan Island Map": {
    #     "on_scenes": [0x1],
    #     "has_items": [("Treasure Map #22", 1)],
    #     "set_if_true": [(0x1BA652, 0x8)]
    # },
    # # TotoK 1F
    # "TotoK Don't open key door": {
    #     "on_scenes": [0x2500],
    #     "not_has_locations": ["TotOK 1F SW Sea Chart Chest"],
    #     "unset_if_true": [(0x1B557D, 0x02)]
    # },
    # "TotoK remove linebeck": {
    #     "on_scenes": [0x2500],
    #     "has_locations": ["TotOK 1F SW Sea Chart Chest"],
    #     "set_if_true": [(0x1B557D, 0x02)]
    # },
}

