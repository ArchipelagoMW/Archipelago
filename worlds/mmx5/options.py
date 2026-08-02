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
    """Boss Level base, set by pinning the collision countdown.

    X5 computes Boss Level as: a BASE from hours remaining on the countdown,
    +1 per Maverick defeated, +1 per special weapon owned, plus a Hunter Rank
    bonus - recalculated at the start of every stage. It scales boss HP (not
    attack patterns) and gates the post-boss reward: level 4+ gives the
    Life/Energy Up choice, level 8+ gives Life+/Energy+ AND an equippable Part.

    The client pins the countdown, so the BASE is fixed for the whole run while
    the Maverick and weapon terms still climb - bosses still get stronger as
    you progress, they just start from the base you pick here.

    relaxed: 17 hours -> base 1. Gentlest bosses; the Life/Energy Up choice
    only starts appearing once you have a few Mavericks and weapons, and the
    Part tier arrives late.
    standard: 8 hours -> base 9. Every boss offers the top reward tier from the
    very first fight. (This was the previous hardcoded behaviour.)
    intense: 1 hour -> base 17. Hardest bosses; top reward tier throughout.

    Note: AP checks never depend on this - the DNA reward locations are checked
    when the boss dies, not when the reward prompt appears - so any setting is
    safe for seed completion. It changes difficulty and vanilla stat pacing.
    """
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
