from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool


class Goal(Choice):
    """Victory condition.

    sigma: reach and defeat Sigma after defeating all 8 Mavericks.
    launch: collect all 8 Enigma/Shuttle Parts and complete a successful
    launch (the client only powers a launch once every part is in hand -
    partial part sets always fail the launch, vanilla-style).
    """
    display_name = "Goal"
    option_sigma = 0
    option_launch = 1
    default = 0


class BossDifficulty(Choice):
    """How hard bosses start out.

    Mega Man X5 scales bosses with a "Boss Level" derived from how many hours
    remain on the colony countdown. The randomizer freezes that countdown, so
    this option chooses what it freezes at - which fixes where the difficulty
    curve begins.

    relaxed: 17 hours remaining, starting Boss Level 1. The gentlest bosses.
    standard: 8 hours remaining, starting Boss Level 9. The default.
    intense: 1 hour remaining, starting Boss Level 17. The hardest bosses.

    Note that FEWER hours means a HIGHER level - the game ramps up as the
    crisis deepens, so "intense" is the one-hour setting.

    Boss Level scales boss HP, not their attack patterns, so higher settings
    make fights longer rather than smarter. It also decides the reward a boss
    gives in the original game: level 4+ offers the Life Up / Energy Up
    choice, and level 8+ upgrades that and adds an equippable Part. On
    "standard" you are past both thresholds from the very first fight; on
    "relaxed" they arrive partway through the run.

    Whatever you pick, the level still climbs as you play - +1 for each
    Maverick defeated and each special weapon you own, recalculated when you
    enter a stage. This only sets the starting point.

    This can never make a seed unbeatable: Archipelago's checks do not depend
    on Boss Level. The DNA reward locations are checked when the boss dies
    rather than when the reward appears, precisely so a low setting cannot
    make them unobtainable.
    """
    # Implementation: the client pins the countdown in frames (relaxed 17 h,
    # standard 8 h, intense 1 h); hours-remaining -> base follows the formula
    # in the research notes, mmx5-ram-notes.md. The base stays fixed all run
    # while the Maverick and weapon terms still climb. "standard" reproduces
    # the 8-hour pin the world used before this became an option.
    display_name = "Boss Difficulty"
    option_relaxed = 0
    option_standard = 1
    option_intense = 2
    default = 1


@dataclass
class MMX5Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    boss_difficulty: BossDifficulty
