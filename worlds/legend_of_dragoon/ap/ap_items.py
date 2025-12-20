from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from ..data.equipment import EQUIPMENT
from ..data.items import ITEMS
from ..data.additions import ADDITIONS


class APItemCategory(Enum):
    EQUIPMENT = auto()
    CONSUMABLE = auto()
    ADDITION = auto()
    KEY_ITEM = auto()
    GOLD = auto()


@dataclass(frozen=True)
class APItem:
    name: str                       # AP display name
    key: str                        # unique internal key
    category: APItemCategory        # Category
    game_key: Optional[str] = None  # links to equipment/item key
    value: int = 0                  # shop, price, gold amount, etc.
    progression: bool = False

AP_EQUIPMENT_ITEMS = []

for eq in EQUIPMENT:
    AP_EQUIPMENT_ITEMS.append(APItem(
        name=eq.name,
        key=f"equipment:{eq.key}",
        category=APItemCategory.EQUIPMENT,
        game_key=eq.key,
        value=eq.value,
    ))

AP_CONSUMABLE_ITEMS = []

for item in ITEMS:
    AP_CONSUMABLE_ITEMS.append(APItem(
        name=item.name,
        key=f"item:{item.key}",
        category=APItemCategory.CONSUMABLE,
        game_key=item.key,
        value=item.value,
    ))

AP_ADDITIONS = []
for addition in ADDITIONS:
    AP_ADDITIONS.append(APItem(
        name= addition.name,
        key=f"addition:{addition.key}",
        category=APItemCategory.ADDITION,
        game_key=addition.key,
        value=300 # set this better later
    ))

AP_ITEM_POOL = (AP_EQUIPMENT_ITEMS + AP_CONSUMABLE_ITEMS + AP_ADDITIONS)
