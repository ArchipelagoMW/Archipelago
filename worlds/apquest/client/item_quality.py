from enum import Enum

from BaseClasses import ItemClassification
from NetUtils import NetworkItem


class ItemQuality(Enum):
    FILLER = 0
    TRAP = 1
    USEFUL = 2
    PROGRESSION = 3
    PROGUSEFUL = 4


def get_quality_for_network_item(network_item: NetworkItem) -> ItemQuality:
    flags = ItemClassification(network_item.flags)
    if ItemClassification.progression in flags:
        if ItemClassification.useful in flags:
            return ItemQuality.PROGUSEFUL
        return ItemQuality.PROGRESSION
    if ItemClassification.useful in flags:
        return ItemQuality.USEFUL
    if ItemClassification.trap in flags:
        return ItemQuality.TRAP
    return ItemQuality.FILLER
