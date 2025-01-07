from BaseClasses import Location, Region
from typing import Dict, Tuple, Optional
from . import names


class MM3Location(Location):
    game = "Mega Man 3"


class MM3Region(Region):
    game = "Mega Man 3"


needle_man_locations: Dict[str, Optional[int]] = {
    names.needle_man: 0x890001,
    names.get_needle_cannon: 0x890101,
    names.get_rush_jet: 0x890111,
}

magnet_man_locations: Dict[str, Optional[int]] = {
    names.magnet_man: 0x890002,
    names.get_magnet_missile: 0x890102
}

gemini_man_locations: Dict[str, Optional[int]] = {
    names.gemini_man: 0x890003,
    names.get_gemini_laser: 0x890103
}

hard_man_locations: Dict[str, Optional[int]] = {
    names.hard_man: 0x890004,
    names.get_hard_knuckle: 0x890104
}

top_man_locations: Dict[str, Optional[int]] = {
    names.top_man: 0x890005,
    names.get_top_spin: 0x890105,
}

snake_man_locations: Dict[str, Optional[int]] = {
    names.snake_man: 0x890006,
    names.get_search_snake: 0x890106,
}

spark_man_locations: Dict[str, Optional[int]] = {
    names.spark_man: 0x890007,
    names.get_spark_shock: 0x890107
}

shadow_man_locations: Dict[str, Optional[int]] = {
    names.shadow_man: 0x890008,
    names.get_shadow_blade: 0x890108,
    names.get_rush_marine: 0x890112
}

doc_air_locations: Dict[str, Optional[int]] = {
    names.doc_air: 0x890010,
}

doc_crash_locations: Dict[str, Optional[int]] = {
    names.doc_crash: 0x890011,
    names.doc_needle: None
}

doc_flash_locations: Dict[str, Optional[int]] = {
    names.doc_flash: 0x890012,
}

doc_bubble_locations: Dict[str, Optional[int]] = {
    names.doc_bubble: 0x890013,
    names.doc_gemini: None
}

doc_wood_locations: Dict[str, Optional[int]] = {
    names.doc_wood: 0x890014,
}

doc_heat_locations: Dict[str, Optional[int]] = {
    names.doc_heat: 0x890015,
    names.doc_shadow: None
}

doc_metal_locations: Dict[str, Optional[int]] = {
    names.doc_metal: 0x890016,
}

doc_quick_locations: Dict[str, Optional[int]] = {
    names.doc_quick: 0x890017,
    names.doc_spark: None
}

break_man_location: Dict[str, Optional[int]] = {
    names.break_man: 0x89000F,
    names.break_stage: None
}

wily_1_locations: Dict[str, Optional[int]] = {
    names.wily_1_boss: 0x890009,
    names.wily_stage_1: None
}

wily_2_locations: Dict[str, Optional[int]] = {
    names.wily_2_boss: 0x89000A,
    names.wily_stage_2: None
}

wily_3_locations: Dict[str, Optional[int]] = {
    names.wily_3_boss: 0x89000B,
    names.wily_stage_3: None
}

wily_4_locations: Dict[str, Optional[int]] = {
    # Wily 4 doesn't have a boss, it just has the RBM rush
    names.wily_stage_4: None
}

wily_5_locations: Dict[str, Optional[int]] = {
    names.wily_5_boss: 0x89000D,
    names.wily_stage_5: None
}

wily_6_locations: Dict[str, Optional[int]] = {
    names.gamma: None
}


etank_1ups: Dict[str, Dict[str, Optional[int]]] = {
    "Needle Man Stage": {
        names.needle_man_c2: 0x890201
    },
    "Gemini Man Stage": {
        names.gemini_man_c1: 0x89020A,
        names.gemini_man_c3: 0x89020C,
        names.gemini_man_c6: 0x89020F,
        names.gemini_man_c7: 0x890210,
        names.gemini_man_c10: 0x890213,
    },
    "Hard Man Stage": {
        names.hard_man_c3: 0x890216,

    },
    "Top Man Stage": {
        names.top_man_c6: 0x890220,
    },
    "Snake Man Stage": {
        names.snake_man_c3: 0x890225,
        names.snake_man_c4: 0x890226,
    },
    "Doc Robot (Needle) - Air": {
        names.doc_needle_c2: 0x890233,
        names.doc_needle_c3: 0x890234,
    },
    "Doc Robot (Gemini) - Flash": {
        names.doc_gemini_c1: 0x89023D,
        names.doc_gemini_c2: 0x89023E,
    },
    "Wily Stage 1": {
        names.wily_1_c1: 0x890248,
        names.wily_1_c2: 0x890249,
        names.wily_1_c4: 0x89024B,
        names.wily_1_c8: 0x89024F,
    },
    "Wily Stage 2": {
        names.wily_2_c3: 0x890256,
        names.wily_2_c9: 0x89025C,
        names.wily_2_c11: 0x89025E,
    },
    "Wily Stage 3": {
        names.wily_3_c3: 0x890263,
        names.wily_3_c4: 0x890264,
        names.wily_3_c10: 0x89026A,
        names.wily_3_c11: 0x89026B
    },
    "Wily Stage 4": {
        names.wily_4_c10: 0x890275,
        names.wily_4_c12: 0x890277,
    },
    "Wily Stage 5": {
        names.wily_5_c3: 0x890282,
        names.wily_5_c4: 0x890283,
    },
    "Wily Stage 6": {
        names.wily_6_c1: 0x890284,
        names.wily_6_c2: 0x890285,
        names.wily_6_c5: 0x890288,
        names.wily_6_c6: 0x890289,
    }
}

energy_pickups: Dict[str, Dict[str, Optional[int]]] = {
    "Needle Man Stage": {
        names.needle_man_c1: 0x890200
    },
    "Magnet Man Stage": {
        names.magnet_man_c1: 0x890202,
        names.magnet_man_c2: 0x890203,
        names.magnet_man_c3: 0x890204,
        names.magnet_man_c4: 0x890205,
        names.magnet_man_c5: 0x890206,
        names.magnet_man_c6: 0x890207,
        names.magnet_man_c7: 0x890208,
        names.magnet_man_c8: 0x890209,
    },
    "Gemini Man Stage": {
        names.gemini_man_c2: 0x89020B,
        names.gemini_man_c4: 0x89020D,
        names.gemini_man_c5: 0x89020E,
        names.gemini_man_c8: 0x890211,
        names.gemini_man_c9: 0x890212,
    },
    "Hard Man Stage": {
        names.hard_man_c1: 0x890214,
        names.hard_man_c2: 0x890215,
        names.hard_man_c4: 0x890217,
        names.hard_man_c5: 0x890218,
        names.hard_man_c6: 0x890219,
        names.hard_man_c7: 0x89021A,
    },
    "Top Man Stage": {
        names.top_man_c1: 0x89021B,
        names.top_man_c2: 0x89021C,
        names.top_man_c3: 0x89021D,
        names.top_man_c4: 0x89021E,
        names.top_man_c5: 0x89021F,
        names.top_man_c7: 0x890221,
        names.top_man_c8: 0x890222,
    },
    "Snake Man Stage": {
        names.snake_man_c1: 0x890223,
        names.snake_man_c2: 0x890224,
        names.snake_man_c5: 0x890227,
    },
    "Spark Man Stage": {
        names.spark_man_c1: 0x890228,
        names.spark_man_c2: 0x890229,
        names.spark_man_c3: 0x89022A,
        names.spark_man_c4: 0x89022B,
        names.spark_man_c5: 0x89022C,
        names.spark_man_c6: 0x89022D,
    },
    "Shadow Man Stage": {
        names.shadow_man_c1: 0x89022E,
        names.shadow_man_c2: 0x89022F,
        names.shadow_man_c3: 0x890230,
        names.shadow_man_c4: 0x890231,
    },
    "Doc Robot (Needle) - Air": {
        names.doc_needle_c1: 0x890232
    },
    "Doc Robot (Needle) - Crash": {
        names.doc_needle_c4: 0x890235,
        names.doc_needle_c5: 0x890236,
        names.doc_needle_c6: 0x890237,
        names.doc_needle_c7: 0x890238,
        names.doc_needle_c8: 0x890239,
        names.doc_needle_c9: 0x89023A,
        names.doc_needle_c10: 0x89023B,
        names.doc_needle_c11: 0x89023C,
    },
    "Doc Robot (Gemini) - Bubble": {
        names.doc_gemini_c3: 0x89023F,
        names.doc_gemini_c4: 0x890240,
    },
    "Doc Robot (Spark) - Metal": {
        names.doc_spark_c1: 0x890241
    },
    "Doc Robot (Spark) - Quick": {
        names.doc_spark_c2: 0x890242
    },
    "Doc Robot (Shadow) - Heat": {
        names.doc_shadow_c1: 0x890243,
        names.doc_shadow_c2: 0x890244,
        names.doc_shadow_c3: 0x890245,
        names.doc_shadow_c4: 0x890246,
        names.doc_shadow_c5: 0x890247,
    },
    "Wily Stage 1": {
        names.wily_1_c3: 0x89024A,
        names.wily_1_c5: 0x89024C,
        names.wily_1_c6: 0x89024D,
        names.wily_1_c7: 0x89024E,
        names.wily_1_c9: 0x890250,
        names.wily_1_c10: 0x890251,
        names.wily_1_c11: 0x890252,
        names.wily_1_c12: 0x890253,
    },
    "Wily Stage 2": {
        names.wily_2_c1: 0x890254,
        names.wily_2_c2: 0x890255,
        names.wily_2_c4: 0x890257,
        names.wily_2_c5: 0x890258,
        names.wily_2_c6: 0x890259,
        names.wily_2_c7: 0x89025A,
        names.wily_2_c8: 0x89025B,
        names.wily_2_c10: 0x89025D,
        names.wily_2_c12: 0x89025F,
        names.wily_2_c13: 0x890260,
    },
    "Wily Stage 3": {
        names.wily_3_c1: 0x890261,
        names.wily_3_c2: 0x890262,
        names.wily_3_c5: 0x890265,
        names.wily_3_c6: 0x890266,
        names.wily_3_c7: 0x890267,
        names.wily_3_c8: 0x890268,
        names.wily_3_c9: 0x890269,
    },
    "Wily Stage 4": {
        names.wily_4_c1: 0x89026C,
        names.wily_4_c2: 0x89026D,
        names.wily_4_c3: 0x89026E,
        names.wily_4_c4: 0x89026F,
        names.wily_4_c5: 0x890270,
        names.wily_4_c6: 0x890271,
        names.wily_4_c7: 0x890272,
        names.wily_4_c8: 0x890273,
        names.wily_4_c9: 0x890274,
        names.wily_4_c11: 0x890276,
        names.wily_4_c13: 0x890278,
        names.wily_4_c14: 0x890279,
        names.wily_4_c15: 0x89027A,
        names.wily_4_c16: 0x89027B,
        names.wily_4_c17: 0x89027C,
        names.wily_4_c18: 0x89027D,
        names.wily_4_c19: 0x89027E,
        names.wily_4_c20: 0x89027F,
    },
    "Wily Stage 5": {
        names.wily_5_c1: 0x890280,
        names.wily_5_c2: 0x890281,
    },
    "Wily Stage 6": {
        names.wily_6_c3: 0x890286,
        names.wily_6_c4: 0x890287,
        names.wily_6_c7: 0x89028A,
    }
}

mm3_regions: Dict[str, Tuple[Tuple[str, ...], Dict[str, Optional[int]], Optional[str]]] = {
    "Needle Man Stage": ((names.needle_man_stage,), needle_man_locations, None),
    "Magnet Man Stage": ((names.magnet_man_stage,), magnet_man_locations, None),
    "Gemini Man Stage": ((names.gemini_man_stage,), gemini_man_locations, None),
    "Hard Man Stage": ((names.hard_man_stage,), hard_man_locations, None),
    "Top Man Stage": ((names.top_man_stage,), top_man_locations, None),
    "Snake Man Stage": ((names.snake_man_stage,), snake_man_locations, None),
    "Spark Man Stage": ((names.spark_man_stage,), spark_man_locations, None),
    "Shadow Man Stage": ((names.shadow_man_stage,), shadow_man_locations, None),
    "Doc Robot (Needle) - Air": ((names.doc_needle_stage,), doc_air_locations, None),
    "Doc Robot (Needle) - Crash": ((), doc_crash_locations, "Doc Robot (Needle) - Air"),
    "Doc Robot (Gemini) - Flash": ((names.doc_gemini_stage,), doc_flash_locations, None),
    "Doc Robot (Gemini) - Bubble": ((), doc_bubble_locations, "Doc Robot (Gemini) - Flash"),
    "Doc Robot (Shadow) - Wood": ((names.doc_shadow_stage,), doc_wood_locations, None),
    "Doc Robot (Shadow) - Heat": ((), doc_heat_locations, "Doc Robot (Shadow) - Wood"),
    "Doc Robot (Spark) - Metal": ((names.doc_spark_stage,), doc_metal_locations, None),
    "Doc Robot (Spark) - Quick": ((), doc_quick_locations, "Doc Robot (Spark) - Metal"),
    "Break Man": ((names.doc_needle, names.doc_gemini, names.doc_spark, names.doc_shadow), break_man_location, None),
    "Wily Stage 1": ((names.break_stage,), wily_1_locations, "Break Man"),
    "Wily Stage 2": ((names.wily_stage_1,), wily_2_locations, "Wily Stage 1"),
    "Wily Stage 3": ((names.wily_stage_2,), wily_3_locations, "Wily Stage 2"),
    "Wily Stage 4": ((names.wily_stage_3,), wily_4_locations, "Wily Stage 3"),
    "Wily Stage 5": ((names.wily_stage_4,), wily_5_locations, "Wily Stage 4"),
    "Wily Stage 6": ((names.wily_stage_5,), wily_6_locations, "Wily Stage 5")
}

location_table: Dict[str, Optional[int]] = {
    **needle_man_locations,
    **magnet_man_locations,
    **gemini_man_locations,
    **hard_man_locations,
    **top_man_locations,
    **snake_man_locations,
    **spark_man_locations,
    **shadow_man_locations,
    **doc_air_locations,
    **doc_crash_locations,
    **doc_flash_locations,
    **doc_bubble_locations,
    **doc_wood_locations,
    **doc_heat_locations,
    **doc_metal_locations,
    **doc_quick_locations,
    **break_man_location,
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


def get_consumables(stage: str) -> Dict[str, int]:
    return {**etank_1ups.get(stage, {}), **energy_pickups.get(stage, {})}


location_groups = {
    "Get Equipped": {
        names.get_needle_cannon,
        names.get_magnet_missile,
        names.get_gemini_laser,
        names.get_hard_knuckle,
        names.get_top_spin,
        names.get_search_snake,
        names.get_spark_shock,
        names.get_shadow_blade,
        names.get_rush_marine,
        names.get_rush_jet,
    },
    "Needle Man Stage": {*needle_man_locations.keys()},
    "Magnet Man Stage": {*magnet_man_locations.keys()},
    "Gemini Man Stage": {*gemini_man_locations.keys()},
    "Hard Man Stage": {*hard_man_locations.keys()},
    "Top Man Stage": {*top_man_locations.keys()},
    "Snake Man Stage": {*snake_man_locations.keys()},
    "Spark Man Stage": {*spark_man_locations.keys()},
    "Shadow Man Stage": {*shadow_man_locations.keys()},
}

lookup_location_to_id: Dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
