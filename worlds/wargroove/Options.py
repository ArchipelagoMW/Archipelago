from typing import Dict, Optional
from dataclasses import dataclass

from schema import Schema, And, Use

from Options import Choice, Range, PerGameCommonOptions, DeathLink, StartInventoryPool, OptionDict, OptionGroup

unit_trap_table: Dict[str, int] = {
    "Soldier": 0,
    "Dog": 0,
    "Spearman": 0,
    "Wagon": 0,
    "Mage": 0,
    "Archer": 0,
    "Knight": 0,
    "Ballista": 0,
    "Trebuchet": 0,
    "Golem": 0,
    "Harpy": 0,
    "Witch": 0,
    "Dragon": 0,
    "Balloon": 0,
    "Barge": 0,
    "Merfolk": 0,
    "Turtle": 0,
    "Harpoon Ship": 0,
    "Warship": 0,
    "Thief": 0,
    "Rifleman": 0
}

unit_trap_schema = Schema(
    {key: And(int, lambda value: 0 <= value <= 10)} for key in unit_trap_table.keys()
)

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

class CustomTrap1Amount(Range):
    """How many items of custom trap 1 are shuffled into the pool."""
    schema = unit_trap_schema
    display_name = "Custom Trap 1 Amount"
    range_start = 0
    range_end = 2
    default = 0

class CustomTrap1Units(OptionDict):
    """Custom units to deploy for a random enemy AI when a Custom Trap 1 is received."""
    schema = unit_trap_schema
    display_name = "Custom Trap 1 Units"
    valid_keys = unit_trap_table.keys()
    default = unit_trap_table

class CustomTrap2Amount(Range):
    """How many items of custom trap 2 are shuffled into the pool."""
    schema = unit_trap_schema
    display_name = "Custom Trap 2 Amount"
    range_start = 0
    range_end = 2
    default = 0

class CustomTrap2Units(OptionDict):
    """Custom units to deploy for a random enemy AI when a Custom Trap 2 is received."""
    schema = unit_trap_schema
    display_name = "Custom Trap 2 Units"
    valid_keys = unit_trap_table.keys()
    default = unit_trap_table

class CustomTrap3Amount(Range):
    """How many items of custom trap 3 are shuffled into the pool."""
    schema = unit_trap_schema
    display_name = "Custom Trap 3 Amount"
    range_start = 0
    range_end = 2
    default = 0

class CustomTrap3Units(OptionDict):
    """Custom units to deploy for a random enemy AI when a Custom Trap 3 is received."""
    schema = unit_trap_schema
    display_name = "Custom Trap 3 Units"
    valid_keys = unit_trap_table.keys()
    default = unit_trap_table

class CustomTrap4Amount(Range):
    """How many items of custom trap 4 are shuffled into the pool."""
    schema = unit_trap_schema
    display_name = "Custom Trap 4 Amount"
    range_start = 0
    range_end = 2
    default = 0

class CustomTrap4Units(OptionDict):
    """Custom units to deploy for a random enemy AI when a Custom Trap 4 is received."""
    schema = unit_trap_schema
    display_name = "Custom Trap 4 Units"
    valid_keys = unit_trap_table.keys()
    default = unit_trap_table

class CustomTrap5Amount(Range):
    """How many items of custom trap 5 are shuffled into the pool."""
    schema = unit_trap_schema
    display_name = "Custom Trap 5 Amount"
    range_start = 0
    range_end = 2
    default = 0

class CustomTrap5Units(OptionDict):
    """Custom units to deploy for a random enemy AI when a Custom Trap 5 is received."""
    schema = unit_trap_schema
    display_name = "Custom Trap 5 Units"
    valid_keys = unit_trap_table.keys()
    default = unit_trap_table

wargroove_option_groups = [
        OptionGroup("General Options", [
            IncomeBoost,
            CommanderDefenseBoost,
            CommanderChoice
        ]),
        # OptionGroup("Traps", [
        #     CustomTrap1Amount,
        #     CustomTrap1Units,
        #     CustomTrap2Amount,
        #     CustomTrap2Units,
        #     CustomTrap3Amount,
        #     CustomTrap3Units,
        #     CustomTrap4Amount,
        #     CustomTrap4Units,
        #     CustomTrap5Amount,
        #     CustomTrap5Units
        # ]),
]

@dataclass
class WargrooveOptions(PerGameCommonOptions):
    income_boost: IncomeBoost
    commander_defense_boost: CommanderDefenseBoost
    commander_choice: CommanderChoice
    # custom_trap_1_amount: CustomTrap1Amount
    # custom_trap_1_units: CustomTrap1Units
    # custom_trap_2_amount: CustomTrap2Amount
    # custom_trap_2_units: CustomTrap2Units
    # custom_trap_3_amount: CustomTrap3Amount
    # custom_trap_3_units: CustomTrap3Units
    # custom_trap_4_amount: CustomTrap4Amount
    # custom_trap_4_units: CustomTrap4Units
    # custom_trap_5_amount: CustomTrap5Amount
    # custom_trap_5_units: CustomTrap5Units
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
