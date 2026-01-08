from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, Toggle, DeathLink


class LevelSanity(DefaultOnToggle):
    """
    Makes level-ups location checks. 
    This adds between 1-29 checks depending on on the LevelSanity Range option below.
    """
    display_name = "LevelSanity"

class LevelSanityRange(Range):
    """
    How many level-ups are included as location checks. Levels after 10 have the magic key in logic to prevent a tedious early grind. 
    """
    display_name = "LevelSanity Range"
    range_start = 2
    range_end = 30
    default = 20

class SearchSanity(DefaultOnToggle):
    """
    Adds search spot items as location checks.
    This adds 3 checks.
    """
    display_name = "SearchSanity"

class ShopSanity(Toggle):
    """
    Buying a piece of equipment sends a location check instead of buying it. Adds progressive equipment items instead.
    This adds 13 checks. This option overrides and disables the randomized equipment shops option below.
    """
    display_name = "ShopSanity"

class MonsterSanity(Toggle):
    """
    Killing a monster for the first time sends a location check. This adds 40 checks. This option overrides and disables
    the random monster zones option below.
    """
    display_name = "MonsterSanity"

class RandomGrowth(Toggle):
    """ 
    Player statistical growth at each level will be randomized.
    """
    display_name = "Randomize Growth"

class RandomMap(Toggle):
    """
    The overworld map will be randomly generated. Stairs leading to other maps (Tantegel Basement, Garin's Grave) 
    are also shuffled.

    Note that this is currently an experimental option! If you roll an unwinnable seed please let the developer know.
    """
    display_name = "Random Map"

class RandomMapSize(Choice):
    """
    Sets the size of the randomly generated map.
    """
    display_name = "Random Map Size"
    option_normal = 0
    option_small = 1
    option_very_small = 2
    default = 0

class RandomSpellLearning(Toggle):
    """ 
    The order and level you learn spells will be random.
    """
    display_name = "Random Spell Learning"

class RandomWeaponShops(Toggle):
    """
    The weapons available in each shop will be randomized.

    Overriden and disabled by Shopsanity option above.
    """
    display_name = "Random Weapon Shops"

class RandomWeaponPrices(Toggle):
    """
    The prices of weapons in shops will be randomized.
    """
    display_name = "Random Weapon Prices"

class HealHurtBeforeMore(Toggle):
    """ 
    HEAL must come before HEALMORE; HURT before HURTMORE. This option only does something if you have Random Spell Learning on
    """
    display_name = "HealHurt Before More"

class RandomXPRequirements(Toggle):
    """ 
    Experience requirements for each level will be randomized
    """
    display_name = "Random XP Requirements"

class EnableMenuWrapping(DefaultOnToggle):
    """ 
    This enables cursor wrapping in menus
    """
    display_name = "Enable Menu Wrapping"

class EnableDeathNecklace(DefaultOnToggle):
    """ 
    Equipping the death necklace will give +10AP and -25% HP
    """
    display_name = "Enable Death Necklace"

class EnableBattleTorches(DefaultOnToggle):
    """ 
    Torches and Fairy water can be thrown at monsters
    """
    display_name = "Enable Torches in Battle"

class RepelInDungeons(DefaultOnToggle):
    """ 
    Enables REPEL to work in dungeons
    """
    display_name = "Repel in Dungeons"

class PermanentRepel(Toggle):
    """ 
    REPEL will always be active
    """
    display_name = "Permanent Repel"

class PermanentTorch(Toggle):
    """ 
    At least a 3x3 area will always be lit in dungeons
    """
    display_name = "Permanent Torch"

class RandomMonsterAbilities(Toggle):
    """ 
    Monster spells and abilities will be randomized
    """
    display_name = "Random Monster Abilities"

class RandomMonsterZones(Toggle):
    """ 
    Monster encounters in each zone will be randomized
    """
    display_name = "Random Monster Zones"

class RandomMonsterStats(Toggle):
    """ 
    Monster strength, agility, and HP will be randomized
    """
    display_name = "Random Monster Stats"

class RandomMonsterXP(Toggle):
    """ 
    The XP and GOLD gained from monsters will be randomized
    """
    display_name = "Random Monster XP & Gold"

class MakeRandomStatsConsistent(Toggle):
    """ 
    This makes the random stats, XP, and GOLD consistent with one another
    """
    display_name = "Make Random Stats Consistent"

class ScaredMetalSlimes(Toggle):
    """ 
    Metal Slimes will always have a chance to run
    """
    display_name = "Scared Metal Slimes"

class ScaledMetalSlimeXP(Toggle):
    """ 
    Metal Slime XP will depend on your current level
    """
    display_name = "Scaled Metal Slime XP"

class FastText(Toggle):
    """ 
    All text will progress much faster
    """
    display_name = "Fast Text"

class SpeedHacks(Toggle):
    """ 
    Various aspects of the game will be much faster
    """
    display_name = "Speed Hacks"

# class ShortCharlock(Toggle):
#     """
#     Charlock Dungeon will be much shorter
#     """
#     display_name = "Short Charlock"

class SummerSale(Toggle):
    """
    All weapons and armor 35-65% off!
    """
    display_name = "Summer Sale"

class LevellingSpeed(Choice):
    """ 
    Determines how fast you level up
    """
    display_name = "Levelling Speed"
    option_normal = 0
    option_fast = 1
    option_very_fast = 2
    default = 1

class NoHurtMore(Toggle):
    """ 
    You will never learn HURTMORE. Monsters can still have it. This only works with Randomized Spells on
    """
    display_name = "No Hurtmore"

class OnlyHealmore(Toggle):
    """ 
    Never learn any spell other than this. This only works with Randomized Spells on
    """
    display_name = "Only Healmore"

class Level1Radiant(Toggle):
    """ 
    If spells are randomized, makes sure the hero always knows Radiant. Overrides 'Only Healmore'
    """
    display_name = "Level 1 Radiant"

class Level1Repel(Toggle):
    """ 
    If spells are randomized, makes sure the hero always knows Repel. Overrides 'Only Healmore'
    """
    display_name = "Level 1 Repel"

class NoNumbers(Toggle):
    """ 
    No numbers will be visible until the Dragonlord fight
    """
    display_name = "No Numbers"

class InvisibleHero(Toggle):
    """ 
    Your sprite will be invisible
    """
    display_name = "Invisible Hero"

class InvisibleNPCs(Toggle):
    """ 
    All NPCs will be invisible
    """
    display_name = "Invisible NPCs"

class BonkDamage(Choice):
    """
    Bonking into walls will deal damage!
    """
    display_name = "Bonk Damage"
    option_none = 0
    option_1_hp = 1
    option_2_hp = 2
    option_20_hp = 3
    option_instakill = 4
    option_random_damage = 5
    option_halve_health = 6
    default = 0

class EasyCharlock(Toggle):
    """ 
    Make it slightly easier to run from high level monsters
    """
    display_name = "Easy Charlock"

class ShuffleMusic(Toggle):
    """ 
    Music in each area will be randomized
    """
    display_name = "Shuffle Music"

class DisableMusic(Toggle):
    """ 
    This disables the game music in most situations
    """
    display_name = "Disable Music"

class ModernSpellNames(DefaultOnToggle):
    """ 
    Use spell names from more recent DQ releases
    """
    display_name = "Modern Spell Names"

class ShowDeathCounter(Toggle):
    """ 
    The stats window will also have a death counter
    """
    display_name = "Show Death Counter"

class DisableSpellFlashing(Toggle):
    """ 
    Prevents the screen from flashing when you cast spells
    """
    display_name = "Disable Spell Flashing"

class SkipOriginalCredits(Toggle):
    """ 
    Skip the original credits and go straight to stat scroll
    """
    display_name = "Skip Original Credits"

class NoirMode(Toggle):
    """ 
    It's all black and white baby!
    """
    display_name = "Noir Mode"

class ReturnEscapes(Toggle):
    """ 
    Return can be used in battle for a guaranteed escape
    """
    display_name = "Return Escapes"

class ReturnToTown(Toggle):
    """ 
    Wings and Return send you to the last place you saved or used an inn at
    """
    display_name = "Return to Town"

class WarpWhistle(Toggle):
    """ 
    The Fairy Flute will work as a warp whistle outside of battle, cycling between places you saved or used an inn at
    """
    display_name = "Warp Whistle"

class LevelupRefill(Toggle):
    """ 
    Have HP and MP refilled afater levelling up
    """
    display_name = "Levelup Refill"

class AsceticKing(DefaultOnToggle):
    """
    King Lorik will let the player keep their hard-earned gold upon dying.
    """
    display_name = "Ascetic King"

class RunMechanics(Choice):
    """
    Change how a successful run is determined.

    DW 1: Vanilla run mechanics
    Safer DW 1: Vanilla run mechanics, 4th run attempt guaranteed
    DW 2: 2/3 chance to run away at every attempt
    DW 4: 1st attempt: 50%, 2nd attempt: 50%, 3rd attempt: 75%, 4th attempt, 100%
    """
    display_name = "Run Mechanics"
    option_dw1 = 0
    option_safer_dw1 = 1
    option_dw2 = 2
    option_dw4 = 3
    default = 0

class CharlockInn(Toggle):
    """ 
    Make the final dive easier by having a comfy bed and breakfast at the Dragonlord's
    """
    display_name = "Charlock Inn"

class DL1Crits(Toggle):
    """ 
    Allow excellent moves against the Dragonlord's 1st form
    """
    display_name = "DL1 Crits"

class DL2Crits(Toggle):
    """ 
    Allow excellent moves against the Dragonlord's 2nd form
    """
    display_name = "DL2 Crits"

class MagicHerbs(Toggle):
    """
    Make herbs refill MP rather than HP
    """
    display_name = "Magic Herbs"

class NormalFluteSpeed(DefaultOnToggle):
    """
    If Speed Hacks is on, the Fairy Flute music will not be sped up
    """
    display_name = "Normal Flute Speed"

class DisableRedFlashes(Toggle):
    """
    Prevents the screen from flashing when walking on damage tiles
    """
    display_name = "Disable Red Flashes"

DWOptionGroups = [
    OptionGroup("Archipelago Options", [
        LevelSanity,
        LevelSanityRange,
        SearchSanity,
        ShopSanity,
        MonsterSanity,
        DeathLink
    ]),
    OptionGroup("Random Options", [
        RandomGrowth,
        RandomMap,
        RandomMapSize,
        RandomSpellLearning,
        RandomWeaponShops,
        RandomWeaponPrices,
        HealHurtBeforeMore, 
        RandomXPRequirements,
        RandomMonsterAbilities,
        RandomMonsterZones,
        RandomMonsterStats,
        RandomMonsterXP,
        MakeRandomStatsConsistent
    ]),
    OptionGroup("Challenge Options", [
        ScaredMetalSlimes,
        ScaledMetalSlimeXP,
        NoHurtMore,
        OnlyHealmore,
        NoNumbers,
        InvisibleHero,
        InvisibleNPCs,
        BonkDamage
    ]),
    OptionGroup("QOL Options", [
        EnableMenuWrapping,
        EnableDeathNecklace,
        EnableBattleTorches,
        RepelInDungeons,
        PermanentRepel,
        PermanentTorch,
        FastText,
        SpeedHacks,
        SummerSale,
        LevellingSpeed,
        Level1Radiant,
        Level1Repel,
        EasyCharlock,
        ModernSpellNames,
        SkipOriginalCredits,
        ReturnEscapes,
        ReturnToTown,
        WarpWhistle,
        LevelupRefill,
        AsceticKing,
        RunMechanics,
        CharlockInn,
        DL1Crits,
        DL2Crits
    ]),
    OptionGroup("Other Options", [
        ShuffleMusic,
        DisableMusic,
        ShowDeathCounter,
        DisableSpellFlashing,
        DisableRedFlashes,
        NoirMode,
        MagicHerbs,
        NormalFluteSpeed
    ])
]

@dataclass
class DWOptions(PerGameCommonOptions):
    levelsanity: LevelSanity
    levelsanity_range: LevelSanityRange
    searchsanity: SearchSanity
    shopsanity: ShopSanity
    monstersanity: MonsterSanity
    death_link: DeathLink

    random_growth: RandomGrowth
    random_map: RandomMap
    random_map_size: RandomMapSize
    random_spell_learning: RandomSpellLearning
    random_weapon_shops: RandomWeaponShops
    random_weapon_prices: RandomWeaponPrices
    heal_hurt_before_more: HealHurtBeforeMore
    random_xp_requirements: RandomXPRequirements
    random_monster_abilities: RandomMonsterAbilities
    random_monster_zones: RandomMonsterZones
    random_monster_stats: RandomMonsterStats
    random_monster_xp: RandomMonsterXP
    make_random_stats_consistent: MakeRandomStatsConsistent

    scared_metal_slimes: ScaredMetalSlimes
    scaled_metal_slime_xp: ScaledMetalSlimeXP
    no_hurtmore: NoHurtMore
    only_healmore: OnlyHealmore
    no_numbers: NoNumbers
    invisible_hero: InvisibleHero
    invisible_npcs: InvisibleNPCs
    bonk_damage: BonkDamage

    enable_menu_wrapping: EnableMenuWrapping
    enable_death_necklace: EnableDeathNecklace
    enable_battle_torches: EnableBattleTorches
    repel_in_dungeons: RepelInDungeons
    permanent_repel: PermanentRepel
    permanent_torch: PermanentTorch
    fast_text: FastText
    speed_hacks: SpeedHacks
    summer_sale: SummerSale
    levelling_speed: LevellingSpeed
    level_1_radiant: Level1Radiant
    level_1_repel: Level1Repel
    easy_charlock: EasyCharlock
    modern_spell_names: ModernSpellNames
    skip_original_credits: SkipOriginalCredits
    return_escapes: ReturnEscapes
    return_to_town: ReturnToTown
    warp_whistle: WarpWhistle
    levelup_refill: LevelupRefill
    ascetic_king: AsceticKing
    run_mechanics: RunMechanics
    charlock_inn: CharlockInn
    dl1_crits: DL1Crits
    dl2_crits: DL2Crits

    shuffle_music: ShuffleMusic
    disable_music: DisableMusic
    show_death_counter: ShowDeathCounter
    disable_spell_flashing: DisableSpellFlashing
    disable_red_flashes: DisableRedFlashes
    noir_mode: NoirMode
    magic_herbs: MagicHerbs
    normal_flute_speed: NormalFluteSpeed