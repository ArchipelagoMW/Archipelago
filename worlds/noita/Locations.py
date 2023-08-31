# Locations are specific points that you would obtain an item at.
from enum import IntEnum
from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Location


class NoitaLocation(Location):
    game: str = "Noita"


class LocationData(NamedTuple):
    id: int
    flag: int = 0
    ltype: Optional[str] = "shop"


class LocationFlag(IntEnum):
    none = 0
    main_path = 1
    side_path = 2
    main_world = 3
    parallel_worlds = 4


# Mapping of items in each region.
# Only the first Hidden Chest and Pedestal are mapped here, the others are created in Regions.
# ltype key: "chest" = Hidden Chests, "pedestal" = Pedestals, "boss" = Boss, "orb" = Orb.
# 110000-110649
location_region_mapping: Dict[str, Dict[str, LocationData]] = {
    "Coal Pits Holy Mountain": {
        "Coal Pits Holy Mountain Shop Item 1":   LocationData(110000),
        "Coal Pits Holy Mountain Shop Item 2":   LocationData(110001),
        "Coal Pits Holy Mountain Shop Item 3":   LocationData(110002),
        "Coal Pits Holy Mountain Shop Item 4":   LocationData(110003),
        "Coal Pits Holy Mountain Shop Item 5":   LocationData(110004),
        "Coal Pits Holy Mountain Spell Refresh": LocationData(110005),
    },
    "Snowy Depths Holy Mountain": {
        "Snowy Depths Holy Mountain Shop Item 1":   LocationData(110006),
        "Snowy Depths Holy Mountain Shop Item 2":   LocationData(110007),
        "Snowy Depths Holy Mountain Shop Item 3":   LocationData(110008),
        "Snowy Depths Holy Mountain Shop Item 4":   LocationData(110009),
        "Snowy Depths Holy Mountain Shop Item 5":   LocationData(110010),
        "Snowy Depths Holy Mountain Spell Refresh": LocationData(110011),
    },
    "Hiisi Base Holy Mountain": {
        "Hiisi Base Holy Mountain Shop Item 1":   LocationData(110012),
        "Hiisi Base Holy Mountain Shop Item 2":   LocationData(110013),
        "Hiisi Base Holy Mountain Shop Item 3":   LocationData(110014),
        "Hiisi Base Holy Mountain Shop Item 4":   LocationData(110015),
        "Hiisi Base Holy Mountain Shop Item 5":   LocationData(110016),
        "Hiisi Base Holy Mountain Spell Refresh": LocationData(110017),
    },
    "Underground Jungle Holy Mountain": {
        "Underground Jungle Holy Mountain Shop Item 1":   LocationData(110018),
        "Underground Jungle Holy Mountain Shop Item 2":   LocationData(110019),
        "Underground Jungle Holy Mountain Shop Item 3":   LocationData(110020),
        "Underground Jungle Holy Mountain Shop Item 4":   LocationData(110021),
        "Underground Jungle Holy Mountain Shop Item 5":   LocationData(110022),
        "Underground Jungle Holy Mountain Spell Refresh": LocationData(110023),
    },
    "Vault Holy Mountain": {
        "Vault Holy Mountain Shop Item 1":   LocationData(110024),
        "Vault Holy Mountain Shop Item 2":   LocationData(110025),
        "Vault Holy Mountain Shop Item 3":   LocationData(110026),
        "Vault Holy Mountain Shop Item 4":   LocationData(110027),
        "Vault Holy Mountain Shop Item 5":   LocationData(110028),
        "Vault Holy Mountain Spell Refresh": LocationData(110029),
    },
    "Temple of the Art Holy Mountain": {
        "Temple of the Art Holy Mountain Shop Item 1":   LocationData(110030),
        "Temple of the Art Holy Mountain Shop Item 2":   LocationData(110031),
        "Temple of the Art Holy Mountain Shop Item 3":   LocationData(110032),
        "Temple of the Art Holy Mountain Shop Item 4":   LocationData(110033),
        "Temple of the Art Holy Mountain Shop Item 5":   LocationData(110034),
        "Temple of the Art Holy Mountain Spell Refresh": LocationData(110035),
    },
    "Laboratory Holy Mountain": {
        "Laboratory Holy Mountain Shop Item 1":   LocationData(110036),
        "Laboratory Holy Mountain Shop Item 2":   LocationData(110037),
        "Laboratory Holy Mountain Shop Item 3":   LocationData(110038),
        "Laboratory Holy Mountain Shop Item 4":   LocationData(110039),
        "Laboratory Holy Mountain Shop Item 5":   LocationData(110040),
        "Laboratory Holy Mountain Spell Refresh": LocationData(110041),
    },
    "Secret Shop": {
        "Secret Shop Item 1": LocationData(110042),
        "Secret Shop Item 2": LocationData(110043),
        "Secret Shop Item 3": LocationData(110044),
        "Secret Shop Item 4": LocationData(110045),
    },
    "Floating Island": {
        "Floating Island Orb": LocationData(110658, LocationFlag.main_path, "orb"),
    },
    "Pyramid": {
        "Kolmisilmän Koipi": LocationData(110649, LocationFlag.main_world, "boss"),
        "Pyramid Orb":       LocationData(110659, LocationFlag.main_world, "orb"),
        "Sandcave Orb":      LocationData(110662, LocationFlag.main_world, "orb"),
    },
    "Overgrown Cavern": {
        "Overgrown Cavern Chest":    LocationData(110526, LocationFlag.main_world, "chest"),
        "Overgrown Cavern Pedestal": LocationData(110546, LocationFlag.main_world, "pedestal"),
    },
    "Lake": {
        "Syväolento": LocationData(110651, LocationFlag.main_world, "boss"),
    },
    "Frozen Vault": {
        "Frozen Vault Orb":      LocationData(110660, LocationFlag.main_world, "orb"),
        "Frozen Vault Chest":    LocationData(110566, LocationFlag.main_world, "chest"),
        "Frozen Vault Pedestal": LocationData(110586, LocationFlag.main_world, "pedestal"),
    },
    "Mines": {
        "Mines Chest":    LocationData(110046, LocationFlag.main_path, "chest"),
        "Mines Pedestal": LocationData(110066, LocationFlag.main_path, "pedestal"),
    },
    # Collapsed Mines is a very small area, combining it with the Mines. Leaving this here in case we change our minds.
    # "Collapsed Mines": {
    #     "Collapsed Mines Chest":    LocationData(110086, LocationFlag.main_path, "chest"),
    #     "Collapsed Mines Pedestal": LocationData(110106, LocationFlag.main_path, "pedestal"),
    # },
    "Ancient Laboratory": {
        "Ylialkemisti": LocationData(110656, LocationFlag.side_path, "boss"),
    },
    "Abyss Orb Room": {
        "Sauvojen Tuntija": LocationData(110650, LocationFlag.side_path, "boss"),
        "Abyss Orb":        LocationData(110665, LocationFlag.main_path, "orb"),
    },
    "Below Lava Lake": {
        "Lava Lake Orb": LocationData(110661, LocationFlag.side_path, "orb"),
    },
    "Coal Pits": {
        "Coal Pits Chest":    LocationData(110126, LocationFlag.main_path, "chest"),
        "Coal Pits Pedestal": LocationData(110146, LocationFlag.main_path, "pedestal"),
    },
    "Fungal Caverns": {
        "Fungal Caverns Chest":    LocationData(110166, LocationFlag.side_path, "chest"),
        "Fungal Caverns Pedestal": LocationData(110186, LocationFlag.side_path, "pedestal"),
    },
    "Snowy Depths": {
        "Snowy Depths Chest":    LocationData(110206, LocationFlag.main_path, "chest"),
        "Snowy Depths Pedestal": LocationData(110226, LocationFlag.main_path, "pedestal"),
    },
    "Magical Temple": {
        "Magical Temple Orb":  LocationData(110663, LocationFlag.side_path, "orb"),
    },
    "Hiisi Base": {
        "Hiisi Base Chest":    LocationData(110246, LocationFlag.main_path, "chest"),
        "Hiisi Base Pedestal": LocationData(110266, LocationFlag.main_path, "pedestal"),
    },
    "Underground Jungle": {
        "Suomuhauki":                  LocationData(110648, LocationFlag.main_path, "boss"),
        "Underground Jungle Chest":    LocationData(110286, LocationFlag.main_path, "chest"),
        "Underground Jungle Pedestal": LocationData(110306, LocationFlag.main_path, "pedestal"),
    },
    "Lukki Lair": {
        "Lukki Lair Orb":      LocationData(110664, LocationFlag.side_path, "orb"),
        "Lukki Lair Chest":    LocationData(110326, LocationFlag.side_path, "chest"),
        "Lukki Lair Pedestal": LocationData(110346, LocationFlag.side_path, "pedestal"),
    },
    "The Vault": {
        "The Vault Chest":    LocationData(110366, LocationFlag.main_path, "chest"),
        "The Vault Pedestal": LocationData(110386, LocationFlag.main_path, "pedestal"),
    },
    "Temple of the Art": {
        "Gate Guardian":              LocationData(110652, LocationFlag.main_path, "boss"),
        "Temple of the Art Chest":    LocationData(110406, LocationFlag.main_path, "chest"),
        "Temple of the Art Pedestal": LocationData(110426, LocationFlag.main_path, "pedestal"),
    },
    "The Tower": {
        "The Tower Chest":    LocationData(110606, LocationFlag.main_world, "chest"),
        "The Tower Pedestal": LocationData(110626, LocationFlag.main_world, "pedestal"),
    },
    "Wizards' Den": {
        "Mestarien Mestari":     LocationData(110655, LocationFlag.main_world, "boss"),
        "Wizards' Den Orb":      LocationData(110668, LocationFlag.main_world, "orb"),
        "Wizards' Den Chest":    LocationData(110446, LocationFlag.main_world, "chest"),
        "Wizards' Den Pedestal": LocationData(110466, LocationFlag.main_world, "pedestal"),
    },
    "Powerplant": {
        "Kolmisilmän silmä":    LocationData(110657, LocationFlag.main_world, "boss"),
        "Power Plant Chest":    LocationData(110486, LocationFlag.main_world, "chest"),
        "Power Plant Pedestal": LocationData(110506, LocationFlag.main_world, "pedestal"),
    },
    "Snow Chasm": {
        "Unohdettu":      LocationData(110653, LocationFlag.main_world, "boss"),
        "Snow Chasm Orb": LocationData(110667, LocationFlag.main_world, "orb"),
    },
    "Deep Underground": {
        "Limatoukka": LocationData(110647, LocationFlag.main_world, "boss"),
    },
    "The Laboratory": {
        "Kolmisilmä": LocationData(110646, LocationFlag.main_path, "boss"),
    },
    "Friend Cave": {
        "Toveri": LocationData(110654, LocationFlag.main_world, "boss"),
    },
    "The Work (Hell)": {
        "The Work (Hell) Orb": LocationData(110666, LocationFlag.main_world, "orb"),
    },
}


# Iterating the hidden chest and pedestal locations here to avoid clutter above
def generate_location_entries(locname: str, locinfo: LocationData) -> Dict[str, int]:
    if locinfo.ltype in ["chest", "pedestal"]:
        return {f"{locname} {i + 1}": locinfo.id + i for i in range(20)}
    return {locname: locinfo.id}


location_name_groups: Dict[str, Set[str]] = {"shop": set(), "orb": set(), "boss": set(), "chest": set(),
                                             "pedestal": set()}
location_name_to_id: Dict[str, int] = {}


for location_group in location_region_mapping.values():
    for locname, locinfo in location_group.items():
        location_name_to_id.update(generate_location_entries(locname, locinfo))
        if locinfo.ltype in ["chest", "pedestal"]:
            for i in range(20):
                location_name_groups[locinfo.ltype].add(f"{locname} {i + 1}")
        else:
            location_name_groups[locinfo.ltype].add(locname)
