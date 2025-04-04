from typing import Dict, List, NamedTuple

from .Names import RegionName

class Celeste64RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, Celeste64RegionData] = {
    "Menu": Celeste64RegionData([RegionName.forsaken_city]),

    RegionName.forsaken_city: Celeste64RegionData([RegionName.intro_islands, RegionName.granny_island, RegionName.highway_island, RegionName.ne_feathers_island, RegionName.se_house_island, RegionName.badeline_tower_upper, RegionName.badeline_island]),

    RegionName.intro_islands:        Celeste64RegionData([RegionName.granny_island]),
    RegionName.granny_island:        Celeste64RegionData([RegionName.highway_island, RegionName.nw_girders_island, RegionName.badeline_tower_lower, RegionName.se_house_island]),
    RegionName.highway_island:       Celeste64RegionData([RegionName.granny_island, RegionName.ne_feathers_island, RegionName.nw_girders_island]),
    RegionName.nw_girders_island:    Celeste64RegionData([RegionName.highway_island]),
    RegionName.ne_feathers_island:   Celeste64RegionData([RegionName.se_house_island, RegionName.highway_island, RegionName.badeline_tower_lower, RegionName.badeline_tower_upper]),
    RegionName.se_house_island:      Celeste64RegionData([RegionName.ne_feathers_island, RegionName.granny_island, RegionName.badeline_tower_lower]),
    RegionName.badeline_tower_lower: Celeste64RegionData([RegionName.se_house_island, RegionName.ne_feathers_island, RegionName.granny_island, RegionName.badeline_tower_upper]),
    RegionName.badeline_tower_upper: Celeste64RegionData([RegionName.badeline_island, RegionName.badeline_tower_lower, RegionName.se_house_island, RegionName.ne_feathers_island, RegionName.granny_island]),
    RegionName.badeline_island:      Celeste64RegionData([RegionName.badeline_tower_upper, RegionName.granny_island, RegionName.highway_island]),
}
