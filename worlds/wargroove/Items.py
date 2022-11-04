import typing

from BaseClasses import Item
from typing import Dict


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    event: bool = False


item_table: Dict[str, ItemData] = {
    # Units
    'Spearman': ItemData(52000, True),
    'Wagon': ItemData(52001, False),
    'Mage': ItemData(52002, True),
    'Archer': ItemData(52003, True),
    'Knight': ItemData(52004, True),
    'Ballista': ItemData(52005, True),
    'Golem': ItemData(52006, False),
    'Harpy': ItemData(52007, True),
    'Witch': ItemData(52008, False),
    'Dragon': ItemData(52009, False),
    'Balloon': ItemData(52010, False),
    'Barge': ItemData(52011, True),
    'Merfolk': ItemData(52012, True),
    'Turtle': ItemData(52013, True),
    'Harpoon Ship': ItemData(52014, True),
    'Warship': ItemData(52015, True),
    'Thief': ItemData(52016, True),
    'Rifleman': ItemData(52017, False),

    # Map Triggers
    'Eastern Bridges': ItemData(52018, True),
    'Southern Walls': ItemData(52019, True),
    'Final Bridges': ItemData(52020, True),
    'Final Walls': ItemData(52021, True),
    'Final Sickle': ItemData(52022, True),

    # Player Buffs
    'Income Boost': ItemData(52023, False),

    'CO Defense Boost': ItemData(52024, False),

    # Event Items
    'Wargroove Victory': ItemData(None, True, True),

}

item_pool: Dict[str, int] = {

    # Player Buffs
    'Income Boost': 8,
    'CO Defense Boost': 7,
}
