import typing

from BaseClasses import Location
from worlds.AutoWorld import World
from .Names import LocationName

class MMX2Location(Location):
    game = "Mega Man X2"

    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, name, address, parent)

STARTING_ID = 0xBE0C00

stage_location_table = {
    LocationName.intro_stage_boss:                      STARTING_ID + 0x0000,
    LocationName.wheel_gator_boss:                      STARTING_ID + 0x0001,
    LocationName.bubble_crab_boss:                      STARTING_ID + 0x0002,
    LocationName.flame_stag_boss:                       STARTING_ID + 0x0003,
    LocationName.morph_moth_boss:                       STARTING_ID + 0x0004,
    LocationName.morph_moth_mini_boss_1:                STARTING_ID + 0x0005,
    LocationName.morph_moth_mini_boss_2:                STARTING_ID + 0x0006,
    LocationName.magna_centipede_boss:                  STARTING_ID + 0x0007,
    LocationName.magna_centipede_mini_boss_1:           STARTING_ID + 0x0008,
    LocationName.magna_centipede_mini_boss_2:           STARTING_ID + 0x0009,
    LocationName.crystal_snail_boss:                    STARTING_ID + 0x000A,
    LocationName.crystal_snail_mini_boss_1:             STARTING_ID + 0x000B,
    LocationName.overdrive_ostrich_boss:                STARTING_ID + 0x000C,
    LocationName.wire_sponge_boss:                      STARTING_ID + 0x000D,
    LocationName.agile_defeated:                        STARTING_ID + 0x000E,
    LocationName.serges_defeated:                       STARTING_ID + 0x000F,
    LocationName.violen_defeated:                       STARTING_ID + 0x0010,
    LocationName.x_hunter_stage_1_boss:                 STARTING_ID + 0x0011,
    LocationName.x_hunter_stage_2_boss:                 STARTING_ID + 0x0012,
    LocationName.x_hunter_stage_3_boss:                 STARTING_ID + 0x0013,
    LocationName.x_hunter_stage_5_zero:                 STARTING_ID + 0x0014,
    LocationName.victory:                               STARTING_ID + 0x0015,
}

boss_rematches = {
    LocationName.x_hunter_stage_4_wheel_gator:          STARTING_ID + 0x0016,
    LocationName.x_hunter_stage_4_bubble_crab:          STARTING_ID + 0x0017,
    LocationName.x_hunter_stage_4_flame_stag:           STARTING_ID + 0x0018,
    LocationName.x_hunter_stage_4_morph_moth:           STARTING_ID + 0x0019,
    LocationName.x_hunter_stage_4_magna_centipede:      STARTING_ID + 0x001A,
    LocationName.x_hunter_stage_4_crystal_snail:        STARTING_ID + 0x001B,
    LocationName.x_hunter_stage_4_overdrive_ostrich:    STARTING_ID + 0x001C,
    LocationName.x_hunter_stage_4_wire_sponge:          STARTING_ID + 0x001D,
}

tank_pickups = {
    LocationName.wheel_gator_heart_tank:                STARTING_ID + 0x001E,
    LocationName.bubble_crab_heart_tank:                STARTING_ID + 0x001F,
    LocationName.flame_stag_heart_tank:                 STARTING_ID + 0x0020,
    LocationName.morph_moth_heart_tank:                 STARTING_ID + 0x0021,
    LocationName.magna_centipede_heart_tank:            STARTING_ID + 0x0022,
    LocationName.crystal_snail_heart_tank:              STARTING_ID + 0x0023,
    LocationName.overdrive_ostrich_heart_tank:          STARTING_ID + 0x0024,
    LocationName.wire_sponge_heart_tank:                STARTING_ID + 0x0025,
    LocationName.bubble_crab_sub_tank:                  STARTING_ID + 0x0026,
    LocationName.magna_centipede_sub_tank:              STARTING_ID + 0x0027,
    LocationName.flame_stag_sub_tank:                   STARTING_ID + 0x0028,
    LocationName.wire_sponge_sub_tank:                  STARTING_ID + 0x0029,
}

upgrade_pickups = {
    LocationName.wheel_gator_arms:                      STARTING_ID + 0x002A,
    LocationName.morph_moth_body:                       STARTING_ID + 0x002B,
    LocationName.crystal_snail_helmet:                  STARTING_ID + 0x002C,
    LocationName.overdrive_ostrich_leg:                 STARTING_ID + 0x002D,
    LocationName.x_hunter_stage_3_shoryuken:            STARTING_ID + 0x002E,
}

pickup_sanity = {
    LocationName.intro_hp_1:                            STARTING_ID + 0x0040,
    LocationName.intro_hp_2:                            STARTING_ID + 0x0041,
    LocationName.wheel_gator_hp_1:                      STARTING_ID + 0x0042,
    LocationName.wheel_gator_hp_2:                      STARTING_ID + 0x0043,
    LocationName.wheel_gator_1up:                       STARTING_ID + 0x0044,
    LocationName.wheel_gator_energy_1:                  STARTING_ID + 0x0045,
    LocationName.wheel_gator_hp_3:                      STARTING_ID + 0x0046,
    LocationName.wheel_gator_hp_4:                      STARTING_ID + 0x0047,
    LocationName.bubble_crab_1up:                       STARTING_ID + 0x0048,
    LocationName.bubble_crab_hp_1:                      STARTING_ID + 0x0049,
    LocationName.bubble_crab_hp_2:                      STARTING_ID + 0x004A,
    LocationName.bubble_crab_energy_1:                  STARTING_ID + 0x004B,
    LocationName.bubble_crab_hp_3:                      STARTING_ID + 0x004C,
    LocationName.bubble_crab_hp_4:                      STARTING_ID + 0x004D,
    LocationName.bubble_crab_energy_2:                  STARTING_ID + 0x004E,
    LocationName.bubble_crab_hp_5:                      STARTING_ID + 0x004F,
    LocationName.bubble_crab_hp_6:                      STARTING_ID + 0x0050,
    LocationName.flame_stag_1up_1:                      STARTING_ID + 0x0051,
    LocationName.flame_stag_hp_1:                       STARTING_ID + 0x0052,
    LocationName.flame_stag_energy_1:                   STARTING_ID + 0x0053,
    LocationName.flame_stag_hp_2:                       STARTING_ID + 0x0054,
    LocationName.flame_stag_energy_2:                   STARTING_ID + 0x0055,
    LocationName.flame_stag_hp_3:                       STARTING_ID + 0x0056,
    LocationName.flame_stag_hp_4:                       STARTING_ID + 0x0057,
    LocationName.flame_stag_1up_2:                      STARTING_ID + 0x0058,
    LocationName.flame_stag_hp_5:                       STARTING_ID + 0x0059,
    LocationName.flame_stag_energy_3:                   STARTING_ID + 0x005A,
    LocationName.flame_stag_hp_6:                       STARTING_ID + 0x005B,
    LocationName.flame_stag_hp_7:                       STARTING_ID + 0x005C,
    LocationName.flame_stag_energy_4:                   STARTING_ID + 0x005D,
    LocationName.flame_stag_hp_8:                       STARTING_ID + 0x005E,
    LocationName.flame_stag_1up_3:                      STARTING_ID + 0x005F,
    LocationName.flame_stag_hp_9:                       STARTING_ID + 0x0060,
    LocationName.morph_moth_1up_1:                      STARTING_ID + 0x0061,
    LocationName.morph_moth_1up_2:                      STARTING_ID + 0x0062,
    LocationName.morph_moth_hp_1:                       STARTING_ID + 0x0063,
    LocationName.morph_moth_hp_2:                       STARTING_ID + 0x0064,
    LocationName.morph_moth_hp_3:                       STARTING_ID + 0x0065,
    LocationName.morph_moth_hp_4:                       STARTING_ID + 0x0066,
    LocationName.morph_moth_hp_5:                       STARTING_ID + 0x0067,
    LocationName.magna_centipede_hp_1:                  STARTING_ID + 0x0068,
    LocationName.magna_centipede_hp_2:                  STARTING_ID + 0x0069,
    LocationName.crystal_snail_hp_1:                    STARTING_ID + 0x006A,
    LocationName.crystal_snail_energy_1:                STARTING_ID + 0x006B,
    LocationName.crystal_snail_hp_2:                    STARTING_ID + 0x008D,
    LocationName.crystal_snail_hp_3:                    STARTING_ID + 0x006C,
    LocationName.crystal_snail_1up_1:                   STARTING_ID + 0x006D,
    LocationName.crystal_snail_hp_4:                    STARTING_ID + 0x006E,
    LocationName.crystal_snail_1up_2:                   STARTING_ID + 0x006F,
    LocationName.overdrive_ostrich_hp_1:                STARTING_ID + 0x0070,
    LocationName.overdrive_ostrich_1up:                 STARTING_ID + 0x0071,
    LocationName.overdrive_ostrich_hp_2:                STARTING_ID + 0x0072,
    LocationName.overdrive_ostrich_energy_1:            STARTING_ID + 0x0073,
    LocationName.overdrive_ostrich_hp_3:                STARTING_ID + 0x0074,
    LocationName.overdrive_ostrich_energy_2:            STARTING_ID + 0x0075,
    LocationName.wire_sponge_1up_1:                     STARTING_ID + 0x0076,
    LocationName.wire_sponge_hp_1:                      STARTING_ID + 0x0077,
    LocationName.wire_sponge_hp_2:                      STARTING_ID + 0x0078,
    LocationName.x_hunter_stage_1_1up_1:                STARTING_ID + 0x0079,
    LocationName.x_hunter_stage_1_hp:                   STARTING_ID + 0x007A,
    LocationName.x_hunter_stage_1_1up_2:                STARTING_ID + 0x007B,
    LocationName.x_hunter_stage_2_hp:                   STARTING_ID + 0x007C,
    LocationName.x_hunter_stage_2_1up:                  STARTING_ID + 0x007D,
    LocationName.x_hunter_stage_3_hp_1:                 STARTING_ID + 0x007E,
    LocationName.x_hunter_stage_3_1up_1:                STARTING_ID + 0x007F,
    LocationName.x_hunter_stage_3_hp_2:                 STARTING_ID + 0x0080,
    LocationName.x_hunter_stage_3_hp_3:                 STARTING_ID + 0x0081,
    LocationName.x_hunter_stage_3_hp_4:                 STARTING_ID + 0x0082,
    LocationName.x_hunter_stage_3_hp_5:                 STARTING_ID + 0x0083,
    LocationName.x_hunter_stage_3_hp_6:                 STARTING_ID + 0x0084,
    LocationName.x_hunter_stage_3_1up_2:                STARTING_ID + 0x0085,
    LocationName.x_hunter_stage_3_hp_7:                 STARTING_ID + 0x0086,
    LocationName.x_hunter_stage_3_hp_8:                 STARTING_ID + 0x0087,
    LocationName.x_hunter_stage_3_1up_3:                STARTING_ID + 0x0088,
    LocationName.x_hunter_stage_3_1up_4:                STARTING_ID + 0x0089,
    LocationName.wheel_gator_hp_5:                      STARTING_ID + 0x008A,
    LocationName.wheel_gator_hp_6:                      STARTING_ID + 0x008B,
    LocationName.wheel_gator_hp_7:                      STARTING_ID + 0x008C,
}

stage_clears = {
    LocationName.wheel_gator_clear:                     STARTING_ID + 0x00C0,
    LocationName.bubble_crab_clear:                     STARTING_ID + 0x00C1,
    LocationName.flame_stag_clear:                      STARTING_ID + 0x00C2,
    LocationName.morph_moth_clear:                      STARTING_ID + 0x00C3,
    LocationName.magna_centipede_clear:                 STARTING_ID + 0x00C4,
    LocationName.crystal_snail_clear:                   STARTING_ID + 0x00C5,
    LocationName.overdrive_ostrich_clear:               STARTING_ID + 0x00C6,
    LocationName.wire_sponge_clear:                     STARTING_ID + 0x00C7,
    LocationName.intro_stage_clear:                     STARTING_ID + 0x00C8,
    LocationName.x_hunter_stage_4_clear:                STARTING_ID + 0x00C9,
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
    "X-Hunter Base 1": {location for location in all_locations.keys() if "X-Hunter Base 1 - " in location},
    "X-Hunter Base 2": {location for location in all_locations.keys() if "X-Hunter Base 2 - " in location},
    "X-Hunter Base 3": {location for location in all_locations.keys() if "X-Hunter Base 3 - " in location},
    "X-Hunter Base 4": {location for location in all_locations.keys() if "X-Hunter Base 4 - " in location},
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
