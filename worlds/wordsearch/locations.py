from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import WordSearchWorld


class WordSearchLocation(Location):
    game = "WordSearch"


class WordSearchLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["WordSearchWorld"], bool] = lambda world: True


location_data_table: Dict[str, WordSearchLocationData] = {
}

def get_location_table():
    location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
    location_table["1 Word Found"] = 101
    for i in range(99):
        location_table[str(i + 2) + " Words Found"] = 102 + i
    return location_table
