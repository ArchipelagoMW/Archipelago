from BaseClasses import Location
from typing import Dict, List, Tuple, Optional
from .Names import *


class MM2Location(Location):
    game = "Mega Man 2"


heat_man_locations = {
    heat_man: 0x880001,
    atomic_fire_get: 0x880101,
    item_1_get: 0x880111,
}

air_man_locations = {
    air_man: 0x880002,
    air_shooter_get: 0x880102,
    item_2_get: 0x880112
}

wood_man_locations = {
    wood_man: 0x880003,
    leaf_shield_get: 0x880103
}

bubble_man_locations = {
    bubble_man: 0x880004,
    bubble_lead_get: 0x880104
}

quick_man_locations = {
    quick_man: 0x880005,
    quick_boomerang_get: 0x880105,
}

flash_man_locations = {
    flash_man: 0x880006,
    time_stopper_get: 0x880106,
    item_3_get: 0x880113,
}

metal_man_locations = {
    metal_man: 0x880007,
    metal_blade_get: 0x880107
}

crash_man_locations = {
    crash_man: 0x880008,
    crash_bomber_get: 0x880108
}

wily_1_locations = {
    wily_1: 0x880009,
}

wily_2_locations = {
    wily_2: 0x88000A
}

wily_3_locations = {
    wily_3: 0x88000B
}

wily_4_locations = {
    wily_4: 0x88000C
}

wily_5_locations = {
    wily_5: 0x88000D
}

wily_6_locations = {
    dr_wily: None
}

consumables = {
    "Heat Man Stage": {
        heat_man_c1: 0x880201,
    },
    "Quick Man Stage": {
        quick_man_c1: 0x880202,
        quick_man_c2: 0x880203,
        quick_man_c3: 0x880204,
        quick_man_c4: 0x880205,
        quick_man_c5: 0x880206,
        quick_man_c6: 0x880207,
        quick_man_c7: 0x880208,
        quick_man_c8: 0x880209,
    },
    "Flash Man Stage": {
        flash_man_c1: 0x88020A,
        flash_man_c2: 0x88020B,
        flash_man_c3: 0x88020C,
        flash_man_c4: 0x88020D,
        flash_man_c5: 0x88020E,
        flash_man_c6: 0x88020F,
    },
    "Metal Man Stage": {
        metal_man_c1: 0x880210,
        metal_man_c2: 0x880211,
        metal_man_c3: 0x880212,
    },
    "Crash Man Stage": {
        crash_man_c1: 0x880213,
        crash_man_c2: 0x880214,
        crash_man_c3: 0x880215,
    },
    "Wily Stage 1": {
        wily_1_c1: 0x880216,
        wily_1_c2: 0x880217,
    },
    "Wily Stage 2": {
        wily_2_c1: 0x880218,
        wily_2_c2: 0x880219,
        wily_2_c3: 0x88021A,
        wily_2_c4: 0x88021B,
        wily_2_c5: 0x88021C,
        wily_2_c6: 0x88021D,
        wily_2_c7: 0x88021E,
    },
    "Wily Stage 3": {
        wily_3_c1: 0x88021F,
        wily_3_c2: 0x880220,
        wily_3_c3: 0x880221,
        wily_3_c4: 0x880222,
    },
    "Wily Stage 4": {
        wily_4_c1: 0x880223,
        wily_4_c2: 0x880224,
        wily_4_c3: 0x880225,
        wily_4_c4: 0x880226,
    }
}

mm2_regions: Dict[str, Tuple[List[str], Dict[str, int], Optional[str]]] = {
    "Heat Man Stage": ([heat_man_stage], heat_man_locations, None),
    "Air Man Stage": ([air_man_stage], air_man_locations, None),
    "Wood Man Stage": ([wood_man_stage], wood_man_locations, None),
    "Bubble Man Stage": ([bubble_man_stage], bubble_man_locations, None),
    "Quick Man Stage": ([quick_man_stage], quick_man_locations, None),
    "Flash Man Stage": ([flash_man_stage], flash_man_locations, None),
    "Metal Man Stage": ([metal_man_stage], metal_man_locations, None),
    "Crash Man Stage": ([crash_man_stage], crash_man_locations, None),
    "Wily Stage 1": ([item_1, item_2, item_3], wily_1_locations, None),
    "Wily Stage 2": ([], wily_2_locations, "Wily Stage 1"),
    "Wily Stage 3": ([], wily_3_locations, "Wily Stage 2"),
    "Wily Stage 4": ([], wily_4_locations, "Wily Stage 3"),
    "Wily Stage 5": ([crash_bomber], wily_5_locations, "Wily Stage 4"),
    "Wily Stage 6": ([bubble_lead, atomic_fire], wily_6_locations, "Wily Stage 5")
}

location_table: Dict[str, Optional[int]] = {
    **heat_man_locations,
    **air_man_locations,
    **wood_man_locations,
    **bubble_man_locations,
    **quick_man_locations,
    **flash_man_locations,
    **metal_man_locations,
    **crash_man_locations,
    **wily_1_locations,
    **wily_2_locations,
    **wily_3_locations,
    **wily_4_locations,
    **wily_5_locations,
}
for table in consumables:
    location_table.update(consumables[table])
