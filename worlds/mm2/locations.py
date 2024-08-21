from BaseClasses import Location, Region
from typing import Dict, Tuple, Optional
from . import names


class MM2Location(Location):
    game = "Mega Man 2"


class MM2Region(Region):
    game = "Mega Man 2"


heat_man_locations: Dict[str, Optional[int]] = {
    names.heat_man: 0x880001,
    names.atomic_fire_get: 0x880101,
    names.item_1_get: 0x880111,
}

air_man_locations: Dict[str, Optional[int]] = {
    names.air_man: 0x880002,
    names.air_shooter_get: 0x880102,
    names.item_2_get: 0x880112
}

wood_man_locations: Dict[str, Optional[int]] = {
    names.wood_man: 0x880003,
    names.leaf_shield_get: 0x880103
}

bubble_man_locations: Dict[str, Optional[int]] = {
    names.bubble_man: 0x880004,
    names.bubble_lead_get: 0x880104
}

quick_man_locations: Dict[str, Optional[int]] = {
    names.quick_man: 0x880005,
    names.quick_boomerang_get: 0x880105,
}

flash_man_locations: Dict[str, Optional[int]] = {
    names.flash_man: 0x880006,
    names.time_stopper_get: 0x880106,
    names.item_3_get: 0x880113,
}

metal_man_locations: Dict[str, Optional[int]] = {
    names.metal_man: 0x880007,
    names.metal_blade_get: 0x880107
}

crash_man_locations: Dict[str, Optional[int]] = {
    names.crash_man: 0x880008,
    names.crash_bomber_get: 0x880108
}

wily_1_locations: Dict[str, Optional[int]] = {
    names.wily_1: 0x880009,
    names.wily_stage_1: None
}

wily_2_locations: Dict[str, Optional[int]] = {
    names.wily_2: 0x88000A,
    names.wily_stage_2: None
}

wily_3_locations: Dict[str, Optional[int]] = {
    names.wily_3: 0x88000B,
    names.wily_stage_3: None
}

wily_4_locations: Dict[str, Optional[int]] = {
    names.wily_4: 0x88000C,
    names.wily_stage_4: None
}

wily_5_locations: Dict[str, Optional[int]] = {
    names.wily_5: 0x88000D,
    names.wily_stage_5: None
}

wily_6_locations: Dict[str, Optional[int]] = {
    names.dr_wily: None
}

etank_1ups: Dict[str, Dict[str, Optional[int]]] = {
    "Heat Man Stage": {
        names.heat_man_c1: 0x880201,
    },
    "Quick Man Stage": {
        names.quick_man_c1: 0x880202,
        names.quick_man_c2: 0x880203,
        names.quick_man_c3: 0x880204,
        names.quick_man_c7: 0x880208,
    },
    "Flash Man Stage": {
        names.flash_man_c2: 0x88020B,
        names.flash_man_c6: 0x88020F,
    },
    "Metal Man Stage": {
        names.metal_man_c1: 0x880210,
        names.metal_man_c2: 0x880211,
        names.metal_man_c3: 0x880212,
    },
    "Crash Man Stage": {
        names.crash_man_c2: 0x880214,
        names.crash_man_c3: 0x880215,
    },
    "Wily Stage 1": {
        names.wily_1_c1: 0x880216,
    },
    "Wily Stage 2": {
        names.wily_2_c3: 0x88021A,
        names.wily_2_c4: 0x88021B,
        names.wily_2_c5: 0x88021C,
        names.wily_2_c6: 0x88021D,
    },
    "Wily Stage 3": {
        names.wily_3_c2: 0x880220,
    },
    "Wily Stage 4": {
        names.wily_4_c3: 0x880225,
        names.wily_4_c4: 0x880226,
    }
}

energy_pickups: Dict[str, Dict[str, Optional[int]]] = {
    "Quick Man Stage": {
        names.quick_man_c4: 0x880205,
        names.quick_man_c5: 0x880206,
        names.quick_man_c6: 0x880207,
        names.quick_man_c8: 0x880209,
    },
    "Flash Man Stage": {
        names.flash_man_c1: 0x88020A,
        names.flash_man_c3: 0x88020C,
        names.flash_man_c4: 0x88020D,
        names.flash_man_c5: 0x88020E,
    },
    "Crash Man Stage": {
        names.crash_man_c1: 0x880213,
    },
    "Wily Stage 1": {
        names.wily_1_c2: 0x880217,
    },
    "Wily Stage 2": {
        names.wily_2_c1: 0x880218,
        names.wily_2_c2: 0x880219,
        names.wily_2_c7: 0x88021E,
        names.wily_2_c8: 0x880227,
        names.wily_2_c9: 0x880228,
        names.wily_2_c10: 0x880229,
        names.wily_2_c11: 0x88022A,
        names.wily_2_c12: 0x88022B,
        names.wily_2_c13: 0x88022C,
        names.wily_2_c14: 0x88022D,
        names.wily_2_c15: 0x88022E,
        names.wily_2_c16: 0x88022F,
    },
    "Wily Stage 3": {
        names.wily_3_c1: 0x88021F,
        names.wily_3_c3: 0x880221,
        names.wily_3_c4: 0x880222,
    },
    "Wily Stage 4": {
        names.wily_4_c1: 0x880223,
        names.wily_4_c2: 0x880224,
    }
}

mm2_regions: Dict[str, Tuple[Tuple[str, ...], Dict[str, Optional[int]], Optional[str]]] = {
    "Heat Man Stage": ((names.heat_man_stage,), heat_man_locations, None),
    "Air Man Stage": ((names.air_man_stage,), air_man_locations, None),
    "Wood Man Stage": ((names.wood_man_stage,), wood_man_locations, None),
    "Bubble Man Stage": ((names.bubble_man_stage,), bubble_man_locations, None),
    "Quick Man Stage": ((names.quick_man_stage,), quick_man_locations, None),
    "Flash Man Stage": ((names.flash_man_stage,), flash_man_locations, None),
    "Metal Man Stage": ((names.metal_man_stage,), metal_man_locations, None),
    "Crash Man Stage": ((names.crash_man_stage,), crash_man_locations, None),
    "Wily Stage 1": ((names.item_1, names.item_2, names.item_3), wily_1_locations, None),
    "Wily Stage 2": ((names.wily_stage_1,), wily_2_locations, "Wily Stage 1"),
    "Wily Stage 3": ((names.wily_stage_2,), wily_3_locations, "Wily Stage 2"),
    "Wily Stage 4": ((names.wily_stage_3,), wily_4_locations, "Wily Stage 3"),
    "Wily Stage 5": ((names.wily_stage_4,), wily_5_locations, "Wily Stage 4"),
    "Wily Stage 6": ((names.wily_stage_5,), wily_6_locations, "Wily Stage 5")
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
        names.atomic_fire_get,
        names.air_shooter_get,
        names.leaf_shield_get,
        names.bubble_lead_get,
        names.quick_boomerang_get,
        names.time_stopper_get,
        names.metal_blade_get,
        names.crash_bomber_get,
        names.item_1_get,
        names.item_2_get,
        names.item_3_get
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
    "Wily 2 Weapon Energy": {names.wily_2_c8, names.wily_2_c9, names.wily_2_c10, names.wily_2_c11, names.wily_2_c12,
                             names.wily_2_c13, names.wily_2_c14, names.wily_2_c15, names.wily_2_c16}
}

lookup_location_to_id: Dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
