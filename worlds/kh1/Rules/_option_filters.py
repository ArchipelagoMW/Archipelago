from rule_builder.options import OptionFilter

from ..Data import LOGIC_BEGINNER, LOGIC_NORMAL, LOGIC_PROUD, LOGIC_MINIMAL
from ..Options import (
    EndoftheWorldUnlock,
    FinalRestDoorKey,
    HalloweenTownKeyItemBundle,
    HundredAcreWood,
    KeybladesUnlockChests,
    LogicDifficulty,
    StackingWorldItems,
)

ABOVE_BEGINNER = OptionFilter(LogicDifficulty, LOGIC_BEGINNER, "gt")
ABOVE_NORMAL = OptionFilter(LogicDifficulty, LOGIC_NORMAL, "gt")
ABOVE_PROUD = OptionFilter(LogicDifficulty, LOGIC_PROUD, "gt")
AT_LEAST_MINIMAL = OptionFilter(LogicDifficulty, LOGIC_MINIMAL, "ge")
BELOW_MINIMAL = OptionFilter(LogicDifficulty, LOGIC_MINIMAL, "lt")
EXACTLY_BEGINNER = OptionFilter(LogicDifficulty, LOGIC_BEGINNER, "eq")
NOT_EXACTLY_BEGINNER = OptionFilter(LogicDifficulty, LOGIC_BEGINNER, "ne")

HUNDRED_ACRE_WOOD_ON = OptionFilter(HundredAcreWood, True, "eq")
HUNDRED_ACRE_WOOD_OFF = OptionFilter(HundredAcreWood, False, "eq")
KEYBLADES_UNLOCK_CHESTS_ON = OptionFilter(KeybladesUnlockChests, True, "eq")
KEYBLADES_UNLOCK_CHESTS_OFF = OptionFilter(KeybladesUnlockChests, False, "eq")
STACKING_WORLD_ITEMS_ON = OptionFilter(StackingWorldItems, True, "eq")
HALLOWEEN_TOWN_KEY_ITEM_BUNDLE_ON = OptionFilter(HalloweenTownKeyItemBundle, True, "eq")

FINAL_REST_DOOR_LUCKY_EMBLEMS = OptionFilter(FinalRestDoorKey, "lucky_emblems", "eq")
FINAL_REST_DOOR_NOT_LUCKY_EMBLEMS = OptionFilter(FinalRestDoorKey, "lucky_emblems", "ne")
EOTW_UNLOCK_LUCKY_EMBLEMS = OptionFilter(EndoftheWorldUnlock, "lucky_emblems", "eq")
