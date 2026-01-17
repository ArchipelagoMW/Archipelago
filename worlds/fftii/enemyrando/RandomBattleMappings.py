from .BattleMappings import BattleMapping
from .EventCodes import EventCode
from .Job import Job
from .RandomizedUnitFactory import RandomizedUnitFactory
from .RandomizedUnits import RandomizedUnit
from .SourceUnit import SourceUnit
from .SpriteSet import SpriteSet
from worlds.fftii.patchersuite.Unit import UnitGender

DolbodarSwampEast1 = BattleMapping(1, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DolbodarSwampEast2 = BattleMapping(2, 2, [
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
DolbodarSwampEast3 = BattleMapping(3, 5, [
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
DolbodarSwampEast4 = BattleMapping(4, 8, [
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
DolbodarSwampWest1 = BattleMapping(5, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DolbodarSwampWest2 = BattleMapping(6, 2, [
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
DolbodarSwampWest3 = BattleMapping(7, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DolbodarSwampWest4 = BattleMapping(8, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth1 = BattleMapping(13, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth2 = BattleMapping(14, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth3 = BattleMapping(15, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsSouth4 = BattleMapping(16, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsWest1 = BattleMapping(17, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
FovohamPlainsWest2 = BattleMapping(18, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsWest3 = BattleMapping(19, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
FovohamPlainsWest4 = BattleMapping(20, 8, [
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
FovohamPlainsEast1 = BattleMapping(21, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsEast2 = BattleMapping(22, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsEast3 = BattleMapping(23, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FovohamPlainsEast4 = BattleMapping(24, 8, [
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
SweegyWoodsEast1 = BattleMapping(25, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
SweegyWoodsEast2 = BattleMapping(26, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsEast3 = BattleMapping(27, 5, [
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
SweegyWoodsEast4 = BattleMapping(28, 8, [
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
SweegyWoodsWest1 = BattleMapping(29, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsWest2 = BattleMapping(30, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
SweegyWoodsWest3 = BattleMapping(31, 5, [
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
SweegyWoodsWest4 = BattleMapping(32, 8, [
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
BerveniaVolcanoNorth1 = BattleMapping(37, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BerveniaVolcanoNorth2 = BattleMapping(38, 2, [
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
BerveniaVolcanoNorth3 = BattleMapping(39, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BerveniaVolcanoNorth4 = BattleMapping(40, 8, [
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
BerveniaVolcanoSouth1 = BattleMapping(41, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BerveniaVolcanoSouth2 = BattleMapping(42, 2, [
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
BerveniaVolcanoSouth3 = BattleMapping(43, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BerveniaVolcanoSouth4 = BattleMapping(44, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertNorth1 = BattleMapping(49, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertNorth2 = BattleMapping(50, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
ZeklausDesertNorth3 = BattleMapping(51, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertNorth4 = BattleMapping(52, 8, [
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
ZeklausDesertSouth1 = BattleMapping(53, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertSouth2 = BattleMapping(54, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertSouth3 = BattleMapping(55, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
ZeklausDesertSouth4 = BattleMapping(56, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertEast1 = BattleMapping(57, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertEast2 = BattleMapping(58, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZeklausDesertEast3 = BattleMapping(59, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZeklausDesertEast4 = BattleMapping(60, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauSouth1 = BattleMapping(61, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauSouth2 = BattleMapping(62, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
LenaliaPlateauSouth3 = BattleMapping(63, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
LenaliaPlateauSouth4 = BattleMapping(64, 8, [
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
LenaliaPlateauNorth1 = BattleMapping(65, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauNorth2 = BattleMapping(66, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
LenaliaPlateauNorth3 = BattleMapping(67, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
LenaliaPlateauNorth4 = BattleMapping(68, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
ZigolisSwampEast1 = BattleMapping(73, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZigolisSwampEast2 = BattleMapping(74, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZigolisSwampEast3 = BattleMapping(75, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.EXPLOSIVE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
ZigolisSwampEast4 = BattleMapping(76, 8, [
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
ZigolisSwampWest1 = BattleMapping(77, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZigolisSwampWest2 = BattleMapping(78, 2, [
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
ZigolisSwampWest3 = BattleMapping(79, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZigolisSwampWest4 = BattleMapping(80, 8, [
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
ZirekileFallsEast5 = BattleMapping(82, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BariusHillSouth5 = BattleMapping(83, 9, [
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
LenaliaPlateauSouth5 = BattleMapping(84, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CALCULATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CALCULATOR, UnitGender.FEMALE),
])
#Used sprite sheets: 2
#===
YuguoWoodsWest1 = BattleMapping(85, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
YuguoWoodsWest2 = BattleMapping(86, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
YuguoWoodsWest3 = BattleMapping(87, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
YuguoWoodsWest4 = BattleMapping(88, 8, [
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
YuguoWoodsEast1 = BattleMapping(89, 0, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
YuguoWoodsEast2 = BattleMapping(90, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
YuguoWoodsEast3 = BattleMapping(91, 5, [
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
YuguoWoodsEast4 = BattleMapping(92, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
DolbodarSwampWest5 = BattleMapping(93, 9, [
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
GrogHillSouth5 = BattleMapping(94, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
])
#Used sprite sheets: 1
#===
BerveniaVolcanoNorth5 = BattleMapping(95, 9, [
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
BariusValleySouth5 = BattleMapping(96, 9, [
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
AraguayWoodsWest1 = BattleMapping(97, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
AraguayWoodsWest2 = BattleMapping(98, 2, [
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
AraguayWoodsWest3 = BattleMapping(99, 5, [
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
AraguayWoodsWest4 = BattleMapping(100, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
AraguayWoodsEast1 = BattleMapping(101, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
AraguayWoodsEast2 = BattleMapping(102, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
AraguayWoodsEast3 = BattleMapping(103, 5, [
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
AraguayWoodsEast4 = BattleMapping(104, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverEast5 = BattleMapping(105, 9, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakNorth5 = BattleMapping(106, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CHEMIST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MEDIATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MEDIATOR, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
AraguayWoodsWest5 = BattleMapping(107, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
])
#Used sprite sheets: 2
#===
YuguoWoodsEast5 = BattleMapping(108, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
])
#Used sprite sheets: 1
#===
GrogHillWest1 = BattleMapping(109, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
GrogHillWest2 = BattleMapping(110, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GrogHillWest3 = BattleMapping(111, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillWest4 = BattleMapping(112, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillSouth1 = BattleMapping(113, 0, [
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
GrogHillSouth2 = BattleMapping(114, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.GEOMANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
GrogHillSouth3 = BattleMapping(115, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GrogHillSouth4 = BattleMapping(116, 8, [
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
GrogHillEast1 = BattleMapping(117, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
GrogHillEast2 = BattleMapping(118, 2, [
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
GrogHillEast3 = BattleMapping(119, 5, [
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
GrogHillEast4 = BattleMapping(120, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BedDesertSouth1 = BattleMapping(121, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BedDesertSouth2 = BattleMapping(122, 2, [
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
BedDesertSouth3 = BattleMapping(123, 5, [
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
BedDesertSouth4 = BattleMapping(124, 8, [
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
BedDesertNorth1 = BattleMapping(125, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BedDesertNorth2 = BattleMapping(126, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.GEOMANCER, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
BedDesertNorth3 = BattleMapping(127, 5, [
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
BedDesertNorth4 = BattleMapping(128, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ORACLE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BedDesertNorth5 = BattleMapping(129, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.GEOMANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
FovohamPlainsWest5 = BattleMapping(130, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
DoguolaPassWest5 = BattleMapping(131, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
SweegyWoodsEast5 = BattleMapping(132, 9, [
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
ZirekileFallsWest1 = BattleMapping(133, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsWest2 = BattleMapping(134, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
ZirekileFallsWest3 = BattleMapping(135, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsWest4 = BattleMapping(136, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsEast1 = BattleMapping(137, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
ZirekileFallsEast2 = BattleMapping(138, 2, [
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
ZirekileFallsEast3 = BattleMapping(139, 5, [
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
ZirekileFallsEast4 = BattleMapping(140, 8, [
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
ZirekileFallsSouth1 = BattleMapping(141, 0, [
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
ZirekileFallsSouth2 = BattleMapping(142, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
ZirekileFallsSouth3 = BattleMapping(143, 5, [
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
ZirekileFallsSouth4 = BattleMapping(144, 8, [
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
BariusHillNorth1 = BattleMapping(145, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BariusHillNorth2 = BattleMapping(146, 2, [
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
BariusHillNorth3 = BattleMapping(147, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusHillNorth4 = BattleMapping(148, 8, [
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
BariusHillSouth1 = BattleMapping(149, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
BariusHillSouth2 = BattleMapping(150, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
BariusHillSouth3 = BattleMapping(151, 5, [
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
BariusHillSouth4 = BattleMapping(152, 8, [
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
PoeskasLakeNorth5 = BattleMapping(153, 9, [
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
ZigolisSwampWest5 = BattleMapping(154, 9, [
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
MandaliaPlainsSouth5 = BattleMapping(155, 9, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
ZeklausDesertSouth5 = BattleMapping(156, 9, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 2
#===
MandaliaPlainsNorth1 = BattleMapping(157, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
MandaliaPlainsNorth2 = BattleMapping(158, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsNorth3 = BattleMapping(159, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsNorth4 = BattleMapping(160, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsSouth1 = BattleMapping(161, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
MandaliaPlainsSouth2 = BattleMapping(162, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
MandaliaPlainsSouth3 = BattleMapping(163, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GRENADE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsSouth4 = BattleMapping(164, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsWest1 = BattleMapping(165, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
MandaliaPlainsWest2 = BattleMapping(166, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsWest3 = BattleMapping(167, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
MandaliaPlainsWest4 = BattleMapping(168, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
DoguolaPassEast1 = BattleMapping(169, 0, [
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
DoguolaPassEast2 = BattleMapping(170, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassEast3 = BattleMapping(171, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
DoguolaPassEast4 = BattleMapping(172, 8, [
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
DoguolaPassWest1 = BattleMapping(173, 0, [
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
DoguolaPassWest2 = BattleMapping(174, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DoguolaPassWest3 = BattleMapping(175, 5, [
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
DoguolaPassWest4 = BattleMapping(176, 8, [
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
BariusValleyWest1 = BattleMapping(181, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyWest2 = BattleMapping(182, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyWest3 = BattleMapping(183, 5, [
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
BariusValleyWest4 = BattleMapping(184, 8, [
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
BariusValleyEast1 = BattleMapping(185, 0, [
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
BariusValleyEast2 = BattleMapping(186, 2, [
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
BariusValleyEast3 = BattleMapping(187, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleyEast4 = BattleMapping(188, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
BariusValleySouth1 = BattleMapping(189, 0, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
BariusValleySouth2 = BattleMapping(190, 2, [
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
BariusValleySouth3 = BattleMapping(191, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
BariusValleySouth4 = BattleMapping(192, 8, [
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
FinathRiverWest1 = BattleMapping(193, 0, [
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
FinathRiverWest2 = BattleMapping(194, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
FinathRiverWest3 = BattleMapping(195, 5, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PISCO_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverWest4 = BattleMapping(196, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINDFLARE, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverEast1 = BattleMapping(197, 0, [
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
FinathRiverEast2 = BattleMapping(198, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SQUIDLARKIN, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
FinathRiverEast3 = BattleMapping(199, 5, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
FinathRiverEast4 = BattleMapping(200, 8, [
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
Horror1 = BattleMapping(201, 12, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Horror2 = BattleMapping(202, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.LANCER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Horror3 = BattleMapping(203, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SAMURAI, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
Horror4 = BattleMapping(204, 12, [
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
PoeskasLakeNorth1 = BattleMapping(205, 0, [
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
PoeskasLakeNorth2 = BattleMapping(206, 2, [
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
PoeskasLakeNorth3 = BattleMapping(207, 5, [
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
PoeskasLakeNorth4 = BattleMapping(208, 8, [
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
PoeskasLakeSouth1 = BattleMapping(209, 0, [
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
PoeskasLakeSouth2 = BattleMapping(210, 2, [
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
PoeskasLakeSouth3 = BattleMapping(211, 5, [
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
PoeskasLakeSouth4 = BattleMapping(212, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Voyage1 = BattleMapping(213, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
])
#Used sprite sheets: 2
#===
Voyage2 = BattleMapping(214, 12, [
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
Voyage3 = BattleMapping(215, 12, [
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
Voyage4 = BattleMapping(216, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CALCULATOR, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CALCULATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
GerminasPeakNorth1 = BattleMapping(217, 0, [
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
GerminasPeakNorth2 = BattleMapping(218, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakNorth3 = BattleMapping(219, 5, [
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
GerminasPeakNorth4 = BattleMapping(220, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakSouth1 = BattleMapping(221, 0, [
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
GerminasPeakSouth2 = BattleMapping(222, 2, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
GerminasPeakSouth3 = BattleMapping(223, 5, [
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
GerminasPeakSouth4 = BattleMapping(224, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Bridge1 = BattleMapping(225, 12, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
Bridge2 = BattleMapping(226, 12, [
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
Bridge3 = BattleMapping(227, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SACRED, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Bridge4 = BattleMapping(228, 12, [
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
Tiger1 = BattleMapping(229, 12, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.VAMPIRE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
Tiger2 = BattleMapping(230, 12, [
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
Tiger3 = BattleMapping(231, 12, [
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
Tiger4 = BattleMapping(232, 12, [
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
Mlapan1 = BattleMapping(233, 12, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Mlapan2 = BattleMapping(234, 12, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.WOODMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBBLEDEGUCK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TRENT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TAIJU, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Mlapan3 = BattleMapping(235, 12, [
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
Mlapan4 = BattleMapping(236, 12, [
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
Valkyries1 = BattleMapping(237, 10, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GREAT_MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Valkyries2 = BattleMapping(238, 10, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MORBOL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Valkyries3 = BattleMapping(239, 10, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.JURAVIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_HAWK, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Valkyries4 = BattleMapping(240, 10, [
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
Delta1 = BattleMapping(241, 10, [
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
Delta2 = BattleMapping(242, 10, [
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
Delta3 = BattleMapping(243, 10, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.MINITAURUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Delta4 = BattleMapping(244, 10, [
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
Terminate1 = BattleMapping(245, 10, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Terminate2 = BattleMapping(246, 10, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.FLOTIBALL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.AHRIMAN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Terminate3 = BattleMapping(247, 10, [
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
Terminate4 = BattleMapping(248, 10, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Nogias1 = BattleMapping(249, 10, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
])
#Used sprite sheets: 1
#===
Nogias2 = BattleMapping(250, 10, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.CUAR, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
Nogias3 = BattleMapping(251, 10, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BULL_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
Nogias4 = BattleMapping(252, 10, [
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