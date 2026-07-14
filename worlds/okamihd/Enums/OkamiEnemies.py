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
    requires_slash: bool = False
    requires_bomb: bool = False


# Reference https://github.com/whataboutclyde/okami-utils/blob/master/data/enemy_id.yaml
class OkamiEnemies(Enum):

    GREEN_IMP = EnnemyData(0x03, "Green Imp", 0, BrushTechniques.POWER_SLASH)
    RED_IMP = EnnemyData(0x00, "Red Imp", 0, BrushTechniques.POWER_SLASH)
    BLUE_IMP = EnnemyData(0x01, "Blue Imp", 0, BrushTechniques.POWER_SLASH)
    YELLOW_IMP = EnnemyData(0x02, "Yellow Imp", 0, BrushTechniques.POWER_SLASH)
    BLACK_IMP = EnnemyData(0x04, "Black Imp", 0, BrushTechniques.POWER_SLASH)
    DEAD_FISH = EnnemyData(0x56, "Dead Fish", 0, BrushTechniques.POWER_SLASH)
    # Not sure if this is the code for waka 1 or 2
    WAKA_1 = EnnemyData(0x7e, "Waka (Agata Forest)", 1)
    WAKA_2 = EnnemyData(0x7e, "Waka (Taka Pass)", 1)
    BUD_OGRE = EnnemyData(0x4d, "Bud Ogre", 1, BrushTechniques.GREENSPROUT_BLOOM,
                          required_techniques=[BrushTechniques.GREENSPROUT_BLOOM])
    SPIDER_QUEEN = EnnemyData(0x2b, "Spider Queen", 1, required_techniques=[BrushTechniques.GREENSPROUT_VINE])
    TEI = EnnemyData(0x24, "Canine Warrior Tei", 1)
    HAYABUSA = EnnemyData(0x21, "Hayabusa", 1)
    UME = EnnemyData(0x22, "Ume", 1)
    TAKE = EnnemyData(0x23, "Take", 1)
    CUTTERS = EnnemyData(0x57, "Mr and Ms.Cutter", 1)
    CROW_TENGU = EnnemyData(0x57, "Crow Tengu", 1, requires_slash=True)
    CHIMERA = EnnemyData(0x4e, "Chimera", 1, requires_slash=True)
    # don't require slash here bc it's required in the cutscene that follows, not to beat the boss itself
    CRIMSON_HELM = EnnemyData(0x11, "Crimson Helm", 1, required_techniques=[BrushTechniques.GALESTORM])
    FIRE_EYE = EnnemyData(0x52, "Fire Eye", 1)
    OROCHI_1 = EnnemyData(0x69, "Orochi (Moon Cave)", 1, required_techniques=[BrushTechniques.WATERSPOUT])
    UBUME = EnnemyData(0x58, "Ubume", 1, required_techniques=[BrushTechniques.GALESTORM])
    ICE_LIPS = EnnemyData(0x53, "Ice Lips", 1)
    JIRO = EnnemyData(0x13, "Jiro", 2)
    SABURO = EnnemyData(0x14, "Saburo", 2)
    ICHIRO = EnnemyData(0x12, "Ichiro", 2, requires_slash=True)
    THUNDER_DOOM_MIRROR = EnnemyData(0x5d, "Thunder Doom Mirror", 2)
    ICE_DOOM_MIRROR = EnnemyData(0x5b, "Ice Doom Mirror", 2)
    WIND_DOOM_MIRROR = EnnemyData(0x5c, "Wind Doom Mirror", 2, required_techniques=[BrushTechniques.VEIL_OF_MIST])
    BLIGHT = EnnemyData(0x7c, "Blight", 2, requires_slash=True)
    THUNDER_EAR = EnnemyData(0x55, "Thunder Ear", 2)
    EARTH_NOSE = EnnemyData(0x54, "Earth Nose", 2, required_techniques=[BrushTechniques.VEIL_OF_MIST])
    BLUE_CYCLOPS = EnnemyData(0x29, "Blue Cyclops", 2)
    BANDIT_SPIDER = EnnemyData(0x0b, "Bandit Spider", 2, required_techniques=[BrushTechniques.GREENSPROUT_VINE])
    TUBE_FOX = EnnemyData(0x0e, "Tube Fox", 3)
    RED_OGRE = EnnemyData(0x66, "Red Ogre", 3)
    BLUE_OGRE = EnnemyData(0x67, "Blue Ogre", 3)
    POLTERGEIST = EnnemyData(0x5e, "Poltergeist", 3)
    HEADLESS_GUARDIAN = EnnemyData(0x71, "Headless Guardian", 3)
    BELL_GUARDIAN = EnnemyData(0x72, "Bell Guardian",3)
    HALO_GUARDIAN = EnnemyData(0x73, "Halo Guardian", 3)
    EXECUTIONER_GUARDIAN = EnnemyData(0x74, "Executioner Guardian", 3)
    NINETAILS_1 = EnnemyData(0x61, "Ninetails", 3, required_techniques=[BrushTechniques.THUNDERSTORM])

    @staticmethod
    def list():
        return list(map(lambda o: o.value, OkamiEnemies))
