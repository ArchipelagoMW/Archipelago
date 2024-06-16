from typing import Dict, List, NamedTuple


class Celeste64RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, Celeste64RegionData] = {
    "Menu": Celeste64RegionData(["Forsaken City"]),
    "Forsaken City": Celeste64RegionData(),
}
