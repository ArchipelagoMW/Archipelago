import typing

from BaseClasses import Item
from typing import Dict


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    event: bool = False

class WitnessItem(Item):
    game: str = "The Witness"


item_table: Dict[str, ItemData] = {
    'Glass Factory Entry': ItemData(158000, True),
    'Symmetry Island Door 1': ItemData(158001, True),
    'Symmetry Island Door 2': ItemData(158002, True),
    'Mill Entry Door Left': ItemData(158003, True),
    'Quarry Entry Gate 1' : ItemData(158004, True),
    'Treehouse Doors 1&2' : ItemData(158005, True),
    'Treehouse Door 3' : ItemData(158006, True),
    'Treehouse Exterior Door Control' : ItemData(158007, True),
	'Shadows Outer Door Control' : ItemData(158008, True),
    'Monastery Left Door' : ItemData(158009, True),
    'Monastery Right Door' : ItemData(158010, True),
    'Swamp Entry' : ItemData(158011, True),
    'Bunker Entry Door' : ItemData(158012, True),
    'Jungle Pop-up Wall' : ItemData(158013, True),
    'Boat Access' : ItemData(158014, True),
    'Desert Surface Door': ItemData(158015, True),
    'Desert Pond Exit Door': ItemData(158016, True),
    'Town Yellow Door' : ItemData(158017, True),
    'Town Church Stars': ItemData(158018, True),
    'Nothing' : ItemData(158500, True),

    # Event Items
    'Victory': ItemData(158600, True, True)
}

junk_weights = {
    "Nothing": 1
}

event_item_pairs: Dict[str, str] = {
    "Final Elevator Control": "Victory",
}
