# Locations are specific points that you would obtain an item at.
from enum import IntEnum
from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class NoitaLocation(Location):
    game: str = "Noita"


class LocationData(NamedTuple):
    id: int
    flag: int = 0
    ltype: Optional[str] = ""


class LocationFlag(IntEnum):
    none = 0
    main_path = 1
    side_path = 2
    main_world = 3
    parallel_worlds = 4


# Mapping of items in each region.
# Only the first Hidden Chest and Pedestal are mapped here, the others are created in Regions.
# ltype key: "chest" = Hidden Chests, "pedestal" = Pedestals, "boss" = Boss, "orb" = Orb.
location_region_mapping: Dict[str, Dict[str, LocationData]] = {
    "Coal Pits Holy Mountain": {
        "Coal Pits Holy Mountain Shop Item 1":   LocationData(111000),
        "Coal Pits Holy Mountain Shop Item 2":   LocationData(111001),
        "Coal Pits Holy Mountain Shop Item 3":   LocationData(111002),
        "Coal Pits Holy Mountain Shop Item 4":   LocationData(111003),
        "Coal Pits Holy Mountain Shop Item 5":   LocationData(111004),
        "Coal Pits Holy Mountain Spell Refresh": LocationData(111035),
    },
    "Snowy Depths Holy Mountain": {
        "Snowy Depths Holy Mountain Shop Item 1":   LocationData(111005),
        "Snowy Depths Holy Mountain Shop Item 2":   LocationData(111006),
        "Snowy Depths Holy Mountain Shop Item 3":   LocationData(111007),
        "Snowy Depths Holy Mountain Shop Item 4":   LocationData(111008),
        "Snowy Depths Holy Mountain Shop Item 5":   LocationData(111009),
        "Snowy Depths Holy Mountain Spell Refresh": LocationData(111036),
    },
    "Hiisi Base Holy Mountain": {
        "Hiisi Base Holy Mountain Shop Item 1":   LocationData(111010),
        "Hiisi Base Holy Mountain Shop Item 2":   LocationData(111011),
        "Hiisi Base Holy Mountain Shop Item 3":   LocationData(111012),
        "Hiisi Base Holy Mountain Shop Item 4":   LocationData(111013),
        "Hiisi Base Holy Mountain Shop Item 5":   LocationData(111014),
        "Hiisi Base Holy Mountain Spell Refresh": LocationData(111037),
    },
    "Underground Jungle Holy Mountain": {
        "Underground Jungle Holy Mountain Shop Item 1":   LocationData(111015),
        "Underground Jungle Holy Mountain Shop Item 2":   LocationData(111016),
        "Underground Jungle Holy Mountain Shop Item 3":   LocationData(111017),
        "Underground Jungle Holy Mountain Shop Item 4":   LocationData(111018),
        "Underground Jungle Holy Mountain Shop Item 5":   LocationData(111019),
        "Underground Jungle Holy Mountain Spell Refresh": LocationData(111038),
    },
    "Vault Holy Mountain": {
        "Vault Holy Mountain Shop Item 1":   LocationData(111020),
        "Vault Holy Mountain Shop Item 2":   LocationData(111021),
        "Vault Holy Mountain Shop Item 3":   LocationData(111022),
        "Vault Holy Mountain Shop Item 4":   LocationData(111023),
        "Vault Holy Mountain Shop Item 5":   LocationData(111024),
        "Vault Holy Mountain Spell Refresh": LocationData(111039),
    },
    "Temple of the Art Holy Mountain": {
        "Temple of the Art Holy Mountain Shop Item 1":   LocationData(111025),
        "Temple of the Art Holy Mountain Shop Item 2":   LocationData(111026),
        "Temple of the Art Holy Mountain Shop Item 3":   LocationData(111027),
        "Temple of the Art Holy Mountain Shop Item 4":   LocationData(111028),
        "Temple of the Art Holy Mountain Shop Item 5":   LocationData(111029),
        "Temple of the Art Holy Mountain Spell Refresh": LocationData(111040),
    },
    "Laboratory Holy Mountain": {
        "Laboratory Holy Mountain Shop Item 1":   LocationData(111030),
        "Laboratory Holy Mountain Shop Item 2":   LocationData(111031),
        "Laboratory Holy Mountain Shop Item 3":   LocationData(111032),
        "Laboratory Holy Mountain Shop Item 4":   LocationData(111033),
        "Laboratory Holy Mountain Shop Item 5":   LocationData(111034),
        "Laboratory Holy Mountain Spell Refresh": LocationData(111041),
    },
    "Secret Shop": {
        "Secret Shop Item 1": LocationData(111042),
        "Secret Shop Item 2": LocationData(111043),
        "Secret Shop Item 3": LocationData(111044),
        "Secret Shop Item 4": LocationData(111045),
    },
    "Floating Island": {
        "Floating Island Orb": LocationData(110501, LocationFlag.main_path, "orb"),
    },
    "Pyramid": {
        "Kolmisilmän Koipi": LocationData(110630, LocationFlag.main_world, "boss"),
        "Pyramid Orb":       LocationData(110502, LocationFlag.main_world, "orb"),
        "Sandcave Orb":      LocationData(110505, LocationFlag.main_world, "orb"),
    },
    "Overgrown Cavern": {
        "Overgrown Cavern Chest":    LocationData(112200, LocationFlag.main_world, "chest"),
        "Overgrown Cavern Pedestal": LocationData(112700, LocationFlag.main_world, "pedestal"),
    },
    "Lake": {
        "Syväolento": LocationData(110650, LocationFlag.main_world, "boss"),
    },
    "Frozen Vault": {
        "Frozen Vault Orb":      LocationData(110503, LocationFlag.main_world, "orb"),
        "Frozen Vault Chest":    LocationData(112260, LocationFlag.main_world, "chest"),
        "Frozen Vault Pedestal": LocationData(112760, LocationFlag.main_world, "pedestal"),
    },
    "Mines": {
        "Mines Chest":    LocationData(112000, LocationFlag.main_path, "chest"),
        "Mines Pedestal": LocationData(112500, LocationFlag.main_path, "pedestal"),
    },
    "Collapsed Mines": {
        "Collapsed Mines Chest":    LocationData(112020, LocationFlag.main_path, "chest"),
        "Collapsed Mines Pedestal": LocationData(112520, LocationFlag.main_path, "pedestal"),
    },
    "Ancient Laboratory": {
        "Ylialkemisti": LocationData(110700, LocationFlag.side_path, "boss"),
    },
    "Abyss Orb Room": {
        "Sauvojen Tuntija": LocationData(110640, LocationFlag.side_path, "boss"),
        "Abyss Orb":        LocationData(110508, LocationFlag.main_path, "orb"),
    },
    "Below Lava Lake": {
        "Lava Lake Orb": LocationData(110504, LocationFlag.side_path, "orb"),
    },
    "Coal Pits": {
        "Coal Pits Chest":    LocationData(112040, LocationFlag.main_path, "chest"),
        "Coal Pits Pedestal": LocationData(112540, LocationFlag.main_path, "pedestal"),
    },
    "Fungal Caverns": {
        "Fungal Caverns Chest":    LocationData(112060, LocationFlag.side_path, "chest"),
        "Fungal Caverns Pedestal": LocationData(112560, LocationFlag.side_path, "pedestal"),
    },
    "Snowy Depths": {
        "Snowy Depths Chest":    LocationData(112080, LocationFlag.main_path, "chest"),
        "Snowy Depths Pedestal": LocationData(112580, LocationFlag.main_path, "pedestal"),
    },
    "Magical Temple": {
        "Magical Temple Orb":  LocationData(110506, LocationFlag.side_path, "orb"),
    },
    "Hiisi Base": {
        "Hiisi Base Chest":    LocationData(112100, LocationFlag.main_path, "chest"),
        "Hiisi Base Pedestal": LocationData(112600, LocationFlag.main_path, "pedestal"),
    },
    "Underground Jungle": {
        "Suomuhauki":                  LocationData(110620, LocationFlag.main_path, "boss"),
        "Underground Jungle Chest":    LocationData(112120, LocationFlag.main_path, "chest"),
        "Underground Jungle Pedestal": LocationData(112620, LocationFlag.main_path, "pedestal"),
    },
    "Lukki Lair": {
        "Lukki Lair Orb":      LocationData(110507, LocationFlag.side_path, "orb"),
        "Lukki Lair Chest":    LocationData(112140, LocationFlag.side_path, "chest"),
        "Lukki Lair Pedestal": LocationData(112640, LocationFlag.side_path, "pedestal"),
    },
    "The Vault": {
        "The Vault Chest":    LocationData(112160, LocationFlag.main_path, "chest"),
        "The Vault Pedestal": LocationData(112660, LocationFlag.main_path, "pedestal"),
    },
    "Temple of the Art": {
        "Gate Guardian":              LocationData(110660, LocationFlag.main_path, "boss"),
        "Temple of the Art Chest":    LocationData(112180, LocationFlag.main_path, "chest"),
        "Temple of the Art Pedestal": LocationData(112680, LocationFlag.main_path, "pedestal"),
    },
    "The Tower": {
        "The Tower Chest":    LocationData(112280, LocationFlag.main_world, "chest"),
        "The Tower Pedestal": LocationData(112780, LocationFlag.main_world, "pedestal"),
    },
    "Wizard's Den": {
        "Mestarien Mestari":     LocationData(110690, LocationFlag.main_world, "boss"),
        "Wizard's Den Orb":      LocationData(110511, LocationFlag.main_world, "orb"),
        "Wizards' Den Chest":    LocationData(112220, LocationFlag.main_world, "chest"),
        "Wizards' Den Pedestal": LocationData(112720, LocationFlag.main_world, "pedestal"),
    },
    "Powerplant": {
        "Kolmisilmän silmä":    LocationData(110710, LocationFlag.main_world, "boss"),
        "Power Plant Chest":    LocationData(112240, LocationFlag.main_world, "chest"),
        "Power Plant Pedestal": LocationData(112740, LocationFlag.main_world, "pedestal"),
    },
    "Snow Chasm": {
        "Unohdettu":      LocationData(110670, LocationFlag.main_world, "boss"),
        "Snow Chasm Orb": LocationData(110510, LocationFlag.main_world, "orb"),
    },
    "Deep Underground": {
        "Limatoukka": LocationData(110610, LocationFlag.main_world, "boss"),
    },
    "The Laboratory": {
        "Kolmisilmä": LocationData(110600, LocationFlag.main_path, "boss"),
    },
    "Friend Cave": {
        "Toveri": LocationData(110680, LocationFlag.main_world, "boss"),
    },
    "The Work (Hell)": {
        "The Work (Hell) Orb": LocationData(110509, LocationFlag.main_world, "orb"),
    },
}


# Iterating the hidden chest and pedestal locations here to avoid clutter above
def generate_location_entries(locname: str, locinfo: LocationData) -> Dict[str, int]:
    if locinfo.ltype in ["chest", "pedestal"]:
        return {f"{locname} {i + 1}": locinfo.id + i for i in range(20)}
    return {locname: locinfo.id}


location_name_to_id: Dict[str, int] = {}
for location_group in location_region_mapping.values():
    for locname, locinfo in location_group.items():
        location_name_to_id.update(generate_location_entries(locname, locinfo))
