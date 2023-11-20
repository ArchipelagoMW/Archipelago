from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Toggle


class Goal(Choice):
    """
    Determines the victory condition

    Three Artifacts: Retrieve the three artifacts of magic and place them in the walking castle
    """
    display_name = "Goal"

    default = 0
    option_three_artifacts = 0


class EarlyRopeAndLantern(DefaultOnToggle):
    """If true, the rope and lantern will be found in early locations for a smoother early game"""

    display_name = "Early Rope & Lantern"


class Deathsanity(Toggle):
    """If true, adds 16 player death locations to the world"""

    display_name = "Deathsanity"


@dataclass
class ZorkGrandInquisitorOptions(PerGameCommonOptions):
    goal: Goal
    early_rope_and_lantern: EarlyRopeAndLantern
    deathsanity: Deathsanity
