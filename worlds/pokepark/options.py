from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, OptionGroup


class Powers(Choice):
    """
    Determines how Power Items are shuffled into the pool.
    Full: Start with all Power Items
    Thunderbolt: Start with one Thunderbolt Power
    Dash: Start with one Dash Power
    ThunderboltDash: Start with one Thunderbolt and Dash Power (Default)
    None: Start with no Powers (Thunderbolt and Dash unusable)
    """
    display_name = "Powers"
    option_full = 0
    option_thunderbolt = 1
    option_dash = 2
    option_thunderbolt_dash = 3
    option_none = 4
    default = 3


class RandomStartingZones(Choice):
    """
    Determines Starting Zone
    Ice Zone: Start with the Ice Zone
    One: Start with one random Starting Zone
    None: Start with Meadow Zone (Default)
    """
    display = "Starting Zone"
    option_none = 0
    option_one = 1
    option_ice_zone = 2
    default = 0


class Goal(Choice):
    """
    Determines World completion condition
    Mew: Beat Mew (Default)
    aftergame: Complete the aftergame Prisma check (needs all friends). Adds aftergame pokemon and their minigames
    """
    display = "Goal Condition"
    option_mew = 0
    option_aftergame = 1


@dataclass
class PokeparkOptions(PerGameCommonOptions):
    power_randomizer: Powers
    starting_zone: RandomStartingZones
    goal: Goal


pokepark_option_groups = [
    OptionGroup("Goal", [
        Goal
    ]),
    OptionGroup("Misc", [
        Powers,
        RandomStartingZones
    ])
]
