from typing import Dict, List, NamedTuple


class WordipelagoRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, WordipelagoRegionData] = {
    "Menu": WordipelagoRegionData(["Letters"]),
    "Letters": WordipelagoRegionData([ "Words", "Word Best", "Green Checks", "Yellow Checks"]),
    "Words": WordipelagoRegionData([]),
    "Green Checks": WordipelagoRegionData([]),
    "Yellow Checks": WordipelagoRegionData([]),
    "Word Best": WordipelagoRegionData([]),
}
