from BaseClasses import Location, Region
from typing import NamedTuple
from . import names


class MM3Location(Location):
    game = "Mega Man 3"


class MM3Region(Region):
    game = "Mega Man 3"


class LocationData(NamedTuple):
    location_id: int | None
    energy: bool = False
    oneup_tank: bool = False


class RegionData(NamedTuple):
    locations: dict[str, LocationData]
    required_items: list[str]
    parent: str = ""

mm3_regions: dict[str, RegionData] = {
    "Needle Man Stage": RegionData({
        names.needle_man: LocationData(0x0001),
        names.get_needle_cannon: LocationData(0x0101),
        names.get_rush_jet: LocationData(0x0111),
        names.needle_man_c1: LocationData(0x0200, energy=True),
        names.needle_man_c2: LocationData(0x0201, oneup_tank=True),
    }, [names.needle_man_stage]),

    "Magnet Man Stage": RegionData({
        names.magnet_man: LocationData(0x0002),
        names.get_magnet_missile: LocationData(0x0102),
        names.magnet_man_c1: LocationData(0x0202, energy=True),
        names.magnet_man_c2: LocationData(0x0203, energy=True),
        names.magnet_man_c3: LocationData(0x0204, energy=True),
        names.magnet_man_c4: LocationData(0x0205, energy=True),
        names.magnet_man_c5: LocationData(0x0206, energy=True),
        names.magnet_man_c6: LocationData(0x0207, energy=True),
        names.magnet_man_c7: LocationData(0x0208, energy=True),
        names.magnet_man_c8: LocationData(0x0209, energy=True),
    }, [names.magnet_man_stage]),

    "Gemini Man Stage": RegionData({
        names.gemini_man: LocationData(0x0003),
        names.get_gemini_laser: LocationData(0x0103),
        names.gemini_man_c1: LocationData(0x020A, oneup_tank=True),
        names.gemini_man_c2: LocationData(0x020B, energy=True),
        names.gemini_man_c3: LocationData(0x020C, oneup_tank=True),
        names.gemini_man_c4: LocationData(0x020D, energy=True),
        names.gemini_man_c5: LocationData(0x020E, energy=True),
        names.gemini_man_c6: LocationData(0x020F, oneup_tank=True),
        names.gemini_man_c7: LocationData(0x0210, oneup_tank=True),
        names.gemini_man_c8: LocationData(0x0211, energy=True),
        names.gemini_man_c9: LocationData(0x0212, energy=True),
        names.gemini_man_c10: LocationData(0x0213, oneup_tank=True),
    }, [names.gemini_man_stage]),

    "Hard Man Stage": RegionData({
        names.hard_man: LocationData(0x0004),
        names.get_hard_knuckle: LocationData(0x0104),
        names.hard_man_c1: LocationData(0x0214, energy=True),
        names.hard_man_c2: LocationData(0x0215, energy=True),
        names.hard_man_c3: LocationData(0x0216, oneup_tank=True),
        names.hard_man_c4: LocationData(0x0217, energy=True),
        names.hard_man_c5: LocationData(0x0218, energy=True),
        names.hard_man_c6: LocationData(0x0219, energy=True),
        names.hard_man_c7: LocationData(0x021A, energy=True),
    }, [names.hard_man_stage]),

    "Top Man Stage": RegionData({
        names.top_man: LocationData(0x0005),
        names.get_top_spin: LocationData(0x0105),
        names.top_man_c1: LocationData(0x021B, energy=True),
        names.top_man_c2: LocationData(0x021C, energy=True),
        names.top_man_c3: LocationData(0x021D, energy=True),
        names.top_man_c4: LocationData(0x021E, energy=True),
        names.top_man_c5: LocationData(0x021F, energy=True),
        names.top_man_c6: LocationData(0x0220, oneup_tank=True),
        names.top_man_c7: LocationData(0x0221, energy=True),
        names.top_man_c8: LocationData(0x0222, energy=True),
    }, [names.top_man_stage]),

    "Snake Man Stage": RegionData({
        names.snake_man: LocationData(0x0006),
        names.get_search_snake: LocationData(0x0106),
        names.snake_man_c1: LocationData(0x0223, energy=True),
        names.snake_man_c2: LocationData(0x0224, energy=True),
        names.snake_man_c3: LocationData(0x0225, oneup_tank=True),
        names.snake_man_c4: LocationData(0x0226, oneup_tank=True),
        names.snake_man_c5: LocationData(0x0227, energy=True),
    }, [names.snake_man_stage]),

    "Spark Man Stage": RegionData({
        names.spark_man: LocationData(0x0007),
        names.get_spark_shock: LocationData(0x0107),
        names.spark_man_c1: LocationData(0x0228, energy=True),
        names.spark_man_c2: LocationData(0x0229, energy=True),
        names.spark_man_c3: LocationData(0x022A, energy=True),
        names.spark_man_c4: LocationData(0x022B, energy=True),
        names.spark_man_c5: LocationData(0x022C, energy=True),
        names.spark_man_c6: LocationData(0x022D, energy=True),
    }, [names.spark_man_stage]),

    "Shadow Man Stage": RegionData({
        names.shadow_man: LocationData(0x0008),
        names.get_shadow_blade: LocationData(0x0108),
        names.get_rush_marine: LocationData(0x0112),
        names.shadow_man_c1: LocationData(0x022E, energy=True),
        names.shadow_man_c2: LocationData(0x022F, energy=True),
        names.shadow_man_c3: LocationData(0x0230, energy=True),
        names.shadow_man_c4: LocationData(0x0231, energy=True),
    }, [names.shadow_man_stage]),

    "Doc Robot (Needle) - Air": RegionData({
        names.doc_air: LocationData(0x0010),
        names.doc_needle_c1: LocationData(0x0232, energy=True),
        names.doc_needle_c2: LocationData(0x0233, oneup_tank=True),
        names.doc_needle_c3: LocationData(0x0234, oneup_tank=True),
    }, [names.doc_needle_stage]),

    "Doc Robot (Needle) - Crash": RegionData({
        names.doc_crash: LocationData(0x0011),
        names.doc_needle: LocationData(None),
        names.doc_needle_c4: LocationData(0x0235, energy=True),
        names.doc_needle_c5: LocationData(0x0236, energy=True),
        names.doc_needle_c6: LocationData(0x0237, energy=True),
        names.doc_needle_c7: LocationData(0x0238, energy=True),
        names.doc_needle_c8: LocationData(0x0239, energy=True),
        names.doc_needle_c9: LocationData(0x023A, energy=True),
        names.doc_needle_c10: LocationData(0x023B, energy=True),
        names.doc_needle_c11: LocationData(0x023C, energy=True),
    }, [], parent="Doc Robot (Needle) - Air"),

    "Doc Robot (Gemini) - Flash": RegionData({
        names.doc_flash: LocationData(0x0012),
        names.doc_gemini_c1: LocationData(0x023D, oneup_tank=True),
        names.doc_gemini_c2: LocationData(0x023E, oneup_tank=True),
    }, [names.doc_gemini_stage]),

    "Doc Robot (Gemini) - Bubble": RegionData({
        names.doc_bubble: LocationData(0x0013),
        names.doc_gemini: LocationData(None),
        names.doc_gemini_c3: LocationData(0x023F, energy=True),
        names.doc_gemini_c4: LocationData(0x0240, energy=True),
    }, [], parent="Doc Robot (Gemini) - Flash"),

    "Doc Robot (Shadow) - Wood": RegionData({
        names.doc_wood: LocationData(0x0014),
    }, [names.doc_shadow_stage]),

    "Doc Robot (Shadow) - Heat": RegionData({
        names.doc_heat: LocationData(0x0015),
        names.doc_shadow: LocationData(None),
        names.doc_shadow_c1: LocationData(0x0243, energy=True),
        names.doc_shadow_c2: LocationData(0x0244, energy=True),
        names.doc_shadow_c3: LocationData(0x0245, energy=True),
        names.doc_shadow_c4: LocationData(0x0246, energy=True),
        names.doc_shadow_c5: LocationData(0x0247, energy=True),
    }, [], parent="Doc Robot (Shadow) - Wood"),

    "Doc Robot (Spark) - Metal": RegionData({
        names.doc_metal: LocationData(0x0016),
        names.doc_spark_c1: LocationData(0x0241, energy=True),
    }, [names.doc_spark_stage]),

    "Doc Robot (Spark) - Quick": RegionData({
        names.doc_quick: LocationData(0x0017),
        names.doc_spark: LocationData(None),
        names.doc_spark_c2: LocationData(0x0242, energy=True),
    }, [], parent="Doc Robot (Spark) - Metal"),

    "Break Man": RegionData({
        names.break_man: LocationData(0x000F),
        names.break_stage: LocationData(None),
    }, [names.doc_needle, names.doc_gemini, names.doc_spark, names.doc_shadow]),

    "Wily Stage 1": RegionData({
        names.wily_1_boss: LocationData(0x0009),
        names.wily_stage_1: LocationData(None),
        names.wily_1_c1: LocationData(0x0248, oneup_tank=True),
        names.wily_1_c2: LocationData(0x0249, oneup_tank=True),
        names.wily_1_c3: LocationData(0x024A, energy=True),
        names.wily_1_c4: LocationData(0x024B, oneup_tank=True),
        names.wily_1_c5: LocationData(0x024C, energy=True),
        names.wily_1_c6: LocationData(0x024D, energy=True),
        names.wily_1_c7: LocationData(0x024E, energy=True),
        names.wily_1_c8: LocationData(0x024F, oneup_tank=True),
        names.wily_1_c9: LocationData(0x0250, energy=True),
        names.wily_1_c10: LocationData(0x0251, energy=True),
        names.wily_1_c11: LocationData(0x0252, energy=True),
        names.wily_1_c12: LocationData(0x0253, energy=True),
    }, [names.break_stage], parent="Break Man"),

    "Wily Stage 2": RegionData({
        names.wily_2_boss: LocationData(0x000A),
        names.wily_stage_2: LocationData(None),
        names.wily_2_c1: LocationData(0x0254, energy=True),
        names.wily_2_c2: LocationData(0x0255, energy=True),
        names.wily_2_c3: LocationData(0x0256, oneup_tank=True),
        names.wily_2_c4: LocationData(0x0257, energy=True),
        names.wily_2_c5: LocationData(0x0258, energy=True),
        names.wily_2_c6: LocationData(0x0259, energy=True),
        names.wily_2_c7: LocationData(0x025A, energy=True),
        names.wily_2_c8: LocationData(0x025B, energy=True),
        names.wily_2_c9: LocationData(0x025C, oneup_tank=True),
        names.wily_2_c10: LocationData(0x025D, energy=True),
        names.wily_2_c11: LocationData(0x025E, oneup_tank=True),
        names.wily_2_c12: LocationData(0x025F, energy=True),
        names.wily_2_c13: LocationData(0x0260, energy=True),
    }, [names.wily_stage_1], parent="Wily Stage 1"),

    "Wily Stage 3": RegionData({
        names.wily_3_boss: LocationData(0x000B),
        names.wily_stage_3: LocationData(None),
        names.wily_3_c1: LocationData(0x0261, energy=True),
        names.wily_3_c2: LocationData(0x0262, energy=True),
        names.wily_3_c3: LocationData(0x0263, oneup_tank=True),
        names.wily_3_c4: LocationData(0x0264, oneup_tank=True),
        names.wily_3_c5: LocationData(0x0265, energy=True),
        names.wily_3_c6: LocationData(0x0266, energy=True),
        names.wily_3_c7: LocationData(0x0267, energy=True),
        names.wily_3_c8: LocationData(0x0268, energy=True),
        names.wily_3_c9: LocationData(0x0269, energy=True),
        names.wily_3_c10: LocationData(0x026A, oneup_tank=True),
        names.wily_3_c11: LocationData(0x026B, oneup_tank=True)
    }, [names.wily_stage_2], parent="Wily Stage 2"),

    "Wily Stage 4": RegionData({
        names.wily_stage_4: LocationData(None),
        names.wily_4_c1: LocationData(0x026C, energy=True),
        names.wily_4_c2: LocationData(0x026D, energy=True),
        names.wily_4_c3: LocationData(0x026E, energy=True),
        names.wily_4_c4: LocationData(0x026F, energy=True),
        names.wily_4_c5: LocationData(0x0270, energy=True),
        names.wily_4_c6: LocationData(0x0271, energy=True),
        names.wily_4_c7: LocationData(0x0272, energy=True),
        names.wily_4_c8: LocationData(0x0273, energy=True),
        names.wily_4_c9: LocationData(0x0274, energy=True),
        names.wily_4_c10: LocationData(0x0275, oneup_tank=True),
        names.wily_4_c11: LocationData(0x0276, energy=True),
        names.wily_4_c12: LocationData(0x0277, oneup_tank=True),
        names.wily_4_c13: LocationData(0x0278, energy=True),
        names.wily_4_c14: LocationData(0x0279, energy=True),
        names.wily_4_c15: LocationData(0x027A, energy=True),
        names.wily_4_c16: LocationData(0x027B, energy=True),
        names.wily_4_c17: LocationData(0x027C, energy=True),
        names.wily_4_c18: LocationData(0x027D, energy=True),
        names.wily_4_c19: LocationData(0x027E, energy=True),
        names.wily_4_c20: LocationData(0x027F, energy=True),
    }, [names.wily_stage_3], parent="Wily Stage 3"),

    "Wily Stage 5": RegionData({
        names.wily_5_boss: LocationData(0x000D),
        names.wily_stage_5: LocationData(None),
        names.wily_5_c1: LocationData(0x0280, energy=True),
        names.wily_5_c2: LocationData(0x0281, energy=True),
        names.wily_5_c3: LocationData(0x0282, oneup_tank=True),
        names.wily_5_c4: LocationData(0x0283, oneup_tank=True),
    }, [names.wily_stage_4], parent="Wily Stage 4"),

    "Wily Stage 6": RegionData({
        names.gamma: LocationData(None),
        names.wily_6_c1: LocationData(0x0284, oneup_tank=True),
        names.wily_6_c2: LocationData(0x0285, oneup_tank=True),
        names.wily_6_c3: LocationData(0x0286, energy=True),
        names.wily_6_c4: LocationData(0x0287, energy=True),
        names.wily_6_c5: LocationData(0x0288, oneup_tank=True),
        names.wily_6_c6: LocationData(0x0289, oneup_tank=True),
        names.wily_6_c7: LocationData(0x028A, energy=True),
    }, [names.wily_stage_5], parent="Wily Stage 5"),
}


def get_boss_locations(region: str) -> list[str]:
    return [location for location, data in mm3_regions[region].locations.items()
            if not data.energy and not data.oneup_tank]


def get_energy_locations(region: str) -> list[str]:
    return [location for location, data in mm3_regions[region].locations.items() if data.energy]


def get_oneup_locations(region: str) -> list[str]:
    return [location for location, data in mm3_regions[region].locations.items() if data.oneup_tank]


location_table: dict[str, int | None] = {
    location: data.location_id for region in mm3_regions.values() for location, data in region.locations.items()
}


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
    **{name: {location for location, data in region.locations.items() if data.location_id} for name, region in mm3_regions.items()}
}

lookup_location_to_id: dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
