import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemType:
    Undernet = "undernet"
    Chip = "chip"
    KeyItem = "key"
    SubChip = "subchip"
    Zenny = "zenny"
    Program = "program"
    BugFrag = "bugfrag"


class ProgressionType:
    Filler = 0
    Useful = 1
    Progression = 2


class ProgramColor:
    White = 1
    Pink = 2
    Yellow = 3
    Red = 4
    Blue = 5
    Green = 6
    Orange = 7
    Purple = 8
    Dark = 9


def ChipCode(c):
    if c == '*':
        return 26
    return ord(c) - ord('A')


class ItemData(typing.NamedTuple):
    code: int
    itemName: str
    progression: ItemClassification
    type: str
    itemID: typing.Optional[int] = 0x00
    subItemID: typing.Optional[int] = 0x00
    count: typing.Optional[int] = 1

    def GenerateItemMessageBox(self) -> bytes:
        pass

class MMBN3Item(Item):
    game: str = "MegaMan Battle Network 3"
    

keyItemList: typing.List[ItemData] = [
    ItemData(0xB31000, ItemName.Progressive_Undernet_Rank, ItemClassification.progression, ItemType.Undernet, 27),
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
    ItemData(0xB31013, ItemName.RegUP1,                    ItemClassification.useful,      ItemType.KeyItem,  98),
    ItemData(0xB31014, ItemName.RegUP2,                    ItemClassification.useful,      ItemType.KeyItem,  99),
    ItemData(0xB31015, ItemName.RegUP3,                    ItemClassification.useful,      ItemType.KeyItem, 100),
    ItemData(0xB31016, ItemName.Mr_Famous_Wristband,       ItemClassification.filler,      ItemType.KeyItem,  57),
    ItemData(0xB31017, ItemName.SubMem,                    ItemClassification.filler,      ItemType.KeyItem, 101)
]

subChipList: typing.List[ItemData] = [
    ItemData(0xB31018, ItemName.Unlocker, ItemClassification.useful, ItemType.SubChip,  117),
    ItemData(0xB31019, ItemName.Untrap,   ItemClassification.filler, ItemType.SubChip,  115),
    ItemData(0xB3101A, ItemName.LockEnmy, ItemClassification.filler, ItemType.SubChip,  116),
    ItemData(0xB3101B, ItemName.MiniEnrg, ItemClassification.filler, ItemType.SubChip,  112),
    ItemData(0xB3101C, ItemName.FullEnrg, ItemClassification.filler, ItemType.SubChip,  113),
    ItemData(0xB3101D, ItemName.SneakRun, ItemClassification.filler, ItemType.SubChip,  114)
]

chipList: typing.List[ItemData] = [
    ItemData(0xB3101E, ItemName.AirShoes_star,     ItemClassification.useful, ItemType.Chip, 168, ChipCode('*')),
    ItemData(0xB3101F, ItemName.AirShot3_star,     ItemClassification.useful, ItemType.Chip,   6, ChipCode('*')),

    ItemData(0xB31020, ItemName.AntiNavi_M,        ItemClassification.useful,      ItemType.Chip, 190, ChipCode('M')),
    ItemData(0xB31021, ItemName.AntiRecv_B,        ItemClassification.useful,      ItemType.Chip, 193, ChipCode('B')),
    ItemData(0xB31022, ItemName.AntiSword_Y,       ItemClassification.useful,      ItemType.Chip, 192, ChipCode('Y')),
    ItemData(0xB31023, ItemName.Aqua_plus_30_star, ItemClassification.useful,      ItemType.Chip, 197, ChipCode('*')),
    ItemData(0xB31024, ItemName.Aura_F,            ItemClassification.useful,      ItemType.Chip, 176, ChipCode('F')),
    ItemData(0xB31025, ItemName.BambooSword_N,     ItemClassification.useful,      ItemType.Chip,  36, ChipCode('N')),
    ItemData(0xB31026, ItemName.Barr100_E,         ItemClassification.useful,      ItemType.Chip, 174, ChipCode('E')),
    ItemData(0xB31027, ItemName.Barr200_E,         ItemClassification.useful,      ItemType.Chip, 175, ChipCode('E')),
    ItemData(0xB31028, ItemName.Barrier_E,         ItemClassification.useful,      ItemType.Chip, 173, ChipCode('E')),
    ItemData(0xB31029, ItemName.Barrier_L,         ItemClassification.useful,      ItemType.Chip, 173, ChipCode('L')),
    ItemData(0xB3102A, ItemName.BlkBomb1_P,        ItemClassification.useful,      ItemType.Chip,  27, ChipCode('P')),
    ItemData(0xB3102B, ItemName.BlkBomb2_S,        ItemClassification.useful,      ItemType.Chip,  28, ChipCode('S')),
    ItemData(0xB3102C, ItemName.Cannon_C,          ItemClassification.filler,      ItemType.Chip,   1, ChipCode('C')),
    ItemData(0xB3102D, ItemName.CopyDmg_star,      ItemClassification.filler,      ItemType.Chip, 194, ChipCode('*')),
    ItemData(0xB3102E, ItemName.CustSwrd_Z,        ItemClassification.useful,      ItemType.Chip,  37, ChipCode('Z')),
    ItemData(0xB3102F, ItemName.DynaWave_V,        ItemClassification.progression, ItemType.Chip,  46, ChipCode('V')),

    ItemData(0xB31030, ItemName.ElecSwrd_P,        ItemClassification.useful,      ItemType.Chip,  35, ChipCode('P')),
    ItemData(0xB31031, ItemName.Fire_plus_30_star, ItemClassification.useful,      ItemType.Chip, 196, ChipCode('*')),
    ItemData(0xB31032, ItemName.FireRat_H,         ItemClassification.useful,      ItemType.Chip, 117, ChipCode('H')),
    ItemData(0xB31033, ItemName.FireSwrd_R,        ItemClassification.useful,      ItemType.Chip,  33, ChipCode('R')),
    ItemData(0xB31034, ItemName.FstGauge_star,     ItemClassification.useful,      ItemType.Chip, 158, ChipCode('*')),
    ItemData(0xB31035, ItemName.GaiaBlde_star,     ItemClassification.useful,      ItemType.Chip, 275, ChipCode('*')),
    ItemData(0xB31036, ItemName.Geddon1_star,      ItemClassification.useful,      ItemType.Chip, 138, ChipCode('*')),
    ItemData(0xB31037, ItemName.Geddon1_D,         ItemClassification.filler,      ItemType.Chip, 138, ChipCode('D')),
    ItemData(0xB31038, ItemName.Geddon3_U,         ItemClassification.useful,      ItemType.Chip, 140, ChipCode('U')),
    ItemData(0xB31039, ItemName.Geyser_B,          ItemClassification.useful,      ItemType.Chip, 107, ChipCode('B')),
    ItemData(0xB3103A, ItemName.GrabBack_K,        ItemClassification.progression, ItemType.Chip, 136, ChipCode('K')),
    ItemData(0xB3103B, ItemName.GrabRvng_A,        ItemClassification.useful,      ItemType.Chip, 137, ChipCode('A')),
    ItemData(0xB3103C, ItemName.GrabRvng_Y,        ItemClassification.useful,      ItemType.Chip, 137, ChipCode('Y')),
    ItemData(0xB3103D, ItemName.GutStrght_S,       ItemClassification.useful,      ItemType.Chip,  48, ChipCode('S')),
    ItemData(0xB3103E, ItemName.Guardian_O,        ItemClassification.useful,      ItemType.Chip, 203, ChipCode('O')),
    ItemData(0xB3103F, ItemName.GutImpact_H,       ItemClassification.useful,      ItemType.Chip,  49, ChipCode('H')),

    ItemData(0xB31040, ItemName.GutImpct_J,        ItemClassification.useful,      ItemType.Chip,  49,  ChipCode('J')),
    ItemData(0xB31041, ItemName.GutPunch_E,        ItemClassification.useful,      ItemType.Chip,  47,  ChipCode('E')),
    ItemData(0xB31042, ItemName.GutsPunch_B,       ItemClassification.useful,      ItemType.Chip,  47,  ChipCode('B')),
    ItemData(0xB31043, ItemName.GutStrgt_Q,        ItemClassification.useful,      ItemType.Chip,  48,  ChipCode('Q')),
    ItemData(0xB31044, ItemName.Hammer_T,          ItemClassification.useful,      ItemType.Chip,  64,  ChipCode('T')),
    ItemData(0xB31045, ItemName.HeatSide_T,        ItemClassification.filler,      ItemType.Chip,  19,  ChipCode('T')),
    ItemData(0xB31046, ItemName.HeroSwrd_P,        ItemClassification.useful,      ItemType.Chip, 207,  ChipCode('P')),
    ItemData(0xB31047, ItemName.HiCannon_star,     ItemClassification.useful,      ItemType.Chip,   2,  ChipCode('*')),
    ItemData(0xB31048, ItemName.Hole_star,         ItemClassification.useful,      ItemType.Chip, 161,  ChipCode('*')),
    ItemData(0xB31049, ItemName.IceStage_star,     ItemClassification.useful,      ItemType.Chip, 180,  ChipCode('*')),
    ItemData(0xB3104A, ItemName.Invis_star,        ItemClassification.useful,      ItemType.Chip, 160,  ChipCode('*')),
    ItemData(0xB3104B, ItemName.Jealousy_J,        ItemClassification.useful,      ItemType.Chip, 214,  ChipCode('J')),
    ItemData(0xB3104C, ItemName.Lance_S,           ItemClassification.useful,      ItemType.Chip,  75,  ChipCode('S')),
    ItemData(0xB3104D, ItemName.LongSwrd_E,        ItemClassification.filler,      ItemType.Chip,  32,  ChipCode('E')),
    ItemData(0xB3104E, ItemName.Magnum1_V,         ItemClassification.useful,      ItemType.Chip,  81,  ChipCode('V')),
    ItemData(0xB3104F, ItemName.Muramasa_M,        ItemClassification.useful,      ItemType.Chip, 202,  ChipCode('M')),

    ItemData(0xB31050, ItemName.Navi_plus_40_star, ItemClassification.useful,      ItemType.Chip, 206, ChipCode('*')),
    ItemData(0xB31051, ItemName.Panic_C,           ItemClassification.useful,      ItemType.Chip,  41, ChipCode('C')),
    ItemData(0xB31052, ItemName.PanlOut3_star,     ItemClassification.useful,      ItemType.Chip, 120, ChipCode('*')),
    ItemData(0xB31053, ItemName.Poltergeist_G,     ItemClassification.useful,      ItemType.Chip, 213, ChipCode('G')),
    ItemData(0xB31054, ItemName.Prism_Q,           ItemClassification.useful,      ItemType.Chip, 142, ChipCode('Q')),
    ItemData(0xB31055, ItemName.Recov10_star,      ItemClassification.useful,      ItemType.Chip, 121, ChipCode('*')),
    ItemData(0xB31056, ItemName.Recov120_star,     ItemClassification.useful,      ItemType.Chip, 125, ChipCode('*')),
    ItemData(0xB31057, ItemName.Recov120_O,        ItemClassification.useful,      ItemType.Chip, 125, ChipCode('O')),
    ItemData(0xB31058, ItemName.Recov120_S,        ItemClassification.progression, ItemType.Chip, 125, ChipCode('S')),
    ItemData(0xB31059, ItemName.Recov150_P,        ItemClassification.useful,      ItemType.Chip, 126, ChipCode('P')),
    ItemData(0xB3105A, ItemName.Recov200_N,        ItemClassification.useful,      ItemType.Chip, 127, ChipCode('N')),
    ItemData(0xB3105B, ItemName.Recov30_star,      ItemClassification.useful,      ItemType.Chip, 122, ChipCode('*')),
    ItemData(0xB3105C, ItemName.Recov300_R,        ItemClassification.useful,      ItemType.Chip, 128, ChipCode('R')),
    ItemData(0xB3105D, ItemName.Recov50_G,         ItemClassification.useful,      ItemType.Chip, 123, ChipCode('G')),
    ItemData(0xB3105E, ItemName.Repair_star,       ItemClassification.useful,      ItemType.Chip, 159, ChipCode('*')),
    ItemData(0xB3105F, ItemName.Repair_A,          ItemClassification.filler,      ItemType.Chip, 159, ChipCode('A')),

    ItemData(0xB31060, ItemName.Rockcube_star,     ItemClassification.useful,      ItemType.Chip, 141, ChipCode('*')),
    ItemData(0xB31061, ItemName.Rook_F,            ItemClassification.useful,      ItemType.Chip, 153, ChipCode('F')),
    ItemData(0xB31062, ItemName.Salamndr_star,     ItemClassification.useful,      ItemType.Chip, 272, ChipCode('*')),
    ItemData(0xB31063, ItemName.SandStage_C,       ItemClassification.useful,      ItemType.Chip, 182, ChipCode('C')),
    ItemData(0xB31064, ItemName.SideGun_S,         ItemClassification.filler,      ItemType.Chip,  12, ChipCode('S')),
    ItemData(0xB31065, ItemName.Slasher_B,         ItemClassification.useful,      ItemType.Chip,  43, ChipCode('B')),
    ItemData(0xB31066, ItemName.SloGuage_star,     ItemClassification.filler,      ItemType.Chip, 157, ChipCode('*')),
    ItemData(0xB31067, ItemName.Snake_D,           ItemClassification.useful,      ItemType.Chip, 131, ChipCode('D')),
    ItemData(0xB31068, ItemName.Snctuary_C,        ItemClassification.useful,      ItemType.Chip, 184, ChipCode('C')),
    ItemData(0xB31069, ItemName.Spreader_star,     ItemClassification.useful,      ItemType.Chip,  13, ChipCode('*')),
    ItemData(0xB3106A, ItemName.Spreader_N,        ItemClassification.useful,      ItemType.Chip,  13, ChipCode('N')),
    ItemData(0xB3106B, ItemName.Spreader_P,        ItemClassification.useful,      ItemType.Chip,  13, ChipCode('P')),
    ItemData(0xB3106C, ItemName.StepCross_Q,       ItemClassification.useful,      ItemType.Chip,  40, ChipCode('Q')),
    ItemData(0xB3106D, ItemName.StepCross_R,       ItemClassification.useful,      ItemType.Chip,  40, ChipCode('R')),
    ItemData(0xB3106E, ItemName.StepSwrd_M,        ItemClassification.useful,      ItemType.Chip,  39, ChipCode('M')),
    ItemData(0xB3106F, ItemName.StepSwrd_N,        ItemClassification.useful,      ItemType.Chip,  39, ChipCode('N')),

    ItemData(0xB31070, ItemName.StepSwrd_O,        ItemClassification.useful,      ItemType.Chip,  39, ChipCode('O')),
    ItemData(0xB31071, ItemName.StepCross_S,       ItemClassification.useful,      ItemType.Chip,  40, ChipCode('S')),
    ItemData(0xB31072, ItemName.Sword_E,           ItemClassification.useful,      ItemType.Chip,  30, ChipCode('E')),
    ItemData(0xB31073, ItemName.Team1_star,        ItemClassification.useful,      ItemType.Chip, 132, ChipCode('*')),
    ItemData(0xB31074, ItemName.Team2_star,        ItemClassification.useful,      ItemType.Chip, 169, ChipCode('*')),
    ItemData(0xB31075, ItemName.Thndrblt_star,     ItemClassification.useful,      ItemType.Chip, 274, ChipCode('*')),
    ItemData(0xB31076, ItemName.Tornado_L,         ItemClassification.useful,      ItemType.Chip,  65, ChipCode('L')),
    ItemData(0xB31077, ItemName.Tsunami_star,      ItemClassification.useful,      ItemType.Chip, 273, ChipCode('*')),
    ItemData(0xB31078, ItemName.VarSword_B,        ItemClassification.useful,      ItemType.Chip,  38, ChipCode('B')),
    ItemData(0xB31079, ItemName.VarSword_F,        ItemClassification.useful,      ItemType.Chip,  38, ChipCode('F')),
    ItemData(0xB3107A, ItemName.WideSwrd_C,        ItemClassification.progression, ItemType.Chip,  31, ChipCode('C')),
    ItemData(0xB3107B, ItemName.WideSwrd_E,        ItemClassification.useful,      ItemType.Chip,  31, ChipCode('E')),
    ItemData(0xB3107C, ItemName.WideSwrd_L,        ItemClassification.useful,      ItemType.Chip,  31, ChipCode('L')),
    ItemData(0xB3107D, ItemName.Yo_Yo1_D,          ItemClassification.useful,      ItemType.Chip,  69, ChipCode('D')),
    ItemData(0xB3107E, ItemName.ZeusHammer_Z,      ItemClassification.useful,      ItemType.Chip, 208, ChipCode('Z')),
    ItemData(0xB3107F, ItemName.BassGS_X,          ItemClassification.useful,      ItemType.Chip, 311, ChipCode('X')),

    ItemData(0xB31080, ItemName.DeltaRay_Z,        ItemClassification.useful,      ItemType.Chip, 301, ChipCode('Z')),
    ItemData(0xB31081, ItemName.Punk_P,            ItemClassification.useful,      ItemType.Chip, 271, ChipCode('P')),
    ItemData(0xB31082, ItemName.DarkAura_A,        ItemClassification.useful,      ItemType.Chip, 308, ChipCode('A')),
    ItemData(0xB31083, ItemName.AlphaArm_Omega_V,  ItemClassification.useful,      ItemType.Chip, 309, ChipCode('V'))
]

programList: typing.List[ItemData] = [
    ItemData(0xB31084, ItemName.Airshoes,          ItemClassification.useful, ItemType.Program, 29, ProgramColor.White),
    ItemData(0xB31085, ItemName.Attack_plus_White, ItemClassification.useful, ItemType.Program, 41, ProgramColor.White),
    ItemData(0xB31086, ItemName.Attack_plus_Pink,  ItemClassification.useful, ItemType.Program, 41, ProgramColor.Pink),
    ItemData(0xB31087, ItemName.BrkChrg,           ItemClassification.useful, ItemType.Program,  3, ProgramColor.Orange),
    ItemData(0xB31088, ItemName.Charge_plus_Pink,  ItemClassification.useful, ItemType.Program, 43, ProgramColor.Pink),
    ItemData(0xB31089, ItemName.Charge_plus_White, ItemClassification.useful, ItemType.Program, 43, ProgramColor.White),
    ItemData(0xB3108A, ItemName.Collect,           ItemClassification.useful, ItemType.Program, 28, ProgramColor.Pink),
    ItemData(0xB3108B, ItemName.GigFldr1,          ItemClassification.useful, ItemType.Program, 48, ProgramColor.Purple),
    ItemData(0xB3108C, ItemName.HP_100_Pink,       ItemClassification.useful, ItemType.Program, 36, ProgramColor.Pink),
    ItemData(0xB3108D, ItemName.HP_100_Yellow,     ItemClassification.useful, ItemType.Program, 36, ProgramColor.Yellow),
    ItemData(0xB3108E, ItemName.HP_200_Yellow,     ItemClassification.useful, ItemType.Program, 37, ProgramColor.Yellow),
    ItemData(0xB3108F, ItemName.HP_500_Yellow,     ItemClassification.useful, ItemType.Program, 39, ProgramColor.Yellow),

    ItemData(0xB31090, ItemName.HubBatc,           ItemClassification.useful, ItemType.Program, 49, ProgramColor.Orange),
    ItemData(0xB31091, ItemName.Jungle,            ItemClassification.useful, ItemType.Program, 27, ProgramColor.White),
    ItemData(0xB31092, ItemName.OilBody,           ItemClassification.useful, ItemType.Program, 24, ProgramColor.Yellow),
    ItemData(0xB31093, ItemName.QuickGge,          ItemClassification.useful, ItemType.Program, 31, ProgramColor.Pink),
    ItemData(0xB31094, ItemName.SetSand,           ItemClassification.useful, ItemType.Program,  7, ProgramColor.Green),
    ItemData(0xB31095, ItemName.SneakRun,          ItemClassification.useful, ItemType.Program, 23, ProgramColor.Pink),
    ItemData(0xB31096, ItemName.Speed_plus_Yellow, ItemClassification.useful, ItemType.Program, 42, ProgramColor.Yellow),
    ItemData(0xB31097, ItemName.WpnLV_plus_White,  ItemClassification.useful, ItemType.Program, 35, ProgramColor.White),
    ItemData(0xB31098, ItemName.WpnLV_plus_Pink,   ItemClassification.useful, ItemType.Program, 35, ProgramColor.Pink),
    ItemData(0xB31099, ItemName.WpnLV_plus_Yellow, ItemClassification.useful, ItemType.Program, 35, ProgramColor.Yellow),
    ItemData(0xB3109A, ItemName.Press,             ItemClassification.useful, ItemType.Program, 20, ProgramColor.White)
]

zennyList: typing.List[ItemData] = [
    ItemData(0x0B3109B, ItemName.zenny_200z,   ItemClassification.filler, ItemType.Zenny, count=200),
    ItemData(0x0B3109C, ItemName.zenny_500z,   ItemClassification.filler, ItemType.Zenny, count=500),
    ItemData(0x0B3109D, ItemName.zenny_600z,   ItemClassification.filler, ItemType.Zenny, count=600),
    ItemData(0x0B3109E, ItemName.zenny_800z,   ItemClassification.filler, ItemType.Zenny, count=800),
    ItemData(0x0B3109F, ItemName.zenny_900z,   ItemClassification.filler, ItemType.Zenny, count=900),

    ItemData(0x0B310A0, ItemName.zenny_1000z,  ItemClassification.filler, ItemType.Zenny, count=1000),
    ItemData(0x0B310A1, ItemName.zenny_1200z,  ItemClassification.filler, ItemType.Zenny, count=1200),
    ItemData(0x0B310A2, ItemName.zenny_1400z,  ItemClassification.filler, ItemType.Zenny, count=1400),
    ItemData(0x0B310A3, ItemName.zenny_1600z,  ItemClassification.filler, ItemType.Zenny, count=1600),
    ItemData(0x0B310A4, ItemName.zenny_1800z,  ItemClassification.filler, ItemType.Zenny, count=1800),
    ItemData(0x0B310A5, ItemName.zenny_2000z,  ItemClassification.filler, ItemType.Zenny, count=2000),
    ItemData(0x0B310A6, ItemName.zenny_3000z,  ItemClassification.filler, ItemType.Zenny, count=3000),
    ItemData(0x0B310A7, ItemName.zenny_9000z,  ItemClassification.filler, ItemType.Zenny, count=9000),
    ItemData(0x0B310A8, ItemName.zenny_10000z, ItemClassification.useful, ItemType.Zenny, count=10000),
    ItemData(0x0B310A9, ItemName.zenny_30000z, ItemClassification.useful, ItemType.Zenny, count=30000),
    ItemData(0x0B310AA, ItemName.zenny_50000z, ItemClassification.useful, ItemType.Zenny, count=50000)
]

bugFragList: typing.List[ItemData] = [
    ItemData(0x0B310AB, ItemName.bugfrag_30, ItemClassification.filler, ItemType.BugFrag, count=30)
]

all_items: typing.List[ItemData] = keyItemList + subChipList + chipList + programList + zennyList + bugFragList
item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in all_items}
items_by_id: typing.Dict[int, ItemData] = {item.code: item for item in all_items}
lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
