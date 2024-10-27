from enum import IntEnum, auto
from Options import Choice, NamedRange

class RandoOptions(IntEnum):
    ItemShufAll   =  0b11000000
    ItemShufTreas =  0b10000000
    ItemShufKey   =  0b01000000
    OmitSuper  =     0b00100000
    OmitAnemos =     0b00010000
    GS1Items =       0b00001000
    ShowItems =      0b00000100
    NoLearning =     0b00000010
    ClassStats =     0b00000001

    EquipShuffle =   0b10000000
    EquipCost =      0b01000000
    EquipStats =     0b00100000
    EquipSort =      0b00010000
    EquipUnleash =   0b00001000
    EquipEffect =    0b00000100
    EquipCurse =     0b00000010
    PsyEnergyPower = 0b00000001

    DjinnShuffle =   0b10000000
    DjinnStats   =   0b01000000
    DjinnPower   =   0b00100000
    DjinnAoe     =   0b00010000
    DjinnScale   =   0b00001000
    SummonCost   =   0b00000100
    SummonPower  =   0b00000010
    SummonSort   =   0b00000001

    CharStatsAdj =   0b10000000
    CharStatsShuf=   0b01000000
    CharEleAdj   =   0b00100000
    CharEletShuf =   0b00010000
    PsyEnergyCost=   0b00001000
    PsyEnergyAoe =   0b00000100
    EnemyPsyPow  =   0b00000010
    EnemyPsyAoe  =   0b00000001

    ShuffPsyGrp  =   0b10100000
    ShuffPsy     =   0b10000000
    ClassPsyEle  =   0b01100000
    ClassPsyGrp  =   0b01000000
    ClassPsyShuf =   0b00100000
    ClassLevels  =   0b00011000
    QolCutscenes =   0b00000100
    QolTickets   =   0b00000010
    QolFastShip  =   0b00000001

    ShipFromStart=   0b10000000
    ShipUnlock   =   0b01000000
    SkipsBasic   =   0b00100000
    SkipsOOBEasy =   0b00010000
    SkipsMaze    =   0b00001000
    BossLogic    =   0b00000100
    FreeAvoid    =   0b00000010
    FreeRetreat  =   0b00000001

    AdvEquip     =   0b10000000
    DummyItems   =   0b01000000
    SkipsOOBHard =   0b00100000
    EquipAttack  =   0b00010000
    QoLHints     =   0b00001000
    StartHeal    =   0b00000100
    StartRevive  =   0b00000010
    StartReveal  =   0b00000001

    ScaleExp     =   0b11110000
    ScaleCoins   =   0b00001111

    EquipDefense =   0b10000000
    StartLevels  =   0b01111111


    EnemyeResRand=   0b10000000
    EnemyeResShuf=   0b01000000
    SancRevFixed =   0b00100000
    SancRevCheap =   0b00010000
    CurseDisable =   0b00001000
    AvoidPatch   =   0b00000100
    RetreatPatch =   0b00000010
    TeleportPatch=   0b00000001

    HardMode     =   0b10000000
    HalveEnc     =   0b01000000
    MajorShuffle =   0b00100000
    EasierBosses =   0b00010000
    RandomPuzzles=   0b00001000
    FixedPuzzles =   0b00000100
    ManualRG     =   0b00000010
    ShipWings    =   0b00000001

    MusicShuffle =   0b10000000
    TeleportAny  =   0b01000000
    ForceBossDrop=   0b00100000
    ForceSuperMin=   0b00010000
    AnemosOpen   =   0b00001000
    AnemosRand   =   0b00000100
    ShufflePCs   =   0b00000010

    def __new__(cls, bit_flag):
        value = len(cls.__members__)
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.bit_flag = bit_flag
        return obj

class StartWithShip(Choice):
    display_name = "Start with ship"
    option_startwithship = 0
    option_shipisclosed = 1
    option_vanilla = 2
    default = 0

class HiddenItems(Choice):
    display_name = "Hidden items"
    option_revealrequired = 0
    option_included = 1
    option_excluded = 2
    default = 0

class CharacterShuffle(Choice):
    display_name = "Character Shuffle"
    option_anywhere = 0
    option_vanilla_shuffled = 1
    option_vanilla = 2
    default = 1

class DjinnShuffle(Choice):
    display_name = "Djinn Shuffle"
    #option_anywhere = 0, not supported yet
    option_vanilla_shuffled = 1
    option_vanilla = 2
    default = 1

class SuperBosses(Choice):
    display_name = "Super Bosses"
    option_excludeoptionalbosses = 0
    option_excludeanemos = 1
    option_allincluded = 2
    default = 0

class DjinnLogic(NamedRange):
    display_name = "Djinn Logic"
    range_start = 0
    range_end = 100
    default = 100

    special_range_names = {
        "casual": 100,
        "hard": 50,
        "none": 0
    }

GSTLAOptions = {
    "starter_ship": StartWithShip,
    "hidden_items": HiddenItems,
    "super_bosses": SuperBosses,
    "djinn_logic": DjinnLogic,
    "djinn_shuffle": DjinnShuffle,
    "character_shuffle": CharacterShuffle
}