from .BattleMappings import BattleMapping
from .Job import Job
from .SourceUnit import SourceUnit
from .SpriteSet import SpriteSet
from worlds.fftii.patchersuite.Unit import UnitGender


SweegyWoods = BattleMapping(384, 1, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BOMB, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
DorterTradeCity1 = BattleMapping(385, 1, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    #SourceUnit(SpriteSet(SpriteSet.WIEGRAF1), Job.WHITE_KNIGHT_C1, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
SandRatCellar = BattleMapping(386, 1, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
GarilandFight = BattleMapping(388, 0, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SQUIRE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
MandaliaPlains = BattleMapping(389, 0, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_PANTHER, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
Miluda1 = BattleMapping(395, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.SQUIRE_ALGUS, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.PRIEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
Miluda2 = BattleMapping(399, 2, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Wiegraf1 = BattleMapping(400, 3, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF1), Job.WHITE_KNIGHT_C1, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
FortZeakden = BattleMapping(401, 3, [
    SourceUnit(SpriteSet(SpriteSet.ZALBAG), Job.ARC_KNIGHT_ZALBAG, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.TETA), Job.TETA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C1), Job.SQUIRE_DELITA, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
DDENDversusElidibs = BattleMapping(402, 14, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BYBLOS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.APANDA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ELIDIBS, UnitGender.MONSTER),
])
#Used sprite sheets: 3
#===
Dorter2 = BattleMapping(403, 4, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION), Job.DARK_KNIGHT_GUEST, UnitGender.MALE),
    #SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 6
#===
AraguayWoods = BattleMapping(404, 4, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION), Job.DARK_KNIGHT_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
ZirekileFalls = BattleMapping(405, 4, [
    SourceUnit(SpriteSet(SpriteSet.GAFGARION), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.OVELIA), Job.PRINCESS, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.DELITA_C2), Job.HOLY_KNIGHT_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
ZalandFortCity = BattleMapping(407, 5, [
    SourceUnit(SpriteSet(SpriteSet.MUSTADIO_GUEST), Job.ENGINEER_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
BariausHill = BattleMapping(409, 5, [
    SourceUnit(SpriteSet(SpriteSet.MUSTADIO_GUEST), Job.ENGINEER_GUEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AGRIAS_GUEST), Job.HOLY_KNIGHT_AGRIAS_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
ZigolisSwamp = BattleMapping(410, 6, [
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
GougMachineCity = BattleMapping(411, 6, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.RUDVICH), Job.RUDVICH, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MUSTADIO), Job.ENGINEER_MUSTADIO, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
BariausValley = BattleMapping(413, 6, [
    SourceUnit(SpriteSet(SpriteSet.AGRIAS), Job.HOLY_KNIGHT_AGRIAS, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GolgorandExecutionSite = BattleMapping(414, 7, [
    SourceUnit(SpriteSet(SpriteSet.GAFGARION_ENEMY), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.TIMEMAGE, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
LionelCastleGate = BattleMapping(415, 7, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION_ENEMY), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
InsideofLionelCastle = BattleMapping(416, 7, [
    SourceUnit(SpriteSet(SpriteSet.DRACLAU), Job.DRACLAU, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.QUEKLAIN), Job.QUEKLAIN, UnitGender.MALE),
])
#Used sprite sheets: 2
#===
GolandCoalCity = BattleMapping(417, 8, [
    SourceUnit(SpriteSet(SpriteSet.OLAN), Job.ASTROLOGIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.THIEF, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MEDIATOR, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Zarghidas = BattleMapping(419, 14, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SQUIRE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.CHEMIST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.CLOUD), Job.SOLDIER, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
OutsideLesaliaGateZalmo1 = BattleMapping(420, 8, [
    SourceUnit(SpriteSet(SpriteSet.ALMA), Job.CLERIC, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ZALMO), Job.HOLY_PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.MONK, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageSecondFloor = BattleMapping(422, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
    #SourceUnit(SpriteSet(SpriteSet.IZLUDE), Job.KNIGHT_BLADE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageThirdFloor = BattleMapping(423, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.IZLUDE), Job.KNIGHT_BLADE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageFirstFloor = BattleMapping(424, 9, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.WIZARD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GrogHill = BattleMapping(426, 10, [
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
RescueRafa = BattleMapping(428, 10, [
    SourceUnit(SpriteSet(SpriteSet.RAFA_GUEST), Job.HEAVEN_KNIGHT_GUEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MALAK), Job.HELL_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
YuguoWoods = BattleMapping(430, 11, [
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_WIZARD), Job.WIZARD_UNDEAD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GHOUL, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GUST, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_TIMEMAGE), Job.TIME_MAGE_UNDEAD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.RAFA_GUEST), Job.HEAVEN_KNIGHT_GUEST, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
RiovanesCastleEntrance = BattleMapping(431, 11, [
    SourceUnit(SpriteSet(SpriteSet.RAFA_GUEST), Job.HEAVEN_KNIGHT_GUEST, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MALAK), Job.HELL_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
InsideofRiovanesCastle = BattleMapping(432, 11, [
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.NONE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ARCHAIC_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.MALE),
    #SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VELIUS), Job.VELIUS, UnitGender.MONSTER),
    #SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.FEMALE),
])
#Used sprite sheets: 6
#===
RooftopofRiovanesCastle = BattleMapping(433, 11, [
    SourceUnit(SpriteSet(SpriteSet.RAFA), Job.HEAVEN_KNIGHT, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    #SourceUnit(SpriteSet(SpriteSet.MALAK_DEAD), Job.MALAK_DEAD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
UndergroundBookStorageFourthFloor = BattleMapping(435, 14, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    #SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
UndergroundBookStorageFifthFloor = BattleMapping(436, 14, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
MurondDeathCity = BattleMapping(438, 14, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SAMURAI, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.KLETIAN), Job.SORCERER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.TIMEMAGE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
LostSacredPrecincts = BattleMapping(439, 14, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.TIAMAT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.DARK_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BALK), Job.ENGINEER_BALK, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
GraveyardofAirships1 = BattleMapping(440, 14, [
    SourceUnit(SpriteSet(SpriteSet.ALMA_DEAD), Job.ALMA_DEAD, UnitGender.FEMALE),
    #SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.HASHMALUM), Job.HASHMALUM, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.AJORA), Job.ALMA_DEAD, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
GraveyardofAirships2 = BattleMapping(441, 14, [
    SourceUnit(SpriteSet(SpriteSet.ALTIMA_2), Job.ALTIMA_2, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALTIMA_1), Job.ALTIMA_1, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.AJORA), Job.AJORA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ULTIMA_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALMA_GOA), Job.ALMA_INITIAL_DEAD, UnitGender.FEMALE),
])
#Used sprite sheets: 5
#===
DoguolaPass = BattleMapping(442, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BerveniaFreeCity = BattleMapping(443, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.SUMMONER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.ARCHER, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MELIADOUL_ENEMY), Job.DIVINE_KNIGHT_MELIADOUL_ENEMY, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_FEMALE), Job.NINJA, UnitGender.FEMALE),
])
#Used sprite sheets: 4
#===
FinathRiver = BattleMapping(444, 12, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.YELLOW_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLACK_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.RED_CHOCOBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.URIBO, UnitGender.MONSTER),
])
#Used sprite sheets: 2
#===
ZalmoII = BattleMapping(445, 12, [
    SourceUnit(SpriteSet(SpriteSet.DELITA_C2), Job.HOLY_KNIGHT_DELITA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ZALMO), Job.HOLY_PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ORACLE, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BalkI = BattleMapping(447, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BALK), Job.ENGINEER_BALK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
SouthWallofBethlaGarrison = BattleMapping(448, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
NorthWallofBethlaGarrison = BattleMapping(449, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MONK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.LANCER, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
BethlaSluice = BattleMapping(450, 12, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.WIZARD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 3
#===
GerminasPeak = BattleMapping(452, 13, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.NINJA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.ARCHER, UnitGender.MALE),
])
#Used sprite sheets: 3
#===
PoeskasLake = BattleMapping(453, 13, [
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_SUMMONER), Job.SUMMONER_UNDEAD, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.REVNANT, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_ORACLE), Job.ORACLE_UNDEAD, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_ARCHER), Job.ARCHER_UNDEAD, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
OutsideofLimberryCastle = BattleMapping(454, 13, [
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.APANDA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
])
#Used sprite sheets: 3
#===
ElmdorII = BattleMapping(456, 13, [
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ULTIMA_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
Zalera = BattleMapping(457, 13, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BONE_SNATCH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.LIVING_BONE, UnitGender.MONSTER),
    #SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.UNDEAD_KNIGHT), Job.KNIGHT_UNDEAD, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.SKELETON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MELIADOUL), Job.DIVINE_KNIGHT_MELIADOUL, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ZALERA), Job.ZALERA, UnitGender.MALE),
])
#Used sprite sheets: 5
#===
Adramelk = BattleMapping(459, 14, [
    SourceUnit(SpriteSet(SpriteSet.ZALBAG), Job.ARC_KNIGHT_ZALBAG, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DYCEDARG), Job.LUNE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ADRAMELK), Job.ADRAMELK, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
StMurondTemple = BattleMapping(460, 14, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.SUMMONER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.GEOMANCER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.MEDIATOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.PRIEST, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
HallofStMurondTemple = BattleMapping(461, 14, [
    SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.KLETIAN), Job.SORCERER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
])
#Used sprite sheets: 3
#===
ChapelofStMurondTemple = BattleMapping(462, 14, [
    SourceUnit(SpriteSet(SpriteSet.ZALBAG_ZOMBIE), Job.ARC_KNIGHT_ZOMBIE, UnitGender.MALE),
    #SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ARCHAIC_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ULTIMA_DEMON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
CollieryUndergroundThirdFloor = BattleMapping(463, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
])
#Used sprite sheets: 2
#===
CollieryUndergroundSecondFloor = BattleMapping(464, 8, [
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.KING_BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BEHEMOTH, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.THIEF, UnitGender.MALE),
])
#Used sprite sheets: 4
#===
CollieryUndergroundFirstFloor = BattleMapping(465, 8, [
    SourceUnit(SpriteSet(SpriteSet.GENERIC_MALE), Job.CHEMIST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.URIBO, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.BLUE_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 4
#===
UndergroundPassageinGoland = BattleMapping(466, 8, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.OCHU, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ARCHAIC_DEMON, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.BEOWULF), Job.TEMPLE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.PLAGUE, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.HOLY_DRAGON), Job.HOLY_DRAGON, UnitGender.MONSTER),
])
#Used sprite sheets: 5
#===
NelveskaTemple = BattleMapping(468, 12, [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.GOBLIN, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.HYUDRA, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.COCATORIS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_GIANT, UnitGender.MONSTER),
])
#Used sprite sheets: 4


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