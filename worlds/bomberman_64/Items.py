from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import Bomb64World


class Bomb64Item(Item):
    game = "Bomberman 64"


class Bomb64ItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    num_exist: int = 1
    can_create: Callable[["Bomb64World"], bool] = lambda world: True


item_data_table: Dict[str, Bomb64ItemData] = {
    "Bombup": Bomb64ItemData(
        code=0x1CAEE0F,
        type=ItemClassification.progression,
        num_exist = 6
    ),
    "Fireup": Bomb64ItemData(
        code=0x1CAEE13,
        type=ItemClassification.progression,
        num_exist = 2
    ),
    "Bomb Kick": Bomb64ItemData(
        code=0x1CAEE09,
        type=ItemClassification.progression,
    ),
    "Power Glove": Bomb64ItemData(
        code=0x1CAEE0A,
        type=ItemClassification.progression,
    ),
    "Remote Bombs": Bomb64ItemData(
        code=0x1CAEE0B,
        type=ItemClassification.progression,
    ),
    "Power Bombs": Bomb64ItemData(
        code=0x1CAEE0C,
        type=ItemClassification.progression,
    ),

    "Heart": Bomb64ItemData(
        code=0x1CAEE07,
        type=ItemClassification.useful,
    ),
    "Gold Card": Bomb64ItemData(
        code=0x1CAEE0D,
        type=ItemClassification.progression,
        num_exist = 0
    ),

    "Green Key": Bomb64ItemData(
        code=0x1CAEE01,
        type=ItemClassification.progression,
        num_exist = 1
    ),
    "Blue Key": Bomb64ItemData(
        code=0x1CAEE02,
        type=ItemClassification.progression,
        num_exist = 1
    ),
    "Red Key": Bomb64ItemData(
        code=0x1CAEE03,
        type=ItemClassification.progression,
        num_exist = 1
    ),
    "White Key": Bomb64ItemData(
        code=0x1CAEE04,
        type=ItemClassification.progression,
        num_exist = 1
    ),
    "Black Key": Bomb64ItemData(
        code=0x1CAEE05,
        type=ItemClassification.progression,
        num_exist = 3
    ),
    "Rainbow Key": Bomb64ItemData(
        code=0x1CAEE0E,
        type=ItemClassification.progression,
        num_exist = 0
    ),

    "Kill Count Reduction": Bomb64ItemData(
        code=0x1CAEE08,
        type=ItemClassification.useful,
        num_exist = 0
    ), 
    "5 Gems": Bomb64ItemData(
        code=0x1CAEE10,
        type=ItemClassification.filler,
        num_exist = 0
    ),
    "Extra Life": Bomb64ItemData(
        code=0x1CAEE11,
        type=ItemClassification.filler,
        num_exist = 0
    ),
    "Boss Medal": Bomb64ItemData(
        code=0x1CAEE06,
        type=ItemClassification.progression,
        num_exist = 0
    ),

    # Traps
    "Fast Virus": Bomb64ItemData(
        code=0x1CAEE18,
        type=ItemClassification.trap,
        num_exist = 0
    ),
    "Sticky Virus": Bomb64ItemData(
        code=0x1CAEE19,
        type=ItemClassification.trap,
        num_exist = 0
    ),
    "Slow Virus": Bomb64ItemData(
        code=0x1CAEE1A,
        type=ItemClassification.trap,
        num_exist = 0
    ),
    
    "Bombless Virus": Bomb64ItemData(
        code=0x1CAEE1B,
        type=ItemClassification.trap,
        num_exist = 0
    ),
    "Restless Virus": Bomb64ItemData(
        code=0x1CAEE1C,
        type=ItemClassification.trap,
        num_exist = 0
    ),
    "Death Virus": Bomb64ItemData(
        code=0x1CAEE1D,
        type=ItemClassification.trap,
        num_exist = 0
    ),

    "Omnicube": Bomb64ItemData(
        code=0x1CAEE12,
        type=ItemClassification.progression,
        num_exist=0
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
