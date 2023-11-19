from dataclasses import dataclass

from Options import Toggle, DefaultOnToggle, PerGameCommonOptions


class EarlyRopeAndLantern(DefaultOnToggle):
    """If true, the rope and lantern will be found in early locations for a smoother early game"""

    display_name = "Early Rope & Lantern"


class SkipOldScratchMinigame(Toggle):
    """If true, allows the player to simply click on the winning square on the Old Scratch card instead of having to
    find the correct path"""

    display_name = "Skip Old Scratch Minigame"


class Deathsanity(Toggle):
    """If true, adds 17 player death locations to the world"""

    display_name = "Deathsanity"


@dataclass
class ZorkGrandInquisitorOptions(PerGameCommonOptions):
    early_rope_and_lantern: EarlyRopeAndLantern
    skip_old_scratch_minigame: SkipOldScratchMinigame
    deathsanity: Deathsanity
