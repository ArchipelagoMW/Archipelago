from dataclasses import dataclass

from Options import NamedRange, Choice, Range, Toggle, DefaultOnToggle, PerGameCommonOptions, StartInventoryPool, OptionGroup

class StrengthIncrease(Range):
    """
    Determines the number of Strength Increases to add to the multiworld.
    
    The randomizer will add all stat ups defined here into a pool and choose up to 99 to add to the multiworld.
    
    Accessory Slot Increases and Item Slot Increases are prioritized first, then the remaining items (up to 99 total) are chosen at random.
    """
    display_name = "STR Increases"
    range_start = 0
    range_end = 100
    default = 24

class DefenseIncrease(Range):
    """
    Determines the number of Defense Increases to add to the multiworld.
    
    The randomizer will add all stat ups defined here into a pool and choose up to 99 to add to the multiworld.
    
    Accessory Slot Increases and Item Slot Increases are prioritized first, then the remaining items (up to 99 total) are chosen at random.
    """
    display_name = "DEF Increases"
    range_start = 0
    range_end = 100
    default = 24

class HPIncrease(Range):
    """
    Determines the number of HP Increases to add to the multiworld.
    
    The randomizer will add all stat ups defined here into a pool and choose up to 99 to add to the multiworld.
    
    Accessory Slot Increases and Item Slot Increases are prioritized first, then the remaining items (up to 99 total) are chosen at random.
    """
    display_name = "HP Increases"
    range_start = 0
    range_end = 100
    default = 23

class APIncrease(Range):
    """
    Determines the number of AP Increases to add to the multiworld.
    
    The randomizer will add all stat ups defined here into a pool and choose up to 99 to add to the multiworld.
    
    Accessory Slot Increases and Item Slot Increases are prioritized first, then the remaining items (up to 99 total) are chosen at random.
    """
    display_name = "AP Increases"
    range_start = 0
    range_end = 100
    default = 18

class MPIncrease(Range):
    """
    Determines the number of MP Increases to add to the multiworld.
    
    The randomizer will add all stat ups defined here into a pool and choose up to 99 to add to the multiworld.
    
    Accessory Slot Increases and Item Slot Increases are prioritized first, then the remaining items (up to 99 total) are chosen at random.
    """
    display_name = "MP Increases"
    range_start = 0
    range_end = 20
    default = 7

class AccessorySlotIncrease(Range):
    """
    Determines the number of Accessory Slot Increases to add to the multiworld.
    
    The randomizer will add all stat ups defined here into a pool and choose up to 99 to add to the multiworld.
    
    Accessory Slot Increases and Item Slot Increases are prioritized first, then the remaining items (up to 99 total) are chosen at random.
    """
    display_name = "Accessory Slot Increases"
    range_start = 0
    range_end = 6
    default = 1

class ItemSlotIncrease(Range):
    """
    Determines the number of Item Slot Increases to add to the multiworld.
    
    The randomizer will add all stat ups defined here into a pool and choose up to 99 to add to the multiworld.
    
    Accessory Slot Increases and Item Slot Increases are prioritized first, then the remaining items (up to 99 total) are chosen at random.
    """
    display_name = "Item Slot Increases"
    range_start = 0
    range_end = 5
    default = 3

class Atlantica(Toggle):
    """
    Toggle whether to include checks in Atlantica.
    """
    display_name = "Atlantica"

class HundredAcreWood(Toggle):
    """
    Toggle whether to include checks in the 100 Acre Wood.
    """
    display_name = "100 Acre Wood"

class SuperBosses(Toggle):
    """
    Toggle whether to include checks behind Super Bosses.
    """
    display_name = "Super Bosses"

class Cups(Choice):
    """
    Determines which cups have their locations added to the multiworld.
    
    Please note that the cup items will still appear in the multiworld even if set to off, as they are required to challenge Sephiroth.

    Off: All cup locations are removed
    
    Cups: Phil, Pegasus, and Hercules cups are included
    
    Hades Cup: Hades Cup is included in addition to Phil, Pegasus, and Hercules cups. If Super Bosses are enabled, then Ice Titan is included
    """
    display_name = "Cups"
    option_off = 0
    option_cups = 1
    option_hades_cup = 2
    default = 0

class FinalRestDoorKey(Choice):
    """
    Determines what grants the player the Final Rest Door Key.
    
    Sephiroth: Defeat Sephiroth
    
    Unknown: Defeat Unknown
    
    Postcards: Turn in an amount of postcards in Traverse Town
    
    Final Ansem: Enter End of the World and defeat Ansem as normal
    
    Puppies: Rescue and return an amount of puppies in Traverse Town
    
    Final Rest: Open the chest in End of the World Final Rest
    """
    display_name = "Final Rest Door Key"
    option_sephiroth = 0
    option_unknown = 1
    option_postcards = 2
    option_lucky_emblems = 3
    option_puppies = 4
    option_final_rest = 5
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
    range_start = 16 // 4
    range_end = 128
    special_range_names = {
        "0.25x": int(16 // 4),
        "0.5x": int(16 // 2),
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
    display_name = "Lucky Emblems to Open End of the World"
    default = 7
    range_start = 0
    range_end = 20

class RequiredLuckyEmblemsDoor(Range):
    """
    If Final Rest Door Key is set to "Lucky Emblems", determines the number of Lucky Emblems required.
    """
    display_name = "Lucky Emblems to Open Final Rest Door"
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
    display_name = "Keyblade Minimum STR Bonus"
    default = 3
    range_start = 0
    range_end = 20

class KeybladeMaxStrength(Range):
    """
    Determines the maximum STR bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum STR Bonus"
    default = 14
    range_start = 0
    range_end = 20

class KeybladeMinCritRateBonus(Range):
    """
    Determines the minimum Crit Rate bonus a keyblade can have.
    """
    display_name = "Keyblade Minimum Crit Rate Bonus"
    default = 0
    range_start = 0
    range_end = 200

class KeybladeMaxCritRateBonus(Range):
    """
    Determines the maximum Crit Rate bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum Crit Rate Bonus"
    default = 200
    range_start = 0
    range_end = 200

class KeybladeMinCritSTRBonus(Range):
    """
    Determines the minimum Crit STR bonus a keyblade can have.
    """
    display_name = "Keyblade Minimum Crit Rate Bonus"
    default = 0
    range_start = 0
    range_end = 16

class KeybladeMaxCritSTRBonus(Range):
    """
    Determines the maximum Crit STR bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum Crit Rate Bonus"
    default = 16
    range_start = 0
    range_end = 16

class KeybladeMinRecoil(Range):
    """
    Determines the minimum recoil a keyblade can have.
    """
    display_name = "Keyblade Minimum Recoil"
    default = 1
    range_start = 1
    range_end = 90

class KeybladeMaxRecoil(Range):
    """
    Determines the maximum recoil a keyblade can have.
    """
    display_name = "Keyblade Maximum Recoil"
    default = 90
    range_start = 1
    range_end = 90

class KeybladeMinMP(Range):
    """
    Determines the minimum MP bonus a keyblade can have.
    """
    display_name = "Keyblade Minimum MP Bonus"
    default = -2
    range_start = -2
    range_end = 5

class KeybladeMaxMP(Range):
    """
    Determines the maximum MP bonus a keyblade can have.
    """
    display_name = "Keyblade Maximum MP Bonus"
    default = 3
    range_start = -2
    range_end = 5

class LevelChecks(Range):
    """
    Determines the maximum level for which checks can be obtained.
    """
    display_name = "Level Checks"
    default = 99
    range_start = 0
    range_end = 99

class ForceStatsOnLevels(NamedRange):
    """
    If this value is less than the value for Level Checks, this determines the minimum level from which only stat ups are obtained at level up locations.
    
    For example, if you want to be able to find any multiworld item from levels 2-50, then just stat ups for levels 51-100, set this value to 51.
    """
    display_name = "Force Stats on Level Starting From"
    default = 2
    range_start = 2
    range_end = 101
    special_range_names = {
        "none": 101,
        "multiworld-to-level-50": 51,
        "all": 2
    }

class BadStartingWeapons(Toggle):
    """
    Forces Kingdom Key, Dream Sword, Dream Shield, and Dream Staff to have vanilla stats.
    """
    display_name = "Bad Starting Weapons"

class DeathLink(Choice):
    """
    If Sora is KO'ed, the other players with "Death Link" on will also be KO'ed.
    The opposite is also true.
    """
    display_name = "Death Link"
    option_off = 0
    option_toggle = 1
    option_on = 2
    default = 0

class DonaldDeathLink(Toggle):
    """
    If Donald is KO'ed, so is Sora.  If Death Link is toggled on in your client, this will send a death to everyone who enabled death link.
    """
    display_name = "Donald Death Link"

class GoofyDeathLink(Toggle):
    """
    If Goofy is KO'ed, so is Sora.  If Death Link is toggled on in your client, this will send a death to everyone who enabled death link.
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
    
    Note: Does not apply to Atlantica, the emblem and carousel chests in Hollow Bastion, or the Aero chest in Neverland currently.
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

    Beginner: Logic only expects what would be the natural solution in vanilla gameplay or similar, as well as a guarantee of tools for boss fights.
    
    Normal: Logic expects some clever use of abilities, exploration of options, and competent combat ability; generally does not require advanced knowledge.
    
    Proud: Logic expects advanced knowledge of tricks and obscure interactions, such as using Combo Master, Dumbo, and other unusual methods to reach locations.
    
    Minimal: Logic expects the bare minimum to get to locations; may require extensive grinding, beating fights with no tools, and performing very difficult or tedious tricks.
    """
    display_name = "Logic Difficulty"
    option_beginner = 0
    option_normal = 5
    option_proud = 10
    option_minimal = 15
    default = 5

class ExtraSharedAbilities(DefaultOnToggle):
    """
    If on, adds extra shared abilities to the pool.  These can stack, so multiple high jumps make you jump higher and multiple glides make you superglide faster.
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

class JungleSlider(Toggle):
    """
    Determines whether checks are behind the Jungle Slider minigame.
    """
    display_name = "Jungle Slider"

class StartingWorlds(Range):
    """
    Number of random worlds to start with in addition to Traverse Town, which is always available.
    
    Will only consider Atlantica if toggled, and will only consider End of the World if its unlock is set to "Item".
    
    These are given by the server, and are received after connection.
    """
    display_name = "Starting Worlds"
    default = 4
    range_start = 0
    range_end = 10
    
class StartingTools(DefaultOnToggle):
    """
    Determines whether you start with Scan and Dodge Roll.
    
    These are given by the server, and are received after connection.
    """
    display_name = "Starting Tools"

class RemoteItems(Choice):
    """
    Determines if items can be placed on locations in your own world in such a way that will force them to be remote items.
    
    Off: When your items are placed in your world, they can only be placed in locations that they can be acquired without server connection (stats on levels, items in chests, etc).
    
    Allow: When your items are placed in your world, items that normally can't be placed in a location in-game are simply made remote (abilities on static events, etc).
    
    Full: All items are remote.  Use this when doing something like a co-op seed.
    """
    display_name = "Remote Items"
    option_off = 0
    option_allow = 1
    option_full = 2
    default = 0

class Slot2LevelChecks(Range):
    """
    Determines how many levels have an additional item.
    
    If Remote Items is OFF, these checks will only contain abilities or items for other players.
    """
    display_name = "Slot 2 Level Checks"
    default = 0
    range_start = 0
    range_end = 33

class ShortenGoMode(DefaultOnToggle):
    """
    If on, the player warps to the final cutscene after defeating Ansem 1 > Darkside > Ansem 2, skipping World of Chaos.
    """
    display_name = "Shorten Go Mode"

class DestinyIslands(Toggle):
    """
    If on, Adds a Destiny Islands item and a number of Raft Materials items to the pool.
    
    When "Destiny Islands" is found, Traverse Town will have an additional place to land - Seashore.
    
    "Raft Materials" allow progress into Day 2 and to Homecoming.  The amount is defined in Day 2 Materials and Homecoming Materials.
    """
    display_name = "Destiny Islands"

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
    display_name = "Mythril In Pool"
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
    display_name = "Randomize Party Member Starting Accessories"

class MaxLevelForSlot2LevelChecks(Range):
    """
    Determines the max level for slot 2 level checks.
    """
    display_name = "Max Level for Slot 2 Level Checks"
    default = 50
    range_start = 2
    range_end = 100

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

class Day2Materials(Range):
    """
    The amount of Raft Materials required to access Day 2.
    """
    display_name = "Day 2 Materials"
    default = 4
    range_start = 0
    range_end = 20

class HomecomingMaterials(Range):
    """
    The amount of Raft Materials required to access Homecoming.
    """
    display_name = "Homecoming Materials"
    default = 10
    range_start = 0
    range_end = 20

class MaterialsInPool(Range):
    """
    The amount of Raft Materials required to access Homecoming.
    """
    display_name = "Materials in Pool"
    default = 16
    range_start = 0
    range_end = 20

class StackingWorldItems(DefaultOnToggle):
    """
    Multiple world items give you the world's associated key item.
    
    WL - Footprints
    
    OC - Entry Pass
    
    DJ - Slides
    
    HT - Forget-Me-Not and Jack-In-The-Box
    
    HB - Theon Vol. 6
    
    Adds an extra world to the pool for each that has a key item (WL, OC, DJ, HT, HB).
    
    Forces Halloween Town Key Item Bundle ON.
    """
    display_name = "Stacking World Items"

class HalloweenTownKeyItemBundle(DefaultOnToggle):
    """
    Obtaining the Forget-Me-Not automatically gives Jack-in-the-Box as well.
    
    Removes Jack-in-the-Box from the pool.
    """
    display_name = "Halloween Town Key Item Bundle"

@dataclass
class KH1Options(PerGameCommonOptions):
    final_rest_door_key: FinalRestDoorKey
    end_of_the_world_unlock: EndoftheWorldUnlock
    required_lucky_emblems_eotw: RequiredLuckyEmblemsEotW
    required_lucky_emblems_door: RequiredLuckyEmblemsDoor
    lucky_emblems_in_pool: LuckyEmblemsInPool
    required_postcards: RequiredPostcards
    required_puppies: RequiredPuppies
    super_bosses: SuperBosses
    atlantica: Atlantica
    hundred_acre_wood: HundredAcreWood
    cups: Cups
    randomize_puppies: RandomizePuppies
    puppy_value: PuppyValue
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
    bad_starting_weapons: BadStartingWeapons
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
    level_checks: LevelChecks
    slot_2_level_checks: Slot2LevelChecks
    force_stats_on_levels: ForceStatsOnLevels
    strength_increase: StrengthIncrease
    defense_increase: DefenseIncrease
    hp_increase: HPIncrease
    ap_increase: APIncrease
    mp_increase: MPIncrease
    accessory_slot_increase: AccessorySlotIncrease
    item_slot_increase: ItemSlotIncrease
    start_inventory_from_pool: StartInventoryPool
    jungle_slider: JungleSlider
    starting_tools: StartingTools
    remote_items: RemoteItems
    shorten_go_mode: ShortenGoMode
    death_link: DeathLink
    destiny_islands: DestinyIslands
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
    unlock_0_volume: Unlock0Volume
    unskippable: Unskippable
    auto_save: AutoSave
    warp_anywhere: WarpAnywhere
    randomize_party_member_starting_accessories: RandomizePartyMemberStartingAccessories
    max_level_for_slot_2_level_checks: MaxLevelForSlot2LevelChecks
    randomize_ap_costs: RandomizeAPCosts
    max_ap_cost: MaxAPCost
    min_ap_cost: MinAPCost
    day_2_materials: Day2Materials
    homecoming_materials: HomecomingMaterials
    materials_in_pool: MaterialsInPool
    stacking_world_items: StackingWorldItems
    halloween_town_key_item_bundle: HalloweenTownKeyItemBundle
    

kh1_option_groups = [
    OptionGroup("Goal", [
        FinalRestDoorKey,
        EndoftheWorldUnlock,
        RequiredLuckyEmblemsDoor,
        RequiredLuckyEmblemsEotW,
        LuckyEmblemsInPool,
        RequiredPostcards,
        RequiredPuppies,
        DestinyIslands,
        Day2Materials,
        HomecomingMaterials,
        MaterialsInPool,
    ]),
    OptionGroup("Locations", [
        SuperBosses,
        Atlantica,
        Cups,
        HundredAcreWood,
        JungleSlider,
        RandomizeEmblemPieces,
        RandomizePostcards,
    ]),
    OptionGroup("Levels", [
        EXPMultiplier,
        LevelChecks,
        Slot2LevelChecks,
        MaxLevelForSlot2LevelChecks,
        ForceStatsOnLevels,
        StrengthIncrease,
        DefenseIncrease,
        HPIncrease,
        APIncrease,
        MPIncrease,
        AccessorySlotIncrease,
        ItemSlotIncrease,
    ]),
    OptionGroup("Keyblades", [
        KeybladesUnlockChests,
        KeybladeStats,
        BadStartingWeapons,
        KeybladeMinStrength,
        KeybladeMaxStrength,
        KeybladeMinCritRateBonus,
        KeybladeMaxCritRateBonus,
        KeybladeMinCritSTRBonus,
        KeybladeMaxCritSTRBonus,
        KeybladeMinRecoil,
        KeybladeMaxRecoil,
        KeybladeMinMP,
        KeybladeMaxMP,
    ]),
    OptionGroup("Synth", [
        OrichalcumInPool,
        OrichalcumPrice,
        MythrilInPool,
        MythrilPrice,
    ]),
    OptionGroup("AP Costs", [
        RandomizeAPCosts,
        MaxAPCost,
        MinAPCost
    ]),
    OptionGroup("Misc", [
        StartingWorlds,
        StartingTools,
        RandomizePuppies,
        PuppyValue,
        InteractInBattle,
        LogicDifficulty,
        ExtraSharedAbilities,
        StackingWorldItems,
        HalloweenTownKeyItemBundle,
        EXPZeroInPool,
        RandomizePartyMemberStartingAccessories,
        DeathLink,
        DonaldDeathLink,
        GoofyDeathLink,
        RemoteItems,
        ShortenGoMode,
        OneHP,
        FourByThree,
        AutoAttack,
        BeepHack,
        ConsistentFinishers,
        EarlySkip,
        FastCamera,
        FasterAnimations,
        Unlock0Volume,
        Unskippable,
        AutoSave,
        WarpAnywhere
    ])
]
