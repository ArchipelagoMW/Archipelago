from typing import Callable, Dict, List, NamedTuple
from BaseClasses import CollectionState


class WordipelagoRegionData(NamedTuple):
    connecting_regions: List[str] = []
    rules: Dict[str, Callable[[CollectionState], bool]] = None

region_data_table: Dict[str, WordipelagoRegionData] = {
    "Menu": WordipelagoRegionData(["Letters"]),
    "Letters": WordipelagoRegionData(
        [ "Word Best", "Green Checks", "Yellow Checks", "Point Shop"]
    ),
    "Words": WordipelagoRegionData([]),
    "Words Chunk 1": WordipelagoRegionData([]),
    "Words Chunk 2": WordipelagoRegionData([]),
    "Words Chunk 3": WordipelagoRegionData([]),
    "Words Chunk 4": WordipelagoRegionData([]),
    "Words Chunk 5": WordipelagoRegionData([]),
    "Streaks": WordipelagoRegionData([]),
    "Streaks Chunk 1": WordipelagoRegionData([]),
    "Streaks Chunk 2": WordipelagoRegionData([]),
    "Streaks Chunk 3": WordipelagoRegionData([]),
    "Streaks Chunk 4": WordipelagoRegionData([]),
    "Streaks Chunk 5": WordipelagoRegionData([]),
    "Point Shop": WordipelagoRegionData([]),
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
    "Green Checks 5": WordipelagoRegionData(["Words, Words Chunk 1"]),
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
