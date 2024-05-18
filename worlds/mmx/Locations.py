import typing

from BaseClasses import Location
from worlds.AutoWorld import World
from .Names import LocationName

class MMXLocation(Location):
    game = "Mega Man X"

    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, name, address, parent)

STARTING_ID = 0xBE0800

stage_location_table = {
    LocationName.armored_armadillo_boss:                STARTING_ID + 0x0000,
    LocationName.chill_penguin_boss:                    STARTING_ID + 0x0001,
    LocationName.spark_mandrill_boss:                   STARTING_ID + 0x0002,
    LocationName.launch_octopus_boss:                   STARTING_ID + 0x0003,
    LocationName.boomer_kuwanger_boss:                  STARTING_ID + 0x0004,
    LocationName.sting_chameleon_boss:                  STARTING_ID + 0x0005,
    LocationName.storm_eagle_boss:                      STARTING_ID + 0x0006,
    LocationName.flame_mammoth_boss:                    STARTING_ID + 0x0007,
    LocationName.sigma_fortress_1_bospider:             STARTING_ID + 0x0008,
    LocationName.sigma_fortress_1_vile:                 STARTING_ID + 0x0009,
    LocationName.sigma_fortress_1_boomer_kuwanger:      STARTING_ID + 0x000A,
    LocationName.sigma_fortress_2_chill_penguin:        STARTING_ID + 0x000B,
    LocationName.sigma_fortress_2_storm_eagle:          STARTING_ID + 0x000C,
    LocationName.sigma_fortress_2_rangda_bangda:        STARTING_ID + 0x000D,
    LocationName.sigma_fortress_3_armored_armadillo:    STARTING_ID + 0x000E,
    LocationName.sigma_fortress_3_sting_chameleon:      STARTING_ID + 0x000F,
    LocationName.sigma_fortress_3_spark_mandrill:       STARTING_ID + 0x0010,
    LocationName.sigma_fortress_3_launch_octopus:       STARTING_ID + 0x0011,
    LocationName.sigma_fortress_3_flame_mammoth:        STARTING_ID + 0x0012,
    LocationName.sigma_fortress_3_d_rex:                STARTING_ID + 0x0013,
    LocationName.sigma_fortress_4_velguarder:           STARTING_ID + 0x0014,
    LocationName.sigma_fortress_4_sigma:                STARTING_ID + 0x0015,
    LocationName.intro_completed:                       STARTING_ID + 0x0016,
    LocationName.intro_mini_boss_1:                     STARTING_ID + 0x001E,
    LocationName.intro_mini_boss_2:                     STARTING_ID + 0x001F,
    LocationName.launch_octopus_mini_boss_1:            STARTING_ID + 0x0017,
    LocationName.launch_octopus_mini_boss_2:            STARTING_ID + 0x0018,
    LocationName.launch_octopus_mini_boss_3:            STARTING_ID + 0x0019,
    LocationName.launch_octopus_mini_boss_4:            STARTING_ID + 0x001A,
    LocationName.spark_mandrill_mini_boss:              STARTING_ID + 0x001B,
    LocationName.armored_armadillo_mini_boss_1:         STARTING_ID + 0x001C,
    LocationName.armored_armadillo_mini_boss_2:         STARTING_ID + 0x001D,
}

tank_pickups = {
    LocationName.armored_armadillo_heart_tank:      STARTING_ID + 0x0030,
    LocationName.armored_armadillo_sub_tank:        STARTING_ID + 0x0031,
    LocationName.chill_penguin_heart_tank:          STARTING_ID + 0x0032,
    LocationName.spark_mandrill_sub_tank:           STARTING_ID + 0x0033,
    LocationName.spark_mandrill_heart_tank:         STARTING_ID + 0x0034,
    LocationName.launch_octopus_heart_tank:         STARTING_ID + 0x0035,
    LocationName.boomer_kuwanger_heart_tank:        STARTING_ID + 0x0036,
    LocationName.sting_chameleon_heart_tank:        STARTING_ID + 0x0037,
    LocationName.storm_eagle_heart_tank:            STARTING_ID + 0x0038,
    LocationName.storm_eagle_sub_tank:              STARTING_ID + 0x0039,
    LocationName.flame_mammoth_heart_tank:          STARTING_ID + 0x003A,
    LocationName.flame_mammoth_sub_tank:            STARTING_ID + 0x003B,
}

upgrade_pickups = {
    LocationName.armored_armadillo_hadouken:    STARTING_ID + 0x0040,
    LocationName.chill_penguin_legs:            STARTING_ID + 0x0041,
    LocationName.sting_chameleon_body:          STARTING_ID + 0x0042,
    LocationName.storm_eagle_helmet:            STARTING_ID + 0x0043,
    LocationName.flame_mammoth_arms:            STARTING_ID + 0x0044,
}

pickup_sanity = {
    LocationName.intro_hp_1:                STARTING_ID + 0x0050,
    LocationName.intro_hp_2:                STARTING_ID + 0x0051,
    LocationName.armored_armadillo_hp_1:    STARTING_ID + 0x0052,
    LocationName.armored_armadillo_hp_2:    STARTING_ID + 0x0053,
    LocationName.armored_armadillo_hp_3:    STARTING_ID + 0x0054,
    LocationName.launch_octopus_hp_1:       STARTING_ID + 0x0055,
    LocationName.sting_chameleon_1up:       STARTING_ID + 0x0056,
    LocationName.sting_chameleon_hp_1:      STARTING_ID + 0x0057,
    LocationName.storm_eagle_1up_1:         STARTING_ID + 0x0058,
    LocationName.storm_eagle_1up_2:         STARTING_ID + 0x0059,
    LocationName.storm_eagle_1up_3:         STARTING_ID + 0x006B,
    LocationName.storm_eagle_hp_1:          STARTING_ID + 0x005A,
    LocationName.storm_eagle_hp_2:          STARTING_ID + 0x005B,
    LocationName.storm_eagle_hp_3:          STARTING_ID + 0x005C,
    #LocationName.storm_eagle_hp_4:          STARTING_ID + 0x005D,
    #LocationName.storm_eagle_energy_1:      STARTING_ID + 0x005E,
    LocationName.flame_mammoth_hp_1:        STARTING_ID + 0x005F,
    LocationName.flame_mammoth_hp_2:        STARTING_ID + 0x0060,
    LocationName.flame_mammoth_1up:         STARTING_ID + 0x0061,
    LocationName.sigma_fortress_3_hp_1:     STARTING_ID + 0x0062,
    LocationName.sigma_fortress_3_hp_2:     STARTING_ID + 0x0063,
    LocationName.sigma_fortress_3_energy_1: STARTING_ID + 0x0064,
    LocationName.sigma_fortress_3_hp_3:     STARTING_ID + 0x0065,
    LocationName.sigma_fortress_3_energy_2: STARTING_ID + 0x0066,
    LocationName.sigma_fortress_3_hp_4:     STARTING_ID + 0x0067,
    LocationName.sigma_fortress_3_energy_3: STARTING_ID + 0x0068,
    LocationName.sigma_fortress_3_1up:      STARTING_ID + 0x0069,
    LocationName.chill_penguin_hp_1:        STARTING_ID + 0x006A,
}

stage_clears = {
    LocationName.armored_armadillo_clear:   STARTING_ID + 0x0070,
    LocationName.chill_penguin_clear:       STARTING_ID + 0x0071,
    LocationName.spark_mandrill_clear:      STARTING_ID + 0x0072,
    LocationName.launch_octopus_clear:      STARTING_ID + 0x0073,
    LocationName.boomer_kuwanger_clear:     STARTING_ID + 0x0074,
    LocationName.sting_chameleon_clear:     STARTING_ID + 0x0075,
    LocationName.storm_eagle_clear:         STARTING_ID + 0x0076,
    LocationName.flame_mammoth_clear:       STARTING_ID + 0x0077
}

all_locations = {
    **stage_clears,
    **stage_location_table,
    **tank_pickups,
    **upgrade_pickups,
    **pickup_sanity
}

location_table = {}

location_groups = {
    "Bosses": {location for location in all_locations.keys() if "Defeated" in location},
    "Heart Tanks": {location for location in all_locations.keys() if "- Heart Tank" in location},
    "Sub Tanks": {location for location in all_locations.keys() if "- Sub Tank" in location},
    "Upgrade Capsules": {location for location in all_locations.keys() if "Capsule" in location},
    "Intro Stage": {location for location in all_locations.keys() if "Intro Stage - " in location},
    "Armored Armadillo Stage": {location for location in all_locations.keys() if "Armored Armadillo - " in location},
    "Chill Penguin Stage": {location for location in all_locations.keys() if "Chill Penguin - " in location},
    "Spark Mandrill Stage": {location for location in all_locations.keys() if "Spark Mandrill - " in location},
    "Launch Octopus Stage": {location for location in all_locations.keys() if "Launch Octopus - " in location},
    "Boomer Kuwanger Stage": {location for location in all_locations.keys() if "Boomer Kuwanger - " in location},
    "Sting Chameleon Stage": {location for location in all_locations.keys() if "Sting Chameleon - " in location},
    "Storm Eagle Stage": {location for location in all_locations.keys() if "Storm Eagle - " in location},
    "Flame Mammoth Stage": {location for location in all_locations.keys() if "Flame Mammoth - " in location},
    "Sigma's Fortress Stage 1": {
        LocationName.sigma_fortress_1_boomer_kuwanger,
        LocationName.sigma_fortress_1_bospider,
        LocationName.sigma_fortress_1_vile,
    },
    "Sigma's Fortress Stage 2": {
        LocationName.sigma_fortress_2_chill_penguin,
        LocationName.sigma_fortress_2_rangda_bangda,
        LocationName.sigma_fortress_2_storm_eagle,
    },
    "Sigma's Fortress Stage 3": {
        LocationName.sigma_fortress_3_1up,
        LocationName.sigma_fortress_3_armored_armadillo,
        LocationName.sigma_fortress_3_sting_chameleon,
        LocationName.sigma_fortress_3_launch_octopus,
        LocationName.sigma_fortress_3_flame_mammoth,
        LocationName.sigma_fortress_3_spark_mandrill,
        LocationName.sigma_fortress_3_d_rex,
        LocationName.sigma_fortress_3_energy_1,
        LocationName.sigma_fortress_3_energy_2,
        LocationName.sigma_fortress_3_energy_3,
        LocationName.sigma_fortress_3_hp_1,
        LocationName.sigma_fortress_3_hp_2,
        LocationName.sigma_fortress_3_hp_3,
        LocationName.sigma_fortress_3_hp_4,
    },
}
    
def setup_locations(world: World):
    location_table = {
        **stage_clears,
        **stage_location_table,
        **tank_pickups,
        **upgrade_pickups,
    }

    if world.options.pickupsanity.value:
        location_table.update({**pickup_sanity})

    return location_table

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
