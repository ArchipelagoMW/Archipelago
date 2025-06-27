from typing import TYPE_CHECKING, NamedTuple, List
from enum import Enum

from .BrushTechniques import BrushTechniques

if TYPE_CHECKING:
    from .. import OkamiWorld

class EnnemyData(NamedTuple):
    code: int
    name: str
    required_weapon_tier: int
    floral_finisher: BrushTechniques | None = None
    required_techniques: List[BrushTechniques] = []

class OkamiEnnemies(Enum):
    GREEN_IMP = EnnemyData(0x03, "Green Imp", 0, BrushTechniques.POWER_SLASH)
    RED_IMP = EnnemyData(0x00, "Red Imp", 0, BrushTechniques.POWER_SLASH)
    YELLOW_IMP = EnnemyData(0x02, "Yellow Imp", 0, BrushTechniques.POWER_SLASH)
    #Not sure if this is the code for waka 1 or 2
    WAKA_1 = EnnemyData(0x7e, "Waka (Agata Forest)",1)
    BUD_OGRE = EnnemyData(0x4d, "Bud Ogre",1,BrushTechniques.GREENSPROUT_BLOOM,required_techniques=[BrushTechniques.GREENSPROUT_BLOOM])

    @staticmethod
    def list():
        return list(map(lambda b: b.value, BrushTechniques))
