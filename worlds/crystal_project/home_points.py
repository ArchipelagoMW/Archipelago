from typing import List, Optional

from .options import CrystalProjectOptions
from .rules import CrystalProjectLogic
from .locations import LocationData
from .constants.ap_regions import *
from .constants.display_regions import *
from .constants.keys import *
from .constants.teleport_stones import *

def get_home_points(player: Optional[int], options: Optional[CrystalProjectOptions]) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    home_point_table: List[LocationData] = [
        LocationData(SPAWNING_MEADOWS_AP_REGION, "AP Spawn Point", 5003),
        LocationData(SPAWNING_MEADOWS_AP_REGION, "Old Nan's Watering Hole", 59),

        LocationData(DELENDE_AP_REGION, "The Pale Grotto Entrance", 44),
        LocationData(DELENDE_AP_REGION, "Soiled Den", 66),
        LocationData(DELENDE_AP_REGION, "Cabin On The Cliff", 94),
        LocationData(DELENDE_AP_REGION, "Fish Hatchery", 127),
        LocationData(DELENDE_AP_REGION, "Delende Peak", 160),
        LocationData(DELENDE_AP_REGION, "Delende Falls", 186),

        LocationData(MERCURY_SHRINE_AP_REGION, "Mercury Shrine", 152),

        LocationData(THE_PALE_GROTTO_AP_REGION, "The Pale Grotto Ruins", 148),

        LocationData(SEASIDE_CLIFFS_AP_REGION, "Seaside Cliffs Camp", 72),

        LocationData(YAMAGAWA_MA_AP_REGION, "Yamagawa M.A. Summit", 165),

        LocationData(PROVING_MEADOWS_AP_REGION, "Proving Meadows Camp", 119),

        LocationData(SKUMPARADISE_AP_REGION, "Skumparadise Entrance", 637),
        LocationData(SKUMPARADISE_AP_REGION, "Skumparadise Depths", 331),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, "Skumparadise Exit", 231),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "Gaea Shrine", 112),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "East Market District", 374),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "Bulletin Square", 890),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "Know-It-All Ducks' House", 559),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "West Market District", 2026),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "Training Grounds", 3057),

        LocationData(CAPITAL_JAIL_AP_REGION, "Capital Jail Entrance", 643),
        LocationData(CAPITAL_JAIL_AP_REGION, "Capital Jail Dark Wing", 915, lambda state: logic.has_key(state, DARK_WING_KEY)),

        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, "Quintar Enthusiast's House", 440),
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, "Rent-A-Quintar", 462),
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, "Quintar Sanctum", 917, lambda state: logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME) or logic.has_vertical_movement(state)),

        LocationData(QUINTAR_SANCTUM_AP_REGION, "Quintar Nameko", 968),

        LocationData(BOOMER_SOCIETY_AP_REGION, "Boomer Society", 170),

        LocationData(OKIMOTO_NS_AP_REGION, "Okimoto N.S. Base", 335),
        LocationData(OKIMOTO_NS_AP_REGION, "Ninja Yashiki", 366),

        LocationData(SALMON_PASS_EAST_AP_REGION, "Salmon Pass Entrance", 367),

        LocationData(SALMON_RIVER_AP_REGION, "Salmon Shack", 1076),

        LocationData(CASTLE_SEQUOIA_AP_REGION, "Castle Sequoia Foyer", 514),

        LocationData(POKO_POKO_DESERT_AP_REGION, "Labyrinth Encampment", 2712, lambda state: logic.has_horizontal_movement(state) and logic.has_vertical_movement(state)),

        LocationData(SARA_SARA_BAZAAR_AP_REGION, "Sara Sara Bazaar Port", 941),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, "Poko Poko West Gate", 3783),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, "Poko Poko East Gate", 3784),

        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, "Ibek's Cave", 2005, lambda state: logic.has_vertical_movement(state)),
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, "Beach Bird's Nest", 2709, lambda state: logic.has_vertical_movement(state)),

        LocationData(BEAURIOR_VOLCANO_AP_REGION, "Beaurior Rock", 1792),
        #TODO: put volcano peak in separate ap region instead of included in Beaurior Rock (also items nearby, not just homepoint stone)
        LocationData(BEAURIOR_ROCK_AP_REGION, "Beaurior Volcano Peak", 3037, lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_key(state, BEAURIOR_BOSS_KEY)),

        LocationData(BEAURIOR_ROCK_AP_REGION, "Boss Room", 822, lambda state: logic.has_key(state, SMALL_KEY, 4)),

        LocationData(ANCIENT_RESERVOIR_AP_REGION, "Ancient Reservoir Entrance", 1124),
        LocationData(ANCIENT_RESERVOIR_AP_REGION, "Main Reservoir Chamber", 1660),

        LocationData(SHOUDU_PROVINCE_AP_REGION, "Shoudu Fields", 576, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "Shoudu Market", 577, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "Shoudu Port", 672),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "Shanty Inn", 1523),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "Sky Arena", 1524, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "Prize Counter", 2731, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "Shoudu Elevator", 3523, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),

        LocationData(GANYMEDE_SHRINE_AP_REGION, "Ganymede Shrine", 1573),

        LocationData(THE_UNDERCITY_AP_REGION, "The Undercity", 1266, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),

        LocationData(PIPELINE_NORTH_AP_REGION, "Capital Pipeline", 1127),
        LocationData(PIPELINE_SOUTH_AP_REGION, "East Capital Pipeline", 1420),

        LocationData(SEQUOIA_ATHENAEUM_ENTRANCE_AP_REGION, "Sequoia Athenaeum", 2361),
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Ice Pass", 2413),
        LocationData(SOUVENIR_SHOP_AP_REGION, "Tall, Tall Souvenir Shop", 1260),
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Land's End Cottage", 2564),
        LocationData(SLIP_GLIDE_RIDE_EXIT_AP_REGION, "Slip Glide Ride Exit", 2743),
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Ice Fisher's Hut", 3014),
        LocationData(UPPER_ICE_LAKES_AP_REGION, "Triton Shrine", 3018),
        LocationData(TALL_TALL_SAVE_POINT_AP_REGION, "Tall, Tall Heights", 3047),

        LocationData(PEAK_RAMPARTS_AP_REGION, "East Ramparts", 1375, lambda state: logic.has_glide(state)),
        LocationData(PEAK_RAMPARTS_AP_REGION, "West Ramparts", 1376, lambda state: logic.has_glide(state)),

        LocationData(SLIP_GLIDE_RIDE_ENTRANCE_AP_REGION, "Slip Glide Ride Entrance", 1550),

        LocationData(LANDS_END_AP_REGION, "Summit Shrine", 1559),

        LocationData(QUINTAR_RESERVE_AP_REGION, "Dione Shrine", 1595),

        LocationData(EUROPA_SHRINE_AP_REGION, "Europa Shrine", 1626),

        LocationData(JIDAMBA_EACLANEYA_AP_REGION, "Eaclaneya Entrance", 1402),
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, "Salmon Room", 2474),

        LocationData(LABYRINTH_CORE_AP_REGION, "Ancient Labyrinth Core", 1739),

        LocationData(DIONE_SHRINE_AP_REGION, "Flyer's Lookout", 2141),

        LocationData(THE_SEQUOIA_AP_REGION, "Top Of The Sequoia", 2452),

        LocationData(THE_CHALICE_OF_TAR_AP_REGION, "The Chalice of Tar", 3055),

        LocationData(THE_OPEN_SEA_AP_REGION, "Sailor's Raft", 3775),

        LocationData(THE_NEW_WORLD_AP_REGION, "Astley's Shrine", 3776),
        LocationData(THE_NEW_WORLD_AP_REGION, "Astley's Keep", 3777),
        LocationData(THE_NEW_WORLD_AP_REGION, "Discipline Hollow", 3797),

        LocationData(CONTINENTAL_TRAM_AP_REGION, "Platform A", 3780),

        LocationData(NEPTUNE_SHRINE_AP_REGION, "Neptune Shrine", 3781),
    ]

    return home_point_table