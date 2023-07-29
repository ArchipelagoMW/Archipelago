from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class RLLocation(Location):
    game: str = "Rogue Legacy"


class RLLocationData(NamedTuple):
    category: str
    code: Optional[int] = None


def get_locations_by_category(category: str) -> Dict[str, RLLocationData]:
    location_dict: Dict[str, RLLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict


location_table: Dict[str, RLLocationData] = {
    # Manor Renovation
    "Manor - Ground Road":                      RLLocationData("Manor",   91_000),
    "Manor - Main Base":                        RLLocationData("Manor",   91_001),
    "Manor - Main Bottom Window":               RLLocationData("Manor",   91_002),
    "Manor - Main Top Window":                  RLLocationData("Manor",   91_003),
    "Manor - Main Rooftop":                     RLLocationData("Manor",   91_004),
    "Manor - Left Wing Base":                   RLLocationData("Manor",   91_005),
    "Manor - Left Wing Window":                 RLLocationData("Manor",   91_006),
    "Manor - Left Wing Rooftop":                RLLocationData("Manor",   91_007),
    "Manor - Left Big Base":                    RLLocationData("Manor",   91_008),
    "Manor - Left Big Upper 1":                 RLLocationData("Manor",   91_009),
    "Manor - Left Big Upper 2":                 RLLocationData("Manor",   91_010),
    "Manor - Left Big Windows":                 RLLocationData("Manor",   91_011),
    "Manor - Left Big Rooftop":                 RLLocationData("Manor",   91_012),
    "Manor - Left Far Base":                    RLLocationData("Manor",   91_013),
    "Manor - Left Far Roof":                    RLLocationData("Manor",   91_014),
    "Manor - Left Extension":                   RLLocationData("Manor",   91_015),
    "Manor - Left Tree 1":                      RLLocationData("Manor",   91_016),
    "Manor - Left Tree 2":                      RLLocationData("Manor",   91_017),
    "Manor - Right Wing Base":                  RLLocationData("Manor",   91_018),
    "Manor - Right Wing Window":                RLLocationData("Manor",   91_019),
    "Manor - Right Wing Rooftop":               RLLocationData("Manor",   91_020),
    "Manor - Right Big Base":                   RLLocationData("Manor",   91_021),
    "Manor - Right Big Upper":                  RLLocationData("Manor",   91_022),
    "Manor - Right Big Rooftop":                RLLocationData("Manor",   91_023),
    "Manor - Right High Base":                  RLLocationData("Manor",   91_024),
    "Manor - Right High Upper":                 RLLocationData("Manor",   91_025),
    "Manor - Right High Tower":                 RLLocationData("Manor",   91_026),
    "Manor - Right Extension":                  RLLocationData("Manor",   91_027),
    "Manor - Right Tree":                       RLLocationData("Manor",   91_028),
    "Manor - Observatory Base":                 RLLocationData("Manor",   91_029),
    "Manor - Observatory Telescope":            RLLocationData("Manor",   91_030),

    # Boss Rewards
    "Castle Hamson Boss Reward":                RLLocationData("Boss",    91_100),
    "Forest Abkhazia Boss Reward":              RLLocationData("Boss",    91_102),
    "The Maya Boss Reward":                     RLLocationData("Boss",    91_104),
    "Land of Darkness Boss Reward":             RLLocationData("Boss",    91_106),

    # Special Locations
    "Jukebox":                                  RLLocationData("Special", 91_200),
    "Painting":                                 RLLocationData("Special", 91_201),
    "Cheapskate Elf's Game":                    RLLocationData("Special", 91_202),
    "Carnival":                                 RLLocationData("Special", 91_203),

    # Diaries
    **{f"Diary {i+1}":                          RLLocationData("Diary",   91_300 + i) for i in range(0,  25)},

    # Chests
    **{f"Castle Hamson - Chest {i+1}":          RLLocationData("Chests",  91_600 + i) for i in range(0,  50)},
    **{f"Forest Abkhazia - Chest {i+1}":        RLLocationData("Chests",  91_700 + i) for i in range(0,  50)},
    **{f"The Maya - Chest {i+1}":               RLLocationData("Chests",  91_800 + i) for i in range(0,  50)},
    **{f"Land of Darkness - Chest {i+1}":       RLLocationData("Chests",  91_900 + i) for i in range(0,  50)},
    **{f"Chest {i+1}":                          RLLocationData("Chests",  92_000 + i) for i in range(0, 200)},

    # Fairy Chests
    **{f"Castle Hamson - Fairy Chest {i+1}":    RLLocationData("Fairies", 91_400 + i) for i in range(0,  15)},
    **{f"Forest Abkhazia - Fairy Chest {i+1}":  RLLocationData("Fairies", 91_450 + i) for i in range(0,  15)},
    **{f"The Maya - Fairy Chest {i+1}":         RLLocationData("Fairies", 91_500 + i) for i in range(0,  15)},
    **{f"Land of Darkness - Fairy Chest {i+1}": RLLocationData("Fairies", 91_550 + i) for i in range(0,  15)},
    **{f"Fairy Chest {i+1}":                    RLLocationData("Fairies", 92_200 + i) for i in range(0,  60)},
}

event_location_table: Dict[str, RLLocationData] = {
    "Castle Hamson Boss Room":                  RLLocationData("Event"),
    "Forest Abkhazia Boss Room":                RLLocationData("Event"),
    "The Maya Boss Room":                       RLLocationData("Event"),
    "Land of Darkness Boss Room":               RLLocationData("Event"),
    "Fountain Room":                            RLLocationData("Event"),
}
