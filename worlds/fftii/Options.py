from dataclasses import dataclass

from Options import Range, PerGameCommonOptions, OptionGroup, StartInventoryPool, DefaultOnToggle, Toggle, Choice, \
    Visibility


# Main Options
class ZodiacStonesInPool(Range):
    """How many Zodiac Stones will be in the item pool.
    If set to less than the number required, will instead become however many are required."""
    display_name = "Zodiac Stones in Pool"
    range_start = 1
    range_end = 13
    default = 6

class ZodiacStonesRequired(Range):
    """How many Zodiac Stones will be required to beat the game."""
    display_name = "Zodiac Stones Required"
    range_start = 1
    range_end = 13
    default = 6

class ZodiacStoneLocations(Choice):
    """Where can Zodiac Stones appear?
    Vanilla limits their possible locations to those events which had one in the vanilla game. Note that this limits
    the number of stones in the pool to 11, with sidequests on, and 8 without.
    Anywhere Local means stones can be at any location in your world.
    Anywhere means stones can be anywhere in the multiworld."""
    display_name = "Zodiac Stone Locations"
    option_vanilla_stones = 0
    option_anywhere_local = 1
    option_anywhere = 2
    default = 0

class FinalBattles(Choice):
    """What the final goal is.
    Vanilla requires the completion of all six final battles in sequence at Murond Death City.
    Altima Only requires only Altima at Murond Death City, and the other endgame battles will be located at Orbonne."""
    display_name = "Final Battles"
    option_vanilla = 0
    option_altima_only = 1
    default = 0

class SidequestBattles(DefaultOnToggle):
    """Are sidequest battles (Colliery, Nelveska, Zarghidas, Deep Dungeon) in the pool of locations?"""
    display_name = "Sidequest Battles"

class JobUnlocks(DefaultOnToggle):
    """Are job unlocks in the item and location pools?"""
    display_name = "Job Unlocks"

class RareBattles(Toggle):
    """Are the rare battles for each battleground in the location pool?"""
    display_name = "Rare Battles"

class PoachLocations(Toggle):
    """Are poaches in the location pool? WARNING: Can be grindy and RNG-heavy."""
    display_name = "Poach Locations"

class LogicalDifficulty(Choice):
    """Affects the placement of logically required shop levels and jobs in the multiworld."""
    display_name = "Logical Difficulty"
    option_easy = 0
    option_normal = 1
    option_difficult = 2
    option_extreme = 3
    default = 1

# Item options
class ChemistPlacement(Choice):
    """Where Chemist is placed in the multiworld when Job Unlocks are enabled.
    Starting will have you start with Chemist.
    Early will ensure Chemist is one of your first items in the multiworld.
    Shuffled will shuffle Chemist into the pool like other jobs."""
    display_name = "Chemist Placement"
    option_starting = 0
    option_early = 1
    option_shuffled = 2
    default = 1

class EarlyPass(DefaultOnToggle):
    """Will a Pass for a neighboring region be an early item?"""
    display_name = "Early Pass"

class StartingShopLevel(Range):
    """The starting shop level of your game."""
    display_name = "Starting Shop Level"
    range_start = 0
    range_end = 14
    default = 0

# Filler item options
class NormalItemWeight(Range):
    """Weight of items normally sold in shops in the filler pool."""
    display_name = "Normal Item Weight"
    range_start = 0
    range_end = 10
    default = 3

class RareItemWeight(Range):
    """Weight of items not normally sold in shops in the filler pool."""
    display_name = "Rare Item Weight"
    range_start = 0
    range_end = 10
    default = 1

class BonusGilItemWeight(Range):
    """Weight of bonus items in the filler pool."""
    display_name = "Bonus Gil Item Weight"
    range_start = 0
    range_end = 10
    default = 2

class JPBoonItemWeight(Range):
    """Weight of JP Boon items that award JP to the team in the filler pool"""
    display_name = "JP Boon Item Weight"
    range_start = 0
    range_end = 10
    default = 1

class BonusGilItemSize(Choice):
    """Adjusts the value of bonus gil items in the pool.
    Normal is 5000/10000/40000. Frugal halves that, Expensive doubles."""
    display_name = "Bonus Gil Item Size"
    option_frugal = 0
    option_normal = 1
    option_expensive = 2
    default = 1

class JPBoonSize(Choice):
    """Adjusts the value of JP Boon items. Normal is 50/100/250 JP. Frugal halves that, Expensive doubles."""
    display_name = "JP Boon Item Size"
    option_frugal = 0
    option_normal = 1
    option_expensive = 2
    default = 1

# QoL options

class EXPGainMultiplier(Choice):
    """Multiplier to in-battle EXP gains."""
    display_name = "EXP Gain Multiplier"
    option_normal = 0
    option_double = 1
    option_quadruple = 2
    default = 1

class JPGainMultiplier(Choice):
    """Multiplier to in-battle JP gains."""
    display_name = "JP Gain Multiplier"
    option_normal = 0
    option_double = 1
    option_quadruple = 2
    default = 1

# Enemy rando options

class EnemyRandomizer(Choice):
    """Randomizes enemies.
    Disabled leaves enemies as vanilla.
    Limited randomizes only bosses with bosses.
    Simple randomizes only generics (both humans and monsters) with generics.
    Advanced randomizes all unique units and all generics with their categories.
    Complex randomizes both generic and special units with each other."""
    display_name = "Enemy Randomizer"
    option_disabled = 0
    option_limited = 1
    option_simple = 2
    option_advanced = 3
    option_complex = 4
    default = 0
    visibility = Visibility.none

class CrossEnemyRandomizer(Toggle):
    """If enabled, randomized humans can become monster units and vice versa."""
    display_name = "Cross Enemy Randomizer"
    visibility = Visibility.none

class RandomizeStoryFightsOnly(Toggle):
    """If enabled, only story and sidequest fights will be randomized,
    and random encounters will be left alone"""
    display_name = "Randomize Story Fights Only"
    visibility = Visibility.none

class EnemyRandomizerLocality(Choice):
    """Controls the scope of enemy randomization.
    Battle randomizes enemy units of the same job differently per battle.
    Region randomizes enemy units of the same job differently per region.
    Global randomizes all enemy units in the game of the same job to the same randpmized job."""
    display_name = "Enemy Randomizer Locality"
    option_battle = 0
    option_region = 1
    option_global = 2
    default = 0
    visibility = Visibility.none

class LucaviRandomizer(Choice):
    """Controls if Lucavi and Altima are included in randomization.
    Disabled leaves Lucavi (Queklain, Velius, Zalera, Adramelk, Hashmalum, Elidibs) the same as vanilla.
    Lucavi enables those locations and jobs to be included in randomization.
    Include Altima also includes Altima 1 and 2 in the randomization. Will cause graphical glitches."""
    display_name = "Lucavi Randomizer"
    option_disabled = 0
    option_lucavi = 1
    option_include_altima = 2
    default = 0
    visibility = Visibility.none

class EnemyRandomizerMethod(Choice):
    """Controls the randomization method for determining randomized units.
    Shuffle disallows duplicate randomized units in the chosen locality.
    Chaos allows duplicate randomized units in the chosen locality."""
    display_name = "Enemy Randomizer Method"
    option_shuffle = 0
    option_chaos = 1
    default = 0
    visibility = Visibility.none

# Unused options
class StartingRegion(Choice):
    """What region to start in. Gallione is easiest, followed by Lesalia and Lionel. Fovoham, Zeltennia, and Limberry
    should only be chosen if you're looking for a challenge."""
    display_name = "Starting Region"
    option_gallione = 0
    option_lesalia = 1
    option_lionel = 2
    option_fovoham = 3
    option_zeltennia = 4
    option_limberry = 5
    default = 0

@dataclass
class FinalFantasyTacticsIIOptions(PerGameCommonOptions):
    zodiac_stones_in_pool: ZodiacStonesInPool
    zodiac_stones_required: ZodiacStonesRequired
    zodiac_stone_locations: ZodiacStoneLocations
    final_battles: FinalBattles
    sidequest_battles: SidequestBattles
    job_unlocks: JobUnlocks
    rare_battles: RareBattles
    poach_locations: PoachLocations
    logical_difficulty: LogicalDifficulty
    chemist_placement: ChemistPlacement
    early_pass: EarlyPass
    starting_shop_level: StartingShopLevel
    normal_item_weight: NormalItemWeight
    rare_item_weight: RareItemWeight
    bonus_gil_item_weight: BonusGilItemWeight
    jp_boon_item_weight: JPBoonItemWeight
    bonus_gil_item_size: BonusGilItemSize
    jp_boon_size: JPBoonSize
    enemy_randomizer: EnemyRandomizer
    cross_enemy_randomizer: CrossEnemyRandomizer
    randomize_story_fights_only: RandomizeStoryFightsOnly
    enemy_randomizer_locality: EnemyRandomizerLocality
    lucavi_randomizer: LucaviRandomizer
    enemy_randomizer_method: EnemyRandomizerMethod
    exp_gain_multiplier: EXPGainMultiplier
    jp_gain_multiplier: JPGainMultiplier
    start_inventory_from_pool: StartInventoryPool

fftii_option_groups = [
    OptionGroup("Main Options", [
        ZodiacStonesInPool,
        ZodiacStonesRequired,
        ZodiacStoneLocations,
        FinalBattles,
        SidequestBattles,
        JobUnlocks,
        PoachLocations,
        RareBattles,
        LogicalDifficulty
    ]),
    OptionGroup("Item Options", [
        ChemistPlacement,
        EarlyPass,
        StartingShopLevel
    ]),
    OptionGroup("Filler Options", [
        NormalItemWeight,
        RareItemWeight,
        BonusGilItemWeight,
        JPBoonItemWeight,
        BonusGilItemSize,
        JPBoonSize
    ]),
    # OptionGroup("Enemy Randomizer Options", [
    #     EnemyRandomizer,
    #     CrossEnemyRandomizer,
    #     RandomizeStoryFightsOnly,
    #     EnemyRandomizerLocality,
    #     LucaviRandomizer,
    #     EnemyRandomizerMethod
    # ]),
    OptionGroup("QOL Options", [
        EXPGainMultiplier,
        JPGainMultiplier
    ])
]