from dataclasses import dataclass
from Options import Choice, Range, PerGameCommonOptions, StartInventoryPool, OptionDict, OptionGroup, \
    DeathLinkMixin


class IncomeBoost(Range):
    """How much extra income the player gets per turn per boost received."""
    display_name = "Income Boost"
    range_start = 0
    range_end = 100
    default = 25


class CommanderDefenseBoost(Range):
    """How much extra defense the player's commander gets per boost received."""
    display_name = "Commander Defense Boost"
    range_start = 0
    range_end = 8
    default = 2


class CommanderChoice(Choice):
    """How the player's commander is selected for missions.
    Locked Random: The player's commander is randomly predetermined for each level.
    Unlockable Factions: The player starts with Mercival and can unlock playable factions.
    Random Starting Faction:  The player starts with a random starting faction and can unlock the rest.
    When playing with unlockable factions, faction items are added to the pool.
    Extra faction items after the first also reward starting Groove charge."""
    display_name = "Commander Choice"
    option_locked_random = 0
    option_unlockable_factions = 1
    option_random_starting_faction = 2


class PlayerSacrificeLimit(Range):
    """How many times the player can sacrifice a unit at the Stronghold per level attempt.
    Sacrificed units are stored in the multiworld for other players to summon."""
    display_name = "Player Sacrifice Limit"
    range_start = 0
    range_end = 5
    default = 0


class PlayerSummonLimit(Range):
    """How many times the player can summon a unit at the Stronghold per level attempt.
    Summoned units are from the multiworld which were sacrificed by other players."""
    display_name = "Player Summon Limit"
    range_start = 0
    range_end = 5
    default = 0


class AISacrificeLimit(Range):
    """How many times the AI can sacrifice a unit at the Stronghold per level attempt.
    Sacrificed units are stored in the multiworld for other AIs to summon."""
    display_name = "AI Sacrifice Limit"
    range_start = 0
    range_end = 5
    default = 0


class AISummonLimit(Range):
    """How many times the AI can summon a unit at the Stronghold per level attempt.
    Summoned units are from the multiworld which were sacrificed by other AIs.
    AI summoning can be overwhelming, use /sacrifice_summon in the client if a level becomes impossible."""
    display_name = "AI Summon Limit"
    range_start = 0
    range_end = 5
    default = 0


wargroove_option_groups = [
        OptionGroup("General Options", [
            IncomeBoost,
            CommanderDefenseBoost,
            CommanderChoice
        ]),
        OptionGroup("Sacrifice and Summon Options", [
            PlayerSacrificeLimit,
            PlayerSummonLimit,
            AISacrificeLimit,
            AISummonLimit,
        ]),
]

@dataclass
class WargrooveOptions(DeathLinkMixin, PerGameCommonOptions):
    income_boost: IncomeBoost
    commander_defense_boost: CommanderDefenseBoost
    commander_choice: CommanderChoice
    player_sacrifice_limit: PlayerSacrificeLimit
    player_summon_limit: PlayerSummonLimit
    ai_sacrifice_limit: AISacrificeLimit
    ai_summon_limit: AISummonLimit
    start_inventory_from_pool: StartInventoryPool
