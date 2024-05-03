from BaseClasses import Location, Region
from typing import Dict, Tuple, Optional
import Names


class MM2Location(Location):
    game = "Mega Man 2"


class MM2Region(Region):
    game = "Mega Man 2"


heat_man_locations: Dict[str, Optional[int]] = {
    Names.heat_man: 0x880001,
    Names.atomic_fire_get: 0x880101,
    Names.item_1_get: 0x880111,
}

air_man_locations: Dict[str, Optional[int]] = {
    Names.air_man: 0x880002,
    Names.air_shooter_get: 0x880102,
    Names.item_2_get: 0x880112
}

wood_man_locations: Dict[str, Optional[int]] = {
    Names.wood_man: 0x880003,
    Names.leaf_shield_get: 0x880103
}

bubble_man_locations: Dict[str, Optional[int]] = {
    Names.bubble_man: 0x880004,
    Names.bubble_lead_get: 0x880104
}

quick_man_locations: Dict[str, Optional[int]] = {
    Names.quick_man: 0x880005,
    Names.quick_boomerang_get: 0x880105,
}

flash_man_locations: Dict[str, Optional[int]] = {
    Names.flash_man: 0x880006,
    Names.time_stopper_get: 0x880106,
    Names.item_3_get: 0x880113,
}

metal_man_locations: Dict[str, Optional[int]] = {
    Names.metal_man: 0x880007,
    Names.metal_blade_get: 0x880107
}

crash_man_locations: Dict[str, Optional[int]] = {
    Names.crash_man: 0x880008,
    Names.crash_bomber_get: 0x880108
}

wily_1_locations: Dict[str, Optional[int]] = {
    Names.wily_1: 0x880009,
    Names.wily_stage_1: None
}

wily_2_locations: Dict[str, Optional[int]] = {
    Names.wily_2: 0x88000A,
    Names.wily_stage_2: None
}

wily_3_locations: Dict[str, Optional[int]] = {
    Names.wily_3: 0x88000B,
    Names.wily_stage_3: None
}

wily_4_locations: Dict[str, Optional[int]] = {
    Names.wily_4: 0x88000C,
    Names.wily_stage_4: None
}

wily_5_locations: Dict[str, Optional[int]] = {
    Names.wily_5: 0x88000D,
    Names.wily_stage_5: None
}

wily_6_locations: Dict[str, Optional[int]] = {
    Names.dr_wily: None
}

etank_1ups: Dict[str, Dict[str, Optional[int]]] = {
    "Heat Man Stage": {
        Names.heat_man_c1: 0x880201,
    },
    "Quick Man Stage": {
        Names.quick_man_c1: 0x880202,
        Names.quick_man_c2: 0x880203,
        Names.quick_man_c3: 0x880204,
        Names.quick_man_c7: 0x880208,
    },
    "Flash Man Stage": {
        Names.flash_man_c2: 0x88020B,
        Names.flash_man_c6: 0x88020F,
    },
    "Metal Man Stage": {
        Names.metal_man_c1: 0x880210,
        Names.metal_man_c2: 0x880211,
        Names.metal_man_c3: 0x880212,
    },
    "Crash Man Stage": {
        Names.crash_man_c2: 0x880214,
        Names.crash_man_c3: 0x880215,
    },
    "Wily Stage 1": {
        Names.wily_1_c1: 0x880216,
    },
    "Wily Stage 2": {
        Names.wily_2_c3: 0x88021A,
        Names.wily_2_c4: 0x88021B,
        Names.wily_2_c5: 0x88021C,
        Names.wily_2_c6: 0x88021D,
    },
    "Wily Stage 3": {
        Names.wily_3_c2: 0x880220,
    },
    "Wily Stage 4": {
        Names.wily_4_c3: 0x880225,
        Names.wily_4_c4: 0x880226,
    }
}

energy_pickups: Dict[str, Dict[str, Optional[int]]] = {
    "Quick Man Stage": {
        Names.quick_man_c4: 0x880205,
        Names.quick_man_c5: 0x880206,
        Names.quick_man_c6: 0x880207,
        Names.quick_man_c8: 0x880209,
    },
    "Flash Man Stage": {
        Names.flash_man_c1: 0x88020A,
        Names.flash_man_c3: 0x88020C,
        Names.flash_man_c4: 0x88020D,
        Names.flash_man_c5: 0x88020E,
    },
    "Crash Man Stage": {
        Names.crash_man_c1: 0x880213,
    },
    "Wily Stage 1": {
        Names.wily_1_c2: 0x880217,
    },
    "Wily Stage 2": {
        Names.wily_2_c1: 0x880218,
        Names.wily_2_c2: 0x880219,
        Names.wily_2_c7: 0x88021E,
        Names.wily_2_c8: 0x880227,
        Names.wily_2_c9: 0x880228,
        Names.wily_2_c10: 0x880229,
        Names.wily_2_c11: 0x88022A,
        Names.wily_2_c12: 0x88022B,
        Names.wily_2_c13: 0x88022C,
        Names.wily_2_c14: 0x88022D,
        Names.wily_2_c15: 0x88022E,
        Names.wily_2_c16: 0x88022F,
    },
    "Wily Stage 3": {
        Names.wily_3_c1: 0x88021F,
        Names.wily_3_c3: 0x880221,
        Names.wily_3_c4: 0x880222,
    },
    "Wily Stage 4": {
        Names.wily_4_c1: 0x880223,
        Names.wily_4_c2: 0x880224,
    }
}

mm2_regions: Dict[str, Tuple[Tuple[str, ...], Dict[str, Optional[int]], Optional[str]]] = {
    "Heat Man Stage": ((Names.heat_man_stage,), heat_man_locations, None),
    "Air Man Stage": ((Names.air_man_stage,), air_man_locations, None),
    "Wood Man Stage": ((Names.wood_man_stage,), wood_man_locations, None),
    "Bubble Man Stage": ((Names.bubble_man_stage,), bubble_man_locations, None),
    "Quick Man Stage": ((Names.quick_man_stage,), quick_man_locations, None),
    "Flash Man Stage": ((Names.flash_man_stage,), flash_man_locations, None),
    "Metal Man Stage": ((Names.metal_man_stage,), metal_man_locations, None),
    "Crash Man Stage": ((Names.crash_man_stage,), crash_man_locations, None),
    "Wily Stage 1": ((Names.item_1, Names.item_2, Names.item_3), wily_1_locations, None),
    "Wily Stage 2": ((Names.wily_stage_1,), wily_2_locations, "Wily Stage 1"),
    "Wily Stage 3": ((Names.wily_stage_2,), wily_3_locations, "Wily Stage 2"),
    "Wily Stage 4": ((Names.wily_stage_3,), wily_4_locations, "Wily Stage 3"),
    "Wily Stage 5": ((Names.wily_stage_4,), wily_5_locations, "Wily Stage 4"),
    "Wily Stage 6": ((Names.wily_stage_5,), wily_6_locations, "Wily Stage 5")
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
        Names.atomic_fire_get,
        Names.air_shooter_get,
        Names.leaf_shield_get,
        Names.bubble_lead_get,
        Names.quick_boomerang_get,
        Names.time_stopper_get,
        Names.metal_blade_get,
        Names.crash_bomber_get,
        Names.item_1_get,
        Names.item_2_get,
        Names.item_3_get
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
    "Wily 2 Weapon Energy": {Names.wily_2_c8, Names.wily_2_c9, Names.wily_2_c10, Names.wily_2_c11, Names.wily_2_c12,
                             Names.wily_2_c13, Names.wily_2_c14, Names.wily_2_c15, Names.wily_2_c16}
}

lookup_location_to_id: Dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
