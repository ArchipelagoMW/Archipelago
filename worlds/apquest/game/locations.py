from enum import Enum

from ..locations import LOCATION_NAME_TO_ID
from .items import Item


class Location(Enum):
    TOP_LEFT_CHEST = LOCATION_NAME_TO_ID["Top Left Room Chest"]
    TOP_MIDDLE_CHEST = LOCATION_NAME_TO_ID["Top Middle Chest"]
    BOTTOM_LEFT_CHEST = LOCATION_NAME_TO_ID["Bottom Left Chest"]
    BOTTOM_LEFT_EXTRA_CHEST = LOCATION_NAME_TO_ID["Bottom Left Extra Chest"]
    BOTTOM_RIGHT_ROOM_LEFT_CHEST = LOCATION_NAME_TO_ID["Bottom Right Room Left Chest"]
    BOTTOM_RIGHT_ROOM_RIGHT_CHEST = LOCATION_NAME_TO_ID["Bottom Right Room Right Chest"]
    ENEMY_DROP = LOCATION_NAME_TO_ID["Right Room Enemy Drop"]


DEFAULT_CONTENT = {
    Location.TOP_LEFT_CHEST: Item.HEALTH_UPGRADE,
    Location.TOP_MIDDLE_CHEST: Item.HEALTH_UPGRADE,
    Location.BOTTOM_LEFT_CHEST: Item.SWORD,
    Location.BOTTOM_LEFT_EXTRA_CHEST: Item.CONFETTI_CANNON,
    Location.BOTTOM_RIGHT_ROOM_LEFT_CHEST: Item.SHIELD,
    Location.BOTTOM_RIGHT_ROOM_RIGHT_CHEST: Item.HAMMER,
    Location.ENEMY_DROP: Item.KEY,
}
