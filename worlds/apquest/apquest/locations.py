from enum import Enum

from items import Item


class Location(Enum):
    TOP_LEFT_CHEST = 1
    TOP_MIDDLE_CHEST = 2
    BOTTOM_LEFT_CHEST = 3
    BOTTOM_RIGHT_CHEST = 4
    ENEMY_DROP = 10


DEFAULT_CONTENT = {
    Location.TOP_LEFT_CHEST: Item.HEALTH_UPGRADE,
    Location.TOP_MIDDLE_CHEST: Item.HEALTH_UPGRADE,
    Location.BOTTOM_LEFT_CHEST: Item.SWORD,
    Location.BOTTOM_RIGHT_CHEST: Item.SHIELD,
    Location.ENEMY_DROP: Item.KEY,
}
