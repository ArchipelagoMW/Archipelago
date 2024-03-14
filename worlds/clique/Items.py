from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld


class CliqueItem(Item):
    game = "Clique"


class CliqueItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


item_data_table: Dict[str, CliqueItemData] = {
    "Feeling of Satisfaction": CliqueItemData(
        code=69696969,
        type=ItemClassification.progression,
    ),
    "Button Activation": CliqueItemData(
        code=69696968,
        type=ItemClassification.progression,
        can_create=lambda multiworld, player: bool(getattr(multiworld, "hard_mode")[player]),
    ),
    "A Cool Filler Item (No Satisfaction Guaranteed)": CliqueItemData(
        code=69696967,
        can_create=lambda multiworld, player: False  # Only created from `get_filler_item_name`.
    ),
    "The Urge to Push": CliqueItemData(
        type=ItemClassification.progression,
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
