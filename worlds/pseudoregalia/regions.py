from typing import NamedTuple, Callable, Dict, List
from BaseClasses import CollectionState
from .options import SpawnPoint


class RegionExit(NamedTuple):
    region: str
    access_rule: Callable[[CollectionState, int], bool] = lambda state, player: True
    breakable_wall: bool = False


origin_region_names: dict[int, str] = {
    SpawnPoint.option_castle_main: "Castle Main",
    SpawnPoint.option_castle_gazebo: "Castle Main",
    SpawnPoint.option_dungeon_mirror: "Dungeon Mirror",
    SpawnPoint.option_library: "Library Main",
    SpawnPoint.option_underbelly_south: "Underbelly => Bailey",
    SpawnPoint.option_underbelly_big_room: "Underbelly Main Upper",
    SpawnPoint.option_bailey_main: "Bailey Lower",
    SpawnPoint.option_keep_main: "Keep Main",
    SpawnPoint.option_keep_north: "Keep Main",
    SpawnPoint.option_theatre_main: "Theatre Main",
}


region_table: Dict[str, List[str]] = {
    "Dungeon Mirror":
        ["Dungeon Slide"],
    "Dungeon Slide":
        ["Dungeon Mirror",
         "Dungeon Strong Eyes",
         "Dungeon Escape Lower"],
    "Dungeon Strong Eyes":
        ["Dungeon Slide",
         "Dungeon => Castle"],
    "Dungeon => Castle":
        ["Dungeon Mirror",
         "Dungeon Strong Eyes",
         "Castle Main"],
    "Dungeon Escape Lower":
        ["Dungeon Slide",
         "Dungeon Escape Upper",
         "Underbelly => Dungeon"],
    "Dungeon Escape Upper":
        ["Dungeon Escape Lower",
         "Theatre Outside Scythe Corridor"],

    "Castle Main":
        ["Dungeon => Castle",
         "Keep Main",
         "Bailey Lower",
         "Library Main",
         "Castle => Theatre Pillar",
         "Castle Spiral Climb",
         "Keep (Northeast) => Castle"],
    "Castle Spiral Climb":
        ["Castle Main",
         "Castle High Climb",
         "Castle By Scythe Corridor",],
    "Castle High Climb":
        [],
    "Castle By Scythe Corridor":
        ["Castle Spiral Climb",
         "Castle High Climb",
         "Castle => Theatre (Front)",],
    "Castle => Theatre (Front)":
        ["Castle By Scythe Corridor",
         "Castle Moon Room",
         "Theatre Main",],
    "Castle Moon Room":
        [],

    "Library Main":
        ["Library Locked",
         "Library Greaves",
         "Library Top",
         "Castle Main"],
    "Library Locked":
        [],
    "Library Greaves":
        ["Library Back"],
    "Library Top":
        ["Library Back"],
    "Library Back":
        ["Library Greaves",
         "Library Top"],

    "Keep Main":
        ["Keep Locked Room",
         "Keep Sunsetter",
         "Keep Throne Room",
         "Keep => Underbelly",
         "Theatre Outside Scythe Corridor",
         "Keep (Northeast) => Castle",
         "Castle Main"],
    "Keep Locked Room":
        ["Keep Sunsetter"],
    "Keep Sunsetter":
        [],
    "Keep Throne Room":
        [],
    "Keep => Underbelly":
        ["Keep Main",
         "Underbelly => Keep"],
    "Keep (Northeast) => Castle":
        ["Keep Main",
         "Castle Main"],

    "Bailey Lower":
        ["Bailey Upper",
         "Castle Main",
         "Theatre Pillar => Bailey",],
    "Bailey Upper":
        ["Bailey Lower",
         "Underbelly => Bailey",
         "Tower Remains",],
    "Tower Remains":
        ["The Great Door",],

    "Underbelly => Dungeon":
        ["Dungeon Escape Lower",
         "Underbelly Light Pillar",
         "Underbelly Ascendant Light"],
    "Underbelly Light Pillar":
        ["Underbelly Main Upper",
         "Underbelly => Dungeon",
         "Underbelly Ascendant Light"],
    "Underbelly Ascendant Light":
        ["Underbelly => Dungeon"],
    "Underbelly Main Lower":
        ["Underbelly => Bailey",
         "Underbelly Hole",
         "Underbelly By Heliacal",
         "Underbelly Main Upper"],
    "Underbelly Main Upper":
        ["Underbelly Main Lower",
         "Underbelly Light Pillar",
         "Underbelly By Heliacal"],
    "Underbelly By Heliacal":
        ["Underbelly Main Upper"],
    "Underbelly => Bailey":
        ["Bailey Upper",
         "Bailey Lower",
         "Underbelly Main Lower",],
    "Underbelly => Keep":
        ["Keep => Underbelly",
         "Underbelly Hole"],
    "Underbelly Hole":
        ["Underbelly Main Lower",
         "Underbelly => Keep"],

    "Theatre Main":
        ["Theatre Outside Scythe Corridor",
         "Theatre Pillar",
         "Castle => Theatre (Front)"],
    "Theatre Pillar => Bailey":
        ["Theatre Pillar",
         "Bailey Lower"],
    "Castle => Theatre Pillar":
        ["Theatre Pillar",
         "Castle Main"],
    "Theatre Pillar":
        ["Theatre Main",
         "Theatre Pillar => Bailey",
         "Castle => Theatre Pillar",],
    "Theatre Outside Scythe Corridor":
        ["Theatre Main",
         "Dungeon Escape Upper",
         "Keep Main"],

    "The Great Door":
        [],
}
