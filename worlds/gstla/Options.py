from dataclasses import dataclass
from enum import IntEnum, auto
from Options import Choice, Toggle, Range, NamedRange, PerGameCommonOptions

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
    """When enabled the items are visible on the floor. This allows for scouting items. Mimics are removed when this option is enabled
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
    Randomized will roll each stat separately
    """
    display_name = "Character Stats Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2
    default = 0

class CharEleShuffle(Choice):
    """Determine how character elements are shuffled
    Vanilla leaves character elements as per the vanilla game
    Shuffled will shuffle them between characters
    Randomized will roll each element separately
    """
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2
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
    option_randomized = 2
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
    option_fixed = 2
    default = 1

class DisableCurses(Toggle):
    """When enabled, curses are removed"""
    display_name = "Remove Curses"

class AvoidPatch(Toggle):
    """When enabled, Avoid always succeeds and will disable encounters. Using it again will enable encounters"""
    display_name = "Avoid Patch"

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

class NamedPuzzles(Choice):
    """Determines how the named puzzles will generate. These include the puzzles for Gambomba Statue, Gaia Rock and Trial Road
    Vanilla uses the name that is given to Felix
    Fixed will force the puzzles to use the name 'Felix'
    Randomized will force the puzzles to be a random name"""
    display_name = "Named Puzzles"
    option_vanilla = 0
    option_fixed = 1
    option_randomized = 2

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

class AnemosAccess(Choice):
    """Determine accesss to Anemos Inner Sanctun
    Vanilla requires all Djinn to be able to enter Anemos Inner Sanctum
    Random will select a value between 16 to 28 Djinn to be able to access Anemos Inner Sanctum
    Open allows you to enter Anemos Inner Sanctum without any Djinn
    """
    display_name = "Anemos Inner Sanctum Access"
    option_vanilla = 0
    option_randomized = 1
    option_open = 2
    default = 0

@dataclass
class GSTLAOptions(PerGameCommonOptions):
    #Pool and Logic settings
    item_shuffle: ItemShuffle #todo, bug with hidden items, maybe support for key items only mode?
    major_minor_split: MajorMinorSplit #todo, progressive items to mayjor / key item locations, minor junky stuff
    reveal_hidden_item: RevealHiddenItem
    omit_locations: OmitLocations
    add_elvenshirt_clericsring: AddGs1Items #todo

    lemurian_ship: StartWithShip
    start_with_wings_of_anemos: ShipWings #todo, logic and event item
    anemos_inner_sanctum_access: AnemosAccess
    shuffle_characters: CharacterShuffle

    #Char And Class Settings
    character_stats: CharStatShuffle
    character_elements: CharEleShuffle

    no_util_psynergy_from_classes: NoLearningUtilPsy
    randomize_class_stat_boosts: ShuffleClassStats
    class_psynergy: ClassPsyShuffle
    psynergy_levels: ClassPsyLevels

    #Psynerg Settings
    adjust_psynergy_power: ShufflePsyPower
    adjust_psynergy_cost: ShufflePsyCost
    randomize_psynergy_aoe: ShufflePsyAoe

    adjust_enemy_psynergy_power: ShuffleEnemyPsyPower
    randomize_enemy_psynergy_aoe: ShuffleEnemyPsyAoe
    enemy_elemental_resistance: EnemyEResShuffle

    start_with_healing_psynergy: StartWithHealPsy
    start_with_revive: StartWithRevivePsy
    start_with_reveal: StartWithRevealPsy #todo, reveal as starter item, remove from pool

    #Djinn and Summon Settings
    shuffle_djinn: DjinnShuffle
    djinn_logic: DjinnLogic
    shuffle_djinn_stat_boosts: ShuffleDjinnStats
    adjust_djinn_attack_power: ShuffleDjinnPower
    randomize_djinn_attack_aoe: ShuffleDjinnAoe
    scale_djinni_battle_difficulty: ScaleWildDjinn

    randomize_summon_costs: ShuffleSummonCosts
    adjust_summon_power: ShuffleSummonPower

    #Equipment Settings
    randomize_equip_compatibility: ShuffleEqCompatibility
    adjust_equip_prices: ShuffleEqPrices
    adjust_equip_stats: ShuffleEqStats
    shuffle_weapon_attack: ShuffleAttack
    shuffle_weapon_effect: ShuffleWpnUnleash
    shuffle_armour_defense: ShuffleDefense
    shuffle_armour_effect: ShuffleArmEffect
    randomize_curses: ShuffleEqCurses
    remove_all_curses: DisableCurses

    #Misc
    show_items_outside_chest: VisibleItems
    free_avoid: FreeAvoid
    free_retreat: FreeRetreat
    #qol-hints not supported yet
    scale_exp: ScaleExpGained
    scale_coins: ScaleGoldGained
    starting_levels: StartLevels
    sanctum_revive_cost: SanctuaryResCost
    avoid_always_works: AvoidPatch
    enable_hard_mode: EnableHardMode
    reduced_encounter_rate: HalveEncounterRate
    easier_bosses: EasierBosses
    name_puzzles: NamedPuzzles
    manual_retreat_glitch: ManualRetreatGlitch
    shuffle_music: MusicShuffle
    teleport_to_dungeons_and_towns: TelportEverywhere
    force_boss_required_checks_to_nonjunk: ForceBossDrops
    prevent_superboss_locked_check_to_progression: ForceSuperBossJunk