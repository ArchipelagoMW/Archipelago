import typing
from dataclasses import dataclass
from Options import Choice, Option, DeathLink, Range, Toggle, PerGameCommonOptions, StartInventoryPool

class Goal(Choice):
    """The victory condition for your run."""

    display_name = "Goal"
    option_save_roland_normal_mode = 0
    option_saturn_normal_mode = 1
    option_warrior_normal_mode = 2
    # option_terramorphous_normal_mode = 3
    # option_warrior_tvhm = 3
    # option_warrior_uvhm = 4
    # option_op_10 = 5
    default = 0

class DeleteStartingGear(Choice):
    """Deletes your character's gear on first connection, avoids granting checks immediately for Skyrocket, Gearbox guns, etc.
    (Please be careful to back up your saves and load the correct character)"""
    display_name = "Delete Starting Gear"
    option_keep = 0
    option_delete = 1
    default = 0

class GearRarityItemPool(Choice):
    """Gear kinds will be added to the item pool as receivable items.
    disabled = Exclude from Item Pool, ability to equip things is always unlocked.
    exclude_seraph_plus = Seraph, Pearlescent, and Effervescent are excluded
    exclude_pearl_plus = Pearlescent and Effervescent are excluded
    exclude_rainbow = Effervescent is excluded
    """
    display_name = "Gear Rarity Receivable Items"
    option_disabled = 0
    option_exclude_seraph_plus = 1
    option_exclude_pearl_plus = 2
    option_exclude_rainbow = 3
    option_all = 4
    default = 1

class ReceiveGearItems(Choice):
    """When receiving gear from the item pool, does it spawn for you or do you only get the ability to equip the ones you find?
    This option does nothing if gear_rarity_item_pool is disabled
    equip_only = Added to item pool, do not spawn gear
    receive_non_unique = Added to item pool, only spawn gear that is not Unique/Legendary/etc. (red-text) 
    receive_all = Added to item pool, spawn all gear
    """
    display_name = "Gear Receive Type"
    option_equip_only = 0
    option_receive_non_unique = 1
    option_receive_all = 2
    # option_receive_unique_only = 4
    default = 2

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


class VaultSymbols(Choice):
    """Vault Symbols as location checks"""
    display_name = "Vault Symbols"
    option_none = 0
    option_all = 1
    # option_base_game_only = 2
    default = 1

class VendingMachines(Choice):
    """Vending Machines as location checks"""
    display_name = "Vending Machines"
    option_none = 0
    option_all = 1
    # option_base_game_only = 2
    default = 1

class EntranceLocks(Choice):
    """
    Moving to another map area (regular or fast travel) is disabled until the associated item is found
    Turning this option off has strange implications. You will basically be expected to goal in sphere one, since nothing would be "out of logic" for you.
    all = You are required to unlock travel items in order to travel to other map areas
    no_locks = Travel Items are not included in the multiworld.
    """
    display_name = "Entrance Locks"
    option_no_locks = 0
    option_all = 1
    # option_base_game_only = 2
    default = 1

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

class SpawnTraps(Choice):
    """Add Spawn Traps to the item pool"""
    display_name = "Entrance Locks"
    option_none = 0
    option_all = 1
    # option_base_game_only = 2
    default = 1

# TODO: split this into separate toggleable quest checks and quest reward items
class QuestRewardRando(Choice):
    """Quest rewards are added to the item pool and Quests completions count as location checks"""
    display_name = "Quest Reward Rando"
    option_none = 0
    option_all = 1
    # option_base_game_only = 2
    default = 1

class GenericMobChecks(Choice):
    """Adds a few checks into the location pool for farming generic mobs. Select a drop chance (default 5%)"""
    display_name = "Generic Mob Checks"
    option_disabled = 0
    option_1_percent = 1
    option_2_percent = 2
    option_3_percent = 3
    option_4_percent = 4
    option_5_percent = 5
    option_6_percent = 6
    option_7_percent = 7
    option_8_percent = 8
    option_9_percent = 9
    option_10_percent = 10
    default = 5

# class NamedEnemyChecks(Choice):
#     """Adds checks into the location pool for killing each named enemy
#     """
#     display_name = "Named Enemy Checks"
#     option_none = 0
#     option_all = 1
#     default = 1

class GearRarityChecks(Choice):
    """Adds checks into the location pool for the first time you pick up gear of each type + rarity combination
    exclude_seraph_plus = Seraph, Pearlescent, and Effervescent are excluded
    exclude_pearl_plus = Pearlescent and Effervescent are excluded
    exclude_rainbow = Effervescent is excluded
    """
    display_name = "Rarity Checks"
    option_disabled = 0
    option_exclude_seraph_plus = 1
    option_exclude_pearl_plus = 2
    option_exclude_rainbow = 3
    option_all = 4
    default = 1

class ChallengeChecks(Choice):
    """Adds checks into the location pool for completing BAR challenges
    """
    display_name = "BAR Challenge Checks"
    option_none = 0
    option_level_1 = 1
    # option_unique_only = 2
    # option_exclude_unique = 3
    # option_level_1_only_exclude_unique = 4
    # option_all = 5
    default = 1

class ChestChecks(Choice):
    """
    Adds checks for opening most Red Chests
    """
    display_name = "Red Chest Checks"
    option_none = 0
    option_all = 1
    # option_base_game_only = 2
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
    default = 2

class RemoveDLCChecks(Choice):
    """
    Removes checks associated with Scarlett, Torgue, Hammerlock, Tina, and Lilith DLCs
    """
    display_name = "Remove DLC Checks"
    option_keep = 0
    option_remove = 1
    # maybe options for specific ones in the future.
    default = 0

class RemoveDigiPeakChecks(Choice):
    """
    Removes checks associated with Digistruct Peak
    """
    display_name = "Remove Digi Peak Checks"
    option_keep = 0
    option_remove = 1
    # maybe options for specific ones in the future.
    default = 0


class RemoveHeadhunterChecks(Choice):
    """
    Removes checks associated with
    Hallowed Hollow, Gluttony Gulch, Marcus's Mercenary Shop, Rotgut Distillery and Wam Bam Island
    """
    display_name = "Remove Headhunter Checks"
    option_keep = 0
    option_remove = 1
    # maybe options for specific ones in the future.
    default = 0

class DeathLink(Toggle):
    display_name = "Death Link"

class DeathLinkPunishment(Choice):
    """
    If DeathLink is off, this option does nothing.
    damage = take fatal damage when a DeathLink is received, but it can be blocked by healthgate.
    ffyl = enter "fight for your life" mode when a DeathLink is received.
    death = instantly die when a DeathLink is received.
    """
    display_name = "Death Link Mode"
    option_damage = 0
    option_ffyl = 1
    option_death = 2
    default = 1

class DeathLinkSendMode(Choice):
    """
    If DeathLink is off, this option does nothing.
    death = Send a DeathLink when you die
    ffyl = Send a DeathLink whenever you fall into "fight for your life" mode
    save_quit = Send a DeathLink whenever you save quit
    save_quit_and_death = Send a DeathLink save quit and whenever you die
    save_quit_and_ffyl = Send a DeathLink save quit and whenever you fall into ffyl
    """
    display_name = "Death Link Mode"
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
    vault_symbols: VaultSymbols
    vending_machines: VendingMachines
    entrance_locks: EntranceLocks
    jump_checks: JumpChecks
    max_jump_height: MaxJumpHeight
    sprint_checks: SprintChecks
    max_sprint_speed: MaxSprintSpeed
    spawn_traps: SpawnTraps
    quest_reward_rando: QuestRewardRando
    generic_mob_checks: GenericMobChecks
    gear_rarity_checks: GearRarityChecks
    challenge_checks: ChallengeChecks
    chest_checks: ChestChecks
    # fill_extra_checks_with: FillExtraChecksWith
    # legendary_rando: LegendaryDropRandomizer
    # named_enemy_rando: NamedEnemyRandomizer
    # drop_multiplier_amt: DropChanceMultiplier
    remove_dlc_checks: RemoveDLCChecks
    remove_digi_peak_checks: RemoveDigiPeakChecks
    remove_headhunter_checks: RemoveHeadhunterChecks
    remove_coop_checks: RemoveCoopChecks
    death_link: DeathLink
    death_link_punishment: DeathLinkPunishment
    death_link_send_mode: DeathLinkSendMode
    start_inventory_from_pool: StartInventoryPool



