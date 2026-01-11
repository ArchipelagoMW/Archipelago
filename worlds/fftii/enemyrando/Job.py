from enum import Enum, IntEnum, unique


@unique
class Job(IntEnum):
    RAMZA_SQUIRE_CHAPTER_1 = 0x01
    RAMZA_SQUIRE_CHAPTER_23 = 0x02
    RAMZA_SQUIRE_CHAPTER_4 = 0x03
    SQUIRE_DELITA = 0x04
    HOLY_KNIGHT_DELITA = 0x05
    ARC_KNIGHT_DELITA = 0x06
    SQUIRE_ALGUS = 0x07
    ARC_KNIGHT_ZALBAG = 0x08
    LUNE_KNIGHT = 0x09
    PRINCESS = 0x0C
    HOLY_SWORDSMAN = 0x0D
    DRAGONER = 0x0F
    HOLY_PRIEST = 0x10
    DARK_KNIGHT_ENEMY = 0x11
    MALAK_DEAD = 0x12
    ALMA_INITIAL_DEAD = 0x14
    ASTROLOGIST = 0x15
    ENGINEER_MUSTADIO = 0x16
    DARK_KNIGHT_GUEST = 0x17
    DRACLAU = 0x18
    HEAVEN_KNIGHT_GUEST = 0x19
    HELL_KNIGHT = 0x1A
    ARC_KNIGHT_ELMDOR = 0x1B
    TETA = 0x1C
    HOLY_KNIGHT_AGRIAS = 0x1E
    TEMPLE_KNIGHT = 0x1F
    WHITE_KNIGHT_C1 = 0x20
    ENGINEER_GUEST = 0x22
    RUDVICH = 0x23
    DIVINE_KNIGHT_VORMAV = 0x24
    DIVINE_KNIGHT_ROFEL = 0x25
    KNIGHT_BLADE = 0x26
    SORCERER = 0x27
    WHITE_KNIGHT_C3 = 0x28
    HEAVEN_KNIGHT = 0x29
    DIVINE_KNIGHT_MELIADOUL = 0x2A
    ENGINEER_BALK = 0x2B
    ALMA_DEAD = 0x2C
    ASSASSIN_CELIA = 0x2D
    ASSASSIN_LEDE = 0x2E
    DIVINE_KNIGHT_MELIADOUL_ENEMY = 0x2F
    CLERIC = 0x30
    AJORA = 0x31
    SOLDIER = 0x32
    ARC_KNIGHT_ZOMBIE = 0x33
    HOLY_KNIGHT_AGRIAS_GUEST = 0x34
    KNIGHT_UNDEAD = 0x3D
    ARCHER_UNDEAD = 0x3F
    ALTIMA_1 = 0x41
    WIZARD_UNDEAD = 0x42
    TIME_MAGE_UNDEAD = 0x44
    ORACLE_UNDEAD = 0x46
    SUMMONER_UNDEAD = 0x47
    ALTIMA_2 = 0x49

    SQUIRE = 0x4A
    CHEMIST = 0x4B
    KNIGHT = 0x4C
    ARCHER = 0x4D
    MONK = 0x4E
    PRIEST = 0x4F
    WIZARD = 0x50
    TIMEMAGE = 0x51
    SUMMONER = 0x52
    THIEF = 0x53
    MEDIATOR = 0x54
    ORACLE = 0x55
    GEOMANCER = 0x56
    LANCER = 0x57
    SAMURAI = 0x58
    NINJA = 0x59
    CALCULATOR = 0x5A
    BARD = 0x5B
    DANCER = 0x5C
    MIME = 0x5D

    YELLOW_CHOCOBO = 0x5E
    BLACK_CHOCOBO = 0x5F
    RED_CHOCOBO = 0x60
    GOBLIN = 0x61
    BLACK_GOBLIN = 0x62
    GOBBLEDEGUCK = 0x63
    BOMB = 0x64
    GRENADE = 0x65
    EXPLOSIVE = 0x66
    RED_PANTHER = 0x67
    CUAR = 0x68
    VAMPIRE = 0x69
    PISCO_DEMON = 0x6A
    SQUIDLARKIN = 0x6B
    MINDFLARE = 0x6C
    SKELETON = 0x6D
    BONE_SNATCH = 0x6E
    LIVING_BONE = 0x6F
    GHOUL = 0x70
    GUST = 0x71
    REVNANT = 0x72
    FLOTIBALL = 0x73
    AHRIMAN = 0x74
    PLAGUE = 0x75
    JURAVIS = 0x76
    STEEL_HAWK = 0x77
    COCATORIS = 0x78
    URIBO = 0x79
    PORKY = 0x7A
    WILDBOW = 0x7B
    WOODMAN = 0x7C
    TRENT = 0x7D
    TAIJU = 0x7E
    BULL_DEMON = 0x7F
    MINITAURUS = 0x80
    SACRED = 0x81
    MORBOL = 0x82
    OCHU = 0x83
    GREAT_MORBOL = 0x84
    BEHEMOTH = 0x85
    KING_BEHEMOTH = 0x86
    DARK_BEHEMOTH = 0x87
    DRAGON = 0x88
    BLUE_DRAGON = 0x89
    RED_DRAGON = 0x8A
    HYUDRA = 0x8B
    HYDRA = 0x8C
    TIAMAT = 0x8D

    HOLY_DRAGON = 0x48
    BYBLOS = 0x90
    STEEL_GIANT = 0x91
    APANDA = 0x96
    ARCHAIC_DEMON = 0x99
    ULTIMA_DEMON = 0x9A

    VELIUS = 0x3C
    ZALERA = 0x3E
    HASHMALUM = 0x40
    QUEKLAIN = 0x43
    ADRAMELK = 0x45
    ELIDIBS = 0x97

monster_families = {
    Job.YELLOW_CHOCOBO: [Job.YELLOW_CHOCOBO, Job.BLACK_CHOCOBO, Job.RED_CHOCOBO],
    Job.BLACK_CHOCOBO: [Job.YELLOW_CHOCOBO, Job.BLACK_CHOCOBO, Job.RED_CHOCOBO],
    Job.RED_CHOCOBO: [Job.YELLOW_CHOCOBO, Job.BLACK_CHOCOBO, Job.RED_CHOCOBO],
    Job.GOBLIN: [Job.GOBLIN, Job.BLACK_GOBLIN, Job.GOBBLEDEGUCK],
    Job.BLACK_GOBLIN: [Job.GOBLIN, Job.BLACK_GOBLIN, Job.GOBBLEDEGUCK],
    Job.GOBBLEDEGUCK: [Job.GOBLIN, Job.BLACK_GOBLIN, Job.GOBBLEDEGUCK],
    Job.BOMB: [Job.BOMB, Job.GRENADE, Job.EXPLOSIVE],
    Job.GRENADE: [Job.BOMB, Job.GRENADE, Job.EXPLOSIVE],
    Job.EXPLOSIVE: [Job.BOMB, Job.GRENADE, Job.EXPLOSIVE],
    Job.RED_PANTHER: [Job.RED_PANTHER, Job.CUAR, Job.VAMPIRE],
    Job.CUAR: [Job.RED_PANTHER, Job.CUAR, Job.VAMPIRE],
    Job.VAMPIRE: [Job.RED_PANTHER, Job.CUAR, Job.VAMPIRE],
    Job.PISCO_DEMON: [Job.PISCO_DEMON, Job.SQUIDLARKIN, Job.MINDFLARE],
    Job.SQUIDLARKIN: [Job.PISCO_DEMON, Job.SQUIDLARKIN, Job.MINDFLARE],
    Job.MINDFLARE: [Job.PISCO_DEMON, Job.SQUIDLARKIN, Job.MINDFLARE],
    Job.SKELETON: [Job.SKELETON, Job.BONE_SNATCH, Job.LIVING_BONE],
    Job.BONE_SNATCH: [Job.SKELETON, Job.BONE_SNATCH, Job.LIVING_BONE],
    Job.LIVING_BONE: [Job.SKELETON, Job.BONE_SNATCH, Job.LIVING_BONE],
    Job.GHOUL: [Job.GHOUL, Job.GUST, Job.REVNANT],
    Job.GUST: [Job.GHOUL, Job.GUST, Job.REVNANT],
    Job.REVNANT: [Job.GHOUL, Job.GUST, Job.REVNANT],
    Job.FLOTIBALL: [Job.FLOTIBALL, Job.AHRIMAN, Job.PLAGUE],
    Job.AHRIMAN: [Job.FLOTIBALL, Job.AHRIMAN, Job.PLAGUE],
    Job.PLAGUE: [Job.FLOTIBALL, Job.AHRIMAN, Job.PLAGUE],
    Job.JURAVIS: [Job.JURAVIS, Job.STEEL_HAWK, Job.COCATORIS],
    Job.STEEL_HAWK: [Job.JURAVIS, Job.STEEL_HAWK, Job.COCATORIS],
    Job.COCATORIS: [Job.JURAVIS, Job.STEEL_HAWK, Job.COCATORIS],
    Job.URIBO: [Job.URIBO, Job.PORKY, Job.WILDBOW],
    Job.PORKY: [Job.URIBO, Job.PORKY, Job.WILDBOW],
    Job.WILDBOW: [Job.URIBO, Job.PORKY, Job.WILDBOW],
    Job.WOODMAN: [Job.WOODMAN, Job.TRENT, Job.TAIJU],
    Job.TRENT: [Job.WOODMAN, Job.TRENT, Job.TAIJU],
    Job.TAIJU: [Job.WOODMAN, Job.TRENT, Job.TAIJU],
    Job.BULL_DEMON: [Job.BULL_DEMON, Job.MINITAURUS, Job.SACRED],
    Job.MINITAURUS: [Job.BULL_DEMON, Job.MINITAURUS, Job.SACRED],
    Job.SACRED: [Job.BULL_DEMON, Job.MINITAURUS, Job.SACRED],
    Job.MORBOL: [Job.MORBOL, Job.OCHU, Job.GREAT_MORBOL],
    Job.OCHU: [Job.MORBOL, Job.OCHU, Job.GREAT_MORBOL],
    Job.GREAT_MORBOL: [Job.MORBOL, Job.OCHU, Job.GREAT_MORBOL],
    Job.BEHEMOTH: [Job.BEHEMOTH, Job.KING_BEHEMOTH, Job.DARK_BEHEMOTH],
    Job.KING_BEHEMOTH: [Job.BEHEMOTH, Job.KING_BEHEMOTH, Job.DARK_BEHEMOTH],
    Job.DARK_BEHEMOTH: [Job.BEHEMOTH, Job.KING_BEHEMOTH, Job.DARK_BEHEMOTH],
    Job.DRAGON: [Job.DRAGON, Job.BLUE_DRAGON, Job.RED_DRAGON],
    Job.BLUE_DRAGON: [Job.DRAGON, Job.BLUE_DRAGON, Job.RED_DRAGON],
    Job.RED_DRAGON: [Job.DRAGON, Job.BLUE_DRAGON, Job.RED_DRAGON],
    Job.HYUDRA: [Job.HYUDRA, Job.HYDRA, Job.TIAMAT],
    Job.HYDRA: [Job.HYUDRA, Job.HYDRA, Job.TIAMAT],
    Job.TIAMAT: [Job.HYUDRA, Job.HYDRA, Job.TIAMAT]
}

special_character_jobs = {
    0x01: "Ramza Squire (Chapter 1)",
    0x02: "Ramza Squire (Chapter 2-3)",
    0x03: "Ramza Squire (Chapter 4)",
    0x04: "Squire (Delita)",
    0x05: "Holy Knight (Delita)",
    0x06: "Arc Knight (Delita)",
    0x07: "Squire (Algus)",
    0x08: "Arc Knight (Zalbag)",
    0x09: "Lune Knight",
    0x0C: "Princess",
    0x0D: "Holy Swordsman",
    0x0F: "Dragoner",
    0x10: "Holy Priest",
    0x11: "Dark Knight (Enemy)",
    0x12: "Malak (Dead)",
    0x14: "Alma (Initial Dead)",
    0x15: "Astrologist",
    0x16: "Engineer (Mustadio)",
    0x17: "Dark Knight (Guest)",
    0x18: "Draclau",
    0x19: "Heaven Knight (Guest)",
    0x1A: "Hell Knight",
    0x1B: "Arc Knight (Elmdor)",
    0x1C: "Teta",
    0x1E: "Holy Knight (Agrias)",
    0x1F: "Temple Knight",
    0x20: "White Knight (Wiegraf, Chapter 1)",
    0x22: "Engineer (Mustadio, Guest))",
    0x23: "Rudvich",
    0x24: "Divine Knight (Vormav)",
    0x25: "Divine Knight (Rofel)",
    0x26: "Knight Blade",
    0x27: "Sorcerer",
    0x28: "White Knight (Wiegraf, Chapter 3)",
    0x29: "Heaven Knight",
    0x2A: "Divine Knight (Meliadoul)",
    0x2B: "Engineer (Balk)",
    0x2C: "Alma (Dead)",
    0x2D: "Assassin (Celia)",
    0x2E: "Assassin (Lede)",
    0x2F: "Divine Knight (Meliadoul, Enemy)",
    0x30: "Cleric",
    0x31: "Ajora",
    0x32: "Soldier",
    0x33: "Arc Knight (Zombie)",
    0x34: "Holy Knight (Agrias, Guest)",
    0x3D: "Knight (Undead)",
    0x3F: "Archer (Undead)",
    0x41: "Altima 1",
    0x42: "Wizard (Undead)",
    0x44: "Time Mage (Undead)",
    0x46: "Oracle (Undead)",
    0x47: "Summoner (Undead)",
    0x49: "Altima 2"
}

generic_jobs = {
    0x4A: "Squire",
    0x4B: "Chemist",
    0x4C: "Knight",
    0x4D: "Archer",
    0x4E: "Monk",
    0x4F: "Priest",
    0x50: "Wizard",
    0x51: "Time Mage",
    0x52: "Summoner",
    0x53: "Thief",
    0x54: "Mediator",
    0x55: "Oracle",
    0x56: "Geomancer",
    0x57: "Lancer",
    0x58: "Samurai",
    0x59: "Ninja",
    0x5A: "Calculator",
    0x5B: "Bard",
    0x5C: "Dancer",
    0x5D: "Mime"
}

generic_monster_jobs = {
    0x5E: "Yellow Chocobo",
    0x5F: "Black Chocobo",
    0x60: "Red Chocobo",
    0x61: "Goblin",
    0x62: "Black Goblin",
    0x63: "Gobbledeguck",
    0x64: "Bomb",
    0x65: "Grenade",
    0x66: "Explosive",
    0x67: "Red Panther",
    0x68: "Cuar",
    0x69: "Vampire",
    0x6A: "Pisco Demon",
    0x6B: "Squidlarkin",
    0x6C: "Mindflare",
    0x6D: "Skeleton",
    0x6E: "Bone Snatch",
    0x6F: "Living Bone",
    0x70: "Ghoul",
    0x71: "Gust",
    0x72: "Revnant",
    0x73: "Flotiball",
    0x74: "Ahriman",
    0x75: "Plague",
    0x76: "Juravis",
    0x77: "Steel Hawk",
    0x78: "Cocatoris",
    0x79: "Uribo",
    0x7A: "Porky",
    0x7B: "Wildbow",
    0x7C: "Woodman",
    0x7D: "Trent",
    0x7E: "Taiju",
    0x7F: "Bull Demon",
    0x80: "Minitaurus",
    0x81: "Sacred",
    0x82: "Morbol",
    0x83: "Ochu",
    0x84: "Great Morbol",
    0x85: "Behemoth",
    0x86: "King Behemoth",
    0x87: "Dark Behemoth",
    0x88: "Dragon",
    0x89: "Blue Dragon",
    0x8A: "Red Dragon",
    0x8B: "Hyudra",
    0x8C: "Hydra",
    0x8D: "Tiamat"
}

special_monster_jobs = {
    0x48: "Holy Dragon",
    0x90: "Byblos",
    0x91: "Steel Giant",
    0x96: "Apanda",
    0x99: "Archaic Demon",
    0x9A: "Ultima Demon"

}

lucavi_jobs = {
    0x3C: "Warlock (Velius)",
    0x3E: "Angel of Death (Zalera)",
    0x40: "Regulator (Hashmalum)",
    0x43: "Impure King (Queklain)",
    0x45: "Ghost of Fury (Adramelk)",
    0x97: "Serpentarius (Elidibs)"
}

all_jobs = {
    **special_character_jobs,
    **generic_jobs,
    **generic_monster_jobs,
    **special_monster_jobs,
    **lucavi_jobs
}

@unique
class UnlockedJob(Enum):
    BASE = 0x00
    CHEMIST = 0x01
    KNIGHT = 0x02
    ARCHER = 0x03
    MONK = 0x04
    PRIEST = 0x05
    WIZARD = 0x06
    TIMEMAGE = 0x07
    SUMMONER = 0x08
    THIEF = 0x09
    MEDIATOR = 0x0A
    ORACLE = 0x0B
    GEOMANCER = 0x0C
    LANCER = 0x0D
    SAMURAI = 0x0E
    NINJA = 0x0F
    CALCULATOR = 0x10
    BARD = 0x11
    DANCER = 0x12
    MIME = 0x13