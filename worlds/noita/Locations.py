# Locations are specific points that you would obtain an item at.
from enum import IntEnum
from typing import Dict, NamedTuple, Optional

from BaseClasses import Location


class NoitaLocation(Location):
    game: str = "Noita"


class LocationData(NamedTuple):
    id: int
    ltype: Optional[str] = ""
    flag: int = 0


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
        "Coal Pits Holy Mountain Shop Item 1": LocationData(111000),
        "Coal Pits Holy Mountain Shop Item 2": LocationData(111001),
        "Coal Pits Holy Mountain Shop Item 3": LocationData(111002),
        "Coal Pits Holy Mountain Shop Item 4": LocationData(111003),
        "Coal Pits Holy Mountain Shop Item 5": LocationData(111004),
        "Coal Pits Holy Mountain Spell Refresh": LocationData(111035),
    },
    "Snowy Depths Holy Mountain": {
        "Snowy Depths Holy Mountain Shop Item 1": LocationData(111005),
        "Snowy Depths Holy Mountain Shop Item 2": LocationData(111006),
        "Snowy Depths Holy Mountain Shop Item 3": LocationData(111007),
        "Snowy Depths Holy Mountain Shop Item 4": LocationData(111008),
        "Snowy Depths Holy Mountain Shop Item 5": LocationData(111009),
        "Snowy Depths Holy Mountain Spell Refresh": LocationData(111036),
    },
    "Hiisi Base Holy Mountain": {
        "Hiisi Base Holy Mountain Shop Item 1": LocationData(111010),
        "Hiisi Base Holy Mountain Shop Item 2": LocationData(111011),
        "Hiisi Base Holy Mountain Shop Item 3": LocationData(111012),
        "Hiisi Base Holy Mountain Shop Item 4": LocationData(111013),
        "Hiisi Base Holy Mountain Shop Item 5": LocationData(111014),
        "Hiisi Base Holy Mountain Spell Refresh": LocationData(111037),
    },
    "Underground Jungle Holy Mountain": {
        "Underground Jungle Holy Mountain Shop Item 1": LocationData(111015),
        "Underground Jungle Holy Mountain Shop Item 2": LocationData(111016),
        "Underground Jungle Holy Mountain Shop Item 3": LocationData(111017),
        "Underground Jungle Holy Mountain Shop Item 4": LocationData(111018),
        "Underground Jungle Holy Mountain Shop Item 5": LocationData(111019),
        "Underground Jungle Holy Mountain Spell Refresh": LocationData(111038),
    },
    "Vault Holy Mountain": {
        "Vault Holy Mountain Shop Item 1": LocationData(111020),
        "Vault Holy Mountain Shop Item 2": LocationData(111021),
        "Vault Holy Mountain Shop Item 3": LocationData(111022),
        "Vault Holy Mountain Shop Item 4": LocationData(111023),
        "Vault Holy Mountain Shop Item 5": LocationData(111024),
        "Vault Holy Mountain Spell Refresh": LocationData(111039),
    },
    "Temple of the Art Holy Mountain": {
        "Temple of the Art Holy Mountain Shop Item 1": LocationData(111025),
        "Temple of the Art Holy Mountain Shop Item 2": LocationData(111026),
        "Temple of the Art Holy Mountain Shop Item 3": LocationData(111027),
        "Temple of the Art Holy Mountain Shop Item 4": LocationData(111028),
        "Temple of the Art Holy Mountain Shop Item 5": LocationData(111029),
        "Temple of the Art Holy Mountain Spell Refresh": LocationData(111040),
    },
    "Laboratory Holy Mountain": {
        "Laboratory Holy Mountain Shop Item 1": LocationData(111030),
        "Laboratory Holy Mountain Shop Item 2": LocationData(111031),
        "Laboratory Holy Mountain Shop Item 3": LocationData(111032),
        "Laboratory Holy Mountain Shop Item 4": LocationData(111033),
        "Laboratory Holy Mountain Shop Item 5": LocationData(111034),
        "Laboratory Holy Mountain Spell Refresh": LocationData(111041),
    },
    "Secret Shop": {
        "Secret Shop Item 1": LocationData(111042),
        "Secret Shop Item 2": LocationData(111043),
        "Secret Shop Item 3": LocationData(111044),
        "Secret Shop Item 4": LocationData(111045),
    },
    "Floating Island": {
        "Floating Island Orb": LocationData(110501, "orb", LocationFlag.main_path),
    },
    "Pyramid": {
        "Kolmisilmän Koipi": LocationData(110630, "boss", LocationFlag.main_world),
        "Pyramid Orb": LocationData(110502, "orb", LocationFlag.main_world),
        "Sandcave Orb": LocationData(110505, "orb", LocationFlag.main_world),
    },
    "Overgrown Cavern": {
        "Overgrown Cavern Chest": LocationData(112200, "chest", LocationFlag.main_world),
        "Overgrown Cavern Pedestal": LocationData(112700, "pedestal", LocationFlag.main_world),
    },
    "Lake": {
        "Syväolento": LocationData(110650, "boss", LocationFlag.main_world),
    },
    "Frozen Vault": {
        "Frozen Vault Orb": LocationData(110503, "orb", LocationFlag.main_world),
        "Frozen Vault Chest": LocationData(112260, "chest", LocationFlag.main_world),
        "Frozen Vault Pedestal": LocationData(112760, "pedestal", LocationFlag.main_world),
    },
    "Mines": {
        "Mines Chest": LocationData(112000, "chest", LocationFlag.main_path),
        "Mines Pedestal": LocationData(112500, "pedestal", LocationFlag.main_path),
    },
    "Collapsed Mines": {
        "Collapsed Mines Chest": LocationData(112020, "chest", LocationFlag.main_path),
        "Collapsed Mines Pedestal": LocationData(112520, "pedestal", LocationFlag.main_path),
    },
    "Ancient Laboratory": {
        "Ylialkemisti": LocationData(110700, "boss", LocationFlag.side_path),
    },
    "Abyss Orb Room": {
        "Sauvojen Tuntija": LocationData(110640, "boss", LocationFlag.side_path),
        "Abyss Orb": LocationData(110508, "orb", LocationFlag.main_path),
    },
    "Below Lava Lake": {
        "Lava Lake Orb": LocationData(110504, "orb", LocationFlag.side_path),
    },
    "Coal Pits": {
        "Coal Pits Chest": LocationData(112040, "chest", LocationFlag.main_path),
        "Coal Pits Pedestal": LocationData(112540, "pedestal", LocationFlag.main_path),
    },
    "Fungal Caverns": {
        "Fungal Caverns Chest": LocationData(112060, "chest", LocationFlag.side_path),
        "Fungal Caverns Pedestal": LocationData(112560, "pedestal", LocationFlag.side_path),
    },
    "Snowy Depths": {
        "Snowy Depths Chest": LocationData(112080, "chest", LocationFlag.main_path),
        "Snowy Depths Pedestal": LocationData(112580, "pedestal", LocationFlag.main_path),
    },
    "Magical Temple": {
        "Magical Temple Orb": LocationData(110506, "orb", LocationFlag.side_path),
    },
    "Hiisi Base": {
        "Hiisi Base Chest": LocationData(112100, "chest", LocationFlag.main_path),
        "Hiisi Base Pedestal": LocationData(112600, "pedestal", LocationFlag.main_path),
    },
    "Underground Jungle": {
        "Suomuhauki": LocationData(110620, "boss", LocationFlag.main_path),
        "Underground Jungle Chest": LocationData(112120, "chest", LocationFlag.main_path),
        "Underground Jungle Pedestal": LocationData(112620, "pedestal", LocationFlag.main_path),
    },
    "Lukki Lair": {
        "Lukki Lair Orb": LocationData(110507, "orb", LocationFlag.side_path),
        "Lukki Lair Chest": LocationData(112140, "chest", LocationFlag.side_path),
        "Lukki Lair Pedestal": LocationData(112640, "pedestal", LocationFlag.side_path),
    },
    "The Vault": {
        "The Vault Chest": LocationData(112160, "chest", LocationFlag.main_path),
        "The Vault Pedestal": LocationData(112660, "pedestal", LocationFlag.main_path),
    },
    "Temple of the Art": {
        "Gate Guardian": LocationData(110660, "boss", LocationFlag.main_path),
        "Temple of the Art Chest": LocationData(112180, "chest", LocationFlag.main_path),
        "Temple of the Art Pedestal": LocationData(112680, "pedestal", LocationFlag.main_path),
    },
    "The Tower": {
        "The Tower Chest": LocationData(112280, "chest", LocationFlag.main_world),
        "The Tower Pedestal": LocationData(112780, "pedestal", LocationFlag.main_world),
    },
    "Wizard's Den": {
        "Mestarien Mestari": LocationData(110690, "boss", LocationFlag.main_world),
        "Wizard's Den Orb": LocationData(110511, "orb", LocationFlag.main_world),
        "Wizards' Den Chest": LocationData(112220, "chest", LocationFlag.main_world),
        "Wizards' Den Pedestal": LocationData(112720, "pedestal", LocationFlag.main_world),
    },
    "Powerplant": {
        "Kolmisilmän silmä": LocationData(110710, "boss", LocationFlag.main_world),
        "Power Plant Chest": LocationData(112240, "chest", LocationFlag.main_world),
        "Power Plant Pedestal": LocationData(112740, "pedestal", LocationFlag.main_world),
    },
    "Snow Chasm": {
        "Unohdettu": LocationData(110670, "boss", LocationFlag.main_world),
        "Snow Chasm Orb": LocationData(110510, "orb", LocationFlag.main_world),
    },
    "Deep Underground": {
        "Limatoukka": LocationData(110610, "boss", LocationFlag.main_world),
    },
    "The Laboratory": {
        "Kolmisilmä": LocationData(110600, "boss", LocationFlag.main_path),
    },
    "Friend Cave": {
        "Toveri": LocationData(110680, "boss", LocationFlag.main_world),
    },
    "The Work (Hell)": {
        "The Work (Hell) Orb": LocationData(110509, "orb", LocationFlag.main_world),
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
