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
    """Starting Boss Level, set via the frozen collision countdown.

    X5 scales boss HP (not attack patterns) with a Boss Level: a base from the
    countdown, plus 1 per Maverick defeated and per special weapon owned.
    Higher levels also unlock better post-boss rewards in-game.

    relaxed: base 1. Gentlest bosses; the better vanilla reward tiers arrive
    only late in the run.
    standard: base 9. Every boss offers the top vanilla reward tier.
    intense: base 17. Hardest bosses; top reward tier throughout.

    Any setting is safe for seed completion - Archipelago checks never depend
    on Boss Level (DNA locations are checked on the boss kill itself).
    """
    # Implementation: the client pins the countdown frames (relaxed 17 h,
    # standard 8 h, intense 1 h; hours-remaining -> base per the formula in
    # the research notes, mmx5-ram-notes.md). The base stays fixed all run
    # while the Maverick
    # and weapon terms still climb. "standard" reproduces the previously
    # hardcoded 8-hour pin.
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
