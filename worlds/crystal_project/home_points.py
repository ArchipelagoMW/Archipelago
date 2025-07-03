from locations import LocationData
from typing import List, Optional

from .options import CrystalProjectOptions
from .rules import CrystalProjectLogic
from .constants.regions import *
from .constants.keys import *
from .constants.key_items import *
from .constants.teleport_stones import *

def get_home_points(player: Optional[int], options: Optional[CrystalProjectOptions]) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    home_point_table: List[LocationData] = [
        LocationData(SPAWNING_MEADOWS, "AP Spawn Point", 5003),
        LocationData(SPAWNING_MEADOWS, "Old Nan's Watering Hole", 59),

        LocationData(DELENDE, "The Pale Grotto Entrance", 44),
        LocationData(DELENDE, "Soiled Den", 66),
        LocationData(DELENDE, "Cabin On The Cliff", 94),
        LocationData(DELENDE, "Fish Hatchery", 127),
        LocationData(DELENDE, "Delende Peak", 160),
        LocationData(DELENDE, "Delende Falls", 186),

        LocationData(MERCURY_SHRINE, "Mercury Shrine", 152),

        LocationData(THE_PALE_GROTTO, "The Pale Grotto Ruins", 148),

        LocationData(SEASIDE_CLIFFS, "Seaside Cliffs Camp", 72),

        LocationData(YAMAGAWA_MA, "Yamagawa M.A. Summit", 165),

        LocationData(PROVING_MEADOWS, "Proving Meadows Camp", 119),

        LocationData(SKUMPARADISE, "Skumparadise Entrance", 637),
        LocationData(SKUMPARADISE, "Skumparadise Depths", 331),

        LocationData(CAPITAL_SEQUOIA, "Skumparadise Exit", 231),
        LocationData(CAPITAL_SEQUOIA, "Gaea Shrine", 112),
        LocationData(CAPITAL_SEQUOIA, "East Market District", 374),
        LocationData(CAPITAL_SEQUOIA, "Bulletin Square", 890),
        LocationData(CAPITAL_SEQUOIA, "Know-It-All Ducks' House", 559),
        LocationData(CAPITAL_SEQUOIA, "West Market District", 2026),
        LocationData(CAPITAL_SEQUOIA, "Training Grounds", 3057),

        LocationData(CAPITAL_JAIL, "Capital Jail Entrance", 643),
        LocationData(CAPITAL_JAIL, "Capital Jail Dark Wing", 915, lambda state: logic.has_key(state, DARK_WING_KEY)),

        LocationData(ROLLING_QUINTAR_FIELDS, "Quintar Enthusiast's House", 440),
        LocationData(ROLLING_QUINTAR_FIELDS, "Rent-A-Quintar", 462),
        LocationData(ROLLING_QUINTAR_FIELDS, "Quintar Sanctum", 917, lambda state: logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS) or logic.has_vertical_movement(state)),

        LocationData(QUINTAR_SANCTUM, "Quintar Nameko", 968),

        LocationData(BOOMER_SOCIETY, "Boomer Society", 170),

        LocationData(OKIMOTO_NS, "Okimoto N.S. Base", 335),
        LocationData(OKIMOTO_NS, "Ninja Yashiki", 366),

        LocationData(SALMON_PASS, "Salmon Pass Entrance", 367),

        LocationData(SALMON_RIVER, "Salmon Shack", 1076),

        LocationData(CASTLE_SEQUOIA, "Castle Sequoia Foyer", 514),

        LocationData(POKO_POKO_DESERT, "Labyrinth Encampment", 2712, lambda state: logic.has_horizontal_movement(state) and logic.has_vertical_movement(state)),

        LocationData(SARA_SARA_BAZAAR, "Sara Sara Bazaar Port", 941),
        LocationData(SARA_SARA_BAZAAR, "Poko Poko West Gate", 3783),
        LocationData(SARA_SARA_BAZAAR, "Poko Poko East Gate", 3784),

        LocationData(SARA_SARA_BEACH_EAST, "Ibek's Cave", 2005, lambda state: logic.has_vertical_movement(state)),
        LocationData(SARA_SARA_BEACH_WEST, "Beach Bird's Nest", 2709, lambda state: logic.has_vertical_movement(state)),

        LocationData(BEAURIOR_VOLCANO, "Beaurior Rock", 1792),
        LocationData(BEAURIOR_VOLCANO, "Beaurior Volcano Peak", 3037, lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_key(state, BEAURIOR_BOSS_KEY)),

        LocationData(BEAURIOR_ROCK, "Boss Room", 822, lambda state: logic.has_key(state, SMALL_KEY, 4)),

        LocationData(ANCIENT_RESERVOIR, "Ancient Reservoir Entrance", 1124),
        LocationData(ANCIENT_RESERVOIR, "Main Reservoir Chamber", 1660),

        LocationData(SHOUDU_PROVINCE, "Shoudu Fields", 576, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE, player=player) or state.can_reach(QUINTAR_RESERVE, player=player)),
        LocationData(SHOUDU_PROVINCE, "Shoudu Market", 577, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE, player=player) or state.can_reach(QUINTAR_RESERVE, player=player)),
        LocationData(SHOUDU_PROVINCE, "Shoudu Port", 672),
        LocationData(SHOUDU_PROVINCE, "Shanty Inn", 1523, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE, player=player) or state.can_reach(QUINTAR_RESERVE, player=player)),
        LocationData(SHOUDU_PROVINCE, "Sky Arena", 1524, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(QUINTAR_RESERVE, player=player)),
        LocationData(SHOUDU_PROVINCE, "Prize Counter", 2731, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE, player=player) or state.can_reach(QUINTAR_RESERVE, player=player)),
        LocationData(SHOUDU_PROVINCE, "Shoudu Elevator", 3523, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE, player=player) or state.can_reach(QUINTAR_RESERVE, player=player)),

        LocationData(GANYMEDE_SHRINE, "Ganymede Shrine", 1573),

        LocationData(THE_UNDERCITY, "The Undercity", 1266),

        LocationData(CAPITAL_PIPELINE, "Capital Pipeline", 1127),
        LocationData(CAPITAL_PIPELINE, "East Capital Pipeline", 1420, lambda state: logic.has_vertical_movement(state) or logic.has_swimming(state) or logic.has_key(state, TRAM_KEY)),

        LocationData(TALL_TALL_HEIGHTS, "Sequoia Athenaeum", 2361, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)),
        LocationData(TALL_TALL_HEIGHTS, "Ice Pass", 2413),
        LocationData(TALL_TALL_HEIGHTS, "Tall, Tall Souvenir Shop", 1260, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)),
        LocationData(TALL_TALL_HEIGHTS, "Land's End Cottage", 2564),
        LocationData(TALL_TALL_HEIGHTS, "Slip Glide Ride Exit", 2743, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)),
        LocationData(TALL_TALL_HEIGHTS, "Ice Fisher's Hut", 3014),
        LocationData(TALL_TALL_HEIGHTS, "Triton Shrine", 3018, lambda state: logic.has_vertical_movement(state) or state.has(TRITON_STONE, player)),
        LocationData(TALL_TALL_HEIGHTS, "Tall, Tall Heights", 3047),

        LocationData(CASTLE_RAMPARTS, "East Ramparts", 1375, lambda state: logic.has_glide(state)),
        LocationData(CASTLE_RAMPARTS, "West Ramparts", 1376, lambda state: logic.has_glide(state)),

        LocationData(SLIP_GLIDE_RIDE, "Slip Glide Ride Entrance", 1550),

        LocationData(LANDS_END, "Summit Shrine", 1559),

        LocationData(QUINTAR_RESERVE, "Dione Shrine", 1595),

        LocationData(JIDAMBA_TANGLE, "Europa Shrine", 1626),

        LocationData(JIDAMBA_EACLANEYA, "Eaclaneya Entrance", 1402),
        LocationData(JIDAMBA_EACLANEYA, "Salmon Room", 2474),

        LocationData(ANCIENT_LABYRINTH, "Ancient Labyrinth Core", 1739, lambda state: state.has(ANCIENT_TABLET_B, player) and state.has(ANCIENT_TABLET_C, player)),

        LocationData(DIONE_SHRINE, "Flyer's Lookout", 2141),

        LocationData(THE_SEQUOIA, "Top Of The Sequoia", 2452),

        LocationData(THE_CHALICE_OF_TAR, "The Chalice of Tar", 3055),

        LocationData(THE_OPEN_SEA, "Sailor's Raft", 3775),

        LocationData(THE_NEW_WORLD, "Astley's Shrine", 3776),
        LocationData(THE_NEW_WORLD, "Astley's Keep", 3777),
        LocationData(THE_NEW_WORLD, "Discipline Hollow", 3797),

        LocationData(CONTINENTAL_TRAM, "Platform A", 3780),

        LocationData(NEPTUNE_SHRINE, "Neptune Shrine", 3781),
    ]

    return home_point_table