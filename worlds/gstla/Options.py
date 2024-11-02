from dataclasses import dataclass
from enum import IntEnum, auto
from Options import Choice, Toggle, Range, NamedRange, PerGameCommonOptions


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
    option_vanilla = 0
    option_shipisclosed = 1
    option_startwithship = 2
    default = 0

class CharacterShuffle(Choice):
    display_name = "Character Shuffle"
    option_anywhere = 2
    option_vanilla_shuffled = 1
    option_vanilla = 0
    default = 1

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

class RevealHiddenItem(Toggle):
    """If enabled all hidden items require Reveal to be logically accessible.
    Note that most hidden items can be gotten regardless of having Reveal or not.
    Also there are a few locations that hard require Reveal to be obtainable, this setting does not alter those.
    """
    display_name = "Reveal Hidden Items"
    default = 1

class ItemShuffle(Choice):
    """Which locations are part of the pool.
    Most is all locations but the pots and barrels containing hidden Items. Note some hidden chests may still exist.
    All is all locations, including hidden items in pots and barrles,"""
    display_name = "Item Shuffle"
    option_most = 2
    option_all = 3
    default = 2

class OmitLocations(Choice):
    """Choose to omit locations containing optional harder boss fights
    None keeps all super bosses in play
    Anemos excludes the Anemos dungeon
    Superboss excludes all super bosses
    """
    option_none = 0
    option_anemos = 1
    option_superboss = 2
    default = 2

class AddGs1Items(Toggle):
    """When enabled adds GS1 items as Elven Shirt and Cleric Ring
    Not yet implemted.
    """
    display_name = "Add GS1 items"

class VisibleItems(Toggle):
    """When enabled the items are visible on the floor. This allows for scouting items.
    Note certain locations are still not visible, for example hidden items in pots or barrels.
    """
    display_name = "Visible Items"
    default = 1

class NoLearningUtilPsy(Toggle):
    """When enabled utility Psynergy is not learned by any classes. Examples of these are Whirlwind and Growth.
    """
    display_name = "No Learning Util Psy"
    default = 1

class ShuffleClassStats(Toggle):
    """When enabled the base stats for classes are randomized"""
    display_name = "Shuffle Class Stats"

class ShuffleEqCompatibility(Toggle):
    """When enabled the compatability for each equipment piece is randomized. 
    Compatibility defines what each character can equip."""
    display_name = "Shuffle Eq Compatability"

class ShuffleEqPrices(Toggle):
    """When enabled the price for each equipment piece is randomized."""
    display_name = "Shuffle Eq Prices"

class ShuffleEqStats(Toggle):
    """When enabled the stats for each equipment piece is randomized."""
    display_name = "Shuffle Eq Stats"

class ShuffleWpnUnleash(Toggle):
    """When enabled the unleashes for weapons are randomized."""
    display_name = "Shuffle Weapon Unleashes"

class ShuffleArmEffect(Toggle):
    """When enabled the bonus effects for armour are randomized."""
    display_name = "Shuffle Armour Effects"

class ShuffleEqCurses(Toggle):
    """When enabled the curses for equipment are randomized."""
    display_name = "Shuffle Armour Effects"

class ShufflePsyPower(Toggle):
    """When enabled the power of Psynergy is randomized"""
    display_name = "Shuffle Psynergy Power"

class DjinnShuffle(Choice):
    """Determine how djinn should be placed in the multiworld.
    Note currently Djinn can only be placed in other djinn locations in their own world due to limitations.
    """
    display_name = "Djinn Shuffle"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    #option_anywhere = 2, not supported yet
    default = 1

class ShuffleDjinnStats(Toggle):
    """When enabled the stats a djinn grant are randomized"""
    display_name = "Shuffle Djinn stat boosts"

class ShuffleDjinnPower(Toggle):
    """When enabled the attack power of djinn are randomized"""
    display_name = "Shuffle Djinn attack power"

class ShuffleDjinnAoe(Toggle):
    """When enabled the Area o Effect of djinn used in battle is randomized."""
    display_name = "Shuffle Djinn Area of Effect"

class ScaleWildDjinn(Toggle):
    """when enabled the Djinn you encounter and fight will get stronger the more Djinn you own."""
    display_name = "Scale Djinn Encounters"

class ShuffleSummonCosts(Toggle):
    """When enabled the costs for Summons is randomized."""
    display_name = "Shuffle Summon costs"

class ShuffleSummonPower(Toggle):
    """when enabled the power of Summons is randomized"""
    display_name = "Shuffle Summon Power"

class CharStatShuffle(Choice):
    """Determine how character stats are shuffled
    Vanilla leaves the stats as per the vanilla game
    Shuffled will shuffle stats between characters
    Randomized will roll each stat seperately
    """
    display_name = "Character Stats Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2,
    default = 0

class CharEleShuffle(Choice):
    """Determine how character elements are shuffled
    Vanilla leaves character elements as per the vanilla game
    Shuffled will shuffle them between characters
    Randomized will roll each element seperately
    """
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2,
    default = 0

class ShufflePsyCost(Toggle):
    """When enabled the cost of Psynergy is shuffled"""
    display_name = "Shuffle Psynergy Cost"

class ShufflePsyAoe(Toggle):
    """When enabled the AoE of Psynergy is shuffled"""
    display_name = "Shuffle Psynergy AoE"

class ShuffleEnemyPsyPower(Toggle):
    """When enabled the power of Enemy Psynergy is randomized"""
    display_name = "Shuffle Enemy Psynergy Power"

class ShuffleEnemyPsyAoe(Toggle):
    """When enabled the AoE of Enemy Psynergy is randomized"""
    display_name = "Shuffle Enemy Psynergy AoE"

class ClassPsyShuffle(Choice):
    """Determine what Psynergy a class will learn
    Vanilla leaves the Psynergy on their vanilla classes
    Class will randomize them by classline
    Group will randomize them by Psynergy group
    Group Element will randomize them by Psynergy group with a preference to the same Element
    Element will randomize them by Psynergy Element
    Full will randomize it completely without grouping or preference
    """
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_class = 1
    option_group = 2
    option_group_element = 5
    option_element = 3
    option_full = 4
    default = 0

class ClassPsyLevels(Choice):
    """Determine what Psynergy a class will learn
    Vanilla leaves the Psynergy on their vanilla classes
    Adjust will randomize them within a margin from vanilla
    Randomized will randomize them completely
    """
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_shuffle = 1
    option_randomized = 2
    default = 0

class QoLDisableCutscenes(Toggle):
    """When enabled, cutscenes will be shortened or removed"""
    display_name = "Skip Cutscenes"

class QoLRemoveGameTickets(Toggle):
    """When enabled, game tickets from and for shops are removed"""
    display_name = "Disable Game Tickets"

class QoLFastShip(Toggle):
    """When enabled, increase the overworld travel speed of the ship"""
    display_name = "Fast Ship"

class FreeAvoid(Toggle):
    """When enabled, the Avoid Psynergy is Free"""
    display_name = "Free Avoid"

class FreeRetreat(Toggle):
    """When enabled, the Retreat Psynergy is Free"""
    display_name = "Free Retreat"

class ShuffleAttack(Toggle):
    """When enabled, the attack stat from weapons is shuffled amongst eachother"""
    display_name = "Shuffle weapon attack"

class StartWithHealPsy(Toggle):
    """When enabled, start the game with atleast one healing Psynergy (Cure, Ply, Wish or Aura)"""
    display_name = "Start with Heal"

class StartWithRevivePsy(Toggle):
    """When enabled, start the game with Revive Psynergy"""
    display_name = "Start with Revive"

class StartWithRevealPsy(Toggle):
    """When enabled, start the game with Reveal Psynergy"""
    display_name = "Start with Reveal"

class ScaleExpGained(Range):
    """Scale how much Exp is earned by the party."""
    display_name = "Scale Exp"
    range_start = 1
    range_end = 15
    default = 3

class ScaleGoldGained(Range):
    """Scale how much Coins are earned by the party."""
    display_name = "Scale Coins"
    range_start = 1
    range_end = 15
    default = 4

class ShuffleDefense(Toggle):
    """When enabled, the defense from equipment is shuffled amongst eachother"""
    display_name = "Shuffle armour defense"


class StartLevels(Range):
    """Determine the starting levels for characters joining the party.
    Note this only increases levels of characters that are lower"""
    display_name = "Starting levels"
    range_start = 5
    range_end = 99
    default = 5

class EnemyEResShuffle(Choice):
    """Determine how Enemy Elemental Resistance is shuffled
    Vanilla leaves the elemental resistance as per the vanilla game
    Shuffled will shuffle them between enemies
    Randomized will roll each enemy seperately
    """
    display_name = "Enemy Elemental Resistance Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2,
    default = 0

class SanctuaryResCost(Choice):
    """Determine how expensive the Sanctuary is to revive characters
    Vanilla leaves the cost per the vanilla game (20x level)
    Reduced will alter the cost to be cheaper than vanilla (2x level)
    Fixed will alter the cost to the same price throughout (100 coins)
    """
    display_name = "Enemy Elemental Resistance Shuffle"
    option_vanilla = 0
    option_reduced = 1
    option_fixed = 2,
    default = 1

class DisableCurses(Toggle):
    """When enabled, curses are removed"""
    display_name = "Remove Curses"

class AvoidPatch(Toggle):
    """When enabled, Avoid always succeeds and will disable encounters. Using it again will enable encounters"""
    display_name = "Avoid Patch"

class TeleportPatch(Toggle):
    """When enabled, allows the use of Retreat on overworld which makes it act like Teleport. 
    Teleport allows you to move to previously visited areas"""
    display_name = "Teleport Patch"

class EnableHardMode(Toggle):
    """When enabled, all enemies will have 50% more health, 25% more attack and defense"""
    display_name = "Enable Hard Mode"

class HalveEncounterRate(Toggle):
    """When enabled, the encounter rate will be halved"""
    display_name = "Reduce Encounter Rate"

class MajorMinorSplit(Toggle):
    """When enabled, all major locations will prefer progressive and all minor locations will prefer filler."""
    display_name = "Major Minor Split"

class EasierBosses(Toggle):
    """When enabled, boss fights will be easier by altering their scripts / stats"""
    display_name = "Easier Bosses"

class RandomPuzzles(Toggle):
    """When enabled, the name based puzzles are randomized"""
    display_name = "Random Puzzles"

class FixedPuzzles(Toggle):
    """When enabled, the name based puzzles are fixed to use name Felix"""
    display_name = "Fixed Puzzles"

class ManualRetreatGlitch(Toggle):
    """When enabled, Hold select to trigger the Retreat glitch.
    Mostly useful for glitches logic"""
    display_name = "Manual Retreat Glitch"

class ShipWings(Toggle):
    """When enabled, the ship starts with the Wings of Anemos."""
    display_name = "Start with Ship Wings"

class MusicShuffle(Toggle):
    """When enabled, music is shuffled amongst eachother."""
    display_name = "Music Shuffle"

class TelportEverywhere(Toggle):
    """When enabled, allows Teleport to target small villages and dungeons"""
    display_name = "Teleport Everywhere"

class ForceBossDrops(Toggle):
    """When enabled, forces bosses to have a useful or progression item."""
    display_name = "Force Bosses to good items"

class ForceSuperBossJunk(Toggle):
    """When enabled, forces super bosses to have a junk item."""
    display_name = "Force SuperBosses to junk items"



@dataclass
class GSTLAOptions(PerGameCommonOptions):
    
    reveal_hidden_item: RevealHiddenItem
    djinn_logic: DjinnLogic

    #Base rando settings
    #Set 1
    item_shuffle: ItemShuffle
    omit_locations: OmitLocations
    gs1_items: AddGs1Items
    visible_items: VisibleItems
    no_learning_util: NoLearningUtilPsy
    shuffle_class_stats: ShuffleClassStats

    #Set 2
    shuffle_eq_prices: ShuffleEqPrices
    shuffle_eq_stats: ShuffleEqStats
    #equip-sort not supported, make weaker equipment appear earlier
    shuffle_weapon_unleah: ShuffleWpnUnleash
    shuffle_armor_effect: ShuffleArmEffect
    shuffle_eq_curses: ShuffleEqCurses
    shuffle_psy_power: ShufflePsyPower

    #Set 3
    djinn_shuffle: DjinnShuffle
    shuffle_djinn_stats: ShuffleDjinnStats
    shuffle_djinn_power: ShuffleDjinnPower
    shuffle_djinn_aoe: ShuffleDjinnAoe
    scale_djinn_enc: ScaleWildDjinn
    shuffle_summon_costs: ShuffleSummonCosts
    shuffle_summon_power: ShuffleSummonPower
    #summon sort not supported, make cheaper summons appear earlier

    #Set 4
    shuffle_char_stats: CharStatShuffle
    shuffle_char_elem: CharEleShuffle
    shuffle_psy_cost: ShufflePsyCost
    shuffle_psy_aoe: ShufflePsyAoe
    shuffle_enmy_psy_power: ShuffleEnemyPsyPower
    shuffle_enmy_psy_aoe: ShuffleEnemyPsyAoe

    #Set 5
    class_psynergy: ClassPsyShuffle
    class_levels: ClassPsyLevels
    qol_cutscenes: QoLDisableCutscenes
    qol_gameticket: QoLRemoveGameTickets
    qol_fastship: QoLFastShip

    #Set 6
    starter_ship: StartWithShip
    #skips-basic not supported, logic changes required
    #skips-oob-easy not supported, logic changes required
    #skips-maze not supported, logic changes required
    #boss-logic, our version is djinnlogic where base rando is binary on/off on djinn requirement we have a scale setting
    free_avoid: FreeAvoid
    free_retreat: FreeRetreat

    #Set 7
    #adv-equip not supported, requires AP to know shop artefact locations and forging locations
    #dummy-items not supported, they are not normally obtainable and we use one of them for foreign world items
    #skips-oob-hard not supported, logic changes required
    shuffle_eq_attack: ShuffleAttack
    #qol-hints not supported yet
    start_heal: StartWithHealPsy
    start_revive: StartWithRevivePsy
    start_reveal: StartWithRevealPsy

    #Set 8
    scale_exp: ScaleExpGained
    scale_coins: ScaleGoldGained

    #Set 9
    shuffle_eq_defense: ShuffleDefense
    start_levels: StartLevels

    #Set 10
    enemy_eres: EnemyEResShuffle
    sanc_revive: SanctuaryResCost
    curse_disabled: DisableCurses
    avoid_patch: AvoidPatch
    #retreat_patch, does nothing in upstream
    teleport_patch: TeleportPatch

    #Set 11
    hard_mode: EnableHardMode
    halve_enc: HalveEncounterRate
    major_min_shuffle: MajorMinorSplit
    easier_bosses: EasierBosses
    random_puzzles: RandomPuzzles
    fixed_puzzles: FixedPuzzles
    manual_rg: ManualRetreatGlitch
    ship_wings: ShipWings

    #Set 12
    music_shuffle: MusicShuffle
    teleport_everywhere: TelportEverywhere
    force_boss_drops: ForceBossDrops
    force_superboss_minors: ForceSuperBossJunk
    #Anemos-access, not supported as it requires logical changes and has few options that seem uninteresting
    character_shuffle: CharacterShuffle