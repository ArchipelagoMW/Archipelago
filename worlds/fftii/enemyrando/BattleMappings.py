from .EventCodes import EventCode
from .Job import Job
from .RandomizedUnitFactory import RandomizedUnitFactory
from .SourceUnit import SourceUnit
from .SpriteSet import SpriteSet
from worlds.fftii.patchersuite.Unit import UnitGender


class BattleMapping:
    name: str
    battle_id: EventCode
    battle_level: int
    source_units = []
    unit_mapping: dict[SourceUnit, RandomizedUnitFactory]

    def __init__(self, battle_id: int, battle_level: int, source_units):
        self.battle_id = EventCode(battle_id)
        self.battle_level = battle_level
        self.source_units = source_units

    def __copy__(self):
        raise NotImplementedError

    def __deepcopy__(self, memo):
        copied_object = BattleMapping(self.battle_id, self.battle_level, self.source_units.copy())
        copied_object.name = self.name
        return copied_object

story_shuffle_source_units: list[SourceUnit] = [
    SourceUnit(SpriteSet(SpriteSet.ALGUS), Job.KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF1), Job.WHITE_KNIGHT_C1, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION_ENEMY), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.GAFGARION_ENEMY), Job.DARK_KNIGHT_ENEMY, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ZALMO), Job.HOLY_PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.IZLUDE), Job.KNIGHT_BLADE, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MALAK), Job.HELL_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MALAK), Job.HELL_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.WIEGRAF2), Job.WHITE_KNIGHT_C3, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.KLETIAN), Job.SORCERER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BALK), Job.ENGINEER_BALK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.MELIADOUL_ENEMY), Job.DIVINE_KNIGHT_MELIADOUL_ENEMY, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ZALMO), Job.HOLY_PRIEST, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.BALK), Job.ENGINEER_BALK, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.CELIA), Job.ASSASSIN_CELIA, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.LEDE), Job.ASSASSIN_LEDE, UnitGender.FEMALE),
    SourceUnit(SpriteSet(SpriteSet.ELMDOR), Job.ARC_KNIGHT_ELMDOR, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.DYCEDARG), Job.LUNE_KNIGHT, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ROFEL), Job.DIVINE_KNIGHT_ROFEL, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.KLETIAN), Job.SORCERER, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VORMAV), Job.DIVINE_KNIGHT_VORMAV, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ZALBAG_ZOMBIE), Job.ARC_KNIGHT_ZOMBIE, UnitGender.MALE)
]

sidequest_shuffle_source_units: list[SourceUnit] = [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.STEEL_GIANT, UnitGender.MONSTER)
]

zodiac_shuffle_source_units: list[SourceUnit] = [
    SourceUnit(SpriteSet(SpriteSet.QUEKLAIN), Job.QUEKLAIN, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.VELIUS), Job.VELIUS, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.HASHMALUM), Job.HASHMALUM, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ZALERA), Job.ZALERA, UnitGender.MALE),
    SourceUnit(SpriteSet(SpriteSet.ADRAMELK), Job.ADRAMELK, UnitGender.MONSTER)
]

zodiac_sidequest_source_units: list[SourceUnit] = [
    SourceUnit(SpriteSet(SpriteSet.MONSTER), Job.ELIDIBS, UnitGender.MONSTER)
]

altima_source_units: list[SourceUnit] = [
    SourceUnit(SpriteSet(SpriteSet.ALTIMA_2), Job.ALTIMA_2, UnitGender.MONSTER),
    SourceUnit(SpriteSet(SpriteSet.ALTIMA_1), Job.ALTIMA_1, UnitGender.MONSTER)
]

valid_shuffle_source_units: list[SourceUnit] = [
    *story_shuffle_source_units
]