from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import CliqueWorld


class CliqueItem(Item):
    game = "Clique"


class CliqueItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["CliqueWorld"], bool] = lambda world: True


item_data_table: Dict[str, CliqueItemData] = {
    "Feeling of Satisfaction": CliqueItemData(
        code=69696969,
        type=ItemClassification.progression,
    ),
    "Button Activation": CliqueItemData(
        code=69696968,
        type=ItemClassification.progression,
        can_create=lambda world: world.options.hard_mode,
    ),
    "A Cool Filler Item (No Satisfaction Guaranteed)": CliqueItemData(
        code=69696967,
        can_create=lambda world: False  # Only created from `get_filler_item_name`.
    ),
    "The Urge to Push": CliqueItemData(
        type=ItemClassification.progression,
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
