from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import WordipelagoWorld


class WordipelagoLocation(Location):
    game = "Wordipelago"


class WordipelagoLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["WordipelagoWorld"], bool] = lambda world: True


location_data_table: Dict[str, WordipelagoLocationData] = {
    "Used A": WordipelagoLocationData(region="Letters", address=1),
    "Used B": WordipelagoLocationData(region="Letters", address=2),
    "Used C": WordipelagoLocationData(region="Letters", address=3),
    "Used D": WordipelagoLocationData(region="Letters", address=4),
    "Used E": WordipelagoLocationData(region="Letters", address=5),
    "Used F": WordipelagoLocationData(region="Letters", address=6),
    "Used G": WordipelagoLocationData(region="Letters", address=7),
    "Used H": WordipelagoLocationData(region="Letters", address=8),
    "Used I": WordipelagoLocationData(region="Letters", address=9),
    "Used J": WordipelagoLocationData(region="Letters", address=10),
    "Used K": WordipelagoLocationData(region="Letters", address=11),
    "Used L": WordipelagoLocationData(region="Letters", address=12),
    "Used M": WordipelagoLocationData(region="Letters", address=13),
    "Used N": WordipelagoLocationData(region="Letters", address=14),
    "Used O": WordipelagoLocationData(region="Letters", address=15),
    "Used P": WordipelagoLocationData(region="Letters", address=16),
    "Used Q": WordipelagoLocationData(region="Letters", address=17),
    "Used R": WordipelagoLocationData(region="Letters", address=18),
    "Used S": WordipelagoLocationData(region="Letters", address=19),
    "Used T": WordipelagoLocationData(region="Letters", address=20),
    "Used U": WordipelagoLocationData(region="Letters", address=21),
    "Used V": WordipelagoLocationData(region="Letters", address=22),
    "Used W": WordipelagoLocationData(region="Letters", address=23),
    "Used X": WordipelagoLocationData(region="Letters", address=24),
    "Used Y": WordipelagoLocationData(region="Letters", address=25),
    "Used Z": WordipelagoLocationData(region="Letters", address=26),

    "1 Correct Letter In Word": WordipelagoLocationData(region="WordBest", address=101),
    "2 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=102),
    "3 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=103),
    "4 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=104),
    "5 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=105),
}

def get_location_table():
    location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
    for i in range(1000):
        location_table["Word " + str(i + 1)] = 201 + i
    return location_table
