import typing
from dataclasses import dataclass
from Options import Choice, Option, DeathLink, Range, Toggle, OptionSet, PerGameCommonOptions, StartInventoryPool, FreeText

class Goal(FreeText):
    """The victory condition for your run. Please specify a valid location which can be found in archi_defs or archi_data.
    """
    display_name = "Goal"
    default = "Enemy: W4R-D3N"

# delete_starting_gear
class DeleteStartingGear(Choice):
    """Deletes your character's gear on first connection, avoids granting checks immediately for Skyrocket, Gearbox guns, etc.
    (Please be careful to back up your saves and load the correct character)"""
    display_name = "Delete Starting Gear"
    option_keep = 0
    alias_off = 0
    option_delete = 1
    alias_remove = 1
    alias_on = 1
    default = 0

# gear_rarity_item_pool
class GearRarityItemPool(Choice):
    """Gear kinds will be added to the item pool as receivable items.
    disabled = Exclude from Item Pool, ability to equip things is always unlocked.
    exclude_seraph_plus = Seraph, Pearlescent, and Effervescent are excluded
    exclude_pearl_plus = Pearlescent and Effervescent are excluded
    exclude_rainbow = Effervescent is excluded
    """
    display_name = "Gear Rarity Receivable Items"
    option_disabled = 0
    alias_remove = 0
    alias_off = 0
    option_exclude_seraph_plus = 1
    option_exclude_pearl_plus = 2
    option_exclude_rainbow = 3
    option_all = 4
    alias_on = 4
    alias_keep = 4
    default = 1

# receive_gear
class ReceiveGearItems(Choice):
    """When receiving gear (licenses) from the item pool, does it spawn for you or do you only get the ability to equip the ones you find.
    This option does nothing if gear_rarity_item_pool is disabled
    equip_only = Added to item pool, do not spawn gear
    receive = Added to item pool, spawn all gear
    """
    display_name = "Gear Receive Type"
    option_equip_only = 0
    alias_off = 0
    option_receive = 1
    alias_receive_all = 1
    alias_on = 1
    default = 1

class FillerGear(Choice):
    """What kind of filler gear should be added to the item pool?
    none = No filler gear will be added
    unique = Unique items (Legendaries, Seraphs, etc. but as filler)
    rarity_groups = Common, Uncommon, etc. as filler
    both = Both unique and non-unique gear
    """
    display_name = "Filler Gear"
    option_none = 0
    alias_off = 0
    alias_remove = 0
    option_unique = 1
    option_rarity_groups = 2
    option_both = 3
    alias_on = 3
    alias_keep = 3
    default = 1

# class FillerItems(Choice):
#     """What items should be added to fill out the item pool?
#     money = Money
#     eridium = Money and Eridium
#     gear = Extra Gear Checks
#     candy = Halloween Candy Spawns 
#     xp = Experience
#     """
#     display_name = "Filler Items"
#     option_money = 0
#     option_eridium = 1
#     option_gear = 2
#     option_candy = 3
#     option_xp = 3
#     default = 3


# vault_symbols
class VaultSymbols(Choice):
    """Vault Symbols as location checks"""
    display_name = "Vault Symbols"
    option_none = 0
    alias_remove = 0
    alias_off = 0
    option_all = 1
    alias_keep = 1
    alias_on = 1
    default = 1

# vending_machines
class VendingMachines(Choice):
    """Vending Machines as location checks"""
    display_name = "Vending Machines"
    option_none = 0
    alias_remove = 0
    alias_off = 0
    option_all = 1
    alias_keep = 1
    alias_on = 1
    default = 1

# entrance_locks
class EntranceLocks(Choice):
    """
    Moving to another map area (regular or fast travel) is disabled until the associated item is found
    Turning this option off has strange implications. You will basically be expected to goal in sphere one, since nothing would be "out of logic" for you.
    all = You are required to unlock travel items in order to travel to other map areas
    no_locks = Travel Items are not included in the multiworld.
    """
    display_name = "Entrance Locks"
    option_no_locks = 0
    alias_none = 0
    alias_remove = 0
    alias_off = 0
    option_all = 1
    alias_keep = 1
    alias_on = 1
    default = 1

# jump_checks TODO: technically not "checks", but alternate wording sounds clunky
class JumpChecks(Choice):
    """How many jump checks should be added to the pool. You will not start with the ability to jump unless you add "Progressive Jump" to your start_inventory_from_pool"""
    display_name = "Jump Checks"
    option_not_disabled = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    default = 3

# max_jump_height
class MaxJumpHeight(Choice):
    """Each jump check will give you an equivalent fraction of your max jump height.
    If Jump Checks is set to "not disabled" you will simply jump this high.
    high = 1.5x
    extra high = 2x"""
    display_name = "Max Jump Height"
    option_regular = 0
    option_high = 1
    option_extra_high = 2
    default = 0

# sprint_checks TODO: technically not "checks", but alternate wording sounds clunky
class SprintChecks(Choice):
    """How many sprint checks should be added to the pool. You will not start with the ability to sprint unless you add "Progressive Sprint" to your start_inventory_from_pool"""
    display_name = "Sprint Checks"
    option_not_disabled = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_5 = 5
    default = 3

# max_sprint_speed
class MaxSprintSpeed(Choice):
    """Each sprint check will give you an equivalent fraction of your max sprint speed.
    If Sprint Checks is set to "not disabled" you will simply sprint this fast.
    fast = 1.5x
    extra fast = 2x"""
    display_name = "Max Sprint Speed"
    option_regular = 0
    option_fast = 1
    option_extra_fast = 2
    option_supersonic = 4
    default = 0

# spawn_traps
class SpawnTraps(Choice):
    """Add Spawn Traps to the item pool. Digistruct Peak DLC is required for these to work."""
    display_name = "Spawn Traps"
    option_none = 0
    alias_remove = 0
    alias_off = 0
    option_all = 1
    alias_keep = 1
    alias_on = 1
    default = 1

# quest_completion_checks
class QuestCompletionChecks(Choice):
    """Quests completions count as location checks"""
    display_name = "Quest Completion Checks"
    option_none = 0
    alias_remove = 0
    alias_off = 0
    option_all = 1
    alias_keep = 1
    alias_on = 1
    default = 1

# quest_reward_items
class QuestRewardItems(Choice):
    """Quest rewards are not given at time of quest completion and are instead added to the item pool
    none = turn this option off
    all = include all quest rewards in the item pool
    only_gear = include quest rewards in the item pool but remove rewards that do not include gear (ex. Best Minion Ever only grants money)
    only_included_regions = include quest rewards in the item pool but remove quests associated with excluded regions (dlc that has been turned off)
    only_included_regions_gear = combination of only_included_regions and only_gear
    """
    display_name = "Quest Reward Items"
    option_none = 0
    alias_remove = 0
    alias_off = 0
    option_all = 1
    alias_keep = 1
    alias_on = 1
    option_only_gear = 2
    option_only_included_regions = 3
    option_only_included_regions_gear = 4
    default = 4

# generic_mob_checks
class GenericMobChecks(Choice):
    """Adds a few checks into the location pool for farming generic mobs. Select a drop chance (default 5%)"""
    display_name = "Generic Mob Checks"
    option_disabled = 0
    alias_off = 0
    alias_remove = 0
    option_1_percent = 1
    option_2_percent = 2
    option_3_percent = 3
    option_4_percent = 4
    option_5_percent = 5
    alias_on = 5
    option_6_percent = 6
    option_7_percent = 7
    option_8_percent = 8
    option_9_percent = 9
    option_10_percent = 10
    default = 5

# TODO: add this option
# class NamedEnemyChecks(Choice):
#     """Adds checks into the location pool for killing each named enemies
#     """
#     display_name = "Named Enemy Checks"
#     option_none = 0
#     option_all = 1
#     default = 1

# gear_rarity_checks
class GearRarityChecks(Choice):
    """Adds checks into the location pool for the first time you pick up gear of each type + rarity combination
    exclude_seraph_plus = Seraph, Pearlescent, and Effervescent are excluded
    exclude_pearl_plus = Pearlescent and Effervescent are excluded
    exclude_rainbow = Effervescent is excluded
    """
    display_name = "Gear Rarity Checks"
    option_disabled = 0
    alias_remove = 0
    alias_off = 0
    option_exclude_seraph_plus = 1
    option_exclude_pearl_plus = 2
    option_exclude_rainbow = 3
    option_all = 4
    alias_keep = 4
    alias_on = 4
    default = 1

# challenge_checks
class ChallengeChecks(Choice):
    """Adds checks into the location pool for completing BAR challenges
    none = No challenge checks in the location pool
    level_1 = Completing level 1 of all challenge checks included in the location pool
    """
    display_name = "BAR Challenge Checks"
    option_none = 0
    alias_remove = 0
    alias_off = 0
    option_level_1 = 1
    # option_unique_only = 2
    # option_exclude_unique = 3
    # option_level_1_only_exclude_unique = 4
    # option_all = 5
    alias_keep = 1
    alias_on = 1
    default = 1

# chest_checks
class ChestChecks(Choice):
    """
    Adds checks for opening most Red Chests
    """
    display_name = "Red Chest Checks"
    option_none = 0
    alias_remove = 0
    alias_off = 0
    option_all = 1
    alias_keep = 1
    alias_on = 1
    default = 1

# class ControlTraps(Choice):
#     """Add Control Traps to the item pool"""
#     display_name = "Entrance Locks"
#     option_none = 0
#     option_all = 1
#     default = 0


# class FillExtraChecksWith(Choice):
#     """
#     Fill extra checks with this kind of item
#     """
#     display_name = "Fill Extra Checks With"
#     option_legendary_guns_and_items = 0
#     option_legendary_items = 1
#     option_legendary_guns = 2
#     option_purple_rarity_stuff = 3
#     default = 0

# TODO: remove_x_checks should maybe be renamed to x_checks: remove/none/off and keep/all/on

# remove_coop_checks
class RemoveCoopChecks(Choice):
    """
    Removes checks that are impossible or difficult to do while playing solo
    keep = don't remove any checks
    remove_impossible = only remove impossible checks
    remove_all = remove difficult and impossible checks
    """
    display_name = "Remove Co-op Checks"
    option_keep = 0
    option_remove_impossible = 1
    option_remove_all = 2
    alias_remove = 2
    default = 2

# remove_ffs_checks
class RemoveFFSChecks(Choice):
    """
    Removes checks and quest rewards associated with Fight for Sanctuary DLC
    """
    display_name = "Remove Fight for Sanctuary DLC Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_tina_checks
class RemoveTinaChecks(Choice):
    """
    Removes checks and quest rewards associated with Tiny Tina's Assault on Dragon Keep DLC
    """
    display_name = "Remove Tiny Tina DLC Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_torgue_checks
class RemoveTorgueChecks(Choice):
    """
    Removes checks associated with Mr. Torgue's Campaign of Carnage DLC
    """
    display_name = "Remove Torgue DLC Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_scarlett_checks
class RemoveScarlettChecks(Choice):
    """
    Removes checks associated with Sir Hammerlock's Big Game Hunt (Oasis) DLC
    """
    display_name = "Remove Scarlett DLC Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_hammerlock_checks
class RemoveHammerlockChecks(Choice):
    """
    Removes checks associated with Sir Hammerlock's Big Game Hunt (Hunter's Grotto) DLC
    """
    display_name = "Remove Hammerlock DLC Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_digi_peak_checks
class RemoveDigiPeakChecks(Choice):
    """
    Removes checks associated with Digistruct Peak DLC
    """
    display_name = "Remove Digistruct Peak Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_headhunter_checks
class RemoveHeadhunterChecks(Choice):
    """
    Removes checks associated with Hallowed Hollow, Gluttony Gulch, Marcus's Mercenary Shop, Rotgut Distillery and Wam Bam Island
    """
    display_name = "Remove Headhunter Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_base_game_checks
class RemoveBaseGameChecks(Choice):
    """
    Removes checks associated with regions in the base game
    """
    display_name = "Remove Base Game Checks"
    option_keep = 0
    option_remove = 1
    default = 0

# remove_specific_region_checks
# TODO: where's a better place to find the region names?
class RemoveSpecificRegionChecks(OptionSet):
    """
    Select specific regions to remove from the randomization. Find region names in Regions.py
    ex. remove_specific_region_checks: ["FinksSlaughterhouse", "TerramorphousPeak"]
    """
    display_name = "Remove Specific Regions"
    from .Regions import region_data_table
    valid_keys = list(region_data_table.keys())

# remove_raidboss_checks
class RemoveRaidbossChecks(Choice):
    """
    Removes checks associated with raid bosses
    """
    display_name = "Remove Raid Boss Checks"
    option_keep = 0
    option_remove = 1
    # maybe options for specific ones in the future.
    default = 0


# max_level_checks
class MaxLevelChecks(Choice):
    """
    Removes checks associated with higher levels. Don't select an arbitrary number, options are listed below.
    none = don't remove any checks based on this rule
    level_14 = good for ending around bloodshot ramparts
    level_20 = good for ending around thousand cuts or level 15 dlcs and headhunters
    level_30 = removes checks beyond warrior
    """
    display_name = "Max Level Checks"
    option_none = 0
    alias_keep = 0
    alias_off = 0
    alias_uncapped = 0
    option_level_14 = 14
    option_level_20 = 20
    option_level_30 = 30
    default = 0

class DeathLink(Toggle):
    display_name = "Death Link"

# death_link_punishment
class DeathLinkPunishment(Choice):
    """
    If DeathLink is off, this option does nothing.
    damage = take near-fatal damage when a DeathLink is received.
    ffyl = instantly enter "fight for your life" mode when a DeathLink is received.
    death = instantly die when a DeathLink is received.
    """
    display_name = "Death Link Punishment"
    option_damage = 0
    option_ffyl = 1
    option_death = 2
    default = 1

# death_link_send_mode
class DeathLinkSendMode(Choice):
    """
    If DeathLink is off, this option does nothing.
    death = Send a DeathLink when you die
    ffyl = Send a DeathLink whenever you fall into "fight for your life" mode
    save_quit = Send a DeathLink whenever you save quit
    save_quit_and_death = Send a DeathLink on save quit and on death
    save_quit_and_ffyl = Send a DeathLink on save quit and when falling into ffyl
    """
    display_name = "Death Link Send Mode"
    option_death = 0
    option_ffyl = 1
    option_save_quit = 2
    option_save_quit_and_death = 3
    option_save_quit_and_ffyl = 4
    default = 0

# class DropChanceMultiplier(Range):
#     """Runs the drop loot function extra times when any enemy dies. Multipliers will be added as items."""
#     display_name = "Drop Chance Multipliers"
#     range_start = 0
#     range_end = 3
#     default = 3

# class LegendaryDropRandomizer(Toggle):
#     """Legendary drops will be removed from loot pools and replaced with checks."""
#     display_name = "Legendary Drop Randomizer"
#
#
# class NamedEnemyRandomizer(Toggle):
#     """Named Enemies without legendary drops like Bone Head 2.0, Bad Maw, and W4R-D3N
#     will also have checks in their loot pools."""
#     display_name = "Named Enemy Randomizer"
#
#
# class RandomLegendariesReceived(Toggle):
#     """Receive random legendaries."""
#     display_name = "Legendary Drop Randomizer"

@dataclass
class Borderlands2Options(PerGameCommonOptions):
    goal: Goal
    delete_starting_gear: DeleteStartingGear
    gear_rarity_item_pool: GearRarityItemPool
    receive_gear: ReceiveGearItems
    filler_gear: FillerGear
    vault_symbols: VaultSymbols
    vending_machines: VendingMachines
    entrance_locks: EntranceLocks
    jump_checks: JumpChecks
    max_jump_height: MaxJumpHeight
    sprint_checks: SprintChecks
    max_sprint_speed: MaxSprintSpeed
    spawn_traps: SpawnTraps
    quest_completion_checks: QuestCompletionChecks
    quest_reward_items: QuestRewardItems
    generic_mob_checks: GenericMobChecks
    gear_rarity_checks: GearRarityChecks
    challenge_checks: ChallengeChecks
    chest_checks: ChestChecks
    # fill_extra_checks_with: FillExtraChecksWith
    # legendary_rando: LegendaryDropRandomizer
    # named_enemy_rando: NamedEnemyRandomizer
    # drop_multiplier_amt: DropChanceMultiplier
    remove_ffs_checks: RemoveFFSChecks
    remove_tina_checks: RemoveTinaChecks
    remove_torgue_checks: RemoveTorgueChecks
    remove_scarlett_checks: RemoveScarlettChecks
    remove_hammerlock_checks: RemoveHammerlockChecks
    remove_digi_peak_checks: RemoveDigiPeakChecks
    remove_headhunter_checks: RemoveHeadhunterChecks
    remove_base_game_checks: RemoveBaseGameChecks
    remove_specific_region_checks: RemoveSpecificRegionChecks
    remove_coop_checks: RemoveCoopChecks
    remove_raidboss_checks: RemoveRaidbossChecks
    max_level_checks: MaxLevelChecks
    death_link: DeathLink
    death_link_punishment: DeathLinkPunishment
    death_link_send_mode: DeathLinkSendMode
    start_inventory_from_pool: StartInventoryPool
