from typing import List, Tuple, Optional

from BaseClasses import Location, LocationProgressType as LocProg, Region
from . import data
from .options import SonicRushOptions

location_description = {}

act_locations: List[Tuple[str, str, LocProg]] = [
    (f"{zone} Act {act} ({char})", f"{zone} ({char})", LocProg.DEFAULT)
    for zone in data.zone_names_without_f_zone
    for act in [1, 2]
    for char in ["Sonic", "Blaze"]
]

act_s_rank_locations: List[Tuple[str, str, LocProg]] = [
    (f"{zone} Act {act} S Rank ({char})", f"{zone} ({char})", LocProg.DEFAULT)
    for zone in data.zone_names_without_f_zone
    for act in [1, 2]
    for char in ["Sonic", "Blaze"]
]

boss_locations: List[Tuple[str, str, LocProg]] = [
    (f"{zone} Boss ({char})", f"{zone} ({char})", LocProg.PRIORITY)
    for zone in data.zone_names_without_f_zone
    for char in ["Sonic", "Blaze"]
]

boss_s_rank_locations: List[Tuple[str, str, LocProg]] = [
    (f"{zone} Boss S Rank ({char})", f"{zone} ({char})", LocProg.PRIORITY)
    for zone in data.zone_names_without_f_zone
    for char in ["Sonic", "Blaze"]
]

f_zone_locations: List[Tuple[str, str, LocProg]] = [
    ("F-Zone (Sonic)", "F-Zone (Sonic)", LocProg.PRIORITY),
    ("F-Zone (Blaze)", "F-Zone (Blaze)", LocProg.PRIORITY),
]

screw_f_zone_locations: List[Tuple[str, str, LocProg]] = [
    ("F-Zone (Sonic)", "F-Zone (Sonic)", LocProg.EXCLUDED),
    ("F-Zone (Blaze)", "F-Zone (Blaze)", LocProg.EXCLUDED),
]

extra_zone_locations: List[Tuple[str, str, LocProg]] = [
    ("Extra Zone", "Extra Zone", LocProg.PRIORITY),
]

special_stage_locations: List[Tuple[str, str, LocProg]] = [
    (f"{zone} Special Stage", f"{zone} (Sonic)", LocProg.PRIORITY)
    for zone in data.zone_names_without_f_zone
]

menu_locations: List[Tuple[str, str, LocProg]] = [
    ("Menu", "Menu", LocProg.DEFAULT)
]

all_locations: List[str] = [
    loc[0] for loc in (
        act_locations +
        act_s_rank_locations +
        boss_locations +
        boss_s_rank_locations +
        f_zone_locations +
        screw_f_zone_locations +
        extra_zone_locations +
        special_stage_locations +
        menu_locations
    )
]


def add_base_acts(options: SonicRushOptions) -> List[Tuple[str, str, LocProg]]:
    return act_locations + (
        act_s_rank_locations if options.include_s_rank_checks in ["only_acts", "all"] else []
    )


def add_bosses(options: SonicRushOptions) -> List[Tuple[str, str, LocProg]]:
    return boss_locations + (
        boss_s_rank_locations if options.include_s_rank_checks in ["only_bosses", "all"] else []
    ) + (
        screw_f_zone_locations if options.screw_f_zone else f_zone_locations
    ) + (
        extra_zone_locations if not options.goal == "extra_zone" else []
    )


def add_special_stages(options: SonicRushOptions) -> List[Tuple[str, str, LocProg]]:
    return special_stage_locations


def add_menu_locations(options: SonicRushOptions) -> List[Tuple[str, str, LocProg]]:
    return menu_locations


class SonicRushLocation(Location):
    game = "Sonic Rush"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocProg):
        super(SonicRushLocation, self).__init__(player, name, address, region)
        self.progress_type = progress_type
