from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions


class Goal(Choice):
    """
    Determines the main completion goal.

    Currently only Lance is supported. More goals can be added later,
    such as Red or all 16 badges.
    """

    display_name = "Goal"

    option_lance = 0

    default = 0


class HMBadgeRequirements(DefaultOnToggle):
    """
    Determines whether HMs require their matching badge in logic.

    When enabled, Surf requires both HM03 Surf and Fog Badge.
    When disabled, Surf only requires HM03 Surf.
    """

    display_name = "HM Badge Requirements"


@dataclass
class PokemonHGSSOptions(PerGameCommonOptions):
    goal: Goal
    hm_badge_requirements: HMBadgeRequirements