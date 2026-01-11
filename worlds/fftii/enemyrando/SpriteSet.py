from enum import Enum, unique


@unique
class SpriteSet(Enum):
    RAMZA_C1 = 0x01
    RAMZA_C23 = 0x02
    RAMZA_C4 = 0x03
    DELITA_C1 = 0x04
    DELITA_C2 = 0x05
    DELITA_C4 = 0x06
    ALGUS = 0x07
    ZALBAG = 0x08
    DYCEDARG = 0x09
    OVELIA = 0x0C
    ORLANDU = 0x0D
    REIS = 0x0F
    ZALMO = 0x10
    GAFGARION_ENEMY = 0x11
    MALAK_DEAD = 0x12
    ALMA_GOA = 0x14
    OLAN = 0x15
    MUSTADIO = 0x16
    GAFGARION = 0x17
    DRACLAU = 0x18
    RAFA_GUEST = 0x19
    MALAK = 0x1A
    ELMDOR = 0x1B
    TETA = 0x1C
    AGRIAS = 0x1E
    BEOWULF = 0x1F
    WIEGRAF1 = 0x20
    MUSTADIO_GUEST = 0x22
    RUDVICH = 0x23
    VORMAV = 0x24
    ROFEL = 0x25
    IZLUDE = 0x26
    KLETIAN = 0x27
    WIEGRAF2 = 0x28
    RAFA = 0x29
    MELIADOUL = 0x2A
    BALK = 0x2B
    ALMA_DEAD = 0x2C
    CELIA = 0x2D
    LEDE = 0x2E
    MELIADOUL_ENEMY = 0x2F
    ALMA = 0x30
    AJORA = 0x31
    CLOUD = 0x32
    ZALBAG_ZOMBIE = 0x33
    AGRIAS_GUEST = 0x34
    VELIUS = 0x3C
    UNDEAD_KNIGHT = 0x3D
    ZALERA = 0x3E
    UNDEAD_ARCHER = 0x3F
    HASHMALUM = 0x40
    ALTIMA_1 = 0x41
    UNDEAD_WIZARD = 0x42
    QUEKLAIN = 0x43
    UNDEAD_TIMEMAGE = 0x44
    ADRAMELK = 0x45
    UNDEAD_ORACLE = 0x46
    UNDEAD_SUMMONER = 0x47
    HOLY_DRAGON = 0x48
    ALTIMA_2 = 0x49
    GENERIC_MALE = 0x80
    GENERIC_FEMALE = 0x81
    MONSTER = 0x82

sprite_sets = {
    0x01: "Ramza",
    0x02: "Ramza",
    0x03: "Ramza",
    0x04: "Delita",
    0x05: "Delita",
    0x06: "Delita",
    0x07: "Algus",
    0x08: "Zalbag",
    0x09: "Dycedarg",
    0x0A: "Larg",
    0x0B: "Goltana",
    0x0C: "Ovelia",
    0x0D: "Orlandu",
    0x0E: "High Priest",
    0x0F: "Reis",
    0x10: "Zalmo",
    0x11: "Gafgarion",
    0x12: "Malak",
    0x13: "Simon",
    0x14: "Alma",
    0x15: "Olan",
    0x16: "Mustadio",
    0x17: "Gafgarion",
    0x18: "Draclau",
    0x19: "Rafa",
    0x1A: "Malak",
    0x1B: "Elmdor",
    0x1C: "Teta",
    0x1D: "Barinten",
    0x1E: "Agrias",
    0x1F: "Beowulf",
    0x20: "Wiegraf",
    0x21: "Balmafula",
    0x22: "Mustadio",
    0x23: "Rudvich",
    0x24: "Vormav",
    0x25: "Rofel",
    0x26: "Izlude",
    0x27: "Kletian",
    0x28: "Wiegraf",
    0x29: "Rafa",
    0x2A: "Meliadoul",
    0x2B: "Balk",
    0x2C: "Alma",
    0x2D: "Celia",
    0x2E: "Lede",
    0x2F: "Meliadoul",
    0x30: "Alma",
    0x31: "Ajora",
    0x32: "Cloud",
    0x33: "Zalbag",
    0x34: "Agrias",

    0x3C: "Velius",
    0x3D: "Undead Knight",
    0x3E: "Zalera",

    0x40: "Hashmalum",
    0x41: "Altima",

    0x43: "Queklain",

    0x45: "Adramelk",

    0x48: "Holy Dragon",
    0x49: "Altima",

    0x80: "Generic Male",
    0x81: "Generic Female",
    0x82: "Monster"
}