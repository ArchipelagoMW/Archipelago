from collections import defaultdict
from enum import Enum

from graphics import Graphic


class Item(Enum):
    KEY = (1,)
    SWORD = (2,)
    SHIELD = (3,)
    HEALTH_UPGRADE = (4,)


ITEM_TO_GRAPHIC = defaultdict(
    lambda: Graphic.UNKNOWN,
    {
        Item.KEY: Graphic.KEY,
        Item.SWORD: Graphic.SWORD,
        Item.SHIELD: Graphic.SHIELD,
        Item.HEALTH_UPGRADE: Graphic.HEALTH_UPGRADE,
    },
)
