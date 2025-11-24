from typing import List, Optional

from .constants.ap_regions import *
from .constants.display_regions import *
from .constants.keys import *
from .locations import LocationData
from .options import CrystalProjectOptions
from .rules import CrystalProjectLogic
#Remember if you update the AP Region a Home Point is in or its name, go change it in the Menu connections function in the region.py file
def get_home_points(player: Optional[int], options: Optional[CrystalProjectOptions]) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    home_point_table: List[LocationData] = [
        LocationData(SPAWNING_MEADOWS_AP_REGION, "HomePoint - AP Spawn Point", 5003),
        LocationData(SPAWNING_MEADOWS_AP_REGION, "HomePoint - Old Nan's Watering Hole", 59),

        LocationData(DELENDE_PLAINS_AP_REGION, "HomePoint - The Pale Grotto Entrance", 44),
        LocationData(DELENDE_PLAINS_AP_REGION, "HomePoint - Soiled Den", 66),
        LocationData(DELENDE_PLAINS_AP_REGION, "HomePoint - Fish Hatchery", 127),
        LocationData(DELENDE_HIGH_BRIDGES_AP_REGION, "HomePoint - Cabin On The Cliff", 94),
        LocationData(DELENDE_HIGH_BRIDGES_AP_REGION, "HomePoint - Delende Falls", 186),
        LocationData(DELENDE_PEAK_AP_REGION, "HomePoint - Delende Peak", 160),

        LocationData(MERCURY_SHRINE_AP_REGION, "HomePoint - Mercury Shrine", 152),

        LocationData(THE_PALE_GROTTO_AP_REGION, "HomePoint - The Pale Grotto Ruins", 148),

        LocationData(SEASIDE_CLIFFS_AP_REGION, "HomePoint - Seaside Cliffs Camp", 72),

        LocationData(YAMAGAWA_MA_AP_REGION, "HomePoint - Yamagawa M.A. Summit", 165),

        LocationData(PROVING_MEADOWS_AP_REGION, "HomePoint - Proving Meadows Camp", 119),

        LocationData(SKUMPARADISE_AP_REGION, "HomePoint - Skumparadise Entrance", 637),
        LocationData(SKUMPARADISE_AP_REGION, "HomePoint - Skumparadise Depths", 331),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, "HomePoint - Skumparadise Exit", 231),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "HomePoint - Gaea Shrine", 112),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "HomePoint - East Market District", 374),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "HomePoint - Bulletin Square", 890),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "HomePoint - Know-It-All Ducks' House", 559),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "HomePoint - West Market District", 2026),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "HomePoint - Training Grounds", 3057),

        LocationData(CAPITAL_JAIL_AP_REGION, "HomePoint - Capital Jail Entrance", 643),
        LocationData(CAPITAL_JAIL_AP_REGION, "HomePoint - Capital Jail Dark Wing", 915, lambda state: logic.has_key(state, DARK_WING_KEY)),

        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, "HomePoint - Quintar Enthusiast's House", 440),
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, "HomePoint - Rent-A-Quintar", 462),
        LocationData(SANCTUM_ENTRANCE_AP_REGION, "HomePoint - Quintar Sanctum", 917),

        LocationData(QUINTAR_SANCTUM_AP_REGION, "HomePoint - Quintar Nameko", 968),

        LocationData(BOOMER_SOCIETY_AP_REGION, "HomePoint - Boomer Society", 170),

        LocationData(OKIMOTO_NS_AP_REGION, "HomePoint - Okimoto N.S. Base", 335),
        LocationData(OKIMOTO_NS_AP_REGION, "HomePoint - Ninja Yashiki", 366),

        LocationData(SALMON_PASS_EAST_AP_REGION, "HomePoint - Salmon Pass Entrance", 367),

        LocationData(SALMON_RIVER_AP_REGION, "HomePoint - Salmon Shack", 1076),

        LocationData(CASTLE_SEQUOIA_AP_REGION, "HomePoint - Castle Sequoia Foyer", 514),

        LocationData(TOWER_OF_ZOT_AP_REGION, "HomePoint - Labyrinth Encampment", 2712),

        LocationData(SARA_SARA_BAZAAR_AP_REGION, "HomePoint - Sara Sara Bazaar Port", 941),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, "HomePoint - Poko Poko West Gate", 3783),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, "HomePoint - Poko Poko East Gate", 3784),

        LocationData(IBEK_CAVE_MOUTH_AP_REGION, "HomePoint - Ibek's Cave", 2005),
        LocationData(BEACH_BIRDS_NEST_AP_REGION, "HomePoint - Beach Bird's Nest", 2709),

        LocationData(BEAURIOR_VOLCANO_AP_REGION, "HomePoint - Beaurior Rock", 1792),
        #TODO: put volcano peak in separate ap region instead of included in Beaurior Rock (also items nearby, not just homepoint stone)
        LocationData(BEAURIOR_ROCK_AP_REGION, "HomePoint - Beaurior Volcano Peak", 3037, lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_key(state, BEAURIOR_BOSS_KEY)),

        LocationData(BEAURIOR_ROCK_AP_REGION, "HomePoint - Boss Room", 822, lambda state: logic.has_key(state, SMALL_KEY, 4)),

        LocationData(ANCIENT_RESERVOIR_AP_REGION, "HomePoint - Ancient Reservoir Entrance", 1124),
        LocationData(ANCIENT_RESERVOIR_AP_REGION, "HomePoint - Main Reservoir Chamber", 1660),

        LocationData(SHOUDU_PROVINCE_AP_REGION, "HomePoint - Shoudu Fields", 576, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "HomePoint - Shoudu Market", 577, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "HomePoint - Shoudu Port", 672),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "HomePoint - Shanty Inn", 1523),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "HomePoint - Sky Arena", 1524, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "HomePoint - Prize Counter", 2731, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, "HomePoint - Shoudu Elevator", 3523, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),

        LocationData(GANYMEDE_SHRINE_AP_REGION, "HomePoint - Ganymede Shrine", 1573),

        LocationData(THE_UNDERCITY_AP_REGION, "HomePoint - The Undercity", 1266, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),

        LocationData(PIPELINE_NORTH_AP_REGION, "HomePoint - Capital Pipeline", 1127),
        LocationData(PIPELINE_SOUTH_AP_REGION, "HomePoint - East Capital Pipeline", 1420),

        LocationData(SEQUOIA_ATHENAEUM_ENTRANCE_AP_REGION, "HomePoint - Sequoia Athenaeum", 2361),
        LocationData(LOWER_ICE_LAKES_AP_REGION, "HomePoint - Ice Pass", 2413),
        LocationData(SOUVENIR_SHOP_AP_REGION, "HomePoint - Tall, Tall Souvenir Shop", 1260),
        LocationData(LOWER_ICE_LAKES_AP_REGION, "HomePoint - Land's End Cottage", 2564),
        LocationData(SLIP_GLIDE_RIDE_EXIT_AP_REGION, "HomePoint - Slip Glide Ride Exit", 2743),
        LocationData(LOWER_ICE_LAKES_AP_REGION, "HomePoint - Ice Fisher's Hut", 3014),
        LocationData(UPPER_ICE_LAKES_AP_REGION, "HomePoint - Triton Shrine", 3018),
        LocationData(TALL_TALL_SAVE_POINT_AP_REGION, "HomePoint - Tall, Tall Heights", 3047),

        LocationData(PEAK_RAMPARTS_AP_REGION, "HomePoint - East Ramparts", 1375, lambda state: logic.has_glide(state)),
        LocationData(PEAK_RAMPARTS_AP_REGION, "HomePoint - West Ramparts", 1376, lambda state: logic.has_glide(state)),

        LocationData(SLIP_GLIDE_RIDE_ENTRANCE_AP_REGION, "HomePoint - Slip Glide Ride Entrance", 1550),

        LocationData(LANDS_END_AP_REGION, "HomePoint - Summit Shrine", 1559),

        LocationData(QUINTAR_RESERVE_AP_REGION, "HomePoint - Dione Shrine", 1595),

        LocationData(EUROPA_SHRINE_AP_REGION, "HomePoint - Europa Shrine", 1626),

        LocationData(JIDAMBA_EACLANEYA_AP_REGION, "HomePoint - Eaclaneya Entrance", 1402),
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, "HomePoint - Salmon Room", 2474),

        LocationData(LABYRINTH_CORE_AP_REGION, "HomePoint - Ancient Labyrinth Core", 1739),

        LocationData(DIONE_SHRINE_AP_REGION, "HomePoint - Flyer's Lookout", 2141),

        LocationData(THE_SEQUOIA_AP_REGION, "HomePoint - Top Of The Sequoia", 2452),

        LocationData(THE_CHALICE_OF_TAR_AP_REGION, "HomePoint - The Chalice of Tar", 3055),

        LocationData(THE_OPEN_SEA_AP_REGION, "HomePoint - Sailor's Raft", 3775),

        LocationData(THE_NEW_WORLD_AP_REGION, "HomePoint - Astley's Shrine", 3776),
        LocationData(THE_NEW_WORLD_AP_REGION, "HomePoint - Astley's Keep", 3777),
        LocationData(THE_NEW_WORLD_AP_REGION, "HomePoint - Discipline Hollow", 3797),

        LocationData(CONTINENTAL_TRAM_AP_REGION, "HomePoint - Platform A", 3780),

        LocationData(NEPTUNE_SHRINE_AP_REGION, "HomePoint - Neptune Shrine", 3781),
    ]

    return home_point_table