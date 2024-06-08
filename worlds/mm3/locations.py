from BaseClasses import Location, Region
from typing import Dict, Tuple, Optional
from .names import (needle_man, magnet_man, gemini_man, hard_man, top_man, snake_man, spark_man, shadow_man,
                    get_needle_cannon, get_magnet_missile, get_gemini_laser, get_hard_knuckle, get_top_spin,
                    get_search_snake, get_spark_shot, get_shadow_blade, get_rush_marine, get_rush_jet,
                    doc_air, doc_crash, doc_flash, doc_bubble, doc_wood, doc_heat, doc_metal, doc_quick,
                    doc_needle, doc_gemini, doc_spark, doc_shadow, break_man, break_stage, wily_1_boss, wily_2_boss,
                    wily_3_boss, wily_5_boss, wily_stage_1, wily_stage_2, wily_stage_3, wily_stage_4, wily_stage_5,
                    gamma, needle_man_stage, magnet_man_stage, gemini_man_stage, hard_man_stage, top_man_stage,
                    snake_man_stage, spark_man_stage, shadow_man_stage, doc_needle_stage, doc_gemini_stage,
                    doc_shadow_stage, doc_spark_stage)


class MM3Location(Location):
    game = "Mega Man 3"


class MM3Region(Region):
    game = "Mega Man 3"


needle_man_locations: Dict[str, Optional[int]] = {
    needle_man: 0x890001,
    get_needle_cannon: 0x890101,
    get_rush_marine: 0x890111,
}

magnet_man_locations: Dict[str, Optional[int]] = {
    magnet_man: 0x890002,
    get_magnet_missile: 0x890102
}

gemini_man_locations: Dict[str, Optional[int]] = {
    gemini_man: 0x890003,
    get_gemini_laser: 0x890103
}

hard_man_locations: Dict[str, Optional[int]] = {
    hard_man: 0x890004,
    get_hard_knuckle: 0x890104
}

top_man_locations: Dict[str, Optional[int]] = {
    top_man: 0x890005,
    get_top_spin: 0x890105,
}

snake_man_locations: Dict[str, Optional[int]] = {
    snake_man: 0x890006,
    get_search_snake: 0x890106,
}

spark_man_locations: Dict[str, Optional[int]] = {
    spark_man: 0x890007,
    get_spark_shot: 0x890107
}

shadow_man_locations: Dict[str, Optional[int]] = {
    shadow_man: 0x890008,
    get_shadow_blade: 0x890108,
    get_rush_jet: 0x890112
}

doc_air_locations: Dict[str, Optional[int]] = {
    doc_air: 0x890010,
}

doc_crash_locations: Dict[str, Optional[int]] = {
    doc_crash: 0x890011,
    doc_needle: None
}

doc_flash_locations: Dict[str, Optional[int]] = {
    doc_flash: 0x890012,
}

doc_bubble_locations: Dict[str, Optional[int]] = {
    doc_bubble: 0x890013,
    doc_gemini: None
}

doc_wood_locations: Dict[str, Optional[int]] = {
    doc_wood: 0x890014,
}

doc_heat_locations: Dict[str, Optional[int]] = {
    doc_heat: 0x890015,
    doc_shadow: None
}

doc_metal_locations: Dict[str, Optional[int]] = {
    doc_metal: 0x890016,
}

doc_quick_locations: Dict[str, Optional[int]] = {
    doc_quick: 0x890017,
    doc_spark: None
}

break_man_location: Dict[str, Optional[int]] = {
    break_man: 0x89000F,
    break_stage: None
}

wily_1_locations: Dict[str, Optional[int]] = {
    wily_1_boss: 0x890009,
    wily_stage_1: None
}

wily_2_locations: Dict[str, Optional[int]] = {
    wily_2_boss: 0x89000A,
    wily_stage_2: None
}

wily_3_locations: Dict[str, Optional[int]] = {
    wily_3_boss: 0x89000B,
    wily_stage_3: None
}

wily_4_locations: Dict[str, Optional[int]] = {
    # Wily 4 doesn't have a boss, it just has the RBM rush
    wily_stage_4: None
}

wily_5_locations: Dict[str, Optional[int]] = {
    wily_5_boss: 0x89000D,
    wily_stage_5: None
}

wily_6_locations: Dict[str, Optional[int]] = {
    gamma: None
}


etank_1ups: Dict[str, Dict[str, Optional[int]]] = {
    "Hard Man Stage": {},
    "Wily Stage 2": {}
}

energy_pickups: Dict[str, Dict[str, Optional[int]]] = {
    "Hard Man Stage": {},
    "Wily Stage 2": {}
}

mm3_regions: Dict[str, Tuple[Tuple[str, ...], Dict[str, Optional[int]], Optional[str]]] = {
    "Needle Man Stage": ((needle_man_stage,), needle_man_locations, None),
    "Magnet Man Stage": ((magnet_man_stage,), magnet_man_locations, None),
    "Gemini Man Stage": ((gemini_man_stage,), gemini_man_locations, None),
    "Hard Man Stage": ((hard_man_stage,), hard_man_locations, None),
    "Top Man Stage": ((top_man_stage,), top_man_locations, None),
    "Snake Man Stage": ((snake_man_stage,), snake_man_locations, None),
    "Spark Man Stage": ((spark_man_stage,), spark_man_locations, None),
    "Shadow Man Stage": ((shadow_man_stage,), shadow_man_locations, None),
    "Doc Robot (Needle) - Air": ((doc_needle_stage,), doc_air_locations, None),
    "Doc Robot (Needle) - Crash": ((), doc_crash_locations, "Doc Robot (Needle) - Air"),
    "Doc Robot (Gemini) - Flash": ((doc_gemini_stage,), doc_flash_locations, None),
    "Doc Robot (Gemini) - Bubble": ((), doc_bubble_locations, "Doc Robot (Gemini) - Flash"),
    "Doc Robot (Shadow) - Wood": ((doc_shadow_stage,), doc_wood_locations, None),
    "Doc Robot (Shadow) - Heat": ((), doc_heat_locations, "Doc Robot (Shadow) - Wood"),
    "Doc Robot (Spark) - Metal": ((doc_spark_stage,), doc_metal_locations, None),
    "Doc Robot (Spark) - Quick": ((), doc_quick_locations, "Doc Robot (Spark) - Metal"),
    "Break Man": ((doc_needle, doc_gemini, doc_spark, doc_shadow), break_man_location, None),
    "Wily Stage 1": ((break_stage,), wily_1_locations, "Break Man"),
    "Wily Stage 2": ((wily_stage_1,), wily_2_locations, "Wily Stage 1"),
    "Wily Stage 3": ((wily_stage_2,), wily_3_locations, "Wily Stage 2"),
    "Wily Stage 4": ((wily_stage_3,), wily_4_locations, "Wily Stage 3"),
    "Wily Stage 5": ((wily_stage_4,), wily_5_locations, "Wily Stage 4"),
    "Wily Stage 6": ((wily_stage_5,), wily_6_locations, "Wily Stage 5")
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

location_groups = {
    "Get Equipped": {
        get_needle_cannon,
        get_magnet_missile,
        get_gemini_laser,
        get_hard_knuckle,
        get_top_spin,
        get_search_snake,
        get_spark_shot,
        get_shadow_blade,
        get_rush_marine,
        get_rush_jet,
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
