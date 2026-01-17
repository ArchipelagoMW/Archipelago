from . import conditions
from .constants import AVRegion
from .types import AccessRule

BOSS_DATA: tuple[str, str, AccessRule] = (
    ("Xedur", AVRegion.XEDUR, conditions.can_damage_boss),
    ("Telal", AVRegion.LOWER_ABSU, conditions.can_damage_boss),
    ("Uruku", AVRegion.URUKU, conditions.can_kill_uruku),
    ("Gir-Tab", AVRegion.GIR_TAB_LOWER_ENTRANCE, conditions.can_kill_gir_tab),
    ("Clone", AVRegion.CLONE, conditions.always_accessible),
    ("Ukhu", AVRegion.UKHU, conditions.can_kill_ukhu),
    ("Sentinel", AVRegion.MAR_URU_ENTRANCE, conditions.can_kill_sentinel),
    ("Xedur Hul", AVRegion.POST_SENTINEL, conditions.always_accessible),
)