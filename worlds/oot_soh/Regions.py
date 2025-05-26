from typing import Dict, List, NamedTuple


class SohRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, SohRegionData] = {
    "Menu": SohRegionData(["Hyrule"]),
    "Hyrule": SohRegionData(),
}
