from typing import Callable, Dict, List, NamedTuple
from BaseClasses import CollectionState


class WordipelagoRegionData(NamedTuple):
    connecting_regions: List[str] = []
    rules: Dict[str, Callable[[CollectionState], bool]] = None

region_data_table: Dict[str, WordipelagoRegionData] = {
    "Menu": WordipelagoRegionData(["Letters"]),
    "Letters": WordipelagoRegionData(
        [ "Word Best", "Green Checks", "Yellow Checks"]
    ),
    "Words": WordipelagoRegionData([]),
    "Green Checks": WordipelagoRegionData(
        ["Green Checks 1"]
    ),
    "Green Checks 1": WordipelagoRegionData(
        ["Green Checks 2"]
    ),
    "Green Checks 2": WordipelagoRegionData(
        ["Green Checks 3"]
    ),
    "Green Checks 3": WordipelagoRegionData(
        ["Green Checks 4"]
    ),
    "Green Checks 4": WordipelagoRegionData(
        ["Green Checks 5"]
    ),
    "Green Checks 5": WordipelagoRegionData(["Words"]),
    "Yellow Checks": WordipelagoRegionData(
        ["Yellow Checks 1"]
    ),
    "Yellow Checks 1": WordipelagoRegionData(
        ["Yellow Checks 2"]
    ),
    "Yellow Checks 2": WordipelagoRegionData(
        ["Yellow Checks 3"]
    ),
    "Yellow Checks 3": WordipelagoRegionData(
        ["Yellow Checks 4"]
    ),
    "Yellow Checks 4": WordipelagoRegionData(
        ["Yellow Checks 5"]
    ),
    "Yellow Checks 5": WordipelagoRegionData([]),
    "Word Best": WordipelagoRegionData([]),
}
