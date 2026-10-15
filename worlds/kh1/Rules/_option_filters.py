from rule_builder.options import OptionFilter

from ..Options import EndoftheWorldUnlock, EvidenceBundle, FinalRestDoorKey
from ..Options import HalloweenTownKeyItemBundle, KeybladesUnlockChests
from ..Options import LogicDifficulty, RaftFinish, SlidesBundle, StackingWorldItems

LOGIC_BEGINNER = LogicDifficulty.option_beginner
LOGIC_NORMAL = LogicDifficulty.option_normal
LOGIC_PROUD = LogicDifficulty.option_proud

ABOVE_BEGINNER = OptionFilter(LogicDifficulty, LOGIC_BEGINNER, "gt")
ABOVE_NORMAL = OptionFilter(LogicDifficulty, LOGIC_NORMAL, "gt")
ABOVE_PROUD = OptionFilter(LogicDifficulty, LOGIC_PROUD, "gt")

KEYBLADES_UNLOCK_CHESTS_OFF = OptionFilter(KeybladesUnlockChests, False, "eq")
STACKING_WORLD_ITEMS_ON = OptionFilter(StackingWorldItems, True, "eq")
HALLOWEEN_TOWN_KEY_ITEM_BUNDLE_ON = OptionFilter(HalloweenTownKeyItemBundle, True, "eq")
SLIDES_BUNDLE_ON = OptionFilter(SlidesBundle, True, "eq")
SLIDES_BUNDLE_OFF = OptionFilter(SlidesBundle, False, "eq")
EVIDENCE_BUNDLE_ON = OptionFilter(EvidenceBundle, True, "eq")
EVIDENCE_BUNDLE_OFF = OptionFilter(EvidenceBundle, False, "eq")
RAFT_FINISH_ON = OptionFilter(RaftFinish, True, "eq")

FINAL_REST_DOOR_LUCKY_EMBLEMS = OptionFilter(FinalRestDoorKey, "lucky_emblems", "eq")
FINAL_REST_DOOR_NOT_LUCKY_EMBLEMS = OptionFilter(FinalRestDoorKey, "lucky_emblems", "ne")
EOTW_UNLOCK_LUCKY_EMBLEMS = OptionFilter(EndoftheWorldUnlock, "lucky_emblems", "eq")
