from dataclasses import dataclass

from Options import Choice, Toggle, Range, PerGameCommonOptions

MAX_COMBAT_TASKS = 16

MAX_PRAYER_TASKS = 5
MAX_MAGIC_TASKS = 7
MAX_RUNECRAFT_TASKS = 8
MAX_CRAFTING_TASKS = 11
MAX_MINING_TASKS = 6
MAX_SMITHING_TASKS = 5
MAX_FISHING_TASKS = 6
MAX_COOKING_TASKS = 6
MAX_FIREMAKING_TASKS = 3
MAX_WOODCUTTING_TASKS = 3

NON_QUEST_LOCATION_COUNT = 49


class StartingArea(Choice):
    """
    Which chunks are available at the start. The player may need to move through locked chunks to reach the starting
    area, but any areas that require quests, skills, or coins are not available as a starting location.

    "Any Bank" rolls a random region that contains a bank.
    Chunksanity can start you in any chunk. Hope you like woodcutting!
    """
    display_name = "Starting Region"
    option_lumbridge = 0
    option_al_kharid = 1
    option_varrock_east = 2
    option_varrock_west = 3
    option_edgeville = 4
    option_falador = 5
    option_draynor = 6
    option_wilderness = 7
    option_any_bank = 8
    option_chunksanity = 9
    default = 0


class BrutalGrinds(Toggle):
    """
    Whether to allow skill tasks without having reasonable access to the usual skill training path.
    For example, if enabled, you could be forced to train smithing without an anvil purely by smelting bars,
    or training fishing to high levels entirely on shrimp.
    """
    display_name = "Allow Brutal Grinds"


class ProgressiveTasks(Toggle):
    """
    Whether skill tasks should always be generated in order of easiest to hardest.
    If enabled, you would not be assigned "Mine Gold" without also being assigned
    "Mine Silver", "Mine Coal", and "Mine Iron". Enabling this will result in a generally shorter seed, but with
    a lower variety of tasks.
    """
    display_name = "Progressive Tasks"


class EnableDuds(Toggle):
    """
    Whether to include filler "Dud" items that serve no purpose but allow for more tasks in the pool.
    """
    display_name = "Enable Duds"


class DudCount(Range):
    """
    How many "Dud" items to include in the pool. This setting is ignored if "Enable Duds" is not included
    """
    display_name = "Dud Item Count"
    range_start = 0
    range_end = 30
    default = 10


class EnableCarePacks(Toggle):
    """
    Whether or not to include useful "Care Pack" items that allow you to trade over specific items.
    Note: Requires your account NOT to be an Ironman. Also, requires access to another account to trade over the items,
    or gold to purchase off of the grand exchange.
    """
    display_name = "Enable Care Packs"

class MaxCombatLevel(Range):
    """
    The highest combat level of monster to possibly be assigned as a task.
    If set to 0, no combat tasks will be generated.
    """
    display_name = "Max Required Enemy Combat Level"
    range_start = 0
    range_end = 1520
    default = 50


class MaxCombatTasks(Range):
    """
    The maximum number of Combat Tasks to possibly be assigned.
    If set to 0, no combat tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Combat Task Count"
    range_start = 0
    range_end = MAX_COMBAT_TASKS
    default = MAX_COMBAT_TASKS


class CombatTaskWeight(Range):
    """
    How much to favor generating combat tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Combat Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxPrayerLevel(Range):
    """
    The highest Prayer requirement of any task generated.
    If set to 0, no Prayer tasks will be generated.
    """
    display_name = "Max Required Prayer Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxPrayerTasks(Range):
    """
    The maximum number of Prayer Tasks to possibly be assigned.
    If set to 0, no Prayer tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Prayer Task Count"
    range_start = 0
    range_end = MAX_PRAYER_TASKS
    default = MAX_PRAYER_TASKS


class PrayerTaskWeight(Range):
    """
    How much to favor generating Prayer tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Prayer Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxMagicLevel(Range):
    """
    The highest Magic requirement of any task generated.
    If set to 0, no Magic tasks will be generated.
    """
    display_name = "Max Required Magic Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxMagicTasks(Range):
    """
    The maximum number of Magic Tasks to possibly be assigned.
    If set to 0, no Magic tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Magic Task Count"
    range_start = 0
    range_end = MAX_MAGIC_TASKS
    default = MAX_MAGIC_TASKS


class MagicTaskWeight(Range):
    """
    How much to favor generating Magic tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Magic Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxRunecraftLevel(Range):
    """
    The highest Runecraft requirement of any task generated.
    If set to 0, no Runecraft tasks will be generated.
    """
    display_name = "Max Required Runecraft Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxRunecraftTasks(Range):
    """
    The maximum number of Runecraft Tasks to possibly be assigned.
    If set to 0, no Runecraft tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Runecraft Task Count"
    range_start = 0
    range_end = MAX_RUNECRAFT_TASKS
    default = MAX_RUNECRAFT_TASKS


class RunecraftTaskWeight(Range):
    """
    How much to favor generating Runecraft tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Runecraft Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxCraftingLevel(Range):
    """
    The highest Crafting requirement of any task generated.
    If set to 0, no Crafting tasks will be generated.
    """
    display_name = "Max Required Crafting Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxCraftingTasks(Range):
    """
    The maximum number of Crafting Tasks to possibly be assigned.
    If set to 0, no Crafting tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Crafting Task Count"
    range_start = 0
    range_end = MAX_CRAFTING_TASKS
    default = MAX_CRAFTING_TASKS


class CraftingTaskWeight(Range):
    """
    How much to favor generating Crafting tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Crafting Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxMiningLevel(Range):
    """
    The highest Mining requirement of any task generated.
    If set to 0, no Mining tasks will be generated.
    """
    display_name = "Max Required Mining Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxMiningTasks(Range):
    """
    The maximum number of Mining Tasks to possibly be assigned.
    If set to 0, no Mining tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Mining Task Count"
    range_start = 0
    range_end = MAX_MINING_TASKS
    default = MAX_MINING_TASKS


class MiningTaskWeight(Range):
    """
    How much to favor generating Mining tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Mining Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxSmithingLevel(Range):
    """
    The highest Smithing requirement of any task generated.
    If set to 0, no Smithing tasks will be generated.
    """
    display_name = "Max Required Smithing Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxSmithingTasks(Range):
    """
    The maximum number of Smithing Tasks to possibly be assigned.
    If set to 0, no Smithing tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Smithing Task Count"
    range_start = 0
    range_end = MAX_SMITHING_TASKS
    default = MAX_SMITHING_TASKS


class SmithingTaskWeight(Range):
    """
    How much to favor generating Smithing tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Smithing Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxFishingLevel(Range):
    """
    The highest Fishing requirement of any task generated.
    If set to 0, no Fishing tasks will be generated.
    """
    display_name = "Max Required Fishing Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxFishingTasks(Range):
    """
    The maximum number of Fishing Tasks to possibly be assigned.
    If set to 0, no Fishing tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Fishing Task Count"
    range_start = 0
    range_end = MAX_FISHING_TASKS
    default = MAX_FISHING_TASKS


class FishingTaskWeight(Range):
    """
    How much to favor generating Fishing tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Fishing Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxCookingLevel(Range):
    """
    The highest Cooking requirement of any task generated.
    If set to 0, no Cooking tasks will be generated.
    """
    display_name = "Max Required Cooking Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxCookingTasks(Range):
    """
    The maximum number of Cooking Tasks to possibly be assigned.
    If set to 0, no Cooking tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Cooking Task Count"
    range_start = 0
    range_end = MAX_COOKING_TASKS
    default = MAX_COOKING_TASKS


class CookingTaskWeight(Range):
    """
    How much to favor generating Cooking tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Cooking Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxFiremakingLevel(Range):
    """
    The highest Firemaking requirement of any task generated.
    If set to 0, no Firemaking tasks will be generated.
    """
    display_name = "Max Required Firemaking Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxFiremakingTasks(Range):
    """
    The maximum number of Firemaking Tasks to possibly be assigned.
    If set to 0, no Firemaking tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Firemaking Task Count"
    range_start = 0
    range_end = MAX_FIREMAKING_TASKS
    default = MAX_FIREMAKING_TASKS


class FiremakingTaskWeight(Range):
    """
    How much to favor generating Firemaking tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Firemaking Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MaxWoodcuttingLevel(Range):
    """
    The highest Woodcutting requirement of any task generated.
    If set to 0, no Woodcutting tasks will be generated.
    """
    display_name = "Max Required Woodcutting Level"
    range_start = 0
    range_end = 99
    default = 50


class MaxWoodcuttingTasks(Range):
    """
    The maximum number of Woodcutting Tasks to possibly be assigned.
    If set to 0, no Woodcutting tasks will be generated.
    This only determines the maximum possible, fewer than the maximum could be assigned.
    """
    display_name = "Max Woodcutting Task Count"
    range_start = 0
    range_end = MAX_WOODCUTTING_TASKS
    default = MAX_WOODCUTTING_TASKS


class WoodcuttingTaskWeight(Range):
    """
    How much to favor generating Woodcutting tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "Woodcutting Task Weight"
    range_start = 0
    range_end = 99
    default = 50


class MinimumGeneralTasks(Range):
    """
    How many guaranteed general progression tasks to be assigned (total level, total XP, etc.).
    General progression tasks will be used to fill out any holes caused by having fewer possible tasks than needed, so
    there is no maximum.
    """
    display_name = "Minimum General Task Count"
    range_start = 0
    range_end = NON_QUEST_LOCATION_COUNT
    default = 10


class GeneralTaskWeight(Range):
    """
    How much to favor generating General tasks over other types of task.
    Weights of all Task Types will be compared against each other, a task with 50 weight
    is twice as likely to appear as one with 25.
    """
    display_name = "General Task Weight"
    range_start = 0
    range_end = 99
    default = 50


@dataclass
class OSRSOptions(PerGameCommonOptions):
    starting_area: StartingArea
    brutal_grinds: BrutalGrinds
    progressive_tasks: ProgressiveTasks
    enable_duds: EnableDuds
    dud_count: DudCount
    enable_carepacks: EnableCarePacks
    max_combat_level: MaxCombatLevel
    max_combat_tasks: MaxCombatTasks
    combat_task_weight: CombatTaskWeight
    max_prayer_level: MaxPrayerLevel
    max_prayer_tasks: MaxPrayerTasks
    prayer_task_weight: PrayerTaskWeight
    max_magic_level: MaxMagicLevel
    max_magic_tasks: MaxMagicTasks
    magic_task_weight: MagicTaskWeight
    max_runecraft_level: MaxRunecraftLevel
    max_runecraft_tasks: MaxRunecraftTasks
    runecraft_task_weight: RunecraftTaskWeight
    max_crafting_level: MaxCraftingLevel
    max_crafting_tasks: MaxCraftingTasks
    crafting_task_weight: CraftingTaskWeight
    max_mining_level: MaxMiningLevel
    max_mining_tasks: MaxMiningTasks
    mining_task_weight: MiningTaskWeight
    max_smithing_level: MaxSmithingLevel
    max_smithing_tasks: MaxSmithingTasks
    smithing_task_weight: SmithingTaskWeight
    max_fishing_level: MaxFishingLevel
    max_fishing_tasks: MaxFishingTasks
    fishing_task_weight: FishingTaskWeight
    max_cooking_level: MaxCookingLevel
    max_cooking_tasks: MaxCookingTasks
    cooking_task_weight: CookingTaskWeight
    max_firemaking_level: MaxFiremakingLevel
    max_firemaking_tasks: MaxFiremakingTasks
    firemaking_task_weight: FiremakingTaskWeight
    max_woodcutting_level: MaxWoodcuttingLevel
    max_woodcutting_tasks: MaxWoodcuttingTasks
    woodcutting_task_weight: WoodcuttingTaskWeight
    minimum_general_tasks: MinimumGeneralTasks
    general_task_weight: GeneralTaskWeight
