from typing import Dict, List, NamedTuple


class CelesteRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, CelesteRegionData] = {
    "Menu": CelesteRegionData(["Forsaken City"]),
    "Forsaken City": CelesteRegionData(),
}
