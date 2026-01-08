from dataclasses import dataclass

from Options import DefaultOnToggle, Range, Toggle, Choice, PerGameCommonOptions

class NpcSanity(Toggle):
    """
    Randomizes the freeable NPCs in the world, making them obtainable from any source.
    """
    internal_name = "npc_sanity"
    display_name = "NPC Sanity"

class ScarabSanity(Toggle):
    """
    Randomizes the scarabs in the world.
    """
    internal_name = "scarab_sanity"
    display_name = "Scarab Sanity"

class SpiritSanity(Toggle):
    """
    Randomizes the spirit in the world.
    """
    internal_name = "spirit_sanity"
    display_name = "Spirit Sanity"

class ShardSanity(Toggle):
    """
    Randomizes the XP shards "groups" (not individual crystals) in the world.
    """
    internal_name = "shard_sanity"
    display_name = "Shard Sanity"

class KeySanity(Toggle):
    """
    Randomizes the small keys of dungeons in the world.
    """
    internal_name = "key_sanity"
    display_name = "Key Sanity"

class BossKeySanity(Toggle):
    """
    Randomizes the boss keys of dungeons in the world.
    """
    internal_name = "boss_key_sanity"
    display_name = "Boss Key Sanity"

class AddTrapItems(Toggle):
    """
    Add trap items to the item pool.
    In Minishoot' Adventures, trap items will force the primordial scarab to be a little chatty and make references to other games.
    (some of which are playable on Archipelago !)
    """
    internal_name = "add_trap_items"
    display_name = "Add Trap Items"

class TrapItemsAppearance(Choice):
    """
    Set the appearance of trap items.
    When set to "Major Items Only", trap items will be disguised as major items.
    When set to "Junk Items Only", trap items will be disguised as junk items.
    When set to "Anything", trap items can be disguised as any other items.
    """
    internal_name = "trap_items_appearance"
    display_name = "Trap Items Appearance"
    option_major_items_only = 0
    option_junk_items_only = 1
    option_anything = 2

class ShopCostModifier(Range):
    """
    Set the super crystal cost modifier for items in shops.
    The value can be between 10 and 200.
    The value is a percentage, so 100 means that the cost will be the same as in vanilla.
    """
    internal_name = "shop_cost_modifier"
    display_name = "Shop Cost Modifier"
    range_start = 10
    range_end = 200
    default = 100

class ScarabItemsCost(Range):
    """
    Set the scarab cost for items in shops.
    The value can be between 1 and 3.
    The value is the number each item will cost in scarabs.
    Note that extra scarabs will remain in the item pool.
    """
    internal_name = "scarab_items_cost"
    display_name = "Scarab Items Cost"
    range_start = 1
    range_end = 3
    default = 3

class SpiritTowerRequirement(Range):
    """
    Set the number of spirits required to enter the Spirit Tower.
    The value can be between 0 and 8.
    This setting does not affect the total number of spirit items in the world, only the number required to access the tower.
    """
    internal_name = "spirit_tower_requirement"
    display_name = "Spirit Tower Requirement"
    range_start = 0
    range_end = 8
    default = 8

class ShowArchipelagoItemCategory(DefaultOnToggle):
    """
    When enabled, Archipelago items sprites will indicate if its an important item (with an arrow pointing up), an helpful one (with the default icon), or not important (with a black and white sprite).
    """
    internal_name = "show_archipelago_item_category"
    display_name = "Show Archipelago item category"

class BlockedForest(DefaultOnToggle):
    """
    Replace the bushes of the secret pond in the forest with rocks. This make the south forest area blocked until you have the supershot.
    With this option enabled, the forest area no longer contains sphere 0 locations locked behind a particular difficult fight without any additional offensive capabilities.
    """
    internal_name = "blocked_forest"
    display_name = "Blocked Forest"

class IgnoreCannonLevelRequirements(Toggle):
    """
    By default, the game will ensure that progressive cannon levels are accessible before fights in late game areas.
    So for example, you will be able to enter Dungeon 3 in logic, but you will need the cannon level 4 to beat the boss, or items behind fights in this dungeon.
    If you enable this option, the cannon level requirements will be ignored, and the logic will expect you to be able to beat all fights with a level 1 cannon.
    """
    internal_name = "ignore_cannon_level_requirements"
    display_name = "Ignore Cannon Level Requirements"

class BoostlessSpringboards(Toggle):
    """
    When this setting is off, the logic will require you to use the boost to jump from springboards.
    When this setting is on, the dash will be enough to jump from springboards logically, which make the dash even more useful.
    """
    internal_name = "boostless_springboards"
    display_name = "Boostless Springboards"

class BoostlessSpiritRaces(Toggle):
    """
    When this setting is off, races against spirits will logically require the boost.
    When this setting is on, the logic will assume that you can complete those races with the dash instead.
    Note that you will still need the boost to complete the the spirits races of the Beach, Scarab Temple and Sunken City.
    Also note that this setting may require you to farm some XP to level up your speed.
    """
    internal_name = "boostless_spirit_races"
    display_name = "Boostless Spirit Races"

class BoostlessTorchRaces(Toggle):
    """
    When this setting is off, timed torch races will logically require the boost.
    When this setting is on, the logic will assume that you can complete those races without it.
    Note that this setting may require you to farm some XP to level up your speed.
    """
    internal_name = "boostless_torch_races"
    display_name = "Boostless Torch Races"

class EnablePrimordialCrystalLogic(Toggle):
    """
    When this setting is on, the Primordial Crystal will be considered in logic to blow up rocks and walls.
    When this setting is off, the logic will assume that you imperatively need Supershot to do that.
    """
    internal_name = "enable_primordial_crystal_logic"
    display_name = "Enable Primordial Crystal Logic"

class ProgressiveDash(Toggle):
    """
    When enabled, the game will fuse the Dash and the Spirit Dash into two cumulative progressive upgrades.
    The first upgrade will always allow you to dash, and the second one will allow you to dash through bullets.
    """
    internal_name = "progressive_dash"
    display_name = "Progressive Dash"

class DashlessGaps(Choice):
    """
    When set on "Needs Dash", you will need the dash to cross gaps, regardless of their size.
    When set on "Needs Boost", you will be able to logically cross gaps with the boost if the gap is small enough.
    When set on "Needs neither", you will be able to cross certains, very tight gaps without any upgrade.
    Note that this last value may require you to farm some XP to level up your speed.
    """
    internal_name = "dashless_gaps"
    display_name = "Dashless Gaps"
    option_needs_dash = 0
    option_needs_boost = 1
    option_needs_neither = 2

class CompletionGoals(Choice):
    """
    Set the goals required to finish the game.
    * Dungeon 5 : Beat the boss of Dungeon 5 and get to the normal ending.
    * Snow : Beat the Unchosen inside the tree and get to the true ending.
    * Dungeon 5 and Snow : Beat both the normal and true ending.
    * Spirit Tower : Collect all spirits and get to the Spirit Tower ending. The number of spirits required to enter the tower can be set with the "Spirit Tower Requirement" option.
    """
    internal_name = "completion_goals"
    display_name = "Completion Goals"
    option_dungeon_5 = 0
    option_snow = 1
    option_dungeon_5_and_snow = 2
    option_spirit_tower = 3

@dataclass
class MinishootOptions(PerGameCommonOptions):
    npc_sanity: NpcSanity
    scarab_sanity: ScarabSanity
    spirit_sanity: SpiritSanity
    shard_sanity: ShardSanity
    key_sanity: KeySanity
    boss_key_sanity: BossKeySanity
    add_trap_items: AddTrapItems
    trap_items_appearance: TrapItemsAppearance
    shop_cost_modifier: ShopCostModifier
    scarab_items_cost: ScarabItemsCost
    spirit_tower_requirement: SpiritTowerRequirement
    show_archipelago_item_category: ShowArchipelagoItemCategory
    blocked_forest: BlockedForest
    ignore_cannon_level_requirements: IgnoreCannonLevelRequirements
    boostless_springboards: BoostlessSpringboards
    boostless_spirit_races: BoostlessSpiritRaces
    boostless_torch_races: BoostlessTorchRaces
    enable_primordial_crystal_logic: EnablePrimordialCrystalLogic
    progressive_dash: ProgressiveDash
    dashless_gaps: DashlessGaps
    completion_goals: CompletionGoals
