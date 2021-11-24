import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink


class AdvancementGoal(Range):
    """Number of advancements required to spawn bosses."""
    displayname = "Advancement Goal"
    range_start = 0
    range_end = 92
    default = 40


class EggShardsRequired(Range):
    """Number of dragon egg shards to collect to spawn bosses."""
    displayname = "Egg Shards Required"
    range_start = 0
    range_end = 40


class EggShardsAvailable(Range):
    """Number of dragon egg shards available to collect."""
    displayname = "Egg Shards Available"
    range_start = 0
    range_end = 40


class BossGoal(Choice):
    """Bosses which must be defeated to finish the game."""
    displayname = "Required Bosses"
    option_none = 0
    option_ender_dragon = 1
    option_wither = 2
    option_both = 3
    default = 1


class ShuffleStructures(Toggle):
    """Enables shuffling of villages, outposts, fortresses, bastions, and end cities."""
    displayname = "Shuffle Structures"


class StructureCompasses(Toggle):
    """Adds structure compasses to the item pool, which point to the nearest indicated structure."""
    displayname = "Structure Compasses"


class BeeTraps(Range): 
    """Replaces a percentage of junk items with bee traps, which spawn multiple angered bees around every player when received."""
    displayname = "Bee Trap Percentage"
    range_start = 0
    range_end = 100


class CombatDifficulty(Choice):
    """Modifies the level of items logically required for exploring dangerous areas and fighting bosses."""
    displayname = "Combat Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1


class HardAdvancements(Toggle):
    """Enables certain RNG-reliant or tedious advancements."""
    displayname = "Include Hard Advancements"


class UnreasonableAdvancements(Toggle):
    """Enables the extremely difficult advancements "How Did We Get Here?" and "Adventuring Time.\""""
    displayname = "Include Unreasonable Advancements"


class PostgameAdvancements(Toggle):
    """Enables advancements that require spawning and defeating the required bosses."""
    displayname = "Include Postgame Advancements"


class SendDefeatedMobs(Toggle):
    """Send killed mobs to other Minecraft worlds which have this option enabled."""
    displayname = "Send Defeated Mobs"


class StartingItems(OptionList):
    """Start with these items. Each entry should be of this format: {item: "item_name", amount: #, nbt: "nbt_string"}"""
    displayname = "Starting Items"


minecraft_options: typing.Dict[str, type(Option)] = {
    "advancement_goal":                     AdvancementGoal,
    "egg_shards_required":                  EggShardsRequired,
    "egg_shards_available":                 EggShardsAvailable,
    "required_bosses":                      BossGoal,
    "shuffle_structures":                   ShuffleStructures,
    "structure_compasses":                  StructureCompasses,
    "bee_traps":                            BeeTraps,
    "combat_difficulty":                    CombatDifficulty,
    "include_hard_advancements":            HardAdvancements,
    "include_unreasonable_advancements":    UnreasonableAdvancements,
    "include_postgame_advancements":        PostgameAdvancements,
    "send_defeated_mobs":                   SendDefeatedMobs,
    "starting_items":                       StartingItems,
    "death_link":                           DeathLink,
}
