from collections import defaultdict
from enum import Enum
from typing import NamedTuple

from ..items import ITEM_NAME_TO_ID
from .graphics import Graphic


class Item(Enum):
    KEY = ITEM_NAME_TO_ID["Key"]
    SWORD = ITEM_NAME_TO_ID["Sword"]
    SHIELD = ITEM_NAME_TO_ID["Shield"]
    HEALTH_UPGRADE = ITEM_NAME_TO_ID["Health Upgrade"]
    CONFETTI_CANNON = ITEM_NAME_TO_ID["Confetti Cannon"]
    REMOTE_ITEM = -1


class RemotelyReceivedItem(NamedTuple):
    remote_item_id: int
    remote_location_id: int
    remote_location_player: int


ITEM_TO_GRAPHIC = defaultdict(
    lambda: Graphic.UNKNOWN,
    {
        Item.KEY: Graphic.KEY,
        Item.SWORD: Graphic.SWORD,
        Item.SHIELD: Graphic.SHIELD,
        Item.HEALTH_UPGRADE: Graphic.HEART,
        Item.CONFETTI_CANNON: Graphic.CONFETTI_CANNON,
        Item.REMOTE_ITEM: Graphic.REMOTE_ITEM,
    },
)
