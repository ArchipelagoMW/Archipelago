from BaseClasses import Location, Region
from typing import NamedTuple
from . import names


class MM2Location(Location):
    game = "Mega Man 2"


class MM2Region(Region):
    game = "Mega Man 2"


class LocationData(NamedTuple):
    location_id: int | None
    energy: bool = False
    oneup_tank: bool = False


class RegionData(NamedTuple):
    locations: dict[str, LocationData]
    required_items: list[str]
    parent: str = ""


mm2_regions: dict[str, RegionData] = {
    "Heat Man Stage": RegionData({
        names.heat_man: LocationData(0x880001),
        names.atomic_fire_get: LocationData(0x880101),
        names.item_1_get: LocationData(0x880111),
        names.heat_man_c1: LocationData(0x880201, oneup_tank=True),
        }, [names.heat_man_stage]),

    "Air Man Stage": RegionData({
        names.air_man: LocationData(0x880002),
        names.air_shooter_get: LocationData(0x880102),
        names.item_2_get: LocationData(0x880112),
        }, [names.air_man_stage]),

    "Wood Man Stage": RegionData({
        names.wood_man: LocationData(0x880003),
        names.leaf_shield_get: LocationData(0x880103),
        }, [names.wood_man_stage]),

    "Bubble Man Stage": RegionData({
        names.bubble_man: LocationData(0x880004),
        names.bubble_lead_get: LocationData(0x880104),
        }, [names.bubble_man_stage]),

    "Quick Man Stage": RegionData({
        names.quick_man: LocationData(0x880005),
        names.quick_boomerang_get: LocationData(0x880105),
        names.quick_man_c1: LocationData(0x880202, oneup_tank=True),
        names.quick_man_c2: LocationData(0x880203, oneup_tank=True),
        names.quick_man_c3: LocationData(0x880204, oneup_tank=True),
        names.quick_man_c4: LocationData(0x880205, energy=True),
        names.quick_man_c5: LocationData(0x880206, energy=True),
        names.quick_man_c6: LocationData(0x880207, energy=True),
        names.quick_man_c7: LocationData(0x880208, oneup_tank=True),
        names.quick_man_c8: LocationData(0x880209, energy=True),
        }, [names.quick_man_stage]),

    "Flash Man Stage": RegionData({
        names.flash_man: LocationData(0x880006),
        names.time_stopper_get: LocationData(0x880106),
        names.item_3_get: LocationData(0x880113),
        names.flash_man_c1: LocationData(0x88020A, energy=True),
        names.flash_man_c2: LocationData(0x88020B, oneup_tank=True),
        names.flash_man_c3: LocationData(0x88020C, energy=True),
        names.flash_man_c4: LocationData(0x88020D, energy=True),
        names.flash_man_c5: LocationData(0x88020E, energy=True),
        names.flash_man_c6: LocationData(0x88020F, oneup_tank=True),
        }, [names.flash_man_stage]),

    "Metal Man Stage": RegionData({
        names.metal_man: LocationData(0x880007),
        names.metal_blade_get: LocationData(0x880107),
        names.metal_man_c1: LocationData(0x880210, oneup_tank=True),
        names.metal_man_c2: LocationData(0x880211, oneup_tank=True),
        names.metal_man_c3: LocationData(0x880212, oneup_tank=True),
        }, [names.metal_man_stage]),

    "Crash Man Stage": RegionData({
        names.crash_man: LocationData(0x880008),
        names.crash_bomber_get: LocationData(0x880108),
        names.crash_man_c1: LocationData(0x880213, energy=True),
        names.crash_man_c2: LocationData(0x880214, oneup_tank=True),
        names.crash_man_c3: LocationData(0x880215, oneup_tank=True),
        }, [names.crash_man_stage]),

    "Wily Stage 1": RegionData({
        names.wily_1: LocationData(0x880009),
        names.wily_stage_1: LocationData(None),
        names.wily_1_c1: LocationData(0x880216, oneup_tank=True),
        names.wily_1_c2: LocationData(0x880217, energy=True),
        }, [names.item_1, names.item_2, names.item_3]),

    "Wily Stage 2": RegionData({
        names.wily_2: LocationData(0x88000A),
        names.wily_stage_2: LocationData(None),
        names.wily_2_c1: LocationData(0x880218, energy=True),
        names.wily_2_c2: LocationData(0x880219, energy=True),
        names.wily_2_c3: LocationData(0x88021A, oneup_tank=True),
        names.wily_2_c4: LocationData(0x88021B, oneup_tank=True),
        names.wily_2_c5: LocationData(0x88021C, oneup_tank=True),
        names.wily_2_c6: LocationData(0x88021D, oneup_tank=True),
        names.wily_2_c7: LocationData(0x88021E, energy=True),
        names.wily_2_c8: LocationData(0x880227, energy=True),
        names.wily_2_c9: LocationData(0x880228, energy=True),
        names.wily_2_c10: LocationData(0x880229, energy=True),
        names.wily_2_c11: LocationData(0x88022A, energy=True),
        names.wily_2_c12: LocationData(0x88022B, energy=True),
        names.wily_2_c13: LocationData(0x88022C, energy=True),
        names.wily_2_c14: LocationData(0x88022D, energy=True),
        names.wily_2_c15: LocationData(0x88022E, energy=True),
        names.wily_2_c16: LocationData(0x88022F, energy=True),
        }, [], "Wily Stage 1"),

    "Wily Stage 3": RegionData({
        names.wily_3: LocationData(0x88000B),
        names.wily_stage_3: LocationData(None),
        names.wily_3_c1: LocationData(0x88021F, energy=True),
        names.wily_3_c2: LocationData(0x880220, oneup_tank=True),
        names.wily_3_c3: LocationData(0x880221, energy=True),
        names.wily_3_c4: LocationData(0x880222, energy=True),
        }, [], "Wily Stage 2"),

    "Wily Stage 4": RegionData({
        names.wily_4: LocationData(0x88000C),
        names.wily_stage_4: LocationData(None),
        names.wily_4_c1: LocationData(0x880223, energy=True),
        names.wily_4_c2: LocationData(0x880224, energy=True),
        names.wily_4_c3: LocationData(0x880225, oneup_tank=True),
        names.wily_4_c4: LocationData(0x880226, oneup_tank=True),
        }, [], "Wily Stage 3"),

    "Wily Stage 5": RegionData({
        names.wily_5: LocationData(0x88000D),
        names.wily_stage_5: LocationData(None),
        }, [], "Wily Stage 4"),

    "Wily Stage 6": RegionData({
        names.dr_wily: LocationData(None),
        }, [], "Wily Stage 5"),
}


def get_boss_locations(region: str) -> list[str]:
    return [location for location, data in mm2_regions[region].locations.items()
            if not data.energy and not data.oneup_tank]


def get_energy_locations(region: str) -> list[str]:
    return [location for location, data in mm2_regions[region].locations.items() if data.energy]


def get_oneup_locations(region: str) -> list[str]:
    return [location for location, data in mm2_regions[region].locations.items() if data.oneup_tank]


location_table: dict[str, int | None] = {
    location: data.location_id for region in mm2_regions.values() for location, data in region.locations.items()
}

location_groups: dict[str, set[str]] = {
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
    "Wily 2 Weapon Energy": {names.wily_2_c8, names.wily_2_c9, names.wily_2_c10, names.wily_2_c11, names.wily_2_c12,
                             names.wily_2_c13, names.wily_2_c14, names.wily_2_c15, names.wily_2_c16},
    **{name: {location for location, data in region.locations.items() if data.location_id}
       for name, region in mm2_regions.items() if name != "Wily Stage 6"}
}

lookup_location_to_id: dict[str, int] = {location: idx for location, idx in location_table.items() if idx is not None}
