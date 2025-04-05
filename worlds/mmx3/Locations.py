import typing

from BaseClasses import Location
from worlds.AutoWorld import World
from .Names import LocationName

class MMX3Location(Location):
    game = "Mega Man X3"

    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, name, address, parent)

starting_id = 0xBE0000

stage_location_table = {
    LocationName.intro_stage_boss:                  starting_id + 0x0000,
    LocationName.intro_stage_mini_boss:             starting_id + 0x0001,
    LocationName.blizzard_buffalo_boss:             starting_id + 0x0002,
    LocationName.toxic_seahorse_boss :              starting_id + 0x0003,
    LocationName.toxic_seahorse_mini_boss:          starting_id + 0x0004,
    LocationName.tunnel_rhino_boss:                 starting_id + 0x0005,
    LocationName.tunnel_rhino_mini_boss:            starting_id + 0x0006,
    LocationName.volt_catfish_boss:                 starting_id + 0x0007,
    LocationName.crush_crawfish_boss:               starting_id + 0x0008,
    LocationName.neon_tiger_boss:                   starting_id + 0x0009,
    LocationName.neon_tiger_mini_boss:              starting_id + 0x000A,
    LocationName.gravity_beetle_boss:               starting_id + 0x000B,
    LocationName.blast_hornet_boss:                 starting_id + 0x000C,
    LocationName.blast_hornet_mini_boss:            starting_id + 0x000D,
    LocationName.doppler_lab_1_boss:                starting_id + 0x000E,
    LocationName.doppler_lab_1_mini_boss:           starting_id + 0x000F,
    LocationName.doppler_lab_2_boss:                starting_id + 0x0010,
    #LocationName.doppler_lab_2_mini_boss:           starting_id + 0x0011,
    LocationName.doppler_lab_3_boss:                starting_id + 0x0012,
    LocationName.victory:                           starting_id + 0x001C,
    LocationName.vile_stage_boss:                   starting_id + 0x001D,
    LocationName.bit_defeat:                        starting_id + 0x001E,
    LocationName.byte_defeat:                       starting_id + 0x001F
}

boss_rematches = {
    LocationName.doppler_lab_3_blizzard_buffalo:    starting_id + 0x0013,
    LocationName.doppler_lab_3_toxic_seahorse:      starting_id + 0x0014,
    LocationName.doppler_lab_3_tunnel_rhino:        starting_id + 0x0015,
    LocationName.doppler_lab_3_volt_catfish:        starting_id + 0x0016,
    LocationName.doppler_lab_3_crush_crawfish:      starting_id + 0x0017,
    LocationName.doppler_lab_3_neon_tiger:          starting_id + 0x0018,
    LocationName.doppler_lab_3_gravity_beetle:      starting_id + 0x0019,
    LocationName.doppler_lab_3_blast_hornet:        starting_id + 0x001A,
}

tank_pickups = {
    LocationName.blizzard_buffalo_heart_tank:   starting_id + 0x0020,
    LocationName.blizzard_buffalo_sub_tank:     starting_id + 0x0021,
    LocationName.toxic_seahorse_heart_tank:     starting_id + 0x0022,
    LocationName.tunnel_rhino_heart_tank:       starting_id + 0x0023,
    LocationName.tunnel_rhino_sub_tank:         starting_id + 0x0024,
    LocationName.volt_catfish_heart_tank:       starting_id + 0x0025,
    LocationName.volt_catfish_sub_tank:         starting_id + 0x0026,
    LocationName.crush_crawfish_heart_tank:     starting_id + 0x0027,
    LocationName.neon_tiger_heart_tank:         starting_id + 0x0028,
    LocationName.neon_tiger_sub_tank:           starting_id + 0x0029,
    LocationName.gravity_beetle_heart_tank:     starting_id + 0x002A,
    LocationName.blast_hornet_heart_tank:       starting_id + 0x002B
}

upgrade_pickups = {
    LocationName.blizzard_buffalo_legs:     starting_id + 0x002C,
    LocationName.toxic_seahorse_leg:        starting_id + 0x002D,
    LocationName.tunnel_rhino_helmet:       starting_id + 0x002E,
    LocationName.volt_catfish_body:         starting_id + 0x002F,
    LocationName.crush_crawfish_body:       starting_id + 0x0030,
    LocationName.neon_tiger_arms:           starting_id + 0x0031,
    LocationName.gravity_beetle_arms:       starting_id + 0x0032,
    LocationName.blast_hornet_helmet:       starting_id + 0x0033,
    #LocationName.doppler_lab_1_gold_armor:  starting_id + 0x0034,
    #LocationName.doppler_lab_2_z_saber:     starting_id + 0x0035,
}

ride_armor_pickups = {
    LocationName.toxic_seahorse_kangaroo_ride:  starting_id + 0x0036,
    LocationName.crush_crawfish_hawk_ride:      starting_id + 0x0037,
    LocationName.gravity_beetle_frog_ride:      starting_id + 0x0038,
    LocationName.blast_hornet_chimera_ride:     starting_id + 0x0039,
}

pickup_sanity = {
    LocationName.intro_stage_hp_1:          starting_id + 0x0040,
    LocationName.intro_stage_hp_2:          starting_id + 0x0041,
    LocationName.blizzard_buffalo_hp_1:     starting_id + 0x0042,
    LocationName.blizzard_buffalo_hp_2:     starting_id + 0x0043,
    LocationName.blizzard_buffalo_hp_3:     starting_id + 0x0044,
    LocationName.blizzard_buffalo_hp_4:     starting_id + 0x0045,
    LocationName.blizzard_buffalo_hp_5:     starting_id + 0x0046,
    LocationName.toxic_seahorse_hp_1:       starting_id + 0x0047,
    LocationName.toxic_seahorse_hp_2:       starting_id + 0x0048,
    LocationName.toxic_seahorse_hp_3:       starting_id + 0x0049,
    LocationName.volt_catfish_energy_1:     starting_id + 0x004A,
    LocationName.volt_catfish_energy_2:     starting_id + 0x004B,
    LocationName.volt_catfish_energy_3:     starting_id + 0x004C,
    LocationName.volt_catfish_hp_1:         starting_id + 0x004D,
    LocationName.volt_catfish_hp_2:         starting_id + 0x004E,
    LocationName.volt_catfish_hp_3:         starting_id + 0x004F,
    LocationName.volt_catfish_hp_4:         starting_id + 0x0050,
    LocationName.volt_catfish_hp_5:         starting_id + 0x0051,
    LocationName.crush_crawfish_1up_1:      starting_id + 0x0052,
    LocationName.crush_crawfish_1up_2:      starting_id + 0x0053,
    LocationName.crush_crawfish_energy_1:   starting_id + 0x0054,
    LocationName.crush_crawfish_hp_1:       starting_id + 0x0055,
    LocationName.crush_crawfish_hp_2:       starting_id + 0x0056,
    LocationName.crush_crawfish_hp_3:       starting_id + 0x0057,
    LocationName.crush_crawfish_hp_4:       starting_id + 0x0058,
    LocationName.crush_crawfish_hp_5:       starting_id + 0x0059,
    LocationName.crush_crawfish_hp_6:       starting_id + 0x005A,
    LocationName.neon_tiger_hp_1:           starting_id + 0x005B,
    LocationName.neon_tiger_hp_2:           starting_id + 0x005C,
    LocationName.neon_tiger_hp_3:           starting_id + 0x005D,
    LocationName.gravity_beetle_1up:        starting_id + 0x005E,
    LocationName.gravity_beetle_energy_1:   starting_id + 0x005F,
    LocationName.gravity_beetle_energy_2:   starting_id + 0x0060,
    LocationName.gravity_beetle_hp_1:       starting_id + 0x0061,
    LocationName.gravity_beetle_hp_2:       starting_id + 0x0062,
    LocationName.gravity_beetle_hp_3:       starting_id + 0x0063,
    LocationName.gravity_beetle_hp_4:       starting_id + 0x0064,
    LocationName.gravity_beetle_hp_5:       starting_id + 0x0065,
    LocationName.gravity_beetle_hp_6:       starting_id + 0x0066,
    LocationName.blast_hornet_hp_1:         starting_id + 0x0067,
    LocationName.blast_hornet_hp_2:         starting_id + 0x0068,
    LocationName.doppler_lab_1_energy:      starting_id + 0x0069,
    LocationName.doppler_lab_1_hp_1:        starting_id + 0x006A,
    LocationName.doppler_lab_1_hp_2:        starting_id + 0x006B,
    LocationName.doppler_lab_3_hp:          starting_id + 0x006C,
    LocationName.vile_stage_energy:         starting_id + 0x006D,
    LocationName.vile_stage_hp_1:           starting_id + 0x006E,
    LocationName.vile_stage_hp_2:           starting_id + 0x006F,
    LocationName.vile_stage_hp_3:           starting_id + 0x0070,
    LocationName.vile_stage_hp_4:           starting_id + 0x0071,
    LocationName.vile_stage_hp_5:           starting_id + 0x0072,
    LocationName.vile_stage_hp_6:           starting_id + 0x0073,
    LocationName.vile_stage_hp_7:           starting_id + 0x0074,
    LocationName.vile_stage_hp_8:           starting_id + 0x0075,
    LocationName.vile_stage_hp_9:           starting_id + 0x0076,
    LocationName.vile_stage_1up:            starting_id + 0x0077,
    LocationName.tunnel_rhino_energy_1:     starting_id + 0x0078,
    LocationName.tunnel_rhino_hp_1:         starting_id + 0x0079
}

stage_clears = {
    LocationName.blizzard_buffalo_clear:    starting_id + 0x0080,
    LocationName.toxic_seahorse_clear:      starting_id + 0x0081,
    LocationName.tunnel_rhino_clear:        starting_id + 0x0082,
    LocationName.volt_catfish_clear:        starting_id + 0x0083,
    LocationName.crush_crawfish_clear:      starting_id + 0x0084,
    LocationName.neon_tiger_clear:          starting_id + 0x0085,
    LocationName.gravity_beetle_clear:      starting_id + 0x0086,
    LocationName.blast_hornet_clear:        starting_id + 0x0087,
    LocationName.intro_stage_clear:         starting_id + 0x0088,
}

all_locations = {
    **stage_clears,
    **boss_rematches,
    **stage_location_table,
    **tank_pickups,
    **upgrade_pickups,
    **ride_armor_pickups,
    **pickup_sanity
}

location_table = {}

location_groups = {
    "Mavericks": {
            LocationName.blizzard_buffalo_boss,
            LocationName.toxic_seahorse_boss,
            LocationName.tunnel_rhino_boss,
            LocationName.volt_catfish_boss,
            LocationName.crush_crawfish_boss,
            LocationName.neon_tiger_boss,
            LocationName.gravity_beetle_boss,
            LocationName.blast_hornet_boss,
        },
    "Bosses": {
            LocationName.intro_stage_boss,
            LocationName.intro_stage_mini_boss,
            LocationName.blizzard_buffalo_boss,
            LocationName.toxic_seahorse_boss,
            LocationName.toxic_seahorse_mini_boss,
            LocationName.tunnel_rhino_boss,
            LocationName.tunnel_rhino_mini_boss,
            LocationName.volt_catfish_boss,
            LocationName.crush_crawfish_boss,
            LocationName.neon_tiger_boss,
            LocationName.neon_tiger_mini_boss,
            LocationName.gravity_beetle_boss,
            LocationName.blast_hornet_boss,
            LocationName.blast_hornet_mini_boss,
            LocationName.doppler_lab_1_boss,
            LocationName.doppler_lab_1_mini_boss,
            LocationName.doppler_lab_2_boss,
            LocationName.doppler_lab_3_boss,
            LocationName.vile_stage_boss,
            LocationName.bit_defeat,
            LocationName.byte_defeat,
        },
    "Heart Tanks": {location for location in all_locations.keys() if "- Heart Tank" in location},
    "Sub Tanks": {location for location in all_locations.keys() if "- Sub Tank" in location},
    "Upgrade Capsules": {location for location in all_locations.keys() if "Capsule" in location},
    "Ride Armors": {location for location in all_locations.keys() if "Ride Armor" in location},
    "Intro Stage": {location for location in all_locations.keys() if "Hunter Base Stage - " in location},
    "Hunter Base Stage": {location for location in all_locations.keys() if "Hunter Base Stage - " in location},
    "Blast Hornet Stage": {location for location in all_locations.keys() if "Blast Hornet Stage - " in location},
    "Blizzard Buffalo Stage": {location for location in all_locations.keys() if "Blizzard Buffalo Stage - " in location},
    "Gravity Beetle Stage": {location for location in all_locations.keys() if "Gravity Beetle Stage - " in location},
    "Toxic Seahorse Stage": {location for location in all_locations.keys() if "Toxic Seahorse Stage - " in location},
    "Volt Catfish Stage": {location for location in all_locations.keys() if "Volt Catfish Stage - " in location},
    "Crush Crawfish Stage": {location for location in all_locations.keys() if "Crush Crawfish Stage - " in location},
    "Tunnel Rhino Stage": {location for location in all_locations.keys() if "Tunnel Rhino Stage - " in location},
    "Neon Tiger Stage": {location for location in all_locations.keys() if "Neon Tiger Stage - " in location},
    "Vile's Stage": {location for location in all_locations.keys() if "Vile's Stage - " in location},
    "Dr. Doppler's Lab 1": {location for location in all_locations.keys() if "Dr. Doppler's Lab 1 - " in location},
    "Dr. Doppler's Lab 3": {location for location in all_locations.keys() if "Dr. Doppler's Lab 3 - " in location},
}
    
def setup_locations(world: World):
    location_table = {
        **stage_clears,
        **stage_location_table,
        **tank_pickups,
        **upgrade_pickups,
        **ride_armor_pickups,
    }

    if world.options.doppler_lab_3_boss_rematch_count.value != 0:
        location_table.update({**boss_rematches})
    if world.options.pickupsanity.value:
        location_table.update({**pickup_sanity})

    return location_table

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
