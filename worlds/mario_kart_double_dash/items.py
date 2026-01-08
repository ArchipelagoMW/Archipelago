from typing import Any, NamedTuple, TYPE_CHECKING
from enum import Enum

from BaseClasses import Item, ItemClassification
from . import game_data

if TYPE_CHECKING:
    from . import MkddWorld

PROG = ItemClassification.progression
FILL = ItemClassification.filler
USEF = ItemClassification.useful
SKIP = ItemClassification.progression_skip_balancing
TRAP = ItemClassification.trap

class ItemType(Enum):
    OTHER = 0
    CHARACTER = 1
    KART = 2
    CUP = 3
    TT_COURSE = 4
    ITEM_UNLOCK = 5
    KART_UPGRADE = 6

class MkddItem(Item):
    game = "Mario Kart Double Dash"


class MkddItemData(NamedTuple):
    name: str
    classification: int
    item_type: ItemType = ItemType.OTHER
    address: int = 0
    count: int = 1
    meta: Any = None


PROGRESSIVE_CLASS = "Progressive CC"
PROGRESSIVE_CUP_SKIP = "Progressive GP Race Skip"
PROGRESSIVE_TIME_TRIAL_ITEM = "Progressive Time Trial Item"
PROGRESSIVE_ENGINE = "Progressive Speed Upgrade"
RANDOM_ITEM = "Nothing"
TROPHY = "Trophy"
VICTORY = "Victory"
SKIP_DIFFICULTY = "Skip Difficulty Calculation"

def get_item_name_tt_course(course: str) -> str:
    return f"{course} Time Trial"

def get_item_name_character_item(character: str, item: str) -> str:
    if character != None:
        return f"{item} for {character}"
    else:
        return f"{item} for Everybody"

def get_item_name_kart_upgrade(upgrade: str, kart: str) -> str:
    return f"{upgrade} for {kart}"


data_table: list[MkddItemData] = [
    MkddItemData("", 0, count = 0), # Id 0 is reserved
    MkddItemData(PROGRESSIVE_CLASS, PROG, count = 3),
    MkddItemData(PROGRESSIVE_CUP_SKIP, USEF, count = 2),
    MkddItemData(PROGRESSIVE_TIME_TRIAL_ITEM, PROG, count = 3),
    MkddItemData(PROGRESSIVE_ENGINE, PROG, count = 0), # Count depends on options.
    MkddItemData(RANDOM_ITEM, FILL),
    MkddItemData(TROPHY, PROG, count = 0),
    MkddItemData(VICTORY, PROG, count = 0),
]
data_table.extend([MkddItemData(char.name, PROG, ItemType.CHARACTER, id) for id, char in enumerate(game_data.CHARACTERS)])
data_table.extend([MkddItemData(name, PROG, ItemType.CUP, id, 1 if id != game_data.CUP_ALL_CUP_TOUR else 0) for id, name in enumerate(game_data.CUPS)])
data_table.extend([MkddItemData(get_item_name_tt_course(course.name), PROG, ItemType.TT_COURSE, id) for id, course in enumerate(game_data.RACE_COURSES)])

for id, kart in enumerate(game_data.KARTS):
    data_table.append(MkddItemData(kart.name, PROG, ItemType.KART, id))
    data_table.extend([
        MkddItemData(get_item_name_kart_upgrade(upgrade.name, kart.name), PROG, ItemType.KART_UPGRADE, id, 0, upgrade)
        for upgrade in game_data.KART_UPGRADES
    ])

for item in game_data.ITEMS:
    classification = PROG if item.usefulness > 0 else FILL
    if item != game_data.ITEM_NONE:
        data_table.append(MkddItemData(
            get_item_name_character_item(None, item.name), classification,
            ItemType.ITEM_UNLOCK, count = 0, meta = {"character":None, "item":item}
            ))
        for character in game_data.CHARACTERS:
            data_table.append(MkddItemData(
                get_item_name_character_item(character.name, item.name), classification,
                ItemType.ITEM_UNLOCK, count = 0, meta = {"character":character, "item":item}
                ))

# Used by Universal Tracker glitched logic.
data_table.append(MkddItemData(SKIP_DIFFICULTY, PROG, count = 0))

name_to_id: dict[str, int] = {item.name:id for (id, item) in enumerate(data_table) if id > 0}
