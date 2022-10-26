from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class RLLocation(Location):
    game: str = "Rogue Legacy"


class RLLocationData(NamedTuple):
    category: str
    code: Optional[int] = None

    @property
    def is_event_location(self):
        return self.code is None


def get_locations_by_category(category: str) -> Dict[str, RLLocationData]:
    location_dict: Dict[str, RLLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict


location_table: Dict[str, RLLocationData] = {
    # Manor Renovation
    "Manor Renovation - Ground Road":           RLLocationData("Manor",   91_000),
    "Manor Renovation - Main Base":             RLLocationData("Manor",   91_001),
    "Manor Renovation - Main Bottom Window":    RLLocationData("Manor",   91_002),
    "Manor Renovation - Main Top Window":       RLLocationData("Manor",   91_003),
    "Manor Renovation - Main Rooftop":          RLLocationData("Manor",   91_004),
    "Manor Renovation - Left Wing Base":        RLLocationData("Manor",   91_005),
    "Manor Renovation - Left Wing Window":      RLLocationData("Manor",   91_006),
    "Manor Renovation - Left Wing Rooftop":     RLLocationData("Manor",   91_007),
    "Manor Renovation - Left Big Base":         RLLocationData("Manor",   91_008),
    "Manor Renovation - Left Big Upper 1":      RLLocationData("Manor",   91_009),
    "Manor Renovation - Left Big Upper 2":      RLLocationData("Manor",   91_010),
    "Manor Renovation - Left Big Windows":      RLLocationData("Manor",   91_011),
    "Manor Renovation - Left Big Rooftop":      RLLocationData("Manor",   91_012),
    "Manor Renovation - Left Far Base":         RLLocationData("Manor",   91_013),
    "Manor Renovation - Left Far Roof":         RLLocationData("Manor",   91_014),
    "Manor Renovation - Left Extension":        RLLocationData("Manor",   91_015),
    "Manor Renovation - Left Tree 1":           RLLocationData("Manor",   91_016),
    "Manor Renovation - Left Tree 2":           RLLocationData("Manor",   91_017),
    "Manor Renovation - Right Wing Base":       RLLocationData("Manor",   91_018),
    "Manor Renovation - Right Wing Window":     RLLocationData("Manor",   91_019),
    "Manor Renovation - Right Wing Rooftop":    RLLocationData("Manor",   91_020),
    "Manor Renovation - Right Big Base":        RLLocationData("Manor",   91_021),
    "Manor Renovation - Right Big Upper":       RLLocationData("Manor",   91_022),
    "Manor Renovation - Right Big Rooftop":     RLLocationData("Manor",   91_023),
    "Manor Renovation - Right High Base":       RLLocationData("Manor",   91_024),
    "Manor Renovation - Right High Upper":      RLLocationData("Manor",   91_025),
    "Manor Renovation - Right High Tower":      RLLocationData("Manor",   91_026),
    "Manor Renovation - Right Extension":       RLLocationData("Manor",   91_027),
    "Manor Renovation - Right Tree":            RLLocationData("Manor",   91_028),
    "Manor Renovation - Observatory Base":      RLLocationData("Manor",   91_029),
    "Manor Renovation - Observatory Telescope": RLLocationData("Manor",   91_030),

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
    **{f"Castle Hamson - Chest {i+1}":          RLLocationData("Chests",  91_600 + i) for i in range(0,  30)},
    **{f"Forest Abkhazia - Chest {i+1}":        RLLocationData("Chests",  91_700 + i) for i in range(0,  30)},
    **{f"The Maya - Chest {i+1}":               RLLocationData("Chests",  91_800 + i) for i in range(0,  30)},
    **{f"Land of Darkness - Chest {i+1}":       RLLocationData("Chests",  91_900 + i) for i in range(0,  30)},
    **{f"Chest {i+1}":                          RLLocationData("Chests",  92_000 + i) for i in range(0, 120)},

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
