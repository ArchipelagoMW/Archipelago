from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool, Toggle


class Goal(Choice):
    """Victory condition.

    all_mavericks: defeat all 8 Mavericks, then reach and defeat Sigma. The
    default, and the way most people want to play.

    sigma: defeat Sigma, however you got there. Mega Man X5 opens the endgame
    when the Eurasia colony situation resolves, and that can happen with only 6
    Mavericks down - so under this goal a run can legitimately finish without
    fighting all eight.

    launch: collect all 8 Enigma/Shuttle Parts and complete a successful
    launch (the client only powers a launch once every part is in hand -
    partial part sets always fail the launch, vanilla-style).
    """
    display_name = "Goal"
    option_sigma = 0
    option_launch = 1
    option_all_mavericks = 2
    default = 2


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


class TextSkip(Toggle):
    """Make dialogue get out of the way.

    Mega Man X5 types dialogue out one character every 5 frames and then waits
    for a button on every box. A single line can run past 200 characters, which
    is about 20 seconds of typing before you can even press advance.

    With this on, each box appears instantly and advances by itself, so
    cutscenes and Alia's in-stage calls play through without input.

    Choices are NOT skipped. Alia's Life Up / Energy Up reward prompt still
    stops and waits for you to pick, and the Enigma / Shuttle launch decision
    is a stage-select menu that this does not touch at all. Nothing that
    affects your run gets answered for you.

    You will not be able to read the story at this speed. Leave it off for a
    first playthrough.
    """
    display_name = "Text Skip"


@dataclass
class MMX5Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    boss_difficulty: BossDifficulty
    text_skip: TextSkip
