from BaseClasses import Location
import typing
import Names


class MM2Location(Location):
    game = "Mega Man 2"


heat_man_locations = {
    Names.heat_man: 0x880001,
    Names.atomic_fire_get: 0x880101,
    Names.item_1_get: 0x880111,
}

air_man_locations = {
    Names.air_man: 0x880002,
    Names.air_shooter_get: 0x880102,
    Names.item_2_get: 0x880112
}

wood_man_locations = {
    Names.wood_man: 0x880003,
    Names.leaf_shield_get: 0x880103
}

bubble_man_locations = {
    Names.bubble_man: 0x880004,
    Names.bubble_lead_get: 0x880104
}

quick_man_locations = {
    Names.quick_man: 0x880005,
    Names.quick_boomerang_get: 0x880105
}

flash_man_locations = {
    Names.flash_man: 0x880006,
    Names.time_stopper_get: 0x880106,
    Names.item_3_get: 0x880113
}

metal_man_locations = {
    Names.metal_man: 0x880007,
    Names.metal_blade_get: 0x880107
}

crash_man_locations = {
    Names.crash_man: 0x880008,
    Names.crash_bomber_get: 0x880108
}

dr_wily_locations = {
    Names.dr_wily: None
}

location_table: typing.Dict[str, typing.Optional[int]] = {
    **heat_man_locations,
    **air_man_locations,
    **wood_man_locations,
    **bubble_man_locations,
    **quick_man_locations,
    **flash_man_locations,
    **metal_man_locations,
    **crash_man_locations
}
