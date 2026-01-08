from typing import Dict, List, NamedTuple


class BingoRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, BingoRegionData] = {
    "Menu": BingoRegionData(["Bingo Board"]),
    "Bingo Board": BingoRegionData(),
}
