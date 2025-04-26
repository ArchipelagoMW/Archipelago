from Options import Choice, Toggle, Range, NamedRange, PerGameCommonOptions, StartInventoryPool
from dataclasses import dataclass

class StartWithShip(Choice):
    """What needs to be done to get the ship?
    Vanilla: requires getting the Black Crystal and completing the Gabomba Statue to get the reward from Madras Mayor to be able to enter the ship and activate it.
    Ship Door Unlocked: The ship door is unlocked but you still require to activate the ship by reaching the engine room. Black Crystal is no longer in the pool as it is not required.
    Available From The Start: allows you to use the ship from the beginning of the game. Black Crystal is no longer in the pool as it is not required.
    """
    internal_name = "lemurian_ship"
    display_name = "Lemurian Ship"
    option_vanilla = 0
    option_ship_door_unlocked = 1
    option_available_from_start = 2
    default = 1

class CharacterShuffle(Choice):
    """Where can you find the other characters?
    Vanilla: makes it like the vanilla experience.
    Vanilla Shuffled: puts the characters in each others locations.
    Anywhere: puts the characters in the multiworld itempool,
    note that Jenna's character location is forced to be a character due to game limiations with psynergy learning.
    """
    internal_name = "shuffle_characters"
    display_name = "Character Shuffle"
    option_vanilla = 0
    option_vanilla_shuffled = 1
    option_anywhere = 2
    default = 1


class SecondStartingCharacter(Choice):
    """Which character will join Felix on Idejima?
    This will always be Jenna when Character Shuffle is set to Vanilla, otherwise it will be whichever character this is set to.
    """
    internal_name = "second_starting_character"
    display_name = "Second Starting Character"
    option_jenna = 0
    option_sheba= 1
    option_piers = 2
    option_isaac = 3
    option_garet = 4
    option_ivan = 5
    option_mia = 6
    default = "random"

class ScaleCharacters(Toggle):
    """Whether to scale character levels by spheres.  Increases generation time."""
    internal_name = "scale_characters"
    display_name = "Scale Characters"
    default = 1

class MaxScaledLevel(Range):
    """The maximum level a scaled character should have.  Only valid if scale_characters is true."""
    internal_name = "max_scaled_level"
    display_name = "Max Scaled Level"
    range_start = 5
    range_end = 99
    default = 24

class DjinnLogic(NamedRange):
    """How much do Djinn affect logic for being able to defeat bosses?
    Assuming this is set to 100 (Normal) beating Briggs expects 6 djinn, Poseidon 24 djinn and Doom Dragon 56 djinn.
    Dullahan goes up to 72 (All Djinn in the game). Setting this to 50 (Hard) will halve all of these numbers and 0 will remove the requirement completely.
    """
    internal_name = "djinn_logic"
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
    internal_name = "reveal_hidden_item"
    display_name = "Reveal Required For Hidden Items"
    default = 1

class ItemShuffle(Choice):
    """Determine which locations in the game are part of the pool.
    All Chests and Tablets: includes all chests and tablets and does not include items from pots, barrels, dug up. Roughly 100 less locations to check from All Items
    All Items: includes everything from the vanilla game, including items in pots, barrels, scooped up, covered in leaves or on the overworld. Roughly 320 locations in total."""
    internal_name = "item_shuffle"
    display_name = "Item Shuffle"
    option_all_chests_and_tablets = 2
    option_all_items = 3
    default = 2

class OmitLocations(Choice):
    """Choose to omit locations containing optional harder boss fights
    No Omission: keeps all super bosses in play.
    Omit Anemos Inner Sanctum: omits Anemos Inner Sanctum. Removes roughly 4 locations from the pool.
    Omit Superbosses and Inner Sanctum: omits all super bosses and Anemos Inner Sanctum. Removes roughly 7 locations from the pool
    """
    internal_name = "omit_locations"
    display_name = "Omit Locations"
    option_no_omission = 0
    option_omit_anemos_inner_sanctum = 1
    option_omit_superbosses_and_inner_sanctum = 2
    default = 2

class AddGs1Items(Toggle):
    """Adds the Elven Shirt and Cleric's Ring from Golden Sun to the item pool.
    """
    internal_name = "add_elvenshirt_clericsring"
    display_name = "Add Elven Shirt and Cleric's ring"
    default = 1

class AddDummyItems(Toggle):
    """Adds a variety of items that are normally unobtainable through normal means in the game.
    These are: Casual Shirt, Golden Boots, Aroma Ring, Golden Shirt, Ninja Sandals, Golden Ring, 
    Herbed Shirt, Knight's Greave, Rainbow Ring, Divine Camisole, Silver Greave and Soul Ring"""
    internal_name = "add_non_obtainable_items"
    display_name = "Add Normally Unobtainable Equipment"
    default = 0

class VisibleItems(Toggle):
    """Chests and Tablets are replaced with their contents on the floor.
    This allows for scouting items. Note certain locations are still not visible,
    for example items in pots or barrels.
    """
    internal_name = "show_items_outside_chest"
    display_name = "Show items outside chest"
    default = 1

class NoLearningUtilPsy(Toggle):
    """Prevents utility Psynergy (Growth, Frost, etc.) from being learned by classes.
    """
    internal_name = "no_util_psynergy_from_classes"
    display_name = "No utility Psynergy from classes"
    default = 1

class RandomizeClassStatBoosts(Toggle):
    """When enabled the base stats for classes are randomized"""
    internal_name = "randomize_class_stat_boosts"
    display_name = "Randomize class stat boosts"
    default = 0

class RandomizeEqCompatibility(Toggle):
    """When enabled the compatability for each equipment piece is randomized. 
    Compatibility defines what each character can equip."""
    internal_name = "randomize_equip_compatibility"
    display_name = "Shuffle Equipment Compatability"
    default = 0

class AdjustEqPrices(Toggle):
    """When enabled the price for each equipment piece is randomized within a margin of vanilla."""
    internal_name = "adjust_equip_prices"
    display_name = "Adjust Equipment Prices"
    default = 0

class AdjustEqStats(Toggle):
    """When enabled the stats for each equipment piece is randomized within a margin of vanilla."""
    internal_name = "adjust_equip_stats"
    display_name = "Adjust Equipment Stats"
    default = 0

class ShuffleWpnEffects(Toggle):
    """When enabled the effects for weapons are shuffled amongst each other."""
    internal_name = "shuffle_weapon_effect"
    display_name = "Shuffle Weapon Effects"
    default = 0

class ShuffleArmEffect(Toggle):
    """When enabled the bonus effects for armour are shuffled amongst each other."""
    internal_name = "shuffle_armour_effect"
    display_name = "Shuffle Armour Effects"
    default = 0

class RandomizeEqCurses(Toggle):
    """When enabled the curses for equipment are randomized."""
    internal_name = "randomize_curses"
    display_name = "Randomize Curses"
    default = 0

class AdjustPsyPower(Toggle):
    """When enabled the power of Psynergy is randomized within a margin of vanilla."""
    internal_name = "adjust_psynergy_power"
    display_name = "Adjust Psynergy Power"
    default = 0

class DjinnShuffle(Choice):
    """How Djinn should be placed in your own world. The client has extra commands to help find which Djinni locations have (not) been checked.
    Note currently Djinn can only be placed in djinn locations in their own world due to game limitations.
    Vanilla keeps them in their vanilla locations.
    Vanilla Shuffled by Element, Djinni are placed in vanilla Djinni locations that share their element.
    Vanilla Shuffled are placed in any vanilla Djinni location regardless of element.
    """
    internal_name = "shuffle_djinn"
    display_name = "Shuffle Djinn"
    option_vanilla = 0
    option_vanilla_shuffled_by_element = 1
    option_vanilla_shuffled = 2
    #option_anywhere = 3, not supported yet
    default = 2

class ShuffleDjinnStats(Toggle):
    """When enabled the stats a djinn grant are shuffled amongst each other."""
    internal_name = "shuffle_djinn_stat_boosts"
    display_name = "Shuffle Djinn stat boosts"
    default = 1

class AdjustDjinnPower(Toggle):
    """When enabled the attack power of djinn are randomized within a margin of vanilla."""
    internal_name = "adjust_djinn_attack_power"
    display_name = "Adjust Djinn attack power"
    default = 0

class RandomizeDjinnAoe(Toggle):
    """When enabled the Area of Effect of djinn used in battle is randomized."""
    internal_name = "randomize_djinn_attack_aoe"
    display_name = "Randomize Djinn Area of Effect"
    default = 0

class ScaleDjinnBattleDifficulty(Toggle):
    """Adjust Djinn battle difficulty based on number of owned Djinn."""
    internal_name = "scale_djinni_battle_difficulty"
    display_name = "Scale Djinn battle difficulty"
    default = 1

class RandomizeSummonCosts(Toggle):
    """When enabled the costs for Summons is randomized."""
    internal_name = "randomize_summon_costs"
    display_name = "Randomize Summon costs"
    default = 0

class AdjustSummonPower(Toggle):
    """when enabled the power of Summons is randomized within a margin of vanilla."""
    internal_name = "adjust_summon_power"
    display_name = "Adjust Summon Power"
    default = 0

class CharStatShuffle(Choice):
    """Determine the stats for characters
    Vanilla: leaves the stats as per the vanilla game.
    Shuffle Character Stats: will shuffle stats between characters.
    Adjust Character Stats: will randomize stats for each character within a margin of vanilla.
    """
    internal_name = "character_stats"
    display_name = "Character Stats Shuffle"
    option_vanilla = 0
    option_shuffle_character_stats = 1
    option_adjust_character_stats = 2
    default = 2

class CharEleShuffle(Choice):
    """Determine how character elements are shuffled
    Vanilla: leaves character elements as per the vanilla game
    Shuffle Character Elements: will shuffle them between characters
    Randomize Character Elements: will randomize each characters element
    """
    internal_name = "character_elements"
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_shuffle_character_elements = 1
    option_randomize_character_elements = 2
    default = 1

class AdjustPsyCost(Toggle):
    """When enabled the PP cost of Psynergy is randomized within a margin of vanilla."""
    internal_name = "adjust_psynergy_cost"
    display_name = "Adjust Psynergy PP Cost"
    default = 0

class RandomizePsyAoe(Toggle):
    """When enabled the AoE of Psynergy is randomized"""
    internal_name = "randomize_psynergy_aoe"
    display_name = "Randomize Psynergy AoE"
    default = 0

class AdjustEnemyPsyPower(Toggle):
    """When enabled the power of Enemy Psynergy is randomized within a margin of vanilla."""
    internal_name = "adjust_enemy_psynergy_power"
    display_name = "Adjust Enemy Psynergy Power"
    default = 0

class RandomizeEnemyPsyAoe(Toggle):
    """When enabled the AoE of Enemy Psynergy is randomized."""
    internal_name = "randomize_enemy_psynergy_aoe"
    display_name = "Randomize Enemy Psynergy AoE"
    default = 0

class ClassPsynergy(Choice):
    """Determine what Psynergy a class will learn
    Vanilla: leaves the Psynergy on their vanilla classes
    Randomize Psynergy by Classline: Learned Psynergy is shuffled by classlines (e.g. Squire will have Brute Psynergy)
    Randomize by Psynergy Group: Learned Psynergy is shuffled by Psynergy groups (e.g. if a class learns Spire, it will also learn Clay Spire)
    Randomize by Psynergy Group Prefer Element: As by group, but with a preference to the same Element
    Randomize by Psynergy Element: Learned Psynergy is freely shuffled with another Psynergy of the same element
    Fully Randomize it will randomize it completely without grouping or preference
    """
    internal_name = "class_psynergy"
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
    Vanilla: leaves the learning of Psynergy on the vanilla levels.
    Adjust Learning Levels: will randomize learning levels within a margin from vanilla.
    Randomize Learning Levels: will randomize learning levels completely.
    """
    internal_name = "psynergy_levels"
    display_name = "Character Element Shuffle"
    option_vanilla = 0
    option_adjust_learning_levels = 1
    option_randomize_learning_levels = 2
    default = 1

class FreeAvoid(Toggle):
    """When enabled, the Avoid Psynergy will cost no PP"""
    internal_name = "free_avoid"
    display_name = "Avoid costs no PP"
    default = 1

class FreeRetreat(Toggle):
    """When enabled, the Retreat Psynergy will cost no PP"""
    internal_name = "free_retreat"
    display_name = "Retreat costs no PP"
    default = 1

class ShuffleAttack(Toggle):
    """When enabled, the attack stat from weapons is shuffled amongst each other"""
    internal_name = "shuffle_weapon_attack"
    display_name = "Shuffle weapon attack"
    default = 0

class StartWithHealPsynergy(Toggle):
    """Start the game with at least one healing Psynergy (Cure, Ply, Wish or Aura)"""
    internal_name = "start_with_healing_psynergy"
    display_name = "Start with Healing Psynergy"
    default = 0

class StartWithRevivePsynergy(Toggle):
    """When enabled, start the game with Revive Psynergy"""
    internal_name = "start_with_revive"
    display_name = "Start with Revive Psynergy"
    default = 0

class ScaleExpGained(Range):
    """Scale how much Exp is earned by the party."""
    internal_name = "scale_exp"
    display_name = "Scale Exp"
    range_start = 1
    range_end = 15
    default = 3

class ScaleCoinsGained(Range):
    """Scale how much Coins are earned by the party."""
    internal_name = "scale_coins"
    display_name = "Scale Coins"
    range_start = 1
    range_end = 15
    default = 4

class ShuffleDefense(Toggle):
    """When enabled, the defense from equipment is shuffled amongst each other"""
    internal_name = "shuffle_armour_defense"
    display_name = "Shuffle armour defense"
    default = 0


class StartingLevels(Range):
    """Determine the starting levels for characters joining the party.
    Note this only increases levels of characters that are lower level than the party"""
    internal_name = "starting_levels"
    display_name = "Starting levels"
    range_start = 5
    range_end = 99
    default = 5

class EnemyEResShuffle(Choice):
    """Determine how Enemy Elemental Resistance is shuffled
    Vanilla: leaves the elemental resistance as per the vanilla game.
    Shuffle Elemental Resistance: will shuffle them between enemies.
    Randomize Elemental Resistance: will randomize the resistances for each enemy.
    """
    internal_name = "enemy_elemental_resistance"
    display_name = "Enemy Elemental Resistance Shuffle"
    option_vanilla = 0
    option_shuffle_elemmental_res = 1
    option_randomize_elemental_res = 2
    default = 0

class SanctuaryReviveCost(Choice):
    """Determine how expensive the Sanctuary is to revive characters
    Vanilla: leaves the cost per the vanilla game (20x level)
    Reduced: will alter the cost to be cheaper than vanilla (2x level)
    Fixed: will alter the cost to the same price throughout (100 coins)
    """
    internal_name = "sanctum_revive_cost"
    display_name = "Sanctum revive cost"
    option_vanilla = 0
    option_reduced = 1
    option_fixed = 2
    default = 1

class RemoveCurses(Toggle):
    """When enabled, curses are removed."""
    internal_name = "remove_all_curses"
    display_name = "Remove all Curses"
    default = 1

class AvoidPatch(Toggle):
    """When enabled, Avoid always succeeds and will disable encounters. Using it again will enable encounters"""
    internal_name = "avoid_always_works"
    display_name = "Toggleable Avoid and always works"
    default = 1

class EnableHardMode(Toggle):
    """When enabled, all enemies will have 50% more health, 25% more attack and defense"""
    internal_name = "enable_hard_mode"
    display_name = "Enable Hard Mode"
    default = 0

class HalveEncounterRate(Toggle):
    """When enabled, the encounter rate will be halved"""
    internal_name = "reduced_encounter_rate"
    display_name = "Reduce Encounter Rate"
    default = 0

class EasierBosses(Toggle):
    """When enabled, boss fights will be easier by altering their scripts / stats"""
    internal_name = "easier_bosses"
    display_name = "Easier Bosses"
    default = 0

class NamedPuzzles(Choice):
    """Determines how the named puzzles will generate. These include the puzzles for Gambomba Statue, Gaia Rock and Trial Road
    Vanilla: uses the name that is given to Felix
    Fixed: will force the puzzles to use the name 'Felix'
    Randomized: will force the puzzles to be a random name"""
    internal_name = "name_puzzles"
    display_name = "Named Puzzles"
    option_vanilla = 0
    option_fixed = 1
    option_randomized = 2
    default = 0

class ManualRetreatGlitch(Toggle):
    """When enabled, Hold select to trigger the Retreat glitch. Logic does not require or expect use of glitches to beat your seed,
    this purely gives more control to activating the glitch over draining your PP to than use it anyway."""
    internal_name = "manual_retreat_glitch"
    display_name = "Manual Retreat Glitch"
    default = 0

class ShipWings(Toggle):
    """When enabled, the ship starts with the Wings of Anemos."""
    internal_name = "start_with_wings_of_anemos"
    display_name = "Start with Ship Wings"
    default = 0

class MusicShuffle(Toggle):
    """When enabled, music is shuffled amongst each other."""
    internal_name = "shuffle_music"
    display_name = "Music Shuffle"
    default = 0

class TelportEverywhere(Toggle):
    """When enabled, allows Teleport to target small villages and dungeons"""
    internal_name = "teleport_to_dungeons_and_towns"
    display_name = "Teleport Everywhere"
    default = 1

class AnemosAccess(Choice):
    """Determine accesss to Anemos Inner Sanctun
    Vanilla: requires all 72 Djinn to be able to enter Anemos Inner Sanctum
    Randomized: will select a value between 16 to 28 Djinn to be able to access Anemos Inner Sanctum
    Open: allows you to enter Anemos Inner Sanctum without any Djinn
    """
    internal_name = "anemos_inner_sanctum_access"
    display_name = "Anemos Inner Sanctum Access"
    option_vanilla = 0
    option_randomized = 1
    option_open = 2
    default = 0

class TrapChance(Range):
    """The chance for filler items in the pool to be replaced by a trap. This can vary from about 70 to 130 traps depending on your settings. Have fun!
    Note that this does not replace every filler item as some options force add filler items to the pool."""
    internal_name = "trap_chance"
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0
    
class MimicTrapWeight(Range):
    """The weight for a trap to be a Mimic. As not all vanilla locations can be mimics.
    Mimics will drop their vanilla contents which tend to be more useful consumables but can also be things like Game Tickets or Lucky Medals.
    Note: Enabling this will force a number of filler items to the pool to ensure generation success due to locations not supporting mimics."""
    internal_name = "mimic_trap_weight"
    display_name = "Mimic Trap Weight"
    range_start = 0
    range_end = 100
    default = 5

class ScaleMimics(Toggle):
    """Whether the strength of mimics should be scaled based on the sphere they are in.  Increases generation time"""
    internal_name = "scale_mimics"
    display_name = "Scale Mimics"
    default = 1

class ForgeMaterialsFillerWeight(Range):
    """The weight for a filler item to be a forge material. These will be forged into any of their regular results.
    Note that forging results are RNG based in the game and the randomizer does not alter this behaviour.
    Examples of materials are Tear Stone, Sylph Feather, Golem Core, Dark Matter and Orihalcon."""
    internal_name = "forge_material_filler_weight"
    display_name = "Forge Material Filler Weight"
    range_start = 0
    range_end = 100
    default = 25

class ForgeMaterialsAreFiller(Toggle):
    """Whether Forge Materials should be marked as filler instead of useful"""
    internal_name = "forge_materials_are_filler"
    display_name = "Forge Materials are Filler"
    default = 0

class RustyMaterialsFillerWeight(Range):
    """The weight for a filler item to be a rusty weapon. These weapons will forge into their counterparts as per usual.
    E.g. you can find a Rusty Sword which when forged turns into the Soul Brand or a Rusty Staff for a Glower Staff."""
    internal_name = "rusty_material_filler_weight"
    display_name = "Rusty Material Filler Weight"
    range_start = 0
    range_end = 100
    default = 10

class StatBoostFillerWeight(Range):
    """The weight for a filler item to be a stat boost item.
    These are Cookie, Hard Nut, Apple, Mint, Power Bread and Lucky Pepper."""
    internal_name = "stat_boost_filler_weight"
    display_name = "Stat Boost Filler Weight"
    range_start = 0
    range_end = 100
    default = 20
    
class UncommonConsumableFillerWeight(Range):
    """The weight for a filler item to be an uncommon consumable.
    Examples of these are Psy Crystal, Mist Potion, Potion and Water of Life."""
    internal_name = "uncommon_consumable_filler_weight"
    display_name = "Uncommon Consumable Filler Weight"
    range_start = 0
    range_end = 100
    default = 25
    
class ForgedEquipmentFillerWeight(Range):
    """The weight for a filler item to be the end result of forging equipment through materials or rusty weapons.
    Examples are Excalibur, Viking Axe, Goblin's Rod, Luna Shield, Astral Circlet and Dragon Boots."""
    internal_name = "forged_equipment_filler_weight"
    display_name = "Forged Equipment Filler Weight"
    range_start = 0
    range_end = 100
    default = 0
    
class LuckyFountainEquipmentFillerWeight(Range):
    """The weight for a filler item to be a lucky item reward from the fountain in Lemuria.
    Examples of these are Hestia Blade, Mighty Axe, Aegis Shield and Crown of Glory."""
    internal_name = "lucky_equipment_filler_weight"
    display_name = "Lucky Fountain Equipment Filler Weight"
    range_start = 0
    range_end = 100
    default = 0

class ShopEquipmentFillerWeight(Range):
    """The weight for a filler item to be equipment from the shop.
    These include the normal things you can buy amongst a few of the artefacts. Think along the lines of Long Sword, Silver Helm, Chain Mail to a Frost Wand."""
    internal_name = "shop_equipment_filler_weight"
    display_name = "Shop Equipment Filler Weight"
    range_start = 0
    range_end = 100
    default = 10

class ArtifactsAreFiller(Toggle):
    """Whether "Rare" Equipment should be considered filler instead of useful.  Rings, Shirts, and Boots are
    not reclassified by this option."""
    internal_name = "artifacts_are_filler"
    display_name = "Artifacts are Filler"
    default = 0

class CoinsFillerWeight(Range):
    """The weight for a filler item to be coins.
    The coin amounts are the vanilla coin items you can find. These vary from 3 coins to 911 coins. Majority is around or below 300."""
    internal_name = "coins_filler_weight"
    display_name = "Coin Filler Weight"
    range_start = 0
    range_end = 100
    default = 15

class CommonConsumablesFillerWeight(Range):
    """The weight for a filler item to be a common consumable.
    Examples of these are Herbs, Vials, Antidotes, Elixirs, Smoke Bombs and Lucky Medals"""
    internal_name = "common_consumable_filler_weight"
    display_name = "Common Consumable Filler Weight"
    range_start = 0
    range_end = 100
    default = 50

class AutoRun(Toggle):
    """Swaps the behavior of holding B when moving (default is now run instead of walk)"""
    internal_name = "auto_run"
    display_name = "Auto Run"
    default = 1

@dataclass
class GSTLAOptions(PerGameCommonOptions):
    #Pool and Logic settings
    item_shuffle: ItemShuffle
    reveal_hidden_item: RevealHiddenItem
    omit_locations: OmitLocations
    add_elvenshirt_clericsring: AddGs1Items
    add_non_obtainable_items: AddDummyItems

    lemurian_ship: StartWithShip
    start_with_wings_of_anemos: ShipWings
    anemos_inner_sanctum_access: AnemosAccess
    shuffle_characters: CharacterShuffle
    second_starting_character: SecondStartingCharacter

    #Char And Class Settings
    scale_characters: ScaleCharacters
    max_scaled_level: MaxScaledLevel
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
    auto_run: AutoRun
    
    start_inventory_from_pool: StartInventoryPool

    #traps
    trap_chance: TrapChance
    mimic_trap_weight: MimicTrapWeight
    scale_mimics: ScaleMimics

    #filler
    forge_material_filler_weight: ForgeMaterialsFillerWeight
    forge_materials_are_filler: ForgeMaterialsAreFiller
    rusty_material_filler_weight: RustyMaterialsFillerWeight
    stat_boost_filler_weight: StatBoostFillerWeight
    uncommon_consumable_filler_weight: UncommonConsumableFillerWeight
    forged_equipment_filler_weight: ForgedEquipmentFillerWeight
    lucky_equipment_filler_weight: LuckyFountainEquipmentFillerWeight
    artifacts_are_filler: ArtifactsAreFiller
    shop_equipment_filler_weight: ShopEquipmentFillerWeight
    coins_filler_weight: CoinsFillerWeight
    common_consumable_filler_weight: CommonConsumablesFillerWeight