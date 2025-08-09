from dataclasses import dataclass
from typing import Any

from Options import PerGameCommonOptions, Choice, OptionGroup, Range


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


class NumRequiredBattleCount(Range):
    """
    Select the number of required consecutive Wins to challenge Battle count Pokemon.
    """
    display = "Number of Battle Count"
    range_start = 0
    range_end = 10
    default = 5


@dataclass
class PokeparkOptions(PerGameCommonOptions):
    power_randomizer: Powers
    starting_zone: RandomStartingZones
    goal: Goal
    num_required_battle_count: NumRequiredBattleCount

    def get_output_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary of option name to value to be placed in
        the output pprk file.

        :return: Dictionary of option name to value for the output file.
        """

        # Note: these options' values must be able to be passed through
        # `yaml.safe_dump`.
        return self.as_dict(
            "num_required_battle_count",
        )


pokepark_option_groups = [
    OptionGroup("Goal", [
        Goal
    ]),
    OptionGroup("Misc", [
        Powers,
        RandomStartingZones,
        NumRequiredBattleCount
    ])
]
