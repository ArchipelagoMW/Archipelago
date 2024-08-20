from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions


class Goal(Choice):
    """The victory condition for your run. Stuff after the goal will not be shuffled."""

    display_name = "Goal"
    option_mechanical_bosses = 0
    # option_calamitas_clone = 1
    option_plantera = 2
    option_golem = 3
    option_empress_of_light = 4
    option_lunatic_cultist = 5
    # option_astrum_deus = 6
    option_moon_lord = 7
    # option_providence_the_profaned_goddess = 8
    # option_devourer_of_gods = 9
    # option_yharon_dragon_of_rebirth = 10
    option_zenith = 11
    # option_calamity_final_bosses = 12
    # option_adult_eidolon_wyrm = 13
    default = 0


class Achievements(Choice):
    """
    Adds checks upon collecting achievements. Achievements for clearing bosses and events are excluded.
    "Exclude Grindy" also excludes fishing achievements.
    """

    display_name = "Achievements"
    option_none = 0
    option_exclude_grindy = 1
    option_exclude_fishing = 2
    option_all = 3
    default = 1


class FillExtraChecksWith(Choice):
    """
    Applies if you have achievements enabled. "Useful Items" helps to make the early game less grindy.
    Items are rewarded to all players in your Terraria world.
    """

    display_name = "Fill Extra Checks With"
    option_coins = 0
    option_useful_items = 1
    default = 1


@dataclass
class TerrariaOptions(PerGameCommonOptions):
    goal: Goal
    achievements: Achievements
    fill_extra_checks_with: FillExtraChecksWith
    death_link: DeathLink
