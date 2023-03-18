# Locations are specific points that you would obtain an item at.
import functools
from enum import IntEnum
from typing import Dict, List, Union, Set, NamedTuple, Optional
from BaseClasses import Location


class NoitaLocation(Location):
    game: str = "Noita"


class LocationData(NamedTuple):
    id: int
    ltype: Optional[str] = ""
    flag: int = 0


class Orbs(IntEnum):
    main_path = 1
    side_path = 2
    main_world = 3
    parallel_worlds = 4


class Bosses(IntEnum):
    main_path = 1
    side_path = 2
    main_world = 3
    parallel_worlds = 4


class HiddenChests(IntEnum):
    main_path = 1
    side_path = 2
    main_world = 3
    parallel_worlds = 4


class Pedestals(IntEnum):
    main_path = 1
    side_path = 2
    main_world = 3
    parallel_worlds = 4


# todo: figure out how to add umlauts and stuff
# 111000 - 111034
# Mapping of items in each region
# Only the first Hidden Chest and Pedestal are mapped here, the others are created in Regions
# ltype key: "hc" = Hidden Chests, "peds" = Pedestals, "boss" = Boss, "orb" = Orb.
location_region_mapping: Dict[str, Dict[str, LocationData]] = {
    "Holy Mountain 1 (To Coal Pits)": {
        "Holy Mountain 1 (To Coal Pits) Shop Item 1": LocationData(111000),
        "Holy Mountain 1 (To Coal Pits) Shop Item 2": LocationData(111001),
        "Holy Mountain 1 (To Coal Pits) Shop Item 3": LocationData(111002),
        "Holy Mountain 1 (To Coal Pits) Shop Item 4": LocationData(111003),
        "Holy Mountain 1 (To Coal Pits) Shop Item 5": LocationData(111004),
        "Holy Mountain 1 (To Coal Pits) Spell Refresh": LocationData(111035),
    },
    "Holy Mountain 2 (To Snowy Depths)": {
        "Holy Mountain 2 (To Snowy Depths) Shop Item 1": LocationData(111005),
        "Holy Mountain 2 (To Snowy Depths) Shop Item 2": LocationData(111006),
        "Holy Mountain 2 (To Snowy Depths) Shop Item 3": LocationData(111007),
        "Holy Mountain 2 (To Snowy Depths) Shop Item 4": LocationData(111008),
        "Holy Mountain 2 (To Snowy Depths) Shop Item 5": LocationData(111009),
        "Holy Mountain 2 (To Snowy Depths) Spell Refresh": LocationData(111036),
    },
    "Holy Mountain 3 (To Hiisi Base)": {
        "Holy Mountain 3 (To Hiisi Base) Shop Item 1": LocationData(111010),
        "Holy Mountain 3 (To Hiisi Base) Shop Item 2": LocationData(111011),
        "Holy Mountain 3 (To Hiisi Base) Shop Item 3": LocationData(111012),
        "Holy Mountain 3 (To Hiisi Base) Shop Item 4": LocationData(111013),
        "Holy Mountain 3 (To Hiisi Base) Shop Item 5": LocationData(111014),
        "Holy Mountain 3 (To Hiisi Base) Spell Refresh": LocationData(111037),
    },
    "Holy Mountain 4 (To Underground Jungle)": {
        "Holy Mountain 4 (To Underground Jungle) Shop Item 1": LocationData(111015),
        "Holy Mountain 4 (To Underground Jungle) Shop Item 2": LocationData(111016),
        "Holy Mountain 4 (To Underground Jungle) Shop Item 3": LocationData(111017),
        "Holy Mountain 4 (To Underground Jungle) Shop Item 4": LocationData(111018),
        "Holy Mountain 4 (To Underground Jungle) Shop Item 5": LocationData(111019),
        "Holy Mountain 4 (To Underground Jungle) Spell Refresh": LocationData(111038),
    },
    "Holy Mountain 5 (To The Vault)": {
        "Holy Mountain 5 (To The Vault) Shop Item 1": LocationData(111020),
        "Holy Mountain 5 (To The Vault) Shop Item 2": LocationData(111021),
        "Holy Mountain 5 (To The Vault) Shop Item 3": LocationData(111022),
        "Holy Mountain 5 (To The Vault) Shop Item 4": LocationData(111023),
        "Holy Mountain 5 (To The Vault) Shop Item 5": LocationData(111024),
        "Holy Mountain 5 (To The Vault) Spell Refresh": LocationData(111039),
    },
    "Holy Mountain 6 (To Temple of the Art)": {
        "Holy Mountain 6 (To Temple of the Art) Shop Item 1": LocationData(111025),
        "Holy Mountain 6 (To Temple of the Art) Shop Item 2": LocationData(111026),
        "Holy Mountain 6 (To Temple of the Art) Shop Item 3": LocationData(111027),
        "Holy Mountain 6 (To Temple of the Art) Shop Item 4": LocationData(111028),
        "Holy Mountain 6 (To Temple of the Art) Shop Item 5": LocationData(111029),
        "Holy Mountain 6 (To Temple of the Art) Spell Refresh": LocationData(111040),
    },
    "Holy Mountain 7 (To The Laboratory)": {
        "Holy Mountain 7 (To The Laboratory) Shop Item 1": LocationData(111030),
        "Holy Mountain 7 (To The Laboratory) Shop Item 2": LocationData(111031),
        "Holy Mountain 7 (To The Laboratory) Shop Item 3": LocationData(111032),
        "Holy Mountain 7 (To The Laboratory) Shop Item 4": LocationData(111033),
        "Holy Mountain 7 (To The Laboratory) Shop Item 5": LocationData(111034),
        "Holy Mountain 7 (To The Laboratory) Spell Refresh": LocationData(111041),
    },
    "Secret Shop": {
        "Secret Shop Item 1": LocationData(111042),
        "Secret Shop Item 2": LocationData(111043),
        "Secret Shop Item 3": LocationData(111044),
        "Secret Shop Item 4": LocationData(111045),
    },
    "Floating Island": {
        "Floating Island Orb": LocationData(110501, "orb", Orbs.main_path),
    },
    "Pyramid": {
        "Kolmisilman Koipi": LocationData(110630, "boss", Bosses.main_world),
        "Pyramid Orb": LocationData(110502, "orb", Orbs.main_world),
        "Sandcave Orb": LocationData(110505, "orb", Orbs.main_world),
    },
    "Overgrown Cavern": {
        "Overgrown Cavern Chest": LocationData(112200, "hc", HiddenChests.main_world),
        "Overgrown Cavern Pedestal": LocationData(112700, "peds", Pedestals.main_world),
    },
    "Lake": {
        "Syvaolento": LocationData(110650, "boss", Bosses.main_world),
    },
    "Frozen Vault": {
        "Frozen Vault Orb": LocationData(110503, "orb", Orbs.main_world),
        "Frozen Vault Chest": LocationData(112260, "hc", HiddenChests.main_world),
        "Frozen Vault Pedestal": LocationData(112760, "peds", Pedestals.main_world),
    },
    "Mines": {
        "Mines Chest": LocationData(112000, "hc", HiddenChests.main_path),
        "Mines Pedestal": LocationData(112500, "peds", Pedestals.main_path),
    },
    "Collapsed Mines": {
        "Collapsed Mines Chest": LocationData(112020, "hc", HiddenChests.side_path),
        "Collapsed Mines Pedestal": LocationData(112520, "peds", Pedestals.side_path),
    },
    "Ancient Laboratory": {
        "Ylialkemisti": LocationData(110700, "boss", Bosses.side_path),
    },
    "Abyss Orb Room": {
        "Sauvojen Tuntija": LocationData(110640, "boss", Bosses.side_path),
        "Abyss Orb": LocationData(110508, "orb", Orbs.main_path),
    },
    "Below Lava Lake": {
        "Lava Lake Orb": LocationData(110504, "orb", Orbs.side_path),
    },
    "Coal Pits": {
        "Coal Pits Chest": LocationData(112040, "hc", HiddenChests.main_path),
        "Coal Pits Pedestal": LocationData(112540, "peds", Pedestals.main_path),
    },
    "Fungal Caverns": {
        "Fungal Caverns Chest": LocationData(112060, "hc", HiddenChests.side_path),
        "Fungal Caverns Pedestal": LocationData(112560, "peds", Pedestals.side_path),
    },
    "Snowy Depths": {
        "Snowy Depths Chest": LocationData(112080, "hc", HiddenChests.main_path),
        "Snowy Depths Pedestal": LocationData(112580, "peds", Pedestals.main_path),
    },
    "Magical Temple": {
        "Magical Temple Orb": LocationData(110506, "orb", Orbs.side_path),
    },
    "Hiisi Base": {
        "Hiisi Base Chest": LocationData(112100, "hc", HiddenChests.main_path),
        "Hiisi Base Pedestal": LocationData(112600, "peds", Pedestals.main_path),
    },
    "Underground Jungle": {
        "Suomuhauki": LocationData(110620, "boss", Bosses.main_path),
        "Underground Jungle Chest": LocationData(112120, "hc", HiddenChests.main_path),
        "Underground Jungle Pedestal": LocationData(112620, "peds", Pedestals.main_path),
    },
    "Lukki Lair": {
        "Lukki Lair Orb": LocationData(110507, "orb", Orbs.side_path),
        "Lukki Lair Chest": LocationData(112140, "hc", HiddenChests.side_path),
        "Lukki Lair Pedestal": LocationData(112640, "peds", Pedestals.side_path),
    },
    "The Vault": {
        "The Vault Chest": LocationData(112160, "hc", HiddenChests.main_path),
        "The Vault Pedestal": LocationData(112660, "peds", Pedestals.main_path),
    },
    "Temple of the Art": {
        "Gate Guardian": LocationData(110660, "boss", Bosses.main_path),
        "Temple of the Art Chest": LocationData(112180, "hc", HiddenChests.main_path),
        "Temple of the Art Pedestal": LocationData(112680, "peds", Pedestals.main_path),
    },
    "The Tower": {
        "The Tower Chest": LocationData(112280, "hc", HiddenChests.main_world),
        "The Tower Pedestal": LocationData(112780, "peds", Pedestals.main_world),
    },
    "Wizard's Den": {
        "Mestarien mestari": LocationData(110700, "boss", Bosses.main_world),
        "Wizard's Den Orb": LocationData(110511, "orb", Orbs.main_world),
        "Wizards' Den Chest": LocationData(112220, "hc", HiddenChests.main_world),
        "Wizards' Den Pedestal": LocationData(112720, "peds", Pedestals.main_world),
    },
    "Powerplant": {
        "Kolmisilman silma": LocationData(110710, "boss", Bosses.main_world),
        "Power Plant Chest": LocationData(112240, "hc", HiddenChests.main_world),
        "Power Plant Pedestal": LocationData(112740, "peds", Pedestals.main_world),
    },
    "Snow Chasm": {
        "Unohdettu": LocationData(110670, "boss", Bosses.main_world),
        "Snow Chasm Orb": LocationData(110510, "orb", Orbs.main_world),
    },
    "Deep Underground": {
        "Limatoukka": LocationData(110610, "boss", Bosses.main_world),
    },
    "The Laboratory": {
        "Kolmisilma": LocationData(110600, "boss", Bosses.main_path),
    },
    "Friend Cave": {
        "Toveri": LocationData(110680, "boss", Bosses.main_world),
    },
    "The Work (Hell)": {
        "The Work (Hell) Orb": LocationData(110509, "orb", Orbs.main_world),
    },
}


location_name_to_id: Dict[str, int] = {}
for location_group in location_region_mapping.values():
    for locname, locinfo in location_group.items():
        if locinfo.ltype in ["hc", "peds"]:
            for i in range(20):
                location_name_to_id.update({f"{locname} {i + 1}": locinfo.id + i - 1})
        else:
            location_name_to_id.update({locname: locinfo.id})
