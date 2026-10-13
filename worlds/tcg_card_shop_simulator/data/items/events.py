from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_EVENTS_OFFSET


class Events(ItemTypeEnum):
    STANDARD = ("Standard Format", ITEMS_EVENTS_OFFSET + 0, ItemClassification.progression)
    PAUPER = ("Pauper Format", ITEMS_EVENTS_OFFSET + 1, ItemClassification.progression)
    FIRE_CUP = ("Fire Cup Format", ITEMS_EVENTS_OFFSET + 2, ItemClassification.progression)
    EARTH_CUP = ("Earth Cup Format", ITEMS_EVENTS_OFFSET + 3, ItemClassification.progression)
    WATER_CUP = ("Water Cup Format", ITEMS_EVENTS_OFFSET + 4, ItemClassification.progression)
    WIND_CUP = ("Wind Cup Format", ITEMS_EVENTS_OFFSET + 5, ItemClassification.progression)
    FIRST_EDITION_VINTAGE = ("First Edition Vintage Format", ITEMS_EVENTS_OFFSET + 6, ItemClassification.progression)
    SILVER_BORDER = ("Silver Border Format", ITEMS_EVENTS_OFFSET + 7, ItemClassification.progression)
    GOLD_BORDER = ("Gold Border Format", ITEMS_EVENTS_OFFSET + 8, ItemClassification.progression)
    EX_BORDER = ("EX Border Format", ITEMS_EVENTS_OFFSET + 9, ItemClassification.progression)
    FULL_ART_BORDER = ("Full Art Border Format", ITEMS_EVENTS_OFFSET + 10, ItemClassification.progression)
    FOIL = ("Foil Format", ITEMS_EVENTS_OFFSET + 11, ItemClassification.progression)

