import typing

from BaseClasses import Location


class LegacyLocation(Location):
    game: str = "Rogue Legacy"


base_location_table = {
    # Manor Upgrades
    "Manor Ground Road": 91000,
    "Manor Main Base": 91001,
    "Manor Main Bottom Window": 91002,
    "Manor Main Top Window": 91003,
    "Manor Main Roof": 91004,
    "Manor Left Wing Base": 91005,
    "Manor Left Wing Window": 91006,
    "Manor Left Wing Roof": 91007,
    "Manor Left Big Base": 91008,
    "Manor Left Big Upper 1": 91009,
    "Manor Left Big Upper 2": 91010,
    "Manor Left Big Windows": 91011,
    "Manor Left Big Roof": 91012,
    "Manor Left Far Base": 91013,
    "Manor Left Far Roof": 91014,
    "Manor Left Extension": 91015,
    "Manor Left Tree 1": 91016,
    "Manor Left Tree 2": 91017,
    "Manor Right Wing Base": 91018,
    "Manor Right Wing Window": 91019,
    "Manor Right Wing Roof": 91020,
    "Manor Right Big Base": 91021,
    "Manor Right Big Upper": 91022,
    "Manor Right Big Roof": 91023,
    "Manor Right High Base": 91024,
    "Manor Right High Upper": 91025,
    "Manor Right High Tower": 91026,
    "Manor Right Extension": 91027,
    "Manor Right Tree": 91028,
    "Manor Observatory Base": 91029,
    "Manor Observatory Telescope": 91030,

    # Main Bosses
    "Khindr's Reward Chest": 91100,
    "Alexander's Reward Chest": 91102,
    "Ponce de Leon's Reward Chest": 91104,
    "Herodotus's Reward Chest": 91106,

    # Special Rooms
    "Jukebox": 91200,

    # Special Locations
    "Castle Hamson": None,
    "Forest Abkhazia": None,
    "The Maya": None,
    "The Land of Darkness": None,
    "Victory": None,
}

diary_location_table = {f"Diary {i + 1}": i + 91300 for i in range(0, 25)}

fairy_chest_location_table = {
    **{f"Castle Hamson Fairy Chest {i + 1}": i + 91400 for i in range(0, 50)},
    **{f"Forest Abkhazia Fairy Chest {i + 1}": i + 91450 for i in range(0, 50)},
    **{f"The Maya Fairy Chest {i + 1}": i + 91500 for i in range(0, 50)},
    **{f"The Land of Darkness Fairy Chest {i + 1}": i + 91550 for i in range(0, 50)},
}

chest_location_table = {
    **{f"Castle Hamson Chest {i + 1}": i + 91600 for i in range(0, 100)},
    **{f"Forest Abkhazia Chest {i + 1}": i + 91700 for i in range(0, 100)},
    **{f"The Maya Chest {i + 1}": i + 91800 for i in range(0, 100)},
    **{f"The Land of Darkness Chest {i + 1}": i + 91900 for i in range(0, 100)},
}

location_table = {
    **base_location_table,
    **diary_location_table,
    **fairy_chest_location_table,
    **chest_location_table,
}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in location_table.items()}
