from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Final

from BaseClasses import ItemClassification
from .Locations import LocationData, get_locations_by_tags

# Item name to ram value conversion
item_ids: Final[Mapping[str, int]] = MappingProxyType({
    "Strength": 0x000002,
    "Speed": 0x000003,
    "Magic": 0x000004,
    "Armour": 0x000005,
    "Gold": 0x000006,
    "Key": 0x000007,
    "XP": 0x000009,
    "Level": 0x00000A,
    "Class": 0x00000B,
    "Max": 0x00000D,
    "Compass": 0x000270,
    "Lightning Potion": 0x001008,
    "Light Potion": 0x002008,
    "Acid Potion": 0x003008,
    "Fire Potion": 0x004008,
    "Acid Breath": 0x800480,
    "Lightning Breath": 0x8004F0,
    "Fire Breath": 0x800460,
    "Light Amulet": 0x400870,
    "Acid Amulet": 0x400880,
    "Lightning Amulet": 0x4008F0,
    "Fire Amulet": 0x400860,
    "Lightning Shield": 0x400CF0,
    "Fire Shield": 0x400C60,
    "Invisibility": 0x4000E0,
    "Levitate": 0x400030,
    "Speed Boots": 0x400173,
    "3-Way Shot": 0x400020,
    "5-Way Shot": 0x400160,
    "Rapid Fire": 0x400050,
    "Reflective Shot": 0x400840,
    "Reflective Shield": 0x400C40,
    "Super Shot": 0x8008B0,
    "Timestop": 0x4000D0,
    "Phoenix Familiar": 0x400110,
    "Growth": 0x400120,
    "Shrink": 0x400130,
    "Thunder Hammer": 0x800940,
    "Anti-Death Halo": 0x7000A0,
    "Invulnerability": 0x7000C0,
    "Health": 0x000001,
    "Runestone": 0x008210,
    "Mirror Shard": 0x008260,
    "Ice Axe of Untar": 0x8201C0,
    "Flame of Tarkana": 0x8201D0,
    "Scimitar of Decapitation": 0x8201E0,
    "Marker's Javelin": 0x8201F0,
    "Soul Savior": 0x820200,
    "Mountain": 0x00804A,
    "Castle": 0x00801A,
    "Hell": 0x00806A,
    "Ice": 0x00807A,
    "Town": 0x00808A,
    "Temple": 0x00809A,
    "Battlefield": 0x0080DA,
    "Skorne": 0x0080EA,
    "Secret": 0x0080FA,
    "Obelisk": 0x00800C,
    "Minotaur": 0x0001A1,
    "Falconess": 0x0001A2,
    "Jackal": 0x0001A3,
    "Tigress": 0x0001A4,
    "Sumner": 0x0001A5,
    "Skorne's Mask": 0x840620,
    "Skorne's Horns": 0x840630,
    "Skorne's Right Gauntlet": 0x840A40,
    "Skorne's Left Gauntlet": 0x840A50,
})

# Character names used for slot data
characters: Final[tuple[str, ...]] = ("Minotaur", "Falconess", "Tigress", "Jackal", "Sumner")

# Base item charge count per pickup
# Some items are bitwise
base_count: Final[Mapping[str, int]] = MappingProxyType({
    "Key": 1,
    "Lightning Potion": 1,
    "Light Potion": 1,
    "Acid Potion": 1,
    "Fire Potion": 1,
    "Acid Breath": 5,
    "Lightning Breath": 5,
    "Fire Breath": 5,
    "Light Amulet": 30,
    "Acid Amulet": 30,
    "Lightning Amulet": 30,
    "Fire Amulet": 30,
    "Lightning Shield": 10,
    "Fire Shield": 10,
    "Invisibility": 30,
    "Levitate": 30,
    "Speed Boots": 30,
    "3-Way Shot": 30,
    "5-Way Shot": 30,
    "Rapid Fire": 30,
    "Reflective Shot": 30,
    "Reflective Shield": 30,
    "Super Shot": 3,
    "Timestop": 15,
    "Phoenix Familiar": 30,
    "Growth": 30,
    "Shrink": 30,
    "Thunder Hammer": 3,
    "Anti-Death Halo": 30,
    "Invulnerability": 30,
    "Fruit": 50,
    "Meat": 100,
    "Gold": 100,
    "Runestone 1": 1,
    "Runestone 2": 2,
    "Runestone 3": 3,
    "Runestone 4": 4,
    "Runestone 5": 5,
    "Runestone 6": 6,
    "Runestone 7": 7,
    "Runestone 8": 8,
    "Runestone 9": 9,
    "Runestone 10": 10,
    "Runestone 11": 11,
    "Runestone 12": 12,
    "Runestone 13": 13,
    "Dragon Mirror Shard": 1,
    "Chimera Mirror Shard": 3,
    "Plague Fiend Mirror Shard": 4,
    "Yeti Mirror Shard": 2,
    "Valley of Fire Obelisk": 1,
    "Dagger Peak Obelisk": 2,
    "Cliffs of Desolation Obelisk": 3,
    "Poisoned Fields Obelisk": 4,
    "Haunted Cemetery Obelisk": 5,
    "Castle Courtyard Obelisk": 6,
    "Dungeon of Torment Obelisk": 7,
    "Ice Axe of Untar": 1,
    "Flame of Tarkana": 1,
    "Scimitar of Decapitation": 1,
    "Marker's Javelin": 1,
    "Soul Savior": 1,
    "Minotaur": 1,
    "Falconess": 1,
    "Tigress": 1,
    "Jackal": 1,
    "Sumner": 1,
    "Poison Fruit": -50,
    "Skorne's Mask": 50,
    "Skorne's Horns": 50,
    "Skorne's Left Gauntlet": 100,
    "Skorne's Right Gauntlet": 100,
    "Portal to Dagger Peak": 1,
    "Portal to Cliffs of Desolation": 2,
    "Portal to Lost Cave": 3,
    "Portal to Volcanic Caverns": 4,
    "Portal to Dragon's Lair": 5,
    "Portal to Dungeon of Torment": 1,
    "Portal to Tower Armory": 2,
    "Portal to Castle Treasury": 3,
    "Portal to Chimera's Keep": 5,
    "Portal to Haunted Cemetery": 1,
    "Portal to Venomous Spire": 2,
    "Portal to Toxic Air Ship": 3,
    "Portal to Vat of the Plague Fiend": 5,
    "Portal to Frozen Camp": 1,
    "Portal to Crystal Mine": 2,
    "Portal to Erupting Fissure": 3,
    "Portal to Yeti's Cavern": 5,
    "Portal to Fortified Towers": 1,
    "Portal to Infernal Fortress": 2
})

# (zone_config << 4) + room_config -> location list
level_locations: Final[Mapping[int, Sequence[LocationData]]] = MappingProxyType({
    # Zone 0x00 - Castle
    0x00: get_locations_by_tags("castle_courtyard"),
    0x01: get_locations_by_tags("dungeon_of_torment"),
    0x02: get_locations_by_tags("tower_armory"),
    0x03: get_locations_by_tags("castle_treasury"),
    0x08: get_locations_by_tags("chimeras_keep"),

    # Zone 0x03 - Mountain
    0x30: get_locations_by_tags("valley_of_fire"),
    0x31: get_locations_by_tags("dagger_peak"),
    0x32: get_locations_by_tags("cliffs_of_desolation"),
    0x33: get_locations_by_tags("lost_cave"),
    0x34: get_locations_by_tags("volcanic_cavern"),
    0x38: get_locations_by_tags("dragons_lair"),

    # Zone 0x07 - Town
    0x70: get_locations_by_tags("poisoned_fields"),
    0x71: get_locations_by_tags("haunted_cemetery"),
    0x72: get_locations_by_tags("venomous_spire"),
    0x73: get_locations_by_tags("toxic_air_ship"),
    0x78: get_locations_by_tags("plague_fiend"),

    # Zone 0x05 - Underworld
    0x50: get_locations_by_tags("gates_of_the_underworld"),

    # Zone 0x06 - Ice
    0x60: get_locations_by_tags("arctic_docks"),
    0x61: get_locations_by_tags("frozen_camp"),
    0x62: get_locations_by_tags("crystal_mine"),
    0x63: get_locations_by_tags("erupting_fissure"),
    0x68: get_locations_by_tags("yeti"),

    # Zone 0x0D - Temple
    0xD0: get_locations_by_tags("desecrated_temple"),
    0xD8: get_locations_by_tags("altar_of_skorne"),

    # Zone 0x0C - Battlefield
    0xC0: get_locations_by_tags("battle_trenches"),
    0xC1: get_locations_by_tags("fortified_towers"),
    0xC2: get_locations_by_tags("infernal_fortress"),
})

local_levels: Final[Sequence[Sequence[LocationData]]] = (
    get_locations_by_tags("castle_courtyard"),
    get_locations_by_tags("dungeon_of_torment"),
    get_locations_by_tags("tower_armory"),
    get_locations_by_tags("castle_treasury"),
    get_locations_by_tags("valley_of_fire"),
    get_locations_by_tags("dagger_peak"),
    get_locations_by_tags("cliffs_of_desolation"),
    get_locations_by_tags("lost_cave"),
    get_locations_by_tags("volcanic_cavern"),
    get_locations_by_tags("poisoned_fields"),
    get_locations_by_tags("haunted_cemetery"),
    get_locations_by_tags("venomous_spire"),
    get_locations_by_tags("toxic_air_ship"),
    get_locations_by_tags("gates_of_the_underworld"),
    get_locations_by_tags("arctic_docks"),
    get_locations_by_tags("frozen_camp"),
    get_locations_by_tags("crystal_mine"),
    get_locations_by_tags("erupting_fissure"),
    get_locations_by_tags("desecrated_temple"),
    get_locations_by_tags("battle_trenches"),
    get_locations_by_tags("fortified_towers"),
    get_locations_by_tags("infernal_fortress")
)

skipped_local_locations: Final[tuple[str, ...]] = (
    "Valley of Fire - Key 1",
    "Valley of Fire - Key 5",
    "Valley of Fire - Obelisk",
    "Dagger Peak - Obelisk",
    "Cliffs of Desolation - Obelisk",
    "Castle Courtyard - Obelisk",
    "Dungeon of Torment - Obelisk",
    "Poisoned Fields - Obelisk",
    "Haunted Cemetery - Obelisk",
    "Dragon's Lair - Dragon Mirror Shard",
    "Chimera's Keep - Chimera Mirror Shard",
    "Vat of the Plague Fiend - Plague Fiend Mirror Shard",
    "Yeti's Cavern - Yeti Mirror Shard"
)

# Compressed level size in ROM
level_size: Final[tuple[int, ...]] = (
    0x9E0,
    0x5E0,
    0x740,
    0x8A0,
    0x90,
    0x3B0,
    0x5A0,
    0x890,
    0x670,
    0x7D0,
    0x90,
    0xCE0,
    0xA50,
    0xA30,
    0x8E0,
    0x20,
    0x760,
    0xE90,
    0xE40,
    0xE00,
    0xCD0,
    0x20,
    0x3F0,
    0x0,
    0xB00,
    0xA30,
    0xB30
)

# Level address in ROM
level_address: Final[tuple[int, ...]] = (
    0xF939B0,
    0xF958B0,
    0xF945B0,
    0xF94EE0,
    0xF84CC0,
    0xF910B0,
    0xF915B0,
    0xF91D00,
    0xF92710,
    0xF92F40,
    0xF84B70,
    0xF84FA0,
    0xF85EB0,
    0xF86B60,
    0xF877C0,
    0xF880E0,
    0xF901C0,
    0xF884E0,
    0xF89370,
    0xF8A5F0,
    0xF8B760,
    0xF8C7C0,
    0xF90B50,
    0x0,
    0xF8D960,
    0xF8E6E0,
    0xF8F110
)

# Level header address in ROM
level_header: Final[tuple[int, ...]] = (
    0xF9DD9C,
    0xF9E07C,
    0xF9DE54,
    0xF9DF0C,
    0xF9DFC4,
    0xF9E6E0,
    0xF9E798,
    0xF9E850,
    0xF9E908,
    0xF9E9C0,
    0xF9EA78,
    0xF9F004,
    0xF9F0BC,
    0xF9F174,
    0xF9F22C,
    0xF9F2E4,
    0xF9E1C0,
    0xF9E330,
    0xF9E3E4,
    0xF9E498,
    0xF9E54C,
    0xF9E600,
    0xF9DC2C,
    0x0,
    0xF9DA04,
    0xF9DABC,
    0xF9DB74
)

# Runestones required to access difficulties
# Used in Rules.py for access calculation
difficulty_lambda: Final[Mapping[int, Sequence[int]]] = MappingProxyType({
    0x3: (0, 1, 2, 3),
    0x0: (0, 3, 4, 5),
    0x7: (0, 5, 6, 7),
    0x6: (0, 7, 8, 9),
    0xD: (0, 9, 10, 11),
    0xC: (0, 11, 12, 13),
    0x5: (0, 13, 13, 13)
})

# ID's for names said by announcer
sounds: Final[Mapping[int, int]] = MappingProxyType({
    0: 0x9D,
    1: 0x9E,
    2: 0xA7,
    3: 0xA5,
    5: 0x9F,
    6: 0xA1,
    7: 0xA0,
    8: 0xA2,
    9: 0xA7
})

# ID's for colors said by announcer
colors: Final[Mapping[int, int]] = MappingProxyType({
    0: 0xA3,
    1: 0xA6,
    2: 0x9C,
    3: 0xA4
})

item_classifications: Final[Mapping[str, ItemClassification]] = MappingProxyType({
    "filler": ItemClassification.filler,
    "useful": ItemClassification.useful,
    "progression": ItemClassification.progression,
    "trap": ItemClassification.trap
})

obelisks: Final[tuple[str, ...]] = (
    "Valley of Fire Obelisk",
    "Dagger Peak Obelisk",
    "Cliffs of Desolation Obelisk",
    "Poisoned Fields Obelisk",
    "Haunted Cemetery Obelisk",
    "Castle Courtyard Obelisk",
    "Dungeon of Torment Obelisk"
)

mirror_shards: Final[tuple[str, ...]] = (
    "Dragon Mirror Shard",
    "Chimera Mirror Shard",
    "Yeti Mirror Shard",
    "Plague Fiend Mirror Shard"
)

portals: Final[Mapping[str, str]] = MappingProxyType({
    "Portal to Dagger Peak": "Mountain",
    "Portal to Cliffs of Desolation": "Mountain",
    "Portal to Lost Cave": "Mountain",
    "Portal to Volcanic Caverns": "Mountain",
    "Portal to Dragon's Lair": "Mountain",
    "Portal to Dungeon of Torment": "Castle",
    "Portal to Tower Armory": "Castle",
    "Portal to Castle Treasury": "Castle",
    "Portal to Chimera's Keep": "Castle",
    "Portal to Frozen Camp": "Ice",
    "Portal to Crystal Mine": "Ice",
    "Portal to Erupting Fissure": "Ice",
    "Portal to Yeti's Cavern": "Ice",
    "Portal to Haunted Cemetery": "Town",
    "Portal to Venomous Spire": "Town",
    "Portal to Toxic Air Ship": "Town",
    "Portal to Vat of the Plague Fiend": "Town",
    "Portal to Fortified Towers": "Battlefield",
    "Portal to Infernal Fortress": "Battlefield"
})

excluded_portals: Final[Mapping[str, list[str]]] = MappingProxyType({
    "Castle" : ["Portal to Dungeon of Torment", "Portal to Tower Armory", "Portal to Castle Treasury", "Portal to Chimera's Keep"],
    "Town" : ["Portal to Haunted Cemetery", "Portal to Venomous Spire", "Portal to Toxic Air Ship", "Portal to Vat of the Plague Fiend"],
    "Ice" : ["Portal to Frozen Camp", "Portal to Crystal Mine", "Portal to Erupting Fissure", "Portal to Yeti's Cavern"],
    "Battlefield" : ["Portal to Fortified Towers", "Portal to Infernal Fortress"]
})

excluded_levels: Final[Mapping[str, list[str]]] = MappingProxyType({
    "Mountain" : ["Valley of Fire", "Dagger Peak", "Cliffs of Desolation", "Lost Cave", "Volcanic Caverns", "Dragon's Lair"],
    "Castle" : ["Castle Courtyard" ,"Dungeon of Torment", "Tower Armory", "Castle Treasury", "Chimera's Keep"],
    "Ice" : ["Arctic Docks", "Frozen Camp", "Crystal Mine", "Erupting Fissure", "Yeti's Cavern"],
    "Town" : ["Poisoned Fields", "Haunted Cemetery", "Venomous Spire", "Toxic Air Ship", "Vat of the Plague Fiend"],
    "Battlefield" : ["Battle Trenches", "Fortified Towers", "Infernal Fortress"]
})

excluded_obelisks: Final[Mapping[str, list[str]]] = MappingProxyType({
    "Castle" : ["Valley of Fire Obelisk", "Dagger Peak Obelisk", "Cliffs of Desolation Obelisk"],
    "Town" : ["Castle Courtyard Obelisk", "Dungeon of Torment Obelisk"],
    "Ice" : ["Poisoned Fields Obelisk", "Haunted Cemetery Obelisk"],
})

# Map location names to offsets in decompressed boss.bin
boss_location_offsets: Final[Mapping[str, int]] = MappingProxyType({
    "Dragon's Lair - Dragon Mirror Shard": 0x9C08,
    "Yeti's Cavern - Yeti Mirror Shard": 0x9C18,
    "Chimera's Keep - Chimera Mirror Shard": 0x9C28,
    "Vat of the Plague Fiend - Plague Fiend Mirror Shard": 0x9C38,
    "Altar of Skorne - Skorne's Mask": 0x9C48,
    "Altar of Skorne - Skorne's Horns": 0x9C58,
    "Altar of Skorne - Skorne's Left Gauntlet": 0x9C68,
    "Altar of Skorne - Skorne's Right Gauntlet": 0x9C78
})

