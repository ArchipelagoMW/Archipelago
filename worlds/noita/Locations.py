# Locations are specific points that you would obtain an item at.
import functools
from enum import IntEnum
from typing import Dict, List, Union, Set, NamedTuple, Optional
from BaseClasses import Location
from .Options import TotalLocations


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


# todo: figure out how to add umlauts and stuff
# 111000 - 111034
# Mapping of items in each region
location_region_mapping: Dict[str, Dict[str, LocationData]] = {
    "Forest": {
        # 110000 - 110500
        # Just putting these here for now
        f"Chest{i+1}": LocationData(110000+i) for i in range(TotalLocations.range_end)
    },
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
    "Mines Hidden Chests": {
        f"Mines Chest {i + 1}": LocationData(112000 + i, "hc", HiddenChests.main_path) for i in range(20)
    },
    "Collapsed Mines Hidden Chests": {
        f"Collapsed Mines Chest {i + 1}": LocationData(112020 + i, "hc", HiddenChests.side_path) for i in range(20)
    },
    "Coal Pits Hidden Chests": {
        f"Coal Pits Chest {i + 1}": LocationData(112040 + i, "hc", HiddenChests.main_path) for i in range(20)
    },
    "Fungal Caverns Hidden Chests": {
        f"Fungal Caverns Chest {i + 1}": LocationData(112060 + i, "hc", HiddenChests.side_path) for i in range(20)
    },
    "Snowy Depths Hidden Chests": {
        f"Snowy Depths Chest {i + 1}": LocationData(112080 + i, "hc", HiddenChests.main_path) for i in range(20)
    },
    "Hiisi Base Hidden Chests": {
        f"Hiisi Base Chest {i + 1}": LocationData(112100 + i, "hc", HiddenChests.main_path) for i in range(20)
    },
    "Underground Jungle Hidden Chests": {
        f"Underground Jungle Chest {i + 1}": LocationData(112120 + i, "hc", HiddenChests.main_path) for i in range(20)
    },
    "Lukki Lair Hidden Chests": {
        f"Lukki Lair Chest {i + 1}": LocationData(112140 + i, "hc", HiddenChests.side_path) for i in range(20)
    },
    "Vault Hidden Chests": {
        f"Vault Chest {i + 1}": LocationData(112160 + i, "hc", HiddenChests.main_path) for i in range(20)
    },
    "Temple of the Art Hidden Chests": {
        f"Temple of the Art Chest {i + 1}": LocationData(112180 + i, "hc", HiddenChests.main_path) for i in range(20)
    },
    "Overgrown Cavern Hidden Chests": {
        f"Overgrown Cavern Chest {i + 1}": LocationData(112200 + i, "hc", HiddenChests.main_world) for i in range(20)
    },
    "Wizards' Den Hidden Chests": {
        f"Wizards' Den Chest {i + 1}": LocationData(112220 + i, "hc", HiddenChests.main_world) for i in range(20)
    },
    "Power Plant Hidden Chests": {
        f"Power Plant Chest {i + 1}": LocationData(112240 + i, "hc", HiddenChests.main_world) for i in range(20)
    },
    "Frozen Vault Hidden Chests": {
        f"Frozen Vault Chest {i + 1}": LocationData(112260 + i, "hc", HiddenChests.main_world) for i in range(20)
    },
    "The Tower Hidden Chests": {
        f"The Tower Chest {i + 1}": LocationData(112280 + i, "hc", HiddenChests.main_world) for i in range(20)
    },
    "Floating Island": {
        "Floating Island Orb": LocationData(110501, "orb", Orbs.main_path),
    },
    "Pyramid": {
        "Kolmisilman Koipi": LocationData(110630, "boss", Bosses.main_world),
        "Pyramid Orb": LocationData(110502, "orb", Orbs.main_world),
        "Sandcave Orb": LocationData(110505, "orb", Orbs.main_world),
    },
    "Lake": {
        "Syvaolento": LocationData(110650, "boss", Bosses.main_world),
    },
    "Frozen Vault": {
        "Frozen Vault Orb": LocationData(110503, "orb", Orbs.main_world),
    },
    "Ancient Laboratory": {
        "Ylialkemisti": LocationData(110700, "boss", Bosses.side_path),
    },
    "Abyss Orb Room": {
        "Sauvojen Tuntija": LocationData(110640, "boss", Bosses.main_path),
        "Abyss Orb": LocationData(110508, "orb", Orbs.main_path),
    },
    "Below Lava Lake": {
        "Lava Lake Orb": LocationData(110504, "orb", Orbs.side_path),
    },
    "Magical Temple": {
        "Magical Temple Orb": LocationData(110506, "orb", Orbs.side_path),
    },
    "Underground Jungle": {
        "Suomuhauki": LocationData(110620, "boss", Bosses.main_path),
    },
    "Lukki Lair": {
        "Lukki Lair Orb": LocationData(110507, "orb", Orbs.side_path),
    },
    "Temple of the Art": {
        "Gate Guardian": LocationData(110660, "boss", Bosses.main_path),
    },
    "The Laboratory": {
        "Kolmisilma": LocationData(110600, "boss", Bosses.side_path),
    },
    "Snow Chasm": {
        "Unohdettu": LocationData(110670, "boss", Bosses.main_world),
        "Snow Chasm Orb": LocationData(110510, "orb", Orbs.main_world),
    },
    "Wizard's Den": {
        "Mestarien mestari": LocationData(110700, "boss", Bosses.main_world),
        "Wizard's Den Orb": LocationData(110511, "orb", Orbs.main_world),
    },
    "Powerplant": {
        "Kolmisilman silma": LocationData(110710, "boss", Bosses.main_world),
    },
    "Deep Underground": {
        "Limatoukka": LocationData(110610, "boss", Bosses.main_world),
    },
    "Friend Cave": {
        "Toveri": LocationData(110680, "boss", Bosses.main_world),
    },
    "The Work (Hell)": {
        "The Work (Hell) Orb": LocationData(110509, "orb", Orbs.main_world),
    },
}

# todo: find a way to get these location counts without manually reading through, or remove the need for them
num_static_locations = sum([len(locs) for locs in location_region_mapping.values()]) - TotalLocations.range_end  # 58
total_locations_generated = sum([len(locs) for locs in location_region_mapping.values()]) - num_static_locations  # 500
orb_mp_locations = 5
orb_mw_locations = 6
boss_mp_locations = 5
boss_mw_locations = 7
shop_locations = 35

# length of 558 entries
location_name_to_id: Dict[str, int] = {}
for location_group in location_region_mapping.values():
    for locname, locinfo in location_group.items():
        location_name_to_id.update({locname: locinfo.id})
