from typing import Dict, List, NamedTuple


class PaintRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, PaintRegionData] = {
    "Menu": PaintRegionData(["Canvas"]),
    "Canvas": PaintRegionData(),
}
