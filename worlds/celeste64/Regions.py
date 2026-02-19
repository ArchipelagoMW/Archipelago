from typing import Dict, List, NamedTuple

from .Names import RegionName

class Celeste64RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, Celeste64RegionData] = {
    "Menu": Celeste64RegionData([RegionName.forsaken_city]),

    RegionName.forsaken_city: Celeste64RegionData([RegionName.intro_islands, RegionName.granny_island, RegionName.highway_island, RegionName.ne_feathers_island, RegionName.se_house_island, RegionName.badeline_tower_upper, RegionName.badeline_island]),

    RegionName.intro_islands:        Celeste64RegionData([RegionName.granny_island]),
    RegionName.granny_island:        Celeste64RegionData([RegionName.highway_island, RegionName.nw_girders_island, RegionName.badeline_tower_lower, RegionName.se_house_island, RegionName.cassette_entrance_1, RegionName.cassette_entrance_2, RegionName.cassette_entrance_4]),
    RegionName.highway_island:       Celeste64RegionData([RegionName.granny_island, RegionName.ne_feathers_island, RegionName.nw_girders_island, RegionName.cassette_entrance_3, RegionName.cassette_entrance_6]),
    RegionName.nw_girders_island:    Celeste64RegionData([RegionName.highway_island]),
    RegionName.ne_feathers_island:   Celeste64RegionData([RegionName.se_house_island, RegionName.highway_island, RegionName.badeline_tower_lower, RegionName.badeline_tower_upper, RegionName.cassette_entrance_7, RegionName.cassette_entrance_8]),
    RegionName.se_house_island:      Celeste64RegionData([RegionName.ne_feathers_island, RegionName.granny_island, RegionName.badeline_tower_lower, RegionName.cassette_entrance_5]),
    RegionName.badeline_tower_lower: Celeste64RegionData([RegionName.se_house_island, RegionName.ne_feathers_island, RegionName.granny_island, RegionName.badeline_tower_upper]),
    RegionName.badeline_tower_upper: Celeste64RegionData([RegionName.badeline_island, RegionName.badeline_tower_lower, RegionName.se_house_island, RegionName.ne_feathers_island, RegionName.granny_island, RegionName.cassette_entrance_9]),
    RegionName.badeline_island:      Celeste64RegionData([RegionName.badeline_tower_upper, RegionName.granny_island, RegionName.highway_island, RegionName.cassette_entrance_10]),

    RegionName.cassette_1:  Celeste64RegionData([]),
    RegionName.cassette_2:  Celeste64RegionData([]),
    RegionName.cassette_3:  Celeste64RegionData([]),
    RegionName.cassette_4:  Celeste64RegionData([]),
    RegionName.cassette_5:  Celeste64RegionData([]),
    RegionName.cassette_6:  Celeste64RegionData([]),
    RegionName.cassette_7:  Celeste64RegionData([]),
    RegionName.cassette_8:  Celeste64RegionData([]),
    RegionName.cassette_9:  Celeste64RegionData([]),
    RegionName.cassette_10: Celeste64RegionData([]),

    RegionName.cassette_entrance_1:  Celeste64RegionData([]),
    RegionName.cassette_entrance_2:  Celeste64RegionData([]),
    RegionName.cassette_entrance_3:  Celeste64RegionData([]),
    RegionName.cassette_entrance_4:  Celeste64RegionData([]),
    RegionName.cassette_entrance_5:  Celeste64RegionData([]),
    RegionName.cassette_entrance_6:  Celeste64RegionData([]),
    RegionName.cassette_entrance_7:  Celeste64RegionData([]),
    RegionName.cassette_entrance_8:  Celeste64RegionData([]),
    RegionName.cassette_entrance_9:  Celeste64RegionData([]),
    RegionName.cassette_entrance_10: Celeste64RegionData([]),
}

cassette_entrance_regions: List[str] = [
    RegionName.cassette_entrance_1,
    RegionName.cassette_entrance_2,
    RegionName.cassette_entrance_3,
    RegionName.cassette_entrance_4,
    RegionName.cassette_entrance_5,
    RegionName.cassette_entrance_6,
    RegionName.cassette_entrance_7,
    RegionName.cassette_entrance_8,
    RegionName.cassette_entrance_9,
    RegionName.cassette_entrance_10,
]

cassette_regions: List[str] = [
    RegionName.cassette_1,
    RegionName.cassette_2,
    RegionName.cassette_3,
    RegionName.cassette_4,
    RegionName.cassette_5,
    RegionName.cassette_6,
    RegionName.cassette_7,
    RegionName.cassette_8,
    RegionName.cassette_9,
    RegionName.cassette_10,
]
