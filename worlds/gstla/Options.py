from dataclasses import dataclass
from Options import Choice, Toggle, Range, NamedRange, PerGameCommonOptions

class StartWithShip(Choice):
    """What needs to be done to get the ship?
    Vanilla requires getting the black crystal and completing the gabomba statue to get the reward from Madras Mayor.
    Ship Door Unlocked involves getting the black crystal and activating the ship as per vanilla.
    Available from the start allows you to use the ship from the beginning of the game.
    """
    display_name = "Lemurian Ship"
    option_vanilla = 0
    option_ship_door_unlocked = 1
    option_available_from_start = 2
    default = 0

class CharacterShuffle(Choice):
    """Where can you find the other characters?
    Vanilla makes it like the vanilla experience.
    Vanilla Shuffled puts the characters in eachothers locations.
    Anywhere puts the characters in the multiworld itempool, 
    note that Jenna's character location is forced to be a character due to game limiations with psynergy learning.
    """
    display_name = "Character Shuffle"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_anywhere = 2
    default = 1


class SecondStartingCharacter(Choice):
    """Which character will join Felix on Idejima?
    This will always be Jenna when Character Shuffle is set to Vanilla, otherwise it will be whichever character this is set to.
    """
    display_name = "Second Starting Character"
    option_jenna = 0
    option_sheba= 1
    option_piers = 2
    option_isaac = 3
    option_garet = 4
    option_ivan = 5
    option_mia = 6
    default = 1

class DjinnLogic(NamedRange):
    """How much do Djinn affect logic for being able to defeat bosses?
    Assuming this is set to 100 (Normal) beating Briggs expects 6 djinn, Poseidon 24 djinn and Doom Dragon 56 djinn.
    Dullahan goes up to 72 (All Djinn in the game). Setting this to 50 (Hard) will halve all of these numbers and 0 will remove the requirement completely.
    """
    display_name = "Djinn Logic"
    range_start = 0
    range_end = 100
    default = 100

    special_range_names = {
        "normal": 100,
        "hard": 50,
        "none": 0
    }

class RevealHiddenItem(Toggle):
    """Require Reveal to be able to logically access hidden items.
    Note that most hidden items can be gotten regardless of having Reveal or not.
    Also there are a few locations that hard require Reveal to be obtainable, this setting does not alter those.
    """
    display_name = "Reveal Hidden Items"
    default = 1

class ItemShuffle(Choice):
    """Determine which locations in the game are part of the pool.
    All Chests and Tablets includes all chests and tablets and does not include hidden items from pots, barrels, dug up.
    All Locations includes everything from the vanilla game, including hidden items in pots, barrels, scooped up, covered in leaves or on the overworld."""
    display_name = "Item Shuffle"
    option_all_chests_and_tablets = 2
    option_all_items = 3
    default = 2

class OmitLocations(Choice):
    """Choose to omit locations containing optional harder boss fights
    No Omission keeps all super bosses in play.
    Omit Anemos Inner Sanctum omits Anemos Inner Sanctum.
    Omit Superbosses and Inner Sanctum omits all super bosses and Anemos Inner Sanctum.
    """
    option_no_omission = 0
    option_omit_anemos_inner_sanctum = 1
    option_omit_superbosses_and_inner_sancutm = 2
    default = 2

class AddGs1Items(Toggle):
    """Adds the Elven Shirt and Cleric's Ring from Golden Sun to the item pool.
    """
    display_name = "Add Elven Shirt and Cleric's ring"

class AddDummyItems(Toggle):
    """Adds a variety of items that are normally unobtainable through normal means in the game.
    These are: Casual Shirt, Golden Boots, Aroma Ring, Golden Shirt, Ninja Sandals, Golden Ring, 
    Herbed Shirt, Knight's Greave, Rainbow Ring, Divine Camisole, Silver Greave and Soul Ring"""

class VisibleItems(Toggle):
    """Chests and Tablets are replaced with their contents on the floor.
    This allows for scouting items. Mimics are removed when this option is enabled.
    Note certain locations are still not visible, for example hidden items in pots or barrels.
    """
    display_name = "Show items outside chest"
    default = 1

class IncludeMimics(Toggle):
    """Some locations may now contain a mimic instead. Due to some limitations they only drop their vanilla item. 
    Note that this will be ignored if items are visible outside of chests.
    """
    display_name = "Include mimics"
    default = 0

class NoLearningUtilPsy(Toggle):
    """Prevents utility Psynergy (Growth, Frost, etc.) from being learned by classes.
    """
    display_name = "No utility Psynergy from classes"
    default = 1

class RandomizeClassStatBoosts(Toggle):
    """When enabled the base stats for classes are randomized"""
    display_name = "Randomize class stat boosts"

class RandomizeEqCompatibility(Toggle):
    """When enabled the compatability for each equipment piece is randomized. 
    Compatibility defines what each character can equip."""
    display_name = "Shuffle Equipment Compatability"

class AdjustEqPrices(Toggle):
    """When enabled the price for each equipment piece is randomized within a margin of vanilla."""
    display_name = "Adjust Equipment Prices"

class AdjustEqStats(Toggle):
    """When enabled the stats for each equipment piece is randomized within a margin of vanilla."""
    display_name = "Adjust Equipment Stats"

class ShuffleWpnEffects(Toggle):
    """When enabled the effects for weapons are shuffled amongst eachother."""
    display_name = "Shuffle Weapon Effects"

class ShuffleArmEffect(Toggle):
    """When enabled the bonus effects for armour are shuffled amongst eachother."""
    display_name = "Shuffle Armour Effects"

class RandomizeEqCurses(Toggle):
    """When enabled the curses for equipment are randomized."""
    display_name = "Randomize Curses"

class AdjustPsyPower(Toggle):
    """When enabled the power of Psynergy is randomized within a margin of vanilla."""
    display_name = "Adjust Psynergy Power"

class DjinnShuffle(Choice):
    """How djinn should be placed in the multiworld.
    Note currently Djinn can only be placed in other djinn locations in their own world due to game limitations.
    """
    display_name = "Shuffle Djinn"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    #option_anywhere = 2, not supported yet
    default = 1

class ShuffleDjinnStats(Toggle):
    """When enabled the stats a djinn grant are shiffled amongst eachother."""
    display_name = "Shuffle Djinn stat boosts"

class AdjustDjinnPower(Toggle):
    """When enabled the attack power of djinn are randomized within a margin of vanilla."""
    display_name = "Adjust Djinn attack power"

class RandomizeDjinnAoe(Toggle):
    """When enabled the Area of Effect of djinn used in battle is randomized."""
    display_name = "Randomize Djinn Area of Effect"

class ScaleDjinnBattleDifficulty(Toggle):
    """Adjust Djinn battle difficulty based on number of owned Djinn."""
    display_name = "Scale Djinn battle difficulty"

class RandomizeSummonCosts(Toggle):
    """When enabled the costs for Summons is randomized."""
    display_name = "Randomize Summon costs"

class AdjustSummonPower(Toggle):
    """when enabled the power of Summons is randomized within a margin of vanilla."""
    display_name = "Adjust Summon Power"

class CharStatShuffle(Choice):
    """Determine the stats for characters
    Vanilla leaves the stats as per the vanilla game.
    Shuffle character stats will shuffle stats between characters.
    Adjust character stats will randomize stats for each character within a margin of vanilla.
    """
    display_name = "Character Stats Shuffle"
    option_vanilla = 0
    option_shuffle_character_stats = 1
    option_adjust_character_stats = 2
    default = 2

class CharEleShuffle(Choice):
    """Determine how character elements are shuffled
    Vanilla leaves character elements as per the vanilla game
    Shuffle character leements will shuffle them between characters
    Randomize character elements will randomize each characters element
    """
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_shuffle_character_elements = 1
    option_randomize_character_elements = 2
    default = 2

class AdjustPsyCost(Toggle):
    """When enabled the PP cost of Psynergy is randomized within a margin of vanilla."""
    display_name = "Adjust Psynergy PP Cost"

class RandomizePsyAoe(Toggle):
    """When enabled the AoE of Psynergy is randomized"""
    display_name = "Randomize Psynergy AoE"

class AdjustEnemyPsyPower(Toggle):
    """When enabled the power of Enemy Psynergy is randomized within a margin of vanilla."""
    display_name = "Adjust Enemy Psynergy Power"

class RandomizeEnemyPsyAoe(Toggle):
    """When enabled the AoE of Enemy Psynergy is randomized."""
    display_name = "Randomize Enemy Psynergy AoE"

class ClassPsynergy(Choice):
    """Determine what Psynergy a class will learn
    Vanilla leaves the Psynergy on their vanilla classes
    Randomize Psynergy by classline
    Randomize them by Psynergy group
    Randomize them by Psynergy group with a preference to the same Element
    Randomize them by Psynergy Element
    Fully Randomize it will randomize it completely without grouping or preference
    """
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_randomize_by_classline = 1
    option_randomize_by_psynergy_group = 2
    option_randomize_by_psynergy_group_prefer_element = 5
    option_randomize_by_psynergy_element = 3
    option_fully_randomized = 4
    default = 2

class ClassPsynergyLevels(Choice):
    """Determine when Psynergy is learned
    Vanilla leaves the learning of Psynergy on the vanilla levels.
    Adjust Learning levels will randomize learning levels within a margin from vanilla.
    Randomize Learning Levels will randomize learning levels completely.
    """
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_adjust_learning_levels = 1
    option_randomize_learning_levels = 2
    default = 1

class FreeAvoid(Toggle):
    """When enabled, the Avoid Psynergy will cost no PP"""
    display_name = "Avoid costs no PP"

class FreeRetreat(Toggle):
    """When enabled, the Retreat Psynergy will cost no PP"""
    display_name = "Retreat costs no PP"

class ShuffleAttack(Toggle):
    """When enabled, the attack stat from weapons is shuffled amongst eachother"""
    display_name = "Shuffle weapon attack"

class StartWithHealPsynergy(Toggle):
    """Start the game with atleast one healing Psynergy (Cure, Ply, Wish or Aura)"""
    display_name = "Start with Healing Psynergy"

class StartWithRevivePsynergy(Toggle):
    """When enabled, start the game with Revive Psynergy"""
    display_name = "Start with Revive Psynergy"

class StartWithRevealPsynergy(Toggle):
    """When enabled, start the game with Reveal Psynergy"""
    display_name = "Start with Reveal Psynergy"

class ScaleExpGained(Range):
    """Scale how much Exp is earned by the party."""
    display_name = "Scale Exp"
    range_start = 1
    range_end = 15
    default = 3

class ScaleCoinsGained(Range):
    """Scale how much Coins are earned by the party."""
    display_name = "Scale Coins"
    range_start = 1
    range_end = 15
    default = 4

class ShuffleDefense(Toggle):
    """When enabled, the defense from equipment is shuffled amongst eachother"""
    display_name = "Shuffle armour defense"


class StartingLevels(Range):
    """Determine the starting levels for characters joining the party.
    Note this only increases levels of characters that are lower level than the party"""
    display_name = "Starting levels"
    range_start = 5
    range_end = 99
    default = 5

class EnemyEResShuffle(Choice):
    """Determine how Enemy Elemental Resistance is shuffled
    Vanilla leaves the elemental resistance as per the vanilla game.
    Shuffle elemental resistance will shuffle them between enemies.
    Randomize elemental resistance will randomize the resistances for each enemy.
    """
    display_name = "Enemy Elemental Resistance Shuffle"
    option_vanilla = 0
    option_shuffle_elemmental_res = 1
    option_randomize_elemental_res = 2
    default = 0

class SanctuaryReviveCost(Choice):
    """Determine how expensive the Sanctuary is to revive characters
    Vanilla leaves the cost per the vanilla game (20x level)
    Reduced will alter the cost to be cheaper than vanilla (2x level)
    Fixed will alter the cost to the same price throughout (100 coins)
    """
    display_name = "Sanctum revive cost"
    option_vanilla = 0
    option_reduced = 1
    option_fixed = 2
    default = 1

class RemoveCurses(Toggle):
    """When enabled, curses are removed."""
    display_name = "Remove all Curses"

class AvoidPatch(Toggle):
    """When enabled, Avoid always succeeds and will disable encounters. Using it again will enable encounters"""
    display_name = "Toggleable Avoid and always works"

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
    """When enabled, Hold select to trigger the Retreat glitch. Logic does not require or expect use of glitches to beat your seed,
    this purely gives more control to activating the glitch over draining your PP to than use it anyway."""
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
    item_shuffle: ItemShuffle
    major_minor_split: MajorMinorSplit
    reveal_hidden_item: RevealHiddenItem
    include_mimics: IncludeMimics
    omit_locations: OmitLocations
    add_elvenshirt_clericsring: AddGs1Items
    add_non_obtainable_items: AddDummyItems

    lemurian_ship: StartWithShip
    start_with_wings_of_anemos: ShipWings
    anemos_inner_sanctum_access: AnemosAccess
    shuffle_characters: CharacterShuffle
    second_starting_character: SecondStartingCharacter

    #Char And Class Settings
    character_stats: CharStatShuffle
    character_elements: CharEleShuffle

    no_util_psynergy_from_classes: NoLearningUtilPsy
    randomize_class_stat_boosts: RandomizeClassStatBoosts
    class_psynergy: ClassPsynergy
    psynergy_levels: ClassPsynergyLevels

    #Psynerg Settings
    adjust_psynergy_power: AdjustPsyPower
    adjust_psynergy_cost: AdjustPsyCost
    randomize_psynergy_aoe: RandomizePsyAoe

    adjust_enemy_psynergy_power: AdjustEnemyPsyPower
    randomize_enemy_psynergy_aoe: RandomizeEnemyPsyAoe
    enemy_elemental_resistance: EnemyEResShuffle

    start_with_healing_psynergy: StartWithHealPsynergy
    start_with_revive: StartWithRevivePsynergy
    start_with_reveal: StartWithRevealPsynergy

    #Djinn and Summon Settings
    shuffle_djinn: DjinnShuffle
    djinn_logic: DjinnLogic
    shuffle_djinn_stat_boosts: ShuffleDjinnStats
    adjust_djinn_attack_power: AdjustDjinnPower
    randomize_djinn_attack_aoe: RandomizeDjinnAoe
    scale_djinni_battle_difficulty: ScaleDjinnBattleDifficulty

    randomize_summon_costs: RandomizeSummonCosts
    adjust_summon_power: AdjustSummonPower

    #Equipment Settings
    randomize_equip_compatibility: RandomizeEqCompatibility
    adjust_equip_prices: AdjustEqPrices
    adjust_equip_stats: AdjustEqStats
    shuffle_weapon_attack: ShuffleAttack
    shuffle_weapon_effect: ShuffleWpnEffects
    shuffle_armour_defense: ShuffleDefense
    shuffle_armour_effect: ShuffleArmEffect
    randomize_curses: RandomizeEqCurses
    remove_all_curses: RemoveCurses

    #Misc
    show_items_outside_chest: VisibleItems
    free_avoid: FreeAvoid
    free_retreat: FreeRetreat
    #qol-hints not supported yet
    scale_exp: ScaleExpGained
    scale_coins: ScaleCoinsGained
    starting_levels: StartingLevels
    sanctum_revive_cost: SanctuaryReviveCost
    avoid_always_works: AvoidPatch
    enable_hard_mode: EnableHardMode
    reduced_encounter_rate: HalveEncounterRate
    easier_bosses: EasierBosses
    name_puzzles: NamedPuzzles
    manual_retreat_glitch: ManualRetreatGlitch
    shuffle_music: MusicShuffle
    teleport_to_dungeons_and_towns: TelportEverywhere