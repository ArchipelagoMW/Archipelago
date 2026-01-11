from .classification import *
from .. import SeasonItemData

table: dict[str, SeasonItemData] = {
    "Spring": SeasonItemData(0x81, 0x181, 0, always_progression),
    "Summer": SeasonItemData(0x82, 0x182, 1, always_progression),
    "Autumn": SeasonItemData(0x83, 0x183, 2, always_progression),
    "Winter": SeasonItemData(0x84, 0x184, 3, always_progression),
}
