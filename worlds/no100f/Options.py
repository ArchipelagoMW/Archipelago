from dataclasses import dataclass

from Options import Toggle, DeathLink, Range, Choice, PerGameCommonOptions, StartInventoryPool, DefaultOnToggle


class IncludeMonsterTokens(DefaultOnToggle):
    """Include Monster Tokens as AP Locations/Items"""
    display_name = "Include Monster Tokens"


class IncludeKeys(Choice):
    """Include Keys as AP Locations/Items"""
    display_name = "Include Keys"
    option_vanilla = 0
    option_keys = 1
    option_keyrings = 2
    default = 0


class IncludeWarpGates(Toggle):
    """Include Warp Gates as AP Locations/Items
    Additionally, to offset issues with snack gates, you will start with 400 Scooby Snacks
    """
    display_name = "Include Warp Gates"


class IncludeSnacks(Toggle):
    """Include Snacks as AP Locations/Items"""
    display_name = "Include Snacks"


class CompletionGoal(Choice):
    """
    Select which completion goal you want for this world:
    0 = Vanilla/Beat Mastermind
    1 = Bosses
    2 = Monster Tokens
    3 = Bosses/Tokens
    4 = Scooby Snacks
    5 = Snacks/Bosses
    6 = Snacks/Tokens
    7 = Bosses/Tokens/Snacks
    For Non-Vanilla options, Mastermind still needs to be defeated - you just can't fight him
    until the goal has been met Snack Clear Conditions will only work with Snacksanity Enabled
    """
    display_name = "Completion Goal"
    option_vanilla = 0
    option_bosses = 1
    option_tokens = 2
    option_bosses_tokens = 3
    option_snacks = 4
    option_bosses_snacks = 5
    option_tokens_snacks = 6
    option_bosses_tokens_snacks = 7
    default = 0


class BossesCount(Range):
    """Sets the number of bosses needed if Boss Completion Goal is being used"""
    display_name = "Boss Kills Count"
    range_start = 1
    range_end = 3
    default = 3


class MonsterTokensCount(Range):
    """Sets the number of tokens needed if Token Completion Goal is being used"""
    display_name = "Token Count"
    range_start = 1
    range_end = 21
    default = 21


class SnackCount(Range):
    """Sets the number of tokens needed if Token Completion Goal is being used"""
    display_name = "Snack Count"
    range_start = 1
    range_end = 5287
    default = 850


class AdvancedLogic(Toggle):
    """Changes generation to expect certain tricks to be performed, intended for experienced players"""
    display_name = "Advanced Logic"
    default = 0


class ExpertLogic(Toggle):
    """Changes generation to expect certain tricks to be performed, intended for even MORE experienced players"""
    display_name = "Expert Logic"
    default = 0


class CreepyEarly(Toggle):
    """Changes generation to expect certain tricks to be performed (CREEPY EARLY [GCN]),
    intended for less sane players"""
    display_name = "Creepy Early"
    default = 0


class Speedster(Toggle):
    """For Fun Setting, permanently makes scooby move at mach speed"""
    display_name = "Speedster"
    default = 0


@dataclass
class NO100FOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    include_monster_tokens: IncludeMonsterTokens
    include_keys: IncludeKeys
    include_warpgates: IncludeWarpGates
    include_snacks: IncludeSnacks
    death_link: DeathLink
    completion_goal: CompletionGoal
    boss_count: BossesCount
    token_count: MonsterTokensCount
    snack_count: SnackCount
    advanced_logic: AdvancedLogic
    expert_logic: ExpertLogic
    creepy_early: CreepyEarly
    speedster: Speedster
