import typing

from BaseClasses import Location
from .Names import LocationName


class LegacyLocation(Location):
    game: str = "Rogue Legacy"


base_location_table = {
    # Manor Renovations
    LocationName.manor_ground_base: 91000,
    LocationName.manor_main_base: 91001,
    LocationName.manor_main_bottom_window: 91002,
    LocationName.manor_main_top_window: 91003,
    LocationName.manor_main_roof: 91004,
    LocationName.manor_left_wing_base: 91005,
    LocationName.manor_left_wing_window: 91006,
    LocationName.manor_left_wing_roof: 91007,
    LocationName.manor_left_big_base: 91008,
    LocationName.manor_left_big_upper1: 91009,
    LocationName.manor_left_big_upper2: 91010,
    LocationName.manor_left_big_windows: 91011,
    LocationName.manor_left_big_roof: 91012,
    LocationName.manor_left_far_base: 91013,
    LocationName.manor_left_far_roof: 91014,
    LocationName.manor_left_extension: 91015,
    LocationName.manor_left_tree1: 91016,
    LocationName.manor_left_tree2: 91017,
    LocationName.manor_right_wing_base: 91018,
    LocationName.manor_right_wing_window: 91019,
    LocationName.manor_right_wing_roof: 91020,
    LocationName.manor_right_big_base: 91021,
    LocationName.manor_right_big_upper: 91022,
    LocationName.manor_right_big_roof: 91023,
    LocationName.manor_right_high_base: 91024,
    LocationName.manor_right_high_upper: 91025,
    LocationName.manor_right_high_tower: 91026,
    LocationName.manor_right_extension: 91027,
    LocationName.manor_right_tree: 91028,
    LocationName.manor_observatory_base: 91029,
    LocationName.manor_observatory_scope: 91030,

    # Boss Rewards
    LocationName.boss_castle: 91100,
    LocationName.boss_forest: 91102,
    LocationName.boss_tower: 91104,
    LocationName.boss_dungeon: 91106,

    # Special Rooms
    LocationName.special_jukebox: 91200,
    LocationName.special_painting: 91201,
    LocationName.special_cheapskate: 91202,
    LocationName.special_carnival: 91203,

    # Special Locations
    LocationName.castle: None,
    LocationName.garden: None,
    LocationName.tower: None,
    LocationName.dungeon: None,
    LocationName.fountain: None,
}

diary_location_table = {f"{LocationName.diary} {i + 1}": i + 91300 for i in range(0, 25)}

fairy_chest_location_table = {
    **{f"{LocationName.castle} - Fairy Chest {i + 1}": i + 91400 for i in range(0, 50)},
    **{f"{LocationName.garden} - Fairy Chest {i + 1}": i + 91450 for i in range(0, 50)},
    **{f"{LocationName.tower} - Fairy Chest {i + 1}": i + 91500 for i in range(0, 50)},
    **{f"{LocationName.dungeon} - Fairy Chest {i + 1}": i + 91550 for i in range(0, 50)},
    **{f"Fairy Chest {i + 1}": i + 92200 for i in range(0, 60)},
}

chest_location_table = {
    **{f"{LocationName.castle} - Chest {i + 1}": i + 91600 for i in range(0, 100)},
    **{f"{LocationName.garden} - Chest {i + 1}": i + 91700 for i in range(0, 100)},
    **{f"{LocationName.tower} - Chest {i + 1}": i + 91800 for i in range(0, 100)},
    **{f"{LocationName.dungeon} - Chest {i + 1}": i + 91900 for i in range(0, 100)},
    **{f"Chest {i + 1}": i + 92000 for i in range(0, 120)},
}

location_table = {
    **base_location_table,
    **diary_location_table,
    **fairy_chest_location_table,
    **chest_location_table,
}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in location_table.items()}
