import typing

from BaseClasses import Location
from worlds.AutoWorld import World
from .Names import LocationName

class MMX2Location(Location):
    game = "Mega Man X2"

    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, name, address, parent)

starting_id = 0xBE0C00

stage_location_table = {
    LocationName.intro_stage_boss:                      starting_id + 0x0000,
    LocationName.wheel_gator_boss:                      starting_id + 0x0001,
    LocationName.bubble_crab_boss:                      starting_id + 0x0002,
    LocationName.flame_stag_boss:                       starting_id + 0x0003,
    LocationName.morph_moth_boss:                       starting_id + 0x0004,
    LocationName.morph_moth_mini_boss_1:                starting_id + 0x0005,
    LocationName.morph_moth_mini_boss_2:                starting_id + 0x0006,
    LocationName.magna_centipede_boss:                  starting_id + 0x0007,
    LocationName.magna_centipede_mini_boss_1:           starting_id + 0x0008,
    LocationName.magna_centipede_mini_boss_2:           starting_id + 0x0009,
    LocationName.crystal_snail_boss:                    starting_id + 0x000A,
    LocationName.crystal_snail_mini_boss_1:             starting_id + 0x000B,
    LocationName.overdrive_ostrich_boss:                starting_id + 0x000C,
    LocationName.wire_sponge_boss:                      starting_id + 0x000D,
    LocationName.agile_defeated:                        starting_id + 0x000E,
    LocationName.serges_defeated:                       starting_id + 0x000F,
    LocationName.violen_defeated:                       starting_id + 0x0010,
    LocationName.x_hunter_stage_1_boss:                 starting_id + 0x0011,
    LocationName.x_hunter_stage_2_boss:                 starting_id + 0x0012,
    LocationName.x_hunter_stage_3_boss:                 starting_id + 0x0013,
    LocationName.x_hunter_stage_5_zero:                 starting_id + 0x0014,
    LocationName.victory:                               starting_id + 0x0015,
}

boss_rematches = {
    LocationName.x_hunter_stage_4_wheel_gator:          starting_id + 0x0016,
    LocationName.x_hunter_stage_4_bubble_crab:          starting_id + 0x0017,
    LocationName.x_hunter_stage_4_flame_stag:           starting_id + 0x0018,
    LocationName.x_hunter_stage_4_morph_moth:           starting_id + 0x0019,
    LocationName.x_hunter_stage_4_magna_centipede:      starting_id + 0x001A,
    LocationName.x_hunter_stage_4_crystal_snail:        starting_id + 0x001B,
    LocationName.x_hunter_stage_4_overdrive_ostrich:    starting_id + 0x001C,
    LocationName.x_hunter_stage_4_wire_sponge:          starting_id + 0x001D,
}

tank_pickups = {
    LocationName.wheel_gator_heart_tank:                starting_id + 0x001E,
    LocationName.bubble_crab_heart_tank:                starting_id + 0x001F,
    LocationName.flame_stag_heart_tank:                 starting_id + 0x0020,
    LocationName.morph_moth_heart_tank:                 starting_id + 0x0021,
    LocationName.magna_centipede_heart_tank:            starting_id + 0x0022,
    LocationName.crystal_snail_heart_tank:              starting_id + 0x0023,
    LocationName.overdrive_ostrich_heart_tank:          starting_id + 0x0024,
    LocationName.wire_sponge_heart_tank:                starting_id + 0x0025,
    LocationName.bubble_crab_sub_tank:                  starting_id + 0x0026,
    LocationName.magna_centipede_sub_tank:              starting_id + 0x0027,
    LocationName.flame_stag_sub_tank:                   starting_id + 0x0028,
    LocationName.wire_sponge_sub_tank:                  starting_id + 0x0029,
}

upgrade_pickups = {
    LocationName.wheel_gator_arms:                      starting_id + 0x002A,
    LocationName.morph_moth_body:                       starting_id + 0x002B,
    LocationName.crystal_snail_helmet:                  starting_id + 0x002C,
    LocationName.overdrive_ostrich_leg:                 starting_id + 0x002D,
}

pickup_sanity = {
}

stage_clears = {
    LocationName.wheel_gator_clear:                     starting_id + 0x0080,
    LocationName.bubble_crab_clear:                     starting_id + 0x0081,
    LocationName.flame_stag_clear:                      starting_id + 0x0082,
    LocationName.morph_moth_clear:                      starting_id + 0x0083,
    LocationName.magna_centipede_clear:                 starting_id + 0x0084,
    LocationName.crystal_snail_clear:                   starting_id + 0x0085,
    LocationName.overdrive_ostrich_clear:               starting_id + 0x0086,
    LocationName.wire_sponge_clear:                     starting_id + 0x0087,
    LocationName.intro_stage_clear:                     starting_id + 0x0088,
}

all_locations = {
    **stage_clears,
    **boss_rematches,
    **stage_location_table,
    **tank_pickups,
    **upgrade_pickups,
    **pickup_sanity
}

location_table = {}

location_groups = {
    "Mavericks": {
        LocationName.wheel_gator_boss,
        LocationName.bubble_crab_boss,
        LocationName.flame_stag_boss,
        LocationName.morph_moth_boss,
        LocationName.magna_centipede_boss,
        LocationName.crystal_snail_boss,
        LocationName.overdrive_ostrich_boss,
        LocationName.wire_sponge_boss,
    },
    "Bosses": {
        LocationName.intro_stage_boss,
        LocationName.wheel_gator_boss,
        LocationName.bubble_crab_boss,
        LocationName.flame_stag_boss,
        LocationName.morph_moth_boss,
        LocationName.morph_moth_mini_boss_1,
        LocationName.morph_moth_mini_boss_2,
        LocationName.magna_centipede_boss,
        LocationName.magna_centipede_mini_boss_1,
        LocationName.magna_centipede_mini_boss_2,
        LocationName.crystal_snail_boss,
        LocationName.crystal_snail_mini_boss_1,
        LocationName.overdrive_ostrich_boss,
        LocationName.wire_sponge_boss,
        LocationName.agile_defeated,
        LocationName.serges_defeated,
        LocationName.violen_defeated,
        LocationName.x_hunter_stage_1_boss,
        LocationName.x_hunter_stage_2_boss,
        LocationName.x_hunter_stage_3_boss,
        LocationName.x_hunter_stage_5_zero,
    },
    "Heart Tanks": {location for location in all_locations.keys() if "- Heart Tank" in location},
    "Sub Tanks": {location for location in all_locations.keys() if "- Sub Tank" in location},
    "Upgrade Capsules": {location for location in all_locations.keys() if "Capsule" in location},
    "Intro Stage": {location for location in all_locations.keys() if "Intro Stage - " in location},
    "Wheel Gator Stage": {location for location in all_locations.keys() if "Wheel Gator - " in location},
    "Bubble Crab Stage": {location for location in all_locations.keys() if "Bubble Crab - " in location},
    "Flame Stag Stage": {location for location in all_locations.keys() if "Flame Stag - " in location},
    "Morph Moth Stage": {location for location in all_locations.keys() if "Morph Moth - " in location},
    "Magna Centipede Stage": {location for location in all_locations.keys() if "Magna Centipede - " in location},
    "Crystal Snail Stage": {location for location in all_locations.keys() if "Crystal Snail - " in location},
    "Overdrive Ostrich Stage": {location for location in all_locations.keys() if "Overdrive Ostrich - " in location},
    "Wire Sponge Stage": {location for location in all_locations.keys() if "Wire Sponge - " in location},
    "X Hunter Base 1": {location for location in all_locations.keys() if "X Hunter Base 1 - " in location},
    "X Hunter Base 2": {location for location in all_locations.keys() if "X Hunter Base 2 - " in location},
    "X Hunter Base 3": {location for location in all_locations.keys() if "X Hunter Base 3 - " in location},
    "X Hunter Base 4": {location for location in all_locations.keys() if "X Hunter Base 4 - " in location},
}
    
def setup_locations(world: World):
    location_table = {
        **stage_clears,
        **stage_location_table,
        **tank_pickups,
        **upgrade_pickups,
    }

    if world.options.base_boss_rematch_count.value != 0:
        location_table.update({**boss_rematches})
    if world.options.pickupsanity.value:
        location_table.update({**pickup_sanity})

    return location_table

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
