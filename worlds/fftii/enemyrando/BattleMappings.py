from worlds.fftii.enemyrando.EventCodes import EventCode
from worlds.fftii.enemyrando.Job import Job
from worlds.fftii.enemyrando.RandomizedUnitFactory import RandomizedUnitFactory
from worlds.fftii.enemyrando.RandomizedUnits import RandomizedUnit
from worlds.fftii.enemyrando.SourceUnit import SourceUnit
from worlds.fftii.enemyrando.SpriteSet import SpriteSet
from worlds.fftii.enemyrando.Unit import UnitGender


class BattleMapping:
    name: str
    battle_id: EventCode
    battle_level: int
    source_units = []
    unit_mapping: dict[SourceUnit, RandomizedUnitFactory]

    def __init__(self, battle_id: int, source_units):
        self.battle_id = EventCode(battle_id)
        self.source_units = source_units

    def __copy__(self):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        copied_object = BattleMapping(self.battle_id, self.source_units.copy())
        copied_object.name = self.name
        return copied_object


DolbodarSwampEast1 = BattleMapping(1, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DolbodarSwampEast2 = BattleMapping(2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DolbodarSwampEast3 = BattleMapping(3, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DolbodarSwampEast4 = BattleMapping(4, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DolbodarSwampWest1 = BattleMapping(5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DolbodarSwampWest2 = BattleMapping(6, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.URIBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DolbodarSwampWest3 = BattleMapping(7, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DolbodarSwampWest4 = BattleMapping(8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth1 = BattleMapping(13, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth2 = BattleMapping(14, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth3 = BattleMapping(15, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth4 = BattleMapping(16, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsWest1 = BattleMapping(17, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
FovohamPlainsWest2 = BattleMapping(18, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsWest3 = BattleMapping(19, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
FovohamPlainsWest4 = BattleMapping(20, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsEast1 = BattleMapping(21, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsEast2 = BattleMapping(22, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsEast3 = BattleMapping(23, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsEast4 = BattleMapping(24, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsEast1 = BattleMapping(25, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
SweegyWoodsEast2 = BattleMapping(26, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsEast3 = BattleMapping(27, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsEast4 = BattleMapping(28, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsWest1 = BattleMapping(29, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsWest2 = BattleMapping(30, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsWest3 = BattleMapping(31, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
SweegyWoodsWest4 = BattleMapping(32, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BerveniaVolcanoNorth1 = BattleMapping(37, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BerveniaVolcanoNorth2 = BattleMapping(38, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BerveniaVolcanoNorth3 = BattleMapping(39, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BerveniaVolcanoNorth4 = BattleMapping(40, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BerveniaVolcanoSouth1 = BattleMapping(41, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BerveniaVolcanoSouth2 = BattleMapping(42, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
BerveniaVolcanoSouth3 = BattleMapping(43, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BerveniaVolcanoSouth4 = BattleMapping(44, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertNorth1 = BattleMapping(49, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertNorth2 = BattleMapping(50, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
ZeklausDesertNorth3 = BattleMapping(51, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertNorth4 = BattleMapping(52, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZeklausDesertSouth1 = BattleMapping(53, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertSouth2 = BattleMapping(54, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertSouth3 = BattleMapping(55, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
ZeklausDesertSouth4 = BattleMapping(56, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertEast1 = BattleMapping(57, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertEast2 = BattleMapping(58, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZeklausDesertEast3 = BattleMapping(59, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertEast4 = BattleMapping(60, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauSouth1 = BattleMapping(61, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauSouth2 = BattleMapping(62, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
LenaliaPlateauSouth3 = BattleMapping(63, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
LenaliaPlateauSouth4 = BattleMapping(64, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
LenaliaPlateauNorth1 = BattleMapping(65, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauNorth2 = BattleMapping(66, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
LenaliaPlateauNorth3 = BattleMapping(67, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauNorth4 = BattleMapping(68, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
ZigolisSwampEast1 = BattleMapping(73, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZigolisSwampEast2 = BattleMapping(74, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZigolisSwampEast3 = BattleMapping(75, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
ZigolisSwampEast4 = BattleMapping(76, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZigolisSwampWest1 = BattleMapping(77, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZigolisSwampWest2 = BattleMapping(78, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
ZigolisSwampWest3 = BattleMapping(79, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZigolisSwampWest4 = BattleMapping(80, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
ZirekileFallsEast5 = BattleMapping(82, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BariusHillSouth5 = BattleMapping(83, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauSouth5 = BattleMapping(84, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CALCULATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CALCULATOR, UnitGender.FEMALE),
])
#Used sprite sheets: 2
#===
YuguoWoodsWest1 = BattleMapping(85, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
YuguoWoodsWest2 = BattleMapping(86, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
YuguoWoodsWest3 = BattleMapping(87, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
YuguoWoodsWest4 = BattleMapping(88, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
YuguoWoodsEast1 = BattleMapping(89, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
YuguoWoodsEast2 = BattleMapping(90, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
YuguoWoodsEast3 = BattleMapping(91, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
YuguoWoodsEast4 = BattleMapping(92, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
DolbodarSwampWest5 = BattleMapping(93, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PORKY, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillSouth5 = BattleMapping(94, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
])
#Used sprite sheets: 1
#===
BerveniaVolcanoNorth5 = BattleMapping(95, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleySouth5 = BattleMapping(96, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TIAMAT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
AraguayWoodsWest1 = BattleMapping(97, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
AraguayWoodsWest2 = BattleMapping(98, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
AraguayWoodsWest3 = BattleMapping(99, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
AraguayWoodsWest4 = BattleMapping(100, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
AraguayWoodsEast1 = BattleMapping(101, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
AraguayWoodsEast2 = BattleMapping(102, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
AraguayWoodsEast3 = BattleMapping(103, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
AraguayWoodsEast4 = BattleMapping(104, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverEast5 = BattleMapping(105, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakNorth5 = BattleMapping(106, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CHEMIST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MEDIATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MEDIATOR, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
AraguayWoodsWest5 = BattleMapping(107, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
])
#Used sprite sheets: 2
#===
YuguoWoodsEast5 = BattleMapping(108, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
])
#Used sprite sheets: 1
#===
GrogHillWest1 = BattleMapping(109, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
GrogHillWest2 = BattleMapping(110, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GrogHillWest3 = BattleMapping(111, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillWest4 = BattleMapping(112, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillSouth1 = BattleMapping(113, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillSouth2 = BattleMapping(114, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.GEOMANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
GrogHillSouth3 = BattleMapping(115, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillSouth4 = BattleMapping(116, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
GrogHillEast1 = BattleMapping(117, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
GrogHillEast2 = BattleMapping(118, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SAMURAI, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 6
#===
GrogHillEast3 = BattleMapping(119, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
GrogHillEast4 = BattleMapping(120, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BedDesertSouth1 = BattleMapping(121, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BedDesertSouth2 = BattleMapping(122, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
BedDesertSouth3 = BattleMapping(123, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BedDesertSouth4 = BattleMapping(124, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
BedDesertNorth1 = BattleMapping(125, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BedDesertNorth2 = BattleMapping(126, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
BedDesertNorth3 = BattleMapping(127, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BedDesertNorth4 = BattleMapping(128, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BedDesertNorth5 = BattleMapping(129, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.GEOMANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
FovohamPlainsWest5 = BattleMapping(130, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
DoguolaPassWest5 = BattleMapping(131, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
SweegyWoodsEast5 = BattleMapping(132, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 7
#===
ZirekileFallsWest1 = BattleMapping(133, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsWest2 = BattleMapping(134, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZirekileFallsWest3 = BattleMapping(135, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsWest4 = BattleMapping(136, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsEast1 = BattleMapping(137, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsEast2 = BattleMapping(138, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsEast3 = BattleMapping(139, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZirekileFallsEast4 = BattleMapping(140, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
ZirekileFallsSouth1 = BattleMapping(141, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsSouth2 = BattleMapping(142, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
ZirekileFallsSouth3 = BattleMapping(143, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsSouth4 = BattleMapping(144, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BariusHillNorth1 = BattleMapping(145, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BariusHillNorth2 = BattleMapping(146, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BariusHillNorth3 = BattleMapping(147, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusHillNorth4 = BattleMapping(148, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusHillSouth1 = BattleMapping(149, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
BariusHillSouth2 = BattleMapping(150, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
BariusHillSouth3 = BattleMapping(151, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusHillSouth4 = BattleMapping(152, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
PoeskasLakeNorth5 = BattleMapping(153, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CHEMIST, UnitGender.FEMALE),
])
#Used sprite sheets: 7
#===
ZigolisSwampWest5 = BattleMapping(154, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SQUIRE, UnitGender.FEMALE),
])
#Used sprite sheets: 7
#===
MandaliaPlainsSouth5 = BattleMapping(155, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
ZeklausDesertSouth5 = BattleMapping(156, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 2
#===
MandaliaPlainsNorth1 = BattleMapping(157, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
MandaliaPlainsNorth2 = BattleMapping(158, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsNorth3 = BattleMapping(159, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsNorth4 = BattleMapping(160, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsSouth1 = BattleMapping(161, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
MandaliaPlainsSouth2 = BattleMapping(162, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
MandaliaPlainsSouth3 = BattleMapping(163, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsSouth4 = BattleMapping(164, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsWest1 = BattleMapping(165, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
MandaliaPlainsWest2 = BattleMapping(166, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsWest3 = BattleMapping(167, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsWest4 = BattleMapping(168, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DoguolaPassEast1 = BattleMapping(169, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassEast2 = BattleMapping(170, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassEast3 = BattleMapping(171, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
DoguolaPassEast4 = BattleMapping(172, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassWest1 = BattleMapping(173, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassWest2 = BattleMapping(174, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassWest3 = BattleMapping(175, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassWest4 = BattleMapping(176, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BariusValleyWest1 = BattleMapping(181, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyWest2 = BattleMapping(182, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyWest3 = BattleMapping(183, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BariusValleyWest4 = BattleMapping(184, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BariusValleyEast1 = BattleMapping(185, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyEast2 = BattleMapping(186, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyEast3 = BattleMapping(187, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyEast4 = BattleMapping(188, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleySouth1 = BattleMapping(189, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BariusValleySouth2 = BattleMapping(190, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleySouth3 = BattleMapping(191, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BariusValleySouth4 = BattleMapping(192, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverWest1 = BattleMapping(193, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverWest2 = BattleMapping(194, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
FinathRiverWest3 = BattleMapping(195, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverWest4 = BattleMapping(196, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverEast1 = BattleMapping(197, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverEast2 = BattleMapping(198, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverEast3 = BattleMapping(199, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
FinathRiverEast4 = BattleMapping(200, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GREAT_MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Horror1 = BattleMapping(201, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Horror2 = BattleMapping(202, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Horror3 = BattleMapping(203, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SAMURAI, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
Horror4 = BattleMapping(204, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 8
#===
PoeskasLakeNorth1 = BattleMapping(205, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
PoeskasLakeNorth2 = BattleMapping(206, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
PoeskasLakeNorth3 = BattleMapping(207, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
PoeskasLakeNorth4 = BattleMapping(208, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
PoeskasLakeSouth1 = BattleMapping(209, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
PoeskasLakeSouth2 = BattleMapping(210, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CHEMIST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
PoeskasLakeSouth3 = BattleMapping(211, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
PoeskasLakeSouth4 = BattleMapping(212, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Voyage1 = BattleMapping(213, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
])
#Used sprite sheets: 2
#===
Voyage2 = BattleMapping(214, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Voyage3 = BattleMapping(215, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GREAT_MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Voyage4 = BattleMapping(216, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CALCULATOR, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CALCULATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
GerminasPeakNorth1 = BattleMapping(217, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakNorth2 = BattleMapping(218, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakNorth3 = BattleMapping(219, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakNorth4 = BattleMapping(220, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakSouth1 = BattleMapping(221, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakSouth2 = BattleMapping(222, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakSouth3 = BattleMapping(223, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakSouth4 = BattleMapping(224, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Bridge1 = BattleMapping(225, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
Bridge2 = BattleMapping(226, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Bridge3 = BattleMapping(227, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Bridge4 = BattleMapping(228, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
])
#Used sprite sheets: 9
#===
Tiger1 = BattleMapping(229, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
Tiger2 = BattleMapping(230, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
Tiger3 = BattleMapping(231, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Tiger4 = BattleMapping(232, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SAMURAI, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 10
#===
Mlapan1 = BattleMapping(233, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Mlapan2 = BattleMapping(234, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Mlapan3 = BattleMapping(235, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 7
#===
Mlapan4 = BattleMapping(236, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MEDIATOR, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SQUIRE, UnitGender.FEMALE),
])
#Used sprite sheets: 12
#===
Valkyries1 = BattleMapping(237, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GREAT_MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Valkyries2 = BattleMapping(238, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Valkyries3 = BattleMapping(239, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Valkyries4 = BattleMapping(240, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 10
#===
Delta1 = BattleMapping(241, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Delta2 = BattleMapping(242, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Delta3 = BattleMapping(243, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Delta4 = BattleMapping(244, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.GEOMANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MEDIATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 12
#===
Terminate1 = BattleMapping(245, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Terminate2 = BattleMapping(246, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Terminate3 = BattleMapping(247, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 6
#===
Terminate4 = BattleMapping(248, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Nogias1 = BattleMapping(249, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Nogias2 = BattleMapping(250, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Nogias3 = BattleMapping(251, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
Nogias4 = BattleMapping(252, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 12
#===
SweegyWoods = BattleMapping(384, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DorterTradeCity1 = BattleMapping(385, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF1), Job.WHITE_KNIGHT_C1, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
SandRatCellar = BattleMapping(386, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
GarilandFight = BattleMapping(388, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SQUIRE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
MandaliaPlains = BattleMapping(389, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
Miluda1 = BattleMapping(395, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
Miluda2 = BattleMapping(399, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Wiegraf1 = BattleMapping(400, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF1), Job.WHITE_KNIGHT_C1, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
FortZeakden = BattleMapping(401, [
    SourceUnit(SpriteSet(SpriteSet.ZALBAG), Job.ARC_KNIGHT_ZALBAG, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.TETA), Job.TETA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
DDENDversusElidibs = BattleMapping(402, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BYBLOS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.APANDA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ELIDIBS, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
Dorter2 = BattleMapping(403, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION), Job.DARK_KNIGHT_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
AraguayWoods = BattleMapping(404, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION), Job.DARK_KNIGHT_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
ZirekileFalls = BattleMapping(405, [
    SourceUnit(SpriteSet(SpriteSet.GAFGARION), Job.DARK_KNIGHT_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.OVELIA), Job.PRINCESS, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C2), Job.HOLY_KNIGHT_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
ZalandFortCity = BattleMapping(407, [
    SourceUnit(SpriteSet(SpriteSet.MUSTADIO_GUEST), Job.ENGINEER_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
BariausHill = BattleMapping(409, [
    SourceUnit(SpriteSet(SpriteSet.MUSTADIO_GUEST), Job.ENGINEER_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
ZigolisSwamp = BattleMapping(410, [
    SourceUnit(SpriteSet(SpriteSet.MUSTADIO_GUEST), Job.ENGINEER_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.URIBO, UnitGender.MONSTER),
])
#Used sprite sheets: 6
#===
GougMachineCity = BattleMapping(411, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.RUDVICH), Job.RUDVICH, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MUSTADIO), Job.ENGINEER_MUSTADIO, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
BariausValley = BattleMapping(413, [
    SourceUnit(SpriteSet(SpriteSet.AGRIAS), Job.HOLY_KNIGHT_AGRIAS, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GolgorandExecutionSite = BattleMapping(414, [
    SourceUnit(SpriteSet(SpriteSet.GAFGARION_ENEMY), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
LionelCastleGate = BattleMapping(415, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION_ENEMY), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
InsideofLionelCastle = BattleMapping(416, [
    SourceUnit(SpriteSet(SpriteSet.DRACLAU), Job.DRACLAU, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.QUEKLAIN), Job.QUEKLAIN, UnitGender.MALE),
])
#Used sprite sheets: 2
#===
GolandCoalCity = BattleMapping(417, [
    SourceUnit(SpriteSet(SpriteSet.OLAN), Job.ASTROLOGIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MEDIATOR, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Zarghidas = BattleMapping(419, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CHEMIST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.CLOUD), Job.SOLDIER, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
OutsideLesaliaGateZalmo1 = BattleMapping(420, [
    SourceUnit(SpriteSet(SpriteSet.ALMA), Job.CLERIC, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ZALMO), Job.HOLY_PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageSecondFloor = BattleMapping(422, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.IZLUDE), Job.KNIGHT_BLADE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageThirdFloor = BattleMapping(423, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.IZLUDE), Job.KNIGHT_BLADE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageFirstFloor = BattleMapping(424, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GrogHill = BattleMapping(426, [
    SourceUnit(SpriteSet(SpriteSet.OLAN), Job.ASTROLOGIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 7
#===
RescueRafa = BattleMapping(428, [
    SourceUnit(SpriteSet(SpriteSet.RAFA_GUEST), Job.HEAVEN_KNIGHT_GUEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MALAK), Job.HELL_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
YuguoWoods = BattleMapping(430, [
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_WIZARD), Job.WIZARD_UNDEAD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_TIMEMAGE), Job.TIME_MAGE_UNDEAD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.RAFA_GUEST), Job.HEAVEN_KNIGHT_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
RiovanesCastleEntrance = BattleMapping(431, [
    SourceUnit(SpriteSet(SpriteSet.RAFA_GUEST), Job.HEAVEN_KNIGHT_GUEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MALAK), Job.HELL_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
InsideofRiovanesCastle = BattleMapping(432, [
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.NONE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ARCHAIC_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VELIUS), Job.VELIUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.FEMALE),
])
#Used sprite sheets: 6
#===
RooftopofRiovanesCastle = BattleMapping(433, [
    SourceUnit(SpriteSet(SpriteSet.RAFA), Job.HEAVEN_KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MALAK_DEAD), Job.MALAK_DEAD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
UndergroundBookStorageFourthFloor = BattleMapping(435, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageFifthFloor = BattleMapping(436, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
MurondDeathCity = BattleMapping(438, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.KLETIAN), Job.SORCERER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
LostSacredPrecincts = BattleMapping(439, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TIAMAT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BALK), Job.ENGINEER_BALK, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GraveyardofAirships1 = BattleMapping(440, [
    SourceUnit(SpriteSet(SpriteSet.ALMA_DEAD), Job.ALMA_DEAD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.HASHMALUM), Job.HASHMALUM, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AJORA), Job.ALMA_DEAD, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
GraveyardofAirships2 = BattleMapping(441, [
    SourceUnit(SpriteSet(SpriteSet.ALTIMA_2), Job.ALTIMA_2, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALTIMA_1), Job.ALTIMA_1, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.AJORA), Job.AJORA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ULTIMA_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALMA_GOA), Job.ALMA_INITIAL_DEAD, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
DoguolaPass = BattleMapping(442, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BerveniaFreeCity = BattleMapping(443, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MELIADOUL_ENEMY), Job.DIVINE_KNIGHT_MELIADOUL_ENEMY, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
FinathRiver = BattleMapping(444, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.URIBO, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
ZalmoII = BattleMapping(445, [
    SourceUnit(SpriteSet(SpriteSet.DELITA_C2), Job.HOLY_KNIGHT_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ZALMO), Job.HOLY_PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BalkI = BattleMapping(447, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BALK), Job.ENGINEER_BALK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
SouthWallofBethlaGarrison = BattleMapping(448, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
NorthWallofBethlaGarrison = BattleMapping(449, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BethlaSluice = BattleMapping(450, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 3
#===
GerminasPeak = BattleMapping(452, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 3
#===
PoeskasLake = BattleMapping(453, [
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_SUMMONER), Job.SUMMONER_UNDEAD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_ORACLE), Job.ORACLE_UNDEAD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_ARCHER), Job.ARCHER_UNDEAD, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
OutsideofLimberryCastle = BattleMapping(454, [
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.APANDA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
])
#Used sprite sheets: 3
#===
ElmdorII = BattleMapping(456, [
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ULTIMA_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Zalera = BattleMapping(457, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_KNIGHT), Job.KNIGHT_UNDEAD, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MELIADOUL), Job.DIVINE_KNIGHT_MELIADOUL, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ZALERA), Job.ZALERA, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
Adramelk = BattleMapping(459, [
    SourceUnit(SpriteSet(SpriteSet.ZALBAG), Job.ARC_KNIGHT_ZALBAG, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DYCEDARG), Job.LUNE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ADRAMELK), Job.ADRAMELK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
StMurondTemple = BattleMapping(460, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.GEOMANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MEDIATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.PRIEST, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
HallofStMurondTemple = BattleMapping(461, [
    SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.KLETIAN), Job.SORCERER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
])
#Used sprite sheets: 3
#===
ChapelofStMurondTemple = BattleMapping(462, [
    SourceUnit(SpriteSet(SpriteSet.ZALBAG_ZOMBIE), Job.ARC_KNIGHT_ZOMBIE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ARCHAIC_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ULTIMA_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
CollieryUndergroundThirdFloor = BattleMapping(463, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 2
#===
CollieryUndergroundSecondFloor = BattleMapping(464, [
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
CollieryUndergroundFirstFloor = BattleMapping(465, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.URIBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
UndergroundPassageinGoland = BattleMapping(466, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ARCHAIC_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.HOLY_DRAGON), Job.HOLY_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
NelveskaTemple = BattleMapping(468, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_GIANT, UnitGender.MONSTER),
])
#Used sprite sheets: 4

DolbodarSwampEast1.name = 'Dolbodar Swamp East 1'
DolbodarSwampEast2.name = 'Dolbodar Swamp East 2'
DolbodarSwampEast3.name = 'Dolbodar Swamp East 3'
DolbodarSwampEast4.name = 'Dolbodar Swamp East 4'
DolbodarSwampWest1.name = 'Dolbodar Swamp West 1'
DolbodarSwampWest2.name = 'Dolbodar Swamp West 2'
DolbodarSwampWest3.name = 'Dolbodar Swamp West 3'
DolbodarSwampWest4.name = 'Dolbodar Swamp West 4'
FovohamPlainsSouth1.name = 'Fovoham Plains South 1'
FovohamPlainsSouth2.name = 'Fovoham Plains South 2'
FovohamPlainsSouth3.name = 'Fovoham Plains South 3'
FovohamPlainsSouth4.name = 'Fovoham Plains South 4'
FovohamPlainsWest1.name = 'Fovoham Plains West 1'
FovohamPlainsWest2.name = 'Fovoham Plains West 2'
FovohamPlainsWest3.name = 'Fovoham Plains West 3'
FovohamPlainsWest4.name = 'Fovoham Plains West 4'
FovohamPlainsEast1.name = 'Fovoham Plains East 1'
FovohamPlainsEast2.name = 'Fovoham Plains East 2'
FovohamPlainsEast3.name = 'Fovoham Plains East 3'
FovohamPlainsEast4.name = 'Fovoham Plains East 4'
SweegyWoodsEast1.name = 'Sweegy Woods East 1'
SweegyWoodsEast2.name = 'Sweegy Woods East 2'
SweegyWoodsEast3.name = 'Sweegy Woods East 3'
SweegyWoodsEast4.name = 'Sweegy Woods East 4'
SweegyWoodsWest1.name = 'Sweegy Woods West 1'
SweegyWoodsWest2.name = 'Sweegy Woods West 2'
SweegyWoodsWest3.name = 'Sweegy Woods West 3'
SweegyWoodsWest4.name = 'Sweegy Woods West 4'
BerveniaVolcanoNorth1.name = 'Bervenia Volcano North 1'
BerveniaVolcanoNorth2.name = 'Bervenia Volcano North 2'
BerveniaVolcanoNorth3.name = 'Bervenia Volcano North 3'
BerveniaVolcanoNorth4.name = 'Bervenia Volcano North 4'
BerveniaVolcanoSouth1.name = 'Bervenia Volcano South 1'
BerveniaVolcanoSouth2.name = 'Bervenia Volcano South 2'
BerveniaVolcanoSouth3.name = 'Bervenia Volcano South 3'
BerveniaVolcanoSouth4.name = 'Bervenia Volcano South 4'
ZeklausDesertNorth1.name = 'Zeklaus Desert North 1'
ZeklausDesertNorth2.name = 'Zeklaus Desert North 2'
ZeklausDesertNorth3.name = 'Zeklaus Desert North 3'
ZeklausDesertNorth4.name = 'Zeklaus Desert North 4'
ZeklausDesertSouth1.name = 'Zeklaus Desert South 1'
ZeklausDesertSouth2.name = 'Zeklaus Desert South 2'
ZeklausDesertSouth3.name = 'Zeklaus Desert South 3'
ZeklausDesertSouth4.name = 'Zeklaus Desert South 4'
ZeklausDesertEast1.name = 'Zeklaus Desert East 1'
ZeklausDesertEast2.name = 'Zeklaus Desert East 2'
ZeklausDesertEast3.name = 'Zeklaus Desert East 3'
ZeklausDesertEast4.name = 'Zeklaus Desert East 4'
LenaliaPlateauSouth1.name = 'Lenalia Plateau South 1'
LenaliaPlateauSouth2.name = 'Lenalia Plateau South 2'
LenaliaPlateauSouth3.name = 'Lenalia Plateau South 3'
LenaliaPlateauSouth4.name = 'Lenalia Plateau South 4'
LenaliaPlateauNorth1.name = 'Lenalia Plateau North 1'
LenaliaPlateauNorth2.name = 'Lenalia Plateau North 2'
LenaliaPlateauNorth3.name = 'Lenalia Plateau North 3'
LenaliaPlateauNorth4.name = 'Lenalia Plateau North 4'
ZigolisSwampEast1.name = 'Zigolis Swamp East 1'
ZigolisSwampEast2.name = 'Zigolis Swamp East 2'
ZigolisSwampEast3.name = 'Zigolis Swamp East 3'
ZigolisSwampEast4.name = 'Zigolis Swamp East 4'
ZigolisSwampWest1.name = 'Zigolis Swamp West 1'
ZigolisSwampWest2.name = 'Zigolis Swamp West 2'
ZigolisSwampWest3.name = 'Zigolis Swamp West 3'
ZigolisSwampWest4.name = 'Zigolis Swamp West 4'
ZirekileFallsEast5.name = 'Zirekile Falls East 5'
BariusHillSouth5.name = 'Barius Hill South 5'
LenaliaPlateauSouth5.name = 'Lenalia Plateau South 5'
YuguoWoodsWest1.name = 'Yuguo Woods West 1'
YuguoWoodsWest2.name = 'Yuguo Woods West 2'
YuguoWoodsWest3.name = 'Yuguo Woods West 3'
YuguoWoodsWest4.name = 'Yuguo Woods West 4'
YuguoWoodsEast1.name = 'Yuguo Woods East 1'
YuguoWoodsEast2.name = 'Yuguo Woods East 2'
YuguoWoodsEast3.name = 'Yuguo Woods East 3'
YuguoWoodsEast4.name = 'Yuguo Woods East 4'
DolbodarSwampWest5.name = 'Dolbodar Swamp West 5'
GrogHillSouth5.name = 'Grog Hill South 5'
BerveniaVolcanoNorth5.name = 'Bervenia Volcano North 5'
BariusValleySouth5.name = 'Barius Valley South 5'
AraguayWoodsWest1.name = 'Araguay Woods West 1'
AraguayWoodsWest2.name = 'Araguay Woods West 2'
AraguayWoodsWest3.name = 'Araguay Woods West 3'
AraguayWoodsWest4.name = 'Araguay Woods West 4'
AraguayWoodsEast1.name = 'Araguay Woods East 1'
AraguayWoodsEast2.name = 'Araguay Woods East 2'
AraguayWoodsEast3.name = 'Araguay Woods East 3'
AraguayWoodsEast4.name = 'Araguay Woods East 4'
FinathRiverEast5.name = 'Finath River East 5'
GerminasPeakNorth5.name = 'Germinas Peak North 5'
AraguayWoodsWest5.name = 'Araguay Woods West 5'
YuguoWoodsEast5.name = 'Yuguo Woods East 5'
GrogHillWest1.name = 'Grog Hill West 1'
GrogHillWest2.name = 'Grog Hill West 2'
GrogHillWest3.name = 'Grog Hill West 3'
GrogHillWest4.name = 'Grog Hill West 4'
GrogHillSouth1.name = 'Grog Hill South 1'
GrogHillSouth2.name = 'Grog Hill South 2'
GrogHillSouth3.name = 'Grog Hill South 3'
GrogHillSouth4.name = 'Grog Hill South 4'
GrogHillEast1.name = 'Grog Hill East 1'
GrogHillEast2.name = 'Grog Hill East 2'
GrogHillEast3.name = 'Grog Hill East 3'
GrogHillEast4.name = 'Grog Hill East 4'
BedDesertSouth1.name = 'Bed Desert South 1'
BedDesertSouth2.name = 'Bed Desert South 2'
BedDesertSouth3.name = 'Bed Desert South 3'
BedDesertSouth4.name = 'Bed Desert South 4'
BedDesertNorth1.name = 'Bed Desert North 1'
BedDesertNorth2.name = 'Bed Desert North 2'
BedDesertNorth3.name = 'Bed Desert North 3'
BedDesertNorth4.name = 'Bed Desert North 4'
BedDesertNorth5.name = 'Bed Desert North 5'
FovohamPlainsWest5.name = 'Fovoham Plains West 5'
DoguolaPassWest5.name = 'Doguola Pass West 5'
SweegyWoodsEast5.name = 'Sweegy Woods East 5'
ZirekileFallsWest1.name = 'Zirekile Falls West 1'
ZirekileFallsWest2.name = 'Zirekile Falls West 2'
ZirekileFallsWest3.name = 'Zirekile Falls West 3'
ZirekileFallsWest4.name = 'Zirekile Falls West 4'
ZirekileFallsEast1.name = 'Zirekile Falls East 1'
ZirekileFallsEast2.name = 'Zirekile Falls East 2'
ZirekileFallsEast3.name = 'Zirekile Falls East 3'
ZirekileFallsEast4.name = 'Zirekile Falls East 4'
ZirekileFallsSouth1.name = 'Zirekile Falls South 1'
ZirekileFallsSouth2.name = 'Zirekile Falls South 2'
ZirekileFallsSouth3.name = 'Zirekile Falls South 3'
ZirekileFallsSouth4.name = 'Zirekile Falls South 4'
BariusHillNorth1.name = 'Barius Hill North 1'
BariusHillNorth2.name = 'Barius Hill North 2'
BariusHillNorth3.name = 'Barius Hill North 3'
BariusHillNorth4.name = 'Barius Hill North 4'
BariusHillSouth1.name = 'Barius Hill South 1'
BariusHillSouth2.name = 'Barius Hill South 2'
BariusHillSouth3.name = 'Barius Hill South 3'
BariusHillSouth4.name = 'Barius Hill South 4'
PoeskasLakeNorth5.name = 'Poeskas Lake North 5'
ZigolisSwampWest5.name = 'Zigolis Swamp West 5'
MandaliaPlainsSouth5.name = 'Mandalia Plains South 5'
ZeklausDesertSouth5.name = 'Zeklaus Desert South 5'
MandaliaPlainsNorth1.name = 'Mandalia Plains North 1'
MandaliaPlainsNorth2.name = 'Mandalia Plains North 2'
MandaliaPlainsNorth3.name = 'Mandalia Plains North 3'
MandaliaPlainsNorth4.name = 'Mandalia Plains North 4'
MandaliaPlainsSouth1.name = 'Mandalia Plains South 1'
MandaliaPlainsSouth2.name = 'Mandalia Plains South 2'
MandaliaPlainsSouth3.name = 'Mandalia Plains South 3'
MandaliaPlainsSouth4.name = 'Mandalia Plains South 4'
MandaliaPlainsWest1.name = 'Mandalia Plains West 1'
MandaliaPlainsWest2.name = 'Mandalia Plains West 2'
MandaliaPlainsWest3.name = 'Mandalia Plains West 3'
MandaliaPlainsWest4.name = 'Mandalia Plains West 4'
DoguolaPassEast1.name = 'Doguola Pass East 1'
DoguolaPassEast2.name = 'Doguola Pass East 2'
DoguolaPassEast3.name = 'Doguola Pass East 3'
DoguolaPassEast4.name = 'Doguola Pass East 4'
DoguolaPassWest1.name = 'Doguola Pass West 1'
DoguolaPassWest2.name = 'Doguola Pass West 2'
DoguolaPassWest3.name = 'Doguola Pass West 3'
DoguolaPassWest4.name = 'Doguola Pass West 4'
BariusValleyWest1.name = 'Barius Valley West 1'
BariusValleyWest2.name = 'Barius Valley West 2'
BariusValleyWest3.name = 'Barius Valley West 3'
BariusValleyWest4.name = 'Barius Valley West 4'
BariusValleyEast1.name = 'Barius Valley East 1'
BariusValleyEast2.name = 'Barius Valley East 2'
BariusValleyEast3.name = 'Barius Valley East 3'
BariusValleyEast4.name = 'Barius Valley East 4'
BariusValleySouth1.name = 'Barius Valley South 1'
BariusValleySouth2.name = 'Barius Valley South 2'
BariusValleySouth3.name = 'Barius Valley South 3'
BariusValleySouth4.name = 'Barius Valley South 4'
FinathRiverWest1.name = 'Finath River West 1'
FinathRiverWest2.name = 'Finath River West 2'
FinathRiverWest3.name = 'Finath River West 3'
FinathRiverWest4.name = 'Finath River West 4'
FinathRiverEast1.name = 'Finath River East 1'
FinathRiverEast2.name = 'Finath River East 2'
FinathRiverEast3.name = 'Finath River East 3'
FinathRiverEast4.name = 'Finath River East 4'
Horror1.name = 'Horror 1'
Horror2.name = 'Horror 2'
Horror3.name = 'Horror 3'
Horror4.name = 'Horror 4'
PoeskasLakeNorth1.name = 'Poeskas Lake North 1'
PoeskasLakeNorth2.name = 'Poeskas Lake North 2'
PoeskasLakeNorth3.name = 'Poeskas Lake North 3'
PoeskasLakeNorth4.name = 'Poeskas Lake North 4'
PoeskasLakeSouth1.name = 'Poeskas Lake South 1'
PoeskasLakeSouth2.name = 'Poeskas Lake South 2'
PoeskasLakeSouth3.name = 'Poeskas Lake South 3'
PoeskasLakeSouth4.name = 'Poeskas Lake South 4'
Voyage1.name = 'Voyage 1'
Voyage2.name = 'Voyage 2'
Voyage3.name = 'Voyage 3'
Voyage4.name = 'Voyage 4'
GerminasPeakNorth1.name = 'Germina Peak North 1'
GerminasPeakNorth2.name = 'Germina Peak North 2'
GerminasPeakNorth3.name = 'Germina Peak North 3'
GerminasPeakNorth4.name = 'Germina Peak North 4'
GerminasPeakSouth1.name = 'Germina Peak South 1'
GerminasPeakSouth2.name = 'Germina Peak South 2'
GerminasPeakSouth3.name = 'Germina Peak South 3'
GerminasPeakSouth4.name = 'Germina Peak South 4'
Bridge1.name = 'Bridge 1'
Bridge2.name = 'Bridge 2'
Bridge3.name = 'Bridge 3'
Bridge4.name = 'Bridge 4'
Tiger1.name = 'Tiger 1'
Tiger2.name = 'Tiger 2'
Tiger3.name = 'Tiger 3'
Tiger4.name = 'Tiger 4'
Mlapan1.name = 'Mlapan 1'
Mlapan2.name = 'Mlapan 2'
Mlapan3.name = 'Mlapan 3'
Mlapan4.name = 'Mlapan 4'
Valkyries1.name = 'Valkyries 1'
Valkyries2.name = 'Valkyries 2'
Valkyries3.name = 'Valkyries 3'
Valkyries4.name = 'Valkyries 4'
Delta1.name = 'Delta 1'
Delta2.name = 'Delta 2'
Delta3.name = 'Delta 3'
Delta4.name = 'Delta 4'
Terminate1.name = 'Terminate 1'
Terminate2.name = 'Terminate 2'
Terminate3.name = 'Terminate 3'
Terminate4.name = 'Terminate 4'
Nogias1.name = 'Nogias 1'
Nogias2.name = 'Nogias 2'
Nogias3.name = 'Nogias 3'
Nogias4.name = 'Nogias 4'
SweegyWoods.name = 'Sweegy Woods'
DorterTradeCity1.name = 'Dorter Trade City1'
SandRatCellar.name = 'Sand Rat Cellar'
GarilandFight.name = 'Gariland Fight'
MandaliaPlains.name = 'Mandalia Plains'
Miluda1.name = 'Miluda1'
Miluda2.name = 'Miluda2'
Wiegraf1.name = 'Wiegraf1'
FortZeakden.name = 'Fort Zeakden'
DDENDversusElidibs.name = 'DD END versus Elidibs'
Dorter2.name = 'Dorter2'
AraguayWoods.name = 'Araguay Woods'
ZirekileFalls.name = 'Zirekile Falls'
ZalandFortCity.name = 'Zaland Fort City'
BariausHill.name = 'Bariaus Hill'
ZigolisSwamp.name = 'Zigolis Swamp'
GougMachineCity.name = 'Goug Machine City'
BariausValley.name = 'Bariaus Valley'
GolgorandExecutionSite.name = 'Golgorand Execution Site'
LionelCastleGate.name = 'Lionel Castle Gate '
InsideofLionelCastle.name = 'Inside of Lionel Castle'
GolandCoalCity.name = 'Goland Coal City'
Zarghidas.name = 'Zarghidas'
OutsideLesaliaGateZalmo1.name = 'Outside Lesalia Gate Zalmo 1'
UndergroundBookStorageSecondFloor.name = 'Underground Book Storage Second Floor'
UndergroundBookStorageThirdFloor.name = 'Underground Book Storage Third Floor'
UndergroundBookStorageFirstFloor.name = 'Underground Book Storage First Floor'
GrogHill.name = 'Grog Hill '
RescueRafa.name = 'Rescue Rafa'
YuguoWoods.name = 'Yuguo Woods'
RiovanesCastleEntrance.name = 'Riovanes Castle Entrance'
InsideofRiovanesCastle.name = 'Inside of Riovanes Castle'
RooftopofRiovanesCastle.name = 'Rooftop of Riovanes Castle'
UndergroundBookStorageFourthFloor.name = 'Underground Book Storage Fourth Floor'
UndergroundBookStorageFifthFloor.name = 'Underground Book Storage Fifth Floor'
MurondDeathCity.name = 'Murond Death City'
LostSacredPrecincts.name = 'Lost Sacred Precincts'
GraveyardofAirships1.name = 'Graveyard of Airships 1'
GraveyardofAirships2.name = 'Graveyard of Airships 2'
DoguolaPass.name = 'Doguola Pass'
BerveniaFreeCity.name = 'Bervenia Free City'
FinathRiver.name = 'Finath River'
ZalmoII.name = 'Zalmo II'
BalkI.name = 'Balk I'
SouthWallofBethlaGarrison.name = 'South Wall of Bethla Garrison'
NorthWallofBethlaGarrison.name = 'North Wall of Bethla Garrison'
BethlaSluice.name = 'Bethla Sluice'
GerminasPeak.name = 'Germinas Peak'
PoeskasLake.name = 'Poeskas Lake'
OutsideofLimberryCastle.name = 'Outside of Limberry Castle'
ElmdorII.name = 'Elmdor II'
Zalera.name = 'Zalera'
Adramelk.name = 'Adramelk'
StMurondTemple.name = 'St Murond Temple'
HallofStMurondTemple.name = 'Hall of St Murond Temple'
ChapelofStMurondTemple.name = 'Chapel of St Murond Temple'
CollieryUndergroundThirdFloor.name = 'Colliery Underground Third Floor'
CollieryUndergroundSecondFloor.name = 'Colliery Underground Second Floor'
CollieryUndergroundFirstFloor.name = 'Colliery Underground First Floor'
UndergroundPassageinGoland.name = 'Underground Passage in Goland'
NelveskaTemple.name = 'Nelveska Temple'

gallione_only_randoms: list[BattleMapping] = [
    MandaliaPlainsNorth1,
    MandaliaPlainsNorth2,
    MandaliaPlainsNorth3,
    MandaliaPlainsNorth4,
    MandaliaPlainsSouth1,
    MandaliaPlainsSouth2,
    MandaliaPlainsSouth3,
    MandaliaPlainsSouth4,
    MandaliaPlainsSouth5,
    MandaliaPlainsWest1,
    MandaliaPlainsWest2,
    MandaliaPlainsWest3,
    MandaliaPlainsWest4,
    SweegyWoodsEast1,
    SweegyWoodsEast2,
    SweegyWoodsEast3,
    SweegyWoodsEast4,
    SweegyWoodsEast5,
    SweegyWoodsWest1,
    SweegyWoodsWest2,
    SweegyWoodsWest3,
    SweegyWoodsWest4,
    LenaliaPlateauSouth1,
    LenaliaPlateauSouth2,
    LenaliaPlateauSouth3,
    LenaliaPlateauSouth4,
    LenaliaPlateauSouth5
]

gallione_randoms_from_fovoham: list[BattleMapping] = [
    LenaliaPlateauNorth1,
    LenaliaPlateauNorth2,
    LenaliaPlateauNorth3,
    LenaliaPlateauNorth4
]

gallione_randoms: list[BattleMapping] = [*gallione_only_randoms, *gallione_randoms_from_fovoham]

gallione_story_fights: list[BattleMapping] = [
    GarilandFight,
    MandaliaPlains,
    SweegyWoods,
    DorterTradeCity1,
    Miluda1,
    Miluda2,
    FortZeakden,
    Dorter2,
    Adramelk
]

gallione_fights: list[BattleMapping] = [*gallione_randoms, *gallione_story_fights]

fovoham_only_randoms: list[BattleMapping] = [
    FovohamPlainsEast1,
    FovohamPlainsEast2,
    FovohamPlainsEast3,
    FovohamPlainsEast4,
    YuguoWoodsEast1,
    YuguoWoodsEast2,
    YuguoWoodsEast3,
    YuguoWoodsEast4,
    YuguoWoodsEast5,
    YuguoWoodsWest1,
    YuguoWoodsWest2,
    YuguoWoodsWest3,
    YuguoWoodsWest4,
    GrogHillWest1,
    GrogHillWest2,
    GrogHillWest3,
    GrogHillWest4
]

fovoham_randoms_from_gallione: list[BattleMapping] = [
    FovohamPlainsWest1,
    FovohamPlainsWest2,
    FovohamPlainsWest3,
    FovohamPlainsWest4,
    FovohamPlainsWest5,
    FovohamPlainsSouth1,
    FovohamPlainsSouth2,
    FovohamPlainsSouth3,
    FovohamPlainsSouth4
]

fovoham_randoms_from_lesalia: list[BattleMapping] = [
    GrogHillSouth1,
    GrogHillSouth2,
    GrogHillSouth3,
    GrogHillSouth4,
    GrogHillSouth5
]

fovoham_randoms_from_zeltennia: list[BattleMapping] = [
    GrogHillEast1,
    GrogHillEast2,
    GrogHillEast3,
    GrogHillEast4
]

fovoham_randoms: list[BattleMapping] = [
    *fovoham_only_randoms, *fovoham_randoms_from_gallione,
    *fovoham_randoms_from_lesalia, *fovoham_randoms_from_zeltennia
]

fovoham_story_fights: list[BattleMapping] = [
    Wiegraf1,
    GrogHill,
    RescueRafa,
    YuguoWoods,
    RiovanesCastleEntrance,
    InsideofRiovanesCastle,
    RooftopofRiovanesCastle
]

fovoham_fights: list[BattleMapping] = [*fovoham_randoms, *fovoham_story_fights]

lesalia_only_randoms: list[BattleMapping] = [
    BerveniaVolcanoSouth1,
    BerveniaVolcanoSouth2,
    BerveniaVolcanoSouth3,
    BerveniaVolcanoSouth4,
    ZeklausDesertNorth1,
    ZeklausDesertNorth2,
    ZeklausDesertNorth3,
    ZeklausDesertNorth4,
    ZeklausDesertEast1,
    ZeklausDesertEast2,
    ZeklausDesertEast3,
    ZeklausDesertEast4,
    AraguayWoodsEast1,
    AraguayWoodsEast2,
    AraguayWoodsEast3,
    AraguayWoodsEast4,
    ZirekileFallsWest1,
    ZirekileFallsWest2,
    ZirekileFallsWest3,
    ZirekileFallsWest4
]

lesalia_randoms_from_gallione: list[BattleMapping] = [
    AraguayWoodsWest1,
    AraguayWoodsWest2,
    AraguayWoodsWest3,
    AraguayWoodsWest4,
    AraguayWoodsWest5,
]

lesalia_randoms_from_fovoham: list[BattleMapping] = [
    BerveniaVolcanoNorth1,
    BerveniaVolcanoNorth2,
    BerveniaVolcanoNorth3,
    BerveniaVolcanoNorth4,
    BerveniaVolcanoNorth5
]

lesalia_randoms_from_lionel: list[BattleMapping] = [
    ZirekileFallsSouth1,
    ZirekileFallsSouth2,
    ZirekileFallsSouth3,
    ZirekileFallsSouth4,
]

lesalia_randoms_from_limberry: list[BattleMapping] = [
    ZirekileFallsEast1,
    ZirekileFallsEast2,
    ZirekileFallsEast3,
    ZirekileFallsEast4,
    ZirekileFallsEast5,
]

lesalia_randoms: list[BattleMapping] = [
    *lesalia_only_randoms, *lesalia_randoms_from_gallione, *lesalia_randoms_from_fovoham,
    *lesalia_randoms_from_lionel, *lesalia_randoms_from_limberry
]

lesalia_story_fights: list[BattleMapping] = [
    SandRatCellar,
    AraguayWoods,
    ZirekileFalls,
    GolandCoalCity,
    OutsideLesaliaGateZalmo1,
    CollieryUndergroundThirdFloor,
    CollieryUndergroundSecondFloor,
    CollieryUndergroundFirstFloor
]

lesalia_fights: list[BattleMapping] = [*lesalia_randoms, *lesalia_story_fights]

lionel_only_randoms: list[BattleMapping] = [
    BariusHillNorth1,
    BariusHillNorth2,
    BariusHillNorth3,
    BariusHillNorth4,
    BariusHillSouth1,
    BariusHillSouth2,
    BariusHillSouth3,
    BariusHillSouth4,
    BariusHillSouth5,
    ZigolisSwampEast1,
    ZigolisSwampEast2,
    ZigolisSwampEast3,
    ZigolisSwampEast4
]

lionel_randoms_from_murond: list[BattleMapping] = [
    ZigolisSwampWest1,
    ZigolisSwampWest2,
    ZigolisSwampWest3,
    ZigolisSwampWest4,
    ZigolisSwampWest5,
]

lionel_randoms: list[BattleMapping] = [*lionel_only_randoms, *lionel_randoms_from_murond]

lionel_story_fights: list[BattleMapping] = [
    ZalandFortCity,
    BariausHill,
    ZigolisSwamp,
    BariausValley,
    GolgorandExecutionSite,
    LionelCastleGate,
    InsideofLionelCastle
]

lionel_fights: list[BattleMapping] = [*lionel_randoms, *lionel_story_fights]

zeltennia_only_randoms: list[BattleMapping] = [
    DoguolaPassEast1,
    DoguolaPassEast2,
    DoguolaPassEast3,
    DoguolaPassEast4,
    FinathRiverEast1,
    FinathRiverEast2,
    FinathRiverEast3,
    FinathRiverEast4,
    FinathRiverEast5,
    FinathRiverWest1,
    FinathRiverWest2,
    FinathRiverWest3,
    FinathRiverWest4,
    GerminasPeakNorth1,
    GerminasPeakNorth2,
    GerminasPeakNorth3,
    GerminasPeakNorth4,
    GerminasPeakNorth5
]

zeltennia_randoms_from_fovoham: list[BattleMapping] = [
    DoguolaPassWest1,
    DoguolaPassWest2,
    DoguolaPassWest3,
    DoguolaPassWest4,
    DoguolaPassWest5
]

zeltennia_randoms_from_limberry: list[BattleMapping] = [
    GerminasPeakSouth1,
    GerminasPeakSouth2,
    GerminasPeakSouth3,
    GerminasPeakSouth4,
]

zeltennia_randoms: list[BattleMapping] = [
    *zeltennia_only_randoms, *zeltennia_randoms_from_fovoham, *zeltennia_randoms_from_limberry
]

zeltennia_story_fights: list[BattleMapping] = [
    DoguolaPass,
    BerveniaFreeCity,
    FinathRiver,
    ZalmoII,
    GerminasPeak,
    NelveskaTemple,
    Zarghidas
]

zeltennia_fights: list[BattleMapping] = [*zeltennia_randoms, *zeltennia_story_fights]

limberry_only_randoms: list[BattleMapping] = [
    BedDesertSouth1,
    BedDesertSouth2,
    BedDesertSouth3,
    BedDesertSouth4,
    DolbodarSwampEast1,
    DolbodarSwampEast2,
    DolbodarSwampEast3,
    DolbodarSwampEast4,
    DolbodarSwampWest1,
    DolbodarSwampWest2,
    DolbodarSwampWest3,
    DolbodarSwampWest4,
    DolbodarSwampWest5,
    PoeskasLakeSouth1,
    PoeskasLakeSouth2,
    PoeskasLakeSouth3,
    PoeskasLakeSouth4
]

limberry_randoms_from_zeltennia: list[BattleMapping] = [
    BedDesertNorth1,
    BedDesertNorth2,
    BedDesertNorth3,
    BedDesertNorth4,
    BedDesertNorth5,
    PoeskasLakeNorth1,
    PoeskasLakeNorth2,
    PoeskasLakeNorth3,
    PoeskasLakeNorth4,
    PoeskasLakeNorth5,
]

limberry_randoms: list[BattleMapping] = [*limberry_only_randoms, *limberry_randoms_from_zeltennia]

limberry_story_fights: list[BattleMapping] = [
    BalkI,
    NorthWallofBethlaGarrison,
    SouthWallofBethlaGarrison,
    BethlaSluice,
    PoeskasLake,
    OutsideofLimberryCastle,
    ElmdorII,
    Zalera
]

limberry_fights: list[BattleMapping] = [*limberry_randoms, *limberry_story_fights]

nogias_fights: list[BattleMapping] = [
    Nogias1,
    Nogias2,
    Nogias3,
    Nogias4,
]

terminate_fights: list[BattleMapping] = [
    Terminate1,
    Terminate2,
    Terminate3,
    Terminate4,
]

delta_fights: list[BattleMapping] = [
    Delta1,
    Delta2,
    Delta3,
    Delta4,
]

valkyries_fights: list[BattleMapping] = [
    Valkyries1,
    Valkyries2,
    Valkyries3,
    Valkyries4
]

mlapan_fights: list[BattleMapping] = [
    Mlapan1,
    Mlapan2,
    Mlapan3,
    Mlapan4
]

tiger_fights: list[BattleMapping] = [
    Tiger1,
    Tiger2,
    Tiger3,
    Tiger4
]

bridge_fights: list[BattleMapping] = [
    Bridge1,
    Bridge2,
    Bridge3,
    Bridge4
]

voyage_fights: list[BattleMapping] = [
    Voyage1,
    Voyage2,
    Voyage3,
    Voyage4
]

horror_fights: list[BattleMapping] = [
    Horror1,
    Horror2,
    Horror3,
    Horror4
]

deep_dungeon_fights: list[BattleMapping] = [
    *nogias_fights, *terminate_fights, *delta_fights, *valkyries_fights,
    *mlapan_fights, *tiger_fights, *bridge_fights, *voyage_fights, *horror_fights
]

murond_story_fights: list[BattleMapping] = [
    GougMachineCity,
    UndergroundBookStorageSecondFloor,
    UndergroundBookStorageThirdFloor,
    UndergroundBookStorageFirstFloor,
    StMurondTemple,
    HallofStMurondTemple,
    ChapelofStMurondTemple,
    UndergroundBookStorageFourthFloor,
    UndergroundBookStorageFifthFloor,
    MurondDeathCity,
    LostSacredPrecincts,
    GraveyardofAirships1,
    GraveyardofAirships2,
    *deep_dungeon_fights
]

all_randoms: list[BattleMapping] = [
    *gallione_randoms, *fovoham_randoms, *lesalia_randoms, *lionel_randoms,
    *zeltennia_randoms, *limberry_randoms
]

all_story_fights: list[BattleMapping] = [
    *gallione_story_fights, *fovoham_story_fights, *lesalia_story_fights,
    *lionel_story_fights, *zeltennia_story_fights, *limberry_story_fights, *murond_story_fights
]

all_fights: list[BattleMapping] = [*all_randoms, *all_story_fights]