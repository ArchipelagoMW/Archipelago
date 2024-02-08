from typing import Dict, List, NamedTuple


class OoTMMRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, OoTMMRegionData] = {
    "Menu": OoTMMRegionData(["The Button Realm"]),
    "The Button Realm": OoTMMRegionData(),
}
