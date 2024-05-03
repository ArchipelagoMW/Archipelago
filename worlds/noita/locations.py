# Locations are specific points that you would obtain an item at.
from enum import IntEnum
from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Location


class NoitaLocation(Location):
    game: str = "Noita"


class LocationData(NamedTuple):
    id: int
    flag: int = 0
    ltype: str = "Shop"


class LocationFlag(IntEnum):
    none = 0
    main_path = 1
    side_path = 2
    main_world = 3
    parallel_worlds = 4


# Mapping of items in each region.
# Only the first Hidden Chest and Pedestal are mapped here, the others are created in Regions.
# ltype key: "Chest" = Hidden Chests, "Pedestal" = Pedestals, "Boss" = Boss, "Orb" = Orb.
# 110000-110671
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
    "The Sky": {
        "Kivi": LocationData(110670, LocationFlag.main_world, "Boss"),
    },
    "Floating Island": {
        "Floating Island Orb": LocationData(110658, LocationFlag.main_path, "Orb"),
    },
    "Pyramid": {
        "Kolmisilmän Koipi": LocationData(110649, LocationFlag.main_world, "Boss"),
        "Pyramid Orb":       LocationData(110659, LocationFlag.main_world, "Orb"),
        "Sandcave Orb":      LocationData(110662, LocationFlag.main_world, "Orb"),
    },
    "Overgrown Cavern": {
        "Overgrown Cavern Chest":    LocationData(110526, LocationFlag.main_world, "Chest"),
        "Overgrown Cavern Pedestal": LocationData(110546, LocationFlag.main_world, "Pedestal"),
    },
    "Lake": {
        "Syväolento": LocationData(110651, LocationFlag.main_world, "Boss"),
        "Tapion vasalli": LocationData(110669, LocationFlag.main_world, "Boss"),
    },
    "Frozen Vault": {
        "Frozen Vault Orb":      LocationData(110660, LocationFlag.main_world, "Orb"),
        "Frozen Vault Chest":    LocationData(110566, LocationFlag.main_world, "Chest"),
        "Frozen Vault Pedestal": LocationData(110586, LocationFlag.main_world, "Pedestal"),
    },
    "Mines": {
        "Mines Chest":    LocationData(110046, LocationFlag.main_path, "Chest"),
        "Mines Pedestal": LocationData(110066, LocationFlag.main_path, "Pedestal"),
    },
    # Collapsed Mines is a very small area, combining it with the Mines. Leaving this here as a reminder

    "Ancient Laboratory": {
        "Ylialkemisti": LocationData(110656, LocationFlag.side_path, "Boss"),
    },
    "Abyss Orb Room": {
        "Sauvojen Tuntija": LocationData(110650, LocationFlag.side_path, "Boss"),
        "Abyss Orb":        LocationData(110665, LocationFlag.main_path, "Orb"),
    },
    "Below Lava Lake": {
        "Lava Lake Orb": LocationData(110661, LocationFlag.side_path, "Orb"),
    },
    "Coal Pits": {
        "Coal Pits Chest":    LocationData(110126, LocationFlag.main_path, "Chest"),
        "Coal Pits Pedestal": LocationData(110146, LocationFlag.main_path, "Pedestal"),
    },
    "Fungal Caverns": {
        "Fungal Caverns Chest":    LocationData(110166, LocationFlag.side_path, "Chest"),
        "Fungal Caverns Pedestal": LocationData(110186, LocationFlag.side_path, "Pedestal"),
    },
    "Snowy Depths": {
        "Snowy Depths Chest":    LocationData(110206, LocationFlag.main_path, "Chest"),
        "Snowy Depths Pedestal": LocationData(110226, LocationFlag.main_path, "Pedestal"),
    },
    "Magical Temple": {
        "Magical Temple Orb":  LocationData(110663, LocationFlag.side_path, "Orb"),
    },
    "Hiisi Base": {
        "Hiisi Base Chest":    LocationData(110246, LocationFlag.main_path, "Chest"),
        "Hiisi Base Pedestal": LocationData(110266, LocationFlag.main_path, "Pedestal"),
    },
    "Underground Jungle": {
        "Suomuhauki":                  LocationData(110648, LocationFlag.main_path, "Boss"),
        "Underground Jungle Chest":    LocationData(110286, LocationFlag.main_path, "Chest"),
        "Underground Jungle Pedestal": LocationData(110306, LocationFlag.main_path, "Pedestal"),
    },
    "Lukki Lair": {
        "Lukki Lair Orb":      LocationData(110664, LocationFlag.side_path, "Orb"),
        "Lukki Lair Chest":    LocationData(110326, LocationFlag.side_path, "Chest"),
        "Lukki Lair Pedestal": LocationData(110346, LocationFlag.side_path, "Pedestal"),
    },
    "The Vault": {
        "The Vault Chest":    LocationData(110366, LocationFlag.main_path, "Chest"),
        "The Vault Pedestal": LocationData(110386, LocationFlag.main_path, "Pedestal"),
    },
    "Temple of the Art": {
        "Gate Guardian":              LocationData(110652, LocationFlag.main_path, "Boss"),
        "Temple of the Art Chest":    LocationData(110406, LocationFlag.main_path, "Chest"),
        "Temple of the Art Pedestal": LocationData(110426, LocationFlag.main_path, "Pedestal"),
    },
    "The Tower": {
        "The Tower Chest":    LocationData(110606, LocationFlag.main_world, "Chest"),
        "The Tower Pedestal": LocationData(110626, LocationFlag.main_world, "Pedestal"),
    },
    "Wizards' Den": {
        "Mestarien Mestari":     LocationData(110655, LocationFlag.main_world, "Boss"),
        "Wizards' Den Orb":      LocationData(110668, LocationFlag.main_world, "Orb"),
        "Wizards' Den Chest":    LocationData(110446, LocationFlag.main_world, "Chest"),
        "Wizards' Den Pedestal": LocationData(110466, LocationFlag.main_world, "Pedestal"),
    },
    "Powerplant": {
        "Kolmisilmän silmä":    LocationData(110657, LocationFlag.main_world, "Boss"),
        "Power Plant Chest":    LocationData(110486, LocationFlag.main_world, "Chest"),
        "Power Plant Pedestal": LocationData(110506, LocationFlag.main_world, "Pedestal"),
    },
    "Snow Chasm": {
        "Unohdettu":      LocationData(110653, LocationFlag.main_world, "Boss"),
        "Snow Chasm Orb": LocationData(110667, LocationFlag.main_world, "Orb"),
    },
    "Meat Realm": {
        "Meat Realm Chest": LocationData(110086, LocationFlag.main_world, "Chest"),
        "Meat Realm Pedestal": LocationData(110106, LocationFlag.main_world, "Pedestal"),
        "Limatoukka": LocationData(110647, LocationFlag.main_world, "Boss"),
    },
    "West Meat Realm": {
        "Kolmisilmän sydän": LocationData(110671, LocationFlag.main_world, "Boss"),
    },
    "The Laboratory": {
        "Kolmisilmä": LocationData(110646, LocationFlag.main_path, "Boss"),
    },
    "Friend Cave": {
        "Toveri": LocationData(110654, LocationFlag.main_world, "Boss"),
    },
    "The Work (Hell)": {
        "The Work (Hell) Orb": LocationData(110666, LocationFlag.main_world, "Orb"),
    },
}


def make_location_range(location_name: str, base_id: int, amt: int) -> Dict[str, int]:
    if amt == 1:
        return {location_name: base_id}
    return {f"{location_name} {i+1}": base_id + i for i in range(amt)}


location_name_groups: Dict[str, Set[str]] = {"Shop": set(), "Orb": set(), "Boss": set(), "Chest": set(),
                                             "Pedestal": set()}
location_name_to_id: Dict[str, int] = {}


for region_name, location_group in location_region_mapping.items():
    location_name_groups[region_name] = set()
    for locname, locinfo in location_group.items():
        # Iterating the hidden chest and pedestal locations here to avoid clutter above
        amount = 20 if locinfo.ltype in ["Chest", "Pedestal"] else 1
        entries = make_location_range(locname, locinfo.id, amount)

        location_name_to_id.update(entries)
        location_name_groups[locinfo.ltype].update(entries.keys())
        location_name_groups[region_name].update(entries.keys())

shop_locations = {name for name in location_name_to_id.keys() if "Shop Item" in name}
