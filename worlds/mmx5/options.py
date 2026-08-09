from dataclasses import dataclass

from Options import (Choice, DefaultOnToggle, PerGameCommonOptions,
                     StartInventoryPool, Toggle)


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


class LaunchOdds(Choice):
    """Whether a launch is a sure thing or a gamble.

    deterministic: the launch succeeds exactly when you hold all 8 Enigma and
    Shuttle Parts, and fails otherwise. No dice. The default.

    vanilla: restores the original game's gamble - more parts means better
    odds, but never certainty. Mega Man X5 rolls against a score derived from
    the parts you hold:

      Enigma   - no parts 6.25%, any parts 12.5% (extra Enigma parts add
                 nothing in the original game either)
      Shuttle  - no parts 12.5%, 1-2 parts 37.5%, 3-4 parts 75%

    WARNING - under the `launch` goal this can make a seed unwinnable. That
    goal needs a SUCCESSFUL launch, you only get two attempts (the Enigma,
    then the Shuttle), and even a full set of parts tops out at 75%. Fail both
    and the colony falls with no third chance. This combination is allowed on
    purpose, but it is a real gamble with your whole run, not a difficulty
    slider.

    Under the `all_mavericks` goal no launch can succeed before all 8 Mavericks
    are down, whatever this is set to - otherwise an early success would open
    the endgame ahead of the goal.
    """
    display_name = "Launch Odds"
    option_deterministic = 0
    option_vanilla = 1
    default = 0


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


class SecretArmorsInPool(Toggle):
    """Add Ultimate Armor and Black Zero to the item pool.

    In the base game both come from a single hidden capsule in Zero Space, so
    you only ever see them right at the end. With this on they are shuffled
    into the multiworld and can turn up at any point in the run.

    Ultimate Armor is X's (unlimited Giga Attack, air dash in any direction);
    Black Zero is Zero's (stronger, faster, and his Z-Saber techniques cost no
    weapon energy). Each only does anything for its own character, so on a
    seed where you stick to one of them the other is dead weight - they are
    never required for anything.

    The Zero Space capsule still works normally, so you can also just find
    them the vanilla way. Receiving an armor first makes that capsule vanish,
    since the game hides a capsule whose armor you already have.

    The two arrive on different schedules: Ultimate Armor shows up at your next
    stage entry, not in the stage you are standing in when it arrives, because
    the game decides which armor X wears as the stage loads. Black Zero applies
    on the spot.
    """
    display_name = "Secret Armors In Pool"


class BossHPRandomization(Choice):
    """Randomize how much HP bosses have.

    Every boss is affected - Mavericks, mid-bosses, Dynamo, Sigma, the Zero
    duel. The roll SCALES what the game would normally give, so Boss Level
    still matters: a tough setting on `intense` boss difficulty compounds.

    off: bosses keep their normal HP
    weak: 40-80% of normal
    regular: 70-130% of normal
    strong: 120-200% of normal
    chaotic: 25-250% of normal

    Each stage rolls once per visit, and the roll is fixed for a given seed
    and situation - dying and retrying gives you the same fight. Bosses met
    during the same visit to a stage (a mid-boss and the stage boss) share
    that stage's roll.

    HP is capped at 127 by the game, so very high rolls on a late-game boss
    can hit that ceiling and come out lower than the multiplier suggests.
    """
    display_name = "Boss HP Randomization"
    option_off = 0
    option_weak = 1
    option_regular = 2
    option_strong = 3
    option_chaotic = 4
    default = 0


class PickupSanity(Toggle):
    """Freestanding pickups become checks.

    Every loose Life Energy, Weapon Energy and 1-UP capsule sitting in a stage
    becomes an Archipelago location - 32 in total, including the ones in Zero
    Space and Sigma's stage. Energy dropped by defeated enemies is unaffected.

    On these seeds a freestanding capsule no longer restores anything when
    touched: collecting it sends its check instead, and the energy it held is
    in the item pool as filler. A capsule keeps respawning until its check is
    confirmed, so nothing is lost to a drop or disconnect.

    The intro stage's single capsule is deliberately NOT a location - the
    intro cannot be revisited, which would make it permanently missable.
    """
    display_name = "Pickupsanity"


class StageUnlocks(Toggle):
    """Lock the eight Maverick stages behind items.

    Normally all eight are open from the moment the intro ends. With this on
    exactly ONE of them is open at the start - which one is decided by the seed
    - and each of the others needs its own "<Boss> Access Codes" item, shuffled
    into the multiworld like anything else.

    A locked stage still shows on the stage-select screen and the cursor still
    moves onto it; pressing confirm simply does nothing until you hold its
    codes. Nothing else about the screen changes - the countdown, the
    Enigma/Shuttle/Zero Space entry and the endgame all behave exactly as they
    normally would.

    Client-side, so it needs no disc change and works on a disc you have
    already patched.
    """
    display_name = "Stage Unlocks"


class RandomizeOptions(Toggle):
    """Let the seed pick your gameplay options for you.

    Rolls `goal`, `boss_difficulty`, `launch_odds`, `text_skip`,
    `pickupsanity`, `boss_hp_randomization`, `secret_armors_in_pool`,
    `stage_unlocks` and `dna_parts_in_pool`. Whatever you wrote for those in
    your YAML is ignored. `endgame_checks` is left alone — it only ever adds
    checks, so there is nothing to gamble on.

    Two combinations are corrected after the roll, because they are traps
    rather than interesting outcomes:

    - `launch` goal with vanilla launch odds can produce a seed nobody can
      finish (two attempts, 75% at best), so the odds are forced back to
      deterministic if the goal lands on `launch`.
    - If the options rolled add more items than the seed has locations,
      `pickupsanity` is switched on to make room rather than failing.

    The result is written to the spoiler log, so you can see what you got.

    Note this can turn on options that change the disc (`pickupsanity`,
    `text_skip`, `launch_odds`), so patch your disc from the generated file
    rather than reusing an old one.
    """
    display_name = "Randomize Options"


class DNAPartsInPool(Choice):
    """Shuffle the equippable DNA Parts into the item pool.

    Mega Man X5 has 16 Parts, but a normal playthrough only ever yields 8 of
    them: each Maverick offers two — one for Life+, one for Energy+ — and
    Alia's prompt makes you give up the other permanently.

    off: Parts work like the base game.

    vanilla_pairs: the seed picks one Part from each boss's pair and shuffles
    those 8 into the multiworld, mirroring vanilla's 8-of-16 economy — the
    Part you end up with has nothing to do with which prompt you answered.
    (`true` in an older YAML means this.)

    all: every one of the 16 Parts enters the pool, including both halves of
    each pair — something the base game never allows. This adds 16 items
    instead of 8, so the seed needs the location budget for it: turn on
    `rematch_checks` and/or `pickupsanity` to make room.

    The Parts the game would have handed you are suppressed, so Parts arrive
    only from the multiworld. The "DNA Part" locations are unchanged and still
    check on the boss kill.

    Six Parts only do anything for one character (Burst Shots, Ultimate Buster
    and Quick Charge are X's; Z-Saber Plus, Z-Saber Extend and Shot Eraser are
    Zero's), so none of them is ever required for anything — on a run played as
    one character the other's are dead weight.

    Client-side, so it needs no disc change.
    """
    display_name = "DNA Parts In Pool"
    option_off = 0
    option_vanilla_pairs = 1
    option_all = 2
    alias_false = 0
    alias_true = 1
    default = 0


class EndgameChecks(DefaultOnToggle):
    """Clearing a Zero Space stage sends a check.

    Adds three locations — Zero Space 1, Zero Space 2 and the X vs Zero fight.
    Without this the entire endgame contains nothing to find: every check in a
    normal seed sits in the eight Maverick stages, so the last stretch of the
    run is pure travel.

    Sigma himself is not a location, because beating him is the goal.

    Client-side, so it needs no disc change.
    """
    display_name = "Endgame Checks"


class RematchChecks(Toggle):
    """Boss Rush rematch kills send checks.

    Adds eight locations, one per Maverick, for defeating their rematch in
    Zero Space's Boss Rush. Together with Endgame Checks this gives the last
    stretch of a run something to find - and it finally makes the rush pay
    for its trouble, which is the most-requested thing testers have asked for.

    Nothing is ever lost in the rush: a killed rematch's teleporter stays
    closed for the rest of that visit, but leaving the stage and re-entering
    resets all eight, so a check you missed (or a fight you lost) can always
    be redone.

    Client-side, so it needs no disc change.

    NEW in this release: the detection mechanism is live-verified for three
    of the eight bosses so far. An unrecognized fight sends nothing rather
    than guessing, so the worst a surprise can do is leave a rematch check
    uncollected until the following release - consider that before placing
    must-have progression on these on a race seed.
    """
    display_name = "Rematch Checks"


class ReploidChecks(Toggle):
    """Rescuing an injured Reploid sends a check.

    Adds 14 locations: 6 in Squid Adler, 3 in Izzy Glow, 5 in The Skiver -
    the yellow injured Reploids you walk into for an extra life. (Duff
    McWhalen's submarine also spits out Reploids, but those are conjured by
    the mid-boss rather than placed in the stage, so they are not checks.)

    Reploids reappear every time you re-enter a stage, so nothing is ever
    permanently missed. One quirk to know: a rescue at the 9-life cap cannot
    be detected (the game has no room to count it) - if that happens, re-enter
    the stage with fewer than 9 lives and rescue again.

    Client-side, so it needs no disc change.

    NEW in this release: Izzy Glow's and The Skiver's Reploids are verified
    on-screen; Squid Adler's six are shipped from disc data with the same
    signature but without an eyeball on each. If one of them misbehaves it
    will be fixed in a release - flag it if you see it.
    """
    display_name = "Reploid Checks"


# Options RandomizeOptions rolls. endgame_checks is deliberately absent (it
# only adds checks) and so are start_inventory_from_pool and randomize_options
# itself, and rematch_checks / reploid_checks for the same only-adds-checks
# reason. Kept next to the option so the two cannot drift apart.
RANDOMIZED_OPTIONS = (
    "goal", "boss_difficulty", "launch_odds", "text_skip", "pickupsanity",
    "boss_hp_randomization", "secret_armors_in_pool", "stage_unlocks",
    "dna_parts_in_pool",
)


@dataclass
class MMX5Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    randomize_options: RandomizeOptions
    goal: Goal
    boss_difficulty: BossDifficulty
    launch_odds: LaunchOdds
    text_skip: TextSkip
    pickupsanity: PickupSanity
    boss_hp_randomization: BossHPRandomization
    secret_armors_in_pool: SecretArmorsInPool
    stage_unlocks: StageUnlocks
    endgame_checks: EndgameChecks
    rematch_checks: RematchChecks
    reploid_checks: ReploidChecks
    dna_parts_in_pool: DNAPartsInPool

