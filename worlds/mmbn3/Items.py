import typing

from enum import IntEnum, Enum
from BaseClasses import Item, ItemClassification
from .Names.ItemName import ItemName


class ItemType(str, Enum):
    Undernet = "undernet"
    Chip = "chip"
    KeyItem = "key"
    SubChip = "subchip"
    Zenny = "zenny"
    Program = "program"
    BugFrag = "bugfrag"
    External = "External"

    __str__ = str.__str__

class ProgramColor(IntEnum):
    White = 1
    Pink = 2
    Yellow = 3
    Red = 4
    Blue = 5
    Green = 6
    Orange = 7
    Purple = 8
    Dark = 9


def chip_code(c):
    if c == '*':
        return 26
    return ord(c) - ord('A')


class ItemData(typing.NamedTuple):
    code: int
    itemName: str
    progression: ItemClassification
    type: ItemType
    itemID: int = 0x00
    subItemID: int = 0x00
    count: int = 1
    recipient: str = "Myself"


class MMBN3Item(Item):
    game: str = "MegaMan Battle Network 3"
    

keyItemList: typing.List[ItemData] = [
    ItemData(0xB31000, ItemName.Progressive_Undernet_Rank, ItemClassification.progression_skip_balancing, ItemType.Undernet, 27),
    ItemData(0xB31001, ItemName.CACDCPas,                  ItemClassification.progression, ItemType.KeyItem,  92),
    ItemData(0xB31002, ItemName.CSciPas,                   ItemClassification.progression, ItemType.KeyItem,  93),
    ItemData(0xB31003, ItemName.CYokaPas,                  ItemClassification.progression, ItemType.KeyItem,  94),
    ItemData(0xB31004, ItemName.CBeacPas,                  ItemClassification.progression, ItemType.KeyItem,  95),
    ItemData(0xB31005, ItemName.WWW_ID,                    ItemClassification.progression, ItemType.KeyItem,  47),
    ItemData(0xB31006, ItemName.OrderSys,                  ItemClassification.useful,      ItemType.KeyItem,  12),
    ItemData(0xB31007, ItemName.ModTools,                  ItemClassification.useful,      ItemType.KeyItem,  55),
    ItemData(0xB31008, ItemName.ExpMem,                    ItemClassification.useful,      ItemType.KeyItem,  97),
    ItemData(0xB31009, ItemName.SpinWht,                   ItemClassification.useful,      ItemType.KeyItem,  71),
    ItemData(0xB3100A, ItemName.SpinPink,                  ItemClassification.useful,      ItemType.KeyItem,  72),
    ItemData(0xB3100B, ItemName.SpinYllw,                  ItemClassification.useful,      ItemType.KeyItem,  73),
    ItemData(0xB3100C, ItemName.SpinRed,                   ItemClassification.useful,      ItemType.KeyItem,  74),
    ItemData(0xB3100D, ItemName.SpinBlue,                  ItemClassification.useful,      ItemType.KeyItem,  75),
    ItemData(0xB3100E, ItemName.SpinGrn,                   ItemClassification.useful,      ItemType.KeyItem,  76),
    ItemData(0xB3100F, ItemName.SpinOrange,                ItemClassification.useful,      ItemType.KeyItem,  77),

    ItemData(0xB31010, ItemName.SpinPurple,                ItemClassification.useful,      ItemType.KeyItem,  78),
    ItemData(0xB31011, ItemName.SpinDark,                  ItemClassification.useful,      ItemType.KeyItem,  79),
    ItemData(0xB31012, ItemName.HPMemory,                  ItemClassification.useful,      ItemType.KeyItem,  96),
    ItemData(0xB31013, ItemName.RegUP1,                    ItemClassification.filler,      ItemType.KeyItem,  98),
    ItemData(0xB31014, ItemName.RegUP2,                    ItemClassification.useful,      ItemType.KeyItem,  99),
    ItemData(0xB31015, ItemName.RegUP3,                    ItemClassification.useful,      ItemType.KeyItem, 100),
    ItemData(0xB31016, ItemName.Mr_Famous_Wristband,       ItemClassification.filler,      ItemType.KeyItem,  57),
    ItemData(0xB31017, ItemName.SubMem,                    ItemClassification.filler,      ItemType.KeyItem, 101),

    ItemData(0xB310B1, ItemName.SubPET, ItemClassification.progression, ItemType.KeyItem, 10),
    ItemData(0xB310B2, ItemName.Needle, ItemClassification.progression, ItemType.KeyItem, 14),
    ItemData(0xB310B3, ItemName.PETCase, ItemClassification.progression, ItemType.KeyItem, 16),
    # ItemData(0xB310B4, ItemName.Parasol, ItemClassification.progression, ItemType.KeyItem, 3),
    ItemData(0xB310DF, ItemName.Hammer, ItemClassification.progression, ItemType.KeyItem, 56)
]

subChipList: typing.List[ItemData] = [
    ItemData(0xB31018, ItemName.Unlocker, ItemClassification.progression, ItemType.SubChip,  117),
    ItemData(0xB31019, ItemName.Untrap,   ItemClassification.filler, ItemType.SubChip,  115),
    ItemData(0xB3101A, ItemName.LockEnmy, ItemClassification.filler, ItemType.SubChip,  116),
    ItemData(0xB3101B, ItemName.MiniEnrg, ItemClassification.filler, ItemType.SubChip,  112),
    ItemData(0xB3101C, ItemName.FullEnrg, ItemClassification.filler, ItemType.SubChip,  113),
    ItemData(0xB3101D, ItemName.SneakRun, ItemClassification.filler, ItemType.SubChip,  114)
]

chipList: typing.List[ItemData] = [
    ItemData(0xB3101E, ItemName.AirShoes_star, ItemClassification.useful, ItemType.Chip, 168, chip_code('*')),
    ItemData(0xB3101F, ItemName.AirShot3_star, ItemClassification.useful, ItemType.Chip, 6, chip_code('*')),

    ItemData(0xB31020, ItemName.AntiNavi_M, ItemClassification.useful, ItemType.Chip, 190, chip_code('M')),
    ItemData(0xB31021, ItemName.AntiRecv_B, ItemClassification.filler, ItemType.Chip, 193, chip_code('B')),
    ItemData(0xB31022, ItemName.AntiSword_Y, ItemClassification.useful, ItemType.Chip, 192, chip_code('Y')),
    ItemData(0xB31023, ItemName.Aqua_plus_30_star, ItemClassification.useful, ItemType.Chip, 197, chip_code('*')),
    ItemData(0xB31024, ItemName.Aura_F, ItemClassification.useful, ItemType.Chip, 176, chip_code('F')),
    ItemData(0xB31025, ItemName.BambooSword_N, ItemClassification.useful, ItemType.Chip, 36, chip_code('N')),
    ItemData(0xB31026, ItemName.Barr100_E, ItemClassification.useful, ItemType.Chip, 174, chip_code('E')),
    ItemData(0xB31027, ItemName.Barr200_E, ItemClassification.useful, ItemType.Chip, 175, chip_code('E')),
    ItemData(0xB31028, ItemName.Barrier_E, ItemClassification.useful, ItemType.Chip, 173, chip_code('E')),
    ItemData(0xB31029, ItemName.Barrier_L, ItemClassification.filler, ItemType.Chip, 173, chip_code('L')),
    ItemData(0xB3102A, ItemName.BlkBomb1_P, ItemClassification.useful, ItemType.Chip, 27, chip_code('P')),
    ItemData(0xB3102B, ItemName.BlkBomb2_S, ItemClassification.useful, ItemType.Chip, 28, chip_code('S')),
    ItemData(0xB3102C, ItemName.Cannon_C, ItemClassification.filler, ItemType.Chip, 1, chip_code('C')),
    ItemData(0xB3102D, ItemName.CopyDmg_star, ItemClassification.filler, ItemType.Chip, 194, chip_code('*')),
    ItemData(0xB3102E, ItemName.CustSwrd_Z, ItemClassification.filler, ItemType.Chip, 37, chip_code('Z')),
    ItemData(0xB3102F, ItemName.DynaWave_V, ItemClassification.progression, ItemType.Chip, 46, chip_code('V')),

    ItemData(0xB31030, ItemName.ElecSwrd_P, ItemClassification.useful, ItemType.Chip, 35, chip_code('P')),
    ItemData(0xB31031, ItemName.Fire_plus_30_star, ItemClassification.filler, ItemType.Chip, 196, chip_code('*')),
    ItemData(0xB31032, ItemName.FireRat_H, ItemClassification.useful, ItemType.Chip, 117, chip_code('H')),
    ItemData(0xB31033, ItemName.FireSwrd_P, ItemClassification.progression, ItemType.Chip, 33, chip_code('P')),
    ItemData(0xB31034, ItemName.FstGauge_star, ItemClassification.useful, ItemType.Chip, 158, chip_code('*')),
    ItemData(0xB31035, ItemName.GaiaBlde_star, ItemClassification.useful, ItemType.Chip, 276, chip_code('*')),
    ItemData(0xB31036, ItemName.Geddon1_star, ItemClassification.filler, ItemType.Chip, 138, chip_code('*')),
    ItemData(0xB31037, ItemName.Geddon1_D, ItemClassification.filler, ItemType.Chip, 138, chip_code('D')),
    ItemData(0xB31038, ItemName.Geddon3_U, ItemClassification.useful, ItemType.Chip, 140, chip_code('U')),
    ItemData(0xB31039, ItemName.Geyser_B, ItemClassification.useful, ItemType.Chip, 107, chip_code('B')),
    ItemData(0xB3103A, ItemName.GrabBack_K, ItemClassification.progression, ItemType.Chip, 136, chip_code('K')),
    ItemData(0xB3103B, ItemName.GrabRvng_A, ItemClassification.filler, ItemType.Chip, 137, chip_code('A')),
    ItemData(0xB3103C, ItemName.GrabRvng_Y, ItemClassification.filler, ItemType.Chip, 137, chip_code('Y')),
    ItemData(0xB3103D, ItemName.GutStrght_S, ItemClassification.useful, ItemType.Chip, 48, chip_code('S')),
    ItemData(0xB3103E, ItemName.Guardian_O, ItemClassification.useful, ItemType.Chip, 203, chip_code('O')),
    ItemData(0xB3103F, ItemName.GutImpact_H, ItemClassification.useful, ItemType.Chip, 49, chip_code('H')),

    ItemData(0xB31040, ItemName.GutImpct_J, ItemClassification.useful, ItemType.Chip, 49, chip_code('J')),
    ItemData(0xB31041, ItemName.GutPunch_E, ItemClassification.filler, ItemType.Chip, 47, chip_code('E')),
    ItemData(0xB31042, ItemName.GutPunch_B, ItemClassification.filler, ItemType.Chip, 47, chip_code('B')),
    ItemData(0xB31043, ItemName.GutStrgt_Q, ItemClassification.useful, ItemType.Chip, 48, chip_code('Q')),
    ItemData(0xB31044, ItemName.Hammer_T, ItemClassification.useful, ItemType.Chip, 64, chip_code('T')),
    ItemData(0xB31045, ItemName.HeatSide_T, ItemClassification.filler, ItemType.Chip, 19, chip_code('T')),
    ItemData(0xB31046, ItemName.HeroSwrd_P, ItemClassification.useful, ItemType.Chip, 207, chip_code('P')),
    ItemData(0xB31047, ItemName.HiCannon_star, ItemClassification.filler, ItemType.Chip, 2, chip_code('*')),
    ItemData(0xB31048, ItemName.Hole_star, ItemClassification.useful, ItemType.Chip, 161, chip_code('*')),
    ItemData(0xB31049, ItemName.IceStage_star, ItemClassification.filler, ItemType.Chip, 180, chip_code('*')),
    ItemData(0xB3104A, ItemName.Invis_star, ItemClassification.useful, ItemType.Chip, 160, chip_code('*')),
    ItemData(0xB3104B, ItemName.Jealousy_J, ItemClassification.filler, ItemType.Chip, 214, chip_code('J')),
    ItemData(0xB3104C, ItemName.Lance_S, ItemClassification.useful, ItemType.Chip, 75, chip_code('S')),
    ItemData(0xB3104D, ItemName.LongSwrd_E, ItemClassification.filler, ItemType.Chip, 32, chip_code('E')),
    ItemData(0xB3104E, ItemName.Magnum1_A, ItemClassification.progression, ItemType.Chip, 81, chip_code('A')),
    ItemData(0xB3104F, ItemName.Muramasa_M, ItemClassification.useful, ItemType.Chip, 202, chip_code('M')),

    ItemData(0xB31050, ItemName.Navi_plus_40_star, ItemClassification.filler, ItemType.Chip, 206, chip_code('*')),
    ItemData(0xB31051, ItemName.Panic_C, ItemClassification.filler, ItemType.Chip, 41, chip_code('C')),
    ItemData(0xB31052, ItemName.PanlOut3_star, ItemClassification.filler, ItemType.Chip, 120, chip_code('*')),
    ItemData(0xB31053, ItemName.Poltergeist_G, ItemClassification.filler, ItemType.Chip, 213, chip_code('G')),
    ItemData(0xB31054, ItemName.Prism_Q, ItemClassification.useful, ItemType.Chip, 142, chip_code('Q')),
    ItemData(0xB31055, ItemName.Recov10_star, ItemClassification.filler, ItemType.Chip, 121, chip_code('*')),
    ItemData(0xB31056, ItemName.Recov120_star, ItemClassification.useful, ItemType.Chip, 125, chip_code('*')),
    ItemData(0xB31057, ItemName.Recov120_O, ItemClassification.filler, ItemType.Chip, 125, chip_code('O')),
    ItemData(0xB31058, ItemName.Recov120_S, ItemClassification.progression, ItemType.Chip, 125, chip_code('S')),
    ItemData(0xB31059, ItemName.Recov150_P, ItemClassification.filler, ItemType.Chip, 126, chip_code('P')),
    ItemData(0xB3105A, ItemName.Recov200_N, ItemClassification.filler, ItemType.Chip, 127, chip_code('N')),
    ItemData(0xB3105B, ItemName.Recov30_star, ItemClassification.progression, ItemType.Chip, 122, chip_code('*')),
    ItemData(0xB3105C, ItemName.Recov300_R, ItemClassification.useful, ItemType.Chip, 128, chip_code('R')),
    ItemData(0xB3105D, ItemName.Recov50_G, ItemClassification.filler, ItemType.Chip, 123, chip_code('G')),
    ItemData(0xB3105E, ItemName.Repair_star, ItemClassification.filler, ItemType.Chip, 159, chip_code('*')),
    ItemData(0xB3105F, ItemName.Repair_A, ItemClassification.filler, ItemType.Chip, 159, chip_code('A')),

    ItemData(0xB31060, ItemName.Rockcube_star, ItemClassification.filler, ItemType.Chip, 141, chip_code('*')),
    ItemData(0xB31061, ItemName.Rook_F, ItemClassification.filler, ItemType.Chip, 153, chip_code('F')),
    ItemData(0xB31062, ItemName.Salamndr_star, ItemClassification.useful, ItemType.Chip, 273, chip_code('*')),
    ItemData(0xB31063, ItemName.SandStage_C, ItemClassification.filler, ItemType.Chip, 182, chip_code('C')),
    ItemData(0xB31064, ItemName.SideGun_S, ItemClassification.filler, ItemType.Chip, 12, chip_code('S')),
    ItemData(0xB31065, ItemName.Slasher_B, ItemClassification.useful, ItemType.Chip, 43, chip_code('B')),
    ItemData(0xB31066, ItemName.SloGauge_star, ItemClassification.filler, ItemType.Chip, 157, chip_code('*')),
    ItemData(0xB31067, ItemName.Snake_D, ItemClassification.useful, ItemType.Chip, 131, chip_code('D')),
    ItemData(0xB31068, ItemName.Snctuary_C, ItemClassification.useful, ItemType.Chip, 184, chip_code('C')),
    ItemData(0xB31069, ItemName.Spreader_star, ItemClassification.useful, ItemType.Chip, 13, chip_code('*')),
    ItemData(0xB3106A, ItemName.Spreader_N, ItemClassification.useful, ItemType.Chip, 13, chip_code('N')),
    ItemData(0xB3106B, ItemName.Spreader_P, ItemClassification.useful, ItemType.Chip, 13, chip_code('P')),
    ItemData(0xB3106C, ItemName.StepCross_Q, ItemClassification.useful, ItemType.Chip, 40, chip_code('Q')),
    ItemData(0xB3106D, ItemName.StepCross_R, ItemClassification.useful, ItemType.Chip, 40, chip_code('R')),
    ItemData(0xB3106E, ItemName.StepSwrd_M, ItemClassification.useful, ItemType.Chip, 39, chip_code('M')),
    ItemData(0xB3106F, ItemName.StepSwrd_N, ItemClassification.useful, ItemType.Chip, 39, chip_code('N')),

    ItemData(0xB31070, ItemName.StepSwrd_O, ItemClassification.useful, ItemType.Chip, 39, chip_code('O')),
    ItemData(0xB31071, ItemName.StepCross_S, ItemClassification.useful, ItemType.Chip, 40, chip_code('S')),
    ItemData(0xB31072, ItemName.Sword_E, ItemClassification.filler, ItemType.Chip, 30, chip_code('E')),
    ItemData(0xB31073, ItemName.Team1_star, ItemClassification.useful, ItemType.Chip, 132, chip_code('*')),
    ItemData(0xB31074, ItemName.Team2_star, ItemClassification.useful, ItemType.Chip, 169, chip_code('*')),
    ItemData(0xB31075, ItemName.Thndrblt_star, ItemClassification.useful, ItemType.Chip, 275, chip_code('*')),
    ItemData(0xB31076, ItemName.Tornado_L, ItemClassification.filler, ItemType.Chip, 65, chip_code('L')),
    ItemData(0xB31077, ItemName.Fountain_star, ItemClassification.useful, ItemType.Chip, 274, chip_code('*')),
    ItemData(0xB31078, ItemName.VarSword_B, ItemClassification.useful, ItemType.Chip, 38, chip_code('B')),
    ItemData(0xB31079, ItemName.VarSword_F, ItemClassification.useful, ItemType.Chip, 38, chip_code('F')),
    ItemData(0xB3107A, ItemName.WideSwrd_C, ItemClassification.progression, ItemType.Chip, 31, chip_code('C')),
    ItemData(0xB3107B, ItemName.WideSwrd_E, ItemClassification.filler, ItemType.Chip, 31, chip_code('E')),
    ItemData(0xB3107C, ItemName.WideSwrd_L, ItemClassification.filler, ItemType.Chip, 31, chip_code('L')),
    ItemData(0xB3107D, ItemName.Yo_Yo1_D, ItemClassification.filler, ItemType.Chip, 69, chip_code('D')),
    ItemData(0xB3107E, ItemName.ZeusHammer_Z, ItemClassification.useful, ItemType.Chip, 208, chip_code('Z')),
    # ItemData(0xB3107F, ItemName.BassGS_X,          ItemClassification.useful,      ItemType.Chip, 312, ChipCode('X')),
    ItemData(0xB3107F, ItemName.Bass_X, ItemClassification.useful, ItemType.Chip, 311, chip_code('X')),

    ItemData(0xB31080, ItemName.DeltaRay_Z, ItemClassification.useful, ItemType.Chip, 302, chip_code('Z')),
    ItemData(0xB31081, ItemName.Punk_P, ItemClassification.useful, ItemType.Chip, 272, chip_code('P')),
    ItemData(0xB31082, ItemName.DarkAura_A, ItemClassification.useful, ItemType.Chip, 309, chip_code('A')),
    ItemData(0xB31083, ItemName.AlphaArm_Omega_V, ItemClassification.useful, ItemType.Chip, 310, chip_code('V')),

    ItemData(0xB310AC, ItemName.SonicWav_W, ItemClassification.progression, ItemType.Chip, 45, chip_code('W')),
    ItemData(0xB310AD, ItemName.Bubbler_C, ItemClassification.progression, ItemType.Chip, 14, chip_code('C')),
    ItemData(0xB310AE, ItemName.Shake1_S, ItemClassification.progression, ItemType.Chip, 110, chip_code('S')),
    ItemData(0xB310AF, ItemName.HoleMetr_H, ItemClassification.progression, ItemType.Chip, 88, chip_code('H')),
    ItemData(0xB310B0, ItemName.Shadow_J, ItemClassification.progression, ItemType.Chip, 165, chip_code('J')),

    ItemData(0xB310B8, ItemName.Roll_R, ItemClassification.filler, ItemType.Chip, 219, chip_code('R')),
    ItemData(0xB310B9, ItemName.RollV2_R, ItemClassification.filler, ItemType.Chip, 220, chip_code('R')),
    ItemData(0xB310BA, ItemName.RollV3_R, ItemClassification.useful, ItemType.Chip, 221, chip_code('R')),

    ItemData(0xB310BB, ItemName.GutsMan_G, ItemClassification.filler, ItemType.Chip, 222, chip_code('G')),
    ItemData(0xB310BC, ItemName.GutsManV2_G, ItemClassification.filler, ItemType.Chip, 223, chip_code('G')),
    ItemData(0xB310BD, ItemName.GutsManV3_G, ItemClassification.useful, ItemType.Chip, 224, chip_code('G')),

    ItemData(0xB310BE, ItemName.ProtoMan_B, ItemClassification.filler, ItemType.Chip, 227, chip_code('B')),
    ItemData(0xB310BF, ItemName.ProtoManV2_B, ItemClassification.filler, ItemType.Chip, 228, chip_code('B')),
    ItemData(0xB310C0, ItemName.ProtoManV3_B, ItemClassification.useful, ItemType.Chip, 229, chip_code('B')),

    ItemData(0xB310C1, ItemName.FlashMan_F, ItemClassification.filler, ItemType.Chip, 232, chip_code('F')),
    ItemData(0xB310C2, ItemName.FlashManV2_F, ItemClassification.filler, ItemType.Chip, 233, chip_code('F')),
    ItemData(0xB310C3, ItemName.FlashManV3_F, ItemClassification.useful, ItemType.Chip, 234, chip_code('F')),

    ItemData(0xB310C4, ItemName.BeastMan_B, ItemClassification.filler, ItemType.Chip, 237, chip_code('B')),
    ItemData(0xB310C5, ItemName.BeastManV2_B, ItemClassification.filler, ItemType.Chip, 238, chip_code('B')),
    ItemData(0xB310C6, ItemName.BeastManV3_B, ItemClassification.useful, ItemType.Chip, 239, chip_code('B')),

    ItemData(0xB310C7, ItemName.BubblMan_B, ItemClassification.filler, ItemType.Chip, 242, chip_code('B')),
    ItemData(0xB310C8, ItemName.BubblManV2_B, ItemClassification.filler, ItemType.Chip, 243, chip_code('B')),
    ItemData(0xB310C9, ItemName.BubblManV3_B, ItemClassification.useful, ItemType.Chip, 244, chip_code('B')),

    ItemData(0xB310CA, ItemName.DesertMan_D, ItemClassification.filler, ItemType.Chip, 247, chip_code('D')),
    ItemData(0xB310CB, ItemName.DesertManV2_D, ItemClassification.filler, ItemType.Chip, 248, chip_code('D')),
    ItemData(0xB310CC, ItemName.DesertManV3_D, ItemClassification.useful, ItemType.Chip, 249, chip_code('D')),

    ItemData(0xB310CD, ItemName.PlantMan_P, ItemClassification.filler, ItemType.Chip, 252, chip_code('P')),
    ItemData(0xB310CE, ItemName.PlantManV2_P, ItemClassification.filler, ItemType.Chip, 253, chip_code('P')),
    ItemData(0xB310CF, ItemName.PlantManV3_P, ItemClassification.useful, ItemType.Chip, 254, chip_code('P')),

    ItemData(0xB310D0, ItemName.FlamMan_F, ItemClassification.filler, ItemType.Chip, 257, chip_code('F')),
    ItemData(0xB310D1, ItemName.FlamManV2_F, ItemClassification.filler, ItemType.Chip, 258, chip_code('F')),
    ItemData(0xB310D2, ItemName.FlamManV3_F, ItemClassification.useful, ItemType.Chip, 259, chip_code('F')),

    ItemData(0xB310D3, ItemName.DrillMan_D, ItemClassification.filler, ItemType.Chip, 262, chip_code('D')),
    ItemData(0xB310D4, ItemName.DrillManV2_D, ItemClassification.filler, ItemType.Chip, 263, chip_code('D')),
    ItemData(0xB310D5, ItemName.DrillManV3_D, ItemClassification.useful, ItemType.Chip, 264, chip_code('D')),

    ItemData(0xB310D6, ItemName.MetalMan_M, ItemClassification.filler, ItemType.Chip, 267, chip_code('M')),
    ItemData(0xB310D7, ItemName.MetalManV2_M, ItemClassification.filler, ItemType.Chip, 268, chip_code('M')),
    ItemData(0xB310D8, ItemName.MetalManV3_M, ItemClassification.useful, ItemType.Chip, 269, chip_code('M')),

    ItemData(0xB310D9, ItemName.KingMan_K, ItemClassification.filler, ItemType.Chip, 277, chip_code('K')),
    ItemData(0xB310DA, ItemName.KingManV2_K, ItemClassification.filler, ItemType.Chip, 278, chip_code('K')),
    ItemData(0xB310DB, ItemName.KingManV3_K, ItemClassification.useful, ItemType.Chip, 279, chip_code('K')),

    ItemData(0xB310DC, ItemName.BowlMan_B, ItemClassification.filler, ItemType.Chip, 287, chip_code('B')),
    ItemData(0xB310DD, ItemName.BowlManV2_B, ItemClassification.filler, ItemType.Chip, 288, chip_code('B')),
    ItemData(0xB310DE, ItemName.BowlManV3_B, ItemClassification.useful, ItemType.Chip, 289, chip_code('B')),
]

programList: typing.List[ItemData] = [
    ItemData(0xB31084, ItemName.Airshoes,          ItemClassification.useful, ItemType.Program, 29, ProgramColor.White),
    ItemData(0xB31085, ItemName.Attack_plus_White, ItemClassification.filler, ItemType.Program, 41, ProgramColor.White),
    ItemData(0xB31086, ItemName.Attack_plus_Pink,  ItemClassification.filler, ItemType.Program, 41, ProgramColor.Pink),
    ItemData(0xB31087, ItemName.BrkChrg,           ItemClassification.useful, ItemType.Program,  3, ProgramColor.Orange),
    ItemData(0xB31088, ItemName.Charge_plus_Pink,  ItemClassification.filler, ItemType.Program, 43, ProgramColor.Pink),
    ItemData(0xB31089, ItemName.Charge_plus_White, ItemClassification.filler, ItemType.Program, 43, ProgramColor.White),
    ItemData(0xB3108A, ItemName.Collect,           ItemClassification.useful, ItemType.Program, 28, ProgramColor.Pink),
    ItemData(0xB3108B, ItemName.GigFldr1,          ItemClassification.useful, ItemType.Program, 48, ProgramColor.Purple),
    ItemData(0xB3108C, ItemName.HP_100_Pink,       ItemClassification.filler, ItemType.Program, 36, ProgramColor.Pink),
    ItemData(0xB3108D, ItemName.HP_100_Yellow,     ItemClassification.filler, ItemType.Program, 36, ProgramColor.Yellow),
    ItemData(0xB3108E, ItemName.HP_200_Yellow,     ItemClassification.useful, ItemType.Program, 37, ProgramColor.Yellow),
    ItemData(0xB3108F, ItemName.HP_500_Yellow,     ItemClassification.useful, ItemType.Program, 39, ProgramColor.Yellow),

    ItemData(0xB31090, ItemName.HubBatc,           ItemClassification.useful, ItemType.Program, 49, ProgramColor.Orange),
    ItemData(0xB31091, ItemName.Jungle,            ItemClassification.useful, ItemType.Program, 27, ProgramColor.White),
    ItemData(0xB31092, ItemName.OilBody,           ItemClassification.useful, ItemType.Program, 24, ProgramColor.Yellow),
    ItemData(0xB31093, ItemName.QuickGge,          ItemClassification.useful, ItemType.Program, 31, ProgramColor.Pink),
    ItemData(0xB31094, ItemName.SetSand,           ItemClassification.useful, ItemType.Program,  7, ProgramColor.Green),
    ItemData(0xB31095, ItemName.SneakRun,          ItemClassification.useful, ItemType.Program, 23, ProgramColor.Yellow),
    ItemData(0xB31096, ItemName.Speed_plus_Yellow, ItemClassification.filler, ItemType.Program, 42, ProgramColor.Yellow),
    ItemData(0xB31097, ItemName.WpnLV_plus_White,  ItemClassification.filler, ItemType.Program, 35, ProgramColor.White),
    ItemData(0xB31098, ItemName.WpnLV_plus_Pink,   ItemClassification.filler, ItemType.Program, 35, ProgramColor.Pink),
    ItemData(0xB31099, ItemName.WpnLV_plus_Yellow, ItemClassification.filler, ItemType.Program, 35, ProgramColor.Yellow),
    ItemData(0xB3109A, ItemName.Press,             ItemClassification.progression, ItemType.Program, 20, ProgramColor.White),

    ItemData(0xB310B7, ItemName.UnderSht,          ItemClassification.useful, ItemType.Program, 30, ProgramColor.White),
    ItemData(0xB310E0, ItemName.Humor,             ItemClassification.progression, ItemType.Program, 45, ProgramColor.Pink),
    ItemData(0xB310E1, ItemName.BlckMnd,           ItemClassification.progression, ItemType.Program, 46, ProgramColor.White)
]

zennyList: typing.List[ItemData] = [
    ItemData(0xB3109B, ItemName.zenny_200z,   ItemClassification.filler, ItemType.Zenny, count=200),
    ItemData(0xB3109C, ItemName.zenny_500z,   ItemClassification.filler, ItemType.Zenny, count=500),
    ItemData(0xB3109D, ItemName.zenny_600z,   ItemClassification.filler, ItemType.Zenny, count=600),
    ItemData(0xB3109E, ItemName.zenny_800z,   ItemClassification.filler, ItemType.Zenny, count=800),
    ItemData(0xB3109F, ItemName.zenny_900z,   ItemClassification.filler, ItemType.Zenny, count=900),

    ItemData(0xB310A0, ItemName.zenny_1000z,  ItemClassification.filler, ItemType.Zenny, count=1000),
    ItemData(0xB310A1, ItemName.zenny_1200z,  ItemClassification.filler, ItemType.Zenny, count=1200),
    ItemData(0xB310A2, ItemName.zenny_1400z,  ItemClassification.filler, ItemType.Zenny, count=1400),
    ItemData(0xB310A3, ItemName.zenny_1600z,  ItemClassification.filler, ItemType.Zenny, count=1600),
    ItemData(0xB310A4, ItemName.zenny_1800z,  ItemClassification.filler, ItemType.Zenny, count=1800),
    ItemData(0xB310A5, ItemName.zenny_2000z,  ItemClassification.filler, ItemType.Zenny, count=2000),
    ItemData(0xB310A6, ItemName.zenny_3000z,  ItemClassification.filler, ItemType.Zenny, count=3000),
    ItemData(0xB310A7, ItemName.zenny_9000z,  ItemClassification.filler, ItemType.Zenny, count=9000),
    ItemData(0xB310A8, ItemName.zenny_10000z, ItemClassification.useful, ItemType.Zenny, count=10000),
    ItemData(0xB310A9, ItemName.zenny_30000z, ItemClassification.useful, ItemType.Zenny, count=30000),
    ItemData(0xB310AA, ItemName.zenny_50000z, ItemClassification.useful, ItemType.Zenny, count=50000)
]

bugFragList: typing.List[ItemData] = [
    ItemData(0xB310AB, ItemName.bugfrag_30, ItemClassification.filler, ItemType.BugFrag, count=30),
    ItemData(0xB310B5, ItemName.bugfrag_10, ItemClassification.filler, ItemType.BugFrag, count=10),
    ItemData(0xB310B6, ItemName.bugfrag_01, ItemClassification.filler, ItemType.BugFrag, count=1)
]

item_frequencies: typing.Dict[str, int] = {
    ItemName.Progressive_Undernet_Rank: 8,
    ItemName.ExpMem: 2,
    ItemName.Unlocker: 10,
    ItemName.HPMemory: 23,
    ItemName.RegUP1: 4,
    ItemName.RegUP2: 13,
    ItemName.RegUP3: 4,
    ItemName.Untrap: 2,
    ItemName.SubMem: 4,
    ItemName.MiniEnrg: 3,
    ItemName.FullEnrg: 5,
    ItemName.CopyDmg_star: 3,
    ItemName.Charge_plus_White: 2,
    ItemName.Charge_plus_Pink: 2,
    ItemName.zenny_600z: 2,
    ItemName.zenny_800z: 2,
    ItemName.zenny_1000z: 2,
    ItemName.zenny_1200z: 2,
    ItemName.bugfrag_01: 10,
    ItemName.bugfrag_10: 5
}

item_groups: typing.Dict[str, typing.Set[str]] = {
    "Key Items": {loc.itemName for loc in keyItemList},
    "Subchips": {loc.itemName for loc in subChipList},
    "Programs": {loc.itemName for loc in programList},
    "BattleChips": {loc.itemName for loc in chipList},
    "Zenny": {loc.itemName for loc in zennyList},
    "BugFrags": {loc.itemName for loc in bugFragList},
    "Navi Chips": {
        ItemName.Roll_R, ItemName.RollV2_R, ItemName.RollV3_R, ItemName.GutsMan_G, ItemName.GutsManV2_G,
        ItemName.GutsManV3_G, ItemName.ProtoMan_B, ItemName.ProtoManV2_B, ItemName.ProtoManV3_B, ItemName.FlashMan_F,
        ItemName.FlashManV2_F, ItemName.FlashManV3_F, ItemName.BeastMan_B, ItemName.BeastManV2_B, ItemName.BeastManV3_B,
        ItemName.BubblMan_B, ItemName.BubblManV2_B, ItemName.BubblManV3_B, ItemName.DesertMan_D, ItemName.DesertManV2_D,
        ItemName.DesertManV3_D, ItemName.PlantMan_P, ItemName.PlantManV2_P, ItemName.PlantManV3_P, ItemName.FlamMan_F,
        ItemName.FlamManV2_F, ItemName.FlamManV3_F, ItemName.DrillMan_D, ItemName.DrillManV2_D, ItemName.DrillManV3_D,
        ItemName.MetalMan_M, ItemName.MetalManV2_M, ItemName.MetalManV3_M, ItemName.KingMan_K, ItemName.KingManV2_K,
        ItemName.KingManV3_K, ItemName.BowlMan_B, ItemName.BowlManV2_B, ItemName.BowlManV3_B
    }
}

all_items: typing.List[ItemData] = keyItemList + subChipList + chipList + programList + zennyList + bugFragList
item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in all_items}
items_by_id: typing.Dict[int, ItemData] = {item.code: item for item in all_items}
