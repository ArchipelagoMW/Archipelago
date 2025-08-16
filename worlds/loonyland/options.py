from dataclasses import dataclass

from Options import Choice, DeathLink, PerGameCommonOptions, Range


class WinCondition(Choice):
    """**Evilizer**: Beat the final boss

    **Badges**: Get X merit badges earned"""

    #NOT IMPLEMENTED: normal_remix: Beat the final boss in normal and remix"""

    display_name = "Win Condition"
    option_evilizer = 0
    option_badges = 1
    # option_normal_remix = 2
    default = 0


class BadgesRequired(Range):
    """For the Badges win con, how many badges are needed"""

    display_name = "Badges Required"
    range_start = 1
    range_end = 40
    default = 30


class Difficulty(Choice):
    """Difficulty Setting"""

    display_name = "Difficulty"
    option_beginner = 0
    option_normal = 1
    option_hard = 5
    option_challenge = 2
    option_mad = 3
    option_loony = 4
    default = 1


class LongChecks(Choice):
    """**Excluded**: Remove 100%, 39 badges, swampdog to 50, witch to lvl 9 spells, 5000 gems,
    the monster point badges, a true hero

    Does nothing if badges are already set to none
    """

    display_name = "Long Checks"
    option_excluded = 0
    option_included = 1
    default = 0


class MultipleSaves(Choice):
    """**Disabled**: Remove badges that require using certain characters/terror mode in adventure mode,
    removes all "takes effect on new game" cheats"""

    display_name = "Multiple Saves"
    option_disabled = 0
    option_enabled = 1
    default = 0


class Remix(Choice):
    """**Excluded**: Remix mode not included"""

    display_name = "Remix"
    option_excluded = 0
    option_included = 1
    default = 0


class OverpoweredCheats(Choice):
    """**Excluded**: Removes Walk Through Walls, Infinite health, Touch of Death

    Also disables Brawlin' as a location, since it requires Touch of Death"""

    display_name = "Overpowered Cheats"
    option_excluded = 0
    option_included = 1
    default = 0


class Badges(Choice):
    """**Full**: All badges and their cheats are in logic

    **Vanilla**: Badges aren't randomized, but are in logic

    **None**: Badges aren't in logic"""

    display_name = "Badges"
    option_none = 0
    option_vanilla = 1
    option_full = 2
    default = 2


class MonsterDolls(Choice):
    """**Full**: Monsters can drop randomized items, monster dolls can be found at locations

    **Vanilla**: Monsters drop their normal monster doll

    **None**: Dolls aren't in logic, the collection quest gives nothing"""

    display_name = "Monster Dolls"
    option_none = 0
    option_vanilla = 1
    option_full = 2
    default = 2


@dataclass
class LoonylandOptions(PerGameCommonOptions):
    win_condition: WinCondition
    badges_required: BadgesRequired
    difficulty: Difficulty
    long_checks: LongChecks
    multisave: MultipleSaves
    remix: Remix
    overpowered_cheats: OverpoweredCheats
    badges: Badges
    dolls: MonsterDolls
    death_link: DeathLink
