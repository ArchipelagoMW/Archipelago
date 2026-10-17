from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_TRAP_OFFSET


class Traps(ItemTypeEnum):
    STINK_TRAP = ("Stink Trap", ITEMS_TRAP_OFFSET + 0, ItemClassification.trap)
    POLTERGEIST_TRAP = ("Poltergeist Trap", ITEMS_TRAP_OFFSET + 1, ItemClassification.trap)
    CREDIT_CARD_FAILURE_TRAP = ("Credit Card Failure Trap", ITEMS_TRAP_OFFSET + 2, ItemClassification.trap)
    DECREASE_CARD_LUCK = ("Decrease Card Luck", ITEMS_TRAP_OFFSET + 3, ItemClassification.trap)
    MARKET_CHANGE_TRAP = ("Market Change Trap", ITEMS_TRAP_OFFSET + 4, ItemClassification.trap)
    CURRENCY_TRAP = ("Currency Trap", ITEMS_TRAP_OFFSET + 5, ItemClassification.trap)

def get_traps_default_dict():
    return {
        trap.value: 50
        for trap in Traps
    }