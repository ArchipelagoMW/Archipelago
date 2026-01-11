from enum import Enum, unique


@unique
class Items(Enum):
    NONE = 0xFF
    RANDOM = 0xFE

    BLOOD_SWORD = 0x17
    SAVE_THE_QUEEN = 0x22
    EXCALIBUR = 0x23
    MASAMUNE = 0x2E
    MACE_OF_ZEUS = 0x41
    BLAST_GUN = 0x4C
    BLAZE_GUN = 0x4A
    GENJI_SHIELD = 0x8C
    GENJI_HELMET = 0x9B
    THIEF_HAT = 0xA8
    CACHUSHA = 0xA9
    BARETTE = 0xAA
    GENJI_ARMOR = 0xB7
    WHITE_ROBE = 0xCC
    CHANTAGE = 0xEC
    GENJI_GAUNTLET = 0xD8