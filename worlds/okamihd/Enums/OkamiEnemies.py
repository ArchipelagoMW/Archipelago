from typing import TYPE_CHECKING, NamedTuple, List
from enum import Enum

from rule_builder.rules import Has, Rule
from .BrushTechniques import BrushTechniques
from ..Rules import slowdown_rule

if TYPE_CHECKING:
    from .. import OkamiWorld


class EnemyData(NamedTuple):
    code: int
    name: str
    required_weapon_tier: int
    floral_finisher: BrushTechniques | None = None
    defeat_condition: Rule | None = None


# Reference https://github.com/whataboutclyde/okami-utils/blob/master/data/enemy_id.yaml
class OkamiEnemies(Enum):
    GREEN_IMP = EnemyData(0x03, "Green Imp", 0, BrushTechniques.POWER_SLASH)
    RED_IMP = EnemyData(0x00, "Red Imp", 0, BrushTechniques.POWER_SLASH)
    BLUE_IMP = EnemyData(0x01, "Blue Imp", 0, BrushTechniques.POWER_SLASH)
    YELLOW_IMP = EnemyData(0x02, "Yellow Imp", 0, BrushTechniques.POWER_SLASH)
    BLACK_IMP = EnemyData(0x04, "Black Imp", 0, BrushTechniques.POWER_SLASH)
    DEAD_FISH = EnemyData(0x56, "Dead Fish", 0, BrushTechniques.POWER_SLASH)
    # Not sure if this is the code for waka 1 or 2
    WAKA_1 = EnemyData(0x7e, "Waka (Agata Forest)", 1)
    WAKA_2 = EnemyData(0x7e, "Waka (Taka Pass)", 1)
    BUD_OGRE = EnemyData(0x4d, "Bud Ogre", 1, BrushTechniques.GREENSPROUT_BLOOM,
                         defeat_condition=Has(BrushTechniques.GREENSPROUT_BLOOM))
    SPIDER_QUEEN = EnemyData(0x2b, "Spider Queen", 1, defeat_condition=Has(BrushTechniques.GREENSPROUT_VINE))
    TEI = EnemyData(0x24, "Canine Warrior Tei", 1)
    HAYABUSA = EnemyData(0x21, "Hayabusa", 1)
    UME = EnemyData(0x22, "Ume", 1)
    TAKE = EnemyData(0x23, "Take", 1)
    CUTTERS = EnemyData(0x57, "Mr and Ms.Cutter", 1)
    CROW_TENGU = EnemyData(0x57, "Crow Tengu", 1, defeat_condition=Has(BrushTechniques.POWER_SLASH))
    CHIMERA = EnemyData(0x4e, "Chimera", 1, defeat_condition=Has(BrushTechniques.POWER_SLASH))
    # don't require slash here bc it's required in the cutscene that follows, not to beat the boss itself
    CRIMSON_HELM = EnemyData(0x11, "Crimson Helm", 1, defeat_condition=Has(BrushTechniques.GALESTORM))
    FIRE_EYE = EnemyData(0x52, "Fire Eye", 1)
    OROCHI_1 = EnemyData(0x69, "Orochi (Moon Cave)", 1, defeat_condition=Has(BrushTechniques.WATERSPOUT))
    UBUME = EnemyData(0x58, "Ubume", 1, defeat_condition=Has(BrushTechniques.GALESTORM))
    ICE_LIPS = EnemyData(0x53, "Ice Lips", 1)
    JIRO = EnemyData(0x13, "Jiro", 2)
    SABURO = EnemyData(0x14, "Saburo", 2)
    ICHIRO = EnemyData(0x12, "Ichiro", 2, defeat_condition=Has(BrushTechniques.POWER_SLASH))
    THUNDER_DOOM_MIRROR = EnemyData(0x5d, "Thunder Doom Mirror", 2)
    ICE_DOOM_MIRROR = EnemyData(0x5b, "Ice Doom Mirror", 2)
    WIND_DOOM_MIRROR = EnemyData(0x5c, "Wind Doom Mirror", 2, defeat_condition=slowdown_rule)
    BLIGHT = EnemyData(0x7c, "Blight", 2, defeat_condition=Has(BrushTechniques.POWER_SLASH))
    THUNDER_EAR = EnemyData(0x55, "Thunder Ear", 2)
    EARTH_NOSE = EnemyData(0x54, "Earth Nose", 2, defeat_condition=slowdown_rule)
    BLUE_CYCLOPS = EnemyData(0x29, "Blue Cyclops", 2)
    BANDIT_SPIDER = EnemyData(0x0b, "Bandit Spider", 2, defeat_condition=Has(BrushTechniques.GREENSPROUT_VINE))
    TUBE_FOX = EnemyData(0x0e, "Tube Fox", 3)
    RED_OGRE = EnemyData(0x66, "Red Ogre", 3)
    BLUE_OGRE = EnemyData(0x67, "Blue Ogre", 3)
    POLTERGEIST = EnemyData(0x5e, "Poltergeist", 3)
    HEADLESS_GUARDIAN = EnemyData(0x71, "Headless Guardian", 3)
    BELL_GUARDIAN = EnemyData(0x72, "Bell Guardian", 3)
    HALO_GUARDIAN = EnemyData(0x73, "Halo Guardian", 3)
    EXECUTIONER_GUARDIAN = EnemyData(0x74, "Executioner Guardian", 3)
    NINETAILS_1 = EnemyData(0x61, "Ninetails", 3, defeat_condition=Has(BrushTechniques.THUNDERSTORM))

    @staticmethod
    def list():
        return list(map(lambda o: o.value, OkamiEnemies))
