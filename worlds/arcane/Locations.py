import typing

from BaseClasses import Location
from .Names import LocationName


class ArcaneLocation(Location):
    game: str = "Arcane: Online Mystery Serial"


s1_main_location_table = {
    # S1E1 locations
    LocationName.s1e1_well: 0xACA001,
    LocationName.s1e1_shed_wall: 0xACA002,
    LocationName.s1e1_shed_logs: 0xACA003,
    LocationName.s1e1_keg: 0xACA004,
    # S1E2 locations
    LocationName.s1e2_bedroom_drawer: 0xACA005,
    LocationName.s1e2_bedroom_lamp: 0xACA006,
    LocationName.s1e2_alvin_1: 0xACA007,
    LocationName.s1e2_alvin_2: 0xACA008,
    LocationName.s1e2_idol_shelf: 0xACA009,
    # S1E3 locations
    LocationName.s1e3_seth_cover: 0xACA00A,
    LocationName.s1e3_globe: 0xACA00B,
    LocationName.s1e3_shelf: 0xACA00C,
    LocationName.s1e3_table: 0xACA00D,
    LocationName.s1e3_chandelier: 0xACA00E,
    LocationName.s1e3_elevator: 0xACA00F,
    LocationName.s1e3_lever: 0xACA010,
    # S1E4 locations
    LocationName.s1e4_waves: 0xACA011,
    LocationName.s1e4_chest: 0xACA012,
    LocationName.s1e4_bottle: 0xACA013,
    LocationName.s1e4_stone: 0xACA014,
}

s2_main_location_table = {
    # S2E1 locations
    LocationName.s2e1_hobo: 0xACA015,
    LocationName.s2e1_crane: 0xACA016,
    LocationName.s2e1_box1: 0xACA017,
    LocationName.s2e1_box2: 0xACA018,
    LocationName.s2e1_box3: 0xACA019,
    LocationName.s2e1_exit: 0xACA01A,
    LocationName.s2e1_table: 0xACA01B,
    LocationName.s2e1_phonograph: 0xACA01C,
    LocationName.s2e1_hole: 0xACA01D,
    LocationName.s2e1_message: 0xACA01E,
    # S2E2 locations
    LocationName.s2e2_violin: 0xACA01F,
    LocationName.s2e2_drawer: 0xACA020,
    LocationName.s2e2_painting: 0xACA021,
    LocationName.s2e2_guy: 0xACA022,
    LocationName.s2e2_closet: 0xACA023,
    LocationName.s2e2_hand_box: 0xACA024,
    # S2E3 locations
    LocationName.s2e3_doorway: 0xACA025,
    LocationName.s2e3_bench: 0xACA026,
    LocationName.s2e3_closet: 0xACA027,
    LocationName.s2e3_reel: 0xACA028,
    LocationName.s2e3_platform: 0xACA029,
    LocationName.s2e3_bag: 0xACA02A,
    LocationName.s2e3_leg_box: 0xACA02B,
    LocationName.s2e3_dinghy: 0xACA02C,
    # S2E4 locations
    LocationName.s2e4_barn_bag: 0xACA02D,
    LocationName.s2e4_stand1: 0xACA02E,
    LocationName.s2e4_stand2: 0xACA02F,
    LocationName.s2e4_cabin_bag: 0xACA030,
    LocationName.s2e4_safe1: 0xACA031,
    LocationName.s2e4_safe2: 0xACA032,
    LocationName.s2e4_safe3: 0xACA033,
    LocationName.s2e4_on_statue: 0xACA034,
    LocationName.s2e4_chair: 0xACA035,
    LocationName.s2e4_in_statue_l: 0xACA036,
    LocationName.s2e4_in_statue_r: 0xACA037,
    LocationName.s2e4_barnstable: 0xACA038,
    # S2E5 locations
    LocationName.s2e5_smith: 0xACA039,
    LocationName.s2e5_gondola: 0xACA03A,
    LocationName.s2e5_armadillo: 0xACA03B,
    LocationName.s2e5_w11: 0xACA03C,
    LocationName.s2e5_helmet: 0xACA03D,
    LocationName.s2e5_aztec: 0xACA03E,
    LocationName.s2e5_model: 0xACA03F,
    # S2E6 locations
    LocationName.s2e6_urn_ped: 0xACA040,
    LocationName.s2e6_vonarburg: 0xACA041,
    LocationName.s2e6_on_fireplace: 0xACA042,
    LocationName.s2e6_mom: 0xACA043,
    LocationName.s2e6_in_fireplace: 0xACA044,
    LocationName.s2e6_monk: 0xACA045,
    LocationName.s2e6_ashes: 0xACA046,
    LocationName.s2e6_cardinal: 0xACA047,
    LocationName.s2e6_paradox: 0xACA048,
    # S2E7 locations
    LocationName.s2e7_bentley: 0xACA049,
    LocationName.s2e7_perch: 0xACA04A,
    LocationName.s2e7_bridge: 0xACA04B,
    LocationName.s2e7_rcoffin1: 0xACA04C,
    LocationName.s2e7_rcoffin2: 0xACA04D,
    LocationName.s2e7_rcoffin3: 0xACA04E,
    LocationName.s2e7_lcoffin: 0xACA04F,
    LocationName.s2e7_eyes: 0xACA050,
    # S2E8 locations
    LocationName.s2e8_trunk1: 0xACA051,
    LocationName.s2e8_trunk2: 0xACA052,
    LocationName.s2e8_ground: 0xACA053,
    LocationName.s2e8_pu_l: 0xACA054,
    LocationName.s2e8_pu_r: 0xACA055,
    LocationName.s2e8_sn: 0xACA056
}

endings_location_table = {
    LocationName.s1e1_end: None,
    LocationName.s1e2_end: None,
    LocationName.s1e3_end: None,
    LocationName.s1e4_end: None,
    LocationName.s2e1_end: None,
    LocationName.s2e2_end: None,
    LocationName.s2e3_end: None,
    LocationName.s2e4_end: None,
    LocationName.s2e5_end: None,
    LocationName.s2e6_end: None,
    LocationName.s2e7_end: None,
    LocationName.s2e8_end: None,
}

all_locations = {
    **s1_main_location_table,
    **s2_main_location_table,
}


def setup_locations():
    location_table = {**s1_main_location_table,
                      **s2_main_location_table,
                      **endings_location_table}

    return location_table


lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
