from dataclasses import dataclass

from Options import NamedRange, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionGroup
from Options import PerGameCommonOptions, StartInventoryPool

class LevelStats(Choice):
    """
    Determines the stat increase Sora gets on each level up.

    Vanilla: Each level gives its vanilla stat increase.

    Shuffle: The vanilla stat increases are shuffled across levels.
    """
    display_name = "LV Stats"
    option_vanilla = 0
    option_shuffle = 1
    default = 0

class LevelCheckLocations(Choice):
    """
    Determines which levels can have additional checks.

    LV 50: 33 additional checks spread randomly across levels 2-50.

    LV 99: 33 additional checks spread randomly across levels 2-99.

    LV 1: No additional level checks.
    """
    display_name = "LV Check Locations"
    option_level_50 = 0
    option_level_99 = 1
    option_level_1 = 2
    default = 0

class LevelCheckItems(Choice):
    """
    Determines what can be found on additional level checks.

    Stats and Abilities: Sora's abilities, Item Slot Increases, and Accessory Slot Increases.

    Anything: Any item.
    """
    display_name = "LV Check Items"
    option_stats_and_abilities = 0
    option_anything = 1
    default = 0

class AdditionalItemSlots(Range):
    """
    Determines the number of additional Item Slot Increases added to the multiworld.
    """
    display_name = "Additional Item Slots"
    range_start = 0
    range_end = 5
    default = 1

class AdditionalAccessorySlots(Range):
    """
    Determines the number of additional Accessory Slot Increases added to the multiworld.
    """
    display_name = "Additional Accessory Slots"
    range_start = 0
    range_end = 6
    default = 1

class SkipHundredAcreWoodMinigames(Toggle):
    """
    Skip the 100 Acre Wood minigames: each one counts as won without being played.
    """
    display_name = "Skip 100 Acre Wood Minigames"

class CupsStandard(Choice):
    """
    Determines how the Olympus Coliseum cups play.

    Normal: The cups play as in vanilla.

    Bosses Only: Each cup is shortened to its boss matches.

    No Fights: Entering a cup clears it immediately and gives its rewards.
    """
    display_name = "Cups Standard"
    option_normal = 0
    option_bosses_only = 1
    option_no_fights = 2
    default = 0

class CupsSoloTimeTrial(Choice):
    """
    Determines how the Solo and Time Trial versions of the cups play.

    Same As Standard: Solo and Time Trial follow the Cups Standard setting.

    Auto Clear: Clearing a cup normally also clears it Solo and Time Trial and gives those rewards.
    """
    display_name = "Cups Solo and Time Trial"
    option_same_as_standard = 0
    option_auto_clear = 1
    default = 0

class FinalRestDoorKey(Choice):
    """
    Determines what grants the player the Final Rest Door Key.
    
    Sephiroth: Defeat Sephiroth in Olympus Coliseum
    
    Unknown: Defeat the Enigmatic Man in Hollow Bastion
    
    Postcards: Turn in an amount of postcards in Traverse Town
    
    Lucky Emblems: Collect an amount of Lucky Emblems
    
    Puppies: Rescue and return an amount of puppies in Traverse Town
    
    Final Rest: Open the chest in End of the World Final Rest

    Anywhere: Can be anywhere in the multiworld
    """
    display_name = "Final Rest Door Key"
    option_sephiroth = 0
    option_unknown = 1
    option_postcards = 2
    option_lucky_emblems = 3
    option_puppies = 4
    option_final_rest = 5
    option_anywhere = 6
    default = 3

class EndoftheWorldUnlock(Choice):
    """Determines how End of the World is unlocked.
    
    Item: You can receive an item called "End of the World" which unlocks the world
    
    Lucky Emblems: A certain amount of lucky emblems are required to unlock End of the World, which is defined in your options"""
    display_name = "End of the World Unlock"
    option_item = 0
    option_lucky_emblems = 1
    default = 1

class RequiredPostcards(Range):
    """
    If "Final Rest Door Key" is set to "Postcards", defines how many postcards are required.
    """
    display_name = "Required Postcards"
    default = 8
    range_start = 1
    range_end = 10

class RequiredPuppies(Choice):
    """
    If "Final Rest Door Key" is set to "Puppies", defines how many puppies are required.
    """
    display_name = "Required Puppies"
    default = 80
    option_10 = 10
    option_20 = 20
    option_30 = 30
    option_40 = 40
    option_50 = 50
    option_60 = 60
    option_70 = 70
    option_80 = 80
    option_90 = 90
    option_99 = 99

class PuppyValue(Range):
    """
    Determines how many dalmatian puppies are given when a puppy item is found.
    """
    display_name = "Puppy Value"
    default = 3
    range_start = 1
    range_end = 99

class RandomizePuppies(DefaultOnToggle):
    """
    If OFF, the "Puppy" item is worth 3 puppies and puppies are placed in vanilla locations.
    
    If ON, the "Puppy" item is worth an amount of puppies defined by "Puppy Value", and are shuffled randomly.
    """
    display_name = "Randomize Puppies"

class EXPMultiplier(NamedRange):
    """
    Determines the multiplier to apply to EXP gained.
    """
    display_name = "EXP Multiplier"
    default = 16 * 4
    range_start = 16
    range_end = 128
    special_range_names = {
        "1x": 16,
        "2x": 16 * 2,
        "3x": 16 * 3,
        "4x": 16 * 4,
        "8x": 16 * 8,
    }

class RequiredLuckyEmblemsEotW(Range):
    """
    If End of the World Unlock is set to "Lucky Emblems", determines the number of Lucky Emblems required.
    """
    display_name = "End of the World Emblems"
    default = 7
    range_start = 0
    range_end = 20

class RequiredLuckyEmblemsDoor(Range):
    """
    If Final Rest Door Key is set to "Lucky Emblems", determines the number of Lucky Emblems required.
    """
    display_name = "Final Rest Door Emblems"
    default = 10
    range_start = 0
    range_end = 20

class LuckyEmblemsInPool(Range):
    """
    Determines the number of Lucky Emblems in the item pool.
    """
    display_name = "Lucky Emblems in Pool"
    default = 13
    range_start = 0
    range_end = 20

class KeybladeStats(Choice):
    """
    Determines whether Keyblade stats should be randomized.
    
    Randomize: Randomly generates stats for each keyblade between the defined minimums and maximums.
    
    Shuffle: Shuffles the stats of the vanilla keyblades amongst each other.
    
    Vanilla: Keyblade stats are unchanged.
    """
    display_name = "Keyblade Stats"
    option_randomize = 0
    option_shuffle = 1
    option_vanilla = 2

class KeybladeMinStrength(Range):
    """
    Determines the minimum STR bonus a keyblade can have.
    """
    display_name = "Keyblade Min STR Bonus"
    default = 3
    range_start = 0
    range_end = 20

class KeybladeMaxStrength(Range):
    """
    Determines the maximum STR bonus a keyblade can have.
    """
    display_name = "Keyblade Max STR Bonus"
    default = 14
    range_start = 0
    range_end = 20

class KeybladeMinCritRateBonus(Range):
    """
    Determines the minimum Crit Rate bonus a keyblade can have.
    """
    display_name = "Keyblade Min Crit Rate Bonus"
    default = 0
    range_start = 0
    range_end = 200

class KeybladeMaxCritRateBonus(Range):
    """
    Determines the maximum Crit Rate bonus a keyblade can have.
    """
    display_name = "Keyblade Max Crit Rate Bonus"
    default = 200
    range_start = 0
    range_end = 200

class KeybladeMinCritSTRBonus(Range):
    """
    Determines the minimum Crit STR bonus a keyblade can have.
    """
    display_name = "Keyblade Min Crit STR Bonus"
    default = 0
    range_start = 0
    range_end = 16

class KeybladeMaxCritSTRBonus(Range):
    """
    Determines the maximum Crit STR bonus a keyblade can have.
    """
    display_name = "Keyblade Max Crit STR Bonus"
    default = 16
    range_start = 0
    range_end = 16

class KeybladeMinRecoil(Range):
    """
    Determines the minimum recoil a keyblade can have.
    """
    display_name = "Keyblade Min Recoil"
    default = 1
    range_start = 1
    range_end = 90

class KeybladeMaxRecoil(Range):
    """
    Determines the maximum recoil a keyblade can have.
    """
    display_name = "Keyblade Max Recoil"
    default = 90
    range_start = 1
    range_end = 90

class KeybladeMinMP(Range):
    """
    Determines the minimum MP bonus a keyblade can have.
    """
    display_name = "Keyblade Min MP Bonus"
    default = -2
    range_start = -2
    range_end = 5

class KeybladeMaxMP(Range):
    """
    Determines the maximum MP bonus a keyblade can have.
    """
    display_name = "Keyblade Max MP Bonus"
    default = 3
    range_start = -2
    range_end = 5

class BadKingdomKey(Toggle):
    """
    Forces Kingdom Key to have vanilla stats.
    """
    display_name = "Bad Kingdom Key"

class DonaldDeathLink(Toggle):
    """
    If Donald is KO'ed, so is Sora.
    """
    display_name = "Donald Death Link"

class GoofyDeathLink(Toggle):
    """
    If Goofy is KO'ed, so is Sora.
    """
    display_name = "Goofy Death Link"

class KeybladesUnlockChests(Toggle):
    """
    If toggled on, the player is required to have a certain keyblade to open chests in certain worlds.
    
    TT   - Lionheart
    WL   - Lady Luck
    OC   - Olympia
    DJ   - Jungle King
    AG   - Three Wishes
    MS   - Wishing Star
    HT   - Pumpkinhead
    NL   - Fairy Harp
    HB   - Divine Rose
    EotW - Oblivion
    HAW  - Spellbinder
    DI   - Oathkeeper
    AL   - Crabclaw
    """
    display_name = "Keyblades Unlock Chests"

class InteractInBattle(DefaultOnToggle):
    """
    Allow Sora to talk to people, examine objects, and open chests in battle.
    """
    display_name = "Interact in Battle"

class LogicDifficulty(Choice):
    """
    Determines what the randomizer logic may expect you to do to reach certain locations.
    """
    display_name = "Logic Difficulty"
    option_beginner = 0
    option_normal = 5
    option_proud = 10
    option_minimal = 15
    default = 5

class ExtraSharedAbilities(DefaultOnToggle):
    """
    If on, adds extra shared abilities to the pool.
    These can stack, so multiple high jumps make you jump higher and multiple glides make you superglide faster.
    """
    display_name = "Extra Shared Abilities"

class EXPZeroInPool(Toggle):
    """
    If on, adds EXP Zero ability to the item pool.  This is redundant if you are planning on playing on Proud.
    """
    display_name = "EXP Zero in Pool"

class RandomizeEmblemPieces(Toggle):
    """
    If off, the Hollow Bastion emblem pieces are in their vanilla locations.
    """
    display_name = "Randomize Emblem Pieces"

class RandomizePostcards(Choice):
    """
    Determines how Postcards are randomized

    All: All Postcards are randomized
    
    Chests: Only the 3 Postcards in chests are randomized
    
    Vanilla: Postcards are in their original location
    """
    display_name = "Randomize Postcards"
    option_all = 0
    option_chests = 1
    option_vanilla = 2

class ExcludedContent(OptionSet):
    """
    Locations in these groups will only contain filler.
    """
    display_name = "Excluded Content"
    valid_keys = ["Super Bosses", "Jungle Slider"]

class StartingWorlds(Range):
    """
    Number of random worlds to start with in addition to Traverse Town, which is always available.
    
    Will only consider End of the World if its unlock is set to "Item".
    """
    display_name = "Starting Worlds"
    default = 4
    range_start = 0
    range_end = 11
    
class StartingTools(DefaultOnToggle):
    """
    Determines whether you start with Scan and Dodge Roll.
    """
    display_name = "Starting Tools"

class RemoteItems(Choice):
    """
    Determines how local items (KH1 items found in KH1) are delivered to the player.
    
    Off: The game handles granting local items.

    Full: The server handles granting local items (requires connection to server).
    """
    display_name = "Remote Items"
    option_off = 0
    option_full = 2
    default = 0

class ShortenGoMode(DefaultOnToggle):
    """
    If on, the player warps to the final cutscene after defeating Ansem 1 > Darkside > Ansem 2, skipping World of Chaos.
    """
    display_name = "Shorten Go Mode"

class MythrilInPool(Range):
    """
    Determines how much Mythril, one of the two synthesis items, is in the item pool.
    
    You need 16 to synth every recipe that requires it.
    """
    display_name = "Mythril In Pool"
    default = 20
    range_start = 16
    range_end = 30

class OrichalcumInPool(Range):
    """
    Determines how much Orichalcum, one of the two synthesis items, is in the item pool.
    
    You need 17 to synth every recipe that requires it.
    """
    display_name = "Orichalcum In Pool"
    default = 20
    range_start = 17
    range_end = 30

class MythrilPrice(Range):
    """
    Determines the cost of Mythril in each shop.
    """
    display_name = "Mythril Price"
    default = 500
    range_start = 100
    range_end = 5000

class OrichalcumPrice(Range):
    """
    Determines the cost of Orichalcum in each shop.
    """
    display_name = "Orichalcum Price"
    default = 500
    range_start = 100
    range_end = 5000

class OneHP(Toggle):
    """
    If on, forces Sora's max HP to 1 and removes the low health warning sound.
    """
    display_name = "One HP"

class FourByThree(Toggle):
    """
    If on, changes the aspect ratio to 4 by 3.
    """
    display_name = "4 by 3"

class AutoAttack(Toggle):
    """
    If on, you can combo by holding confirm.
    """
    display_name = "Auto Attack"

class BeepHack(Toggle):
    """
    If on, removes low health warning sound.  Works up to max health of 41.
    """
    display_name = "Beep Hack"

class ConsistentFinishers(Toggle):
    """
    If on, 30% chance finishers are now 100% chance.
    """
    display_name = "Consistent Finishers"

class EarlySkip(DefaultOnToggle):
    """
    If on, allows skipping cutscenes immediately that normally take time to be able to skip.
    """
    display_name = "Early Skip"

class FastCamera(Toggle):
    """
    If on, speeds up camera movement and camera centering.
    """
    display_name = "Fast Camera"

class FasterAnimations(DefaultOnToggle):
    """
    If on, speeds up animations during which you can't play.
    """
    display_name = "Faster Animations"

class SkipSummonAnimations(Toggle):
    """
    If on, summons appear immediately: their entrance cutscenes are skipped and the "Give me strength!" opener is shortened.
    """
    display_name = "Skip Summon Animations"

class Unlock0Volume(Toggle):
    """
    If on, volume 1 mutes the audio channel.
    """
    display_name = "Unlock 0 Volume"

class Unskippable(DefaultOnToggle):
    """
    If on, makes unskippable cutscenes skippable.
    """
    display_name = "Unskippable"

class AutoSave(DefaultOnToggle):
    """
    If on, enables auto saving.
    
    Press L1+L2+R1+R2+D-Pad Left to instantly load continue state.
    
    Press L1+L2+R1+R2+D-Pad Right to instantly load autosave.
    """
    display_name = "AutoSave"

class WarpAnywhere(Toggle):
    """
    If on, enables the player to warp at any time, even when not at a save point.
    
    Press L1+L2+R2+Select to open the Save/Warp menu at any time.
    """
    display_name = "WarpAnywhere"

class RandomizePartyMemberStartingAccessories(DefaultOnToggle):
    """
    If on, the 10 accessories that some party members (Aladdin, Ariel, Jack, Peter Pan, Beast) start with are randomized.
    
    10 random accessories will be distributed amongst any party member aside from Sora in their starting equipment.
    """
    display_name = "Randomize Accessories"

class RandomizeAPCosts(Choice):
    """
    Off: No randomization

    Shuffle: Ability AP Costs will be shuffled amongst themselves.
    
    Randomize: Ability AP Costs will be randomized to the specified max and min.
    
    Distribute: Ability AP Costs will totalled and re-distributed randomly between the specified max and min.
    """
    display_name = "Randomize AP Costs"
    option_off = 0
    option_shuffle = 1
    option_randomize = 2
    option_distribute = 3
    default = 0

class MaxAPCost(Range):
    """
    If Randomize AP Costs is set to Randomize or Distribute, this defined the max AP cost an ability can have.
    """
    display_name = "Max AP Cost"
    default = 5
    range_start = 4
    range_end = 9

class MinAPCost(Range):
    """
    If Randomize AP Costs is set to Randomize or Distribute, this defined the min AP cost an ability can have.
    """
    display_name = "Min AP Cost"
    default = 0
    range_start = 0
    range_end = 2

class Day1Materials(Range):
    """
    The amount of Raft Materials required to finish Day 1.
    """
    display_name = "Day 1 Materials"
    default = 4
    range_start = 0
    range_end = 20

class Day2Materials(Range):
    """
    The amount of Raft Materials required to finish Day 2.
    """
    display_name = "Day 2 Materials"
    default = 10
    range_start = 0
    range_end = 20

class MaterialsInPool(Range):
    """
    The amount of Raft Materials in the item pool.
    """
    display_name = "Materials in Pool"
    default = 13
    range_start = 0
    range_end = 20

class RaftFinish(Toggle):
    """
    If on, finishing Day 2 lets you warp to Homecoming (Final Bosses).
    """
    display_name = "Raft Finish"

class StackingWorldItems(DefaultOnToggle):
    """
    Multiple world items give you the world's associated key item.
    
    WL - Footprints
    
    OC - Entry Pass
    
    DJ - Slides
    
    HT - Forget-Me-Not and Jack-In-The-Box
    
    HB - Theon Vol. 6

    AL - Crystal Trident
    
    Adds an extra world to the pool for each that has a key item (WL, OC, DJ, HT, HB, AL).
    
    Forces Halloween Town Item Bundle, Slides Bundle and Evidence Bundle ON.
    """
    display_name = "Stacking World Items"

class HalloweenTownKeyItemBundle(DefaultOnToggle):
    """
    Obtaining the Forget-Me-Not automatically gives Jack-in-the-Box as well.
    
    Removes Jack-in-the-Box from the pool.
    """
    display_name = "Halloween Town Item Bundle"

class SlidesBundle(DefaultOnToggle):
    """
    Obtaining Slide 1 gives all six slides at once (the item is shown as "Slides" in game).
    
    When off, Slide 2 through Slide 6 are separate items too, and all six are needed to show the slides to Jane.
    
    Forced ON when Stacking World Items is on.
    """
    display_name = "Slides Bundle"

class EvidenceBundle(DefaultOnToggle):
    """
    Only the Footprints are in the pool; they are all the evidence Wonderland needs.

    When off, Footprints, Claw Marks, Stench and Antenna are all in the pool. Any one of them lets the trial start.

    Forced ON when Stacking World Items is on.
    """
    display_name = "Evidence Bundle"

class RandomizeSpellMPCosts(Choice):
    """
    Off: No randomization.
    Shuffle: Spell costs will be shuffled amongst themselves, (2 single pip spells, 3 single MP spells, 2 double MP spells)
    Randomize: Spell costs will be randomized individually based on the defined upper and lower bounds.
    """
    display_name = "Randomize Spell MP Costs"
    option_off = 0
    option_shuffle = 1
    option_randomize = 2
    default = 0

class SpellMPCostMin(Choice):
    """
    Define the minimum MP cost a spell can have.
    """
    display_name = "Spell MP Cost Minimum"
    option_half_pip = 15
    option_pip = 30
    option_1_mp = 100
    option_2_mp = 200
    option_3_mp = 300
    default = 15
    
class SpellMPCostMax(Choice):
    """
    Define the maximum MP cost a spell can have.
    """
    display_name = "Spell MP Cost Maximum"
    option_half_pip = 15
    option_pip = 30
    option_1_mp = 100
    option_2_mp = 200
    option_3_mp = 300
    default = 300

class IndividualSpellLevelCosts(Toggle):
    """
    If randomizing or shuffling spell MP costs, each indiviudal level of a spell (for example Fire vs Fira vs Firaga)
    can have different MP costs.
    """
    display_name = "Individual Spell Level Costs"
    
class ScalingSpellPotency(DefaultOnToggle):
    """
    If randomizing or shuffling spell MP costs, each spell will have its effectiveness scaled relative to its new cost.
    """
    display_name = "Scaling Spell Potency"
    
class AccessoryAugments(Toggle):
    """
    Accessories are assigned special effects in addition to their normal effects.
    
    These can be either positive or negative.
    """
    display_name = "Accessory Augments"

class AugmentAbilitiesFromPool(Toggle):
    """
    If accessory augments is on, if an accessory's augment is assigned an ability, that ability can only be found on that accessory.
    """
    display_name = "Augment Abilities from Pool"

@dataclass
class KH1Options(PerGameCommonOptions):
    final_rest_door_key: FinalRestDoorKey
    end_of_the_world_unlock: EndoftheWorldUnlock
    required_lucky_emblems_eotw: RequiredLuckyEmblemsEotW
    required_lucky_emblems_door: RequiredLuckyEmblemsDoor
    lucky_emblems_in_pool: LuckyEmblemsInPool
    required_postcards: RequiredPostcards
    required_puppies: RequiredPuppies
    skip_hundred_acre_wood_minigames: SkipHundredAcreWoodMinigames
    cups_standard: CupsStandard
    cups_solo_time_trial: CupsSoloTimeTrial
    randomize_puppies: RandomizePuppies
    puppy_value: PuppyValue
    excluded_content: ExcludedContent
    starting_worlds: StartingWorlds
    keyblades_unlock_chests: KeybladesUnlockChests
    interact_in_battle: InteractInBattle
    exp_multiplier: EXPMultiplier
    logic_difficulty: LogicDifficulty
    extra_shared_abilities: ExtraSharedAbilities
    exp_zero_in_pool: EXPZeroInPool
    randomize_emblem_pieces: RandomizeEmblemPieces
    randomize_postcards: RandomizePostcards
    donald_death_link: DonaldDeathLink
    goofy_death_link: GoofyDeathLink
    keyblade_stats: KeybladeStats
    bad_kingdom_key: BadKingdomKey
    keyblade_min_str: KeybladeMinStrength
    keyblade_max_str: KeybladeMaxStrength
    keyblade_min_crit_rate: KeybladeMinCritRateBonus
    keyblade_max_crit_rate: KeybladeMaxCritRateBonus
    keyblade_min_crit_str: KeybladeMinCritSTRBonus
    keyblade_max_crit_str: KeybladeMaxCritSTRBonus
    keyblade_min_recoil: KeybladeMinRecoil
    keyblade_max_recoil: KeybladeMaxRecoil
    keyblade_min_mp: KeybladeMinMP
    keyblade_max_mp: KeybladeMaxMP
    level_stats: LevelStats
    level_check_locations: LevelCheckLocations
    level_check_items: LevelCheckItems
    additional_item_slots: AdditionalItemSlots
    additional_accessory_slots: AdditionalAccessorySlots
    start_inventory_from_pool: StartInventoryPool
    starting_tools: StartingTools
    remote_items: RemoteItems
    shorten_go_mode: ShortenGoMode
    orichalcum_in_pool: OrichalcumInPool
    orichalcum_price: OrichalcumPrice
    mythril_in_pool: MythrilInPool
    mythril_price: MythrilPrice
    one_hp: OneHP
    four_by_three: FourByThree
    auto_attack: AutoAttack
    beep_hack: BeepHack
    consistent_finishers: ConsistentFinishers
    early_skip: EarlySkip
    fast_camera: FastCamera
    faster_animations: FasterAnimations
    skip_summon_animations: SkipSummonAnimations
    unlock_0_volume: Unlock0Volume
    unskippable: Unskippable
    auto_save: AutoSave
    warp_anywhere: WarpAnywhere
    randomize_party_member_starting_accessories: RandomizePartyMemberStartingAccessories
    randomize_ap_costs: RandomizeAPCosts
    max_ap_cost: MaxAPCost
    min_ap_cost: MinAPCost
    day_1_materials: Day1Materials
    day_2_materials: Day2Materials
    materials_in_pool: MaterialsInPool
    raft_finish: RaftFinish
    stacking_world_items: StackingWorldItems
    halloween_town_key_item_bundle: HalloweenTownKeyItemBundle
    slides_bundle: SlidesBundle
    evidence_bundle: EvidenceBundle
    randomize_spell_mp_costs: RandomizeSpellMPCosts
    spell_mp_cost_min: SpellMPCostMin
    spell_mp_cost_max: SpellMPCostMax
    individual_spell_level_costs: IndividualSpellLevelCosts
    scaling_spell_potency: ScalingSpellPotency
    accessory_augments: AccessoryAugments
    augment_abilities_from_pool: AugmentAbilitiesFromPool
    

kh1_option_groups = [
    OptionGroup("Goal", [
        FinalRestDoorKey,
        EndoftheWorldUnlock,
        RequiredLuckyEmblemsEotW,
        RequiredLuckyEmblemsDoor,
        LuckyEmblemsInPool,
        RequiredPostcards,
        RequiredPuppies,
        Day1Materials,
        Day2Materials,
        MaterialsInPool,
        RaftFinish,
    ]),
    OptionGroup("Locations", [
        CupsStandard,
        CupsSoloTimeTrial,
        SkipHundredAcreWoodMinigames,
        RandomizeEmblemPieces,
        RandomizePostcards,
        RandomizePuppies,
        PuppyValue,
        ExcludedContent,
    ]),
    OptionGroup("Levels", [
        EXPMultiplier,
        LevelStats,
        LevelCheckLocations,
        LevelCheckItems,
        AdditionalItemSlots,
        AdditionalAccessorySlots,
    ]),
    OptionGroup("Equipment", [
        KeybladesUnlockChests,
        KeybladeStats,
        BadKingdomKey,
        KeybladeMaxStrength,
        KeybladeMinStrength,
        KeybladeMaxCritRateBonus,
        KeybladeMinCritRateBonus,
        KeybladeMaxCritSTRBonus,
        KeybladeMinCritSTRBonus,
        KeybladeMaxRecoil,
        KeybladeMinRecoil,
        KeybladeMaxMP,
        KeybladeMinMP,
        AccessoryAugments,
        AugmentAbilitiesFromPool,
        RandomizePartyMemberStartingAccessories,
    ]),
    OptionGroup("Synth", [
        MythrilPrice,
        MythrilInPool,
        OrichalcumPrice,
        OrichalcumInPool,
    ]),
    OptionGroup("AP / MP Costs", [
        RandomizeAPCosts,
        MaxAPCost,
        MinAPCost,
        RandomizeSpellMPCosts,
        SpellMPCostMin,
        SpellMPCostMax,
        IndividualSpellLevelCosts,
        ScalingSpellPotency,
    ]),
    OptionGroup("Toggles", [
        EXPZeroInPool,
        OneHP,
        FourByThree,
        AutoAttack,
        BeepHack,
        ConsistentFinishers,
        EarlySkip,
        FastCamera,
        FasterAnimations,
        SkipSummonAnimations,
        Unlock0Volume,
        Unskippable,
        AutoSave,
        WarpAnywhere,
    ]),
    OptionGroup("Misc", [
        StartingWorlds,
        StartingTools,
        StackingWorldItems,
        HalloweenTownKeyItemBundle,
        SlidesBundle,
        EvidenceBundle,
        InteractInBattle,
        LogicDifficulty,
        ExtraSharedAbilities,
        DonaldDeathLink,
        GoofyDeathLink,
        RemoteItems,
        ShortenGoMode,
    ]),
]
