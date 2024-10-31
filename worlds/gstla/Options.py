from dataclasses import dataclass
from enum import IntEnum, auto
from Options import Choice, NamedRange, PerGameCommonOptions


class RandoOptions(IntEnum):
    #1st Byte--
    ItemShufAll   =  0b11000000
    """
    All item locations in the game are in the pool
    """

    ItemShufTreas =  0b10000000
    """
    Most locations are in the game are in the pool
    """

    ItemShufKey   =  0b01000000
    """
    Only key items are in the pool
    """

    OmitSuper  =     0b00100000
    """
    Omit Super + Anemos
    """

    OmitAnemos =     0b00010000
    """
    Omit just Anemos
    """

    GS1Items =       0b00001000
    """
    Include Elven Shirt and Cleric ring
    """

    ShowItems =      0b00000100
    """
    Are items on the floor or in chests?
    """

    NoLearning =     0b00000010
    """
    Can classes learn growth, whirlwind etc
    """

    ClassStats =     0b00000001
    """
    Are classes shuffled in stats
    """

    #2nd Byte---
    EquipShuffle =   0b10000000
    """
    Shuffle equip compatibilty
    """

    EquipCost =      0b01000000
    """
    Adjust equipment prices
    """

    EquipStats =     0b00100000
    """
    #Adjust equipment stats
    """

    EquipSort =      0b00010000
    """
    Make weaker equipment more likely early
    """

    EquipUnleash =   0b00001000
    """
    Shuffle unleashes from weapons
    """

    EquipEffect =    0b00000100
    """
    Shuffle armor effects
    """

    EquipCurse =     0b00000010
    """
    Randomize Curses
    """

    PsyEnergyPower = 0b00000001
    """
    Adjust Psy Power
    """

    #3rd Byte--
    DjinnShuffle =   0b10000000
    """
    Shuffle Djinn
    """

    DjinnStats   =   0b01000000
    """
    Shuffle Djinn stats
    """

    DjinnPower   =   0b00100000 
    """
    Adjust Djinn attack power
    """

    DjinnAoe     =   0b00010000 
    """
    Randomize Djinn Aoe size
    """

    DjinnScale   =   0b00001000 
    """
    Scale wild Djinn based on how many are owned
    """

    SummonCost   =   0b00000100
    """
    Ranodmize Summon Costs
    """

    SummonPower  =   0b00000010
    """
    Adjust Summon Power
    """

    SummonSort   =   0b00000001
    """
    More likely to find cheaper summons early
    """

    #4th Byte--
    CharStatsAdj =   0b10000000
    """
    Adjust Character Stats
    """

    CharStatsShuf=   0b01000000
    """
    Shuffle Character Stats
    """

    CharEleAdj   =   0b00100000
    """
    Randomize Character Elements
    """

    CharEletShuf =   0b00010000
    """
    Shuffle Character Elements
    """

    PsyEnergyCost=   0b00001000
    """
    Adjust Psy Cost
    """

    PsyEnergyAoe =   0b00000100
    """
    Adjust Psy Aoe size
    """

    EnemyPsyPow  =   0b00000010
    """
    Adjust Enemy Psy power
    """

    EnemyPsyAoe  =   0b00000001
    """
    Adjust Enemy Psy Aoe size
    """

    #5th Byte--
    ShuffPsyGrp  =   0b10100000
    """
    Randomize by Psy group (prefer same ele)
    """

    ShuffPsy     =   0b10000000
    """
    Fully Randomize Psy
    """

    ClassPsyEle  =   0b01100000
    """
    Randomize by Psy element
    """

    ClassPsyGrp  =   0b01000000
    """
    Randomize by Psy group
    """

    ClassPsyShuf =   0b00100000
    """
    Randomize by Class
    """

    ClassLevelsRand  =   0b00010000
    """
    Fully randomize Psy levels
    """

    ClassLevelsShuf  =   0b00001000
    """
    Shuffle Psy levels
    """

    QolCutscenes =   0b00000100
    """
    Skip cutscenes
    """

    QolTickets   =   0b00000010
    """
    Disable game tickets from shops
    """

    QolFastShip  =   0b00000001
    """
    Faster ship movement on overworld
    """

    #6th Byte--
    ShipFromStart=   0b10000000
    """
    Start with the ship
    """

    ShipUnlock   =   0b01000000
    """
    Ship door is unlocked but still need defeat the boss to use it
    """

    SkipsBasic   =   0b00100000
    """
    Basic skips such as retreat glithc might be required, Retreat 0 PP will be disabled
    """

    SkipsOOBEasy =   0b00010000
    """
    Simple OOB skips may be required, Retreat 0 PP will be disabled
    """

    SkipsMaze    =   0b00001000
    """
    Perform Gaia Rock Maze without Growth
    """

    BossLogic    =   0b00000100
    """
    Remove logical djinn requirement from bosses
    """

    FreeAvoid    =   0b00000010
    """
    Avoid costs 0 PP
    """

    FreeRetreat  =   0b00000001
    """
    Retreat costs 0 PP
    """


    #7th Byte--
    AdvEquip     =   0b10000000
    """
    Shuffle shop artefacts and forgeable equipemnt
    """

    DummyItems   =   0b01000000
    """
    Shuffle dummy items that are not normally obtainable
    """

    SkipsOOBHard =   0b00100000
    """
    Hard OOB skips with complex movement may be required, Retreat 0 PP will be disabled
    """

    EquipAttack  =   0b00010000
    """
    Shuffle weapon attack
    """

    QoLHints     =   0b00001000
    """
    Add ingame item hints
    """

    StartHeal    =   0b00000100
    """
    Start with a Healing Psy
    """

    StartRevive  =   0b00000010
    """
    Start with Revive Psy
    """

    StartReveal  =   0b00000001
    """
    Start with Reveal
    """

    #8th Byte--
    ScaleExp     =   0b11110000
    """
    Scale Exp from 1 (vanilla) to max 15
    """

    ScaleCoins   =   0b00001111
    """
    Scale Coins from 1 (vanilla) to max 15
    """

    #9th Byte--
    EquipDefense =   0b10000000
    """
    Shuffle equipment defense
    """

    StartLevels  =   0b01111111
    """
    Starting levels from 5 to 99
    """

    #10th Byte--
    EnemyeResRand=   0b10000000
    """
    Randomize Enemy eleRes
    """

    EnemyeResShuf=   0b01000000
    """
    Shuffle Enemy eleRes
    """

    SancRevFixed =   0b00100000
    """
    Sanc Revive fixed at 100 coins
    """

    SancRevCheap =   0b00010000
    """
    Sanc Revive scales by 2x levels (vanilla is 20x level)
    """

    CurseDisable =   0b00001000
    """
    Remove all curses
    """

    AvoidPatch   =   0b00000100
    """
    Make avoid a toggleable, it always works and it toggles encounters
    """

    RetreatPatch =   0b00000010
    """
    Does nothing
    """

    TeleportPatch=   0b00000001
    """
    Makes retreat act as Teleport on Overworld
    """

    #11th Byte--
    HardMode     =   0b10000000
    """
    Enemies have 50% more hp and 25% more power&defense
    """

    HalveEnc     =   0b01000000
    """
    Half the encounter rate
    """

    MajorShuffle =   0b00100000
    """
    Enable Major / Minor split for item shuffle, only for Most and All
    """

    EasierBosses =   0b00010000
    """
    Bosses are easier
    """

    RandomPuzzles=   0b00001000
    """
    Make name based puzzle random
    """

    FixedPuzzles =   0b00000100
    """
    Make name based puzzles fixed to name Felix
    """

    ManualRG     =   0b00000010
    """
    Hold select to trigger the Retreat glitch
    """

    ShipWings    =   0b00000001
    """
    Start with the wings of Anemos
    """

    #12th Byte--
    MusicShuffle =   0b10000000
    """
    Shuffle ingame music
    """

    TeleportAny  =   0b01000000
    """
    Allow teleport to teleport to dungeons / small towns
    """

    ForceBossDrop=   0b00100000
    """
    Force bosses to have progression items
    """

    ForceSuperMin=   0b00010000
    """
    Prevent super bosses from having progression items
    """

    AnemosOpen   =   0b00001000
    """
    Anemos sanctum is always open
    """

    AnemosRand   =   0b00000100
    """
    Anoemos sacntum needs between 16 to 28 djinn to enter
    """

    ShufflePCs   =   0b00000010
    """
    Randomize the playable characters
    """

    def __new__(cls, bit_flag: int):
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

@dataclass
class GSTLAOptions(PerGameCommonOptions):
    starter_ship: StartWithShip
    hidden_items: HiddenItems
    super_bosses: SuperBosses
    djinn_logic: DjinnLogic
    djinn_shuffle: DjinnShuffle
    character_shuffle: CharacterShuffle
