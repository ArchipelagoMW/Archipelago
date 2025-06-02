from locations import LocationData
from typing import List, Optional, Callable, NamedTuple
from .options import CrystalProjectOptions
from .rules import CrystalProjectLogic

def get_home_points(player: Optional[int], options: Optional[CrystalProjectOptions]) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    home_point_table: List[LocationData] = [
        LocationData("Spawning Meadows", "Old Nan's Watering Hole", 59),

        LocationData("Delende", "The Pale Grotto Entrance", 44),
        LocationData("Delende", "Soiled Den", 66),
        LocationData("Delende", "Cabin On The Cliff", 94),
        LocationData("Delende", "Fish Hatchery", 127),
        LocationData("Delende", "Delende Peak", 160),
        LocationData("Delende", "Delende Falls", 186),

        LocationData("Mercury Shrine", "Mercury Shrine", 152),

        LocationData("Pale Grotto", "The Pale Grotto Ruins", 148),

        LocationData("Seaside Cliffs", "Seaside Cliffs Camp", 72),

        LocationData("Yamagawa M.A.", "Yamagawa M.A. Summit", 165),

        LocationData("Proving Meadows", "Proving Meadows Camp", 119),

        LocationData("Skumparadise", "Skumparadise Entrance", 637),
        LocationData("Skumparadise", "Skumparadise Depths", 331),

        LocationData("Capital Sequoia", "Skumparadise Exit", 231),
        LocationData("Capital Sequoia", "Gaea Shrine", 112),
        LocationData("Capital Sequoia", "East Market District", 374),
        LocationData("Capital Sequoia", "Bulletin Square", 890),
        LocationData("Capital Sequoia", "Know-It-All Ducks' House", 559),
        LocationData("Capital Sequoia", "West Market District", 2026),
        LocationData("Capital Sequoia", "Training Grounds", 3057),

        LocationData("Capital Jail", "Capital Jail Entrance", 643),
        LocationData("Capital Jail", "Capital Jail Dark Wing", 915),

        LocationData("Rolling Quintar Fields", "Quintar Enthusiast's House", 440),
        LocationData("Rolling Quintar Fields", "Rent-A-Quintar", 462),
        LocationData("Rolling Quintar Fields", "Quintar Sanctum", 917),

        LocationData("Quintar Sanctum", "Quintar Nameko", 968),

        LocationData("Boomer Society", "Boomer Society", 170),

        LocationData("Okimoto N.S.", "Okimoto N.S. Base", 335),
        LocationData("Okimoto N.S.", "Ninja Yashiki", 366),

        LocationData("Salmon Pass", "Salmon Pass Entrance", 367),

        LocationData("Salmon River", "Salmon Shack", 1076),

        LocationData("Castle Sequoia", "Castle Sequoia Foyer", 514),

        LocationData("Poko Poko Desert", "Labyrinth Encampment", 2712),

        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar Port", 941),
        LocationData("Sara Sara Bazaar", "Poko Poko West Gate", 3783),
        LocationData("Sara Sara Bazaar", "Poko Poko East Gate", 3784),

        LocationData("Sara Sara Beach", "Ibek's Cave", 2005),
        LocationData("Sara Sara Beach", "Beach Bird's Nest", 2709),

        LocationData("Beaurior Volcano", "Beaurior Rock", 1792),
        LocationData("Beaurior Volcano", "Beaurior Volcano Peak", 3037),

        LocationData("Beaurior Rock", "Boss Room", 822),

        LocationData("Ancient Reservoir", "Ancient Reservoir Entrance", 1124),
        LocationData("Ancient Reservoir", "Main Reservoir Chamber", 1660),

        LocationData("Shoudu Province", "Shoudu Fields", 576),
        LocationData("Shoudu Province", "Shoudu Market", 577),
        LocationData("Shoudu Province", "Shoudu Port", 672),
        LocationData("Shoudu Province", "Shanty Inn", 1523),
        LocationData("Shoudu Province", "Sky Arena", 1524),
        LocationData("Shoudu Province", "Prize Counter", 2731),
        LocationData("Shoudu Province", "Shoudu Elevator", 3523),

        LocationData("Ganymede Shrine", "Ganymede Shrine", 1573),

        LocationData("The Undercity", "The Undercity", 1266),

        LocationData("Capital Pipeline", "Capital Pipeline", 1127),
        LocationData("Capital Pipeline", "East Capital Pipeline", 1420),

        LocationData("Tall Tall Heights", "Sequoia Athenaeum", 2361),
        LocationData("Tall Tall Heights", "Ice Pass", 2413),
        LocationData("Tall Tall Heights", "Tall, Tall Souvenir Shop", 1260),
        LocationData("Tall Tall Heights", "Land's End Cottage", 2564),
        LocationData("Tall Tall Heights", "Slip Glide Ride Exit", 2743),
        LocationData("Tall Tall Heights", "Ice Fisher's Hut", 3014),
        LocationData("Tall Tall Heights", "Triton Shrine", 3018),
        LocationData("Tall Tall Heights", "Tall, Tall Heights", 3047),

        LocationData("Castle Ramparts", "East Ramparts", 1375),
        LocationData("Castle Ramparts", "West Ramparts", 1376),

        LocationData("Slip Glide Ride", "Slip Glide Ride Entrance", 1550),

        LocationData("Lands End", "Summit Shrine", 1559),

        LocationData("Quintar Reserve", "Dione Shrine", 1595),

        LocationData("Jidamba Tangle", "Europa Shrine", 1626),

        LocationData("Jidamba Eaclaneya", "Eaclaneya Entrance", 1402),
        LocationData("Jidamba Eaclaneya", "Salmon Room", 2474),

        LocationData("Ancient Labyrinth", "Ancient Labyrinth Core", 1739),

        LocationData("Dione Shrine", "Flyer's Lookout", 2141),

        LocationData("The Sequoia", "Top Of The Sequoia", 2452),

        LocationData("The Chalice of Tar", "The Chalice of Tar", 3055),

        LocationData("The Open Sea", "Sailor's Raft", 3775),

        LocationData("The New World", "Astley's Shrine", 3776),
        LocationData("The New World", "Astley's Keep", 3777),
        LocationData("The New World", "Discipline Hollow", 3797),

        LocationData("Continental Tram", "Platform A", 3780),

        LocationData("Neptune Shrine", "Neptune Shrine", 3781)
    ]

    return home_point_table