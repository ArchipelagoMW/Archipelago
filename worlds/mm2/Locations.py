from BaseClasses import Location, Region
from typing import Dict, Tuple, Optional
from .Names import *


class MM2Location(Location):
    game = "Mega Man 2"


class MM2Region(Region):
    game = "Mega Man 2"


heat_man_locations: Dict[str, Optional[int]] = {
    heat_man: 0x880001,
    atomic_fire_get: 0x880101,
    item_1_get: 0x880111,
}

air_man_locations: Dict[str, Optional[int]] = {
    air_man: 0x880002,
    air_shooter_get: 0x880102,
    item_2_get: 0x880112
}

wood_man_locations: Dict[str, Optional[int]] = {
    wood_man: 0x880003,
    leaf_shield_get: 0x880103
}

bubble_man_locations: Dict[str, Optional[int]] = {
    bubble_man: 0x880004,
    bubble_lead_get: 0x880104
}

quick_man_locations: Dict[str, Optional[int]] = {
    quick_man: 0x880005,
    quick_boomerang_get: 0x880105,
}

flash_man_locations: Dict[str, Optional[int]] = {
    flash_man: 0x880006,
    time_stopper_get: 0x880106,
    item_3_get: 0x880113,
}

metal_man_locations: Dict[str, Optional[int]] = {
    metal_man: 0x880007,
    metal_blade_get: 0x880107
}

crash_man_locations: Dict[str, Optional[int]] = {
    crash_man: 0x880008,
    crash_bomber_get: 0x880108
}

wily_1_locations: Dict[str, Optional[int]] = {
    wily_1: 0x880009,
    wily_stage_1: None
}

wily_2_locations: Dict[str, Optional[int]] = {
    wily_2: 0x88000A,
    wily_stage_2: None
}

wily_3_locations: Dict[str, Optional[int]] = {
    wily_3: 0x88000B,
    wily_stage_3: None
}

wily_4_locations: Dict[str, Optional[int]] = {
    wily_4: 0x88000C,
    wily_stage_4: None
}

wily_5_locations: Dict[str, Optional[int]] = {
    wily_5: 0x88000D,
    wily_stage_5: None
}

wily_6_locations: Dict[str, Optional[int]] = {
    dr_wily: None
}

etank_1ups: Dict[str, Dict[str, Optional[int]]] = {
    "Heat Man Stage": {
        heat_man_c1: 0x880201,
    },
    "Quick Man Stage": {
        quick_man_c1: 0x880202,
        quick_man_c2: 0x880203,
        quick_man_c3: 0x880204,
        quick_man_c7: 0x880208,
    },
    "Flash Man Stage": {
        flash_man_c2: 0x88020B,
        flash_man_c6: 0x88020F,
    },
    "Metal Man Stage": {
        metal_man_c1: 0x880210,
        metal_man_c2: 0x880211,
        metal_man_c3: 0x880212,
    },
    "Crash Man Stage": {
        crash_man_c2: 0x880214,
        crash_man_c3: 0x880215,
    },
    "Wily Stage 1": {
        wily_1_c1: 0x880216,
    },
    "Wily Stage 2": {
        wily_2_c3: 0x88021A,
        wily_2_c4: 0x88021B,
        wily_2_c5: 0x88021C,
        wily_2_c6: 0x88021D,
    },
    "Wily Stage 3": {
        wily_3_c2: 0x880220,
    },
    "Wily Stage 4": {
        wily_4_c3: 0x880225,
        wily_4_c4: 0x880226,
    }
}

energy_pickups: Dict[str, Dict[str, Optional[int]]] = {
    "Quick Man Stage": {
        quick_man_c4: 0x880205,
        quick_man_c5: 0x880206,
        quick_man_c6: 0x880207,
        quick_man_c8: 0x880209,
    },
    "Flash Man Stage": {
        flash_man_c1: 0x88020A,
        flash_man_c3: 0x88020C,
        flash_man_c4: 0x88020D,
        flash_man_c5: 0x88020E,
    },
    "Crash Man Stage": {
        crash_man_c1: 0x880213,
    },
    "Wily Stage 1": {
        wily_1_c2: 0x880217,
    },
    "Wily Stage 2": {
        wily_2_c1: 0x880218,
        wily_2_c2: 0x880219,
        wily_2_c7: 0x88021E,
        wily_2_c8: 0x880227,
        wily_2_c9: 0x880228,
        wily_2_c10: 0x880229,
        wily_2_c11: 0x88022A,
        wily_2_c12: 0x88022B,
        wily_2_c13: 0x88022C,
        wily_2_c14: 0x88022D,
        wily_2_c15: 0x88022E,
        wily_2_c16: 0x88022F,
    },
    "Wily Stage 3": {
        wily_3_c1: 0x88021F,
        wily_3_c3: 0x880221,
        wily_3_c4: 0x880222,
    },
    "Wily Stage 4": {
        wily_4_c1: 0x880223,
        wily_4_c2: 0x880224,
    }
}

mm2_regions: Dict[str, Tuple[Tuple[str, ...], Dict[str, Optional[int]], Optional[str]]] = {
    "Heat Man Stage": ((heat_man_stage,), heat_man_locations, None),
    "Air Man Stage": ((air_man_stage,), air_man_locations, None),
    "Wood Man Stage": ((wood_man_stage,), wood_man_locations, None),
    "Bubble Man Stage": ((bubble_man_stage,), bubble_man_locations, None),
    "Quick Man Stage": ((quick_man_stage,), quick_man_locations, None),
    "Flash Man Stage": ((flash_man_stage,), flash_man_locations, None),
    "Metal Man Stage": ((metal_man_stage,), metal_man_locations, None),
    "Crash Man Stage": ((crash_man_stage,), crash_man_locations, None),
    "Wily Stage 1": ((item_1, item_2, item_3), wily_1_locations, None),
    "Wily Stage 2": ((wily_stage_1,), wily_2_locations, "Wily Stage 1"),
    "Wily Stage 3": ((wily_stage_2,), wily_3_locations, "Wily Stage 2"),
    "Wily Stage 4": ((wily_stage_3,), wily_4_locations, "Wily Stage 3"),
    "Wily Stage 5": ((wily_stage_4,), wily_5_locations, "Wily Stage 4"),
    "Wily Stage 6": ((wily_stage_5,), wily_6_locations, "Wily Stage 5")
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

for table in etank_1ups:
    location_table.update(etank_1ups[table])

for table in energy_pickups:
    location_table.update(energy_pickups[table])

location_groups = {
    "Get Equipped": {
        atomic_fire_get,
        air_shooter_get,
        leaf_shield_get,
        bubble_lead_get,
        quick_boomerang_get,
        time_stopper_get,
        metal_blade_get,
        crash_bomber_get,
        item_1_get,
        item_2_get,
        item_3_get
    },
    "Heat Man Stage": {*heat_man_locations.keys(), *etank_1ups["Heat Man Stage"].keys()},
    "Air Man Stage": {*air_man_locations.keys()},
    "Wood Man Stage": {*wood_man_locations.keys()},
    "Bubble Man Stage": {*bubble_man_locations.keys()},
    "Quick Man Stage": {*quick_man_locations.keys(), *etank_1ups["Quick Man Stage"].keys(),
                        *energy_pickups["Quick Man Stage"].keys()},
    "Flash Man Stage": {*flash_man_locations.keys(), *etank_1ups["Flash Man Stage"].keys(),
                        *energy_pickups["Flash Man Stage"].keys()},
    "Metal Man Stage": {*metal_man_locations.keys(), *etank_1ups["Metal Man Stage"].keys()},
    "Crash Man Stage": {*crash_man_locations.keys(), *etank_1ups["Crash Man Stage"].keys(),
                        *energy_pickups["Crash Man Stage"].keys()},
    "Wily 2 Weapon Energy": {wily_2_c8, wily_2_c9, wily_2_c10, wily_2_c11, wily_2_c12, wily_2_c13, wily_2_c14,
                             wily_2_c15, wily_2_c16}
}

lookup_location_to_id: Dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
